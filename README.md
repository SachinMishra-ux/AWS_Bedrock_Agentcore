# AWS Bedrock AgentCore - Architecture & Deployment Scenarios

This repository showcases three progressively advanced architectural scenarios for deploying autonomous AI agents on the **Amazon Bedrock AgentCore Runtime**:

| Directory                                  | Architecture                                      | Key Capabilities                                                                                        |
| :----------------------------------------- | :------------------------------------------------ | :------------------------------------------------------------------------------------------------------ |
| **`rag_agent_agentcore`**          | **Scenario 1: Base RAG Agent**              | Stateless container deployment, FAISS vector search, Bedrock Converse model orchestration.              |
| **`rag_agent_agentcore_memory`**   | **Scenario 2: Memory-Enabled RAG Agent**    | Multi-turn conversational persistence using**Bedrock AgentCore Managed Memory (STM + LTM)**.      |
| **`rag_agent_agentcore_registry`** | **Scenario 3: Memory + MCP Registry Agent** | Dynamic tool discovery via**Bedrock AgentCore MCP Registry** + Remote MCP tools + STM/LTM memory. |

---

## 🛠️ Global Prerequisites & Setup

```bash
# 1. Initialize environment (if setting up fresh)
uv init
uv add langchain langchain-aws langchain-community langgraph faiss-cpu bedrock-agentcore langgraph-checkpoint-aws mcp requests boto3 python-dotenv

# 2. Configure AWS Credentials
aws configure
```

### 🔐 IAM Permissions & Inline Policy

Ensure your IAM user (`sachinmishra`) has the following inline policy attached (named `AgentCoreDeploymentPolicy`), which grants permissions across Bedrock AgentCore, AWS Agent Registry (`agent-registry:*`), ECR, CodeBuild, and S3:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AgentCoreAndRegistryFullAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:*",
        "agent-registry:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "ECRRepositoryAccess",
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:DescribeRepositories",
        "ecr:CreateRepository",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecr:PutImage",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CodeBuildAndLogsAccess",
      "Effect": "Allow",
      "Action": [
        "codebuild:CreateProject",
        "codebuild:StartBuild",
        "codebuild:BatchGetBuilds",
        "codebuild:BatchGetProjects",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:GetLogEvents",
        "logs:DescribeLogStreams",
        "logs:PutDeliverySource",
        "logs:PutDeliveryDestination",
        "logs:CreateDelivery",
        "logs:GetDeliverySource",
        "logs:GetDeliveryDestination"
      ],
      "Resource": "*"
    },
    {
      "Sid": "IAMRoleCreationAndPassRole",
      "Effect": "Allow",
      "Action": [
        "iam:CreateRole",
        "iam:GetRole",
        "iam:AttachRolePolicy",
        "iam:PutRolePolicy",
        "iam:PassRole"
      ],
      "Resource": "*"
    },
    {
      "Sid": "S3SourceBucketAccess",
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": "*"
    }
  ]
}
```

> For full least-privilege breakdowns and managed policies, see **[AGENTCORE_IAM_POLICIES.md](AGENTCORE_IAM_POLICIES.md)**.

---

## 🚀 Scenario 1: Base RAG Agent (`rag_agent_agentcore`)

Demonstrates containerizing and deploying a basic RAG agent to the AWS Bedrock AgentCore runtime without external memory persistence.

### Local Testing

```bash
cd rag_agent_agentcore
uv run test_bedrock.py    # Test Bedrock model connectivity
uv run agent.py           # Test RAG query locally
```

### Lifecycle Commands

```bash
cd rag_agent_agentcore

# 1. Configure agent deployment
agentcore configure -e ./main.py

# 2. Build ARM64 container in CodeBuild and deploy runtime
agentcore deploy

# 3. Check status
agentcore status

# 4. Invoke agent
agentcore invoke '{"prompt": "What is FAISS and how is it used?"}'

# 5. Destroy resources
agentcore destroy --delete-ecr-repo --force
```

---

## 🧠 Scenario 2: Memory-Enabled RAG Agent (`rag_agent_agentcore_memory`)

Demonstrates multi-turn conversational memory using **AWS Bedrock AgentCore Managed Memory**:

* **Short-Term Memory (STM)**: Checkpointed with `AgentCoreMemorySaver`.
* **Long-Term Memory (LTM)**: Profile/preference persistence with `AgentCoreMemoryStore`.

### 1. Configuration

Check `rag_agent_agentcore_memory/config.py`:

```python
# Set to your active Bedrock AgentCore Memory Resource ID (from .bedrock_agentcore.yaml)
MEMORY_ID = os.getenv("AGENTCORE_MEMORY_ID", "rag_agent_mem-6ht3cVFZSK")
```

### 2. Lifecycle Commands

```bash
cd rag_agent_agentcore_memory

# 1. Configure agent deployment
agentcore configure -e ./main.py

# 2. Deploy to AgentCore runtime
agentcore deploy

# 3. Check status
agentcore status

# 4. Destroy resources
agentcore destroy --delete-ecr-repo --force
```

### 3. Testing Conversational Memory Across Turns

```bash
# Turn 1: Introduce user identity
agentcore invoke '{"prompt": "Hi, my name is Sachin and I live in Bangalore."}'

# Turn 2: Test short-term memory recall
agentcore invoke '{"prompt": "Do you remember what my name is?"}'

# Turn 3: Test RAG + personal context recall
agentcore invoke '{"prompt": "Can you summarize Google Gemini and explain how it can help me?"}'
```

---

## 🌐 Scenario 3: Memory + MCP Registry Agent (`rag_agent_agentcore_registry`)

Demonstrates an enterprise-ready architecture connecting:

1. **AWS Bedrock AgentCore Registry**: Dynamically resolves endpoints for remote Model Context Protocol (MCP) servers (`bedrock-agentcore-control`).
2. **Remote MCP Tools**: Executes salary prediction and market analytics tools (`predict_salary`, `explain_salary_prediction`, `salary_gap_analysis`).
3. **Managed Memory (STM + LTM)**: Retains candidate profiles and evaluation parameters across conversational turns.
4. **Local Knowledge Base**: Grounded RAG retrieval for facts and technical questions.

### Step 1: Create the Registry in AWS Console

1. Open the [AWS Bedrock / Agent Registry Console](https://console.aws.amazon.com/bedrock) in **`us-east-1`**.
2. Navigate to **AWS Agent Registry > Registries** > Click **Create registry**.
3. Settings:
   * **Name**: `salary_prediction_mcp_server`
   * **Auto-approval**: **Enabled** *(allows submitted MCP records to be approved automatically)*
4. Copy the generated **Registry ID** (e.g. `dYczX6QjgCpmY3Eb`).

### Step 2: Configure Environment Variables

Ensure `.env` contains your registry ID and FastMCP credentials:

```env
mcp_url="https://salary-prediction-mcp.fastmcp.app/mcp"
fastmcp_api_key="your-fastmcp-api-key"
AGENTCORE_REGISTRY_ID="dYczX6QjgCpmY3Eb"
```

### Step 3: Register MCP Server into the Registry

You can register the MCP record via the AWS Console or programmatically:

* **Console (Recommended)**: In AWS Console > **AWS Agent Registry** > Select `salary_prediction_mcp_server` > **Registry records** > Click **Create record** (Name: `salary-prediction-mcp`, Type: `MCP`, Transport: `SSE`, Endpoint: `https://salary-prediction-mcp.fastmcp.app/mcp/sse`, Header: `Authorization: Bearer <key>`).
* **CLI/Script**: Run `uv run register_mcp.py` inside `rag_agent_agentcore_registry`.

> **Permissions**: Requires `agent-registry:*` IAM permissions (see [AGENTCORE_IAM_POLICIES.md](AGENTCORE_IAM_POLICIES.md)). If programmatic API access to the preview control plane is restricted, the runtime in `tools.py` automatically falls back to your `.env` endpoint.

### Step 4: Configure and Deploy the Agent

```bash
cd rag_agent_agentcore_registry

# 1. Configure agent deployment
agentcore configure -e ./main.py

# 2. Deploy to AgentCore runtime
agentcore deploy

# 3. Check status
agentcore status

# 4. Destroy resources (when cleaning up)
agentcore destroy --delete-ecr-repo --force
```

### Step 5: Testing MCP Tool Invocations & Multi-Turn Retention

```bash
# Turn 1: Provide full candidate profile (triggers MCP predict_salary and saves to memory)
agentcore invoke '{"prompt": "Can you predict my expected market salary? Details: Experience is 5 years, Education level is 1 (Bachelors), 5 skills, Location index is 1, Current salary is 20 LPA. My name is Sachin."}'

# Turn 2: Test MCP explain tool (recalls parameters from memory without re-typing)
agentcore invoke '{"prompt": "Can you explain why that prediction was made for my profile?"}'

# Turn 3: Test salary gap analysis via MCP
agentcore invoke '{"prompt": "Perform a salary gap analysis for the same details."}'

# Turn 4: Test Knowledge Base RAG tool (profile & architecture questions)
agentcore invoke '{"prompt": "What is the overall year of experience for Sachin Mishra?"}'
agentcore invoke '{"prompt": "What are AWS Bedrock AgentCore short-term and long-term memory options?"}'
```

---

### Step 6: Running the Web UI & Backend Server

A full-stack Web interface is included at the project root:

1. **Start the FastAPI Backend**:
   ```bash
   # From root directory
   python main.py
   ```
   *(Runs locally at `http://localhost:8000`)*

2. **Open the Web UI**:
   Navigate to `http://localhost:8000` in your web browser (or open `index.html` directly).

---

## 🔄 Redeployment Guide (When Code or Knowledge Base Changes)

Because the agent runs as a containerized workload on AWS Bedrock AgentCore, **local modifications to code or documents are not reflected in the cloud until redeployed**.

If you make any changes to:
- Knowledge base documents in `vector_store.py`
- Tool signatures or implementations in `tools.py`
- System prompts or agent logic in `agent.py`
- Dependencies in `requirements.txt`

**Run redeployment:**
```bash
cd rag_agent_agentcore_registry
agentcore deploy
```
*(CodeBuild will automatically rebuild the container image, push to ECR, and update the AgentCore runtime)*

---

## 🛠️ Troubleshooting & Common Issues

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **Agent doesn't know newly added facts from `vector_store.py`** | Container running in AWS hasn't been updated with local code edits. | Run `agentcore deploy` in `rag_agent_agentcore_registry` to rebuild and update the container image. |
| **Agent says "I don't have this in conversation context" instead of searching docs** | The model assumed the question was about conversation history rather than knowledge base docs. | Ensure `agent.py` system prompt instructs the agent to check `query_knowledge_base` first, and ensure the tool docstring mentions the entity. |
| **MCP Tool Authentication error (`401` or `403`)** | Missing or invalid API key header. | Verify `fastmcp_api_key` in `.env`. If using AWS Agent Registry, ensure the record has `Authorization: Bearer <key>` configured. |
| **FastAPI Backend returns `500` or connection error** | Mismatched or outdated `AGENT_RUNTIME_ARN`. | Verify `AGENT_RUNTIME_ARN` in `main.py` and `.env` matches the deployed ARN (`arn:aws:bedrock-agentcore:us-east-1:869935080204:runtime/mcp_rag_agent-zRXrbS2g9V`). |

---

## 🔍 Debugging & CloudWatch Runtime Logs

Tail live logs directly from the runtime containers:

```bash
# Scenario 1 (rag_agent_agentcore)
aws logs tail /aws/bedrock-agentcore/runtimes/rag_agent-DEFAULT --log-stream-name-prefix "2026/10/13/[runtime-logs]" --since 1h

# Scenario 2 (rag_agent_agentcore_memory)
aws logs tail /aws/bedrock-agentcore/runtimes/rag_agent_memory-DEFAULT --log-stream-name-prefix "2026/10/13/[runtime-logs]" --since 1h

# Scenario 3 (rag_agent_agentcore_registry)
aws logs tail /aws/bedrock-agentcore/runtimes/mcp_rag_agent-zRXrbS2g9V-DEFAULT --log-stream-name-prefix "2026/10/13/[runtime-logs]" --follow
```

---

## 📚 Documentation Reference

* **[AGENTCORE_IAM_POLICIES.md](AGENTCORE_IAM_POLICIES.md)**: IAM managed and inline policy requirements for `agentcore deploy`.

