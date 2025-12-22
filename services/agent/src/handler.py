import json
from agent_core import answer

def lambda_handler(event, context):
    q = None

    if isinstance(event, dict):
        q = event.get("query")

        if not q and "body" in event and isinstance(event["body"], str):
            try:
                body = json.loads(event["body"])
                q = body.get("query")
            except Exception:
                pass

    if not q:
        q = "count"

    resp = answer(q)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"answer": resp})
    }
