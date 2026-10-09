"""Knowledge-graph ingestion coverage for the Uptime Kuma connector.

Exercises the real ``ingest_entities`` / ``ingest_monitors`` seam against a fake
``agent_connector_sdk.ingest`` transport (no engine required), asserting the
submitted records/relationships and the Uptime Kuma monitor -> :UptimeMonitor /
heartbeat -> :HeartbeatStat mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest

from uptime_kuma_agent.kg_ingest import (
    ingest_documents,
    ingest_entities,
    ingest_monitors,
)


class _FakeTransport:
    """Fakes the transport boundary one level below ``KnowledgeIngest``."""

    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def source_status(self, connector: str, stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: bytes) -> str:
        raise AssertionError("this connector's ingestion carries no media")


@pytest.fixture
def ingest() -> tuple[KnowledgeIngest, _FakeTransport]:
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "UptimeMonitor", "name": "web"},
            {"id": "b", "node_type": "HeartbeatStat"},
        ],
        [{"source": "b", "target": "a", "relationship": "heartbeatOf"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    request = transport.requests[0]
    ids = {record.record_id for record in request.records}
    assert ids == {"a", "b"}
    assert request.relationships[0].relation_reference.endswith("/heartbeatOf")


async def test_ingest_monitors_maps_monitor_and_heartbeats(ingest):
    service, transport = ingest
    res = await ingest_monitors(
        [
            {
                "id": 3,
                "name": "api",
                "type": "http",
                "url": "https://api.example/health",
                "interval": 60,
                "active": True,
            }
        ],
        {
            3: [
                {"status": 1, "time": "2026-07-04 10:00:00", "ping": 12.5, "msg": ""},
                {
                    "status": 0,
                    "time": "2026-07-04 10:01:00",
                    "ping": None,
                    "msg": "down",
                },
            ]
        },
        ingest=service,
    )
    # 1 monitor + 2 heartbeats = 3 nodes; 2 heartbeatOf edges
    assert res == {"nodes": 3, "edges": 2}
    request = transport.requests[0]
    by_id = {record.record_id: record for record in request.records}
    mon = by_id["uptimekuma:monitor:3"]
    assert mon.mapping_reference.endswith("/UptimeMonitor")
    assert mon.payload["monitorType"] == "http"
    assert mon.payload["monitorUrl"] == "https://api.example/health"
    assert mon.payload["checkInterval"] == 60
    assert mon.payload["monitorActive"] is True
    assert mon.payload["uptimeKumaId"] == "3"
    hb_ids = [k for k in by_id if k.startswith("uptimekuma:heartbeat:3:")]
    assert len(hb_ids) == 2
    up = by_id["uptimekuma:heartbeat:3:2026-07-04T10-00-00"]
    assert up.mapping_reference.endswith("/HeartbeatStat")
    assert up.payload["heartbeatStatus"] == 1
    assert up.payload["ping"] == 12.5
    assert all(
        rel.target.record_id == "uptimekuma:monitor:3"
        and rel.relation_reference.endswith("/heartbeatOf")
        for rel in request.relationships
    )


async def test_ingest_monitors_without_heartbeats(ingest):
    service, transport = ingest
    res = await ingest_monitors([{"id": 1, "name": "web", "type": "http"}], ingest=service)
    assert res == {"nodes": 1, "edges": 0}
    request = transport.requests[0]
    assert request.records[0].record_id == "uptimekuma:monitor:1"


async def test_ingest_documents_writes_document_nodes(ingest):
    service, transport = ingest
    res = await ingest_documents(
        [{"id": "uptimekuma:doc:1", "text": "monitor api is degraded", "title": "api"}],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    request = transport.requests[0]
    node = request.records[0]
    assert node.mapping_reference.endswith("/Document")
    assert node.payload["text"] == "monitor api is degraded"


async def test_ingest_empty_entities_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)


async def test_ingest_empty_documents_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one document"):
        await ingest_documents([], ingest=service)
