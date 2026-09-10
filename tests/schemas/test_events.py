"""Tests for canonical domain-event schema primitives."""

from __future__ import annotations

import unittest
from dataclasses import FrozenInstanceError

from creative_os.schemas.events import (
    DomainEventActor,
    DomainEventActorKind,
    DomainEventAddress,
    DomainEventEnvelope,
    DomainEventLog,
    DomainEventType,
)


class DomainEventSchemaTests(unittest.TestCase):
    def test_exactly_sixteen_frozen_event_types_exist(self) -> None:
        self.assertEqual(len(DomainEventType), 16)

    def test_event_inventory_matches_phase_2(self) -> None:
        expected = {
            "SOURCE_ACCESSED",
            "CLAIM_STATUS_ASSERTED",
            "CLAIM_DISPUTED",
            "CLAIM_SUPERSEDED",
            "CLAIM_REJECTED",
            "ASSET_RIGHTS_ATTESTED",
            "ASSET_STATE_CHANGED",
            "CREATIVE_STATE_CHANGED",
            "PACKAGE_STATE_CHANGED",
            "EXPERIMENT_INVALIDATED",
            "RUN_STATUS_CHANGED",
            "RUN_STEP_COMPLETED",
            "RUN_DECISION",
            "RUN_REJECTION",
            "RUN_ERROR",
            "RUN_RETRY",
        }
        self.assertEqual({item.value for item in DomainEventType}, expected)

    def test_exactly_four_canonical_logs_exist(self) -> None:
        self.assertEqual(
            {item.value for item in DomainEventLog},
            {"evidence", "asset", "campaign", "run"},
        )

    def test_envelope_preserves_canonical_fields(self) -> None:
        actor = DomainEventActor(
            kind=DomainEventActorKind.RUNTIME,
            id="svc-orchestrator",
        )
        event = DomainEventEnvelope(
            event_seq=417,
            event_type=DomainEventType.CLAIM_STATUS_ASSERTED,
            subject_ref="CLM-magnesio-500-0007",
            occurred_at="2026-09-04T13:41:08Z",
            actor=actor,
            run_id="RUN-20260904T1132Z-a91c4e",
            step_id="E3#004",
            payload={"status": "SUPPORTED"},
        )
        self.assertEqual(event.event_seq, 417)
        self.assertEqual(event.actor.kind, DomainEventActorKind.RUNTIME)
        self.assertEqual(event.step_id, "E3#004")

    def test_event_address_and_envelope_are_frozen(self) -> None:
        address = DomainEventAddress(DomainEventLog.EVIDENCE, 417)
        with self.assertRaises(FrozenInstanceError):
            address.event_seq = 418


if __name__ == "__main__":
    unittest.main()
