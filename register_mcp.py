import boto3
import json
import time
import sys

region = "us-east-1"
registry_id = "your-registry-id"  # Replace with your actual registry ID

bedrock_agentcore_control_client = boto3.client("bedrock-agentcore-control", region_name=region)
bedrock_agentcore_client = boto3.client("bedrock-agentcore", region_name=region)

# Define MCP server configuration with remote SSE transport and Bearer token
mcp_server_config = {
    "name": "app.fastmcp/salary-prediction",
    "description": "Salary Prediction MCP Server deployed on fastmcp.app",
    "version": "1.0.0",
    "transport": {
        "type": "sse",
        "url": "https://SalaryPredictionMCPServer.fastmcp.app/mcp/sse",
        "headers": {
            "Authorization": "Bearer your fastmcp api key"  # Replace with your actual FastMCP API key
        }
    }
}

print("Attempting to create registry record...")
try:
    record = bedrock_agentcore_control_client.create_registry_record(
        registryId=registry_id,
        name="salary-prediction-mcp",
        descriptorType="MCP",
        descriptors={
            "mcp": {
                "server": {
                    "inlineContent": json.dumps(mcp_server_config)
                }
            }
        }
    )
except Exception as e:
    print(f"Failed to create registry record: {e}")
    sys.exit(1)

record_id = record["recordArn"].split("/")[-1]
print(f"Record created successfully with ID: {record_id}")

# Wait for record to leave CREATING state
print("Waiting for record to leave CREATING state...")
while True:
    rec = bedrock_agentcore_control_client.get_registry_record(registryId=registry_id, recordId=record_id)
    rec_status = rec["status"]
    if rec_status != "CREATING":
        print(f"Record status: {rec_status}")
        if rec_status == "CREATE_FAILED":
            print(f"Error Details: {rec.get('statusReason', 'No reason provided')}")
        break
    print(f"  Status: {rec_status}, waiting 5s...")
    time.sleep(5)

if rec_status == "CREATE_FAILED":
    sys.exit(1)

# Step 2: Submit for approval
try:
    bedrock_agentcore_control_client.submit_registry_record_for_approval(
        registryId=registry_id,
        recordId=record_id
    )
    print("Submitted for approval")
except Exception as e:
    print(f"Failed to submit for approval: {e}")

# Step 3: Approve
try:
    bedrock_agentcore_control_client.update_registry_record_status(
        registryId=registry_id,
        recordId=record_id,
        status="APPROVED",
        statusReason="Approved for testing"
    )
    print("Approved")
except Exception as e:
    print(f"Failed to approve: {e}")

# Wait for record to become visible in search results
print("Waiting 15s for record indexing...")
time.sleep(15)

# Step 4: List records via control plane
results = bedrock_agentcore_control_client.list_registry_records(registryId=registry_id)
print("Registry records list:")
print(json.dumps(results["registryRecords"], indent=2, default=str))

# Step 5: Search approved record
try:
    results = bedrock_agentcore_client.search_registry_records(
        registryIds=[registry_id],
        searchQuery="Salary",
        maxResults=10
    )
    print("Search results:")
    print(json.dumps(results["registryRecords"], indent=2, default=str))
except Exception as e:
    print(f"Failed to search registry records: {e}")
