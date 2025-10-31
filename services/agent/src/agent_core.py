import csv
from pathlib import Path

DATA_PATH = Path("data/transactions.csv")

def load_transactions(file_path: Path = DATA_PATH):
    try:
        with open(file_path, newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

def answer(query: str) -> str:
    txns = load_transactions()
    if not txns:
        return "No data found. Add data/transactions.csv first."

    q = query.lower()
    if "total" in q:
        total = sum(float(t["amount"]) for t in txns)
        return f"Total transaction amount: ${total:.2f}"
    if "count pending" in q or "pending count" in q:
        return f"Pending transactions: {sum(1 for t in txns if t.get('status','').lower()=='pending')}"
    if "count" in q:
        return f"Number of transactions: {len(txns)}"
    return "Supported: 'total', 'count', 'count pending'."
