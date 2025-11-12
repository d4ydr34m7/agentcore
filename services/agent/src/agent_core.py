import csv
from pathlib import Path
from config import get_cfg
from bedrock_client import llm_ask

def load_transactions(file_path: Path):
    try:
        with open(file_path, newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def answer(query: str) -> str:
    cfg = get_cfg()
    txns = load_transactions(Path(cfg["data_path"]))

    q = query.lower().strip()
    # cheap/local skills first
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
