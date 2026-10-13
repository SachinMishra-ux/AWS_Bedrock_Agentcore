import os
from langchain.agents import create_agent
from langchain_aws import ChatBedrockConverse
from langgraph_checkpoint_aws import AgentCoreMemorySaver, AgentCoreMemoryStore
import config
from tools import query_knowledge_base

try:
    from middleware import MemoryMiddleware
except ImportError:
    from rag_agent_agentcore_memory.middleware import MemoryMiddleware

def compile_rag_agent(checkpointer=None, store=None):
    """Initializes LLM and compiles the LangGraph RAG agent with memory checkpointing."""
    
    # Initialize Bedrock Converse LLM
    llm = ChatBedrockConverse(
        model=config.CHAT_MODEL_ID,
        temperature=config.TEMPERATURE,
        region_name=config.AWS_REGION
    )
    
    # System prompt focusing on RAG and conversational memory
    rag_system_prompt = (
        "You are a specialized RAG Assistant equipped with short-term and long-term memory. "
        "Your goals are:\n"
        "1. Answer user queries using the query_knowledge_base tool. Query the knowledge base first to retrieve facts and cite sources.\n"
        "2. Retain conversational context across multiple turns. Remember user details, name, and preferences shared during the chat.\n"
        "3. When answering, personalize responses using previously recalled context whenever relevant."
    )
    
    # Configure AgentCore Managed Memory (STM checkpointer & LTM store)
    if checkpointer is None:
        if config.MEMORY_ID:
            checkpointer = AgentCoreMemorySaver(
                memory_id=config.MEMORY_ID,
                region_name=config.AWS_REGION
            )
            
    if store is None:
        if config.MEMORY_ID:
            store = AgentCoreMemoryStore(
                memory_id=config.MEMORY_ID,
                region_name=config.AWS_REGION
            )
        
    agent = create_agent(
        model=llm,
        tools=[query_knowledge_base],
        system_prompt=rag_system_prompt,
        checkpointer=checkpointer,
        store=store,
        middleware=[MemoryMiddleware()]
    )
    return agent
