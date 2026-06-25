import os
import uuid
import json
import boto3
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="AWS Bedrock AgentCore API Wrapper",
    description="REST API wrapper around the deployed RAG Agent on Bedrock AgentCore"
)

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Schemas
class ChatRequest(BaseModel):
    prompt: str
    session_id: str = None  # Optional: Pass this to preserve multi-turn memory context

class ChatResponse(BaseModel):
    session_id: str
    response: str

# Configuration
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AGENT_RUNTIME_ARN = os.getenv(
    "AGENT_RUNTIME_ARN",
    "arn:aws:bedrock-agentcore:us-east-1:869935080204:runtime/mcp_rag_agent-Z7rC3q5flc"
)

# Initialize the Bedrock AgentCore client
try:
    agentcore_client = boto3.client("bedrock-agentcore", region_name=AWS_REGION)
except Exception as e:
    print(f"⚠️ Error initializing boto3 client: {e}")
    agentcore_client = None

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    if not agentcore_client:
        raise HTTPException(
            status_code=500,
            detail="AWS Bedrock AgentCore client is not initialized. Check your credentials."
        )
    
    # Use existing session ID or generate a new unique one
    session_id = request.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
    elif len(session_id) < 33:
        # Deterministically map short session IDs to a valid 36-character UUID to satisfy AWS validation
        session_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, session_id))
    
    # Payload matching the format expected by @app.entrypoint
    payload_data = {
        "prompt": request.prompt,
        "session_id": session_id
    }
    
    try:
        # Invoke the runtime session in AWS Bedrock AgentCore
        response = agentcore_client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_RUNTIME_ARN,
            runtimeSessionId=session_id,
            payload=json.dumps(payload_data)
        )
        
        # Read and decode response body from AgentCore stream
        response_body = response.get("response").read().decode("utf-8")
        result_json = json.loads(response_body)
        
        # Extract the 'result' key returned by your entrypoint
        answer = result_json.get("result", "No response returned from agent.")
        
        return ChatResponse(
            session_id=session_id,
            response=answer
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to invoke Bedrock AgentCore runtime: {str(e)}"
        )

if __name__ == "__main__":
    # Start the API server locally on port 8000 with reload enabled
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
