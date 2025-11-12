from pathlib import Path
import os, yaml

CFG_PATH = Path("services/agent/config/config.yaml")

def get_cfg():
    cfg = {"env":"dev","model_id":os.getenv("MODEL_ID","anthropic.claude-3-haiku-20240307-v1:0"),
           "region":os.getenv("AWS_REGION","us-east-1"),
           "data_path":"data/transactions.csv",
           "use_bedrock": True}
    if CFG_PATH.exists():
        with open(CFG_PATH) as f:
            y = yaml.safe_load(f) or {}
            cfg.update(y)
    return cfg
