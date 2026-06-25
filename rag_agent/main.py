import sys
import sys
import os
# Dynamically add the current directory to sys.path to support direct imports of local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
    
from agent import compile_rag_agent

def main():
    # Compile the agent
    agent = compile_rag_agent()
    
    # Use command-line arguments as query if provided, otherwise default to the notebook query
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Can you explain what Google Gemini is and list some of the latest models?"
        
    print(f"User Query: {query}\n")
    
    # Invoke the agent synchronously using invoke()
    config = {"configurable": {"thread_id": "rag-agent-thread"}}
    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )
    
    # Print the final answer
    print("=== RAG AGENT ANSWER ===\n")
    print(response["messages"][-1].content)

if __name__ == "__main__":
    main()

