import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()

MODEL = os.getenv("VERTEX_MODEL", "gemini-2.5-flash")


def build_workiq_server_params() -> StdioServerParameters:
    use_npx = os.getenv("WORKIQ_USE_NPX", "true").lower() == "true"

    if use_npx:
        package_name = os.getenv("WORKIQ_NPX_PACKAGE", "@microsoft/workiq@latest")
        return StdioServerParameters(
            command="npx",
            args=["-y", package_name, "mcp"],
        )

    command = os.getenv("WORKIQ_COMMAND", "workiq")
    args = os.getenv("WORKIQ_ARGS", "mcp").split()
    return StdioServerParameters(
        command=command,
        args=args,
    )


root_agent = LlmAgent(
    name="workiq_vertex_demo",
    model=MODEL,
    instruction=(
        "You are a Microsoft 365 productivity assistant. "
        "For questions about meetings, emails, documents, Teams messages, or people, "
        "use the WorkIQ tools. "
        "Be concise, useful, and business-friendly. "
        "If the WorkIQ tool returns insufficient detail, say so clearly."
    ),
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=build_workiq_server_params(),
                timeout=60,
            ),
            tool_filter=["ask_work_iq", "accept_eula", "get_debug_link"],
        )
    ],
)
