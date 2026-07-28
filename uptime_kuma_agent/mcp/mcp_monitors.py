"""MCP tools for monitors operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from uptime_kuma_agent.auth import get_client


def _normalize_monitor_identifier(kwargs: dict) -> dict:
    """Translate the public monitor identifier to the upstream client's ``id_``."""
    normalized = dict(kwargs)
    supplied = [
        key for key in ("monitor_id", "id", "id_") if normalized.get(key) is not None
    ]
    if not supplied:
        raise ValueError("params_json must include 'monitor_id'")
    if len(supplied) > 1:
        raise ValueError(
            "params_json must include only one of 'monitor_id', 'id', or 'id_'"
        )
    normalized["id_"] = normalized.pop(supplied[0])
    return normalized


def register_monitors_tools(mcp: FastMCP):
    @mcp.tool(tags={"monitors"})
    async def uptime_kuma_monitors(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_monitors', 'get_monitor', 'add_monitor', 'edit_monitor', 'delete_monitor', 'pause_monitor', 'resume_monitor'"
        ),
        params_json: str = Field(
            default="{}",
            description=(
                "JSON action parameters. Monitor-specific actions use "
                "'monitor_id' (for example, {\"monitor_id\": 95})."
            ),
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
        except Exception:
            return {"error": "Invalid params_json: expected a JSON object"}

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
            kwargs = _normalize_monitor_identifier(kwargs)
            return await run_blocking(client.get_monitor, **kwargs)
        if action == "add_monitor":
            return await run_blocking(client.add_monitor, **kwargs)
        if action == "edit_monitor":
            kwargs = _normalize_monitor_identifier(kwargs)
            return await run_blocking(client.edit_monitor, **kwargs)
        if action == "delete_monitor":
            kwargs = _normalize_monitor_identifier(kwargs)
            return await run_blocking(client.delete_monitor, **kwargs)
        if action == "pause_monitor":
            kwargs = _normalize_monitor_identifier(kwargs)
            return await run_blocking(client.pause_monitor, **kwargs)
        if action == "resume_monitor":
            kwargs = _normalize_monitor_identifier(kwargs)
            return await run_blocking(client.resume_monitor, **kwargs)
        raise ValueError(f"Unknown action: {action}")
