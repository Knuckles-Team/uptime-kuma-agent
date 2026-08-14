"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_monitors`` seam with a fake engine
client (no engine required), asserting the txn add_node/commit + edge calls and the
Uptime Kuma monitor -> :UptimeMonitor / heartbeat -> :HeartbeatStat mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.security.brain_context import ActorContext, use_actor
from agent_utilities.models.company_brain import ActorType
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session

from uptime_kuma_agent.kg_ingest import (
    ingest_documents,
    ingest_entities,
    ingest_monitors,
)


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "UptimeMonitor", "name": "web"},
            {"id": "b", "node_type": "HeartbeatStat"},
        ],
        [{"source": "b", "target": "a", "relationship": "heartbeatOf"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(c.changes.applied) == 1
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "uptime-kuma-agent"
    assert c.nodes.values["a"]["domain"] == "uptimekuma"
    assert c.changes.edges == [("b", "a", {"relationship": "heartbeatOf"})]


def test_ingest_monitors_maps_monitor_and_heartbeats():
    c = _FakeClient()
    res = ingest_monitors(
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
        client=c,
    )
    # 1 monitor + 2 heartbeats = 3 nodes; 2 heartbeatOf edges
    assert res == {"nodes": 3, "edges": 2}
    mon = c.nodes.values["uptimekuma:monitor:3"]
    assert mon["node_type"] == "UptimeMonitor"
    assert mon["monitorType"] == "http"
    assert mon["monitorUrl"] == "https://api.example/health"
    assert mon["checkInterval"] == 60
    assert mon["monitorActive"] is True
    assert mon["uptimeKumaId"] == "3"
    # heartbeat nodes are typed + linked
    hb_ids = [k for k in c.nodes.values if k.startswith("uptimekuma:heartbeat:3:")]
    assert len(hb_ids) == 2
    up = c.nodes.values["uptimekuma:heartbeat:3:2026-07-04T10-00-00"]
    assert up["node_type"] == "HeartbeatStat"
    assert up["heartbeatStatus"] == 1
    assert up["ping"] == 12.5
    assert all(
        rel[1] == "uptimekuma:monitor:3" and rel[2] == {"relationship": "heartbeatOf"}
        for rel in c.changes.edges
    )


def test_ingest_monitors_without_heartbeats():
    c = _FakeClient()
    res = ingest_monitors(
        [{"id": 1, "name": "web", "type": "http"}], client=c
    )
    assert res == {"nodes": 1, "edges": 0}
    assert c.nodes.values["uptimekuma:monitor:1"]["node_type"] == "UptimeMonitor"


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "uptimekuma:doc:1", "text": "monitor api is degraded", "title": "api"}],
        client=c,
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.nodes.values["uptimekuma:doc:1"]
    assert node["node_type"] == "Document"
    assert node["text"] == "monitor api is degraded"


def test_retired_node_type_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities(
            [{"id": "retired", "type": "RetiredAlias"}],
            client=_FakeClient(),
        )


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
