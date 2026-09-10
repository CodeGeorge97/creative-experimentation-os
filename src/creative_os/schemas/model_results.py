"""Provider-neutral structured model-result schemas."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from creative_os.schemas.validation import StructuralValidationResult


@dataclass(frozen=True, slots=True)
class ModelTransportMetadata:
    """Normalized transport metadata retained for runtime traceability."""

    provider: str
    model: str | None = None
    request_id: str | None = None


@dataclass(frozen=True, slots=True)
class ModelUncertainty:
    """Explicit uncertainty or unresolved item reported by model output."""

    code: str
    message: str
    path: tuple[str | int, ...] = ()
    requires_resolution: bool = False


@dataclass(frozen=True, slots=True)
class ProviderNeutralModelResult:
    """Structured model result before deterministic domain acceptance."""

    invocation_id: str
    output_type: str
    payload: Mapping[str, object]
    uncertainties: tuple[ModelUncertainty, ...] = ()
    upstream_binding_refs: tuple[str, ...] = ()
    transport: ModelTransportMetadata | None = None
    structural_validation: StructuralValidationResult = field(
        default_factory=StructuralValidationResult
    )

    @property
    def is_structurally_valid(self) -> bool:
        """Reflect structural validation only, never domain validity."""
        return self.structural_validation.is_valid
