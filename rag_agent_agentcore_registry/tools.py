import os
import time
import json
import requests
import boto3
from langchain.tools import tool
from vector_store import query_vector_store
import config

def fetch_mcp_config_from_registry():
    """Queries official AWS Agent Registry API to fetch the transport config of the MCP server"""
    try:
        from botocore.auth import SigV4Auth
        from botocore.awsrequest import AWSRequest
        
        region = config.AWS_REGION
        registry_id = config.REGISTRY_ID
        record_id = getattr(config, "RECORD_ID", None)

        if not registry_id or not record_id or registry_id == "your-registry-id":
            return None, None

        session = boto3.Session()
        creds = session.get_credentials().get_frozen_credentials()
        url = f"https://agent-registry-control.{region}.api.aws/registries/{registry_id}/records/{record_id}"

        req = AWSRequest(method="GET", url=url, headers={"Host": f"agent-registry-control.{region}.api.aws"})
        SigV4Auth(creds, "agent-registry", region).add_auth(req)
        resp = requests.get(url, headers=dict(req.headers), timeout=10)

        if resp.status_code == 200:
            rec = resp.json()
            descriptors = rec.get("descriptors", {})
            mcp_server = descriptors.get("mcpServer", {})
            data_str = mcp_server.get("data")
            if data_str:
                mcp_config = json.loads(data_str)
                transport = mcp_config.get("transport", {})
                print(f"✅ Dynamically discovered MCP Server '{rec.get('name')}' from AWS Agent Registry (Record ID: {record_id})")
                return transport.get("url"), transport.get("headers", {})
        else:
            print(f"Notice: Agent Registry returned status {resp.status_code}: {resp.text[:100]}")
            return None, None
    except Exception as e:
        print(f"Notice: Using configured MCP endpoint (AgentCore registry query returned: {e})")
        return None, None

# Attempt to fetch MCP configuration from the Bedrock AgentCore registry
mcp_url, mcp_headers = fetch_mcp_config_from_registry()

# Fallback to configured MCP_URL and FASTMCP_API_KEY from .env
if not mcp_url:
    mcp_url = config.MCP_URL
    auth_header = f"Bearer {config.FASTMCP_API_KEY}" if config.FASTMCP_API_KEY else ""
    mcp_headers = {
        "Authorization": auth_header
    } if auth_header else {}

headers_with_accept = {
    "Accept": "application/json, text/event-stream",
    **mcp_headers
}

def call_remote_mcp(tool_name: str, arguments: dict) -> str:
    """Invokes a tool on the remote MCP Server via JSON-RPC 2.0 / SSE"""
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        },
        "id": int(time.time())
    }
    post_url = mcp_url[:-4] if mcp_url.endswith("/sse") else mcp_url
    try:
        r = requests.post(post_url, headers=headers_with_accept, json=payload, timeout=20)
        if r.status_code != 200:
            return f"Error: MCP server returned status code {r.status_code}: {r.text}"
        for line in r.text.split("\n"):
            if line.startswith("data:"):
                data_json = json.loads(line[5:].strip())
                result = data_json.get("result", {})
                content_list = result.get("content", [])
                if content_list and "text" in content_list[0]:
                    return content_list[0]["text"]
                return str(result)
        # In case the response is standard JSON rather than SSE
        try:
            res_json = r.json()
            if "result" in res_json:
                res_content = res_json["result"].get("content", [])
                if res_content and "text" in res_content[0]:
                    return res_content[0]["text"]
                return str(res_json["result"])
        except Exception:
            pass
        return f"Response received: {r.text}"
    except Exception as e:
        return f"Error calling MCP tool: {e}"

@tool
def query_knowledge_base(query: str) -> str:
    """Queries the knowledge base vector database for information regarding individuals (e.g., Sachin Mishra and his background, experience, skills), AWS Bedrock AgentCore features (short-term and long-term memory options), LangChain, FAISS, Gemini models, and RAG architectures."""
    try:
        results = query_vector_store(query, k=3)
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
    """Predict expected market salary based on profile parameters via the registered MCP Server.
    
    Args:
        experience_years: Years of professional experience (e.g. 5).
        education_level: Education level index (e.g. 1 for Bachelors, 2 for Masters).
        num_skills: Total number of technical skills.
        location_index: Location tier index (e.g. 1 for Tier-1 city).
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
    """Explain why the salary prediction was made based on profile parameters via the registered MCP Server.
    
    Args:
        experience_years: Years of professional experience.
        education_level: Education level index.
        num_skills: Total number of technical skills.
        location_index: Location tier index.
        current_salary_lpa: Current salary in LPA.
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
    """Analyze how underpaid or overpaid the candidate is based on profile parameters via the registered MCP Server.
    
    Args:
        experience_years: Years of professional experience.
        education_level: Education level index.
        num_skills: Total number of technical skills.
        location_index: Location tier index.
        current_salary_lpa: Current salary in LPA.
    """
    args = {
        "experience_years": experience_years,
        "education_level": education_level,
        "num_skills": num_skills,
        "location_index": location_index,
        "current_salary_lpa": current_salary_lpa
    }
    return call_remote_mcp("salary_gap_analysis", args)
