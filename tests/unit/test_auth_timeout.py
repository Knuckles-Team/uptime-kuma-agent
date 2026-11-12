"""CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R006: a slow Uptime Kuma still connects."""

import json
from importlib import resources
from unittest.mock import MagicMock, patch

import uptime_kuma_agent.auth as auth


def test_default_timeout_covers_a_slow_login(monkeypatch):
    monkeypatch.delenv("UPTIME_KUMA_TIMEOUT", raising=False)
    monkeypatch.setenv("UPTIME_KUMA_USERNAME", "u")
    monkeypatch.setenv("UPTIME_KUMA_PASSWORD", "p")
    monkeypatch.setattr(auth, "_client", None)
    client = MagicMock()
    client.sio.connected = True
    client.sio.namespaces = {"/": "connected"}
    with patch("uptime_kuma_agent.auth._new_client", return_value=client) as new:
        auth.get_client()
    assert new.call_args.kwargs["timeout"] == 120


def test_operator_prompt_names_only_served_tools():
    path = (
        resources.files("uptime_kuma_agent")
        / "prompts"
        / "uptime-kuma-agent-operator.json"
    )
    tools = json.loads(path.read_text())["agent"]["tools"]
    assert "uptime_kuma_monitors" not in tools
    assert "uptime_kuma_status" not in tools
    assert "uptime_kuma_get_monitors" in tools
