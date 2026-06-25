from langchain.agents import create_agent
from langchain_aws import ChatBedrockConverse
from langgraph.checkpoint.memory import MemorySaver
import config
from tools import query_knowledge_base

def compile_rag_agent(checkpointer=None):
    """Initializes LLM and compiles the LangGraph RAG agent with memory checkpointing."""
    
    # Initialize Bedrock Converse LLM (e.g. us.amazon.nova-2-lite-v1:0)
    llm = ChatBedrockConverse(
        model=config.CHAT_MODEL_ID,
        temperature=config.TEMPERATURE,
        region_name=config.AWS_REGION
    )
    
    # Define system instruction parameters instructing RAG behavior
    rag_system_prompt = (
        "You are a specialized RAG Assistant. Your goal is to answer user queries using the query_knowledge_base tool. "
        "Whenever the user asks a question, always query the knowledge base first to retrieve facts. "
        "Answer based strictly on the retrieved contents. Do not make up facts. "
        "Always cite the source of your information in your final answer (e.g. '[Source: Gemini Fact Sheet]')."
    )
    
    # Compile Agent using create_agent
    # If no custom checkpointer is passed, we default to MemorySaver for local persistence
    if checkpointer is None:
        checkpointer = MemorySaver()
        
    agent = create_agent(
        model=llm,
        tools=[query_knowledge_base],
        system_prompt=rag_system_prompt,
        checkpointer=checkpointer
    )
    return agent
