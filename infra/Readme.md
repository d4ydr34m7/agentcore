# Infra Setup Plan

This folder will contain all AWS setup files for the AgentCore project.

### Goal
Keep the setup lightweight and low-cost while learning and testing.

### Planned Components
- **S3** – store small data or prompts
- **Lambda + API Gateway** – host the agent logic
- **Bedrock AgentCore** – main agent runtime
- **OpenSearch (optional)** – for retrieval, only created when needed
- **IAM + KMS** – access control and encryption
- **CloudWatch** – logs and monitoring

### Current Cost Strategy
- Use **OpenSearch** only during testing, delete when idle.
- Use **Bedrock Haiku model** for cheaper API calls.
- Clean up unused resources.

### Current Status
Infra not deployed yet — will start with basic S3 + Lambda setup first.
