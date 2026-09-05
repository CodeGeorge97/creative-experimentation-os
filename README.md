# Creative Experimentation OS — Chile

A repository-first system for evidence-grounded creative experimentation for Meta Ads in the Chilean market.

The system is designed around the chain:

SOURCE → OBSERVATION → INSIGHT → HYPOTHESIS → CONCEPT → EXPERIMENT → CREATIVE → PRODUCTION → PERFORMANCE → LEARNING

## Current phase

- Phase 1 — System Design: frozen.
- Phase 2 — Data Architecture: frozen.
- Phase 3A — Repository Migration Design: frozen.
- Phase 3B — Physical repository migration: current.
- Phase 3C — Knowledge provenance: required before Phase 4.
- Phase 4 — Claude Skills: not started.
- Phase 5+ — Runtime, models, orchestration and production integrations: not started.

No production runtime or Skills exist yet.

## Repository structure

### `docs/`
Architecture, phase documents and migration history.

### `config/`
Canonical authored configuration.

There are exactly nine top-level YAML registries:

1. `evidence_policy.yaml`
2. `deny_list.yaml`
3. `narrative_library.yaml`
4. `format_profiles.yaml`
5. `category_profiles.yaml`
6. `creative_taxonomy.yaml`
7. `experiment_variables.yaml`
8. `diversity_targets.yaml`
9. `tool_capability.yaml`

During Phase 3B these registries are intentionally fail-closed with:

`status: PLACEHOLDER_NOT_AUTHORISED`

A run must not start while a required registry remains unauthorised.

`config/styles/` is reserved for authored Style Profile registry entities and is not a tenth run-level registry.

### `knowledge/`
Structured knowledge that may later be retrieved into reasoning and generation.

`knowledge/_quarantine/` contains restricted material. Phase 3C will author the required provenance records. Until then, knowledge without valid provenance is not retrievable.

### `sources/`
Raw immutable upstream source documents. Sources are never edited in place.

### `store/`
Canonical system of record.

Canonical manifest inputs are JSON entity/artefact records and JSONL event logs. Runtime data written here is authoritative and git-tracked.

Entity-scope directories are created only when real records exist; empty trees are not scaffolded in advance.

### `reviews/`
Git-tracked, deterministic human-readable renders derived from canonical artefacts.

Reviews are not canonical and are outside the source manifest.

### `media/`
Binary media payloads and repository-origin files awaiting registration.

During Phase 3B, the 15 existing reference samples under `media/_unregistered/` remain git-tracked. They are not registered assets yet.

A future Media Cutover will be a separate explicitly-approved operation after a durable payload strategy exists.

### `incoming/`
Operator drop zone for files awaiting ingestion.

Files entering here are treated as user-supplied input. Contents are transient and non-canonical.

### `var/`
Derived, rebuildable, cached, temporary and exported runtime material.

Deleting `var/` must cost only time, never canonical truth.

## Reserved future boundaries

The following names are intentionally not scaffolded yet:

- `.claude/skills/` — Phase 4
- `src/` — Phase 5
- `tests/` — Phase 5

The phase that first writes real content into one of these boundaries creates it.

## Design principles

- Canonical truth lives in tracked structured records, not filenames.
- Canonical paths are derived from identifiers.
- Immutable versions are never overwritten.
- SQLite is an index only and is always rebuildable.
- Skills provide procedure and knowledge; tools provide capability.
- Media payloads are distinct from canonical Asset Registry records.
- Ignored or derived files must never become the only copy of canonical truth.
- Evidence, provenance and policy fail closed when required information is missing.

## Documentation

Start with:

- `docs/PHASE_1_SYSTEM_DESIGN.md`
- `docs/PHASE_2_DATA_ARCHITECTURE.md`
- `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md`
- `docs/MIGRATIONS.md`

`PRE_FLIGHT_AUDIT.md` is an immutable historical snapshot at the repository root and must not be moved or edited.
