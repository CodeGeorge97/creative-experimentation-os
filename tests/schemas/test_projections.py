"""Focused tests for the approved Stage 17F projection representation."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError, fields
from types import MappingProxyType
from typing import Mapping, get_type_hints

from creative_os.schemas.canonical import CanonicalRecordRef, CanonicalUpstreamBinding
from creative_os.schemas.projections import (
    InputProjection,
    ProjectionConfigRef,
    ProjectionKnowledgeRef,
)


class ProjectionSchemaTests(unittest.TestCase):
    def config_fields(self):
        return dict(ref="config/evidence_policy@v4", content_hash="sha256:" + "a" * 64)

    def knowledge_fields(self):
        return dict(
            knowledge_id="KNW-schwartz-persuasion",
            source_ref="fixture-source@v2",
            tier="supplied-tier",
            retrieval_policy="supplied-policy",
            fragment_locator="supplied-fragment",
            fragment_content_hash="sha256:" + "b" * 64,
            provenance=MappingProxyType({"supplied": ("source", "position")}),
        )

    def projection_fields(self):
        reference = CanonicalRecordRef(
            "PRD-acme-magnesio-500/product_truth", "v2", "sha256:" + "c" * 64
        )
        return dict(
            payload=MappingProxyType({"supplied": ("selected",)}),
            source_bindings=(CanonicalUpstreamBinding("product_truth", reference),),
            provenance_refs=("PRD-acme-magnesio-500/product_truth@v2#facts",),
            config_refs=(ProjectionConfigRef(**self.config_fields()),),
            knowledge_refs=(ProjectionKnowledgeRef(**self.knowledge_fields()),),
        )

    def cases(self):
        return (
            (InputProjection, self.projection_fields()),
            (ProjectionConfigRef, self.config_fields()),
            (ProjectionKnowledgeRef, self.knowledge_fields()),
        )

    def test_construction_preserves_exact_supplied_values(self):
        for schema, supplied in self.cases():
            instance = schema(**supplied)
            for name, value in supplied.items():
                with self.subTest(schema=schema.__name__, field=name):
                    self.assertEqual(getattr(instance, name), value)
                    self.assertIs(getattr(instance, name), value)

    def test_exact_approved_fields_and_types(self):
        expected = {
            InputProjection: dict(
                payload=Mapping[str, object],
                source_bindings=tuple[CanonicalUpstreamBinding, ...],
                provenance_refs=tuple[str, ...],
                config_refs=tuple[ProjectionConfigRef, ...],
                knowledge_refs=tuple[ProjectionKnowledgeRef, ...],
            ),
            ProjectionConfigRef: dict(ref=str, content_hash=str),
            ProjectionKnowledgeRef: dict(
                knowledge_id=str, source_ref=str, tier=str, retrieval_policy=str,
                fragment_locator=str | None, fragment_content_hash=str | None,
                provenance=Mapping[str, object],
            ),
        }
        for schema, annotations in expected.items():
            with self.subTest(schema=schema.__name__):
                self.assertEqual(tuple(f.name for f in fields(schema)), tuple(annotations))
                self.assertEqual(get_type_hints(schema), annotations)

    def test_every_field_is_required_and_extra_fields_are_rejected(self):
        for schema, supplied in self.cases():
            for name in supplied:
                with self.subTest(schema=schema.__name__, missing=name):
                    incomplete = supplied.copy()
                    del incomplete[name]
                    with self.assertRaises(TypeError):
                        schema(**incomplete)
            with self.assertRaises(TypeError):
                schema(**supplied, unexpected=True)

    def test_fragment_fields_allow_explicit_none_independently(self):
        for locator in (None, "supplied-fragment"):
            for content_hash in (None, "sha256:" + "b" * 64):
                with self.subTest(locator=locator, content_hash=content_hash):
                    supplied = self.knowledge_fields()
                    supplied.update(
                        fragment_locator=locator, fragment_content_hash=content_hash
                    )
                    reference = ProjectionKnowledgeRef(**supplied)
                    self.assertEqual(reference.fragment_locator, locator)
                    self.assertEqual(reference.fragment_content_hash, content_hash)

    def test_multiple_exact_bindings_and_provenance_remain_distinct(self):
        supplied = self.projection_fields()
        first = supplied["source_bindings"][0]
        second_ref = CanonicalRecordRef(
            first.reference.record_id, "v3", "sha256:" + "d" * 64
        )
        second = CanonicalUpstreamBinding("supplied-comparison", second_ref)
        supplied["source_bindings"] = (first, second)
        supplied["provenance_refs"] += (
            "PRD-acme-magnesio-500/product_truth@v3#facts",
        )
        projection = InputProjection(**supplied)
        self.assertIs(projection.source_bindings[0], first)
        self.assertIs(projection.source_bindings[0].reference, first.reference)
        self.assertIs(projection.source_bindings[1], second)
        self.assertIs(projection.source_bindings[1].reference, second_ref)
        self.assertEqual(projection.provenance_refs, supplied["provenance_refs"])
        self.assertNotEqual(first.reference, second_ref)

    def test_explicit_empty_collections_are_preserved(self):
        projection = InputProjection({}, (), (), (), ())
        self.assertEqual(projection.payload, {})
        for name in ("source_bindings", "provenance_refs", "config_refs", "knowledge_refs"):
            self.assertEqual(getattr(projection, name), ())

    def test_all_fields_are_frozen_and_instances_are_slotted(self):
        for schema, supplied in self.cases():
            instance = schema(**supplied)
            self.assertFalse(hasattr(instance, "__dict__"))
            for definition in fields(instance):
                with self.subTest(schema=schema.__name__, field=definition.name):
                    with self.assertRaises(FrozenInstanceError):
                        setattr(instance, definition.name, None)
                    with self.assertRaises(FrozenInstanceError):
                        delattr(instance, definition.name)

    def test_mapping_immutability_is_shallow_without_copying(self):
        payload = {"supplied": ["original"]}
        projection = InputProjection(payload, (), (), (), ())
        provenance = {"supplied": ["original"]}
        supplied = self.knowledge_fields()
        supplied["provenance"] = provenance
        reference = ProjectionKnowledgeRef(**supplied)
        payload["supplied"].append("caller-change")
        provenance["supplied"].append("caller-change")
        self.assertIs(projection.payload, payload)
        self.assertIs(reference.provenance, provenance)
        self.assertEqual(projection.payload["supplied"], ["original", "caller-change"])
        self.assertEqual(reference.provenance["supplied"], ["original", "caller-change"])


if __name__ == "__main__":
    unittest.main()
