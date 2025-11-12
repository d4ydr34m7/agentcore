import json, boto3
from pathlib import Path

def load_system_prompt(path=Path("services/agent/prompts/system.md")) -> str:
    return path.read_text().strip() if path.exists() else "You are helpful and concise."

def llm_ask(prompt: str, model_id: str, region: str) -> str:
    client = boto3.client("bedrock-runtime", region_name=region)
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        "system": load_system_prompt(),
    }
    resp = client.invoke_model(modelId=model_id, body=json.dumps(body))
    data = json.loads(resp["body"].read())
    return data["content"][0]["text"]
