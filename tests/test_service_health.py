"""Service health is projected through the actual MCP tool."""

import asyncio
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from fastmcp import Client

from uptime_kuma_agent.service_health import MAX_MONITORS, service_health

ROOT = Path(__file__).resolve().parents[1]


class FakeProvider:
    def get_monitors(self):
        return [
            {"id": 1, "name": "Example service", "password": "private"},
            {"id": 2, "name": "New service"},
        ]

    def get_heartbeats(self):
        return {
            1: [
                {"time": "2026-01-01 00:02:00", "status": 0},
                {"time": "2026-01-01 00:01:00", "status": 1},
            ]
        }


@pytest.mark.spec("CONN-UPTIME-KUMA-AGENT-SERVICE-HEALTH-R001")
def test_served_health_contract():
    from scion_sdk.access_contract import parse_access_contracts

    from uptime_kuma_agent.mcp_server import get_mcp_instance

    fixture = json.loads((ROOT / "tests/fixtures/service_health.json").read_text())
    (contract,) = parse_access_contracts(
        (ROOT / "uptime_kuma_agent/ontology/access_contracts.ttl").read_text()
    )
    assert {field for _, field in contract.predicates} == {
        "name",
        "status",
        "last_check",
    }

    async def run():
        with (
            patch(
                "sys.argv", ["connector", "--transport", "stdio", "--auth-type", "none"]
            ),
            patch(
                "uptime_kuma_agent.mcp_server.get_client", return_value=FakeProvider()
            ),
        ):
            server, _, _ = get_mcp_instance()
            async with Client(server) as client:
                return await client.call_tool(
                    contract.operation, {}, raise_on_error=False
                )

    result = asyncio.run(run())
    assert not result.is_error
    rows = (
        result.data if result.data is not None else json.loads(result.content[0].text)
    )
    assert rows == fixture
    assert "private" not in str(rows)


def test_invalid_or_ambiguous_source_data_is_refused():
    provider = FakeProvider()
    with pytest.raises(ValueError):
        service_health(provider.get_monitors() * (MAX_MONITORS + 1), {})
    with pytest.raises(ValueError):
        service_health(provider.get_monitors(), {1: [{"time": "bad", "status": 1}]})
    with pytest.raises(ValueError):
        service_health(provider.get_monitors(), {1: [], "1": []})
    with pytest.raises(ValueError):
        service_health(
            provider.get_monitors(),
            {
                1: [
                    {"time": "2026-01-01T00:00:00Z", "status": 1},
                    {"time": "2026-01-01T00:00:00Z", "status": 0},
                ]
            },
        )
