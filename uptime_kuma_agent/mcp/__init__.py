"""MCP tool registration modules for uptime-kuma-agent.

Auto-generated during ecosystem standardization.
Each domain has its own module with a register_*_tools function.
"""

from uptime_kuma_agent.mcp.mcp_monitors import register_monitors_tools
from uptime_kuma_agent.mcp.mcp_status import register_status_tools

__all__ = [
    "register_monitors_tools",
    "register_status_tools",
]
