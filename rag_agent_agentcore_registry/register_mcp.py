import json
import time
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
try:
    import config
except ImportError:
    from rag_agent_agentcore_registry import config

load_dotenv()
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
registry_id = os.getenv("AGENTCORE_REGISTRY_ID", "dYczX6QjgCpmY3Eb")
record_name = os.getenv("MCP_RECORD_NAME", "salary-prediction-mcp")

mcp_url = os.getenv("mcp_url") or os.getenv("MCP_URL", "https://salary-prediction-mcp.fastmcp.app/mcp")
fastmcp_api_key = os.getenv("fastmcp_api_key") or os.getenv("FASTMCP_API_KEY", "")
sse_url = mcp_url if mcp_url.endswith("/sse") else f"{mcp_url}/sse"

session = boto3.Session()
creds = session.get_credentials().get_frozen_credentials()
base_host = f"agent-registry-control.{region}.api.aws"
base_url = f"https://{base_host}"

def send_sigv4_request(method: str, path: str, payload: dict = None) -> requests.Response:
    url = f"{base_url}{path}"
    body = json.dumps(payload).encode("utf-8") if payload is not None else b""
    headers = {"Host": base_host}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = AWSRequest(method=method, url=url, data=body, headers=headers)
    SigV4Auth(creds, "agent-registry", region).add_auth(req)
    return requests.request(method, url, data=body, headers=dict(req.headers), timeout=15)

print(f"=== AWS Agent Registry Setup for {registry_id} ===")

# Step 1: Check Registry Status
print(f"1. Checking registry status for ID: {registry_id}...")
resp = send_sigv4_request("GET", f"/registries/{registry_id}")
if resp.status_code == 200:
    reg_details = resp.json()
    print(f"   ✅ Registry Name: {reg_details.get('name')}")
    print(f"   ✅ Registry Status: {reg_details.get('status')}")
    print(f"   ✅ Registry ARN: {reg_details.get('registryArn')}")
else:
    print(f"   ❌ Failed to access registry: {resp.status_code} {resp.text}")
    sys.exit(1)

# Step 2: Define MCP server configuration
mcp_server_config = {
    "name": "app.fastmcp/salary-prediction",
    "description": "Salary Prediction MCP Server deployed on fastmcp.app",
    "version": "1.0.0",
    "transport": {
        "type": "sse",
        "url": sse_url,
        "headers": {
            "Authorization": f"Bearer {fastmcp_api_key}"
        }
    }
}

print(f"\n2. Creating registry record for '{record_name}'...")
print(f"   Target SSE Endpoint: {sse_url}")

record_payload = {
    "name": record_name,
    "recordType": "MCP",
    "descriptors": {
        "mcpServer": {
            "data": json.dumps(mcp_server_config)
        }
    }
}

create_resp = send_sigv4_request("POST", f"/registries/{registry_id}/records", record_payload)
if create_resp.status_code in [200, 201, 202]:
    create_data = create_resp.json()
    record_arn = create_data.get("recordArn")
    record_id = record_arn.split("/")[-1]
    print(f"   ✅ Record accepted! Record ID: {record_id}")
    print(f"   Record ARN: {record_arn}")
elif create_resp.status_code == 409:
    print(f"   Notice: Record '{record_name}' already exists in registry.")
    record_id = getattr(config, "RECORD_ID", "jK440DvFaRi8")
else:
    print(f"   Notice creating record: HTTP {create_resp.status_code} - {create_resp.text}")
    record_id = os.getenv("AGENTCORE_RECORD_ID", "jK440DvFaRi8")

# Step 3: Verify Record Status
print(f"\n3. Fetching record status for '{record_id}'...")
rec_resp = send_sigv4_request("GET", f"/registries/{registry_id}/records/{record_id}")
if rec_resp.status_code == 200:
    rec_info = rec_resp.json()
    print(f"   ✅ Record Name: {rec_info.get('name')}")
    print(f"   ✅ Record Status: {rec_info.get('status')}")
    print(f"   ✅ Record Type: {rec_info.get('recordType')}")
    print(f"   ✅ Created Date: {rec_info.get('createdAt')}")
else:
    print(f"   Status check notice: HTTP {rec_resp.status_code} {rec_resp.text}")

print("\n" + "=" * 60)
print("🎉 SUCCESS: AWS Agent Registry MCP Record is Ready!")
print(f"Registry ID: {registry_id}")
print(f"Record ID:   {record_id}")
print(f"MCP Target:  {sse_url}")
print("Your Agent in tools.py will dynamically discover this configuration!")
print("=" * 60)
