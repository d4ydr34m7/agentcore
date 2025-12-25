# AgentCore – Serverless Analytics Agent

## What this is
A serverless analytics agent that answers deterministic questions locally (fast + cheap) and uses an LLM for open-ended insights (grounded, low-hallucination).

## Architecture
Client → API Gateway (HTTP API) → Lambda → (S3 dataset + Bedrock LLM)

- S3: stores `data/transactions.csv`
- Lambda: intent routing + local skills + grounded Bedrock fallback
- Bedrock: Claude (Haiku) for reasoning on computed facts
- API Gateway: exposes `POST /query`

## How it works
### Local skills (deterministic)
Examples: `summary`, `insights`, `top merchants`, `count pending`, `total`

### LLM fallback (only for open-ended questions)
- Triggered only when query doesn’t match known skill shapes
- Prompt is grounded using computed facts + a few sample rows (not raw dataset)

## API
### Endpoint
`POST /query`

### Request
```json
{ "query": "top merchants" }
