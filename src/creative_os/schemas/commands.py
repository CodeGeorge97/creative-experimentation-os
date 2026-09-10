"""Provider-neutral runtime command envelopes (Phase 5 sections 15 and 18.7).

Literal annotations describe allowed values; construction does not validate
runtime values or domain prerequisites. Frozen envelopes are shallowly immutable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Mapping

from creative_os.schemas.canonical import CanonicalRecordRef, CanonicalUpstreamBinding
from creative_os.schemas.validation import StructuralValidationResult


CommandName = Literal[
    "build_product_truth",
    "research_chile_market",
    "build_strategy_hypotheses",
    "build_concepts",
    "select_experiment_plan",
    "build_creatives",
    "review_creatives",
    "prepare_production",
]

RunLifecycle = Literal[
    "READY",
    "RUNNING",
    "WAITING_HUMAN",
    "RETRY_PENDING",
    "BLOCKED",
    "FAILED",
    "COMPLETED",
]


@dataclass(frozen=True, slots=True)
class RuntimeCommandRequest:
    """Supplied command scope; references do not establish domain eligibility."""

    command_name: CommandName
    run_id: str
    input_bindings: tuple[CanonicalUpstreamBinding, ...]
    config_snapshot_refs: Mapping[str, str]
    knowledge_refs: Mapping[str, str]
    inputs: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class RuntimeCommandResult:
    """Reported runtime outcome; lifecycle state is supplied by orchestration."""

    command_name: CommandName
    run_id: str
    lifecycle_state: RunLifecycle
    canonical_outputs: tuple[CanonicalRecordRef, ...]
    runtime_outputs: Mapping[str, object]
    result_metadata: Mapping[str, object]
    structural_validation: StructuralValidationResult = field(
        default_factory=StructuralValidationResult
    )
