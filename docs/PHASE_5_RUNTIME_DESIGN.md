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

### 13.12 Adapter Modules

The planned `adapters/` package is:

```text
adapters/
  __init__.py
  persistence/
  config/
  knowledge/
  model/
  tools/
```

Each adapter family isolates an external or infrastructure-facing concern from the runtime core.

### 13.13 Persistence Adapters

`adapters/persistence/` owns canonical filesystem storage, append-only event storage and SQLite projection mechanics.

Persistence adapters execute storage operations requested by the runtime but do not make domain decisions.

SQLite remains rebuildable and non-authoritative.

### 13.14 Config Adapters

`adapters/config/` owns loading, parsing and validating the nine frozen config registries.

Config adapters return validated config snapshots to runtime consumers.

They must not invent missing policy values or mutate config as a side effect of model reasoning.

### 13.15 Knowledge Adapters

`adapters/knowledge/` owns retrieval from approved knowledge sources.

Retrieval results preserve applicable knowledge identity, provenance, tier and retrieval policy.

Production retrieval excludes quarantine material and `KNW-schwartz-integration`.

### 13.16 Model Provider Adapters

`adapters/model/` owns provider-specific model transport.

Provider SDKs, authentication, request formatting and raw provider responses remain behind this boundary.

Model adapters do not own Skill procedure, workflow sequencing or persistence.

### 13.17 External Tool Adapters

`adapters/tools/` owns integrations with external production and analysis capabilities.

Examples may include video generation, image generation, voice generation or other approved providers.

Tool adapters expose normalized capability contracts to the runtime.

They do not decide creative strategy or production routing policy.

### 13.18 Adapter Boundary Rules

- Provider SDK imports remain inside the relevant adapter family.
- Adapters must not call frozen Skills directly.
- Adapters must not own workflow sequencing.
- Adapters must not silently bypass deterministic validation.
- Persistence adapters do not make SQLite authoritative.
- Config adapters do not invent policy defaults.
- Knowledge adapters do not expose quarantine material to production runtime.
- Model adapters treat raw model output as untrusted.
- Tool adapters report capabilities and results; orchestration decides when they are invoked.

### 13.19 Model Runtime Modules

The planned `model/` package is:

```text
model/
  __init__.py
  invocation.py
  requests.py
  responses.py
  validation.py
```

Ownership:

- `invocation.py` owns provider-neutral model invocation coordination.
- `requests.py` owns normalized model request contracts.
- `responses.py` owns normalized model response contracts.
- `validation.py` owns structural validation of model-returned data before downstream use.

Model runtime rules:

- Model runtime code must remain provider-neutral.
- Provider-specific SDK calls belong in `adapters/model/`.
- Raw provider output is untrusted.
- Model invocation does not write canonical persistence directly.
- Model invocation does not allocate canonical IDs.
- Model invocation must use explicit input projections and required output contracts.

### 13.20 Prompt Modules

The planned `prompts/` package is:

```text
prompts/
  __init__.py
  loader.py
  runtime/
```

`loader.py` owns loading runtime prompt resources.

`prompts/runtime/` contains stage-specific model-facing prompt resources.

Prompt resources may compose runtime context, Skill selection, retrieved knowledge and config-derived constraints.

Prompt resources must not duplicate frozen Skill procedure, policy registries or knowledge bodies.

### 13.21 Model and Prompt Boundary Rules

- Prompts describe a model call; they do not own workflow sequencing.
- Prompts do not write persistence.
- Prompts do not contain authoritative policy values that belong in config.
- Prompts do not embed retrieved knowledge bodies as permanent source material.
- Model runtime validates structure but does not replace deterministic domain services.
- Skill procedure remains in `.claude/skills/` rather than being copied into runtime prompts.

## 14. Orchestration State Model

The orchestration state model represents the active execution status of one runtime run.

It is operational state only.

It does not replace, redefine or become authoritative over the frozen canonical state machines from Phase 2.

### 14.1 Run Lifecycle

An active run may occupy one of these orchestration lifecycle states:

- `READY` — validated prerequisites exist and execution may begin.
- `RUNNING` — the orchestrator is actively executing a stage.
- `WAITING_HUMAN` — execution is paused at a required human gate.
- `RETRY_PENDING` — a bounded retry is eligible but has not yet executed.
- `BLOCKED` — deterministic policy, invariant or required input prevents progression.
- `FAILED` — execution terminated because a non-recoverable runtime failure occurred.
- `COMPLETED` — the requested runtime command completed successfully.

These lifecycle values describe orchestration execution only.

Canonical artefact/entity states remain governed by the frozen Phase 2 state machines.

### 14.2 Active Run State

The in-memory active run state must carry explicit runtime context.

At minimum it records:

- exact run identity supplied through deterministic runtime mechanisms
- current runtime command
- current orchestration stage
- orchestration lifecycle state
- exact input artefact/version bindings
- config snapshot references
- retrieved knowledge references
- completed stage records
- pending human gate, if any
- retry counters and retry eligibility
- current failure/block reason, if any
- validated outputs available to downstream stages

Active run state is transient coordination state.

It must not be treated as canonical persisted source of truth.

### 14.3 State Ownership Rules

- `orchestration/state.py` owns the active in-memory representation.
- The orchestrator requests state changes; deterministic transition validation remains separate.
- Human approval is recorded only from an actual gate decision.
- Retry state must preserve the reason for the previous failure.
- A blocked run must not progress until its blocking condition is resolved through an allowed path.
- Completion requires all command-specific mandatory stages and gates to be satisfied.
- Runtime state must never silently relax frozen invariants.

### 14.4 Stage Progression

Each orchestration stage has explicit entry conditions and exit conditions.

A stage may begin only when:

- required upstream outputs exist
- required deterministic validations have passed
- required config is available
- required knowledge retrieval is complete or explicitly not required
- no unresolved blocking condition is active
- any required upstream human gate has been approved

A stage may finish only when its mandatory outputs have been produced and validated.

The orchestrator must not skip a mandatory stage merely because a later output appears generatable.

### 14.5 Human Gate Transitions

The three frozen human gates are:

1. Truth & Evidence
2. Concepts & Experiment Plan
3. Production Release

When a required gate is reached:

- lifecycle changes to `WAITING_HUMAN`
- downstream execution stops
- the pending gate identity is recorded
- exact artefact/version bindings presented for approval are recorded

On approval:

- the gate decision is recorded
- approved bindings remain exact
- execution may continue only from the permitted downstream stage

On rejection:

- the rejection reason is recorded
- the run does not advance
- remediation follows an explicit allowed path

The runtime must never infer, fabricate or auto-approve a human gate.

### 14.6 Retry Transitions

A recoverable failure may move `RUNNING` to `RETRY_PENDING` only when the failure class explicitly permits retry.

Retry execution must preserve:

- original failure class
- original failure reason
- retry attempt number
- maximum permitted attempts
- any changed runtime input used for the retry

If retry eligibility is exhausted, the run moves to `FAILED` or `BLOCKED` according to the failure class.

A retry must never:

- bypass a required human gate
- weaken deterministic validation
- relax compliance or policy constraints
- invent missing evidence
- mutate frozen artefact history

### 14.7 Blocking Transitions

`BLOCKED` represents a condition that prevents legal progression but may be resolvable without treating the run as internally failed.

Examples include:

- required evidence missing
- required config missing
- required approval pending or rejected
- deterministic HARD_BLOCK
- unsupported tool capability

A blocked run may resume only after the specific blocking condition is resolved through an allowed transition.

### 14.8 Failure-to-State Mapping

Runtime failure classes map to orchestration behavior explicitly.

Default mappings are:

- invalid input -> `BLOCKED`
- missing required evidence -> `BLOCKED`
- schema-invalid model output -> `RETRY_PENDING` when retry eligibility remains, otherwise `FAILED`
- deterministic validation failure -> `BLOCKED`
- policy/config block -> `BLOCKED`
- unresolved evidence conflict -> `BLOCKED`
- retrieval failure -> `RETRY_PENDING` when recoverable, otherwise `FAILED`
- model invocation failure -> `RETRY_PENDING` when recoverable, otherwise `FAILED`
- tool invocation failure -> `RETRY_PENDING` when recoverable, otherwise `FAILED`
- persistence failure -> `RETRY_PENDING` when recoverable, otherwise `FAILED`
- human-gate pending -> `WAITING_HUMAN`
- unsupported capability -> `BLOCKED`
- internal invariant violation -> `FAILED`

These mappings describe default runtime behavior.

Specific retry eligibility may be further constrained by the runtime command, config or deterministic failure classification.

### 14.9 Terminal States

`COMPLETED` and `FAILED` are terminal orchestration states for a run execution attempt.

`BLOCKED` is non-progressing but may be resumable if its blocking condition is explicitly resolved.

`WAITING_HUMAN` is paused rather than terminal.

`RETRY_PENDING` is temporary and must resolve to another lifecycle state through an explicit retry transition.

### 14.10 Completion Rules

A run may become `COMPLETED` only when:

- the requested runtime command has satisfied its mandatory stages
- all required deterministic validations have passed
- all required human gates have approved exact bound artefact versions
- required persistence operations have succeeded
- no unresolved block or failure remains

Completion represents successful execution of the requested command, not proof that every possible downstream workflow has run.

### 14.11 Failure Preservation

Failure information must remain inspectable after a run stops progressing.

At minimum the runtime preserves:

- failure class
- machine-readable failure code
- human-readable reason
- stage where the failure occurred
- retry eligibility
- retry count
- relevant artefact/version bindings
- relevant provider or adapter reference when applicable

The runtime must not convert a failure into success merely because partial outputs exist.

## 15. Runtime Command Contract

A runtime command is a provider-neutral request for the system to execute a defined workflow objective.

Commands express intent and required scope.

They do not contain Skill procedure, provider transport or persistence mechanics.

### 15.1 Command Categories

V1 runtime commands are grouped into these categories:

- truth and evidence commands
- market intelligence commands
- strategy and hypothesis commands
- concept and experiment commands
- creative execution commands
- compliance and validation commands
- production preparation commands

### 15.2 Common Command Contract

Every runtime command definition must declare:

- command name
- command purpose
- required input bindings
- optional input bindings
- required config snapshots
- required knowledge retrieval classes
- mandatory orchestration stages
- permitted Skill invocations
- required deterministic validations
- required human gates
- expected canonical outputs
- expected non-canonical runtime outputs
- retry eligibility
- blocking conditions
- completion conditions

### 15.3 Command Boundary Rules

- Commands describe requested execution; they do not perform execution themselves.
- Commands must remain provider-neutral.
- Commands do not embed policy values.
- Commands do not embed knowledge bodies.
- Commands do not allocate model-generated canonical IDs.
- Commands do not bypass human gates.
- Commands do not silently widen their own scope during execution.
- A command may invoke multiple Skills only through orchestration.
- Command completion must be evaluated against its declared completion conditions.

### 15.4 `build_product_truth`

Purpose: establish the evidence-bound Product Truth required by downstream creative work.

Required scope:

- supplied product and brand inputs
- available evidence references
- applicable evidence-policy config snapshot

Permitted Skill:

- `product-intelligence`

Required runtime behavior:

- distinguish observed, supported, inferred and unknown information according to frozen contracts
- run required deterministic evidence and binding validation
- preserve uncertainty and unresolved conflicts
- prepare exact material for Human Gate 1: Truth & Evidence

Completion requires the required Product Truth output to be valid, bound and approved where Human Gate 1 applies.

### 15.5 `research_chile_market`

Purpose: build Chile-specific market intelligence from approved product context and retrieved evidence.

Required scope:

- approved Product Truth bindings
- approved market-research inputs
- eligible Chile market evidence
- applicable research config snapshots

Permitted Skill:

- `market-intelligence-cl`

Required runtime behavior:

- retrieve only eligible knowledge and research sources
- preserve evidence references and provenance
- surface problems, desires, objections, alternatives, customer language, awareness and sophistication signals
- preserve research gaps and conflicting signals

The command does not create creative concepts or scripts.

### 15.6 `build_strategy_hypotheses`

Purpose: transform approved truth and market intelligence into falsifiable creative strategy.

Required scope:

- approved Product Truth bindings
- validated market-intelligence inputs
- applicable strategy config snapshots
- eligible persuasion knowledge

Permitted Skill:

- `creative-strategist`

Expected reasoning outputs include:

- Audience Model
- Persuasion Projection
- Insights
- falsifiable Hypotheses

Required runtime behavior:

- preserve exact upstream bindings
- reject a proposed Hypothesis without a falsification condition
- run required deterministic schema and binding validation
- stop before concept selection, scripting or production

This command produces strategy candidates for downstream concept and experiment work.

### 15.7 `build_concepts`

Purpose: transform validated Hypotheses into format-agnostic Concept candidates.

Required scope:

- validated Hypothesis bindings
- approved upstream Product Truth and market-intelligence bindings
- applicable creative-taxonomy and strategy config snapshots

Permitted Skill:

- `creative-strategist`

Required runtime behavior:

- preserve the strategic dimensions inherited from each Hypothesis
- preserve the Hypothesis falsification condition
- produce Concept candidates without scripting or production execution
- validate Concept structure and upstream bindings

A Concept must remain format-agnostic at this stage.

The command does not perform final diversity selection.

### 15.8 `select_experiment_plan`

Purpose: deterministically select an eligible and strategically diverse experiment set from supplied candidates.

Required scope:

- validated Hypothesis and Concept candidates
- creative-taxonomy config snapshot
- experiment-variables config snapshot
- diversity-targets config snapshot

Required deterministic services include:

- eligibility validation
- duplicate and overlap evaluation
- diversity measurement
- experiment-variable validation
- deterministic final selection mechanics
- experiment-lock validation

The selection process must not generate new Concepts to repair a weak candidate pool.

If the candidate pool cannot satisfy required constraints, the command blocks and surfaces the deficiency.

The resulting experiment plan is prepared for Human Gate 2: Concepts & Experiment Plan.

### 15.9 Concept and Experiment Boundary

- Skill reasoning proposes strategic candidates.
- Deterministic services evaluate selection constraints.
- The orchestrator coordinates the process.
- Human Gate 2 approves the exact experiment-plan bindings.
- No script or production package is created before the approved experiment boundary permits it.
- Gate 2 approval must not contain forward creative IDs that do not yet exist.

### 15.10 `build_creatives`

Purpose: transform an approved experiment plan into production-oriented Creative execution candidates without invoking production providers.

Required scope:

- Human Gate 2 approved experiment-plan bindings
- exact approved Hypothesis and Concept bindings
- applicable narrative-library config snapshot
- applicable format-profile config snapshot
- applicable creative-taxonomy config snapshot
- supplied eligible voice and style options when relevant
- eligible persuasion and language knowledge

Permitted Skill:

- `script-engine`

Expected reasoning outputs include:

- Hook Strategy
- selected format, narrative, style and voice fit from supplied eligible options
- persuasion beats
- complete exact word-for-word script
- Chile-localized final language
- hook execution
- storyboard and shot list
- continuity-aware visual plan
- explicit execution gaps or uncertainties

Required runtime behavior:

- preserve exact approved Hypothesis and Concept bindings
- preserve experiment-variable locks
- require complete scripts without unresolved placeholders
- run structural schema validation
- run deterministic localization-invariance checks where required
- preserve unresolved execution gaps rather than invent unsupported facts
- prepare outputs for downstream compliance and production checks

### 15.11 Creative Execution Boundary

- `script-engine` owns creative execution reasoning, not production-provider invocation.
- Voice fit selects among supplied eligible options; it does not synthesize audio.
- Storyboard and shot list describe production intent; they do not generate media.
- Chile localization changes expression without changing approved strategic meaning.
- Claim verification and claim-freedom computation remain deterministic downstream concerns.
- Compliance judgement remains owned by `compliance-reviewer`.
- No audio, image or video generation occurs inside `build_creatives`.
- No production package is released before downstream validation permits it.

### 15.12 `review_creatives`

Purpose: evaluate finalized Creative candidates for semantic compliance risk and required deterministic creative validation before production preparation.

Required scope:

- finalized Chile-localized Creative bindings
- exact Product Truth and approved experiment bindings
- applicable evidence-policy and deny-list config snapshots
- applicable category-profile config snapshot
- current policy context when required

Permitted Skill:

- `compliance-reviewer`

Compliance judgement may evaluate:

- implied claims
- ambiguity as risk
- semantic claim intensification
- testimonial risk
- before/after risk
- native-format impersonation risk
- category-sensitive risk
- qualification sufficiency
- urgency and scarcity risk
- current policy-sensitive concerns

Permitted compliance verdicts are:

- `LOW`
- `MEDIUM`
- `HIGH_RISK`
- `POLICY_REVIEW_REQUIRED`

Required deterministic validation may include:

- claim binding validation
- claim-freedom computation
- deterministic deny-list checks
- deterministic HARD_BLOCK checks
- localization-invariance validation
- exact upstream binding validation
- structural schema validation

### 15.13 Compliance and Validation Boundary

- `compliance-reviewer` provides judgement; it does not author policy.
- `compliance-reviewer` does not issue deterministic `HARD_BLOCK`.
- Deterministic `HARD_BLOCK` conditions remain owned by deterministic services and config.
- Claim verification is not delegated to the compliance Skill.
- A low compliance-risk verdict does not override deterministic validation failure.
- A deterministic pass does not erase semantic risk surfaced by the compliance Skill.
- Review findings must remain bound to the exact localized Creative version reviewed.
- Failed or unresolved review does not proceed silently to production.
- This command does not invoke audio, image or video generation.

### 15.14 `prepare_production`

Purpose: transform validated Creative outputs into exact production-ready packages without invoking media-generation providers.

Required scope:

- reviewed and validated Creative bindings
- exact approved experiment bindings
- applicable format-profile config snapshot
- applicable tool-capability config snapshot
- eligible production-tool options
- eligible and authorized voice options when speech is required
- required product, character, visual or reference assets

Expected production-package content includes:

- exact Creative and script bindings
- target duration and aspect ratio
- approved format and visual execution plan
- storyboard and shot requirements
- required source and reference assets
- selected or eligible voice profile bindings
- language and locale requirements
- candidate provider/tool routes
- capability requirements
- deterministic feasibility results
- estimated generation cost when available
- applicable runtime or config-supplied budget constraint
- unresolved production risks or missing inputs

Required runtime behavior:

- validate that required assets and bindings exist
- validate experiment locks before production release
- validate tool capability against the requested execution
- estimate provider cost before generation when the provider exposes cost estimation
- surface an over-budget route before any paid generation occurs
- preserve provider-neutral production intent separately from provider-specific execution details
- prepare exact material for Human Gate 3: Production Release

### 15.15 Voice Preparation Boundary

When speech is required, production preparation may bind an eligible authorized voice profile.

A voice profile identifies an approved voice option and its relevant execution metadata.

Voice selection must come from supplied eligible options rather than being invented by the production adapter.

The approved script remains the source text for speech generation.

Voice synthesis itself occurs only after Production Release through an approved production tool boundary.

### 15.16 Cost and Capability Boundary

- Cost estimates are provider observations, not creative-quality judgements.
- Budget limits are supplied through explicit runtime or config policy rather than hidden constants.
- Tool adapters report supported capabilities and estimated costs when available.
- Tool adapters do not decide whether a creative is strategically worth producing.
- The runtime may reject or escalate a production route that exceeds its supplied budget constraint.
- A cheaper provider route must not silently weaken an approved experiment variable or required execution constraint.

### 15.17 Production Release Boundary

- `prepare_production` performs no paid media generation.
- Human Gate 3 approves exact production-package bindings.
- Production providers may be invoked only after required Production Release approval.
- Approval of one package does not implicitly approve another package or later mutated version.
- Provider-specific results remain downstream of the frozen production-package intent.

## 16. Model Invocation Contract

A model invocation is an explicit provider-neutral reasoning request executed through the runtime model boundary.

Every invocation must be independently inspectable and reproducible from its bound inputs.

### 16.1 Required Invocation Fields

Every model invocation declares:

- invocation identity
- invocation purpose
- runtime command and orchestration stage
- selected Skill or explicit reasoning role
- exact input projection
- exact upstream artefact/version bindings
- retrieved knowledge references
- applicable config-derived constraints
- required output schema
- uncertainty requirements
- validation path
- retry eligibility
- failure behavior

### 16.2 Input Projection Rule

The model receives only the minimum runtime projection required for the invocation.

Canonical storage objects must not be exposed wholesale merely because they are available.

Input projections are derived views and never become an alternative canonical source of truth.

### 16.3 Skill Invocation Rule

When a frozen Skill owns the requested reasoning procedure, the invocation must identify that Skill explicitly.

The runtime must not copy frozen Skill procedure into ad-hoc prompts as a substitute for Skill invocation.

A model invocation may use only the knowledge classes permitted by the selected Skill and runtime boundary.

### 16.4 Output Trust Boundary

Model output is untrusted until required structural and deterministic validation succeeds.

A successful provider response does not imply a successful runtime invocation.

Schema-invalid output must not be persisted as canonical state.

Validated model output may proceed only to the downstream boundary declared by the runtime command.

## 16. Model Invocation Contract

A model invocation is an explicit provider-neutral reasoning request executed through the runtime model boundary.

Every invocation must be independently inspectable and reproducible from its bound inputs.

### 16.5 Invocation Assembly

A model invocation is assembled from distinct runtime inputs rather than one undifferentiated prompt body.

The invocation assembly may include:

- selected frozen Skill procedure
- stage-specific runtime prompt resource
- minimal model-facing input projection
- retrieved knowledge references and excerpts permitted by the Skill
- validated config-derived constraints
- required output schema
- run and artefact binding metadata required for traceability

### 16.6 Assembly Ownership

The orchestrator coordinates invocation assembly.

Runtime prompt loading is owned by the prompt boundary.

Knowledge retrieval is owned by the knowledge adapter.

Config loading and validation are owned by the config adapter.

Input projections and output schemas are owned by the schema boundary.

Provider request formatting is owned by the model adapter.

No single assembly component becomes authoritative over the others.

### 16.7 Knowledge Injection Rules

- Knowledge is retrieved for the invocation and is not permanently embedded into runtime prompts.
- Every injected knowledge item preserves its applicable identity and provenance metadata.
- Knowledge consumption must respect the selected Skill knowledge declaration.
- Quarantine material is excluded from production runtime retrieval.
- `KNW-schwartz-integration` is never injected into runtime model calls.
- Missing required knowledge must be surfaced rather than replaced with invented content.

### 16.8 Config Injection Rules

- Only validated config values relevant to the invocation are injected.
- Config values remain distinguishable from model-authored text and retrieved knowledge.
- Runtime prompts must not duplicate authoritative config values as hidden constants.
- Missing required config blocks execution rather than causing the model to invent a default.

### 16.9 Prompt Composition Rules

- Runtime prompts frame the current task and output expectations.
- Runtime prompts do not restate the full frozen Skill procedure.
- Runtime prompts do not permanently embed knowledge bodies.
- Runtime prompts do not redefine canonical schemas.
- Runtime prompts do not override deterministic validation or human gates.

### 16.10 Schema Binding

Every structured model invocation binds an explicit required output schema before provider execution.

The schema must be known before the model response is received.

A provider response that cannot satisfy the bound schema is treated as an invalid model result.

### 16.11 Model Result Validation

Model results pass through explicit validation before downstream use.

Validation occurs in this order:

1. provider response availability
2. response decoding and structural parsing
3. bound output-schema validation
4. required binding and reference validation
5. applicable deterministic domain validation
6. downstream eligibility decision

A result that fails an earlier validation layer must not bypass that layer because later content appears useful.

### 16.12 Invalid Model Result Classes

At minimum, model-result failures distinguish:

- provider transport failure
- empty or unusable provider response
- decoding or parsing failure
- schema-invalid structure
- missing required field
- invalid enum or constrained value
- missing or invalid upstream binding
- unsupported canonical reference
- deterministic domain-rule failure
- unresolved uncertainty required by the invocation contract

### 16.13 Retry Eligibility

Only failures classified as recoverable may enter model-invocation retry behavior.

Retry-eligible examples may include:

- transient provider transport failure
- rate-limit or temporary provider availability failure
- decoding failure where a bounded repair attempt is permitted
- schema-invalid model output where a bounded correction attempt is permitted

Non-retryable examples include:

- missing required upstream evidence
- deterministic HARD_BLOCK
- missing required config
- required human approval not granted
- invariant violation caused by invalid canonical state

### 16.14 Retry Rules

- Retry attempts are bounded.
- Every retry preserves the original invocation identity lineage.
- Every retry records the previous failure class and reason.
- Retry instructions may clarify structural requirements but must not silently relax domain constraints.
- A retry must not fabricate missing upstream data.
- A retry must not bypass required deterministic validation.
- A retry must not substitute a different Skill unless the runtime command explicitly permits that change.
- Exhausted retry eligibility resolves through the orchestration failure model.

### 16.15 Model Repair Boundary

A model-repair attempt may correct formatting or structurally incomplete output only when the required semantic inputs already exist.

Repair must not invent evidence, policy, approvals, canonical IDs or unsupported facts.

Repair output is validated through the same schema and deterministic path as an original model result.

## 17. Deterministic Service Boundaries

A deterministic service implements mechanically enforceable runtime logic whose result must not depend on open-ended model judgement.

Deterministic services must be reproducible from the same validated inputs and applicable config snapshot.

### 17.1 Common Service Contract

Every deterministic service declares:

- service purpose
- accepted input contract
- required config inputs
- deterministic algorithm or rule source
- explicit output contract
- machine-readable failure conditions
- whether warnings are possible
- whether the service may block progression
- relevant frozen invariant references
- test obligations

### 17.2 Determinism Rules

- The same validated inputs and config must produce the same result.
- Services do not call Skills or language models.
- Services do not perform network access.
- Services do not invoke production providers.
- Services do not write canonical persistence directly.
- Services do not fabricate missing config or upstream data.
- Services may reject invalid input rather than infer a convenient replacement.
- Policy-bearing values come from validated config or frozen contracts.
- A deterministic result must be explainable through machine-readable reasons.

### 17.3 Service Result Shape

A deterministic service result must distinguish:

- success or failure status
- normalized output data, when applicable
- violations
- warnings
- machine-readable reason codes
- relevant input bindings
- relevant config bindings

Warnings do not silently override failures.

Successful execution of the service code does not imply that the domain result passed validation.

### 17.4 Identity Service — `ids.py`

`ids.py` owns deterministic construction and validation of canonical runtime identifiers defined by the frozen data architecture.

Accepted inputs may include:

- canonical entity or artefact type
- deterministic identity source fields
- required namespace or prefix information from frozen contracts

The service may:

- validate canonical ID shape
- construct canonical IDs from permitted deterministic inputs
- reject malformed or unsupported IDs
- detect type/ID mismatches

The service must not:

- accept arbitrary model-authored IDs as canonical truth
- generate random identity when the frozen contract requires derivation
- infer an entity type from an invalid identifier
- silently repair an ambiguous identity collision

Identity construction must remain deterministic and testable.

### 17.5 Binding Service — `bindings.py`

`bindings.py` owns deterministic exact-reference binding and verification.

A binding may include:

- canonical artefact or entity ID
- exact version
- content hash
- referenced upstream IDs and versions
- applicable run binding metadata

The service may:

- construct exact bindings from validated canonical inputs
- verify that an ID, version and hash refer to the expected immutable content
- detect stale or mismatched references
- compare expected and actual bindings
- verify that downstream output preserves required upstream bindings

The service must reject:

- mutable aliases where an exact version is required
- version/hash mismatch
- ID/type mismatch
- missing required upstream binding
- binding to content that cannot be deterministically resolved

### 17.6 Identity and Binding Boundary

- Skills never allocate canonical IDs.
- Model output never becomes authoritative for canonical identity.
- Persistence adapters store and retrieve bindings but do not decide whether a binding is valid.
- Orchestration coordinates identity requests but does not implement ID algorithms.
- Exact bindings are established before required human-gate approval.
- Human approval binds the exact versions and hashes presented at the gate.
- Later mutation requires a new version and, where applicable, renewed approval.

### 17.7 Evidence Service — `evidence.py`

`evidence.py` owns deterministic evidence eligibility and coverage computation from validated evidence inputs and the applicable evidence-policy config.

Accepted inputs may include:

- validated evidence records
- evidence provenance and tier metadata
- required claim or artefact context
- applicable evidence-policy config snapshot
- exact upstream bindings

The service may:

- determine evidence eligibility according to frozen rules and config
- compute deterministic evidence coverage
- identify unsupported or insufficiently supported requirements
- preserve the distinction between observed, supported, inferred and unknown information
- return machine-readable coverage gaps and reasons

The service must not:

- invent missing evidence
- upgrade inferred material into substantiating evidence without an allowed rule
- treat model confidence as evidence strength
- silently resolve conflicting evidence through creative judgement

### 17.8 Claim Service — `claims.py`

`claims.py` owns deterministic claim-freedom computation and exact claim-binding checks.

Accepted inputs may include:

- finalized or candidate claim text
- exact Product Truth bindings
- eligible evidence results
- applicable evidence-policy config
- category-profile constraints where required

The service may:

- compute allowed claim freedom from validated evidence and frozen rules
- verify that a claim remains within its approved evidence boundary
- detect unsupported claim intensification
- detect claim drift between approved and localized or revised copy
- report claim-specific violations and reason codes

The service must not:

- write persuasive copy
- decide strategic messaging priority
- invent substantiation
- replace open-ended compliance judgement

### 17.9 Evidence and Claim Boundary

- `product-intelligence` reasons about Product Truth; it does not calculate deterministic evidence coverage.
- `script-engine` writes claims and copy; it does not decide claim freedom.
- `compliance-reviewer` evaluates semantic risk; it does not verify substantiation.
- Evidence eligibility and claim freedom remain deterministic downstream controls.
- Inferred basis alone must not substantiate hard claims where the frozen evidence contract forbids it.
- A localized or rewritten claim must remain within the same approved evidence boundary.
- Claim validation binds to the exact final text being reviewed or produced.

### 17.10 Policy Check Service — `policy_checks.py`

`policy_checks.py` owns deterministic policy and deny-list checks whose outcomes are mechanically derivable from validated inputs and policy-bearing config.

Accepted inputs may include:

- exact Creative or claim bindings
- deterministic claim-validation results
- applicable deny-list config snapshot
- applicable category-profile config snapshot
- other explicitly required validated policy-bearing config

The service may:

- evaluate configured deterministic deny-list conditions
- evaluate configured category-sensitive deterministic restrictions
- return machine-readable policy violations
- emit deterministic `HARD_BLOCK` only when a frozen or configured rule explicitly requires it
- preserve the exact rule and config binding responsible for a block

The service must not:

- perform open-ended semantic compliance judgement
- infer new policy from model knowledge
- author or modify policy rules
- fetch or reinterpret external policy independently
- convert a compliance-risk opinion into `HARD_BLOCK` without a deterministic rule
- silently relax a configured prohibition

### 17.11 HARD_BLOCK Boundary

`HARD_BLOCK` is a deterministic runtime outcome, not a Skill verdict.

A `HARD_BLOCK` must identify the exact deterministic rule or configured condition that caused it.

The `compliance-reviewer` may surface semantic risk but cannot create, remove or override `HARD_BLOCK`.

A low compliance-risk judgement cannot override an active deterministic `HARD_BLOCK`.

Removing a `HARD_BLOCK` requires the underlying blocking condition to be resolved through an allowed runtime path.

### 17.12 Policy Ownership Boundary

- Policy content belongs in config or an explicitly approved external policy source, not in the Skill.
- `policy_checks.py` interprets deterministic policy rules but does not author them.
- The config adapter loads policy-bearing config; it does not decide compliance outcomes.
- The compliance Skill handles judgement where deterministic evaluation is insufficient.
- Orchestration coordinates the result but cannot override a deterministic block.

### 17.13 Diversity Service — `diversity.py`

`diversity.py` owns deterministic diversity measurement and selection constraint evaluation over supplied eligible candidates.

Accepted inputs may include:

- validated Hypothesis and Concept candidates
- strategic dimension values carried by each candidate
- creative-taxonomy config snapshot
- diversity-targets config snapshot
- experiment-variables config snapshot where applicable

The service may:

- measure candidate distribution across configured strategic dimensions
- detect configured overlap or insufficient diversity
- evaluate whether a candidate set satisfies diversity targets
- rank or select from already eligible candidates according to deterministic selection rules
- return machine-readable diversity deficiencies

The service must not:

- generate new Hypotheses or Concepts
- rewrite candidate strategy to manufacture diversity
- use model judgement as a hidden tie-breaker unless an upstream contract explicitly supplies a resolved value
- silently weaken diversity targets to make a candidate pool pass

### 17.14 Experiment Lock Service — `experiment_lock.py`

`experiment_lock.py` owns deterministic verification that approved experiment variables remain unchanged where the frozen experiment contract requires them to remain locked.

Accepted inputs may include:

- Human Gate 2 approved experiment-plan bindings
- approved Hypothesis and Concept bindings
- declared locked experiment variables
- downstream Creative or production-package candidate
- applicable experiment-variables config snapshot

The service may:

- compare approved and downstream experiment-variable values
- detect unauthorized variable drift
- identify the exact variable that changed
- return machine-readable lock violations
- block progression when a required lock is violated

The service must not:

- decide which experiment should have been approved
- rewrite downstream Creative content to repair a violation
- silently accept variable drift because the new version appears stronger
- mutate the approved Gate 2 experiment plan

### 17.15 Diversity and Experiment Boundary

- `creative-strategist` proposes strategy; `diversity.py` evaluates deterministic portfolio constraints.
- Diversity selection operates only on supplied eligible candidates.
- Human Gate 2 approves the exact experiment-plan bindings.
- `experiment_lock.py` protects approved experimental intent downstream.
- Script quality does not justify changing a locked experimental variable.
- Production feasibility does not silently authorize experiment drift.
- If an approved experiment must change materially, it returns through an explicit allowed redesign and approval path.

### 17.16 Package Service — `packages.py`

`packages.py` owns deterministic production-package identity and package-level consistency validation.

Accepted inputs may include:

- validated Creative bindings
- approved experiment-plan bindings
- required production intent
- exact voice, asset and reference bindings where applicable
- tool-capability and format-profile references

The service may:

- derive package identity deterministically from permitted bound inputs
- verify package consistency against approved Creative and experiment intent
- detect missing required production references
- verify exact package-level bindings
- return machine-readable package-integrity violations

The service must not:

- generate Creative strategy
- select a provider based on subjective preference
- invoke production tools
- mutate approved upstream intent
- use model-authored package IDs as canonical identity

### 17.17 Feasibility Service — `feasibility.py`

`feasibility.py` owns deterministic evaluation of whether a proposed production route satisfies supplied capability and execution constraints.

Accepted inputs may include:

- production-package requirements
- format-profile config snapshot
- tool-capability config snapshot
- candidate provider/tool capability observations
- required duration, resolution, aspect ratio and media-input constraints
- required audio, voice or reference-media constraints

The service may:

- compare requested execution against supported capability
- validate duration and output-format compatibility
- validate required input-media support
- validate audio or voice capability requirements
- detect unsupported combinations
- return eligible and ineligible route results with machine-readable reasons

The service must not:

- invent provider capability not present in supplied observations or config
- generate media
- select a strategically better concept
- silently degrade an approved execution requirement to make a route feasible

### 17.18 Package and Feasibility Boundary

- Package identity is pure-derived from approved and validated inputs.
- Feasibility evaluates supplied candidate routes; it does not create new creative intent.
- Provider capability is observed through adapters and interpreted deterministically here.
- A route that cannot satisfy a required approved constraint is ineligible.
- A cheaper route must not silently weaken required quality, format, experiment or voice constraints.
- Over-budget evaluation is coordinated separately from technical feasibility when budget policy is supplied.

### 17.19 Manifest Service — `manifests.py`

`manifests.py` owns deterministic manifest structure, reference and integrity validation.

Accepted inputs may include:

- canonical or production manifest candidate
- exact artefact and entity bindings
- required asset references
- required version and hash bindings
- applicable manifest contract from the frozen data architecture

The service may:

- validate required manifest fields and structure
- verify referenced IDs and exact versions
- verify required content hashes
- detect missing, stale or inconsistent references
- verify that required package or artefact members are represented
- return machine-readable integrity violations

The service must not:

- invent missing manifest members
- resolve ambiguous references by guessing
- rewrite upstream canonical content
- treat filesystem presence alone as proof of canonical validity

### 17.20 State Transition Service — `transitions.py`

`transitions.py` owns deterministic validation of requested canonical state transitions against the frozen Phase 2 state machines.

Accepted inputs may include:

- canonical entity or artefact type
- exact current canonical state
- requested next state
- required transition context or event
- applicable exact bindings

The service may:

- verify that the requested transition exists in the frozen state machine
- verify required transition prerequisites
- reject illegal state jumps
- distinguish invalid transition from missing prerequisite
- return machine-readable transition violations

The service must not:

- invent new canonical states
- invent new transition edges
- allow orchestration convenience to override the frozen state machine
- infer human approval when a transition requires an approved gate

### 17.21 Manifest and Transition Boundary

- Persistence adapters perform storage operations but do not decide manifest validity.
- Filesystem presence does not make an asset canonically valid.
- Orchestration requests progression; `transitions.py` determines canonical transition validity.
- Active orchestration lifecycle state remains separate from canonical artefact/entity state.
- Human-gate requirements remain exact prerequisites where the frozen transition contract requires them.
- An invalid canonical transition must fail explicitly rather than being silently coerced.

### 17.22 Localization Service — `localization.py`

`localization.py` owns deterministic verification of localization invariants; it does not perform open-ended language localization.

Accepted inputs may include:

- source Creative or script bindings
- localized Creative or script candidate
- declared target locale
- protected canonical references and placeholders
- locked experiment-variable bindings
- applicable deterministic localization constraints supplied by the runtime contract

The service may:

- verify declared locale identifiers and required localization metadata
- verify preservation of protected canonical references
- verify preservation of required placeholders and structural tokens
- detect deterministic loss or mutation of locked experiment variables
- delegate exact claim-boundary validation to `claims.py` where claim text changed
- return machine-readable localization-invariant violations

The service must not:

- translate or rewrite copy
- decide whether language sounds naturally Chilean
- infer cultural appropriateness through open-ended judgement
- invent locale-specific policy
- silently alter protected bindings to make localized content pass

### 17.23 Localization Ownership Boundary

- `script-engine` owns natural Chilean-language adaptation and final script wording.
- `localization.py` verifies only mechanically enforceable localization invariants.
- Semantic claim drift remains owned by `claims.py`.
- Semantic compliance risk remains owned by `compliance-reviewer`.
- Localization must not alter locked experiment intent.
- Deterministic localization checks do not replace human or model judgement about natural language quality.

## 18. Schema Ownership

Schemas define runtime data shape, structural constraints and representation boundaries.

Schemas do not own workflow sequencing, open-ended reasoning, persistence mechanics or deterministic domain-policy decisions.

### 18.1 Common Schema Rules

Schemas may own:

- field names and types
- required and optional field structure
- enums and structurally constrained values defined by frozen contracts
- serialization and deserialization shape
- structural reference shape
- structural version and hash fields
- provider-neutral runtime result representation
- machine-readable validation error structure

Schemas must not own:

- workflow sequencing
- retry decisions
- human-gate decisions
- Skill invocation
- model invocation
- network access
- persistence writes
- provider SDK behavior
- evidence eligibility decisions
- claim-freedom computation
- diversity selection
- policy `HARD_BLOCK` decisions
- production-route feasibility decisions
- canonical state-transition decisions

### 18.2 Schema Module Ownership

- `canonical.py` defines canonical artefact and entity record shapes required by the frozen data architecture.
- `commands.py` defines runtime command request, response and command-envelope shapes.
- `projections.py` defines the shapes of minimal runtime and model input projections; it does not construct or select their content.
- `model_results.py` defines provider-neutral structured model-result shapes expected after transport decoding.
- `validation.py` owns reusable structural schema-validation primitives and normalized structural validation errors only.
- `events.py` defines payload shapes for the frozen Phase 2 domain-event types.

### 18.3 Schema Boundary

- Deterministic services consume validated schema instances and enforce domain rules.
- Orchestration consumes schemas but owns progression and failure mapping.
- Persistence adapters serialize and store schema-shaped data but do not own canonical schema definitions.
- Provider adapters translate provider-specific transport into provider-neutral runtime structures.
- Skills and prompts do not define competing canonical schemas.
- Schema validation success does not imply deterministic domain validation success.

### 18.4 Canonical Schema Ownership — `canonical.py`

`canonical.py` represents the canonical artefact and entity record shapes frozen by Phase 2 without redefining their domain taxonomy.

Canonical schema representation must preserve:

- canonical ID field shape
- immutable version identity
- exact content-hash representation where required
- exact upstream reference and binding shape
- canonical state field shape where defined by the frozen data architecture
- provenance and required metadata structure
- immutable record semantics at the representation boundary

`canonical.py` must not:

- allocate canonical IDs
- derive package IDs
- decide whether evidence is eligible
- determine whether a state transition is legal
- mutate a prior canonical version
- infer missing canonical fields from model output
- redefine the eight canonical artefact types or twenty first-class entity types frozen in Phase 2

A changed canonical record is represented as a new immutable version rather than an in-place mutation.

### 18.5 Domain Event Schema Ownership — `events.py`

`events.py` represents the payload shapes of the sixteen domain event types frozen in Phase 2.

Domain-event schema representation must preserve:

- exact event-type identity
- referenced canonical IDs and exact versions where required
- event payload structure
- relevant run or causal bindings
- machine-readable event metadata required by the frozen contract
- append-only event semantics

`events.py` must not:

- create new domain event types
- mutate previously recorded events
- apply canonical state transitions
- infer human approval
- reconstruct missing event history by guessing
- treat an event payload as authority to bypass deterministic validation

### 18.6 Canonical and Event Relationship

- Canonical records are immutable versioned truth; domain events are append-only historical facts.
- Schemas represent both structures but do not execute persistence.
- A domain event may reference canonical versions but does not mutate them directly.
- Canonical state changes require the deterministic transition contract before persistence.
- Human-gate events must preserve the exact approved version and hash bindings required by the frozen data architecture.
- SQLite projections may derive views from canonical records and events but remain non-authoritative.
- Rebuilding SQLite must not change canonical JSON/YAML truth or append-only event history.

### 18.7 Runtime Command Schema Ownership — `commands.py`

`commands.py` represents provider-neutral runtime command request, response and envelope shapes without implementing command behavior.

Command schema representation may include:

- command name
- run identity reference
- exact input bindings
- applicable config snapshot references
- declared knowledge retrieval references where applicable
- command-specific structured input fields
- normalized runtime result shape
- blocking, failure or completion result metadata

`commands.py` must not:

- sequence command stages
- invoke Skills or models
- allocate run or canonical IDs
- load config or knowledge
- decide retry eligibility
- decide human-gate progression
- persist command results
- redefine the eight V1 runtime command contracts frozen in Section 15

### 18.8 Projection Schema Ownership — `projections.py`

`projections.py` defines structural shapes for minimal runtime and model input projections.

A projection may represent:

- selected canonical fields required by a stage
- exact source artefact and version bindings
- required provenance references
- selected deterministic validation results
- explicitly permitted config-derived constraints
- explicitly permitted knowledge references
- protected experiment or claim bindings where required

`projections.py` must not:

- decide which canonical fields a stage needs
- retrieve source records
- perform knowledge retrieval
- load config
- summarize missing information through model judgement
- add fields merely because they are available upstream
- remove required provenance or binding information

### 18.9 Command and Projection Boundary

- Section 15 owns runtime command semantics; `commands.py` represents their structural request and result shapes.
- Orchestration owns command execution and stage sequencing.
- Invocation assembly owns selection of the minimum permitted input projection for each model call.
- `projections.py` provides the validated shape into which selected projection data is placed.
- A projection is derived runtime input, not a new canonical artefact.
- Projection construction must preserve exact source bindings so outputs remain traceable to canonical inputs.
- Full canonical records are not injected into a model call merely because they are available.
- Missing required projected data blocks or fails through the applicable runtime contract rather than being invented.

### 18.10 Model Result Schema Ownership — `model_results.py`

`model_results.py` defines provider-neutral structured result shapes for model outputs after provider transport decoding and before downstream deterministic domain acceptance.

Model-result schema representation may include:

- invocation identity reference
- declared output type
- structured model payload
- uncertainty or unresolved-item fields required by the invocation contract
- exact upstream binding echoes where required
- normalized transport metadata needed by runtime validation
- structural validation status representation

`model_results.py` must not:

- call model providers
- repair model output
- decide retry eligibility
- infer missing domain values
- decide evidence sufficiency
- decide policy outcome
- convert structurally valid output directly into canonical truth

### 18.11 Structural Validation Ownership — `validation.py`

`validation.py` owns reusable structural schema-validation primitives and normalized structural validation-error representation.

Structural validation may detect:

- missing required fields
- invalid field types
- invalid enum or constrained structural values
- malformed structural references
- malformed version or hash field representation
- structurally invalid nested payloads
- unexpected fields where the bound schema forbids them

Structural validation errors must be machine-readable and identify the affected field or path where possible.

`validation.py` must not:

- evaluate evidence eligibility
- compute claim freedom
- decide diversity adequacy
- issue policy `HARD_BLOCK`
- decide production feasibility
- decide canonical transition legality
- decide retry or orchestration state

### 18.12 Model Result and Validation Boundary

- Provider adapters decode provider-specific transport before provider-neutral model-result validation.
- A provider-success response can still fail structural validation.
- Structural validation precedes deterministic domain validation.
- Structural validity does not make model output authoritative.
- Model-result repair is governed by the Model Invocation Contract, not by schemas.
- Canonical persistence occurs only after all applicable downstream validation and orchestration requirements succeed.

## 19. Persistence Adapter Boundary

Persistence adapters implement storage and retrieval mechanics for validated runtime and canonical data without owning domain validity, workflow progression or policy decisions.

### 19.1 Common Persistence Adapter Contract

Every persistence adapter declares:

- storage purpose
- accepted schema-shaped inputs
- storage location or backend class
- read contract
- write contract
- immutability or append-only requirements where applicable
- conflict and failure behavior
- exact binding preservation requirements
- rebuild or recovery expectations where applicable
- machine-readable persistence errors

### 19.2 Persistence Rules

- Persistence adapters do not call Skills or language models.
- Persistence adapters do not decide evidence eligibility.
- Persistence adapters do not decide claim freedom.
- Persistence adapters do not issue policy `HARD_BLOCK`.
- Persistence adapters do not decide human-gate approval.
- Persistence adapters do not decide canonical transition legality.
- Persistence adapters preserve exact IDs, versions, hashes and upstream bindings supplied by validated runtime inputs.
- Persistence failure does not authorize mutation of domain meaning.
- Missing persisted data must not be reconstructed by guessing.

### 19.3 Canonical Storage Authority

- Canonical JSON/YAML records remain authoritative immutable versioned truth.
- Append-only domain events remain authoritative historical facts.
- SQLite remains a rebuildable non-authoritative projection.
- Filesystem media and operational files remain referenced assets, not canonical authority by filesystem presence alone.
- Persistence adapters must not promote a projection or cached representation into canonical truth.

### 19.4 Persistence and Orchestration Boundary

- Orchestration decides when a validated runtime step is eligible to persist.
- Deterministic services decide domain validity before persistence where required.
- Schemas define persisted shape but do not execute storage.
- Persistence adapters return success, conflict or failure results to orchestration.
- A successful write does not imply that a human gate or later workflow stage is approved.
- Persistence retries follow orchestration retry policy and must preserve write semantics.

### 19.5 Canonical Record Persistence

Canonical record persistence owns filesystem storage and retrieval mechanics for immutable versioned canonical JSON/YAML records.

Canonical persistence may:

- write a new validated canonical version to its deterministic storage location
- retrieve an exact canonical ID and version
- retrieve exact stored content for hash verification
- detect an existing-version collision
- report missing, conflicting or unreadable canonical records

Canonical persistence must:

- preserve the supplied canonical ID exactly
- preserve the supplied immutable version exactly
- preserve exact upstream bindings
- preserve the validated serialized canonical content
- reject overwrite of an existing immutable canonical version
- fail explicitly when a requested exact version cannot be resolved

Canonical persistence must not:

- mutate an existing canonical version in place
- silently substitute the latest version for an exact requested version
- allocate canonical IDs
- decide whether a new version is domain-valid
- reinterpret canonical content while writing or reading it

### 19.6 Append-Only Domain Event Persistence

Domain-event persistence owns append and retrieval mechanics for the frozen Phase 2 domain-event history.

Event persistence may:

- append a validated domain event
- retrieve persisted events according to supported deterministic lookup keys
- preserve causal, run and canonical bindings supplied in the event payload
- report append, retrieval or storage-integrity failures

Event persistence must:

- preserve append-only history
- preserve exact event identity and event payload
- preserve referenced canonical IDs and versions
- reject mutation or replacement of an already persisted event
- fail explicitly rather than reconstruct missing event history

Event persistence must not:

- invent new event types
- infer an event that was never persisted
- reorder historical meaning to make a workflow appear valid
- infer human approval from surrounding events
- apply canonical state transitions itself

### 19.7 Canonical Record and Event Relationship

- A canonical write and an event append remain distinct persistence operations with distinct contracts.
- Canonical records describe immutable versioned truth.
- Domain events describe append-only historical facts.
- An event may reference an exact canonical version but does not mutate that version.
- Persistence success must preserve the exact validated bindings supplied by runtime.
- Partial persistence failure must be surfaced to orchestration rather than hidden through compensating domain invention.
- Recovery must preserve canonical immutability and event append-only semantics.

### 19.8 SQLite Projection Persistence

SQLite persistence owns storage, query and rebuild mechanics for the twenty-two rebuildable projections frozen in Phase 2.

SQLite projection persistence may:

- materialize projection rows from validated canonical records and domain events
- update rebuildable projection state when authoritative source data changes through valid runtime progression
- query supported projection views and indexes
- detect missing or stale projection data where deterministically possible
- clear and rebuild projections from authoritative sources
- report query, write, integrity or rebuild failures

SQLite projection persistence must:

- preserve source canonical IDs, versions and bindings required by each projection
- preserve enough source identity to trace a projection row back to authoritative records or events
- treat projection contents as disposable and rebuildable
- support deterministic rebuild from authoritative canonical records and domain events
- fail explicitly when projection integrity cannot be established

SQLite projection persistence must not:

- become canonical authority
- overwrite canonical JSON/YAML truth
- rewrite append-only event history
- allocate canonical identity
- infer missing authoritative data from projection rows
- treat projection-only data as proof that a canonical record exists
- make domain-policy, human-gate or canonical-transition decisions

### 19.9 Projection Rebuild Contract

A projection rebuild starts from authoritative canonical records and append-only domain events, never from an older SQLite database as its source of truth.

Rebuild behavior must:

- preserve canonical and event source data unchanged
- recreate projection state deterministically from supported authoritative inputs
- make projection schema or rebuild failures explicit
- avoid introducing new canonical facts during reconstruction
- allow the prior SQLite projection store to be discarded when a clean rebuild is required

Successful rebuild means the projection is usable; it does not change or re-approve canonical truth.

### 19.10 SQLite Authority Boundary

- SQLite is optimized for runtime lookup and analysis, not canonical authorship.
- A projection row is a derived representation of authoritative source data.
- If SQLite disagrees with authoritative canonical or event data, the projection is stale or invalid.
- Runtime must resolve authoritative facts from canonical records or events when exact truth is required.
- Projection repair occurs by correcting the projection or rebuilding it, not by mutating authoritative history to match SQLite.
- Deleting and rebuilding SQLite must not change canonical IDs, versions, hashes, approvals or event history.

### 19.11 Media and Operational Filesystem Persistence

Media and operational filesystem persistence owns storage and retrieval mechanics for non-canonical binary and operational files such as images, audio, video, production outputs and temporary runtime artefacts.

Filesystem persistence may:

- write supplied binary or operational files to deterministic or runtime-assigned storage locations
- retrieve exact stored files or file metadata when requested
- report file presence, size, path and storage failures
- preserve externally supplied content hashes where required
- support temporary and durable operational storage classes where explicitly defined

Filesystem persistence must:

- preserve the exact file bytes supplied for a completed write
- preserve required package, asset or manifest references supplied by validated runtime inputs
- report missing or unreadable files explicitly
- distinguish temporary operational files from durable referenced assets where the runtime contract requires it
- preserve exact storage references returned to runtime

Filesystem persistence must not:

- treat file existence as canonical validity
- infer human approval from file presence
- infer production success from a provider output file alone
- decide whether a voice, image, video or asset is authorized for use
- assign canonical meaning to an unbound file
- silently replace a bound asset with another file at the same logical reference

### 19.12 Media Reference Integrity

A media reference becomes meaningful to the runtime only through an explicit validated binding or manifest relationship.

Media-reference integrity may require:

- stable storage reference
- content hash where required
- asset or package binding
- provenance or source metadata where required
- authorization metadata where applicable
- exact version or revision information where the frozen contract requires it

Changing the bytes of a bound durable asset requires a new content identity or version relationship rather than silent replacement.

### 19.13 Filesystem Authority Boundary

- Filesystem storage proves that bytes are present, not that domain requirements passed.
- Manifest validation determines whether required referenced assets are complete and consistent.
- Feasibility validation determines whether an asset is usable for a proposed production route.
- Authorization or usage eligibility must come from validated runtime data, config or approved bindings, not from the filename.
- Human Gate 3 approval binds the exact production package and required references presented for release.
- Temporary provider outputs remain non-canonical until the applicable runtime path validates and persists their required relationships.
- Deleting an unreferenced temporary file does not alter canonical truth or append-only event history.

## 20. Config Loading Boundary

Config adapters load, parse and structurally validate policy-bearing runtime configuration without owning the domain decisions that consume it.

### 20.1 Frozen Config Registries

Phase 5 consumes exactly the nine config registries frozen in Phase 2:

- `evidence_policy`
- `deny_list`
- `narrative_library`
- `format_profiles`
- `category_profiles`
- `creative_taxonomy`
- `experiment_variables`
- `diversity_targets`
- `tool_capability`

Phase 5 must not create an additional policy-bearing registry without an explicit architecture change.

### 20.2 Common Config Adapter Contract

Every config adapter operation declares:

- requested registry identity
- requested exact config version or snapshot reference where required
- source location
- parse contract
- structural validation contract
- normalized provider-neutral config result
- failure behavior
- exact snapshot binding information

### 20.3 Config Adapter Rules

- Config adapters load and parse config; they do not make downstream domain decisions.
- Config adapters do not call Skills or language models.
- Config adapters do not invent missing policy values.
- Config adapters do not silently substitute an unrelated registry.
- Required invalid config blocks use of that config.
- Required missing config blocks execution rather than causing a hidden default.
- Loaded config must preserve the exact snapshot or version identity used by runtime.
- Policy-bearing defaults must be explicit in validated config or frozen contracts.
- Environment-specific transport or file-location details must not change config semantics.

### 20.4 Config Consumption Boundary

- Deterministic services consume validated config values but do not mutate them.
- Skills receive only explicitly permitted config-derived constraints through runtime projection or invocation assembly.
- Orchestration coordinates which required config snapshots apply to a command and stage.
- Persistence may store config references but does not reinterpret config meaning.
- A config snapshot used for validation remains traceable through downstream bindings where required.

### 20.5 Config Resolution

Config resolution converts an allowed config request into an exact validated snapshot binding before that config is consumed by runtime logic.

Resolution may start from:

- an explicitly requested exact config version
- an explicitly requested snapshot reference
- an allowed floating selector such as the currently active version when the runtime contract permits resolution by selector

After resolution, runtime consumption uses the resulting exact snapshot binding rather than continuing to follow a floating selector.

Config resolution must:

- resolve the requested registry unambiguously
- validate that the resolved content belongs to the requested registry
- structurally validate the resolved config before use
- establish exact version or snapshot identity
- establish content hash where the config contract requires one
- return the exact binding used by downstream runtime logic

Config resolution must not:

- silently switch to a newer version after an exact snapshot has been bound
- substitute another registry because the requested one is unavailable
- reinterpret invalid config into a usable form through model judgement
- invent a snapshot identity for unversioned unknown content

### 20.6 Config Snapshot Stability

An exact config snapshot bound to a run, command or stage remains stable for the scope declared by that runtime contract.

Publishing a newer config version does not retroactively alter already bound runtime inputs, validations, outputs or human-gate bindings.

The runtime must preserve enough config identity to reproduce which policy-bearing values were applied.

A downstream result that depends on config must remain traceable to the exact relevant config snapshot where the frozen architecture requires that dependency to be preserved.

### 20.7 Explicit Config Rebinding

Changing an already bound config snapshot is an explicit runtime action, never an implicit side effect of loading the newest config.

An explicit rebind must:

- identify the old exact snapshot binding
- identify the new exact snapshot binding
- identify which runtime validations or outputs depend on the changed config
- return affected downstream work through the applicable validation or orchestration path
- preserve prior historical bindings rather than rewriting them

An explicit config rebind must not:

- rewrite a prior human approval to appear as though it used the new config
- silently preserve downstream eligibility when required validation depended on the old config
- mutate historical canonical records or domain events
- bypass renewed validation or approval when the applicable frozen contract requires it

### 20.8 Config Snapshot and Human-Gate Boundary

- Human-gate approval applies to the exact artefact, version, hash and relevant config bindings presented at that gate where required by the frozen contract.
- A newer config version does not automatically invalidate historical approval.
- Reusing historical approval for changed inputs or required config bindings is forbidden.
- Orchestration determines whether a config change requires revalidation, renewed approval, redesign or a new runtime path according to the frozen dependencies.
- Config adapters expose exact snapshots; they do not decide whether approval must be renewed.

## 21. Knowledge Retrieval Boundary

Knowledge adapters retrieve approved runtime knowledge with provenance and eligibility controls without owning strategic reasoning, Skill procedure or workflow progression.

### 21.1 Common Knowledge Retrieval Contract

Every knowledge retrieval operation declares:

- requested knowledge class or allowed knowledge identity set
- command and stage context
- permitted Skill or reasoning role where relevant
- retrieval query or deterministic lookup criteria
- provenance requirements
- eligibility requirements
- exclusion rules
- normalized retrieval result shape
- exact retrieved knowledge references
- failure behavior

### 21.2 Knowledge Retrieval Rules

- Knowledge adapters retrieve source material; they do not perform strategic synthesis.
- Knowledge adapters do not call Skills or language models to decide source eligibility.
- Knowledge adapters do not mutate knowledge source content.
- Knowledge adapters do not invent missing knowledge.
- Retrieval must preserve source identity and provenance required by the frozen knowledge contract.
- Retrieval must preserve enough identity for downstream outputs to remain traceable to the knowledge actually used.
- Only knowledge explicitly eligible for the requesting runtime context may be returned.
- Runtime retrieval must exclude quarantined material.
- Runtime retrieval must exclude `KNW-schwartz-integration`.
- Retrieval failure is surfaced to orchestration rather than replaced by unsupported model knowledge.

### 21.3 Knowledge Result Shape

A normalized knowledge retrieval result may include:

- knowledge ID
- knowledge version or immutable source reference where applicable
- provenance metadata
- knowledge tier or eligibility metadata
- retrieved source fragment or approved representation
- retrieval reason or match metadata
- exact source binding required for traceability

Knowledge retrieval results are runtime inputs, not new canonical strategic conclusions.

### 21.4 Knowledge Consumption Boundary

- Invocation assembly injects only the retrieved knowledge permitted for that model call.
- Skills retain their frozen procedural ownership and do not absorb retrieved knowledge into their definitions.
- Prompts frame the task but do not embed full knowledge-source bodies.
- Deterministic services do not reinterpret retrieved knowledge through open-ended judgement.
- Persistence may preserve knowledge references but does not decide knowledge eligibility.
- Orchestration coordinates retrieval requirements and failure handling but does not perform knowledge synthesis.

### 21.5 Skill Knowledge Eligibility

Runtime knowledge retrieval must respect both the requesting command/stage contract and the frozen knowledge eligibility of the Skill being invoked.

A knowledge source is eligible for direct Skill consumption only when that direct relationship is explicitly permitted by the frozen Skill contract.

Knowledge availability elsewhere in the repository does not create implicit Skill eligibility.

### 21.6 Frozen Direct Skill Knowledge Routing

The frozen Phase 4 direct Skill knowledge bindings are:

- `product-intelligence` → no direct knowledge binding
- `market-intelligence-cl` → `KNW-schwartz-persuasion`
- `creative-strategist` → `KNW-schwartz-persuasion`
- `script-engine` → `KNW-schwartz-persuasion`, `KNW-schwartz-language`
- `compliance-reviewer` → `KNW-schwartz-persuasion`

Phase 5 runtime must not silently broaden these direct Skill knowledge bindings.

### 21.7 Supplemental Runtime Knowledge

Supplemental runtime knowledge may be retrieved only when the command and stage contract explicitly permits the relevant knowledge class or identity.

Supplemental runtime retrieval:

- remains separate from the frozen Skill definition
- preserves exact provenance and knowledge identity
- must be relevant to the declared command and stage purpose
- must satisfy the applicable knowledge eligibility rules
- must not create a new implicit direct Skill binding
- must not override the frozen procedural ownership of a Skill
- must exclude quarantined material
- must exclude `KNW-schwartz-integration`

Methodology knowledge may therefore support an eligible runtime stage only through an explicit runtime retrieval contract, not merely because the source exists.

### 21.8 Language Knowledge Restriction

`KNW-schwartz-language` has exactly one direct Skill consumer: `script-engine`.

The runtime must reject direct injection of `KNW-schwartz-language` into:

- `product-intelligence`
- `market-intelligence-cl`
- `creative-strategist`
- `compliance-reviewer`

This restriction preserves the frozen separation between language execution and upstream truth, market, strategy and compliance reasoning.

### 21.9 Knowledge Routing Failure

Knowledge routing fails explicitly when:

- the requested source is excluded from runtime retrieval
- the requested direct Skill binding is not permitted
- required provenance cannot be established
- the command or stage does not permit the requested knowledge class
- an exact required knowledge reference cannot be resolved

Routing failure is surfaced to orchestration and must not be repaired by silently substituting general model knowledge.

### 21.10 Knowledge Provenance Binding

Knowledge consumed by a runtime stage must preserve enough provenance to identify the exact source material actually supplied to downstream reasoning.

A knowledge provenance binding may include:

- knowledge ID
- exact knowledge version or immutable source reference where applicable
- source provenance metadata
- retrieved fragment locator or equivalent source position where available
- retrieved fragment content hash where required by the knowledge contract
- retrieval command and stage context
- retrieval query or deterministic lookup criteria where required for auditability

The binding records what was actually retrieved; it must not imply that unretrieved portions of the source were supplied to the model.

### 21.11 Retrieval Result Stability

Once a knowledge result is selected for a runtime invocation, downstream traceability uses the exact retrieved knowledge references rather than a later floating retrieval result.

Publishing, replacing or adding eligible knowledge later does not retroactively alter the knowledge bindings of an already executed invocation.

Re-running retrieval may produce a different eligible result set, but that new result set is a new runtime input and must receive its own exact bindings.

Runtime must not silently replace an unavailable historical knowledge reference with a newer source and present the result as equivalent.

### 21.12 Fragment and Source Integrity

Retrieved fragments remain subordinate to their exact source provenance.

Knowledge retrieval must not:

- detach a fragment from its source identity
- merge fragments from different sources into one fabricated provenance record
- attribute model-generated synthesis to a knowledge source
- broaden a fragment claim beyond what the retrieved source material contains
- treat retrieval ranking as proof of source truth or strategic correctness

When multiple sources are returned, each source retains its own provenance and binding.

### 21.13 Knowledge Update Boundary

A knowledge-source update creates a new usable source version or immutable reference relationship where the knowledge storage contract supports versioning; it does not rewrite historical runtime bindings.

If required knowledge changes materially during an active workflow:

- the new source must be retrieved through an allowed runtime path
- the new exact knowledge binding must be recorded
- dependent model reasoning must be rerun where required
- downstream validation or approval must be revisited when the frozen dependency contract requires it
- historical invocations retain their original knowledge bindings

Knowledge adapters expose retrieval results and provenance; orchestration determines what dependent work must be rerun.

## 22. External Tool Adapter Boundary

External tool adapters translate validated provider-neutral runtime operations into provider-specific API or tool calls and normalize their results without owning creative strategy, workflow policy or production approval.

### 22.1 Common External Tool Adapter Contract

Every external tool operation declares:

- provider or tool identity
- requested operation identity
- exact validated input bindings
- required capability assumptions or references
- provider-specific request translation
- execution authorization supplied by runtime where required
- normalized provider-neutral result shape
- externally returned artefact or job references where applicable
- cost or usage metadata when exposed by the provider
- machine-readable provider error result

### 22.2 External Tool Adapter Rules

- Tool adapters may perform network or provider API access required by their operation.
- Tool adapters do not perform creative strategy or concept selection.
- Tool adapters do not invoke Skills to reinterpret an execution request.
- Tool adapters do not decide human-gate approval.
- Tool adapters do not decide claim freedom or compliance outcome.
- Tool adapters do not issue policy `HARD_BLOCK`.
- Tool adapters do not silently weaken supplied production requirements.
- Tool adapters do not invent provider capability that was not observed or configured.
- Tool adapters preserve exact upstream package, asset, voice and execution bindings supplied by runtime.
- Provider-specific behavior must be normalized before downstream runtime consumption.

### 22.3 Execution Authorization Boundary

An adapter receives permission to execute from orchestration; it does not infer permission from the presence of valid inputs.

Paid or externally consequential production execution must not begin merely because a technically feasible route exists.

Where Human Gate 3 is required, the adapter may execute the released production operation only after orchestration supplies the applicable approved release binding.

The adapter must not fabricate, infer or substitute a missing release approval.

Authorization to use a voice, image, video, identity or other restricted asset must be represented in validated runtime inputs where required; the adapter does not infer authorization from file presence or provider availability.

### 22.4 Provider-Neutral Result Boundary

Provider responses must be translated into runtime-neutral results before orchestration or deterministic services consume them.

A normalized external-tool result may include:

- provider job or request reference
- execution status
- produced asset references
- observed output metadata
- actual or estimated cost metadata when available
- provider warnings
- normalized failure class and provider diagnostic reference

Provider success does not imply production-package validity, human approval or canonical persistence.

Provider output remains subject to the applicable manifest, binding, validation and persistence contracts.

### 22.5 Capability Discovery

External tool adapters may discover or retrieve provider capability observations required to evaluate candidate production routes.

Capability observations may include:

- supported operation types
- supported duration ranges
- supported aspect ratios
- supported resolutions or quality modes
- supported image, video, audio or reference inputs
- supported voice or audio execution modes
- provider model or route identity
- relevant provider limits or constraints
- observation timestamp or freshness metadata where available

Capability discovery must:

- preserve the provider identity and observed route or model identity
- distinguish observed provider capability from configured runtime policy
- surface unavailable or ambiguous capability information explicitly
- normalize provider-specific capability data before deterministic feasibility evaluation

Capability discovery must not:

- declare a route feasible by itself
- invent unsupported capability
- silently assume an unknown capability is supported
- turn a provider recommendation into creative strategy
- alter approved production requirements to match available capability

### 22.6 Cost Preflight

Where a provider exposes pricing or estimation capability, the external tool adapter may request a cost or usage estimate before consequential execution.

A normalized cost preflight result may include:

- provider and route identity
- exact execution parameters used for estimation
- estimated provider credits or usage units
- estimated monetary cost when exposed or deterministically convertible from an approved rate source
- estimate timestamp or freshness metadata
- provider pricing reference or diagnostic metadata where available
- uncertainty or unavailable-estimate status

Cost preflight must:

- occur before paid execution when the runtime contract requires an estimate and the provider supports estimation
- preserve the exact parameters on which the estimate was based
- distinguish estimate from final billed usage
- surface estimate failure or unavailability explicitly
- avoid treating stale pricing observations as guaranteed current cost

Cost preflight must not:

- hardcode provider prices into deterministic service logic
- invent an estimate when the provider or approved pricing source cannot supply one
- authorize spending
- silently reduce quality, duration, voice or other approved requirements to lower cost

### 22.7 Capability, Feasibility and Budget Boundary

- Tool adapters observe provider capability; `feasibility.py` determines technical eligibility against supplied requirements.
- Tool adapters expose cost observations or estimates; they do not decide whether the spend is acceptable.
- Budget limits and cost policy must come from explicit validated runtime inputs, config or another approved policy source rather than hidden source-code constants.
- A technically feasible route may still be blocked by budget or release policy.
- A cheaper route is eligible only if it still satisfies all required approved execution constraints.
- Provider capability or pricing changes do not retroactively alter historical production-route bindings.
- Final billed usage may differ from preflight estimates and must be recorded as observed execution metadata when available.

### 22.8 External Execution Request

A consequential provider execution request is assembled only from validated production inputs and an applicable orchestration release decision.

An execution request preserves:

- provider and route identity
- exact production-package binding
- exact asset and voice bindings where applicable
- exact execution parameters
- applicable release authorization binding
- runtime attempt identity or request correlation reference

The adapter must transmit provider-specific parameters without silently changing approved runtime meaning.

### 22.9 Provider Job Lifecycle

Where a provider exposes asynchronous jobs, the adapter owns provider-specific submission, status retrieval and result-fetch mechanics.

Normalized operational job status may distinguish:

- submitted
- running
- succeeded
- failed
- cancelled where supported
- unknown or unresolved provider state

These are operational provider statuses and do not redefine Phase 2 canonical state machines or the orchestration states defined in Section 14.

Provider job tracking must preserve the provider job reference and originating runtime attempt binding.

### 22.10 Ambiguous Execution and Retry Safety

A transport failure after request submission may leave execution acceptance ambiguous.

When provider acceptance may have occurred, runtime must not blindly repeat a consequential or paid operation.

Where supported, the adapter should reconcile the existing provider request or job before orchestration authorizes another execution attempt.

Retry handling must:

- preserve execution-attempt lineage
- preserve known provider job or request references
- distinguish confirmed rejection from unknown acceptance state
- surface unresolved execution state explicitly
- avoid duplicate paid execution when provider reconciliation can establish the original job state

The adapter does not independently authorize a replacement paid attempt.

### 22.11 Provider Output Boundary

A successful provider job produces an external-tool result, not automatically an approved or canonical production artefact.

Provider output handling must preserve:

- exact originating production-package binding
- provider job reference
- produced file or asset references
- observed output metadata
- provider warnings or diagnostics where available
- actual billed usage or cost metadata when exposed

Produced media remains subject to required binding, manifest, validation, persistence and downstream release contracts.

A provider-reported success must not fabricate missing runtime bindings or erase prior execution failures.

## 23. Error Taxonomy

Runtime errors use a normalized provider-neutral taxonomy so orchestration can reason about failures without depending on component-specific exception formats.

### 23.1 Frozen Runtime Failure Classes

Phase 5 uses exactly the thirteen runtime failure classes established by the Runtime Boundary Contract:

- `invalid_input`
- `missing_required_evidence`
- `schema_invalid_model_output`
- `deterministic_validation_failure`
- `policy_or_config_block`
- `unresolved_evidence_conflict`
- `retrieval_failure`
- `model_invocation_failure`
- `tool_invocation_failure`
- `persistence_failure`
- `human_gate_pending`
- `unsupported_capability`
- `internal_invariant_violation`

Phase 5 implementation must not create ad hoc top-level failure classes outside this taxonomy without an explicit architecture change.

### 23.2 Normalized Runtime Error Shape

A normalized runtime error may include:

- failure class
- machine-readable error code
- human-readable diagnostic message
- source component or boundary
- command and stage context
- exact affected runtime or canonical bindings where applicable
- normalized cause metadata
- external provider diagnostic reference where applicable
- prior attempt or failure lineage where applicable
- redaction-safe structured diagnostic details

The normalized error must preserve enough information for deterministic handling and auditability without requiring orchestration to parse provider-specific exception text.

### 23.3 Error Ownership Rules

- Components classify failures into the normalized taxonomy at their defined boundary.
- Provider adapters normalize provider-specific failures before returning them to runtime.
- Deterministic services return machine-readable domain violations rather than throwing strategic interpretations.
- Schema validation returns structural validation errors without deciding domain validity.
- Persistence adapters report storage failures without inventing recovery state.
- Knowledge and config adapters report retrieval or loading failures without silently substituting data.
- Error normalization does not authorize retry, blocking, approval or workflow progression.
- Orchestration owns mapping normalized failures to `RETRY_PENDING`, `BLOCKED`, `FAILED`, `WAITING_HUMAN` or other allowed lifecycle handling.
- Error handling must not erase the original failure reason when a later retry occurs.

### 23.4 Error Taxonomy Boundary

- Failure class describes what happened; orchestration state describes what the runtime does next.
- Provider HTTP or SDK status codes are diagnostics, not runtime failure classes by themselves.
- A successful transport operation may still produce a schema or deterministic validation failure.
- A domain block must not be disguised as a transport failure to gain retry eligibility.
- An internal invariant violation must remain explicit and must not be downgraded into a user-correctable input error.
- Human-gate pending is an explicit runtime condition and must not be represented as provider or validation failure.

### 23.5 Boundary Error Normalization

Each runtime boundary converts implementation-specific failures into the frozen normalized runtime taxonomy before returning control to orchestration.

Boundary normalization may map:

- malformed command input to `invalid_input`
- unavailable required substantiation to `missing_required_evidence`
- structurally invalid model output to `schema_invalid_model_output`
- failed deterministic domain rules to `deterministic_validation_failure`
- explicit deterministic policy or required-config prohibition to `policy_or_config_block`
- unresolved conflicting eligible evidence to `unresolved_evidence_conflict`
- knowledge retrieval failure to `retrieval_failure`
- model-provider execution failure to `model_invocation_failure`
- external production-tool execution failure to `tool_invocation_failure`
- canonical, event, projection or filesystem storage failure to `persistence_failure`
- required unresolved human approval to `human_gate_pending`
- unsatisfied required provider capability to `unsupported_capability`
- broken frozen runtime invariant to `internal_invariant_violation`

These mappings classify the failure source; they do not by themselves decide lifecycle handling or retry eligibility.

### 23.6 Cause Preservation

Normalization must preserve the original cause information required for diagnosis, reconciliation and auditability.

Preserved cause information may include:

- originating component
- original exception or provider diagnostic class
- provider status or error code
- provider request or job reference
- affected field or schema path
- violated deterministic rule code
- storage operation and target class
- exact runtime attempt lineage
- safe nested cause reference when one normalized failure was caused by another boundary failure

Cause preservation must not require orchestration to interpret raw provider text in order to determine the top-level runtime failure class.

### 23.7 Error Cause Chain

When one failure originates from another, runtime preserves a causal chain rather than replacing the earlier failure.

For example, a model invocation may fail because its knowledge retrieval dependency failed; the later runtime error may reference the retrieval failure without rewriting it as though the model provider itself failed.

A retry attempt creates new attempt diagnostics while preserving prior failure lineage.

Successful retry resolution does not erase the historical failure that caused the retry.

### 23.8 Diagnostic Safety

Normalized diagnostics must contain enough detail for debugging and auditability while respecting runtime redaction requirements.

Diagnostic handling must not:

- expose secrets or credentials merely because a provider returned them in an error payload
- copy unrestricted raw provider responses into canonical domain content
- mutate failure classification to hide an internal invariant violation
- discard a provider job reference needed to reconcile ambiguous paid execution
- discard exact bindings needed to identify the affected runtime input

Provider-specific diagnostics remain supporting metadata; normalized runtime classification remains provider-neutral.

## 24. Observability and Event Boundary

Runtime observability records execution behavior for diagnosis, traceability, performance analysis and operational audit without becoming canonical domain truth.

### 24.1 Common Runtime Observability Record

A runtime observability record may include:

- record or trace identity
- timestamp
- run identity
- command identity
- stage identity
- source component or boundary
- attempt or correlation identity
- operational event name
- outcome or status
- relevant exact config, knowledge or canonical bindings
- normalized failure reference where applicable
- provider job, usage or cost metadata where applicable

Observability records must preserve enough correlation information to reconstruct the operational path of a run without requiring canonical domain records to contain runtime implementation detail.

### 24.2 Observability Rules

- Observability may record command, stage, invocation, validation, retry, persistence and external-tool execution activity.
- Observability may record timing, usage and cost metadata where available.
- Observability may reference exact canonical, config and knowledge bindings used by runtime.
- Observability must not create canonical IDs or canonical versions.
- Observability must not authorize workflow progression.
- Observability must not infer human approval.
- Observability must not convert provider success into domain success.
- Observability must not become the source of truth for canonical artefacts, approvals or domain state.
- Missing observability data must not be reconstructed by inventing canonical history.

### 24.3 Runtime Observability vs Domain Events

Runtime observability records and Phase 2 domain events are separate classes of information with separate authority.

Runtime observability records describe how the software executed.

Phase 2 domain events describe authoritative append-only domain facts.

An operational trace that records a domain-event append does not replace the persisted domain event itself.

A domain event must not be reconstructed solely from runtime logs when the authoritative event record is missing.

Operational events must not expand or redefine the sixteen domain event types frozen in Phase 2.

### 24.4 Observability Ownership Boundary

- Runtime components may emit provider-neutral observability records about their own execution.
- Orchestration owns run-level correlation and lifecycle context.
- Adapters may expose provider diagnostics, job references, timing and usage metadata for normalization.
- Persistence of observability data, if configured, remains operational storage and not canonical authority.
- Domain-event creation and persistence follow the frozen schema, validation and append-only contracts rather than observability convenience.
- Deterministic services consume domain inputs; they do not derive domain validity from logs or telemetry.

### 24.5 Trace Correlation

Runtime observability must preserve correlation across related operations without requiring components to share provider-specific implementation details.

Correlation may include:

- run identity
- command identity
- stage identity
- invocation or execution-attempt identity
- parent or causal trace reference
- provider request or job reference
- exact relevant canonical, config and knowledge bindings

A retry creates a new attempt identity while preserving correlation to the original run, stage and prior failure lineage.

Provider-specific request identifiers supplement runtime correlation; they do not replace runtime identity.

### 24.6 Observability Redaction and Data Minimization

Observability records must minimize stored content to what is required for operational diagnosis, traceability, usage analysis and auditability.

Observability must not intentionally persist:

- API keys, authentication tokens or credentials
- unrestricted secrets from environment or config sources
- raw provider payloads merely for convenience
- full knowledge-source bodies when exact source references are sufficient
- full canonical artefact contents when exact bindings are sufficient
- unrestricted model prompts or responses when structured metadata and validated bindings are sufficient

Diagnostic content that may contain secrets or restricted data must be redacted or normalized before observability persistence.

Redaction must not remove identifiers required to reconcile ambiguous paid execution, exact affected bindings or normalized failure classification.

### 24.7 Cost and Usage Observability

Runtime observability may record provider usage and cost information when exposed by the applicable model or external-tool boundary.

Cost and usage records must distinguish:

- preflight estimate
- actual observed usage
- actual billed cost where exposed
- unavailable or unknown cost status

Cost observability should preserve:

- provider and route identity
- run, command, stage and attempt correlation
- exact execution parameters relevant to the cost observation
- estimate or observation timestamp where available
- provider usage units such as credits or tokens where applicable
- monetary amount only when supplied or derived from an approved explicit rate source

An estimated cost must not later be represented as actual billed usage merely because execution succeeded.

### 24.8 Observability Authority and Retention Boundary

Observability retention policy is operational policy and must not redefine canonical retention or append-only domain history.

Removing or rotating operational logs must not alter canonical records, human approvals or domain events.

Observability data may support debugging, reconciliation, performance analysis and cost reporting but must not become the sole evidence that a canonical domain action occurred.

If an authoritative record is required by the frozen architecture, an observability record cannot substitute for it.

## 25. Test Architecture

Phase 5 testing verifies deterministic behavior, contract boundaries, orchestration semantics and adapter integration without making paid or nondeterministic provider execution a prerequisite for core correctness.

### 25.1 Common Test Principles

Tests must:

- preserve the frozen Phase 1 through Phase 4 contracts
- verify deterministic logic with reproducible inputs
- distinguish structural validation from domain validation
- verify exact ID, version, hash and binding behavior where applicable
- verify failure classification and orchestration handling separately
- test human-gate behavior without inventing approval
- isolate provider-specific behavior behind adapters
- avoid paid external execution in the default automated suite
- make fixtures explicit and traceable to the contract they test
- fail when implementation silently broadens authority across boundaries

### 25.2 Test Layers

Phase 5 uses these test layers:

- unit tests
- schema tests
- deterministic service tests
- orchestration transition tests
- adapter contract tests
- persistence integration tests
- config and knowledge boundary tests
- model invocation contract tests
- external-tool simulation tests
- end-to-end runtime command tests

### 25.3 Test Authority Boundary

- Tests verify frozen contracts; they do not redefine them.
- Golden fixtures are examples of expected behavior, not new policy sources.
- Mock provider success must not bypass runtime validation.
- Mock human approval must remain explicit test input.
- A passing provider simulation does not prove real provider capability unless separately verified through an allowed integration check.
- Paid live-provider tests, if later added, remain opt-in and separate from the default deterministic suite.
- Test helpers must not hide policy, IDs, approvals or config defaults that production code is forbidden to invent.

### 25.4 Schema Test Ownership

Schema tests verify structural representation only.

Schema tests cover:

- required and optional fields
- field types
- enum and structural constraints
- serialization and deserialization shape
- malformed references, versions and hashes
- provider-neutral model-result structure
- normalized structural validation errors

Schema tests must not assert evidence sufficiency, claim freedom, policy outcome, feasibility or workflow progression.

### 25.5 Deterministic Service Test Ownership

Deterministic service tests verify mechanically enforceable domain behavior from explicit validated inputs and config snapshots.

Service tests cover:

- canonical ID construction and validation
- exact binding verification
- evidence eligibility and coverage computation
- claim-freedom and claim-drift checks
- deterministic policy and `HARD_BLOCK` rules
- diversity constraints and experiment locks
- package integrity and feasibility checks
- manifest validation
- canonical transition legality
- localization invariant preservation

Service tests must be reproducible and must not call Skills, models, networks or persistence backends.

### 25.6 Orchestration Test Ownership

Orchestration tests verify operational lifecycle behavior without reimplementing deterministic domain rules inside the test.

Orchestration tests cover:

- legal progression through runtime stages
- all seven orchestration states
- human-gate waiting and explicit approval transitions
- retry eligibility and bounded retry behavior
- failure-to-state mapping
- completion prerequisites
- preservation of retry and failure lineage
- blocked and resumable paths

Orchestration tests use explicit service and adapter results as inputs; they do not fabricate domain validity implicitly.

### 25.7 Adapter Contract Test Ownership

Adapter contract tests verify translation between provider-neutral runtime contracts and backend-specific mechanics.

Adapter contract tests cover:

- persistence read/write contract behavior
- config loading and exact snapshot binding
- knowledge retrieval eligibility and provenance preservation
- model-provider request and response normalization
- external-tool capability normalization
- cost-preflight normalization
- provider job and ambiguous-execution reconciliation behavior
- provider-specific error normalization

Adapter contract tests must not redefine strategy, policy, approval, feasibility or orchestration authority.

### 25.8 Integration Test Ownership

Integration tests verify collaboration across real Phase 5 boundaries while keeping unrelated external nondeterminism controlled.

Integration tests may cover:

- schema plus deterministic-service validation flow
- deterministic services plus canonical and event persistence
- canonical records plus SQLite projection rebuild
- config loading plus exact snapshot consumption
- knowledge retrieval plus provenance-preserving invocation assembly
- model-result validation plus deterministic downstream validation
- orchestration plus persistence failure handling
- orchestration plus simulated external-tool job reconciliation

Integration tests should use real implementation across the boundaries under test and replace unrelated external providers with controlled fakes or fixtures.

Integration tests must not use provider availability, current pricing or live model behavior as the source of expected domain truth.

### 25.9 End-to-End Runtime Command Tests

End-to-end runtime tests execute complete V1 runtime command paths through provider-neutral runtime interfaces using deterministic or simulated external dependencies by default.

End-to-end tests must cover the eight V1 runtime commands:

- `build_product_truth`
- `research_chile_market`
- `build_strategy_hypotheses`
- `build_concepts`
- `select_experiment_plan`
- `build_creatives`
- `review_creatives`
- `prepare_production`

End-to-end coverage must include:

- successful command completion
- required blocking paths
- required human-gate waiting and approval paths
- recoverable retry paths
- retry exhaustion where applicable
- exact binding propagation
- config and knowledge traceability
- persistence and observability side effects required by the runtime contract

An end-to-end test may stop at prepared and approved production release without invoking paid media generation.

### 25.10 Provider Simulation Boundary

Default automated tests use deterministic provider simulations for model and external-tool boundaries.

A provider simulation may represent:

- successful structured response
- schema-invalid model response
- transient provider failure
- rate-limit or temporary-unavailable condition
- synchronous external-tool result
- asynchronous submitted, running and succeeded job lifecycle
- confirmed provider failure
- ambiguous execution acceptance requiring reconciliation
- capability observation
- cost preflight and actual-usage metadata

Provider simulations must preserve the same provider-neutral contracts consumed by production runtime code.

Tests must not add production-only bypasses merely to make simulated providers easier to use.

Live provider checks, if later implemented, verify adapter compatibility and observed capability only; they do not replace deterministic runtime tests.

### 25.11 Test Fixture Ownership

Test fixtures provide explicit reproducible inputs and expected supporting data for tests without becoming runtime policy or canonical production truth.

Fixtures may represent:

- valid and invalid canonical records
- exact ID, version and hash bindings
- evidence and claim cases
- config snapshots
- knowledge retrieval results with provenance
- human-gate pending and approved inputs
- deterministic service results
- model responses
- provider capability observations
- external-tool jobs and results
- persistence failures and recovery cases
- observability and normalized error records

Fixture data must make important assumptions explicit rather than relying on hidden helper defaults.

### 25.12 Golden Test Boundary

Golden tests may be used where stable structured output or serialization behavior is contractually important.

Appropriate golden-test targets may include:

- canonical serialization shape
- normalized runtime command envelopes
- domain-event payload serialization
- provider-neutral model results
- normalized provider capability results
- normalized runtime errors
- manifests and deterministic package representations

Golden tests must not freeze open-ended model wording, strategic creativity or subjective language quality as though those outputs were deterministic contracts.

A golden fixture changes only when the underlying approved contract or intentionally expected representation changes.

### 25.13 Test Data Safety

Default test data must be synthetic, sanitized or explicitly approved for test use.

Test fixtures must not require:

- production API keys or credentials
- unrestricted private provider payloads
- unauthorized voice or identity assets
- hidden production policy values
- mutable live provider state
- paid external execution

Real production artefacts, voices or provider responses may be used only through an explicitly approved test path with appropriate authorization, redaction and isolation.

### 25.14 Fixture Authority Boundary

- Fixtures demonstrate cases; frozen contracts define required behavior.
- A fixture must not create a new enum, policy rule, state or capability merely because a test expects it.
- Test helper convenience must not override exact bindings, approvals or config snapshots.
- Updating a fixture to make a failing implementation pass is forbidden unless the expected contract itself intentionally changed.
- Provider fixtures must preserve production provider-neutral schemas rather than creating test-only response shapes.
- Golden outputs remain derived test expectations, not canonical runtime artefacts.
