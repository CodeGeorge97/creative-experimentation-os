"""Canonical immutable record representation primitives."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CanonicalRecordRef:
    """Exact immutable reference to one canonical record version."""

    record_id: str
    version: str
    content_hash: str


@dataclass(frozen=True, slots=True)
class CanonicalUpstreamBinding:
    """Named exact upstream canonical dependency."""

    role: str
    reference: CanonicalRecordRef


@dataclass(frozen=True, slots=True)
class CanonicalRecordEnvelope:
    """Provider-neutral structural envelope for canonical records."""

    record_id: str
    record_type: str
    version: str
    content_hash: str
    state: str | None = None
    upstream_bindings: tuple[CanonicalUpstreamBinding, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    metadata: tuple[tuple[str, str], ...] = ()

    @property
    def reference(self) -> CanonicalRecordRef:
        """Return the exact identity/version/hash reference."""
        return CanonicalRecordRef(
            record_id=self.record_id,
            version=self.version,
            content_hash=self.content_hash,
        )
