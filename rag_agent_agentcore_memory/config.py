import os
from dotenv import load_dotenv

load_dotenv()

# AWS Configurations
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Bedrock Model Configurations
CHAT_MODEL_ID = os.getenv("CHAT_MODEL_ID", "us.amazon.nova-2-lite-v1:0")
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")

# Agent Parameters
TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.0"))

# Active Bedrock AgentCore Memory Resource ID (from .bedrock_agentcore.yaml)
MEMORY_ID = os.getenv("AGENTCORE_MEMORY_ID", "rag_agent_mem-6ht3cVFZSK")
