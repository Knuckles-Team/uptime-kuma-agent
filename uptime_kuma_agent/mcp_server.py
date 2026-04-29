import warnings

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

# General urllib3/chardet mismatch warnings
warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from dotenv import find_dotenv, load_dotenv
from fastmcp import Context, FastMCP
from pydantic import Field

__version__ = "0.1.7"

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import (
    create_mcp_server,
    ctx_confirm_destructive,
    ctx_progress,
)

from .auth import get_client

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def register_monitors_tools(mcp: FastMCP):
    @mcp.tool(name="uptime-kuma-get-monitors", description="Get all monitors")
    def uptime_kuma_get_monitors(
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> list[dict[str, Any]]:
        return get_client().get_monitors()

    @mcp.tool(
        name="uptime-kuma-get-monitor", description="Get a specific monitor by ID"
    )
    def uptime_kuma_get_monitor(
        monitor_id: int,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        return get_client().get_monitor(monitor_id)

    @mcp.tool(name="uptime-kuma-add-monitor", description="Add a new monitor")
    def uptime_kuma_add_monitor(
        name: str,
        type: str,
        url: str | None = None,
        interval: int = 60,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        result = get_client().add_monitor(
            name=name, type=type, url=url, interval=interval
        )
        return {"msg": result}

    @mcp.tool(name="uptime-kuma-edit-monitor", description="Edit an existing monitor")
    def uptime_kuma_edit_monitor(
        monitor_id: int,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        result = get_client().edit_monitor(monitor_id)
        return {"msg": result}

    @mcp.tool(name="uptime-kuma-delete-monitor", description="Delete a monitor")
    async def uptime_kuma_delete_monitor(
        monitor_id: int,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        if not await ctx_confirm_destructive(ctx, "uptime kuma delete monitor"):
            return {"status": "cancelled", "message": "Operation cancelled by user"}
        await ctx_progress(ctx, 0, 100)
        result = get_client().delete_monitor(monitor_id)
        return {"msg": result}

    @mcp.tool(name="uptime-kuma-pause-monitor", description="Pause a monitor")
    def uptime_kuma_pause_monitor(
        monitor_id: int,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        result = get_client().pause_monitor(monitor_id)
        return {"msg": result}

    @mcp.tool(name="uptime-kuma-resume-monitor", description="Resume a monitor")
    def uptime_kuma_resume_monitor(
        monitor_id: int,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        result = get_client().resume_monitor(monitor_id)
        return {"msg": result}


def register_status_tools(mcp: FastMCP):
    @mcp.tool(
        name="uptime-kuma-get-status", description="Get status for a specific monitor"
    )
    def uptime_kuma_get_status(
        monitor_id: int,
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        beats = get_client().get_heartbeats(monitor_id)
        if isinstance(beats, list) and len(beats) > 0:
            return beats[-1]
        return {}

    @mcp.tool(
        name="uptime-kuma-get-uptime", description="Get uptime percentages for monitors"
    )
    def uptime_kuma_get_uptime(
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> dict[str, Any]:
        return get_client().info()


def register_prompts(mcp: FastMCP):
    @mcp.prompt(
        name="uptime-kuma-summary",
        description="Get a summary of Uptime Kuma monitors and their status.",
    )
    def uptime_kuma_summary() -> str:
        return "List all monitors, their type, and check their current status."


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    load_dotenv(find_dotenv())

    args, mcp, middlewares = create_mcp_server(
        name="uptime-kuma",
        version=__version__,
        instructions="Uptime Kuma Agent MCP Server",
    )

    registered_tags = []

    if to_boolean(os.getenv("MONITORSTOOL", "True")):
        register_monitors_tools(mcp)
        registered_tags.append("monitors")

    if to_boolean(os.getenv("STATUSTOOL", "True")):
        register_status_tools(mcp)
        registered_tags.append("status")

    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares, registered_tags


def mcp_server():
    mcp, args, middlewares, registered_tags = get_mcp_instance()

    print(f"Uptime Kuma Agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {registered_tags}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error(f"Invalid transport: {args.transport}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
