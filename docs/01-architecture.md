### Goal
Simple starting point for how the AgentCore system will work.

### Phase 1 (Basic)
- Runs locally, without AWS setup.
- The agent receives a question, understands it, and fetches data from a small local file or mock source.
- Uses the Bedrock Haiku model to generate responses.
- Focus is on getting the basic flow working end-to-end before moving to the cloud.

### TODO
Add “Phase 2 (AWS)” section when starting cloud deployment.

### AWS Bedrock Models (for reference)

| Provider | Model Name | Type / Strength | Notes |
|-----------|-------------|-----------------|--------|
| **Anthropic** | Claude 3 Haiku | Text / Reasoning |
| | Claude 3 Sonnet | Text / Reasoning (balanced) | better accuracy |
| | Claude 3 Opus | Text / Reasoning (strongest) | expensive, enterprise use |
| **Amazon** | Titan Text G1 | Text generation | internal AWS model |
| | Titan Embed G1 | Embedding | used for retrieval |
| **Meta** | Llama 3 (8B / 70B) | Text / Code | open models |
| **Cohere** | Command R+ / R+ Mini | Retrieval-optimized | great for RAG |
| **Mistral / Mixtral** | Mistral 7B, Mixtral 8x7B | Text / Code | fast, open-weight |
| **AI21 Labs** | Jurassic-2 Ultra / Mid | Text generation | older but solid |
| **Stability AI** | SDXL 1.0 | Image generation | for visual agents |


### Notes
Will start with **Claude 3 Haiku** to keep costs and latency low.  
And switch later if better reasoning or retrieval handling is needed.