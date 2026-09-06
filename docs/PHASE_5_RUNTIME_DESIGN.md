# Phase 5 — Runtime Design

Status: DRAFT
Base freeze: `phase-4-complete`

## 1. Purpose

Phase 5 defines the runtime architecture that executes the frozen Creative Experimentation OS design.

This phase converts previously frozen architecture into explicit runtime contracts before implementation begins.

Phase 5 does not redesign the five Phase 4 Skills.

The runtime preserves these boundaries:

- Skills = reusable procedural reasoning.
- Orchestrator = workflow control.
- Deterministic services = enforceable computation and validation.
- Config = policy, thresholds, taxonomies, enumerations and capability limits.
- Knowledge = retrieved source material.
- Prompts = runtime model-facing instructions.
- Persistence = canonical artefact and event storage.
- SQLite = rebuildable query/index projection.
- Filesystem = media and operational assets.
- Model = reasoning and generation.

## 2. Frozen Inputs

Phase 5 inherits without reinterpretation:

- `docs/PHASE_1_SYSTEM_DESIGN.md`
- `docs/PHASE_2_DATA_ARCHITECTURE.md`
- `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md`
- `docs/PHASE_4_SKILLS_DESIGN.md`
- the five frozen Phase 4 Skills
- the nine Phase 2 config registries
- the canonical artefact, entity, event and ID contracts
- the three human gates
- the Phase 3 knowledge provenance model

If Phase 5 discovers a conflict with a frozen contract, implementation must stop and surface the conflict.

Phase 5 must not silently rewrite prior architecture.

## 3. Runtime Components

### 3.1 Orchestrator

The orchestrator owns workflow execution.

It may:

- sequence stages
- assemble model context
- invoke Skills
- invoke deterministic services
- invoke retrieval
- invoke persistence adapters
- invoke approved external tool adapters
- manage retries
- evaluate stage completion
- enforce human gates
- allocate or request canonical IDs through deterministic runtime mechanisms
- assemble the RUN head
- bind exact artefact versions
- record workflow events

It must not:

- contain domain persuasion reasoning that belongs in a Skill
- embed policy that belongs in config
- embed knowledge content
- replace deterministic validation with model judgement
- directly implement external provider behavior
- silently mutate immutable canonical artefacts

### 3.2 Deterministic Services

Deterministic services own rules that must be mechanically enforceable.

Examples include:

- canonical ID construction and validation
- version and hash binding
- schema validation
- evidence coverage computation
- claim-freedom computation
- deterministic deny-list checks
- deterministic HARD_BLOCK conditions
- diversity calculation and selection
- experiment-lock validation
- package identity derivation
- localization-invariance checks
- deterministic feasibility checks
- manifest validation
- event/state-transition validation

A deterministic service must not make open-ended strategic or creative judgements that belong in a Skill.

### 3.3 Runtime Prompts

Runtime prompts are orchestration resources.

They may:

- frame a specific model call
- select the relevant Skill
- provide runtime context
- provide retrieved knowledge
- provide config-derived constraints
- request a schema-conformant response
- specify the current workflow stage

They must not become an alternative policy store or knowledge store.

Prompt resources will live under the runtime source tree in a later implementation stage.

Phase 5 design does not create them yet.

### 3.4 Schemas and Model-Facing Projections

Schemas define machine-checkable runtime interfaces.

They must distinguish between:

1. canonical persisted artefacts
2. runtime command/input structures
3. model-facing projections
4. model-response structures
5. deterministic validation results
6. event payloads

A model-facing projection may expose only the data needed for that call.

It must not be treated as a second canonical source of truth.

Model output is untrusted until validated and transformed by the appropriate runtime boundary.

### 3.5 Persistence Adapters

Persistence adapters own storage mechanics.

They may:

- read canonical JSON/YAML artefacts
- write new immutable versions
- append domain events
- rebuild or update SQLite projections
- read/write approved filesystem paths
- resolve exact artefact versions and hashes

They must not:

- invent domain decisions
- modify frozen historical versions
- bypass canonical invariants
- make SQLite authoritative
- allow a Skill to write directly to canonical storage

## 4. Dependency Direction

Runtime dependencies flow inward toward stable contracts.

Conceptually:

```text
CLI / Entry Point
       |
       v
  Orchestrator
   /    |     \
  v     v      v
Skills Services Adapters
  |       |       |
  v       v       v
Knowledge Config Storage / Tools
```

Additional rules:

- Skills do not import persistence adapters.
- Skills do not import provider adapters.
- Skills do not allocate canonical IDs.
- Deterministic services do not call the model.
- Persistence adapters do not call Skills.
- Tool adapters do not own workflow sequencing.
- Prompts do not own persistence.
- Config is consumed; it is not mutated by runtime reasoning.

## 5. Model Boundary

Every model invocation must have an explicit contract consisting of:

- invocation purpose
- selected Skill or reasoning role
- exact input projection
- retrieved knowledge references
- applicable config-derived constraints
- required output shape
- uncertainty expectations
- validation path
- retry behavior
- failure behavior

Raw model output must never become canonical state merely because generation completed successfully.

The runtime must validate, normalize and bind outputs before persistence.

## 6. Skill Boundary

The five frozen Skills remain:

- `product-intelligence`
- `market-intelligence-cl`
- `creative-strategist`
- `script-engine`
- `compliance-reviewer`

The runtime may invoke them but must not absorb or duplicate their procedural reasoning.

Skill outputs are reasoning results, not canonical persistence operations.

The orchestrator determines when the result is eligible to proceed to deterministic validation, persistence or a human gate.

## 7. Knowledge Boundary

Knowledge remains retrieved rather than embedded.

Runtime retrieval must preserve, where applicable:

- `knowledge_id`
- provenance
- tier
- retrieval policy
- source reference

The runtime must exclude:

- quarantine material from production retrieval
- `KNW-schwartz-integration` from runtime knowledge consumption

`KNW-schwartz-integration` remains design-time input only.

## 8. Config Boundary

The nine frozen config registries remain policy-bearing inputs:

- evidence policy
- deny list
- narrative library
- format profiles
- category profiles
- creative taxonomy
- experiment variables
- diversity targets
- tool capability

Phase 5 runtime code may interpret and enforce config.

Runtime code must not silently hardcode a policy value merely because the current config happens to contain that value.

## 9. Persistence Boundary

Canonical state remains based on immutable, versioned artefacts and append-only events.

SQLite remains a rebuildable projection and is never authoritative.

The runtime must preserve:

- immutable canonical artefact versions
- immutable entity records
- append-only events
- exact version/hash binding
- deterministic package identity
- no model-generated canonical IDs

Writes occur only through deterministic persistence boundaries.

## 10. Human Gates

The three frozen human gates remain workflow boundaries:

1. Truth & Evidence
2. Concepts & Experiment Plan
3. Production Release

The runtime may prepare gate material and record gate decisions.

It must not simulate human approval.

A missing required approval blocks downstream execution.

## 11. Failure Model

Runtime failures must be explicit.

At minimum, runtime execution must distinguish:

- invalid input
- missing required evidence
- schema-invalid model output
- deterministic validation failure
- policy/config block
- unresolved evidence conflict
- retrieval failure
- model invocation failure
- tool invocation failure
- persistence failure
- human-gate pending
- unsupported capability
- internal invariant violation

Retries must be deliberate and bounded.

A retry must not silently relax a frozen invariant.

## 12. Phase 5 Design Rule

No runtime implementation begins until the following contracts are designed:

1. package/module topology
2. orchestration state model
3. runtime command contract
4. model invocation contract
5. deterministic service boundaries
6. schema ownership
7. persistence adapter boundary
8. config loading boundary
9. knowledge retrieval boundary
10. external tool adapter boundary
11. error taxonomy
12. observability/event boundary
13. test architecture

Only after these contracts are reviewed may `src/` or `tests/` be created.

## 13. Package / Module Topology

The following topology is the planned runtime source layout.

It is a design contract only. Phase 5 does not create `src/` yet.

```text
src/creative_os/
  __init__.py
  cli.py
  runtime/
    __init__.py
  orchestration/
    __init__.py
  model/
    __init__.py
  services/
    __init__.py
  schemas/
    __init__.py
  adapters/
    __init__.py
    persistence/
      __init__.py
    config/
      __init__.py
    knowledge/
      __init__.py
    model/
      __init__.py
    tools/
      __init__.py
  prompts/
    __init__.py
```

The frozen Skills remain outside this tree under `.claude/skills/`.

Repository roots such as `config/`, `knowledge/`, `store/`, `media/` and `var/` remain data or operational roots, not Python packages.

### 13.1 Top-Level Ownership

- `cli.py` is a thin entry boundary. It parses user-facing invocation and delegates to runtime commands.
- `runtime/` owns provider-neutral runtime commands, execution context and run-level coordination contracts.
- `orchestration/` owns stage sequencing, human gates, retries and workflow progression.
- `model/` owns provider-neutral model invocation contracts and validated model-call results.
- `services/` owns deterministic domain computation and validation.
- `schemas/` owns machine-checkable data interfaces and contains no I/O behavior.
- `adapters/` owns interaction with storage, config, knowledge, model providers and external tools.
- `prompts/` owns runtime model-facing prompt resources and their loading boundary.

### 13.2 Structural Rules

- Provider SDK imports are allowed only behind the relevant adapter boundary.
- Deterministic services must remain free of model, network and persistence calls.
- Schemas must not perform workflow sequencing or external I/O.
- Orchestration may depend on contracts but must not implement provider-specific transport.
- Runtime prompts must not duplicate policy, knowledge or frozen Skill procedure.
- Root data directories must not be imported as if they were Python packages.
- No generic `utils.py`, `helpers.py` or equivalent catch-all module is permitted.
- No single orchestrator module may absorb deterministic services, persistence and model transport.

### 13.3 Runtime Modules

The planned `runtime/` package is:

```text
runtime/
  __init__.py
  commands.py
  context.py
  run_head.py
```

Ownership:

- `commands.py` owns provider-neutral runtime command definitions and dispatch-facing command identity.
- `context.py` owns the explicit per-run execution context passed through runtime boundaries.
- `run_head.py` owns assembly of the exact run-level references required by the frozen data architecture.

Runtime module rules:

- Runtime commands express requested execution; they do not perform persistence or provider transport themselves.
- CLI parsing must not leak into runtime command definitions.
- Execution context must be passed explicitly rather than hidden in mutable process globals.
- Execution context may reference resolved dependencies, config snapshots and exact artefact bindings.
- `run_head.py` assembles run metadata but does not invent model-generated canonical IDs.
- Runtime modules coordinate contracts; strategic reasoning remains in Skills.

### 13.4 Orchestration Modules

The planned `orchestration/` package is:

```text
orchestration/
  __init__.py
  engine.py
  stages.py
  state.py
  transitions.py
  gates.py
  retries.py
```

Ownership:

- `engine.py` owns workflow execution and delegates work to the appropriate boundary.
- `stages.py` owns the named workflow-stage definitions and their required entry/exit contracts.
- `state.py` owns the in-memory orchestration state representation for an active run.
- `transitions.py` owns workflow progression requests and delegates deterministic transition validity to the appropriate service.
- `gates.py` owns orchestration behavior around the three frozen human gates.
- `retries.py` owns bounded retry policy execution using retry constraints supplied by runtime policy or config.

### 13.5 Orchestration Separation Rules

- `engine.py` must not contain provider SDK calls.
- `engine.py` must not implement deterministic domain algorithms.
- `engine.py` must not embed Skill procedure.
- `stages.py` describes workflow structure; it does not persist canonical artefacts.
- `state.py` is active-run state, not canonical persisted source of truth.
- `transitions.py` coordinates transitions but does not replace deterministic state-transition validation.
- `gates.py` may detect pending approval but must never fabricate human approval.
- `retries.py` must never relax an invariant, compliance decision or required human gate.
- Retry counts and timing values that are policy-bearing must come from config or an explicit runtime contract rather than hidden constants.

### 13.6 Orchestrator Anti-Monolith Constraint

The orchestration engine is a coordinator, not a domain service.

Adding a new deterministic rule must normally extend `services/`, not `engine.py`.

Adding provider-specific behavior must normally extend an adapter, not `engine.py`.

Adding reusable persuasion or creative reasoning must remain in the frozen Skill boundary rather than move into orchestration.

### 13.7 Deterministic Service Modules

The planned `services/` package is:

```text
services/
  __init__.py
  ids.py
  bindings.py
  evidence.py
  claims.py
  policy_checks.py
  diversity.py
  experiment_lock.py
  packages.py
  localization.py
  feasibility.py
  manifests.py
  transitions.py
```

Ownership:

- `ids.py` owns deterministic canonical ID construction and ID validation.
- `bindings.py` owns deterministic version, content-hash and exact-reference binding checks.
- `evidence.py` owns deterministic evidence coverage and evidence-eligibility computation defined by config and frozen contracts.
- `claims.py` owns deterministic claim-freedom computation and claim-binding checks.
- `policy_checks.py` owns deterministic deny-list checks and deterministic HARD_BLOCK conditions only.
- `diversity.py` owns deterministic diversity measurement, constraint evaluation and final selection mechanics.
- `experiment_lock.py` owns deterministic validation that approved experiment variables remain locked where required.
- `packages.py` owns pure-derived production package identity and package-level deterministic consistency checks.
- `localization.py` owns deterministic localization-invariance checks after language generation.
- `feasibility.py` owns deterministic feasibility checks against supplied format and tool-capability constraints.
- `manifests.py` owns deterministic manifest structure, reference and integrity validation.
- `transitions.py` owns deterministic state-transition validity against the frozen state machines.

### 13.8 Deterministic Service Rules

- Services receive explicit inputs and return explicit results.
- Services must not call Skills or language models.
- Services must not perform network access.
- Services must not write canonical persistence directly.
- Services may consume validated config values supplied through their call boundary.
- Services must not silently invent policy defaults when required config is missing.
- `policy_checks.py` must remain separate from open-ended compliance judgement owned by `compliance-reviewer`.
- `claims.py` must not decide persuasive strategy or rewrite copy.
- `diversity.py` selects from supplied eligible candidates; it does not generate new creative concepts.
- `localization.py` checks semantic invariance; Chilean expression generation remains in `script-engine`.
- `feasibility.py` evaluates supplied capability constraints; it does not own external production routing.
- State-transition validation remains deterministic even when orchestration requests the transition.

### 13.9 Schema Modules

The planned `schemas/` package is:

```text
schemas/
  __init__.py
  canonical.py
  commands.py
  projections.py
  model_results.py
  validation.py
  events.py
```

Ownership:

- `canonical.py` owns runtime schema representations of the frozen canonical artefact and entity contracts.
- `commands.py` owns machine-checkable runtime command and command-input structures.
- `projections.py` owns minimal model-facing input projections for individual invocations.
- `model_results.py` owns required structured shapes returned from model-facing reasoning calls.
- `validation.py` owns structures used to report deterministic validation outcomes, violations and warnings.
- `events.py` owns machine-checkable payload structures for the frozen domain event types.

### 13.10 Schema Ownership Rules

- Schema modules contain data contracts, not workflow execution.
- Schema modules perform no external I/O.
- Canonical schemas must reflect the frozen data architecture rather than redefine it.
- A model-facing projection is not canonical state.
- A model-result schema describes expected structure but does not make model output trusted.
- Model output becomes eligible for persistence only after required validation and deterministic transformation.
- Validation-result schemas must distinguish machine failure from warnings and model judgement.
- Event schemas must preserve append-only event semantics.
- Schema validation must not allocate model-generated canonical IDs.

### 13.11 Service-to-Schema Boundary

Deterministic services consume validated schema-compatible inputs and return schema-compatible results.

Schemas describe shape; services enforce deterministic domain rules.

Neither layer owns orchestration sequencing, Skill reasoning, provider transport or persistence mechanics.
