#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from starlette.requests import Request
from starlette.responses import JSONResponse

from uptime_kuma_agent.auth import get_client

__version__ = "0.25.0"

logger = get_logger(name="uptime-kuma-agent")
logger.setLevel(logging.INFO)


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
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "get_heartbeats":
            return client.get_heartbeats(**kwargs)
        if action == "info":
            return client.info(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="uptime-kuma-agent MCP",
        version=__version__,
        instructions="uptime-kuma-agent MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    DEFAULT_MONITORSTOOL = to_boolean(os.getenv("MONITORSTOOL", "True"))
    if DEFAULT_MONITORSTOOL:
        register_monitors_tools(mcp)
    DEFAULT_STATUSTOOL = to_boolean(os.getenv("STATUSTOOL", "True"))
    if DEFAULT_STATUSTOOL:
        register_status_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"uptime-kuma-agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
