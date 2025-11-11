import os, json, sys, boto3, botocore

MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
REGION   = os.getenv("AWS_REGION", "us-east-1")

client = boto3.client("bedrock-runtime", region_name=REGION)

def ask(prompt: str) -> str:
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        "system": "You are helpful!",
    }

    resp = client.invoke_model(modelId=MODEL_ID, body=json.dumps(body))
    data = json.loads(resp["body"].read())
    return data["content"][0]["text"]

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "Say hello!"
    try:
        print(ask(q))
    except botocore.exceptions.ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in {"AccessDeniedException", "ValidationException"}:
            print(f"[Bedrock error: {code}] Check: model access enabled, region={REGION}, profile creds valid.")
        else:
            print(f"[Error] {e}")