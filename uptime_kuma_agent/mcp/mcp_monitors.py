"""MCP tools for monitors operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action, run_blocking
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

        valid_actions = [
            "get_monitors",
            "get_monitor",
            "add_monitor",
            "edit_monitor",
            "delete_monitor",
            "pause_monitor",
            "resume_monitor",
        ]
        resolved = resolve_action(action, valid_actions, service="uptime-kuma-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_monitors":
            return await run_blocking(client.get_monitors, **kwargs)
        if action == "get_monitor":
            return await run_blocking(client.get_monitor, **kwargs)
        if action == "add_monitor":
            return await run_blocking(client.add_monitor, **kwargs)
        if action == "edit_monitor":
            return await run_blocking(client.edit_monitor, **kwargs)
        if action == "delete_monitor":
            return await run_blocking(client.delete_monitor, **kwargs)
        if action == "pause_monitor":
            return await run_blocking(client.pause_monitor, **kwargs)
        if action == "resume_monitor":
            return await run_blocking(client.resume_monitor, **kwargs)
        raise ValueError(f"Unknown action: {action}")
