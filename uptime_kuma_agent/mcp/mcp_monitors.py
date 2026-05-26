"""MCP tools for monitors operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from uptime_kuma_agent.auth import get_client


def register_monitors_tools(mcp: FastMCP):
    @mcp.tool(tags={"monitors"})
    async def uptime_kuma_monitors(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_monitors', 'get_monitor', 'add_monitor', 'edit_monitor', 'delete_monitor', 'pause_monitor', 'resume_monitor'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage uptime kuma monitors operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_monitors":
            return client.get_monitors(**kwargs)
        if action == "get_monitor":
            return client.get_monitor(**kwargs)
        if action == "add_monitor":
            return client.add_monitor(**kwargs)
        if action == "edit_monitor":
            return client.edit_monitor(**kwargs)
        if action == "delete_monitor":
            return client.delete_monitor(**kwargs)
        if action == "pause_monitor":
            return client.pause_monitor(**kwargs)
        if action == "resume_monitor":
            return client.resume_monitor(**kwargs)
        raise ValueError(f"Unknown action: {action}")
