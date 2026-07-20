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
import sys
from typing import Any

from agent_utilities.core.config import load_config
from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.server_factory import create_mcp_server
from agent_utilities.mcp.verbose_tools import register_tool_surface
from starlette.requests import Request
from starlette.responses import JSONResponse

from uptime_kuma_agent.auth import get_client

__version__ = "1.0.1"

logger = get_logger(name="uptime-kuma-agent")
logger.setLevel(logging.INFO)


def _optional_client_type() -> type[Any] | None:
    """Load the upstream client only when verbose reflection needs it.

    Condensed tool-schema discovery is intentionally offline and must remain
    available from a source checkout even when the runtime-only client package
    has not been installed. Actual tool execution still imports it fail-closed
    through :func:`get_client`.
    """
    try:
        from uptime_kuma_api import UptimeKumaApi
    except ImportError:
        return None
    return UptimeKumaApi


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
        except Exception:
            return {"error": "Operation failed"}

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
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ["get_heartbeats", "info"]
        resolved = resolve_action(action, valid_actions, service="uptime-kuma-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_heartbeats":
            return client.get_heartbeats(**kwargs)
        if action == "info":
            return client.info(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_ingest_tools(mcp: FastMCP):
    @mcp.tool(tags={"ingest"})
    async def uptime_ingest_monitors(
        params_json: str = Field(
            default="{}",
            description="JSON of options: {'include_heartbeats': bool} — also pull "
            "and ingest recent heartbeat samples per monitor.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Natively ingest Uptime Kuma monitors into epistemic-graph as typed nodes.

        Lists monitors via the Uptime Kuma client and pushes them (as
        :UptimeMonitor nodes, plus optional :HeartbeatStat timeseries samples linked
        via :heartbeatOf) through the authoritative native-ingest transaction.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        if ctx:
            ctx.info("Ingesting Uptime Kuma monitors into the knowledge graph...")
        import json as _json

        from uptime_kuma_agent.kg_ingest import ingest_monitors

        try:
            opts = _json.loads(params_json) if params_json else {}
        except Exception:  # noqa: BLE001
            return {"error": "Operation failed"}

        monitors = client.get_monitors()
        records = monitors if isinstance(monitors, list) else [monitors]
        records = [
            r.model_dump() if hasattr(r, "model_dump") else r
            for r in records
            if r is not None
        ]

        heartbeats = None
        if opts.get("include_heartbeats"):
            try:
                heartbeats = client.get_heartbeats()
            except Exception as e:  # noqa: BLE001 — heartbeats optional/best-effort
                logger.warning(
                    "get_heartbeats failed: error_type=%s", type(e).__name__
                )
                heartbeats = None

        result = ingest_monitors(records, heartbeats)
        return {"listed": len(records), "ingested": result}


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="uptime-kuma-agent MCP",
        version=__version__,
        instructions="uptime-kuma-agent MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    register_tool_surface(
        mcp,
        client_cls=_optional_client_type(),
        get_client=get_client,
        service="uptime-kuma-agent",
        tools_module=sys.modules[__name__],
    )

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
