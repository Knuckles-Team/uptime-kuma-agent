import runpy
from unittest.mock import patch

import pytest


@pytest.mark.concept("CONCEPT:UK-OS.config.uka-4")
@patch("uptime_kuma_agent.mcp_server.mcp_server")
def test_main_execution(mock_mcp_server):
    # Use runpy to execute the __main__.py file, mocking the actual server function.
    # agent_server.py (A2A/LLM-agent entrypoint) was removed (EH-484 SDK-GAP);
    # __main__ now runs the MCP server.
    runpy.run_module("uptime_kuma_agent.__main__", run_name="__main__")
    mock_mcp_server.assert_called_once()
