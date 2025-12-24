import csv
import io
from collections import Counter
import boto3

from config import get_cfg
from bedrock_client import llm_ask

s3 = boto3.client("s3")

def load_transactions_s3(bucket: str, key: str):
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        body = obj["Body"].read().decode("utf-8")
        return list(csv.DictReader(io.StringIO(body)))
    except Exception:
        return []

def _to_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default

def answer(query: str):
    """
    Returns a STRUCTURED result (dict), not a plain string.
    handler.py will wrap it into the final HTTP response.
    """
    cfg = get_cfg()
    bucket = cfg["data_bucket"]
    key = cfg["data_key"]
    txns = load_transactions_s3(bucket, key)

    q = (query or "").lower().strip()

    # Helpful metadata for every response
    source = {"bucket": bucket, "key": key, "rows": len(txns)}

    # No data cases
    if not txns and any(x in q for x in ["total", "count", "summary", "top", "sum", "health"]):
        return {
            "ok": False,
            "message": "No data found. Upload data/transactions.csv to S3.",
            "source": source
        }

    # HEALTHCHECK
    if q in ["health", "healthcheck", "status"]:
        return {
            "ok": True,
            "message": "ok",
            "source": source
        }

    # SUMMARY
    if "summary" in q and txns:
        amounts = [_to_float(t.get("amount")) for t in txns]
        total = sum(amounts)
        avg = total / len(amounts) if amounts else 0.0
        return {
            "ok": True,
            "result": {
                "count": len(txns),
                "total_amount": round(total, 2),
                "avg_amount": round(avg, 2),
                "min_amount": round(min(amounts), 2) if amounts else 0.0,
                "max_amount": round(max(amounts), 2) if amounts else 0.0,
            },
            "source": source
        }

    # COUNT (overall or by type/status)
    if "count" in q and txns:
        if "deposit" in q:
            return {"ok": True, "result": {"count_deposits": sum(1 for t in txns if (t.get("type","").lower()=="deposit"))}, "source": source}
        if "withdrawal" in q:
            return {"ok": True, "result": {"count_withdrawals": sum(1 for t in txns if (t.get("type","").lower()=="withdrawal"))}, "source": source}
        if "pending" in q:
            return {"ok": True, "result": {"count_pending": sum(1 for t in txns if (t.get("status","").lower()=="pending"))}, "source": source}
        return {"ok": True, "result": {"count": len(txns)}, "source": source}

    # TOTAL / SUM (overall or by type)
    if ("total" in q or "sum" in q) and txns:
        if "deposit" in q:
            total = sum(_to_float(t.get("amount")) for t in txns if (t.get("type","").lower()=="deposit"))
            return {"ok": True, "result": {"sum_deposits": round(total, 2)}, "source": source}
        if "withdrawal" in q:
            total = sum(_to_float(t.get("amount")) for t in txns if (t.get("type","").lower()=="withdrawal"))
            return {"ok": True, "result": {"sum_withdrawals": round(total, 2)}, "source": source}

        total = sum(_to_float(t.get("amount")) for t in txns)
        return {"ok": True, "result": {"total_amount": round(total, 2)}, "source": source}

    # TOP TYPES
    if ("top" in q and "type" in q) or ("top types" in q):
        types = [t.get("type","").lower().strip() or "unknown" for t in txns]
        c = Counter(types).most_common(5)
        return {"ok": True, "result": {"top_types": [{"type": k, "count": v} for k, v in c]}, "source": source}

    # TOP MERCHANTS
    if ("top" in q and "merchant" in q) or ("top merchants" in q):
        merchants = [t.get("merchant","").strip() or "unknown" for t in txns]
        c = Counter(merchants).most_common(5)
        return {"ok": True, "result": {"top_merchants": [{"merchant": k, "count": v} for k, v in c]}, "source": source}

    # Fall back to Bedrock (for natural language)
    if cfg.get("use_bedrock", False):
        text = llm_ask(query, cfg["model_id"], cfg["region"])
        return {"ok": True, "result": {"llm_answer": text}, "source": source}

    return {
        "ok": False,
        "message": "Try: count | total | summary | count deposits | sum withdrawals | top types | top merchants | health",
        "source": source
    }
