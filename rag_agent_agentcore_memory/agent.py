import os
from langchain.agents import create_agent
from langchain_aws import ChatBedrockConverse
#from langgraph.checkpoint.memory import MemorySaver
from langgraph_checkpoint_aws import AgentCoreMemorySaver, AgentCoreMemoryStore
import config
from tools import query_knowledge_base, predict_salary, explain_salary_prediction, salary_gap_analysis

try:
    from middleware import MemoryMiddleware
except ImportError:
    from rag_agent_agentcore_memory.middleware import MemoryMiddleware

def compile_rag_agent(checkpointer=None, store=None):
    """Initializes LLM and compiles the LangGraph RAG agent with memory checkpointing."""
    
    # Initialize Bedrock Converse LLM (e.g. us.amazon.nova-2-lite-v1:0)
    llm = ChatBedrockConverse(
        model=config.CHAT_MODEL_ID,
        temperature=config.TEMPERATURE,
        region_name=config.AWS_REGION
    )
    
    # Define system instruction parameters instructing RAG and Salary Prediction behavior
    rag_system_prompt = (
        "You are a specialized RAG and Salary Prediction Assistant. "
        "Your goals are:\n"
        "1. Answer general user queries using the query_knowledge_base tool. Always query the knowledge base first to retrieve facts, and strictly cite sources.\n"
        "2. Assist users with salary predictions, explanations, and salary gap analysis using the predict_salary, "
        "explain_salary_prediction, and salary_gap_analysis tools. "
        "Ensure you ask or extract the required profile details (experience_years, education_level, num_skills, "
        "location_index, and current_salary_lpa) when performing salary prediction/analysis tasks."
    )
    
    # Compile Agent using create_agent
    # If no custom checkpointer/store is passed, we check if AgentCore memory is enabled via config
    if checkpointer is None:
        if config.MEMORY_ID:
            # Use managed AWS Bedrock AgentCore Memory Saver
            checkpointer = AgentCoreMemorySaver(
                memory_id=config.MEMORY_ID,
                region_name=config.AWS_REGION
            )
            
    if store is None:
        if config.MEMORY_ID:
            # Use managed AWS Bedrock AgentCore Memory Store
            store = AgentCoreMemoryStore(
                memory_id=config.MEMORY_ID,
                region_name=config.AWS_REGION
            )
        
    agent = create_agent(
        model=llm,
        tools=[query_knowledge_base, predict_salary, explain_salary_prediction, salary_gap_analysis],
        system_prompt=rag_system_prompt,
        checkpointer=checkpointer,
        store=store,
        middleware=[MemoryMiddleware()]
    )
    return agent
