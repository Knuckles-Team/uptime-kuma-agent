"""Native epistemic-graph ingestion for Uptime Kuma records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. The package natively pushes its
availability-monitoring data into the ONE epistemic-graph knowledge graph as **typed
OWL nodes** (``:UptimeMonitor``, ``:HeartbeatStat``) + links, matching the classes
federated by ``uptime_kuma_agent.ontology`` (``uptimekuma.ttl``).

Everything is delegated to the shared fleet primitive
``agent_utilities.knowledge_graph.memory.native_ingest`` when it is importable; that
primitive is the ONE implementation of the engine txn write path. The import is GUARDED
— when the primitive (or the whole KG stack / a reachable engine) is absent, a
self-contained txn fallback over the lightweight ``GraphComputeEngine()._client`` is
used, and if that too is unavailable every entry point **no-ops** (returns ``None``),
so the connector runs with zero KG infrastructure and never raises.

Node ids follow ``uptimekuma:<class>:<externalId>``. Timeseries heartbeat samples are
modelled as ``:HeartbeatStat`` nodes linked to their monitor via ``:heartbeatOf``.
"""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger("uptime_kuma_agent.kg")

_SOURCE = "uptime-kuma-agent"
_DOMAIN = "uptimekuma"
_DEFAULT_GRAPH = "__commons__"


# --------------------------------------------------------------------------- #
# write path — delegate to the shared primitive, else self-contained fallback #
# --------------------------------------------------------------------------- #
def _native() -> Any | None:
    """Return the shared ``native_ingest`` module, or ``None`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.memory import native_ingest
    except Exception as e:  # noqa: BLE001 — primitive/KG stack absent
        logger.debug("native_ingest primitive unavailable: %s", e)
        return None
    return native_ingest


def _fallback_client() -> tuple[Any | None, str]:
    """Resolve ``(engine_client, graph)`` directly — the self-contained txn path."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or _DEFAULT_GRAPH)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _fallback_write(
    nodes: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    client: Any | None,
    graph: str | None,
) -> dict[str, int] | None:
    """Self-contained txn write (mirrors the shared primitive's ``_write_nodes``)."""
    nodes = [n for n in (nodes or []) if n.get("id")]
    if not nodes:
        return None
    if client is None:
        client, graph = _fallback_client()
    if client is None:
        return None
    graph = graph or _DEFAULT_GRAPH
    try:
        txn = client.txn.begin(graph=graph)
        for node in nodes:
            props = {k: v for k, v in node.items() if k != "id" and v is not None}
            props.setdefault("source", _SOURCE)
            props.setdefault("domain", _DOMAIN)
            client.txn.add_node(txn, node["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)
    logger.info("KG ingest: wrote %d nodes, %d edges", len(nodes), edges)
    return {"nodes": len(nodes), "edges": edges}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (never raises). ``client``/``graph``
    may be injected (tests); otherwise resolved on demand.
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    native = _native()
    if native is not None and client is None:
        return native.ingest_entities(
            entities, relationships, source=source, domain=domain
        )
    return _fallback_write(entities, relationships, client=client, graph=graph)


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder).

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Returns ``{"nodes":n, "edges":0}`` or ``None``.
    """
    native = _native()
    if native is not None and client is None:
        return native.ingest_documents(documents, source=source, domain=domain)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    nodes: list[dict[str, Any]] = []
    for doc in documents or []:
        did = doc.get("id")
        text = doc.get("text") or doc.get("content")
        if not did or not text:
            continue
        node = {k: v for k, v in doc.items() if k not in ("content",) and v is not None}
        node["id"] = did
        node["type"] = "Document"
        node["text"] = text
        node.setdefault("created_at", now)
        nodes.append(node)
    return _fallback_write(nodes, None, client=client, graph=graph)


# --------------------------------------------------------------------------- #
# domain mappers — Uptime Kuma records -> typed nodes                          #
# --------------------------------------------------------------------------- #
def _monitor_entity(mon: dict[str, Any]) -> dict[str, Any] | None:
    mid = mon.get("id")
    if mid is None:
        return None
    active = mon.get("active")
    return {
        "id": f"uptimekuma:monitor:{mid}",
        "type": "UptimeMonitor",
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
                "type": "HeartbeatStat",
                "heartbeatStatus": beat.get("status"),
                "ping": float(ping) if ping is not None else None,
                "heartbeatTime": beat.get("time"),
                "heartbeatMsg": beat.get("msg"),
                "uptimeKumaId": str(monitor_id),
            }
        )
        relationships.append({"source": hid, "target": mon_node, "type": "heartbeatOf"})
    return entities, relationships


def ingest_monitors(
    monitors: list[dict[str, Any]],
    heartbeats: dict[Any, list[dict[str, Any]]] | None = None,
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
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
