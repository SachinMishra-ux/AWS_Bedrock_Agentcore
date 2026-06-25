import sys
import os

# Dynamically add the current directory to sys.path to support direct imports of local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from agent import compile_rag_agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Initialize the AgentCore app instance
app = BedrockAgentCoreApp()

# Compile the RAG agent
agent = compile_rag_agent()

# AgentCore Entrypoint
@app.entrypoint
def agent_invocation(payload, context):
    """Handler for agent invocation in AgentCore runtime"""
    print("Received payload:", payload)
    print("Context:", context)
    
    # Extract query/prompt, session_id, and actor_id from the payload
    query = payload.get("prompt", "No prompt found in input")
    session_id = payload.get("session_id", "default-session")
    actor_id = payload.get("actor_id", "default-user")
    
    print(f"Executing Agent with Query: {query} for Actor: {actor_id}")
    
    # Invoke the compiled agent synchronously
    config = {
        "configurable": {
            "thread_id": session_id,
            "actor_id": actor_id
        }
    }
    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    
    print("Result:", result)
    
    # Extract final assistant message text
    final_answer = result["messages"][-1].content
    
    # Return the answer to AgentCore
    return {"result": final_answer}

if __name__ == "__main__":
    app.run()


