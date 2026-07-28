"""MCP tools for status operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from uptime_kuma_agent.auth import get_client


def register_status_tools(mcp: FastMCP):
    @mcp.tool(tags={"status"})
    async def uptime_kuma_status(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_heartbeats', 'info'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage uptime kuma status operations."""
        if ctx:
            ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Invalid params_json: expected a JSON object"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["get_heartbeats", "info"]
        resolved = resolve_action(action, valid_actions, service="uptime-kuma-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_heartbeats":
            return await run_blocking(client.get_heartbeats, **kwargs)
        if action == "info":
            return await run_blocking(client.info, **kwargs)
        raise ValueError(f"Unknown action: {action}")
