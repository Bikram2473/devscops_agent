import os
import json
from typing import TypedDict, Optional
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

# --- NEW MCP IMPORTS ---
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

# 1. Define the Memory (State)
class TriageState(TypedDict):
    service_name: str
    error_type: str
    stack_trace: str
    root_cause_analysis: Optional[str]
    github_issue_link: Optional[str]
    status: str
    iterations: int

# 2. Define the AI diagnostician Node
def diagnostic_node(state: TriageState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    prompt = f"Analyze this stack trace from {state['service_name']}. Error: {state['error_type']}\nTrace: {state['stack_trace']}\nProvide a brief root cause."

    response = llm.invoke(prompt)
    return {"root_cause_analysis": response.content, "status": "diagnosed"}

# 3. Define the MCP GitHub Integration Node
async def mcp_github_node(state: TriageState):
    # Setup MCP Server connection to GitHub using the official Node.js server
    server_params = StdioServerParameters(
        command="npx.cmd",          # Windows uses npx.cmd (Mac/Linux users would use just "npx")
        args=["-y", "@modelcontextprotocol/server-github"],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
            "PATH": os.getenv("PATH")               # Required for Python to locate Node.js
        }
    )

    # Connect to the MCP Server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Format the bug report payload
            title = f"🚨 Crash Report: {state['service_name']} - {state['error_type']}"
            body = (
                f"### Auto-Generated Triage Report\n\n"
                f"**Service:** {state['service_name']}\n"
                f"**Error:** `{state['error_type']}`\n\n"
                f"**AI Root Cause Analysis:**\n{state['root_cause_analysis']}\n\n"
                f"**Stack Trace:**\n```python\n{state['stack_trace']}\n```"
            ) 

            # Tell the MCP server to execute the 'create_issue' tool on your GitHub
            result = await session.call_tool("create_issue", arguments={
                "owner": "Bikram2473",
                "repo": "devscops_triage_test",
                "title": title,
                "body": body
            })

            # The MCP server returns a JSON string containing the new live issue data
            try:
                issue_json = json.loads(result.context[0].text)
                issue_url = issue_json.get("html_url", "URL extracted successfully!")
            except Exception:
                issue_url = str(result.content[0].text)

            return {"github_issue_link": issue_url, "status": "ticket_created"}

# 4. Build the Graph
workflow = StateGraph(TriageState)
workflow.add_node("diagnostician", diagnostic_node)
workflow.add_node("mcp_integrator", mcp_github_node)

workflow.add_edge(START, "diagnostician")
workflow.add_edge("diagnostician", "mcp_integrator")
workflow.add_edge("mcp_integrator", END)

compiled_triage_agent = workflow.compile()

# 5. Background Task Executor
async def process_incident(log_data: dict):
    initial_state = {
        "service_name": log_data["service_name"],
        "error_type": log_data["error_type"],
        "stack_trace": log_data["stack_trace"],
        "root_cause_analysis": None,
        "github_issue_link": None,
        "status": "ingested",
        "iterations": 0
    }

    # We use await ainvoke() because the MCP node runs asynchronously now
    final_state = await compiled_triage_agent.ainvoke(initial_state)
    print(f"\n[SUCCESS] Real Incident Logged on GitHub: \n{final_state['github_issue_link']}")