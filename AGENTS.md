# Creative Experimentation OS — Agent Instructions

## Source of truth
- `phase-5-design-freeze-v2` is the authoritative implementation baseline.
- Frozen architecture lives in:
  - `docs/PHASE_1_SYSTEM_DESIGN.md`
  - `docs/PHASE_2_DATA_ARCHITECTURE.md`
  - `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md`
  - `docs/PHASE_4_SKILLS_DESIGN.md`
  - `docs/PHASE_5_RUNTIME_DESIGN.md`
- Read the relevant frozen contract before implementing a stage.

## Frozen boundaries
- Never redesign frozen Phase 1–5 contracts.
- Never modify frozen Phase 1–4 documents or `.claude/skills/` unless explicitly instructed by the human operator.
- Do not invent IDs, event types, enums, policy values, schema fields, state transitions, config registries, knowledge routes, or capability rules.
- If a frozen contract is ambiguous, stop and report the ambiguity instead of guessing.

## Architecture rules
- Skills contain reasoning/procedure only.
- Orchestration owns sequencing, retries, gates, IDs, retrieval, persistence, and tool invocation.
- Config owns policy, thresholds, taxonomies, enums, and capability settings.
- Knowledge is retrieved; do not embed runtime knowledge bodies in source code.
- Provider SDK imports are allowed only inside adapters.
- Business and policy constants belong in config, not hidden source constants.
- SQLite projections are rebuildable and non-authoritative.
- Canonical records are immutable and versioned.
- Domain events are append-only.
- HARD_BLOCK decisions are deterministic only.

## Implementation workflow
- Work one implementation stage at a time.
- Do not continue into the next stage without validation.
- Add or update tests for every new implementation unit.
- Use Python 3.12 on Windows with `py -3.12`.
- Run the relevant tests before every checkpoint.
- Run `git diff --check` before every checkpoint.
- Do not commit if tests or audits fail.
- Do not use `git clean`.
- Do not delete unexpected files.
- Do not modify PDFs.

## Git safety
- Active implementation branch: `phase-5-runtime-implementation`.
- Preserve `phase-5-design-freeze` as historical.
- Correct frozen design baseline: `phase-5-design-freeze-v2`.
- Never rewrite or move frozen tags.
- Never force-push unless explicitly instructed by the human operator.

## Agent behavior
- Prefer minimal, contract-driven changes.
- Do not refactor unrelated code.
- Do not broaden scope beyond the requested stage.
- Report files changed, tests run, failures found, and final git status.
- Stop on contract ambiguity, destructive risk, or frozen-boundary conflict.
