import importlib
import json
import runpy
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from starlette.responses import JSONResponse

from uptime_kuma_agent.mcp_server import mcp_server, register_status_tools

# The package re-exports the mcp_server function, shadowing the submodule attribute.
mcp_server_module = importlib.import_module("uptime_kuma_agent.mcp_server")


@pytest.mark.concept("CONCEPT:UK-OS.config.uka-2")
@pytest.mark.asyncio
async def test_uptime_kuma_service_health_tool():
    captured_tools = {}
    mock_mcp = MagicMock()

    def tool_decorator(*args, **kwargs):
        def decorator(func):
            captured_tools[func.__name__] = func
            return func

        return decorator

    mock_mcp.tool = tool_decorator

    register_status_tools(mock_mcp)
    # The hand-written status tools hold no action router: one typed tool each.
    assert set(captured_tools) == {"uptime_kuma_service_health"}

    mock_client = MagicMock()
    mock_client.get_monitors.return_value = [{"id": 1, "name": "mon1", "active": True}]
    mock_client.get_heartbeats.return_value = {
        1: [{"status": 1, "time": "2026-01-01 00:00:00"}]
    }
    res = await captured_tools["uptime_kuma_service_health"](client=mock_client)
    assert isinstance(res, list)
    mock_client.get_monitors.assert_called_once_with()
    mock_client.get_heartbeats.assert_called_once_with()


@pytest.mark.concept("CONCEPT:UK-OS.config.uka-3")
@pytest.mark.asyncio
async def test_health_check_route():
    # Capture custom route
    captured_routes = {}
    mock_mcp = MagicMock()

    def custom_route_decorator(path, methods=None):
        assert methods == ["GET"]

        def decorator(func):
            captured_routes[path] = func
            return func

        return decorator

    mock_mcp.custom_route = custom_route_decorator

    mcp_server_module.register_server_surface(mock_mcp)

    assert "/health" in captured_routes
    health_check_func = captured_routes["/health"]

    # Call health check with mock Request
    mock_request = MagicMock()
    response = await health_check_func(mock_request)
    assert isinstance(response, JSONResponse)
    assert json.loads(bytes(response.body).decode()) == {"status": "OK"}


@pytest.mark.concept("CONCEPT:UK-OS.config.uka")
def test_mcp_server_cli_runners():
    # Test mcp_server for various transport flags
    mock_mcp = MagicMock()
    mock_args = MagicMock()
    mock_args.host = "127.0.0.1"
    mock_args.port = 8888
    mock_args.auth_type = "none"

    # Test stdio
    mock_args.transport = "stdio"
    with patch(
        "uptime_kuma_agent.mcp_server.get_mcp_instance",
        return_value=(mock_mcp, mock_args, []),
    ):
        mcp_server()
        mock_mcp.run.assert_called_once_with(transport="stdio")

    # Test streamable-http
    mock_mcp.reset_mock()
    mock_args.transport = "streamable-http"
    with patch(
        "uptime_kuma_agent.mcp_server.get_mcp_instance",
        return_value=(mock_mcp, mock_args, []),
    ):
        mcp_server()
        mock_mcp.run.assert_called_once_with(
            transport="streamable-http", host="127.0.0.1", port=8888
        )

    # Test sse
    mock_mcp.reset_mock()
    mock_args.transport = "sse"
    with patch(
        "uptime_kuma_agent.mcp_server.get_mcp_instance",
        return_value=(mock_mcp, mock_args, []),
    ):
        mcp_server()
        mock_mcp.run.assert_called_once_with(
            transport="sse", host="127.0.0.1", port=8888
        )

    # Test invalid transport
    mock_mcp.reset_mock()
    mock_args.transport = "invalid-transport"
    with patch(
        "uptime_kuma_agent.mcp_server.get_mcp_instance",
        return_value=(mock_mcp, mock_args, []),
    ):
        with patch("sys.exit") as mock_exit:
            mcp_server()
            mock_exit.assert_called_once_with(1)


@pytest.mark.concept("CONCEPT:UK-OS.config.uka")
def test_import_warning_handling():
    # Mock requests.exceptions to trigger ImportError when importing RequestsDependencyWarning
    with patch.dict(sys.modules, {"requests.exceptions": None}):
        import importlib

        importlib.reload(sys.modules["uptime_kuma_agent.mcp_server"])


@pytest.mark.concept("CONCEPT:UK-OS.config.uka")
def test_mcp_server_main_block():
    mock_mcp = MagicMock()
    mock_args = MagicMock()
    mock_args.transport = "stdio"

    with patch(
        "scion_sdk.mcp.server.create_mcp_server",
        return_value=(mock_args, mock_mcp, []),
    ):
        with patch("sys.argv", ["mcp_server.py"]):
            runpy.run_path(str(Path(mcp_server_module.__file__)), run_name="__main__")

    mock_mcp.run.assert_called_once_with(transport="stdio")
