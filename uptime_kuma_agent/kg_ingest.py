"""Native epistemic-graph ingestion for Uptime Kuma records.

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Connector-specific mappers emit
canonical node_type nodes and relationship edges. The required agent-utilities
native-ingest primitive owns the transaction and raises NativeIngestError when the
authoritative engine cannot commit.
"""

from __future__ import annotations

from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_documents as _native_ingest_documents,
)
from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_entities as _native_ingest_entities,
)

_SOURCE = "uptime-kuma-agent"
_DOMAIN = "uptimekuma"


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write canonical typed nodes and relationships through agent-utilities."""
    return _native_ingest_entities(
        entities,
        relationships,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write searchable documents through the authoritative native-ingest path."""
    return _native_ingest_documents(
        documents,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


def _monitor_entity(mon: dict[str, Any]) -> dict[str, Any] | None:
    mid = mon.get("id")
    if mid is None:
        return None
    active = mon.get("active")
    return {
        "id": f"uptimekuma:monitor:{mid}",
        "node_type": "UptimeMonitor",
        "name": mon.get("name"),
        "monitorType": mon.get("type"),
        "monitorUrl": mon.get("url"),
        "checkInterval": mon.get("interval"),
        "monitorActive": bool(active) if active is not None else None,
        "uptimeKumaId": str(mid),
        "externalToolId": str(mid),
    }


def _heartbeat_entities(
    monitor_id: Any, beats: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    mon_node = f"uptimekuma:monitor:{monitor_id}"
    for idx, beat in enumerate(beats or []):
        if not isinstance(beat, dict):
            continue
        # Prefer a stable sample key: timestamp, else positional index.
        stamp = beat.get("time") or beat.get("timestamp") or str(idx)
        safe = str(stamp).replace(" ", "T").replace(":", "-")
        hid = f"uptimekuma:heartbeat:{monitor_id}:{safe}"
        ping = beat.get("ping")
        entities.append(
            {
                "id": hid,
                "node_type": "HeartbeatStat",
                "heartbeatStatus": beat.get("status"),
                "ping": float(ping) if ping is not None else None,
                "heartbeatTime": beat.get("time"),
                "heartbeatMsg": beat.get("msg"),
                "uptimeKumaId": str(monitor_id),
            }
        )
        relationships.append({"source": hid, "target": mon_node, "relationship": "heartbeatOf"})
    return entities, relationships


def ingest_monitors(
    monitors: list[dict[str, Any]],
    heartbeats: dict[Any, list[dict[str, Any]]] | None = None,
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Map Uptime Kuma monitor records (+ optional heartbeats) to typed nodes.

    ``monitors``: list of monitor dicts (``client.get_monitors()``) → ``:UptimeMonitor``.
    ``heartbeats``: optional ``{monitor_id: [beat, …]}`` (``client.get_heartbeats()``) →
    ``:HeartbeatStat`` nodes linked to their monitor via ``:heartbeatOf``.
    Returns ``{"nodes":n, "edges":m}`` or ``None``.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for mon in monitors or []:
        ent = _monitor_entity(mon)
        if ent is None:
            continue
        entities.append(ent)
    for monitor_id, beats in (heartbeats or {}).items():
        h_ents, h_rels = _heartbeat_entities(monitor_id, beats)
        entities.extend(h_ents)
        relationships.extend(h_rels)
    return ingest_entities(entities, relationships, client=client, graph=graph)
