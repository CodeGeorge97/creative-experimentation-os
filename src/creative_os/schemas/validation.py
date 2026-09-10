"""Provider-neutral structural validation primitives."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class StructuralErrorCode(StrEnum):
    """Machine-readable structural validation failure classes."""

    MISSING_REQUIRED_FIELD = "missing_required_field"
    INVALID_FIELD_TYPE = "invalid_field_type"
    INVALID_ENUM_VALUE = "invalid_enum_value"
    MALFORMED_REFERENCE = "malformed_reference"
    MALFORMED_VERSION = "malformed_version"
    MALFORMED_HASH = "malformed_hash"
    INVALID_NESTED_PAYLOAD = "invalid_nested_payload"
    UNEXPECTED_FIELD = "unexpected_field"


@dataclass(frozen=True, slots=True)
class StructuralValidationIssue:
    """One normalized structural validation issue."""

    code: StructuralErrorCode
    path: tuple[str | int, ...]
    message: str
    expected: str | None = None
    actual: str | None = None


@dataclass(frozen=True, slots=True)
class StructuralValidationResult:
    """Immutable collection of structural validation issues."""

    issues: tuple[StructuralValidationIssue, ...] = ()

    @property
    def is_valid(self) -> bool:
        return not self.issues
