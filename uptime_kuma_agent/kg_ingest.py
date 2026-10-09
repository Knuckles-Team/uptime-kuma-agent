"""Native epistemic-graph ingestion for Uptime Kuma records.

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Connector-specific mappers emit
canonical node_type nodes and relationship edges. The ``agent_connector_sdk.ingest``
knowledge-ingest facade owns the transaction and raises ``IngestError`` when the
engine cannot commit.
"""

from __future__ import annotations

from typing import Any

from agent_connector_sdk.ingest import (
    ChangeSet,
    Document,
    Entity,
    IngestBinding,
    IngestError,
    KnowledgeIngest,
    Relationship,
    current_ingest,
)

_BINDING = IngestBinding(connector="uptime-kuma-agent", stream="uptimekuma")


def _to_entity(record: dict[str, Any]) -> Entity:
    return Entity(
        id=record.get("id"),
        node_type=record.get("node_type"),
        properties={k: v for k, v in record.items() if k not in ("id", "node_type")},
    )


def _to_relationship(record: dict[str, Any]) -> Relationship:
    props = {
        k: v for k, v in record.items() if k not in ("source", "target", "relationship")
    }
    return Relationship(
        source=record.get("source"),
        target=record.get("target"),
        relationship=record.get("relationship"),
        properties=props or None,
    )


def _to_document(record: dict[str, Any]) -> Document:
    return Document(
        id=record.get("id"),
        text=record.get("text"),
        title=record.get("title"),
        source_uri=record.get("source_uri"),
        properties={
            k: v
            for k, v in record.items()
            if k not in ("id", "text", "title", "source_uri")
        },
    )


async def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write canonical typed nodes and relationships through the SDK's ingest facade."""
    if not entities:
        raise IngestError("ingest_entities needs at least one entity")
    change_set = ChangeSet(
        entities=tuple(_to_entity(e) for e in entities),
        relationships=tuple(_to_relationship(r) for r in relationships or ()),
    )
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


async def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Write searchable documents through the SDK's ingest facade."""
    if not documents:
        raise IngestError("ingest_documents needs at least one document")
    change_set = ChangeSet(documents=tuple(_to_document(d) for d in documents))
    service = ingest or current_ingest()
    receipt = await service.submit(_BINDING, change_set)
    return {"nodes": receipt.affected_count, "edges": receipt.relationship_count}


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
        relationships.append(
            {"source": hid, "target": mon_node, "relationship": "heartbeatOf"}
        )
    return entities, relationships


async def ingest_monitors(
    monitors: list[dict[str, Any]],
    heartbeats: dict[Any, list[dict[str, Any]]] | None = None,
    *,
    ingest: KnowledgeIngest | None = None,
) -> dict[str, int]:
    """Map Uptime Kuma monitor records (+ optional heartbeats) to typed nodes.

    ``monitors``: list of monitor dicts (``client.get_monitors()``) → ``:UptimeMonitor``.
    ``heartbeats``: optional ``{monitor_id: [beat, …]}`` (``client.get_heartbeats()``) →
    ``:HeartbeatStat`` nodes linked to their monitor via ``:heartbeatOf``.
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
    return await ingest_entities(entities, relationships, ingest=ingest)
