import json
import runpy
import sys
from unittest.mock import MagicMock, patch

import pytest
from starlette.responses import JSONResponse

from uptime_kuma_agent.mcp_server import (
    get_mcp_instance,
    mcp_server,
    register_monitors_tools,
    register_status_tools,
)


@pytest.mark.concept("CONCEPT:UK-OS.config.uka")
@pytest.mark.asyncio
async def test_uptime_kuma_monitors_tool():
    # Capture the tool function
    captured_tools = {}
    mock_mcp = MagicMock()

    def tool_decorator(*args, **kwargs):
        def decorator(func):
            captured_tools[func.__name__] = func
            return func

        return decorator

    mock_mcp.tool = tool_decorator

    # Register tools
    register_monitors_tools(mock_mcp)
    uptime_kuma_monitors = captured_tools["uptime_kuma_monitors"]

    # Mock client and context
    mock_client = MagicMock()
    mock_ctx = MagicMock()

    # 1. Test invalid params_json
    res = await uptime_kuma_monitors(
        action="get_monitors",
        params_json="{invalid json",
        client=mock_client,
        ctx=mock_ctx,
    )
    assert "error" in res
    assert "Invalid params_json" in res["error"]
    mock_ctx.info.assert_called_with("Executing tool...")

    # 2. Test get_monitors
    mock_client.get_monitors.return_value = [{"id": 1, "name": "mon1"}]
    res = await uptime_kuma_monitors(
        action="get_monitors",
        params_json=json.dumps({"foo": "bar"}),
        client=mock_client,
        ctx=None,
    )
    assert res == [{"id": 1, "name": "mon1"}]
    mock_client.get_monitors.assert_called_once_with(foo="bar")

    # 3. Test get_monitor
    mock_client.get_monitor.return_value = {"id": 1}
    res = await uptime_kuma_monitors(
        action="get_monitor",
        params_json=json.dumps({"id": 1}),
        client=mock_client,
        ctx=None,
    )
    assert res == {"id": 1}
    mock_client.get_monitor.assert_called_once_with(id=1)

    # 4. Test add_monitor
    mock_client.add_monitor.return_value = {"status": "added"}
    res = await uptime_kuma_monitors(
        action="add_monitor",
        params_json=json.dumps({"name": "new_mon"}),
        client=mock_client,
        ctx=None,
    )
    assert res == {"status": "added"}
    mock_client.add_monitor.assert_called_once_with(name="new_mon")

    # 5. Test edit_monitor
    mock_client.edit_monitor.return_value = {"status": "edited"}
    res = await uptime_kuma_monitors(
        action="edit_monitor",
        params_json=json.dumps({"id": 1, "name": "edit"}),
        client=mock_client,
        ctx=None,
    )
    assert res == {"status": "edited"}
    mock_client.edit_monitor.assert_called_once_with(id=1, name="edit")

    # 6. Test delete_monitor
    mock_client.delete_monitor.return_value = {"status": "deleted"}
    res = await uptime_kuma_monitors(
        action="delete_monitor",
        params_json=json.dumps({"id": 1}),
        client=mock_client,
        ctx=None,
    )
    assert res == {"status": "deleted"}
    mock_client.delete_monitor.assert_called_once_with(id=1)

    # 7. Test pause_monitor
    mock_client.pause_monitor.return_value = {"status": "paused"}
    res = await uptime_kuma_monitors(
        action="pause_monitor",
        params_json=json.dumps({"id": 1}),
        client=mock_client,
        ctx=None,
    )
    assert res == {"status": "paused"}
    mock_client.pause_monitor.assert_called_once_with(id=1)

    # 8. Test resume_monitor
    mock_client.resume_monitor.return_value = {"status": "resumed"}
    res = await uptime_kuma_monitors(
        action="resume_monitor",
        params_json=json.dumps({"id": 1}),
        client=mock_client,
        ctx=None,
    )
    assert res == {"status": "resumed"}
    mock_client.resume_monitor.assert_called_once_with(id=1)

    # 9. Test unknown action
    with pytest.raises(ValueError) as exc_info:
        await uptime_kuma_monitors(
            action="invalid_action", params_json="{}", client=mock_client, ctx=None
        )
    assert "list_actions" in str(exc_info.value)

    # 10. Test discovery (list_actions)
    res = await uptime_kuma_monitors(
        action="list_actions", params_json="{}", client=mock_client, ctx=None
    )
    assert "get_monitors" in res["actions"]


@pytest.mark.concept("CONCEPT:UK-OS.config.uka-2")
@pytest.mark.asyncio
async def test_uptime_kuma_status_tool():
    captured_tools = {}
    mock_mcp = MagicMock()

    def tool_decorator(*args, **kwargs):
        def decorator(func):
            captured_tools[func.__name__] = func
            return func

        return decorator

    mock_mcp.tool = tool_decorator

    register_status_tools(mock_mcp)
    uptime_kuma_status = captured_tools["uptime_kuma_status"]

    mock_client = MagicMock()
    mock_ctx = MagicMock()

    # 1. Test invalid params_json
    res = await uptime_kuma_status(
        action="info", params_json="{bad", client=mock_client, ctx=mock_ctx
    )
    assert "error" in res
    assert "Invalid params_json" in res["error"]

    # 2. Test get_heartbeats
    mock_client.get_heartbeats.return_value = ["heartbeat"]
    res = await uptime_kuma_status(
        action="get_heartbeats",
        params_json=json.dumps({"monitor_id": 1}),
        client=mock_client,
        ctx=None,
    )
    assert res == ["heartbeat"]
    mock_client.get_heartbeats.assert_called_once_with(monitor_id=1)

    # 3. Test info
    mock_client.info.return_value = {"version": "1.0"}
    res = await uptime_kuma_status(
        action="info", params_json="{}", client=mock_client, ctx=None
    )
    assert res == {"version": "1.0"}
    mock_client.info.assert_called_once_with()

    # 4. Test unknown action
    with pytest.raises(ValueError) as exc_info:
        await uptime_kuma_status(
            action="bad_action", params_json="{}", client=mock_client, ctx=None
        )
    assert "list_actions" in str(exc_info.value)

    # 5. Test discovery (list_actions)
    res = await uptime_kuma_status(
        action="list_actions", params_json="{}", client=mock_client, ctx=None
    )
    assert "info" in res["actions"]


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

    with patch("uptime_kuma_agent.mcp_server.create_mcp_server") as mock_create:
        mock_create.return_value = (MagicMock(), mock_mcp, [])
        get_mcp_instance()

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
        "agent_utilities.mcp.server_factory.create_mcp_server",
        return_value=(mock_args, mock_mcp, []),
    ):
        with patch("sys.argv", ["mcp_server.py"]):
            runpy.run_module("uptime_kuma_agent.mcp_server", run_name="__main__")

    mock_mcp.run.assert_called_once_with(transport="stdio")
