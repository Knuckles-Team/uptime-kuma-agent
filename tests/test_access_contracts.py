"""Monitor and heartbeat access contracts bind fields the served tools return."""

import asyncio
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from fastmcp import Client
from scion_sdk.access_contract import parse_access_contracts

ROOT = Path(__file__).resolve().parents[1]


class RecordingProvider:
    def __init__(self):
        rec = ROOT / "tests/recordings"
        self.monitors = json.loads((rec / "uptimemonitor.json").read_text())
        self.heartbeats = json.loads((rec / "heartbeatstat.json").read_text())

    def get_monitors(self):
        return self.monitors

    def get_heartbeats(self):
        return self.heartbeats


@pytest.mark.spec("CONN-UPTIME-KUMA-AGENT-CONNECTOR-CONTENT-R002")
def test_monitor_and_heartbeat_contracts():
    from uptime_kuma_agent.mcp_server import get_mcp_instance

    contracts = {
        c.operation: c
        for c in parse_access_contracts(
            (ROOT / "uptime_kuma_agent/ontology/access_contracts.ttl").read_text()
        )
    }
    monitors = contracts["uptime_kuma_get_monitors"]
    heartbeats = contracts["uptime_kuma_get_heartbeats"]
    assert monitors.class_iri.endswith("#UptimeMonitor")
    assert heartbeats.class_iri.endswith("#HeartbeatStat")
    assert monitors.key_field == "id"
    assert heartbeats.pagination == monitors.pagination == "none"

    async def call(contract):
        with (
            patch(
                "sys.argv", ["connector", "--transport", "stdio", "--auth-type", "none"]
            ),
            patch(
                "uptime_kuma_agent.mcp_server.get_client",
                return_value=RecordingProvider(),
            ),
        ):
            server, _, _ = get_mcp_instance()
            async with Client(server) as client:
                result = await client.call_tool(
                    contract.operation, {}, raise_on_error=False
                )
        assert not result.is_error
        return json.loads(result.content[0].text)

    rows = asyncio.run(call(monitors))
    assert rows == RecordingProvider().monitors
    assert {f for _, f in monitors.predicates} <= set(rows[0])
    by_monitor = asyncio.run(call(heartbeats))
    beats = [b for group in by_monitor.values() for b in group]
    assert beats and {f for _, f in heartbeats.predicates} <= set(beats[0])
    assert heartbeats.key_field in beats[0]
