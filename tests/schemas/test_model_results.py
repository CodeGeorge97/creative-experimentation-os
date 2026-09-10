"""Tests for provider-neutral model-result schemas."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError

from creative_os.schemas.model_results import (
    ModelTransportMetadata,
    ModelUncertainty,
    ProviderNeutralModelResult,
)
from creative_os.schemas.validation import (
    StructuralErrorCode,
    StructuralValidationIssue,
    StructuralValidationResult,
)


class ModelResultSchemaTests(unittest.TestCase):
    def test_empty_structural_validation_is_valid(self) -> None:
        result = ProviderNeutralModelResult(
            invocation_id="inv-001",
            output_type="creative_result",
            payload={"headline": "Example"},
        )
        self.assertTrue(result.is_structurally_valid)

    def test_structural_issue_does_not_pass(self) -> None:
        issue = StructuralValidationIssue(
            code=StructuralErrorCode.MISSING_REQUIRED_FIELD,
            path=("headline",),
            message="headline is required",
        )
        result = ProviderNeutralModelResult(
            invocation_id="inv-002",
            output_type="creative_result",
            payload={},
            structural_validation=StructuralValidationResult((issue,)),
        )
        self.assertFalse(result.is_structurally_valid)

    def test_traceability_metadata_is_preserved(self) -> None:
        uncertainty = ModelUncertainty(
            code="missing_context",
            message="Additional context required",
            requires_resolution=True,
        )
        result = ProviderNeutralModelResult(
            invocation_id="inv-003",
            output_type="strategy_result",
            payload={"status": "partial"},
            uncertainties=(uncertainty,),
            upstream_binding_refs=("product-truth:v3:abc123",),
            transport=ModelTransportMetadata(
                provider="example-provider",
                model="example-model",
                request_id="req-123",
            ),
        )
        self.assertEqual(result.transport.provider, "example-provider")
        self.assertTrue(result.uncertainties[0].requires_resolution)
        self.assertEqual(
            result.upstream_binding_refs,
            ("product-truth:v3:abc123",),
        )

    def test_result_is_frozen(self) -> None:
        result = ProviderNeutralModelResult(
            invocation_id="inv-004",
            output_type="test",
            payload={},
        )
        with self.assertRaises(FrozenInstanceError):
            result.output_type = "changed"


if __name__ == "__main__":
    unittest.main()
