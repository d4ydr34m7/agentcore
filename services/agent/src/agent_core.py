import csv
import io
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

def answer(query: str) -> str:
    cfg = get_cfg()
    txns = load_transactions_s3(cfg["data_bucket"], cfg["data_key"])
    q = query.lower().strip()
   
    if "total" in q and txns:
        total = sum(float(t["amount"]) for t in txns)
        return f"Total transaction amount: ${total:.2f}"
    if ("count pending" in q or "pending count" in q) and txns:
        return f"Pending transactions: {sum(1 for t in txns if t.get('status','').lower()=='pending')}"
    if "count" in q and txns:
        return f"Number of transactions: {len(txns)}"
    if not txns and any(x in q for x in ["total","count"]):
        return "No data found. Add data/transactions.csv first."

    # fall back to Bedrock for natural questions
    if cfg.get("use_bedrock", False):
        return llm_ask(query, cfg["model_id"], cfg["region"])

    return "No matching local skill. Enable Bedrock or ask 'total'/'count'."
