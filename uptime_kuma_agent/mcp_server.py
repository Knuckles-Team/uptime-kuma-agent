#!/usr/bin/python
import warnings
from importlib.metadata import version as package_version

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

from scion_sdk.config import load_config
from scion_sdk.connector import build_server
from scion_sdk.mcp.concurrency import run_blocking
from scion_sdk.mcp.tool_surface import register_tool_surface
from starlette.requests import Request
from starlette.responses import JSONResponse

from uptime_kuma_agent.auth import get_client
from uptime_kuma_agent.service_health import MonitorHealth, service_health

__version__ = package_version("uptime-kuma-agent")

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
        from uptime_kuma_agent.api_client import operations_class

        return operations_class()
    except ImportError:
        return None


def register_status_tools(mcp: FastMCP):
    @mcp.tool(tags={"status"})
    async def uptime_kuma_service_health(client=Depends(get_client)) -> list[MonitorHealth]:
        """Read monitor health from the latest observed heartbeat.

        A monitor with no heartbeat is returned with status ``unknown``."""
        monitors = await run_blocking(client.get_monitors)
        heartbeats = await run_blocking(client.get_heartbeats)
        return service_health(monitors, heartbeats)


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
        """Natively ingest Uptime Kuma monitors into medulla as typed nodes.

        Lists monitors via the Uptime Kuma client and pushes them (as
        :UptimeMonitor nodes, plus optional :HeartbeatStat timeseries samples linked
        via :heartbeatOf) through the authoritative native-ingest transaction.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        if ctx:
            await ctx.info("Ingesting Uptime Kuma monitors into the knowledge graph...")
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
                logger.warning("get_heartbeats failed: error_type=%s", type(e).__name__)
                heartbeats = None

        result = await ingest_monitors(records, heartbeats)
        return {"listed": len(records), "ingested": result}


def get_mcp_instance(*, command_args=None) -> tuple[Any, ...]:
    """Initialize the legacy MCP entry point with its existing configuration."""
    load_config()
    args, mcp = build_server("uptime_kuma_agent", command_args=command_args)
    return mcp, args, list(mcp.middleware)


def register_server_surface(mcp: FastMCP) -> None:
    """Reuse the existing custom health route and tool registrar in order."""

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
