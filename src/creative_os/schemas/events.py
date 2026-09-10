"""Canonical append-only domain-event schema primitives."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class DomainEventLog(StrEnum):
    """The four canonical append-only event logs."""

    EVIDENCE = "evidence"
    ASSET = "asset"
    CAMPAIGN = "campaign"
    RUN = "run"


class DomainEventType(StrEnum):
    """The sixteen frozen Phase 2 domain-event discriminators."""

    SOURCE_ACCESSED = "SOURCE_ACCESSED"
    CLAIM_STATUS_ASSERTED = "CLAIM_STATUS_ASSERTED"
    CLAIM_DISPUTED = "CLAIM_DISPUTED"
    CLAIM_SUPERSEDED = "CLAIM_SUPERSEDED"
    CLAIM_REJECTED = "CLAIM_REJECTED"
    ASSET_RIGHTS_ATTESTED = "ASSET_RIGHTS_ATTESTED"
    ASSET_STATE_CHANGED = "ASSET_STATE_CHANGED"
    CREATIVE_STATE_CHANGED = "CREATIVE_STATE_CHANGED"
    PACKAGE_STATE_CHANGED = "PACKAGE_STATE_CHANGED"
    EXPERIMENT_INVALIDATED = "EXPERIMENT_INVALIDATED"
    RUN_STATUS_CHANGED = "RUN_STATUS_CHANGED"
    RUN_STEP_COMPLETED = "RUN_STEP_COMPLETED"
    RUN_DECISION = "RUN_DECISION"
    RUN_REJECTION = "RUN_REJECTION"
    RUN_ERROR = "RUN_ERROR"
    RUN_RETRY = "RUN_RETRY"


class DomainEventActorKind(StrEnum):
    """Actor kinds permitted by the canonical event envelope."""

    RUNTIME = "RUNTIME"
    OPERATOR = "OPERATOR"


@dataclass(frozen=True, slots=True)
class DomainEventActor:
    """Actor recorded on a canonical domain event."""

    kind: DomainEventActorKind
    id: str


@dataclass(frozen=True, slots=True)
class DomainEventAddress:
    """Canonical event address: log plus append-assigned sequence."""

    log: DomainEventLog
    event_seq: int


@dataclass(frozen=True, slots=True)
class DomainEventEnvelope:
    """Canonical append-only domain-event envelope."""

    event_seq: int
    event_type: DomainEventType
    subject_ref: str
    occurred_at: str
    actor: DomainEventActor
    run_id: str
    payload: Mapping[str, object]
    step_id: str | None = None
