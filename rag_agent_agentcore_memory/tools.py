import os
import time
import json
import requests
import boto3
from langchain.tools import tool
from vector_store import query_vector_store

def fetch_mcp_config_from_registry():
    """Queries AWS Bedrock AgentCore registry to fetch the transport config of salary-prediction-mcp"""
    try:
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        registry_id = "your-registry-id"  # Replace with your actual registry ID
        record_name = "salary-prediction-mcp"  # Replace with your actual record name

        control_client = boto3.client("bedrock-agentcore-control", region_name=region)
        records = control_client.list_registry_records(registryId=registry_id).get("registryRecords", [])
        
        target_record = None
        for r in records:
            if r["name"] == record_name:
                target_record = r
                break
                
        if not target_record:
            return None, None
            
        rec = control_client.get_registry_record(registryId=registry_id, recordId=target_record["recordId"])
        inline_content = rec["descriptors"]["mcp"]["server"]["inlineContent"]
        mcp_config = json.loads(inline_content)
        transport = mcp_config.get("transport", {})
        return transport.get("url"), transport.get("headers", {})
    except Exception as e:
        print(f"Warning: Failed to fetch MCP configuration from registry: {e}")
        return None, None

# Fetch MCP configuration from the registry
mcp_url, mcp_headers = fetch_mcp_config_from_registry()

# Fallback in case registry call is not available or failed
if not mcp_url:
    mcp_url = "https://SalaryPredictionMCPServer.fastmcp.app/mcp"
    mcp_headers = {
        "Authorization": "Bearer your fastmcp api key"  # Replace with your actual FastMCP API key
    }

headers_with_accept = {
    "Accept": "application/json, text/event-stream",
    **mcp_headers
}

def call_remote_mcp(tool_name: str, arguments: dict) -> str:
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": int(time.time())
    }
    try:
        r = requests.post(mcp_url, headers=headers_with_accept, json=payload, timeout=15)
        if r.status_code != 200:
            return f"Error: MCP server returned status code {r.status_code}"
        for line in r.text.split("\n"):
            if line.startswith("data:"):
                data_json = json.loads(line[5:].strip())
                result = data_json.get("result", {})
                content_list = result.get("content", [])
                if content_list and "text" in content_list[0]:
                    return content_list[0]["text"]
                return str(result)
        return "Error: No data event found in SSE response"
    except Exception as e:
        return f"Error calling MCP tool: {e}"

@tool
def query_knowledge_base(query: str) -> str:
    """Queries the vector database knowledge base for information matching the search query and returns relevant documents."""
    try:
        results = query_vector_store(query, k=2)
        if not results:
            return f"No matching information found in the knowledge base for: '{query}'"
        
        output_str = f"Matching Documents found for '{query}':\n\n"
        for i, doc in enumerate(results, 1):
            output_str += f"Document {i}:\n"
            output_str += f"Content: {doc.page_content}\n"
            output_str += f"Source Metadata: {doc.metadata.get('source', 'Unknown')}\n\n"
        return output_str
    except Exception as e:
        return f"Error querying knowledge base: {str(e)}"

@tool
def predict_salary(
    experience_years: int,
    education_level: int,
    num_skills: int,
    location_index: int,
    current_salary_lpa: float
) -> str:
    """Predict expected market salary based on profile parameters.
    
    Args:
        experience_years: The years of experience.
        education_level: Education level index.
        num_skills: Number of skills.
        location_index: Location index.
        current_salary_lpa: Current salary in LPA (Lakhs Per Annum).
    """
    args = {
        "experience_years": experience_years,
        "education_level": education_level,
        "num_skills": num_skills,
        "location_index": location_index,
        "current_salary_lpa": current_salary_lpa
    }
    return call_remote_mcp("predict_salary", args)

@tool
def explain_salary_prediction(
    experience_years: int,
    education_level: int,
    num_skills: int,
    location_index: int,
    current_salary_lpa: float
) -> str:
    """Explain why the salary prediction was made based on profile parameters.
    
    Args:
        experience_years: The years of experience.
        education_level: Education level index.
        num_skills: Number of skills.
        location_index: Location index.
        current_salary_lpa: Current salary in LPA (Lakhs Per Annum).
    """
    args = {
        "experience_years": experience_years,
        "education_level": education_level,
        "num_skills": num_skills,
        "location_index": location_index,
        "current_salary_lpa": current_salary_lpa
    }
    return call_remote_mcp("explain_salary_prediction", args)

@tool
def salary_gap_analysis(
    experience_years: int,
    education_level: int,
    num_skills: int,
    location_index: int,
    current_salary_lpa: float
) -> str:
    """Analyze how underpaid or overpaid the user is based on profile parameters.
    
    Args:
        experience_years: The years of experience.
        education_level: Education level index.
        num_skills: Number of skills.
        location_index: Location index.
        current_salary_lpa: Current salary in LPA (Lakhs Per Annum).
    """
    args = {
        "experience_years": experience_years,
        "education_level": education_level,
        "num_skills": num_skills,
        "location_index": location_index,
        "current_salary_lpa": current_salary_lpa
    }
    return call_remote_mcp("salary_gap_analysis", args)
