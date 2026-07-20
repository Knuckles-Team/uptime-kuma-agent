"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_monitors`` seam with a fake engine
client (no engine required), asserting the txn add_node/commit + edge calls and the
Uptime Kuma monitor -> :UptimeMonitor / heartbeat -> :HeartbeatStat mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError

from uptime_kuma_agent.kg_ingest import (
    ingest_documents,
    ingest_entities,
    ingest_monitors,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def add_edge(self, txn, source, target, props):
        self.edges.append((source, target, props))

    def commit(self, txn):
        self.committed = True
        return True


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "UptimeMonitor", "name": "web"},
            {"id": "b", "node_type": "HeartbeatStat"},
        ],
        [{"source": "b", "target": "a", "relationship": "heartbeatOf"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "uptime-kuma-agent"
    assert c.txn.nodes["a"]["domain"] == "uptimekuma"
    assert c.txn.edges == [("b", "a", {"relationship": "heartbeatOf"})]


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
        graph="__commons__",
    )
    # 1 monitor + 2 heartbeats = 3 nodes; 2 heartbeatOf edges
    assert res == {"nodes": 3, "edges": 2}
    mon = c.txn.nodes["uptimekuma:monitor:3"]
    assert mon["node_type"] == "UptimeMonitor"
    assert mon["monitorType"] == "http"
    assert mon["monitorUrl"] == "https://api.example/health"
    assert mon["checkInterval"] == 60
    assert mon["monitorActive"] is True
    assert mon["uptimeKumaId"] == "3"
    # heartbeat nodes are typed + linked
    hb_ids = [k for k in c.txn.nodes if k.startswith("uptimekuma:heartbeat:3:")]
    assert len(hb_ids) == 2
    up = c.txn.nodes["uptimekuma:heartbeat:3:2026-07-04T10-00-00"]
    assert up["node_type"] == "HeartbeatStat"
    assert up["heartbeatStatus"] == 1
    assert up["ping"] == 12.5
    assert all(
        rel[1] == "uptimekuma:monitor:3" and rel[2] == {"relationship": "heartbeatOf"}
        for rel in c.txn.edges
    )


def test_ingest_monitors_without_heartbeats():
    c = _FakeClient()
    res = ingest_monitors(
        [{"id": 1, "name": "web", "type": "http"}], client=c, graph="__commons__"
    )
    assert res == {"nodes": 1, "edges": 0}
    assert c.txn.nodes["uptimekuma:monitor:1"]["node_type"] == "UptimeMonitor"


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "uptimekuma:doc:1", "text": "monitor api is degraded", "title": "api"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.txn.nodes["uptimekuma:doc:1"]
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
