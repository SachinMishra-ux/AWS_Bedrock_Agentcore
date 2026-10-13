import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from current directory and parent directory
load_dotenv()
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# AWS Configurations
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Bedrock Model Configurations
CHAT_MODEL_ID = os.getenv("CHAT_MODEL_ID", "us.amazon.nova-2-lite-v1:0")
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")

# Agent Parameters
TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.0"))

# Active Bedrock AgentCore Memory Resource ID
MEMORY_ID = os.getenv("AGENTCORE_MEMORY_ID", "rag_agent_mem-6ht3cVFZSK")

# AWS Bedrock AgentCore MCP Registry Configuration
REGISTRY_ID = os.getenv("AGENTCORE_REGISTRY_ID", "dYczX6QjgCpmY3Eb")
RECORD_ID = os.getenv("AGENTCORE_RECORD_ID", "jK440DvFaRi8")
MCP_RECORD_NAME = os.getenv("MCP_RECORD_NAME", "salary-prediction-mcp")

# MCP Server Credentials & Endpoint
MCP_URL = os.getenv("mcp_url") or os.getenv("MCP_URL", "https://salary-prediction-mcp.fastmcp.app/mcp")
FASTMCP_API_KEY = os.getenv("fastmcp_api_key") or os.getenv("FASTMCP_API_KEY", "api-key-placeholder")
