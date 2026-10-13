import os
from langchain.agents import create_agent
from langchain_aws import ChatBedrockConverse
from langgraph_checkpoint_aws import AgentCoreMemorySaver, AgentCoreMemoryStore
import config
from tools import query_knowledge_base, predict_salary, explain_salary_prediction, salary_gap_analysis

try:
    from middleware import MemoryMiddleware
except ImportError:
    from rag_agent_agentcore_registry.middleware import MemoryMiddleware

def compile_rag_agent(checkpointer=None, store=None):
    """Initializes LLM and compiles the LangGraph RAG Agent with Bedrock AgentCore Memory and MCP Registry tools."""
    
    # Initialize Bedrock Converse LLM
    llm = ChatBedrockConverse(
        model=config.CHAT_MODEL_ID,
        temperature=config.TEMPERATURE,
        region_name=config.AWS_REGION
    )
    
    # System prompt instructing RAG, MCP tool usage, and memory behavior
    rag_system_prompt = (
        "You are an Advanced RAG & Salary Prediction Assistant running on AWS Bedrock AgentCore. "
        "You have access to:\n"
        "1. RAG Tool ('query_knowledge_base'): Use to query documents and cite sources from the knowledge base.\n"
        "2. MCP Tools ('predict_salary', 'explain_salary_prediction', 'salary_gap_analysis'): "
        "Discovered dynamically via the AWS Bedrock AgentCore Registry. Use these to analyze user profiles and predict compensation.\n"
        "3. Multi-turn Conversational Memory: You automatically recall user details across conversational turns.\n\n"
        "Instructions:\n"
        "- ALWAYS use 'query_knowledge_base' whenever the user asks about facts, concepts, background, or information about individuals (such as Sachin Mishra and his experience or background), AWS Bedrock AgentCore memory options (STM / LTM), or technical architecture.\n"
        "- If information about a person or topic exists in the knowledge base, answer the question using the retrieved knowledge base documents.\n"
        "- Only use the MCP salary tools ('predict_salary', etc.) when the user is explicitly requesting a salary prediction, compensation explanation, or market gap analysis.\n"
        "- Always remember previously mentioned parameters so the user doesn't have to repeat themselves."
    )
    
    # Set up managed Bedrock AgentCore Memory (STM Saver & LTM Store)
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
        tools=[query_knowledge_base, predict_salary, explain_salary_prediction, salary_gap_analysis],
        system_prompt=rag_system_prompt,
        checkpointer=checkpointer,
        store=store,
        middleware=[MemoryMiddleware()]
    )
    return agent
