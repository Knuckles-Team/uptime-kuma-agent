import pytest
from uptime_kuma_agent.mcp_server import get_mcp_instance
from fastmcp import FastMCP

def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully."""
    mcp, args, middlewares, registered_tags = get_mcp_instance()
    assert isinstance(mcp, FastMCP)
    assert "uptime-kuma" in mcp.name
    assert len(registered_tags) > 0

def test_import_uptime_kuma_agent():
    """Test that the package can be imported."""
    import uptime_kuma_agent
    assert uptime_kuma_agent.__version__ is not None
