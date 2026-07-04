"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_monitors`` seam with a fake engine
client (no engine required), asserting the txn add_node/commit + edge calls and the
Uptime Kuma monitor -> :UptimeMonitor / heartbeat -> :HeartbeatStat mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from uptime_kuma_agent.kg_ingest import (
    ingest_documents,
    ingest_entities,
    ingest_monitors,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "UptimeMonitor", "name": "web"},
            {"id": "b", "type": "HeartbeatStat"},
        ],
        [{"source": "b", "target": "a", "type": "heartbeatOf"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "uptime-kuma-agent"
    assert c.txn.nodes["a"]["domain"] == "uptimekuma"
    assert c.edges.edges == [("b", "a", {"type": "heartbeatOf"})]


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
    assert mon["type"] == "UptimeMonitor"
    assert mon["monitorType"] == "http"
    assert mon["monitorUrl"] == "https://api.example/health"
    assert mon["checkInterval"] == 60
    assert mon["monitorActive"] is True
    assert mon["uptimeKumaId"] == "3"
    # heartbeat nodes are typed + linked
    hb_ids = [k for k in c.txn.nodes if k.startswith("uptimekuma:heartbeat:3:")]
    assert len(hb_ids) == 2
    up = c.txn.nodes["uptimekuma:heartbeat:3:2026-07-04T10-00-00"]
    assert up["type"] == "HeartbeatStat"
    assert up["heartbeatStatus"] == 1
    assert up["ping"] == 12.5
    assert all(
        rel[1] == "uptimekuma:monitor:3" and rel[2] == {"type": "heartbeatOf"}
        for rel in c.edges.edges
    )


def test_ingest_monitors_without_heartbeats():
    c = _FakeClient()
    res = ingest_monitors(
        [{"id": 1, "name": "web", "type": "http"}], client=c, graph="__commons__"
    )
    assert res == {"nodes": 1, "edges": 0}
    assert c.txn.nodes["uptimekuma:monitor:1"]["type"] == "UptimeMonitor"


def test_ingest_documents_writes_document_nodes():
    c = _FakeClient()
    res = ingest_documents(
        [{"id": "uptimekuma:doc:1", "text": "monitor api is degraded", "title": "api"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    node = c.txn.nodes["uptimekuma:doc:1"]
    assert node["type"] == "Document"
    assert node["text"] == "monitor api is degraded"


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "UptimeMonitor"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_monitors([], client=_FakeClient()) is None
