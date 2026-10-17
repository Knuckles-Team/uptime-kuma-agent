"""Uptime Kuma ontology contribution (CONCEPT:AU-KG.ontology.federation-provider-leg).

Data-only subpackage: it carries ``uptimekuma.ttl`` (the ``owl:Ontology``
``http://knuckles.team/kg/uptimekuma`` module) which the Graph OS hub federates in via
the ``agent_connector_sdk.ontology_providers`` entry-point. It holds no business logic
and no heavy imports so the hub can resolve it cheaply.
"""
