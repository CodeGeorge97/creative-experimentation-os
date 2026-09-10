"""Tests for the approved Stage 17E command envelope representation."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError, fields
from typing import get_args

from creative_os.schemas.canonical import CanonicalRecordRef, CanonicalUpstreamBinding
from creative_os.schemas.commands import (
    CommandName,
    RunLifecycle,
    RuntimeCommandRequest,
    RuntimeCommandResult,
)
from creative_os.schemas.validation import (
    StructuralErrorCode,
    StructuralValidationIssue,
    StructuralValidationResult,
)


class CommandSchemaTests(unittest.TestCase):
    def request_fields(self):
        return dict(
            command_name="build_product_truth",
            run_id="RUN-20260904T1132Z-a91c4e",
            input_bindings=(),
            config_snapshot_refs={},
            knowledge_refs={},
            inputs={},
        )

    def result_fields(self):
        return dict(
            command_name="build_product_truth",
            run_id="RUN-20260904T1132Z-a91c4e",
            lifecycle_state="COMPLETED",
            canonical_outputs=(),
            runtime_outputs={},
            result_metadata={},
        )

    def test_exact_command_names_and_construction(self):
        names = (
            "build_product_truth", "research_chile_market",
            "build_strategy_hypotheses", "build_concepts",
            "select_experiment_plan", "build_creatives",
            "review_creatives", "prepare_production",
        )
        self.assertEqual(get_args(CommandName), names)
        for name in names:
            with self.subTest(command=name):
                request = self.request_fields()
                result = self.result_fields()
                request["command_name"] = result["command_name"] = name
                self.assertEqual(RuntimeCommandRequest(**request).command_name, name)
                self.assertEqual(RuntimeCommandResult(**result).command_name, name)

    def test_exact_lifecycle_values_and_construction(self):
        states = (
            "READY", "RUNNING", "WAITING_HUMAN", "RETRY_PENDING",
            "BLOCKED", "FAILED", "COMPLETED",
        )
        self.assertEqual(get_args(RunLifecycle), states)
        for state in states:
            with self.subTest(state=state):
                supplied = self.result_fields()
                supplied["lifecycle_state"] = state
                self.assertEqual(RuntimeCommandResult(**supplied).lifecycle_state, state)

    def test_only_approved_fields_and_required_arguments(self):
        for schema, supplied, optional in (
            (RuntimeCommandRequest, self.request_fields(), ()),
            (RuntimeCommandResult, self.result_fields(), ("structural_validation",)),
        ):
            self.assertEqual(tuple(f.name for f in fields(schema)), tuple(supplied) + optional)
            for name in supplied:
                with self.subTest(schema=schema.__name__, missing=name):
                    incomplete = supplied.copy()
                    del incomplete[name]
                    with self.assertRaises(TypeError):
                        schema(**incomplete)
            with self.assertRaises(TypeError):
                schema(**supplied, unexpected=True)

    def test_exact_bindings_snapshots_and_payloads_are_preserved(self):
        reference = CanonicalRecordRef("record-upstream", "v2", "sha256:" + "a" * 64)
        binding = CanonicalUpstreamBinding("product_truth", reference)
        supplied = self.request_fields()
        supplied.update(
            input_bindings=(binding,),
            config_snapshot_refs={"evidence_policy": "sha256:" + "b" * 64},
            knowledge_refs={"KNW-schwartz-persuasion": "sha256:" + "c" * 64},
            inputs={"supplied": ("opaque",)},
        )
        request = RuntimeCommandRequest(**supplied)
        for name, value in supplied.items():
            self.assertEqual(getattr(request, name), value)
        self.assertIs(request.input_bindings[0], binding)
        self.assertIs(request.input_bindings[0].reference, reference)
        result_data = self.result_fields()
        result_data.update(
            canonical_outputs=(reference,),
            runtime_outputs={"supplied": ("opaque",)},
            result_metadata={"supplied": "diagnostic"},
        )
        result = RuntimeCommandResult(**result_data)
        for name, value in result_data.items():
            self.assertEqual(getattr(result, name), value)
        self.assertIs(result.canonical_outputs[0], reference)

    def test_default_validation_results_are_fresh_and_empty(self):
        first = RuntimeCommandResult(**self.result_fields())
        second = RuntimeCommandResult(**self.result_fields())
        self.assertIsNot(first.structural_validation, second.structural_validation)
        self.assertEqual(first.structural_validation.issues, ())
        self.assertTrue(first.structural_validation.is_valid)

    def test_structural_issues_do_not_rewrite_reported_lifecycle(self):
        validation = StructuralValidationResult((StructuralValidationIssue(
            code=StructuralErrorCode.MISSING_REQUIRED_FIELD,
            path=("inputs",),
            message="Required field missing",
        ),))
        result = RuntimeCommandResult(
            **self.result_fields(), structural_validation=validation
        )
        self.assertIs(result.structural_validation, validation)
        self.assertFalse(result.structural_validation.is_valid)
        self.assertEqual(result.lifecycle_state, "COMPLETED")

    def test_envelope_fields_are_frozen_and_slotted(self):
        for envelope in (
            RuntimeCommandRequest(**self.request_fields()),
            RuntimeCommandResult(**self.result_fields()),
        ):
            self.assertFalse(hasattr(envelope, "__dict__"))
            for definition in fields(envelope):
                with self.subTest(schema=type(envelope).__name__, field=definition.name):
                    with self.assertRaises(FrozenInstanceError):
                        setattr(envelope, definition.name, None)


if __name__ == "__main__":
    unittest.main()
