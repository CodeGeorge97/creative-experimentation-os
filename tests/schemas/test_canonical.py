"""Tests for canonical schema primitives."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError

from creative_os.schemas.canonical import (
    CanonicalRecordEnvelope,
    CanonicalRecordRef,
    CanonicalUpstreamBinding,
)


class CanonicalSchemaTests(unittest.TestCase):
    def test_exact_reference_preserves_identity_version_and_hash(self) -> None:
        reference = CanonicalRecordRef(
            record_id="record-001",
            version="v3",
            content_hash="abc123",
        )
        self.assertEqual(reference.record_id, "record-001")
        self.assertEqual(reference.version, "v3")
        self.assertEqual(reference.content_hash, "abc123")

    def test_envelope_reference_matches_record_identity(self) -> None:
        record = CanonicalRecordEnvelope(
            record_id="record-002",
            record_type="example_type",
            version="v4",
            content_hash="def456",
        )
        self.assertEqual(
            record.reference,
            CanonicalRecordRef("record-002", "v4", "def456"),
        )

    def test_upstream_bindings_are_preserved_exactly(self) -> None:
        upstream = CanonicalUpstreamBinding(
            role="product_truth",
            reference=CanonicalRecordRef(
                record_id="record-upstream",
                version="v2",
                content_hash="hash-upstream",
            ),
        )
        record = CanonicalRecordEnvelope(
            record_id="record-downstream",
            record_type="example_type",
            version="v1",
            content_hash="hash-downstream",
            upstream_bindings=(upstream,),
        )
        self.assertEqual(record.upstream_bindings, (upstream,))

    def test_canonical_record_is_frozen(self) -> None:
        record = CanonicalRecordEnvelope(
            record_id="record-003",
            record_type="example_type",
            version="v1",
            content_hash="ghi789",
        )
        with self.assertRaises(FrozenInstanceError):
            record.version = "v2"


if __name__ == "__main__":
    unittest.main()
