"""Minimal input projection shapes (Phase 5 sections 18.8 and 18.9).

All fields are supplied explicitly. Construction preserves supplied values;
it does not validate domain eligibility or select projection content.
Frozen dataclasses provide shallow immutability only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from creative_os.schemas.canonical import CanonicalUpstreamBinding


@dataclass(frozen=True, slots=True)
class ProjectionConfigRef:
    """Exact supplied config reference and content hash; no config loading."""

    ref: str
    content_hash: str


@dataclass(frozen=True, slots=True)
class ProjectionKnowledgeRef:
    """Supplied knowledge identity and provenance; no knowledge retrieval."""

    knowledge_id: str
    source_ref: str
    tier: str
    retrieval_policy: str
    fragment_locator: str | None
    fragment_content_hash: str | None
    provenance: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class InputProjection:
    """Selected runtime input with exact bindings, not canonical state."""

    payload: Mapping[str, object]
    source_bindings: tuple[CanonicalUpstreamBinding, ...]
    provenance_refs: tuple[str, ...]
    config_refs: tuple[ProjectionConfigRef, ...]
    knowledge_refs: tuple[ProjectionKnowledgeRef, ...]
