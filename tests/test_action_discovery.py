"""Action-discovery standardization tests for uptime-kuma-agent.

Verifies that the action-routed MCP tools expose ``list_actions`` discovery and
raise a rich did-you-mean error (mentioning ``list_actions``) on unknown actions
via the shared ``agent_utilities.mcp.action_dispatch`` helper.
"""

from unittest.mock import MagicMock

import pytest

from uptime_kuma_agent.mcp_server import (
    register_monitors_tools,
    register_status_tools,
)


def _capture(register) -> dict:
    captured: dict = {}
    mock_mcp = MagicMock()

    def tool_decorator(*args, **kwargs):
        def decorator(func):
            captured[func.__name__] = func
            return func

        return decorator

    mock_mcp.tool = tool_decorator
    register(mock_mcp)
    return captured


@pytest.mark.asyncio
async def test_monitors_list_actions_and_did_you_mean():
    tool = _capture(register_monitors_tools)["uptime_kuma_monitors"]
    client = MagicMock()

    res = await tool(action="list_actions", params_json="{}", client=client, ctx=None)
    assert "get_monitors" in res["actions"]
    assert res["service"] == "uptime-kuma-agent"

    with pytest.raises(ValueError) as exc_info:
        await tool(action="bogus", params_json="{}", client=client, ctx=None)
    assert "list_actions" in str(exc_info.value)


@pytest.mark.asyncio
async def test_status_list_actions_and_did_you_mean():
    tool = _capture(register_status_tools)["uptime_kuma_status"]
    client = MagicMock()

    res = await tool(action="actions", params_json="{}", client=client, ctx=None)
    assert "info" in res["actions"]
    assert "get_heartbeats" in res["actions"]

    with pytest.raises(ValueError) as exc_info:
        await tool(action="nope", params_json="{}", client=client, ctx=None)
    assert "list_actions" in str(exc_info.value)
