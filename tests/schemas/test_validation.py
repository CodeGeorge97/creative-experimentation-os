"""Tests for structural validation primitives."""

from __future__ import annotations

import unittest

from creative_os.schemas.validation import (
    StructuralErrorCode,
    StructuralValidationIssue,
    StructuralValidationResult,
)


class StructuralValidationTests(unittest.TestCase):
    def test_empty_result_is_valid(self) -> None:
        result = StructuralValidationResult()
        self.assertTrue(result.is_valid)

    def test_issue_makes_result_invalid(self) -> None:
        issue = StructuralValidationIssue(
            code=StructuralErrorCode.MISSING_REQUIRED_FIELD,
            path=("creative", "claim_text"),
            message="claim_text is required",
        )
        result = StructuralValidationResult((issue,))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.issues[0].path, ("creative", "claim_text"))

    def test_error_codes_are_provider_neutral_strings(self) -> None:
        self.assertEqual(
            StructuralErrorCode.INVALID_ENUM_VALUE.value,
            "invalid_enum_value",
        )


if __name__ == "__main__":
    unittest.main()
