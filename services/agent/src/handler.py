import json
from agent_core import answer

def lambda_handler(event, context):
    q = None
    if isinstance(event, dict):
        q = event.get("query")
        if not q and "body" in event and isinstance(event["body"], str):
            try:
                q = json.loads(event["body"]).get("query")
            except Exception:
                pass

    if not q:
        q = "health"

    result = answer(q)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "query": q,
            **(result if isinstance(result, dict) else {"ok": True, "result": {"answer": str(result)}})
        })
    }
