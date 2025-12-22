import os
from pathlib import Path

def get_cfg():
    return {
        "env": os.getenv("ENV", "dev"),
        "model_id": os.getenv("MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
        "region": os.getenv("AWS_REGION", "us-east-1"),

        # S3 location for your CSV
        "data_bucket": os.getenv("DATA_BUCKET", "agentcore-dev-data"),
        "data_key": os.getenv("DATA_KEY", "data/transactions.csv"),

        "use_bedrock": os.getenv("USE_BEDROCK", "true").lower() == "true",
    }
