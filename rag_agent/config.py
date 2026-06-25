import os

# AWS Configurations
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Bedrock Model Configurations
# We use us.amazon.nova-2-lite-v1:0 for fast inference, and amazon.titan-embed-text-v2:0 for text embedding
CHAT_MODEL_ID = os.getenv("CHAT_MODEL_ID", "us.amazon.nova-2-lite-v1:0")
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")

# Agent Parameters
TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.0"))
