# AWS Bedrock AgentCore - RAG Agent with Memory & MCP Registry

This agent demonstrates an enterprise-grade agent built on **AWS Bedrock AgentCore Runtime** featuring:

1. **AWS Agent Registry Integration**: Dynamically discovers remote Model Context Protocol (MCP) servers registered in the **Bedrock AgentCore Registry**.
2. **Remote MCP Tool Execution**: Calls FastMCP tools (`predict_salary`, `explain_salary_prediction`, `salary_gap_analysis`) using SSE/HTTP transport and API keys.
3. **Multi-Turn Conversational Memory**: Utilizes **AWS Bedrock AgentCore Managed Memory (STM + LTM)** to recall candidate details across conversation turns.
4. **Retrieval-Augmented Generation (RAG)**: In-memory FAISS knowledge base grounding factual answers with citations.

---

## 📁 Package Layout

- **`config.py`**: Model IDs, AWS region, Memory ID, and Registry ID.
- **`register_mcp.py`**: Helper script to register, approve, and index MCP server descriptors in the AWS Agent Registry.
- **`tools.py`**: Dynamically queries the registry (`bedrock-agentcore-control`) and dispatches calls to remote MCP endpoints.
- **`middleware.py`**: Intercepts LLM input/output to store and retrieve long-term profile memories via `AgentCoreMemoryStore`.
- **`agent.py`**: Compiles the LangGraph agent combining RAG, MCP tools, and AgentCore Memory.
- **`main.py`**: AgentCore container runtime entrypoint (`@app.entrypoint`).
- **`Dockerfile`**: Container definition for ARM64 CodeBuild cloud builds.

---

## 🚀 Setup & Deployment Walkthrough

### Step 1: Create the AWS Agent Registry in the AWS Console

1. Open the [AWS Bedrock / Agent Registry Console](https://console.aws.amazon.com/bedrock) in **`us-east-1`**.
2. In the left navigation pane under **AWS Agent Registry**, click **Registries**.
3. Click **Create registry**:
   * **Name**: `salary_prediction_mcp_server`
   * **Description**: `salary_prediction_mcp_server`
   * **Auto-approval**: **Enabled** *(allows newly submitted records to be approved automatically)*
4. Once created, note your **Registry ID** (e.g. `dYczX6QjgCpmY3Eb`).

---

### Step 2: Configure Environment Variables

In your `.env` file (at the project root or in `rag_agent_agentcore_registry/.env`):

```env
# AWS Credentials
AWS_ACCESS_KEY_ID="your-access-key"
AWS_SECRET_ACCESS_KEY="your-secret-key"
AWS_DEFAULT_REGION="us-east-1"

# FastMCP Server URL & API Key
mcp_url="https://salary-prediction-mcp.fastmcp.app/mcp"
fastmcp_api_key="your-fastmcp-api-key"

# Your AWS Agent Registry ID (from Step 1)
AGENTCORE_REGISTRY_ID="dYczX6QjgCpmY3Eb"
```

---

### Step 3: Register the MCP Server into the Registry

You can add the MCP record directly via the AWS Console or programmatically:

#### Option A: Via the AWS Agent Registry Console (Recommended)

1. In the [AWS Console](https://console.aws.amazon.com/bedrock), navigate to **AWS Agent Registry** > **Registries** > Select your registry (`salary_prediction_mcp_server`).
2. Scroll to the **Registry records** section and click **Create record** (or **Add record**).
3. Fill in the MCP record configuration:
   * **Record Name**: `salary-prediction-mcp`
   * **Record Type**: `MCP`
   * **Transport Type**: `SSE`
   * **Endpoint URL**: `https://salary-prediction-mcp.fastmcp.app/mcp/sse`
   * **Headers**: `Authorization: Bearer <your-fastmcp-api-key>`
4. Click **Create** / **Submit**. With Auto-approval enabled, the status immediately becomes **`APPROVED`** and is indexed for discovery.

#### Option B: Via Python Script

```bash
cd rag_agent_agentcore_registry
uv run register_mcp.py
```

### IAM Policy Required (Inline Policy)

Ensure your IAM User (`sachinmishra`) has the following inline policy attached (e.g. named `AgentCoreDeploymentPolicy`), which includes **`agent-registry:*`** and **`bedrock-agentcore:*`**:

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

---

### Step 4: Configure and Deploy the Agent

```bash
cd rag_agent_agentcore_registry

# Configure entrypoint and Dockerfile
agentcore configure -e ./main.py

# Build ARM64 container and deploy to Bedrock AgentCore
agentcore deploy
```

---

### Step 5: Invoke and Test Multi-Turn Memory with MCP Tools

Test multi-turn salary prediction and memory retention:

**Turn 1: Initial Profile Submission (triggers MCP predict_salary & saves to memory)**

```bash
agentcore invoke '{"prompt": "Can you predict my expected market salary? Experience: 5 years, Education level: 1 (Bachelors), Skills: 5, Location index: 1, Current salary: 20 LPA. My name is Sachin."}'
```

**Turn 2: Explain Prediction (recalls parameters from memory without repeating them)**

```bash
agentcore invoke '{"prompt": "Can you explain why that prediction was made for my profile?"}'
```

**Turn 3: Salary Gap Analysis (utilizes MCP salary gap tool with saved context)**

```bash
agentcore invoke '{"prompt": "Perform a salary gap analysis for the same details."}'
```

**Turn 4: Knowledge Base RAG Queries (Profile & Architecture)**

```bash
# Test Sachin Mishra profile from vector store
agentcore invoke '{"prompt": "What is the overall year of experience for Sachin Mishra?"}'

# Test AgentCore memory architecture facts
agentcore invoke '{"prompt": "What are AWS Bedrock AgentCore short-term and long-term memory options?"}'
```

---

## 🔄 Redeployment Guide (When Code or Knowledge Base Changes)

Because the agent runs inside a container image deployed to AWS Bedrock AgentCore, **local edits (to `vector_store.py`, `tools.py`, `agent.py`, etc.) are not automatically reflected in the cloud until redeployed**.

Whenever you update files in this folder, run:
```bash
agentcore deploy
```
*CodeBuild will build the new ARM64 image, upload it to ECR, and update the AgentCore runtime seamlessly.*

---

## 🛠️ Troubleshooting

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **Agent doesn't know facts added to `vector_store.py`** | Local changes have not been deployed to AWS. | Run `agentcore deploy` to rebuild the container image and update the runtime. |
| **Agent says "not in conversation context" instead of querying knowledge base** | Model assumed information was a session parameter. | Ensure `agent.py` system prompt instructs checking `query_knowledge_base` first, and ensure `tools.py` docstring covers the topic. |
| **FastMCP authentication error (`401` / `403`)** | Missing/incorrect API key. | Verify `fastmcp_api_key` in `.env` and verify registry record header (`Authorization: Bearer <key>`). |
| **Tail Live Logs** | Need real-time logs for debugging. | `aws logs tail /aws/bedrock-agentcore/runtimes/mcp_rag_agent-zRXrbS2g9V-DEFAULT --log-stream-name-prefix "2026/10/13/[runtime-logs]" --follow` |

---

### Step 6: Cleanup (Optional)

To delete all deployed resources (AgentCore Runtime, ECR repository, CodeBuild project, and Memory):

```bash
agentcore destroy --delete-ecr-repo --force
```

