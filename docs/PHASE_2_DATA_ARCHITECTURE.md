# PHASE 2 — DATA ARCHITECTURE
## Creative Experimentation OS — Chile

**Date:** 2026-09-04
**Revision:** 3 — final freeze correction pass applied (see **§AJ**). Twelve corrections raised across three external audit passes, twelve accepted.
**Status:** Data contract and data-model design. No implementation code, no Python models, no schema files in final locations, no SQLite database, no repository reorganisation, no runtime dependencies installed.
**Predecessor:** `docs/PHASE_1_SYSTEM_DESIGN.md` (Revision 2 — external audit corrections applied). Treated as **frozen architecture**.
**Historical source:** `PRE_FLIGHT_AUDIT.md` — read, not modified.
**Authorisation:** Phase 2 only. Phase 3 not started.

**Language note:** written in English because the required section headers are in English. The *system* produces Spanish (`es-CL`) output.

**Reading order for the impatient:** §A (verdict) → §C (object map) → §E (identifiers) → §F (unknown semantics) → §G.0 (lifecycle model) → §Y (invariants) → §AG (what was cut) → §AJ (what the audit changed).

---

## A. Executive Data Architecture Verdict

### Is the Phase 1 architecture representable as data?

**Yes — and it is representable with substantially less machinery than the Master Prompt's field lists imply.** The epistemic spine (`SOURCE → OBSERVATION → INSIGHT → HYPOTHESIS → CONCEPT → EXPERIMENT → CREATIVE → PERFORMANCE → LEARNING`) is the load-bearing structure, and it survives intact. Almost everything else in the specification is either a **field of one of nine objects**, a **projection**, or a **configuration file**.

The design below carries:

| | Count |
|---|---|
| Canonical artefact types (campaign deliverables) | **8** |
| Canonical system records | **2** (Run head, Gate Decision) |
| Canonical stores | **4** (Evidence Ledger, Asset Registry, Config Registry, Event Log) |
| First-class entity types | **20** |
| Identifier types retained for V1-Core | **19** (5 registry, 1 content-deterministic, 3 random-allocated, 9 scope-ordinal, 1 pure-derived) |
| Canonical config registries | **9** |
| SQLite projection objects | **22** (20 relational + 1 FTS + 1 metadata) |
| Domain event types | **16** |
| Validation invariants | **120** |
| State machines | **8**, all derived — none stored |
| DATA ADRs | **33** |

### The four structural decisions that carry the design

**1. Three storage regimes, and nothing mutable in any of them.** Artefacts are **versioned and immutable** (integer version + content hash + `supersedes` + `inputs[]`). Entity records are **immutable**, written once, and they represent **creation**. Everything that changes afterwards — a source being re-accessed, a claim becoming verified, an asset being attested and promoted, a run accumulating steps and rejections — is an **append-only domain event**, and current state is a **deterministic fold** of the record's initial state over those events. No canonical record has a field that is ever rewritten in place, and **no fact is written twice**: creation lives in the record, change lives in the log, never both (§G.0).

**2. One `Fact` shape, four keys, used everywhere a field can be unknown.** `{value, state, refs, note}`. It appears in Product Truth, Brand Snapshot, Market Snapshot and Audience Model. There is no second epistemic vocabulary. The Master Prompt's five missing-data concepts collapse into **six** epistemic states plus one rule: **`ABSENT` is a value, not a state.**

**3. A single `dimensions` block travels the whole pipeline.** The six strategic dimensions the diversity solver measures (`awareness_state`, `core_problem`, `dominant_desire`, `current_belief`, `angle_mechanism`, `psychological_hypothesis`) are minted once on the **Hypothesis**, inherited unchanged by the **Concept**, and inherited unchanged by the **Creative**. They are simultaneously the diversity vector, the near-duplicate detector's input, and the future performance feature vector. One definition, three consumers, zero back-fill.

**4. Sub-objects are addressed by path, not by minted IDs.** `CRE-acme-3f8b21-07@v3#hook.copy` addresses the hook copy without a `HOOK_ID`. The same scheme addresses script segments, scenes, beats and experiment arms. This is what kills `ANGLE_ID`, `VARIANT_ID`, `HOOK_ID`, `SEGMENT_ID`, `SCENE_ID`, `BEAT_ID` and `ARM_ID` — seven identifier types the Master Prompt's noun list would otherwise have produced.

### What this design refuses to do

- **No numeric confidence anywhere.** Not one `0-1`, `0-10` or `0-100` field survives. Where the Master Prompt asked for a coverage score, the answer is an enumerated state plus a **count of fields in each state** — counts are measured, so they are permitted.
- **No `COMPLETE | PARTIAL | ABSENT` coverage enum.** Audited and rejected in favour of the epistemic enum plus counts (§I). A dimension that is "PARTIAL" tells an operator nothing about whether it may be claimed; `INFERRED` does.
- **No claim can enter a script through a path that does not pass a deterministic evidence-class check.** The binding runs on the **final localised text**, not on the draft.
- **No model ever emits an identifier.** IDs are allocated by the orchestrator. Model-facing schemas are a narrowed projection of storage schemas with every ID, hash and derived field removed. This is an invariant, not a convention.
- **No artefact carries a forward reference to something that does not exist yet.** The Experiment Plan approved at Gate 2 contains no `creative_id`, because creatives do not exist at Gate 2. Binding is a separate, later, deterministic step (§O.6). The same rule retires `CAMPAIGN_ID`'s ordinal, which needed a campaign scope in order to create one (§E.1.2).
- **No mutable allocator state.** An ordinal is `max(existing in that namespace and scope) + 1`, computed from the records that bear it, so nothing separate can desynchronise. V1 pays for this by **forbidding concurrent writers within an allocation scope** rather than claiming safety it does not have (§E.1.1).
- **No human gate may change an input that generation already consumed.** A gate cannot clear a `HARD_BLOCK`, cannot approve while requiring a change, and cannot raise a claim-freedom tier — including the regulated-category cap, which has no override path in V1 (§V.2).

### The three risks this data model does not eliminate

1. **Semantic claim intensification during localisation** that changes no claim reference and drops no verbatim qualification. The deterministic checks catch set-level and verbatim-level changes; genuine rewording that overstates within the same claim reaches `COMPLIANCE_REVIEW` as judgement. Named honestly in §AE Case G and §AF.
2. **A thin evidence base producing ten well-formed, well-grounded, strategically similar concepts.** The `dimensions` spread audit detects dimensional collapse; it cannot detect ten concepts that differ dimensionally and say the same thing aloud. Gate 2's human read remains the only control (Phase 1 §Q.4).
3. **Configuration drift.** The **nine** authored config registries (§B.1) now carry real enforcement weight, and one of them — `evidence_policy` — retroactively determines source quality classes. They are hashed into every run and into every artefact's `inputs[]`, so a bad edit is attributable and its effect on prior verifications is detectable on rebuild; nothing prevents the edit itself.

### Contradictions found with Phase 1

**One boundary conflict and one cold-start conflict, no architectural contradiction.**

1. Phase 1 §F places the Brand Snapshot in Phase I (step 3, before Gate 1) and produced by the same Skill as Product Truth, while the Master Prompt §4 lists it as possible content of the Research Dossier (Phase II, after Gate 1). These cannot both hold. Resolved in §I and DATA_ADR-004 — **approved by the user**: the Brand Snapshot is a section of Product Truth.
2. Revision 1 of this document made `identity != VERIFIED` compute to `T0` and halt, which would have stopped a campaign whose product is directly *observed* from the supplied image but not externally verifiable — contradicting both Phase 1 §M (*"Brand research returns nothing → proceed at T1 on image observations alone"*) and the product's minimum-input requirement. Corrected in §I.5: `T0` now means identity is **not established at all**; `OBSERVED` identity lands at `T1`.

---

## B. Canonical Data Principles

These are the data-layer expression of Phase 1 §C. Where a Phase 1 principle already covers it, the reference is given rather than restated.

**P1 — Every field that can be unknown carries an explicit epistemic state.** `null` is never a meaningful value. (Phase 1 §C.1)

**P2 — `ABSENT` is a value, not a state.** "The product contains no gluten" is `{value: false, state: VERIFIED}`. "We did not look" is `{value: null, state: NOT_COLLECTED}`. Conflating them is the failure §7 of the Master Prompt names.

**P3 — Derived data is labelled at the field level and is never accepted as input.** Every object and every non-obvious field carries one of `CANONICAL`, `DERIVED_DETERMINISTIC`, `DERIVED_GENERATIVE`, `EPHEMERAL`, `INDEX_ONLY`, `EXTERNAL_REFERENCE`. A writer that supplies a `DERIVED_DETERMINISTIC` field is rejected — the service computes it.

**P4 — Three storage regimes, and no fourth.** Artefacts version. Entity records are written once. Change is an appended event. No object does two of these, and no object does none of them. (§G.0)

**P5 — Immutability on write, without exception.** An artefact version is frozen the moment it is written, not the moment something references it; an entity record is frozen the moment it is registered. Corrections create `v+1` for artefacts and a new event for entities. Nothing in the canonical store is ever rewritten in place — there is no field anywhere whose value is updated.

**P6 — Identity is assigned by the orchestrator, never by a model and never by a filename or row number.** Ordinal identifiers are `max(existing in that namespace and scope) + 1`, allocated and persisted as one atomic operation under a single writer per allocation scope, so identity needs no mutable counter — and V1 forbids concurrent allocation within a scope rather than claiming to be safe under it (§E.1.1). (Master Prompt §6)

**P7 — Sub-objects are addressed by fragment path.** Mint an ID only when the object outlives its parent or is referenced from a different artefact family.

**P8 — Enumerations over scalars; counts where something is genuinely counted.** (Phase 1 §C.8, §Y.2)

**P9 — Provenance travels with content into the prompt.** A retrieval hit carries `knowledge_id`, `tier` and `retrieval_policy`. (Phase 1 §C.6)

**P10 — Only deterministic checks may write `HARD_BLOCK`.** The `HARD_BLOCK` value is absent from every model-facing schema's enum, so a model cannot emit one even by accident. (Phase 1 §C.16, ADR-032)

**P11 — Quality objectives are recorded as targets with attainment, never as constraints.** Any field whose value can be improved by inventing evidence is specified wrongly. (Phase 1 §C.17)

**P12 — Policy is data, not code, and the list of policy files is closed.** Claim-type→evidence-class requirements, the deny-list, narrative patterns, format constraints, taxonomies and the generation-duration ceiling live in the **nine** config registries of §B.1, hashed into every run. Changing policy must not require a schema migration; adding a *tenth* implicit config dependency is a defect (INV-115).

**P13 — SQLite holds nothing that cannot be rebuilt.** Enforced by a rebuild-and-diff check, not by discipline. (Phase 1 ADR-004)

**P14 — Reasoning summaries, never reasoning traces.** Run Manifests store `decision`, `rationale`, `alternatives_rejected` as written statements. Chain-of-thought is `EPHEMERAL` and is never persisted. (Master Prompt §40)

**P15 — Sensitive attributes are never inferred.** Audience demographic, health-status, ethnicity, religion and sexual-orientation fields may hold `OBSERVED` or `UNKNOWN` only. `INFERRED` is schema-invalid for them. This is the one place where the relaxation in §F.2 (an inference may cite its basis) does **not** apply: for these fields, no basis makes an inference acceptable.

### B.1 The canonical Config Registry — nine files, and only nine

Every enforcement rule, taxonomy and threshold in the system resolves to exactly one of these. This list is authoritative: §W's `versions.config`, every artefact's `inputs[]`, `creative.lineage.config`, §AF R3 and §AI all use it verbatim, and any reference to configuration not on this list is a defect.

| # | Registry | Contains | Read by |
|---|---|---|---|
| 1 | `evidence_policy` | Source-class derivation rules, publisher registry, claim-type × evidence-class matrix, minimum independent-source counts | Source classifier, claim verifier, safety validator |
| 2 | `deny_list` | Compliance hard-block rules with `rule_id`, basis and applicable field paths | Deny-list matcher, concept pre-screen |
| 3 | `narrative_library` | Narrative patterns: `NARRATIVE_PATTERN_ID`, structure, format affinity | `creative-strategist`, `script-engine` |
| 4 | `format_profiles` | Per-format speaker counts, allowed segment kinds, forbidden kinds, likeness rules | Script validator, feasibility service |
| 5 | `category_profiles` | Per-category required identity fields, `not_applicable` field list, extension fields, `regulated` flag | Product Truth writer, coverage service, claim-freedom resolver |
| 6 | `creative_taxonomy` | `angle_mechanisms`, `psychological_hypotheses`, `hook_entry_devices`, `claim_territories`, persuasion-strategy enums | `creative-strategist`, `script-engine`, claim-freedom resolver, diversity solver |
| 7 | `experiment_variables` | Testable variable → Creative Record field path | Experiment designer, lock validator |
| 8 | `diversity_targets` | Default target counts per dimension | Diversity solver |
| 9 | `tool_capability` | Generation-unit duration ceiling and other tool limits, each with `verification_status` | Feasibility service, package assembler |

`creative_taxonomy` exists because Revision 1 referenced a `config/psych_hypotheses` file that appeared in no list — an implicit dependency. Folding angle mechanisms, psychological hypotheses, hook entry devices and claim territories into one taxonomy file keeps the strategic vocabulary in one reviewable place and keeps the registry count closed.

---

## C. Canonical Object Map

### C.1 The spine

```
                    ┌────────────────────────────────────┐
   AUTHORED CONFIG  │  CONFIG REGISTRY — nine files      │  evidence_policy · deny_list
   (hashed, §B.1)   │  (YAML, human-authored)            │  narrative_library · format_profiles
                    └────────────────┬───────────────────┘  category_profiles · creative_taxonomy
                                     │ hashed into every    experiment_variables · diversity_targets
                                     │ run and artefact     tool_capability
   ┌───────────┐   ┌───────────┐     │
   │  BRAND    │──►│  PRODUCT  │     │
   └───────────┘   └─────┬─────┘     │
                         │           │
                   ┌─────▼───────────▼────────────────────────────────────────┐
                   │              CAMPAIGN  ◄── CAMPAIGN BRIEF (artefact 1)   │
                   └─────┬────────────────────────────────────────────────────┘
                         │
                         │  every step below is executed by a RUN (immutable head)
                         │  and appended to the EVENT LOG
                         │
   ╔═════════════════════▼══════════════════════════════════════════════════╗
   ║  EVIDENCE LEDGER  (immutable records, product-scoped)                  ║
   ║                                                                        ║
   ║   ┌────────┐   1..n   ┌─────────────────────┐  1..n  ┌─────────────┐   ║
   ║   │ SOURCE │─────────►│ EVIDENCE_EXTRACTION │───────►│ OBSERVATION │   ║
   ║   └────────┘    E1     │  (E1 output, proof) │  E2/E3 └──────┬──────┘   ║
   ║        ▲               └─────────────────────┘               │         ║
   ║        │ snapshot                                     n..m   │         ║
   ║   ┌────┴────┐                                    ┌───────────▼──────┐  ║
   ║   │  ASSET  │                                    │      CLAIM       │  ║
   ║   └────┬────┘                                    └─────────┬────────┘  ║
   ╚════════╪══════════════════════════════════════════════════╪═══════════╝
            │                                                  │
            │        ╔═════════════════════════════════════╗   │
            └───────►║  EVENT LOG  (append-only, 4 scopes) ║◄──┘
                     ║  evidence · asset · campaign · run  ║
                     ║      │                              ║
                     ║      ▼  deterministic fold          ║
                     ║  DERIVED CURRENT STATE              ║
                     ║  claim.status · asset.state+rights  ║
                     ║  creative.state · package.state     ║
                     ║  experiment.state · campaign.state  ║
                     ║  run manifest · source.accessed_at  ║
                     ╚═════════════════════════════════════╝
                                        │ refs
   ┌────────────────────────────────────▼───────────────────────┐
   │  PRODUCT TRUTH  (artefact 2, product-scoped, versioned)    │
   │    · product facts  · brand snapshot  · coverage vector    │
   │    · claim_freedom { tier, permitted_territories }         │
   └────────────────────────────────────┬───────────────────────┘
                                        │
                          ▲ HUMAN GATE 1 — TRUTH & EVIDENCE
                                        │
   ┌────────────────────────────────────▼───────────────────────┐
   │  RESEARCH DOSSIER  (artefact 3, campaign-scoped, versioned)│
   │    · market snapshot   · audience model + persuasion       │
   │    · INSIGHT[]  (addressable, embedded)                    │
   │    · refs → OBSERVATION[] (customer language, competitors) │
   └────────────────────────────────────┬───────────────────────┘
                                        │
   ┌────────────────────────────────────▼───────────────────────┐
   │  HYPOTHESIS POOL  (artefact 4, versioned)  20–30           │
   │    HYPOTHESIS · dimensions{6} · falsification_condition    │
   └────────────────────────────────────┬───────────────────────┘
                                        │ 10 selected
   ┌────────────────────────────────────▼───────────────────────┐
   │  EXPERIMENT PLAN  (artefact 5, versioned)                  │
   │    · CONCEPT[] (embedded, addressable)                     │
   │    · diversity_audit                                       │
   │    · EXPERIMENT DESIGN[]  arms → concept + creative_slot   │
   │      (NO creative_id — creatives do not exist yet)         │
   └────────────────────────────────────┬───────────────────────┘
                                        │
                          ▲ HUMAN GATE 2 — CONCEPTS & EXPERIMENT DESIGN
                                        │
   ┌────────────────────────────────────▼───────────────────────┐
   │  CREATIVE RECORD ×10 (artefact 6, versioned, per-instance) │
   │    identity · lineage · strategy · execution · hook        │
   │    script · visual_plan · evidence · quality · compliance  │
   │    feasibility · experiment{arm_binding}                   │
   │    (state is NOT stored here — it is folded from events)   │
   └───────────┬───────────────────────────────────┬────────────┘
               │                                   │
               │  EXPERIMENT BINDING + LOCK VALIDATION           
               │  (DERIVED_DETERMINISTIC projection, §O.6)      
               │  arm_key → creative_id@version                 
               │                                   │
               │ locked projection                 │ derived projection
   ┌───────────▼──────────────┐        ┌───────────▼───────────────┐
   │ PRODUCTION PACKAGE ×10   │        │  META TEST PLAN           │
   │ (artefact 7, locked)     │        │  (artefact 8, versioned)  │
   └───────────┬──────────────┘        └───────────────────────────┘
               │
   ▲ HUMAN GATE 3 — PRODUCTION RELEASE  (GATE_DECISION binds exact hashes)
               │
   ┌───────────▼──────────────┐     ┌─────────────────────────────────────┐
   │  V1-PRODUCTION           │     │  FUTURE (interface only)            │
   │  generated ASSET records │────►│  PUBLICATION → PERFORMANCE →        │
   │  derived_from lineage    │     │  EXPERIMENT ANALYSIS → LEARNING     │
   └──────────────────────────┘     └─────────────────────────────────────┘
```

### C.2 Cardinalities

| Relationship | Cardinality | Note |
|---|---|---|
| BRAND → PRODUCT | 1..n | |
| PRODUCT → PRODUCT TRUTH version | 1..n | Product-scoped, not campaign-scoped |
| PRODUCT → CAMPAIGN | 1..n | |
| CAMPAIGN → RUN | 1..n | A campaign may be resumed; each resumption is a run |
| SOURCE → EVIDENCE_EXTRACTION | 1..n | One per (source, run, E1 call) |
| EVIDENCE_EXTRACTION → OBSERVATION | 1..n | E2/E3 output |
| OBSERVATION → CLAIM | n..m | A claim may rest on several observations; an observation may support several claims |
| OBSERVATION → INSIGHT | n..m | ≥ 1 observation required |
| INSIGHT → HYPOTHESIS | n..m | ≥ 1 insight **or** observation required |
| HYPOTHESIS → CONCEPT | 1..0-1 | A selected hypothesis becomes exactly one concept |
| CONCEPT → CREATIVE SLOT | 1..n | Slots are declared at Gate 2; creatives fill them later |
| CREATIVE SLOT → CREATIVE | 1..0-1 | Resolved by the binding step after Phase IV |
| CONCEPT → CREATIVE | 1..n | Usually 1 in V1; the model permits several formats per concept |
| EXPERIMENT ARM → CREATIVE | 1..0-1 | Via the binding; an arm is unbound until its slot is filled |
| CREATIVE → EXPERIMENT ARM | 1..0-1 | A creative occupies at most one arm (INV-107) |
| CREATIVE → PRODUCTION PACKAGE | 1..n | One package per locked creative version |
| PRODUCTION PACKAGE → generated ASSET | 1..n | V1-Production |
| ASSET → ASSET (`derived_from`) | n..m, acyclic | Rights lineage DAG |
| GATE_DECISION → artefact version | 1..n | Binds by `content_hash` |
| ENTITY → DOMAIN EVENT | 1..n | Every state change; the fold produces current state |

### C.3 What is deliberately *not* in the map

`ANGLE` (attribute of a hypothesis, Phase 1 §O) · `VARIANT` (a creative plus an experiment-arm relationship, §36) · `HOOK` (four addressable sub-objects of a creative, §28) · `CUSTOMER_LANGUAGE_ENTRY` (an observation with `kind: CUSTOMER_LANGUAGE`) · `BRAND_SNAPSHOT` (a section of Product Truth, §I) · `CREATIVE_DNA` (a deterministic projection, §AB) · `PERSONA` / `SEGMENT` (the Audience Model is one object in V1) · `VOICE_PROFILE` (deferred; V1-Core carries a Voice **Specification**, Phase 1 §K).

---

## D. Artefact vs Entity vs Value Object Classification

Seven classes, applied to every object in the design.

| Class | Definition | Storage regime | Examples |
|---|---|---|---|
| **Versioned artefact** | A durable deliverable with a lifecycle, reviewed by humans, referenced by downstream work | Integer version + hash; immutable per version | Campaign Brief, Product Truth, Research Dossier, Hypothesis Pool, Experiment Plan, Creative Record, Production Package, Meta Test Plan |
| **First-class entity** | Has identity, is referenced from outside its container, has a lineage or a derived state machine | **Immutable record** (written once), or a versioned artefact | Brand, Product, Campaign, Run, Source, Evidence Extraction, Observation, Insight, Claim, Hypothesis, Concept, Experiment, Creative, Production Package, Asset, Style Profile, Narrative Pattern, Gate Decision, Knowledge Resource, Domain Event |
| **Embedded value object** | Has no identity of its own; meaningless outside its parent; addressed by fragment path | Inline in the parent | `Fact`, `Locator`, `Dimensions`, `BeliefBridge`, `VoiceSpecification`, `Hook.copy`, `ScriptSegment`, `Scene`, `GenerationUnit`, `ContinuityAnchor`, `ExperimentArm`, `MeasurementPlan`, `CoverageDimension`, `RightsBlock` |
| **Domain event** | An append-only, timestamped statement that something happened; the **only** way any canonical state changes | Append-only log, four scopes (§G.0) | `SOURCE_ACCESSED`, `CLAIM_STATUS_ASSERTED`, `ASSET_STATE_CHANGED`, `CREATIVE_STATE_CHANGED`, `RUN_REJECTION` |
| **Derived projection** | Recomputable from canonical artefacts and the event log by a pure function | Materialised in SQLite, or rendered to a git-tracked file marked derived | Creative DNA, coverage vector, claim-freedom tier, **every current state**, the **Run Manifest**, the **experiment binding**, Markdown gate renders, every SQLite table |
| **Enumeration** | A closed or registry-backed value set | Config registry (YAML) or schema enum | Epistemic states, claim statuses, source classes, formats, narrative patterns, territories, shot framings |
| **Transient reasoning state** | Model scratch work, intermediate prompts, raw API envelopes | **Never persisted** | Chain-of-thought, unparsed tool envelopes, retry scratch |

### D.1 The five judgement calls

**Insight is first-class but embedded.** It has an ID and is referenced by hypotheses, but it is born inside the Research Dossier and is only meaningful with it. It is stored inline and addressed as `CMP-acme-3f8b21/research_dossier@v2#insights[INS-acme-3f8b21-004]`. The consequence — anything citing an insight must pin the dossier version — is the correct behaviour anyway.

**Concept is first-class but embedded** in the Experiment Plan, for the same reason and by the same mechanism. This is what Master Prompt §4 item 5 asks for.

**Production Package is a versioned artefact *and* a projection.** It is materialised (not a view) because V1-Production must be able to work from it alone, but it must remain byte-reconstructible from the Creative Record version it projects plus the projector version. Both properties are required; §R shows how they coexist.

**Run Manifest is a derived projection over a system record, not a campaign artefact.** The canonical parts are an immutable **RUN head** (what was known when the run started) and the run's **event log** (everything that then happened). The manifest a human reads is the fold of the two. It is **outside** the eight artefact families: a Gate 3 reviewer approves creatives, not the log of how they were made. Master Prompt §4's audit question is answered "outside."

**Domain Event is a first-class entity without a minted ID.** It has identity — `(log, event_seq)` — but that identity is the append position in its own log, not an allocated identifier. This is the deliberate application of P7: an event never outlives its log and is never referenced from another artefact family, so minting an `EVENT_ID` would add an identifier type and buy nothing.

---

## E. Identifier Architecture

### E.1 The five creation authorities

Revision 1 called `GATE_ID` and `EXTRACTION_ID` "derived handles". They are not: both contain a monotonically increasing ordinal, and an ordinal has to come from somewhere. Revision 2 named that honestly but then answered it wrongly, claiming the ordinal was `count(entries in the log) + 1` and that atomic append made a counter unnecessary. **Atomic append and unique ordinal allocation are different problems**, and conflating them is the error Correction 10 identifies: two writers can each read `N` and each try to write `N+1`, and the fact that both appends complete atomically is exactly why both succeed. Atomicity guarantees a well-formed file, not a unique number.

| Authority | Who assigns | Uniqueness rests on | Members |
|---|---|---|---|
| **Registry (human)** | Operator or author, at registration | A human choosing a distinct slug | `BRAND_ID`, `PRODUCT_ID`, `STYLE_ID`, `NARRATIVE_PATTERN_ID`, `KNOWLEDGE_ID` |
| **Content-deterministic** | Pure function of the record's own content | The hash | `SOURCE_ID` |
| **Random-allocated** | Orchestrator, from a time or entropy source | Entropy — no coordination required | `CAMPAIGN_ID`, `RUN_ID`, `ASSET_ID` |
| **Scope-ordinal** | Orchestrator, inside an existing scope, under a **single-writer guarantee** | Serialisation within the scope (§E.1.1) | `OBSERVATION_ID`, `INSIGHT_ID`, `CLAIM_ID`, `HYPOTHESIS_ID`, `CONCEPT_ID`, `EXPERIMENT_ID`, `CREATIVE_ID`, `GATE_ID`, `EXTRACTION_ID` |
| **Pure-derived** | A total function of other identifiers; no ordering, no entropy | The function | `PACKAGE_ID` |

**`PACKAGE_ID` is the only genuinely derived identifier.** `PKG-<creative-suffix>-v<n>` is a total function of `(creative_id, creative_version)` and can be recomputed by anyone holding those two values.

### E.1.1 Scope-ordinal allocation — the actual rule

The term "log-positional" is retired: it described the wrong mechanism. An entity ordinal is **not** an event-log position — insights, hypotheses and concepts are not entries in any of the four domain-event logs at all, and reading a generic log count to number a different namespace was never coherent.

```
next_ordinal(namespace, scope) = max(existing ordinal for that ENTITY NAMESPACE
                                     within that SCOPE) + 1
```

Four properties, and the third is the one Revision 2 was missing:

1. **Namespace- and scope-specific.** `HYP` ordinals within campaign `CMP-acme-3f8b21` are computed from existing `HYP-acme-3f8b21-*` identifiers, never from a log's length. `max + 1`, not `count + 1` — so a gap left by a deleted or never-persisted record does not cause a reuse.
2. **Allocation and the canonical write are one atomic operation.** The orchestrator does not hand out a number and write later; it resolves `max + 1` and persists the record bearing it as a single unit. A failure leaves neither.
3. **Single writer per allocation scope.** An allocation scope is `(entity namespace, scope id)` — e.g. hypotheses of one campaign, observations of one product, gate decisions of one campaign. **V1 forbids concurrent writers to the same scope** (INV-117). This is not a hopeful assumption: Phase 1 §V's storage decision is a single-user, single-machine, self-hosted orchestrator, and Phase 1 §D.1 places one run on one operator's machine. Two runs on *different* campaigns touch different scopes and may proceed in parallel; two runs on the same campaign are serialised by the runtime.
4. **No mutable counter file.** `max + 1` is computed by reading the records that already exist, so there is no separate number that can drift out of step with the data it numbers (INV-116). Ordinals are never reused, including after a rejection (INV-118).

**What this design does not claim.** It does not claim to be safe under concurrent writers — it forbids them. Making scope-ordinal allocation concurrency-safe would need either a lock, a compare-and-swap, or a serialising service, and none of those is worth building for a single-operator V1. If a later version needs concurrent campaign execution, the honest options are to serialise per scope through the orchestrator, or to move the affected identifiers to random allocation. Recording the constraint is what makes that choice available later rather than discovered in production.

### E.1.2 Why `CAMPAIGN_ID` is random-allocated

`CMP-acme-3f8b21` was circular: a campaign-scoped ordinal needs a campaign scope to exist, and the campaign id *is* what establishes that scope. There is no scope to count within at the moment the campaign is created. The alternative — a global per-brand campaign counter — reintroduces exactly the mutable global state the design removed, to buy nothing but a prettier number.

```
CAMPAIGN_ID   CMP-<brand-slug>-<6 hex>     CMP-acme-3f8b21
```

The brand prefix keeps it readable and greppable; the suffix is entropy, needs no coordination, and cannot collide in practice. Campaign ordering comes from `created_at`, which is what ordering should have come from anyway — `001` never meant "first", it meant "first successfully allocated", which is not the same thing.

**No model in the system may emit an identifier.** Model-facing schemas omit every ID field; the orchestrator assigns and attaches them after validation. This is INV-06 and it is the single cheapest defence against fabricated cross-references.

### E.2 Formats

```
BRAND_ID              BRD-<slug>                        BRD-acme
PRODUCT_ID            PRD-<brand-slug>-<slug>           PRD-acme-magnesio-500
STYLE_ID              STY-<format>-<slug>               STY-ugc-raw-handheld
NARRATIVE_PATTERN_ID  NAR-<slug>                        NAR-confession
KNOWLEDGE_ID          KNW-<slug>                        KNW-schwartz-persuasion

CAMPAIGN_ID           CMP-<brand-slug>-<6 hex>          CMP-acme-3f8b21
RUN_ID                RUN-<UTC compact>-<6 hex>         RUN-20260904T1132Z-a91c4e
SOURCE_ID             SRC-<sha256(locator_root ⏎ content_sha256)[:12]>
                                                        SRC-4f9a2c81d0b7
OBSERVATION_ID        OBS-<product-slug>-<NNNN>         OBS-magnesio-500-0042
CLAIM_ID              CLM-<product-slug>-<NNNN>         CLM-magnesio-500-0007
INSIGHT_ID            INS-<campaign-suffix>-<NNN>       INS-acme-3f8b21-004
HYPOTHESIS_ID         HYP-<campaign-suffix>-<NNN>       HYP-acme-3f8b21-017
CONCEPT_ID            CON-<campaign-suffix>-<NN>        CON-acme-3f8b21-03
EXPERIMENT_ID         EXP-<campaign-suffix>-<NN>        EXP-acme-3f8b21-01
CREATIVE_ID           CRE-<campaign-suffix>-<NN>        CRE-acme-3f8b21-07
ASSET_ID              AST-<12 hex>                      AST-7b31e0c9d4a2
GATE_ID               GAT-<campaign-suffix>-<NNN>       GAT-acme-3f8b21-003
EXTRACTION_ID         EXT-<run-suffix>-<NNN>            EXT-a91c4e-012

PACKAGE_ID (derived)  PKG-<creative-suffix>-v<n>        PKG-acme-3f8b21-07-v1

DOMAIN EVENT          not an identifier type — addressed as (log, event_seq)
                                                        evidence@CMP-acme-3f8b21#0417
```

### E.3 Properties per identifier

"Allocation scope" is the `(namespace, scope)` pair a scope-ordinal is unique within, and the pair that V1 serialises (§E.1.1). It is not always the same as the *uniqueness* scope: an `OBSERVATION_ID` is unique per product because its ordinal is allocated per product.

| ID | Authority | Allocation scope | Uniqueness scope | Immutable | Human-readable | Reusable across campaigns |
|---|---|---|---|---|---|---|
| `BRAND_ID` | Registry | — | Global | Yes | Required | — |
| `PRODUCT_ID` | Registry | — | Global | Yes | Required | — |
| `STYLE_ID` | Registry | — | Global | Yes | Required | **Yes** |
| `NARRATIVE_PATTERN_ID` | Registry | — | Global | Yes | Required | **Yes** |
| `KNOWLEDGE_ID` | Registry | — | Global | Yes | Required | **Yes** |
| `SOURCE_ID` | Content-deterministic | — | Global, per occurrence | Yes | No | **Yes** |
| `CAMPAIGN_ID` | Random | — | Global | Yes | Brand prefix only | — |
| `RUN_ID` | Random | — | Global | Yes | Sortable, not descriptive | — |
| `ASSET_ID` | Random | — | Global | Yes | No | **Yes** |
| `OBSERVATION_ID` | Scope-ordinal | `(OBS, product)` | Product | Yes | Partially | **Yes** |
| `CLAIM_ID` | Scope-ordinal | `(CLM, product)` | Product | Yes | Partially | **Yes** |
| `INSIGHT_ID` | Scope-ordinal | `(INS, campaign)` | Campaign | Yes | Partially | No |
| `HYPOTHESIS_ID` | Scope-ordinal | `(HYP, campaign)` | Campaign | Yes | Partially | No |
| `CONCEPT_ID` | Scope-ordinal | `(CON, campaign)` | Campaign | Yes | Partially | No |
| `EXPERIMENT_ID` | Scope-ordinal | `(EXP, campaign)` | Campaign | Yes | Partially | No |
| `CREATIVE_ID` | Scope-ordinal | `(CRE, campaign)` | Campaign | Yes | Partially | No |
| `GATE_ID` | Scope-ordinal | `(GAT, campaign)` | Campaign | Yes | No | No |
| `EXTRACTION_ID` | Scope-ordinal | `(EXT, run)` | Run | Yes | No | No |
| `PACKAGE_ID` | Pure-derived | — | Campaign | Yes | Yes | No |

**Ordinals are never reused.** If `HYP-acme-3f8b21-017` is rejected, `017` is retired — because the next ordinal is `max + 1` over identifiers that already exist, and a rejected record still exists. Nothing recycles a gap, and no counter exists to be lost, corrupted or double-issued (INV-118).

### E.4 Content identity vs provenance identity

**`SOURCE_ID` is deterministic over the *occurrence*, not over the content alone.**

```
SOURCE_ID = "SRC-" + sha256( locator_root.value + "\n" + content_sha256 )[:12]
```

Revision 1 hashed content only, which collapsed two genuinely different provenance records whenever their bytes matched. The failure is concrete and consequential: **the same PDF hosted by a regulator and by the manufacturer has identical bytes and completely different evidentiary authority.** Under content-only identity the second retrieval would resolve to the first record, and a claim substantiated by the *regulator's* copy would silently inherit — or lose — its class depending on which copy was fetched first. That is the A1/A2 distinction (Phase 1 ADR-034) destroyed by an identifier choice.

The corrected model separates the two identities cleanly:

| | Field | Answers |
|---|---|---|
| **Provenance identity** | `source_id` (over `locator_root` + `content_sha256`) | "Which occurrence of this document did we read, and from whom?" |
| **Content identity** | `content_sha256` | "Is this the same document, wherever it came from?" |

Consequences, all of them wanted:

- Two SOURCE records may share `content_sha256` while differing in `locator_root`, `publisher_declared`, derived `owner_relationship` and derived `quality_class`. Both are kept. Neither is a duplicate.
- Re-fetching the same URL with unchanged bytes yields the **same** `source_id` — so it is an *access event*, not a new record (§G.0).
- Re-fetching the same URL with changed bytes yields a **different** `source_id` — "the page changed under us" stays visible, which was the one property worth keeping from Revision 1.
- Content deduplication is still available, by grouping on `content_sha256`; the `sources` projection indexes it (§Z).
- **No second document object is introduced.** The audit's constraint is met: one entity, two identity fields.

**`ASSET_ID` is neither content- nor occurrence-derived; it is random-allocated.** Two records may legitimately share bytes and differ in rights provenance (the same image supplied by the operator and also present in the repository), and unlike a source there is no stable "locator" to disambiguate them — the same file can be re-uploaded from anywhere. Rights attach to provenance, not to bytes. `content_sha256` is a field; a deterministic check raises `SHARED_CONTENT_DIFFERENT_RIGHTS` when two asset records share a hash and differ in derived state or rights owner (§S).

### E.5 Artefact addressing and fragment references

Artefacts that are singletons per scope have **no ID of their own**. They are addressed by `(scope_id, artefact_type, version)`:

```
PRODUCT_TRUTH      product_id  + version    PRD-acme-magnesio-500/product_truth@v2
CAMPAIGN_BRIEF     campaign_id + version    CMP-acme-3f8b21/campaign_brief@v1
RESEARCH_DOSSIER   campaign_id + version    CMP-acme-3f8b21/research_dossier@v2
HYPOTHESIS_POOL    campaign_id + version    CMP-acme-3f8b21/hypothesis_pool@v1
EXPERIMENT_PLAN    campaign_id + version    CMP-acme-3f8b21/experiment_plan@v3
META_TEST_PLAN     campaign_id + version    CMP-acme-3f8b21/meta_test_plan@v1
```

**Fragment reference grammar** — the mechanism that eliminates seven ID types:

```
<artefact-address>#<path>

CRE-acme-3f8b21-07@v3#hook.copy
CRE-acme-3f8b21-07@v3#script.segments[s-014]
CRE-acme-3f8b21-07@v3#visual_plan.scenes[sc-03]
CMP-acme-3f8b21/experiment_plan@v3#experiments[EXP-acme-3f8b21-01].arms[a2]
CMP-acme-3f8b21/research_dossier@v2#insights[INS-acme-3f8b21-004]
```

A fragment reference **must** carry the version. A reference without `@v<n>` is schema-invalid (INV-11). This is what makes "approving V3 must not silently approve V4" mechanically true rather than a policy.

Local keys inside an artefact (`s-014`, `sc-03`, `a2`, `b-hook`) are **stable within a version** and may be renumbered between versions — which is precisely why the version is mandatory in the reference.

### E.6 Deferred and eliminated

**Deferred (interface defined, not allocated in V1-Core):** `VOICE_ID` (V1-Production, Phase 1 §K) · `META_AD_ID`, `POST_ID`, `AD_SET_ID` (`EXTERNAL_REFERENCE`, performance layer) · `LEARNING_ID` (performance layer) · `GENERATION_ATTEMPT_ID` (V1-Production).

**Eliminated with reasons:**

| Rejected ID | Why |
|---|---|
| `ANGLE_ID` | An angle is an attribute block of a hypothesis (Phase 1 §O). Nothing references an angle independently. |
| `VARIANT_ID` | A variant is `CREATIVE_ID` + an experiment arm. The arm already records `variable_value`. (§36) |
| `HOOK_ID` × 4 | Fragment paths `#hook.strategy\|copy\|visual\|audio` are individually addressable. (§28) |
| `SEGMENT_ID`, `SCENE_ID`, `BEAT_ID` | Local keys inside a versioned creative. |
| `ARM_ID` | Local key inside a versioned experiment. |
| `BRAND_SNAPSHOT_ID` | A section of Product Truth. |
| `CUSTOMER_LANGUAGE_ID` | An observation with `kind: CUSTOMER_LANGUAGE`. |
| `PERSONA_ID` / `SEGMENT_ID` | The V1 Audience Model is one object. Reintroduce when the first campaign genuinely targets two segments. |
| `CREATIVE_DNA_ID` | A projection of the Creative Record. |
| `EVIDENCE_LEDGER_ID` | The ledger is a store, not an object. |
| `EVENT_ID` | A domain event is addressed by `(log, event_seq)`. It never outlives its log and is never referenced from another artefact family, so an identifier type would buy nothing (D.1). |
| `SOURCE_ACCESS_EVENT_ID`, `CLAIM_EVENT_ID`, `ASSET_EVENT_ID`, `RUN_EVENT_ID` | Four identifier types the audit invited. All rejected: one typed event envelope with a `event_type` discriminator covers every case, and the local key is sufficient. |
| `EXPERIMENT_BINDING_ID` | The binding is a derived projection keyed by `(experiment_id, arm_key)`. |
| `CREATIVE_SLOT_ID` | A local key inside the Experiment Plan version. |

---

## F. Unknown / Missing Semantics

### F.1 The minimum enum

The Master Prompt lists five concepts: `UNKNOWN`, `NOT_APPLICABLE`, `NOT_COLLECTED`, `PENDING_VERIFICATION`, `ABSENT`. Audited:

| Proposed | Verdict |
|---|---|
| `UNKNOWN` | **Keep.** Researched, unresolved. |
| `NOT_COLLECTED` | **Keep.** No attempt made. Different from `UNKNOWN` in exactly the way that matters: `UNKNOWN` is a research finding, `NOT_COLLECTED` is a gap in the run. |
| `NOT_APPLICABLE` | **Keep.** The field is meaningless for this category. |
| `PENDING_VERIFICATION` | **Reject as a field state.** It is a *claim lifecycle* state, and Master Prompt §14 warns against reusing Product Truth states for claims. It becomes `CLAIM.status = UNVERIFIED`. |
| `ABSENT` | **Reject as a state. It is a value.** `{value: false \| [], state: VERIFIED}` says the product definitively lacks the thing. Making it a state would make "verified absence" indistinguishable from "no data", which is the exact error §7 warns about, inverted. |

Combined with the four Phase 1 epistemic states, the **single field-state enum** is:

```
epistemic_state:
  VERIFIED        source-anchored at or above the required class for this field
  OBSERVED        directly observed by the system (image, label, page text)
  INFERRED        interpretation — may rest on evidence, but is not itself
                  an observation or a verified fact; never promotable in place
  UNKNOWN         researched, unresolved
  NOT_COLLECTED   not attempted in this run
  NOT_APPLICABLE  meaningless for this category
```

Six values. One enum. Used by `Fact`, by the coverage vector and by nothing else.

### F.2 The rules

`refs` means something different either side of the observation/interpretation line, and the difference is what the rules encode:

- for `VERIFIED` and `OBSERVED`, `refs` is **substantiating evidence** — the field's value is asserted *by* those records;
- for `INFERRED`, `refs` is **interpretive basis** — the field's value is a reading *of* those records, and remains the reader's inference.

| Rule | Statement |
|---|---|
| **F-R1** | `value: null` is legal **only** when `state ∈ {UNKNOWN, NOT_COLLECTED, NOT_APPLICABLE}`. |
| **F-R2** | `state ∈ {VERIFIED, OBSERVED}` requires `refs` non-empty, and those refs substantiate the value. |
| **F-R3** | `state: INFERRED` requires `note` non-empty stating the inferential step. `refs` **may be non-empty**, and where the inference rests on evidence it **must** be — an interpretation that discards its basis is unreviewable. `refs` here are basis, never substantiation. |
| **F-R4** | `state: UNKNOWN` requires `note` naming what was attempted. `NOT_COLLECTED` requires no note. This is what makes the two distinguishable in review. |
| **F-R5** | `INFERRED` values may **never** be promoted in place. Promotion to `OBSERVED` or `VERIFIED` requires a **new artefact version** carrying a new `Fact` whose refs substantiate the value at the evidence class the field's claim type requires. |
| **F-R6** | `INFERRED` values may never substantiate a `CLAIM`, may never bind to a script line, and are counted separately from `VERIFIED`/`OBSERVED` in the coverage roll-up. An `INFERRED` field can never raise the claim-freedom tier. |
| **F-R7** | Sensitive fields (§B P15) accept only `OBSERVED`, `UNKNOWN`, `NOT_COLLECTED`, `NOT_APPLICABLE`. `INFERRED` and `VERIFIED` are schema-invalid for them **regardless of basis** — this is the one carve-out from F-R3. |
| **F-R8** | Empty string `""` is never written. Use `null` with the appropriate state. |
| **F-R9** | An `INFERRED` fact with empty `refs` is a **bare inference**: legitimate for genuinely conventional readings, but forbidden on fields where a stereotype is the obvious lazy answer — `awareness_state` and `sophistication_state` (INV-112), and every sensitive field (F-R7). |

**Why F-R3 changed.** Revision 1 required `refs` to be *empty* on `INFERRED`, reasoning that an inference citing evidence must really be an observation. That is epistemically wrong, and it forced a bad choice: three observations about repeat purchases and stated priorities may support the interpretation *"buyers appear to prioritise convenience over price"* without that interpretation being either observed or verified. Under the old rule the strategist had to either drop the basis (making the interpretation unreviewable) or mislabel the interpretation as `OBSERVED` (making an inference look like a fact). Both outcomes are worse than the thing the rule was trying to prevent. The distinction that actually matters — *may this substantiate a product claim?* — is carried by F-R6, which is unchanged.

### F.3 The `Fact` value object

**Classification: CANONICAL** (the `value` and `refs`), with `state` **DERIVED_DETERMINISTIC** when written by the evidence pipeline and **DERIVED_GENERATIVE** when written by a Skill from an image or from category knowledge. The distinction is recorded once per artefact in `provenance.produced_by`, not per field.

```yaml
# The universal Fact shape — four keys, no nesting beyond `value`
value:  <scalar | list | object | null>
state:  VERIFIED | OBSERVED | INFERRED | UNKNOWN | NOT_COLLECTED | NOT_APPLICABLE
refs:   [ "OBS-magnesio-500-0042", "CLM-magnesio-500-0007" ]   # OBS-* or CLM-*
        # substantiation when VERIFIED/OBSERVED; basis when INFERRED; empty otherwise
note:   "string | null"
```

Audited against the Master Prompt §8 proposal: `source_refs` and `observation_refs` are **merged into one `refs` list**, because a source is always reachable through its observation and a two-list shape invites writers to populate one and not the other. `notes` → `note` (singular; one string, not a list). Result: four keys instead of five, one reference list instead of two, and self-describing prefixes make the polymorphism free.

### F.4 Minimal example

```json
{
  "material": { "value": null, "state": "NOT_COLLECTED", "refs": [], "note": null },
  "contains_gluten": { "value": false, "state": "VERIFIED",
                       "refs": ["CLM-magnesio-500-0011"], "note": null },
  "shelf_life_months": { "value": null, "state": "UNKNOWN", "refs": [],
                         "note": "Official product page and label image checked; not stated." },
  "expiry_date": { "value": null, "state": "NOT_APPLICABLE", "refs": [], "note": null },
  "typical_use_frequency": { "value": "daily", "state": "INFERRED", "refs": [],
                             "note": "Bare inference: category convention for oral supplements. Not on label, no observation cites it." }
}
```

And an inference that *does* rest on evidence — the case Revision 1 could not express:

```json
{
  "purchase_priority": {
    "value": "convenience over price",
    "state": "INFERRED",
    "refs": ["OBS-magnesio-500-0044", "OBS-magnesio-500-0051", "OBS-magnesio-500-0058"],
    "note": "Interpretation. Three reviews mention repeat purchase despite a cheaper alternative being named in the same review. No source states a priority ordering."
  }
}
```

Four different kinds of "we don't have a value", plus two kinds of inference, each actionable and each distinguishable. Neither inference can appear as a claim in a script (F-R6); the second one can be argued with, because its basis is on the record.

---

## G. Versioning and Immutability

### G.0 The lifecycle model — immutable record + domain events → derived state

Revision 1 declared ledger records "append-only and unversioned" and then required several of them to change: a `SOURCE` grew its `accessed_at[]`, a `CLAIM` moved through `UNVERIFIED → VERIFIED → DISPUTED`, an `ASSET` accumulated rights attestations and state transitions, a `RUN MANIFEST` accreted steps, decisions, rejections, costs and outputs for the whole length of a run, and `creative.state` walked five values without the creative's content changing. Each of those is an in-place mutation of something the document called immutable. Appending to a list inside a stored record is still rewriting that record.

The correction is one mechanism, applied uniformly:

```
       IMMUTABLE ENTITY RECORD              APPEND-ONLY DOMAIN EVENTS
       creation, written once          +    SUBSEQUENT CHANGE ONLY
       never rewritten                      one typed envelope, four logs
                        │                             │
                        └──────────────┬──────────────┘
                                       ▼
                            DERIVED CURRENT STATE
                    a pure fold, in event_seq order, recomputable
                    from scratch at any time, stored only in SQLite
```

**The division of labour is exact: creation is the record, change is an event.** An entity's existence and its initial state are established by writing its record and by nothing else. There is no creation event anywhere in the system (INV-119).

This matters for correctness, not tidiness. A `record + creation event` pair is a **dual write across two files**: if the record lands and the event does not, the entity exists with no state; if the event lands and the record does not, the fold references a subject that is not there. Making that safe needs a cross-file transaction, which a git-tracked filesystem store does not offer and which V1 should not be building. Removing the pair removes the problem instead of guarding it.

The initial state is therefore a **pure function of the record**, not a payload someone wrote:

| Entity | Initial state, derived from the record | Change thereafter |
|---|---|---|
| `ASSET` | `origin.kind` ⇒ `USER_UPLOAD → USER_PROVIDED_UNVERIFIED`, `REPOSITORY`/`THIRD_PARTY_FETCH → REFERENCE`, `GENERATED → GENERATED_DRAFT` | `ASSET_STATE_CHANGED`, `ASSET_RIGHTS_ATTESTED` |
| `CLAIM` | `UNVERIFIED` | `CLAIM_STATUS_ASSERTED`, `CLAIM_DISPUTED`, `CLAIM_SUPERSEDED`, `CLAIM_REJECTED` |
| `CREATIVE` version | `DRAFT` | `CREATIVE_STATE_CHANGED` |
| `PRODUCTION PACKAGE` | `DRAFT` | `PACKAGE_STATE_CHANGED` |
| `EXPERIMENT` | `DESIGNED` | Gate decisions and the binding projection; `EXPERIMENT_INVALIDATED` |
| `RUN` | `RUNNING` (the head is written when the run starts) | `RUN_STATUS_CHANGED` |
| `SOURCE` | `first_accessed_at` on the record | `SOURCE_ACCESSED` for **re-**access only |
| `GATE_DECISION` | The record *is* the decision; it has no lifecycle | — |
| `CAMPAIGN` | `INTAKE` | Derived from gate decision records |

`GATE_DECISION` is the clearest case. It is already an immutable canonical record carrying reviewer, verdict, hashes and reasoning; a `GATE_DECISION_RECORDED` event restating that a decision was made was a second copy of a fact that cannot change. Campaign state now folds **directly over gate decision records**, which is both simpler and one fewer place for the two to disagree.

**One event envelope, not four event types.** The audit invited `SOURCE_ACCESS_EVENT`, `CLAIM_EVENT`, `ASSET_EVENT` and `RUN_EVENT`. Four record types with four identifier types would be event sourcing for its own sake. One typed envelope with a discriminator does the same work:

```yaml
# DOMAIN EVENT — CANONICAL, append-only. Addressed as (log, event_seq).
event_seq:    417                      # append position in this log; not an allocated ID
event_type:   CLAIM_STATUS_ASSERTED
subject_ref:  CLM-magnesio-500-0007    # the entity whose state this changes
occurred_at:  "2026-09-04T13:41:08Z"
actor:        { kind: RUNTIME | OPERATOR, id: "svc-orchestrator" }
run_id:       RUN-20260904T1132Z-a91c4e
step_id:      "E3#004" | null
payload:      { … }                    # closed schema, one per event_type
```

**Four logs, scoped to match the entities they describe.** Scope is not decoration: the evidence log is product-scoped because claims outlive campaigns, the asset log is global because assets are shared, and the run log is run-scoped because a resumed run is a new run.

| Log | Scope | Event types |
|---|---|---|
| `evidence` | Product | `SOURCE_ACCESSED` (re-access only) · `CLAIM_STATUS_ASSERTED` · `CLAIM_DISPUTED` · `CLAIM_SUPERSEDED` · `CLAIM_REJECTED` |
| `asset` | Global | `ASSET_RIGHTS_ATTESTED` · `ASSET_STATE_CHANGED` |
| `campaign` | Campaign | `CREATIVE_STATE_CHANGED` · `PACKAGE_STATE_CHANGED` · `EXPERIMENT_INVALIDATED` |
| `run` | Run | `RUN_STATUS_CHANGED` · `RUN_STEP_COMPLETED` · `RUN_DECISION` · `RUN_REJECTION` · `RUN_ERROR` · `RUN_RETRY` |

**Sixteen event types, down from twenty-two.** Six were removed by the final freeze pass, each because it duplicated a fact another canonical artefact already carried:

| Removed | Why | Where the fact lives now |
|---|---|---|
| `ASSET_REGISTERED` | Creation duplicate | The ASSET record; initial state derives from `origin.kind` |
| `GATE_DECISION_RECORDED` | Creation duplicate | The GATE_DECISION record; campaign state folds over those records |
| `EXPERIMENT_STATE_CHANGED` (except invalidation) | `APPROVED` comes from a gate decision, `BOUND` and `LOCK_VALIDATED` from the binding projection — all derived | Renamed `EXPERIMENT_INVALIDATED`, the one transition that is a decision rather than a derivation |
| `ASSET_WITHDRAWN` | A state change wearing a different name | `ASSET_STATE_CHANGED` |
| `RUN_SOURCE_CONSULTED` | Duplicated `SOURCE_ACCESSED` and the SOURCE record | The envelope already carries `run_id`; the manifest filters the evidence log plus SOURCE records with matching `created_by_run_id` |
| `RUN_COST_RECORDED` | Duplicated `RUN_STEP_COMPLETED.cost_usd` | Summed from step events |
| `RUN_OUTPUT_WRITTEN` | Duplicated the artefact's own `created_by_run_id` | `outputs[]` is derived by scanning artefacts for that run |

**What each Revision 1 mutation became:**

| Was (Revision 1) | Is now |
|---|---|
| `SOURCE.accessed_at[]` grows | `first_accessed_at` on the immutable record; `SOURCE_ACCESSED` events for **later** accesses only; `accessed_at[]` is the concatenation |
| `CLAIM.status` changes | Record folds to `UNVERIFIED`; `CLAIM_STATUS_ASSERTED` and friends move it |
| `CLAIM.disputed_by` set symmetrically | One `CLAIM_DISPUTED` event naming **both** claims. Asymmetry is now unrepresentable rather than merely forbidden |
| `ASSET.rights` edited on attestation | `ASSET_RIGHTS_ATTESTED` carrying the whole rights block; the fold is last-write-wins with full history |
| `ASSET.state` + `state_history[]` | Initial state from `origin.kind`; `ASSET_STATE_CHANGED` events carry `from`, `to`, `reason`, `conditions_met[]`; `state_history` **is** the record-derived start plus the event slice |
| `RUN MANIFEST` accretes everything | Immutable **RUN head** (§W.1) + run event log; the manifest is the fold (§W.2) |
| `creative.state` + `state.history[]` | Record folds to `DRAFT`; `CREATIVE_STATE_CHANGED` events move it |
| `package.state`, `experiment.state`, campaign state | `PACKAGE_STATE_CHANGED`; experiment and campaign state fold over gate decision records and the binding projection |

**What this does not become.** There are no aggregates, no snapshots, no projections-of-projections, no command objects, no event versioning scheme, no replay-from-offset machinery, no eventual consistency. The fold is a `for` loop over an append-only file, run by the index builder, and its output lives only in SQLite (§Z) and in rendered reviews. If the fold is lost, it is recomputed; if the log is lost, so is the history, which is why the log is canonical and git-tracked and the fold is not.

**Why the state machines get simpler, not more complex.** A stored state field has to be defended against writers; a folded state has no writer to defend against. Every state machine in §X is now a specification of *which events are legal from which folded state*, which is exactly what a state machine is, and the illegal transition is refused at append time rather than discovered later in a stored record that someone edited.

### G.1 The three regimes

| | **Versioned artefacts** | **Immutable entity records** | **Domain events** |
|---|---|---|---|
| **Members** | The 8 artefact types | Source, Evidence Extraction, Observation, Claim, Asset, Gate Decision, Run head, Brand, Product | The four logs above |
| **Represents** | A deliverable, at a version | **Creation**, and everything about the entity that cannot change | **Change only** — never creation |
| **Identity** | `(scope_id, artefact_type, version)` or `(entity_id, version)` | Record ID | `(log, event_seq)` |
| **Written** | Once per version | Once, at creation | Once, appended |
| **Changed** | Never — new version | **Never** | Never — new event |
| **Current state** | The highest version | Initial state derived from the record, then folded with its events | — |
| **History** | Every version retained | Record + its event slice | The log |
| **Ordering** | Monotonic integer `version` | `created_at` | `event_seq` |

**One canonical fact has one canonical representation.** A fact is either in a record or in an event, never in both — which is what makes the two-file write unnecessary and the fold unambiguous.

No object belongs to two regimes, and no object belongs to none. That is the whole check: if a field changes over time and is not in an event payload, the design is wrong (INV-101).

### G.2 The version block (every artefact)

```yaml
version:            3                      # CANONICAL, monotonic integer, per identity
created_at:         "2026-09-04T14:22:07Z" # CANONICAL, UTC, RFC 3339, second precision
created_by_run_id:  RUN-20260904T1132Z-a91c4e
created_by_actor:   { kind: RUNTIME|OPERATOR, id: "svc-orchestrator" }
content_hash:       "sha256:9f3c…"         # DERIVED_DETERMINISTIC
supersedes:         2 | null
supersede_reason:   "Gate 1 correction: identity was mis-observed" | null
inputs:                                    # CANONICAL — every input, pinned
  - { ref: "PRD-acme-magnesio-500/product_truth@v2", hash: "sha256:11ab…" }
  - { ref: "CMP-acme-3f8b21/research_dossier@v2",       hash: "sha256:77de…" }
  - { ref: "config/evidence_policy@v4",              hash: "sha256:c0ff…" }
provenance:
  produced_by:      DETERMINISTIC | GENERATIVE | HUMAN | MIXED
  skills:           { script-engine: "1.2.0" }
  models:           { drafting: "claude-opus-5", critic: "claude-opus-5" }
  prompts:          { script_draft: "sha256:aa11…" }
```

### G.3 Versioning scheme — audited

| Candidate | Verdict |
|---|---|
| **Semantic versioning** | **Rejected.** There is no public API surface. "Is this a breaking change to a Product Truth?" is a judgement call that will be made inconsistently, and inconsistent version semantics are worse than none. |
| **Content hash alone** | **Rejected.** Not human-orderable. "Which came first, `9f3c` or `11ab`?" has no answer without a lookup, and gate reviews are human work. |
| **Integer + content hash** | **Accepted.** The integer orders and is quotable in conversation; the hash identifies, detects tampering, and binds gate approvals. |

`content_hash` is computed over the **canonical serialization** (§G.7) of the artefact **with the `content_hash` field itself omitted**, so the hash is reproducible by any reader.

### G.4 Immutability policy

**P5 — every artefact version is immutable on write.** Phase 1 §42 permits editing a version until something references it; this design is stricter, for three reasons: reference counting is a distributed-state problem in a filesystem store; the `latest` pointer makes the "not yet referenced" window invisible to a reviewer; and git makes an in-place edit of a written version detectable but not preventable, so the rule needs to be simple enough that a violation is obvious in a diff.

Consequences, stated plainly:

- Product Truth v2 does not modify v1. Creative `CRE-acme-3f8b21-07` generated from Product Truth v1 keeps pointing at v1 forever, and remains explainable eighteen months later.
- A typo correction costs a version. Accepted. Versions are cheap; attribution is not.
- **A state change costs an event, not a version.** This is what makes strict immutability affordable: a creative walking `DRAFT → VALIDATED → REVIEWED → LOCKED` produces four events and **one** artefact version, not four versions of identical content. Revision 1 had no answer to this and would have forced either version churn or an in-place write.
- **There are now zero mutable objects in the canonical store.** Revision 1 conceded one — the allocator counter — and scope-ordinal allocation (§E.1.1) has removed it: the next ordinal is `max + 1` over records that already exist, so nothing separate is kept and nothing can drift. The price, stated rather than hidden, is that allocation is serialised per scope instead of being concurrency-safe (INV-117).

### G.5 The `latest` pointer

A `latest` pointer per artefact identity may exist as a **DERIVED_DETERMINISTIC** convenience (highest `version` whose state is not `REJECTED`). It is never authoritative, never referenced by another artefact's `inputs[]`, and is recomputable by listing versions. **No downstream reference may resolve through `latest`** (INV-12) — every stored reference pins a version.

### G.6 What "reproducible" means here

Phase 1 §W's standard is adopted verbatim: **re-derivable, not re-runnable.** The data-layer obligation is that from a `RUN_ID` a reader can reconstruct, without re-running anything: every input artefact version and hash, every config hash, every model ID, every source consulted, every decision recorded, every rejection recorded, and every output artefact version. `inputs[]` plus the Run Manifest plus git history is exactly that set.
### G.7 File serialization — audited, not assumed

The audit criteria are the ones Master Prompt §45 names: machine validation, human review, diff quality, escaping of full scripts and multiline spoken copy, determinism, schema support.

| Criterion | JSON | YAML |
|---|---|---|
| Machine validation | JSON Schema is native | Requires conversion; schema tooling is second-class |
| Deterministic round-trip | One canonical form is achievable (sorted keys, fixed indent) | Multiple valid renderings of the same data; parsers disagree |
| Escaping full scripts | Poor — `\n` and `\"` inside one long string | Excellent — block scalars (`\|`) render spoken Spanish naturally |
| Human review | Poor for prose, adequate for structure | Good for both |
| Diff quality | Good if the structure is granular; bad if text is one long value | Good |
| Type hazards | None | Real: `no` → `false`, unquoted `Ella dijo: hola` breaks, sexagesimal, tab handling |
| Hashing | Trivially stable | Stable only over raw bytes, not over re-serialization |

**Decision — JSON for every machine artefact and every ledger record; YAML only for hand-authored config; Markdown for human review.**

1. **JSON is canonical** for the 8 artefact types and all ledger/registry records. UTF-8, no BOM, LF newlines, 2-space indent, keys sorted lexicographically, no trailing whitespace, one file per artefact version. `content_hash` is `sha256` over this rendering with the `content_hash` key removed.
2. **The diff-quality objection is answered by granularity, not by format.** Script text lives in `script.segments[].text`, one segment per object, so editing one line changes one line of JSON. A monolithic `script_text` field would have made YAML necessary; the segment model makes it unnecessary.
3. **YAML is used only where a human is the author** — `config/*.yaml` and knowledge front-matter. These are loaded with a safe loader under a restricted schema, and their hash is taken **over the file bytes**, never over a re-serialization, which sidesteps YAML's round-trip non-determinism entirely.
4. **Human review is served by a derived Markdown render**, `DERIVED_DETERMINISTIC` and git-tracked, regenerated from the JSON at gate time. A Gate 3 reviewer reads a rendered package, not raw JSON — and because the render is derived and hashed, it cannot silently disagree with the artefact.

This is chosen for determinism and validation, not aesthetics. YAML would read better and hash worse, and the artefact whose hash binds a human approval is not the place to trade determinism for readability.

### G.8 Schema strategy

**Decision — Pydantic v2 models as the single source of truth, generating JSON Schema (2020-12) artefacts.** Phase 1 ADR-001 chose Python; Anthropic structured outputs consume JSON Schema; Pydantic supplies runtime validation plus the cross-field and referential rules that JSON Schema alone cannot express (F-R1…F-R8, INV-40, INV-44). One definition, two consumers, no hand-maintained schema drift.

**The critical constraint: model-facing schemas are a narrowed projection of storage schemas.**

| | Storage schema | Model-facing schema |
|---|---|---|
| IDs | Present | **Removed** — the orchestrator allocates (INV-06) |
| `content_hash`, `version`, `inputs[]` | Present | Removed |
| `DERIVED_DETERMINISTIC` fields | Present | **Removed** — a service computes them |
| `HARD_BLOCK` enum values | Present on `safety` | **Absent everywhere** (P10) |
| `additionalProperties` | — | `false`, with `strict: true` |
| Evidence extraction (E1) | — | **No schema at all** — citations and structured outputs are mutually exclusive (Phase 1 ADR-006/031) |

Phase 2 defines these as **contracts**, expressed above as concise JSON/YAML shapes. No Python is written, no schema file is created, and no final repository location is chosen — Phase 3 owns layout and Phase 4 onward owns implementation.

---

## H. Campaign Brief Schema

**PURPOSE** — The single canonical record of what the operator asked for. Everything downstream that is "a choice, not a finding" traces to here.
**CANONICAL OR DERIVED** — `CANONICAL INPUT`. No field in this artefact is ever written by a model.
**OWNING COMPONENT** — Campaign Intake (orchestrator step + script, Phase 1 §D).
**LIFECYCLE** — Created at intake. Re-versioned only by an operator (e.g. Gate 2 changes the batch size). Never modified by a run.
**IDENTIFIER** — `(campaign_id, campaign_brief, version)`. Creates the `CAMPAIGN_ID`.
**VERSIONING RULE** — New version on any operator change. A run that consumed v1 keeps pointing at v1.

### Required fields

```yaml
campaign_id / brand_id / product_id
market:              "CL"                      # ISO 3166-1 alpha-2
language:            "es-CL"                   # BCP 47
onboarding_level:    1 | 2 | 3 | 4
objective:           free text, one paragraph, operator-written
batch:
  size:              10
  format_mix:        { UGC: 5, PODCAST: 2, ANIMATION: 3 }   # HARD CONSTRAINT
provided_assets:     [ ASSET_ID ]              # ≥ 1 product image at level 1
operator:            { name, identifier }
```

### Optional fields

```yaml
diversity_targets:   { awareness_state: 3, core_problem: 4, dominant_desire: 3,
                       current_belief: 3, angle_mechanism: 4,
                       psychological_hypothesis: 4, narrative_pattern: 5 }
                     # DEFAULTS from config/diversity_targets; overridable here.
                     # TARGETS, never constraints (Phase 1 §Q).
constraints:
  brand:             [ "never use the word X", "always show the cap closed" ]
  negative:          [ "no white coats", "no before/after" ]
  required_qualifiers: [ free text ]
offer:               { kind: DISCOUNT|BUNDLE|FREE_SHIPPING|NONE,
                       description, valid_from, valid_until, claim_refs: [] }
target_duration_s:   { UGC: 40, PODCAST: 60, ANIMATION: 30 }
budget_ceiling_usd:  120                       # per-campaign runtime cost ceiling
notes:               free text
```

### Enums

`onboarding_level: 1..4` · `format: UGC | PODCAST | ANIMATION` (validated against `config/format_profiles`, not hardcoded) · `offer.kind`.

### Relationships

`brand_id` → BRAND · `product_id` → PRODUCT · `provided_assets[]` → ASSET · consumed by every downstream artefact via `inputs[]`.

### Invariants

INV-01 `sum(format_mix.values()) == batch.size`. INV-02 every `provided_assets[]` entry resolves to a registered ASSET. INV-03 at onboarding level 1, at least one asset has `asset_type: PRODUCT_IMAGE`. INV-04 `diversity_targets` values are integers ≤ `batch.size`. INV-05 no field of this artefact may be written by a generative step.

### Minimal example

```json
{
  "campaign_id": "CMP-acme-3f8b21",
  "brand_id": "BRD-acme", "product_id": "PRD-acme-magnesio-500",
  "market": "CL", "language": "es-CL", "onboarding_level": 1,
  "objective": "EXAMPLE_ONLY — first paid-social test for this product in Chile.",
  "batch": { "size": 10, "format_mix": { "UGC": 5, "PODCAST": 2, "ANIMATION": 3 } },
  "provided_assets": ["AST-7b31e0c9d4a2"],
  "operator": { "name": "EXAMPLE_ONLY", "identifier": "op-01" },
  "version": 1, "created_at": "2026-09-04T11:32:00Z",
  "created_by_run_id": "RUN-20260904T1132Z-a91c4e",
  "content_hash": "sha256:…", "supersedes": null, "inputs": []
}
```

---

## I. Product Truth Schema

**PURPOSE** — Everything the system believes about the product and its brand, with the epistemic state of every belief, and the deterministic consequence of those states (coverage, claim freedom).
**CANONICAL OR DERIVED** — **MIXED, and the mix is the point.** `facts.*` are `DERIVED_GENERATIVE` when written from image analysis or category knowledge, and `CANONICAL` when the value came from the operator. `coverage` and `claim_freedom` are `DERIVED_DETERMINISTIC` and may not be written by any model.
**OWNING COMPONENT** — `product-intelligence` Skill (facts) + Product Truth Completeness service and Claim Freedom resolver (coverage, tier).
**LIFECYCLE** — Created in Phase I of a run. Corrected at Gate 1 by an operator (new version). Extended by later runs at higher onboarding levels (new version). Product-scoped, so it survives the campaign.
**IDENTIFIER** — `(product_id, product_truth, version)`.
**VERSIONING RULE** — New version on any fact change, any operator correction, or any re-derivation of coverage. `supersede_reason` required.

### I.1 The Brand Snapshot boundary decision

**Recommendation: the Brand Snapshot is a section *inside* Product Truth, not a section of the Research Dossier.**

Three reasons: (1) Phase 1 §E #1 merged Brand Intelligence into `product-intelligence` precisely because brand facts and product facts are the same procedure with the same failure mode; (2) Phase 1 §F places Brand Snapshot at step 3, in Phase I, **before** Gate 1, while the Research Dossier is built in Phase II **after** Gate 1 — putting them in one artefact would require the dossier to exist before the gate that precedes it; (3) brand facts are `Fact`-shaped exactly like product facts, so one artefact means one shape, one validator and one review.

This diverges from Master Prompt §4's suggestion that the dossier "may contain Brand Snapshot", which is why §4 asked for the boundary to be audited. **Approved by the user in the external audit pass** (DATA_ADR-004, status `ACCEPTED`).

### I.2 Shape

```yaml
product_id / brand_id / version-block
category_profile_id:  "CAT-supplement-oral"      # → config/category_profiles
onboarding_level:     1

facts:                                            # every leaf is a Fact
  identity:
    product_name / brand_name / manufacturer / sku / gtin
    country_of_origin
  category:
    category / subcategory / regulated:  Fact<bool>
  visual:
    form_factor / container / colour / label_text_verbatim / approximate_size
  composition:
    ingredients[] / concentration / material / allergens / free_from[]
  function:
    intended_use / usage_instructions / dosage / frequency / duration_of_use
  commercial:
    price / currency / channel / availability / offer_terms
  proof:
    certifications[] / test_reports[] / clinical_references[]
  restrictions:
    contraindications / age_restrictions / regulatory_notices
  extensions:                                     # per category_profile
    <field_name>: Fact

brand_snapshot:                                   # same Fact shape
  positioning / category_context / claims_made_publicly[] / tone_of_voice
  proof_assets[] / official_channels[] / known_disputes[]

coverage:            <DERIVED_DETERMINISTIC — §I.4>
claim_freedom:       <DERIVED_DETERMINISTIC — §I.5>
```

### I.3 Core fields vs category extensions

The Master Prompt §8 warning is honoured: **not every category field is universal.** The split is:

| | Where | Applies |
|---|---|---|
| **Core fields** | `facts.identity`, `facts.category`, `facts.visual`, `facts.function`, `facts.commercial` | Every product |
| **Conditional core** | `facts.composition`, `facts.proof`, `facts.restrictions` | Present for all, but individual fields resolve to `NOT_APPLICABLE` via the category profile |
| **Extensions** | `facts.extensions.*` | Declared by `config/category_profiles/<id>.yaml` |

A category profile is a small authored YAML:

```yaml
category_profile_id: CAT-supplement-oral
regulated: true                  # → claim-freedom tier is capped at T2, unconditionally (V1)
required_for_identity: [ product_name, brand_name, category ]
not_applicable:      [ facts.visual.material, facts.function.duration_of_use ]
extension_fields:
  - { name: serving_size,   dimension: composition }
  - { name: servings_per_container, dimension: composition }
```

**V1 ships two profiles**: `CAT-generic` and `CAT-supplement-oral`. That is enough to prove the mechanism and to exercise the regulated-category cap that Phase 1 §M requires.

### I.4 Coverage vector — audited and specified

**The Master Prompt §9 proposal `COMPLETE | PARTIAL | ABSENT` is rejected.** It answers "how much do we have" when the only question that matters downstream is "at what epistemic level do we have it". `PARTIAL` cannot drive a claim-freedom decision; `INFERRED` can.

**Coverage is the epistemic enum plus counts.** Per dimension:

```yaml
coverage:
  identity:
    state:  VERIFIED            # DERIVED: weakest state among this dimension's REQUIRED fields
    counts: { VERIFIED: 3, OBSERVED: 1, INFERRED: 0,
              UNKNOWN: 0, NOT_COLLECTED: 0, NOT_APPLICABLE: 1 }
    gaps:   []                  # field names not in {VERIFIED, OBSERVED, NOT_APPLICABLE}
  category:      { … }
  visual:        { … }
  composition:   { state: UNKNOWN, counts: {…}, gaps: [ingredients, concentration] }
  function:      { … }
  outcomes:      { … }
  commercial:    { … }
  proof:         { … }
  differentiation: { … }
  brand_context: { … }
```

Ten dimensions, matching Phase 1 §M. Rules:

- `state` = the **weakest** state present among the dimension's *required* fields, ordered `VERIFIED > OBSERVED > INFERRED > UNKNOWN > NOT_COLLECTED`, with `NOT_APPLICABLE` excluded from the ordering.
- A dimension whose every required field is `NOT_APPLICABLE` has `state: NOT_APPLICABLE`.
- `counts` are **measured**, not scored — permitted under §54.
- `INFERRED` is counted, never promoted, and never raises a dimension above `INFERRED` (F-R6). An interpretation with a solid basis is still not coverage.
- `gaps[]` is the operator's to-do list. This is the whole reason the vector exists: each entry is a specific, fixable gap (Phase 1 §M).
- No aggregate. There is no `overall_coverage` field and there will not be one.

### I.5 Claim freedom — precise tier definitions

Claim freedom is a **pure function** of `coverage` + `category_profile.regulated` + `disputed_claims`. Identical every run, computed by code, recorded, and inspectable.

**`T0` means the product is not identified. It does not mean the product is not externally verifiable.** Revision 1 made `identity != VERIFIED` compute to `T0` and halt, which would have refused every campaign whose product is legible in the supplied image but absent from the web — the exact minimum input the system exists to serve, and a direct contradiction of Phase 1 §M (*"Brand research returns nothing → proceed at T1 on image observations alone"*). An `OBSERVED` identity is an identity.

```
identity_established :=
     coverage.identity.state ∈ {OBSERVED, VERIFIED}
     AND every field in category_profile.required_for_identity
         has state ∈ {OBSERVED, VERIFIED, NOT_APPLICABLE}

T0   NOT identity_established
     (identity UNKNOWN / NOT_COLLECTED / INFERRED, or a required identity
      field unresolved — e.g. an illegible or ambiguous image)
     → HALT. Produce nothing. Request input.

T1   identity_established
     → evidence-safe territories only (below). This is where a Level-1
       cold start lands, and it is a productive territory.

T2   coverage.identity.state == VERIFIED                      ← VERIFIED required
     AND coverage.composition.state ∈ {VERIFIED, NOT_APPLICABLE}
     AND coverage.outcomes.state    ∉ {VERIFIED}

T3   coverage.identity.state == VERIFIED
     AND coverage.composition.state ∈ {VERIFIED, NOT_APPLICABLE}
     AND coverage.outcomes.state == VERIFIED
     AND every outcome-supporting claim has status VERIFIED at class A1

CAP  category_profile.regulated == true  ⇒  tier = min(tier, T2)
     UNCONDITIONALLY IN V1. There is no override path and no gate may lift it.
```

**The regulated cap has no escape hatch, and the reason is temporal, not moral.** Revision 2 allowed a Gate 3 override (`REGULATED_TIER_RELEASE`) to release a regulated creative above T2. That could never have worked: the tier is pinned onto the Creative Record at creation, and *everything upstream of Gate 3 already ran under it*. The compliance pre-screen killed any hypothesis needing an outcome promise, the concepts were designed inside T2's territory set, and the script was written and claim-bound against T2. By Gate 3 there is no T3 creative to release — there is a T2 creative and a reviewer being asked to relabel it. A gate cannot retroactively make an argument that was never generated.

Raising claim freedom is therefore not a review decision at all; it is an **input** decision, and it has to happen before concepts exist. A future version that needs regulated T3 would add a pre-creative regulatory workflow producing an explicitly versioned effective-policy artefact, consumed by the claim-freedom resolver alongside `category_profiles`, with the whole downstream pipeline then running under the raised tier. **That workflow is deferred and is not designed here** (DATA_ADR-031). For V1 the rule is flat: regulated ⇒ T2, full stop.

**`T2` and `T3` still require `identity.state == VERIFIED`** (INV-113), and that is not an inconsistency. Making a composition or outcome claim *about a product* presupposes knowing which product it is; an observed-but-unverified identity is enough to talk about what is visibly true and about the audience's situation, and not enough to assert what is inside the bottle. The tier ladder therefore has one step that upgrades on identity verification and two that upgrade on evidence — which is exactly the shape of the underlying epistemics.

**Permitted territories** — the tier is only useful if "what may be claimed" is data. It is:

```
CLAIM_TERRITORY enum
  OBSERVABLE_ATTRIBUTE      what is visibly true of the object
  CATEGORY_CONTEXT          statements about the category, not the product
  PROBLEM_CONTEXT           the audience's problem, evidenced by research
  SITUATIONAL_NARRATIVE     story, situation, moment of use
  IDENTITY_LIFESTYLE        who uses it and how they see themselves
  PRODUCT_INTERACTION       how the product is handled and used
  PRICE_OFFER               price, offer terms
  COMPOSITION_STATEMENT     what it contains / is made of
  MECHANISM_EXPLANATION     how it works, at the depth evidence supports
  CERTIFICATION_REFERENCE   the fact of holding a certification
  SOCIAL_PROOF_TESTIMONIAL  attributed customer statements
  OUTCOME_PROMISE           what it does for the user
  TIMEFRAME_CLAIM           how fast
  NUMERIC_PERFORMANCE       quantified effect
  COMPARATIVE_SUPERIORITY   better than an alternative
```

```yaml
claim_freedom:
  tier: T1                                   # DERIVED_DETERMINISTIC
  identity_basis: OBSERVED                   # OBSERVED | VERIFIED — why T1 and not T2
  permitted_territories:
    - OBSERVABLE_ATTRIBUTE
    - CATEGORY_CONTEXT
    - PROBLEM_CONTEXT
    - SITUATIONAL_NARRATIVE
    - IDENTITY_LIFESTYLE
    - PRODUCT_INTERACTION
    # PRICE_OFFER is present ONLY when coverage.commercial.state == VERIFIED (INV-114)
  forbidden_territories: [ PRICE_OFFER, COMPOSITION_STATEMENT, MECHANISM_EXPLANATION,
                           OUTCOME_PROMISE, TIMEFRAME_CLAIM, NUMERIC_PERFORMANCE,
                           COMPARATIVE_SUPERIORITY, CERTIFICATION_REFERENCE,
                           SOCIAL_PROOF_TESTIMONIAL ]
  limiting_factors:
    - { dimension: identity,    state: OBSERVED, gaps: [manufacturer, sku] }
    - { dimension: composition, state: UNKNOWN,  gaps: [ingredients, concentration] }
    - { dimension: commercial,  state: UNKNOWN,  gaps: [price] }
  computed_by: "claim-freedom-resolver@1.0.0"
  capped_by_regulated_category: false          # true ⇒ tier is T2 and cannot be raised
```

**The T1 territory set is evidence-safe by construction.** Every territory it permits is satisfiable from what a product image and market research actually establish: what the object visibly is, what the category is, what the audience's problem is, how the moment of use looks, who the user is, and how the product is handled. None of them asserts anything about the product's contents, mechanism or effect. `PRICE_OFFER` is the one conditional member — it is a factual assertion about commerce, so it enters only when `coverage.commercial.state == VERIFIED` (INV-114), and at a Level-1 cold start it will usually be absent.

`T2` adds `COMPOSITION_STATEMENT`, `MECHANISM_EXPLANATION`, `CERTIFICATION_REFERENCE`. `T3` adds `OUTCOME_PROMISE`, `TIMEFRAME_CLAIM`, `NUMERIC_PERFORMANCE` and — only with A1 evidence on both sides — `COMPARATIVE_SUPERIORITY`. `SOCIAL_PROOF_TESTIMONIAL` requires a `TESTIMONIAL` claim with an authorised consent record, independently of tier.

**A territory being permitted is necessary, never sufficient.** The tier opens a door; the claim-type × evidence-class matrix (§J.6) still has to be satisfied for each individual assertion at binding time. A creative at T3 whose numeric performance claim rests on A2 evidence is hard-blocked exactly as one at T1 would be. The tier prevents whole categories of argument from being *attempted*; the binding check prevents individual claims from being *made*.

No tier's meaning depends on a model's opinion. Every input to the function is either an enumerated state produced by the deterministic coverage roll-up, or a boolean from an authored config file.

### I.6 Invariants

INV-13 `coverage` and `claim_freedom` are rejected if present in a model's output. INV-14 `tier == T0` — meaning identity is **not established** — halts the run; no hypothesis, concept or creative may be created under this Product Truth version. An `OBSERVED` identity is established and does not halt. INV-15 every `Fact` obeys F-R1…F-R9. INV-16 a `Fact` with `state: VERIFIED` whose `refs` include a `CLM-*` requires that claim's derived `status == VERIFIED`. INV-17 `label_text_verbatim` is an `OBSERVED` fact **about the label**; a fact asserting the same content **about the product** must be a separate field with its own state (Phase 1 §M). INV-113 `T2` and `T3` require `coverage.identity.state == VERIFIED`. INV-114 `PRICE_OFFER` is permitted only when `coverage.commercial.state == VERIFIED`.

### I.7 Minimal example (Level 1 cold start, EXAMPLE_ONLY)

```json
{
  "product_id": "PRD-acme-magnesio-500", "brand_id": "BRD-acme",
  "category_profile_id": "CAT-supplement-oral", "onboarding_level": 1,
  "facts": {
    "identity": {
      "product_name": { "value": "EXAMPLE_ONLY", "state": "VERIFIED",
                        "refs": ["OBS-magnesio-500-0003"], "note": null },
      "manufacturer": { "value": null, "state": "UNKNOWN", "refs": [],
                        "note": "Official site checked; manufacturer not stated." }
    },
    "visual": {
      "form_factor": { "value": "bottle", "state": "OBSERVED",
                       "refs": ["OBS-magnesio-500-0001"], "note": null },
      "label_text_verbatim": { "value": "EXAMPLE_ONLY", "state": "OBSERVED",
                               "refs": ["OBS-magnesio-500-0002"], "note": null }
    },
    "composition": {
      "ingredients": { "value": null, "state": "UNKNOWN", "refs": [],
                       "note": "Label image legible only in part; no official spec sheet found." }
    }
  },
  "coverage": { "identity": { "state": "VERIFIED",
                              "counts": { "VERIFIED": 1, "OBSERVED": 0, "INFERRED": 0,
                                          "UNKNOWN": 1, "NOT_COLLECTED": 3,
                                          "NOT_APPLICABLE": 0 },
                              "gaps": ["manufacturer", "sku", "gtin", "country_of_origin"] } },
  "claim_freedom": { "tier": "T1", "capped_by_regulated_category": false }
}
```

---

## J. Source / Evidence / Claim Schema

The Evidence Ledger is **one store of immutable records, scoped to the product**, holding four record types: `SOURCE`, `EVIDENCE_EXTRACTION`, `OBSERVATION`, `CLAIM`. Everything that changes about them — a re-access, a verification, a dispute — is an event in the `evidence` log (§G.0). Market and audience observations live here too, distinguished by `subject`. One store, one ID scheme, one FTS index, reusable across campaigns for the same product.

### J.1 SOURCE

**PURPOSE** — Provenance for everything. **CANONICAL, immutable.** Owned by the Evidence Ledger writer.
**LIFECYCLE** — Written once, on first retrieval of this `(locator_root, content)` pair. **Never edited.** Re-retrieval appends a `SOURCE_ACCESSED` event.
**IDENTIFIER** — `SOURCE_ID`, deterministic over `(locator_root, content_sha256)` — occurrence identity, not content identity (§E.4).

```yaml
# --- immutable record -------------------------------------------------------
source_id:          SRC-4f9a2c81d0b7        # sha256(locator_root ⏎ content_sha256)[:12]
source_type:        WEB_PAGE | PDF | IMAGE | MARKETPLACE_LISTING | REVIEW_AGGREGATE
                    | SOCIAL_THREAD | VIDEO | REGULATORY_DOCUMENT | LAB_REPORT
                    | BRAND_DOCUMENT | OPERATOR_STATEMENT
title:              string
publisher_declared: string | null           # as stated by the artefact itself — raw, unjudged
locator_root:       { kind: URL | FS_PATH, value: string }   # ← half of the identity
content_sha256:     "sha256:…"              # ← other half; also the dedup key
publication_date:   { value: "2025-11-02" | null, state: <epistemic_state> }
first_accessed_at:  "2026-09-04T11:40:12Z"
snapshot_asset_id:  AST-…  | null           # stored copy; REQUIRED for class A1/A2/B
language:           "es" | "en" | …
market:             "CL" | "GLOBAL" | null
notes:              string | null
created_at / created_by_run_id

# --- derived, recomputed on every index build (§J.2) ------------------------
owner_relationship: INDEPENDENT | MANUFACTURER | RETAILER | COMPETITOR
                    | USER_GENERATED | UNKNOWN        # DERIVED_DETERMINISTIC
quality_class:      A1 | A2 | B | C | D | E | F       # DERIVED_DETERMINISTIC
quality_class_basis:"regulatory domain + independent publisher"   # DERIVED
policy_ref:         "config/evidence_policy@v4"       # which policy produced the class

# --- derived from the evidence event log ------------------------------------
accessed_at:        [ "2026-09-04T11:40:12Z", "2026-09-11T09:02:44Z" ]
access_count:       2
```

**Two records, identical bytes, different authority — and both survive.** A regulator's copy and a manufacturer's copy of the same PDF share `content_sha256` and differ in `locator_root`, so they are two SOURCE records with two `source_id`s, and they classify A1 and A2 respectively. Under Revision 1's content-only identity the second retrieval would have collapsed into the first and a clinical claim could have inherited the wrong class. Grouping by `content_sha256` still answers "is this the same document?" whenever that is the question being asked.

**Snapshots are not optional for load-bearing classes.** A claim substantiated by a web page that later changes is unfalsifiable without a stored copy. `snapshot_asset_id` is required for A1, A2 and B (INV-20).

### J.2 Source quality — classification is derived, not asserted, and not stored as truth

```
A1  regulator · independent authoritative primary · peer-reviewed primary research
    · accredited third-party lab report
A2  official manufacturer / brand documentation · spec sheet · certificate of analysis
    · official label · official price list
B   trusted secondary · industry body · established publication
C   marketplace listing · verified-purchase review aggregates
D   social discussion · Reddit · TikTok comments · forums
E   competitor advertising claims
F   unattributed · unknown · AI-generated · unresolvable
```

`owner_relationship` and `quality_class` are both **DERIVED_DETERMINISTIC**, computed from `(source_type, locator_root, publisher_declared)` against `evidence_policy`'s publisher registry. Neither is written by a model, neither is stored as an asserted value on the immutable record, and neither is taken from what the source says about itself (INV-105). Phase 1's named failure mode — *"A2 masquerading as A1"* — is prevented structurally: a brand page citing unnamed "studies" resolves to `owner_relationship: MANUFACTURER` from its own domain, so it classifies A2 regardless of its rhetoric.

**Classification corrections are config edits, not record edits.** If a publisher was mis-registered — an independent standards body mistaken for a trade association, say — the fix is one line in `evidence_policy`, and every affected class is recomputed on the next index build. The SOURCE record never changes, so provenance is not rewritten to make a classification convenient. The price is that a policy edit can retroactively change a class: **a claim's verification event records the `policy_ref` under which it was verified** (§J.5), so `rebuild --verify` surfaces any claim whose stored verification no longer holds under current policy, rather than silently re-blessing or silently invalidating it.

**Source quality is purpose-dependent.** There is no global `A > B > C > D` comparison anywhere in the system. The only ordering that exists is *within a claim type*, supplied by the matrix in §J.6. Class D is the **preferred** class for `CUSTOMER_LANGUAGE`.

### J.3 EVIDENCE_EXTRACTION — the E1 record that makes provenance provable

**PURPOSE** — Persist E1's citation-bearing output so that E3's reconciliation is auditable after the fact, and so that "the locator originated in E1" is a checkable statement rather than a claim about the pipeline.
**CANONICAL.** Append-only. Never edited. This record is the *proof*.

```yaml
extraction_id:      EXT-a91c4e-012
run_id / step_id:   RUN-…  /  "E1#012"
source_id:          SRC-4f9a2c81d0b7
model:              "claude-opus-5"
citations_enabled:  true                   # always true; INV-22
schema_enforced:    false                  # always false; INV-22
prose:              "<E1's full text output>"
citation_set:                              # verbatim from the API response
  - { index: 0, cited_text: "…", document_title: "…",
      page_location: { start_page: 4, end_page: 4 } }
  - { index: 1, cited_text: "…", char_location: { start: 8120, end: 8290 } }
quoted_spans:                              # for non-document (web) sources
  - { url: "https://…", quoted_text: "…", retrieved_title: "…",
      accessed_at: "2026-09-04T11:40:12Z" }
created_at
```

### J.4 OBSERVATION

**PURPOSE** — A traceable statement about what was found. Not an interpretation.
**CANONICAL** (the `verbatim`), **DERIVED_GENERATIVE** (the `statement`, produced by E2).
**LIFECYCLE** — Written by E3 after reconciliation. Never edited. Product-scoped.

```yaml
observation_id:     OBS-magnesio-500-0042
source_id:          SRC-…
extraction_id:      EXT-…                  # REQUIRED — the E1 record it came from
locator:
  kind:             PAGE | CHAR_RANGE | SECTION | TIMESTAMP | URL_SPAN
  document_title:   string | null
  page:             int | null
  char_start / char_end: int | null
  section:          string | null
  t_start / t_end:  number | null          # seconds
locator_origin:     E1_CITATION | E1_QUOTE  # REQUIRED, no default; INV-21
verbatim:           "exact quoted text, unmodified"
statement:          "E2's normalised restatement"
subject:            { type: PRODUCT | BRAND | MARKET | COMPETITOR | AUDIENCE,
                      id: PRD-… | BRD-… | null }
kind:               FACT_STATEMENT | CUSTOMER_LANGUAGE | COMPETITOR_CLAIM
                    | MARKET_DATUM | REVIEW_AGGREGATE | REGULATORY_STATEMENT
language / market
customer_language:                          # present only when kind == CUSTOMER_LANGUAGE
  platform:         MARKETPLACE_REVIEW | REDDIT | TIKTOK_COMMENT | FORUM | INSTAGRAM | OTHER
  register:         COLLOQUIAL | NEUTRAL | FORMAL | UNKNOWN
  topic:            string | null
  objection:        string | null
  desire:           string | null
  purchase_stage:   PRE_PURCHASE | POST_PURCHASE | UNKNOWN
  audience_hint:    Fact                    # OBSERVED or UNKNOWN only; INV-24
created_at / created_by_run_id
```

**Verbatim vs model summary is structural, not advisory** (Master Prompt §18). `verbatim` is the exact text E1 cited; `statement` is E2's normalisation. Both are stored, both are indexed separately in FTS, and a `CUSTOMER_LANGUAGE` observation with an empty `verbatim` is rejected (INV-23). Generated Chilean phrasing can therefore never occupy the field that means "a real customer said this".

### J.5 CLAIM

**PURPOSE** — A factual assertion about a subject, with a lifecycle independent of the fields that cite it.
**CANONICAL, immutable.** Product-scoped. The record states *what is asserted*; the event log states *what became of it*.
**LIFECYCLE** — Written once. Every subsequent lifecycle change is an `evidence` log event, and `status` is the fold (§G.0). Folded `UNVERIFIED` until a `CLAIM_STATUS_ASSERTED` event carries `VERIFIED`; `DISPUTED` on a `CLAIM_DISPUTED` event; `SUPERSEDED`/`REJECTED` terminal.

```yaml
claim_id:           CLM-magnesio-500-0007
subject:            { type: PRODUCT|BRAND|MARKET|COMPETITOR, id: PRD-… }
claim_type:         <see §J.6>
statement:          "neutral, non-promotional statement of the assertion"
language:           "es" | "en"
qualification:      "string | null"        # non-null ⇒ REQUIRED wherever the claim is used
evidence_refs:      [ OBS-… ]              # the observations this claim rests on
created_at / created_by_run_id / created_by_step

# --- derived by folding the evidence event log ------------------------------
status:             UNVERIFIED | VERIFIED | DISPUTED | REJECTED | SUPERSEDED
disputed_by:        [ CLM-… ]              # from CLAIM_DISPUTED events
superseded_by:      CLM-… | null           # from CLAIM_SUPERSEDED events
verification:                              # from the latest CLAIM_STATUS_ASSERTED payload
  required_class:   A1
  classes_present:  [ A2 ]
  independent_sources: 1
  required_sources: 1
  result:           INSUFFICIENT_CLASS
  evaluated_by:     "claim-verifier@1.0.0"
  policy_ref:       "config/evidence_policy@v4"
  evaluated_at:     "2026-09-04T13:41:08Z"
```

The events that move a claim:

```yaml
event_type: CLAIM_STATUS_ASSERTED     # by the deterministic verifier only
subject_ref: CLM-magnesio-500-0007
payload: { status: VERIFIED, required_class: A2, classes_present: [A2],
           independent_sources: 1, required_sources: 1, result: SATISFIED,
           evaluated_by: "claim-verifier@1.0.0", policy_ref: "config/evidence_policy@v4" }

event_type: CLAIM_DISPUTED            # ONE event, naming BOTH claims
subject_ref: CLM-magnesio-500-0007
payload: { with: CLM-magnesio-500-0019, basis_observation_refs: [OBS-…, OBS-…],
           note: "sources disagree on concentration" }
```

**Symmetry is no longer a rule to enforce; it is a shape.** Revision 1 stored `disputed_by` on both records and needed INV-25 to keep them in step. One event naming both claims makes an asymmetric dispute **unrepresentable**: the fold cannot produce a state where A disputes B and B does not dispute A, because there is only one fact to fold.

**Fields audited out of the Master Prompt §14 list:**

| Dropped | Why |
|---|---|
| `risk` | Risk is a compliance verdict on a *script line in context*, not a property of a fact. Storing it here would let a claim look "low risk" while the line using it is not. |
| `qualification_required: bool` | Redundant with `qualification != null`. Two fields, one truth, guaranteed to drift. |
| `commercial_use` | Pure function of `claim_type` + `verification.result` + evidence policy. Computed, not stored. |
| `version` | Claims never version. Correction = a new claim plus a `CLAIM_SUPERSEDED` event. |

**Claim status is deliberately not the Fact epistemic enum** (Master Prompt §14). `DISPUTED` has no field-state analogue, and `INFERRED` has no claim analogue — an inference is not a claim, and allowing it to be one is exactly how unsupported product facts enter ads.

### J.6 Claim type × minimum evidence — the policy matrix

`config/evidence_policy.yaml` is **CANONICAL, authored, versioned, hashed into every Run Manifest**. It is data because it must be specialisable by category later without a schema change (§P12).

| `claim_type` | Minimum class | Acceptable | Context-only | Independent sources |
|---|---|---|---|---|
| `PRODUCT_IDENTITY` | A2 | A1, A2 | B, C | 1 |
| `SPECIFICATION` | A2 | A1, A2 | B | 1 |
| `INGREDIENT_LIST` | A2 | A1, A2 | — | 1 |
| `MATERIAL` | A2 | A1, A2 | B | 1 |
| `DIMENSIONS_WEIGHT` | A2 | A1, A2 | B, C | 1 |
| `PRICE` | A2 | A1, A2, C | B | 1 |
| `AVAILABILITY` | A2 | A1, A2, C | B | 1 |
| `MANUFACTURER_STATED_FEATURE` | A2 | A1, A2 | B | 1 |
| `CERTIFICATION_HELD` | A2 (the certificate) | A1, A2 | B | 1 |
| `CATEGORY_FACT` | B | A1, A2, B | C | 1 |
| `MARKET_PERCEPTION` | B | A1, B, C | D | 2 |
| `SCIENTIFIC_MECHANISM` | **A1** | A1 | A2, B | 1 |
| `MEDICAL_EFFICACY` | **A1** | A1 | — | 1 |
| `HEALTH_OUTCOME` | **A1** | A1 | — | 1 |
| `SAFETY` | **A1** | A1 | — | 1 |
| `NUMERIC_PERFORMANCE` | **A1** | A1 | A2 | 1 |
| `COMPARATIVE_SUPERIORITY` | **A1 for both sides** | A1 | — | 2 |
| `DURABILITY_GUARANTEE` | A1, or A2 + test report | A1, A2+LAB | B | 1 |
| `CUSTOMER_TESTIMONIAL` | C (attributable) | C, D | — | 1 |
| `CUSTOMER_LANGUAGE` | **D preferred** | C, D | A2, B, E | 3 |

Reading rules, stated so no one has to infer them:

- **`ACCEPTABLE`** = this class alone can move the claim to `VERIFIED`.
- **`CONTEXT_ONLY`** = may be recorded as an observation supporting the claim, and may appear in a research narrative, but **cannot contribute to verification**. This is the cell that stops a brand PDF substantiating efficacy.
- Class **E** is evidence of *what a competitor asserts*, never of what is true. It is `CONTEXT_ONLY` everywhere, and `ACCEPTABLE` for nothing.
- Class **F** is `ACCEPTABLE` for nothing and `CONTEXT_ONLY` for nothing. An F source may be recorded; it may not support anything.
- `CUSTOMER_LANGUAGE` requiring 3 independent sources is a **register** guard, not a truth guard: one Reddit comment is a person, three converging comments are a way of speaking.

### J.7 The E1 → E2 → E3 lineage in data

```
SOURCE (SRC-…, content_sha256, snapshot_asset_id)
   │
   │  E1: citations ON, schema OFF
   ▼
EVIDENCE_EXTRACTION (EXT-…, citation_set[], quoted_spans[])   ← persisted CANONICAL proof
   │
   │  E2: schema ON, citations OFF, input = EXT record ONLY
   ▼
(candidate observation records, in memory — EPHEMERAL)
   │
   │  E3: deterministic. For each candidate:
   │        locator ∈ EXT.citation_set  (page/char match)         else REJECT
   │        verbatim ⊆ some EXT.cited_text | quoted_text          else REJECT
   │        locator_origin set from which set matched              else REJECT
   ▼
OBSERVATION (OBS-…, extraction_id → EXT-…, locator_origin)
   │
   ▼
CLAIM (CLM-…, evidence_refs → OBS-…, verification computed from policy)
```

**How the data proves the locator originated in E1:** every OBSERVATION carries `extraction_id`, and the EXTRACTION record carries the raw `citation_set`. An auditor — or a CI check — re-runs the set-membership test at any later date without a model. `locator_origin` records which set matched. An observation with no resolvable `extraction_id` cannot exist (INV-21), and an extraction record is never edited.

**What is deliberately *not* stored:** raw API response envelopes, `document_index` (an artefact of the request's document ordering, meaningless later), token usage per citation, and any model reasoning. `document_title` and the location object are normalised into `locator`; everything else stays out of the domain model (Master Prompt §13).

### J.8 Ledger invariants

INV-18 an OBSERVATION's `source_id` must equal its EXTRACTION's `source_id`. INV-19 a folded `status: VERIFIED` requires a `CLAIM_STATUS_ASSERTED` event whose payload carries `result: SATISFIED` and a named `policy_ref`. INV-20 a SOURCE deriving to class A1/A2/B must have `snapshot_asset_id`. INV-21 `locator_origin` is required and `extraction_id` must resolve. INV-22 an EXTRACTION with `schema_enforced: true` or `citations_enabled: false` is invalid. INV-23 `kind: CUSTOMER_LANGUAGE` requires non-empty `verbatim`. INV-24 `customer_language.audience_hint.state ∈ {OBSERVED, UNKNOWN, NOT_COLLECTED}`. INV-25 a dispute is recorded as a single `CLAIM_DISPUTED` event naming both claims; the fold sets `DISPUTED` on both, and an asymmetric dispute is unrepresentable. INV-26 a `DISPUTED`, `UNVERIFIED`, `REJECTED` or `SUPERSEDED` claim may not bind to a script line. INV-104 `source_id` is deterministic over `(locator_root, content_sha256)`; two records sharing `content_sha256` with different `locator_root` are distinct and both retained. INV-105 `owner_relationship` and `quality_class` are derived on every build from the record plus the pinned evidence policy, and are never accepted as written values.

---

## K. Research Dossier Schema

**PURPOSE** — Everything the system learned about the market, the audience and the competitive field for this campaign, plus the interpretations built on it.
**CANONICAL OR DERIVED** — `DERIVED_GENERATIVE` throughout, except `observation_refs[]` which are `CANONICAL` references and `spread` counts which are `DERIVED_DETERMINISTIC`.
**OWNING COMPONENT** — `market-intelligence-cl` Skill (research, customer language) and `creative-strategist` Skill (audience model, persuasion projection, insights).
**LIFECYCLE** — Built in Phase II after Gate 1. Re-versioned when research is widened (the default resolution for an unmet diversity target, Phase 1 §Q).
**IDENTIFIER** — `(campaign_id, research_dossier, version)`.
**VERSIONING RULE** — New version on any change. Because insights live here, a new dossier version invalidates nothing automatically — hypotheses pin the version they used.

### K.1 What lives inside vs outside

| Element | Where | Why |
|---|---|---|
| **Brand Snapshot** | **Product Truth** (§I.1) | Same procedure, same shape, produced pre-Gate-1 |
| **Market Snapshot** | Embedded, `Fact`-shaped | Campaign-scoped; no independent consumer |
| **Audience Model** | Embedded, one object | §L |
| **Persuasion Context** | Embedded as a *projection* of the Audience Model | §L.2 — one canonical object, one strategic projection |
| **Customer Language Corpus** | **Outside** — OBSERVATION records, referenced | Grows across campaigns; needs FTS; is evidence, not interpretation |
| **Competitor observations** | **Outside** — OBSERVATION records, referenced | Same reason |
| **Objections / desires / beliefs / alternatives / awareness / sophistication** | Fields of the Audience Model | They are dimensions of one audience, not twelve documents |
| **Insights** | Embedded, addressable by `INSIGHT_ID` | Born here, consumed by hypotheses, meaningless alone |

**This is the answer to Master Prompt §17's warning**: twelve sections do not become twelve files. They become two embedded objects, one embedded addressable list, and two reference lists into the ledger.

### K.2 Shape

```yaml
campaign_id / product_id / version-block

market_snapshot:                        # Fact-shaped
  market: "CL"
  category_size_signal / growth_signal / seasonality / price_range
  distribution_channels / regulatory_context / cultural_context

competitive_field:
  competitor_observation_refs: [ OBS-… ]      # kind: COMPETITOR_CLAIM
  observed_positioning: [ { competitor, positioning: Fact, refs: [OBS-…] } ]
  observed_claim_territories: [ CLAIM_TERRITORY ]   # what competitors are claiming
  saturation_signal: Fact                     # feeds sophistication, never assumed

customer_language:
  observation_refs: [ OBS-… ]                 # kind: CUSTOMER_LANGUAGE
  spread:                                     # DERIVED_DETERMINISTIC counts
    total: 61
    by_platform:      { MARKETPLACE_REVIEW: 28, REDDIT: 11, TIKTOK_COMMENT: 22 }
    by_purchase_stage:{ PRE_PURCHASE: 24, POST_PURCHASE: 30, UNKNOWN: 7 }
    distinct_sources: 9

audience_model:      <§L.1>
persuasion_projection: <§L.2>

insights:
  - insight_id:      INS-acme-3f8b21-004
    domain:          PRODUCT | MARKET | AUDIENCE | COMPETITOR | LANGUAGE
    statement:       "the interpretation"
    basis_observation_refs: [ OBS-… ]         # ≥ 1 REQUIRED
    reasoning:       "why the observations support this reading"
    counter_evidence_refs: [ OBS-… ]          # observations that cut against it
    basis:                                    # DERIVED_DETERMINISTIC — measured, not graded
      observation_count:      4
      distinct_source_count:  3
      source_classes_present: [ B, C, D ]
      counter_evidence_count: 1
research_gaps:
  - { dimension: "core_problem", note: "only two distinct problems evidenced",
      observation_count: 61, distinct_problems_evidenced: 2 }
```

### K.3 Insight rules

**`strength: DIRECT | INDIRECT` is removed.** Revision 1 defined `DIRECT` as *"≥ 2 basis observations from ≥ 2 distinct sources"*, which is a source count wearing the costume of an evidential judgement. It is wrong in both directions: one regulator statement (class A1) can support a direct reading, and two loosely-worded social comments (class D) do not become strong by being two. A count that determines a grade is an evidence score, and §54 forbids exactly that.

What replaces it is what was actually being counted, stated as counts and left uninterpreted:

| Field | Meaning |
|---|---|
| `observation_count` | How many observations the reading rests on |
| `distinct_source_count` | How many independent sources those came from |
| `source_classes_present` | Which evidence classes are in the basis — the field that carries authority |
| `counter_evidence_count` | How many observations cut against it |

A reviewer at Gate 2 reads `{observation_count: 1, distinct_source_count: 1, source_classes_present: [A1]}` and understands it differently from `{observation_count: 6, distinct_source_count: 4, source_classes_present: [D]}`, and neither the solver nor a model has pre-decided which is stronger. Where the *system* needs an authority judgement it uses the claim-type matrix (§J.6), which is class-aware and purpose-specific — not a count.

INV-27 an INSIGHT with an empty `basis_observation_refs` is invalid — this is the mechanism that makes Phase 1 §N's "Observation → Insight" promotion rule structural. INV-28 `statement` and `reasoning` are separate fields, and `statement` may not simply restate a single observation's `verbatim` — an insight that is a quote is an observation. INV-29 an insight records `observation_count`, `distinct_source_count`, `source_classes_present` and `counter_evidence_count`, all computed deterministically from its refs; **no strength grade, tier or score is stored on an insight**, and no field may be derived from a raw count alone.

`research_gaps[]` is written by a **deterministic** counter over the observation set, not by the Skill. It is the input to the diversity solver's `INSUFFICIENT_EVIDENCE_FOR_DIVERSITY_TARGET` finding, and it exists so that a thin evidence base is a recorded finding rather than an inference someone makes later.

---

## L. Audience / Persuasion Schema

### L.1 Audience Model — one object, evidence-linked

**CANONICAL OR DERIVED** — `DERIVED_GENERATIVE`; every field is a `Fact`, so every field is either evidence-linked or explicitly `UNKNOWN`.
**OWNING COMPONENT** — `creative-strategist`, one pass (Phase 1 §G.1 merges §40's six stages into this).

```yaml
audience_model:
  label:                "primary"            # V1 has exactly one; see §L.3
  problem:
    surface_problem:    Fact<string>
    deep_problem:       Fact<string>
  desire:
    functional_desire:  Fact<string>
    emotional_desire:   Fact<string>
    identity_desire:    Fact<string>
  friction:
    fear:               Fact<string>
    frustration:        Fact<string>
    objections:         Fact<list[string]>
  belief:
    current_belief:     Fact<string>
    desired_belief:     Fact<string>
  landscape:
    alternatives:       Fact<list[string]>   # incl. "do nothing"
    awareness_state:    Fact<AWARENESS_STATE>
    sophistication_state: Fact<SOPHISTICATION_STATE>
  context:
    purchase_context:   Fact<string>
    usage_context:      Fact<string>
  sensitive:                                 # OBSERVED | UNKNOWN | NOT_COLLECTED only
    life_stage_signal:  Fact<string>
```

**Enums**

```
AWARENESS_STATE        UNAWARE | PROBLEM_AWARE | SOLUTION_AWARE | PRODUCT_AWARE | MOST_AWARE
SOPHISTICATION_STATE   STAGE_1 | STAGE_2 | STAGE_3 | STAGE_4 | STAGE_5
```

**Rules.**

**INV-30 (revised).** `awareness_state` and `sophistication_state` may hold `state: INFERRED` **only with non-empty `refs` and a `note` naming the observations and the inferential step.** A bare inference on these two fields — `INFERRED` with empty `refs` — is schema-invalid (INV-112).

Revision 1 forbade `INFERRED` outright here, and that over-corrected. Phase 1 §E quotes the framework's actual rule: *"Do not infer sophistication merely from category age."* The word doing the work is **merely**. Awareness and sophistication are almost never *observed* in the way a label's text is observed — they are read off competitor claim density, review vocabulary, and how much explanation buyers demand. Forcing that reading into `OBSERVED` would have mislabelled an interpretation as a fact, and forcing it into `UNKNOWN` would have thrown away the best evidence the research produced. The rule that matters is **no stereotype-only inference**, and requiring a cited basis expresses exactly that: category age alone leaves `refs` empty, so it is refused.

An `INFERRED` awareness or sophistication state remains an interpretation everywhere it is consumed: it cannot substantiate a claim (F-R6), it does not raise the claim-freedom tier, and it is surfaced as such in the Gate 1 and Gate 2 renders so a reviewer can disagree with the reading rather than with a number.

**INV-31.** No field may encode ethnicity, religion, health status, sexual orientation, disability or precise age of the audience; `sensitive.*` accepts only broad life-stage signals and only when observed. F-R3's relaxation does **not** reach these fields (F-R7): no basis makes a sensitive-attribute inference acceptable.

### L.2 Persuasion projection — strategy, not evidence

Master Prompt §20 asks whether Schwartz fields overlap the Audience Model. They do, by roughly 70 % (Phase 1 §G.2). The resolution is a strict split:

> **Evidence fields live in the Audience Model exactly once. The projection holds only fields that are choices.**

```yaml
persuasion_projection:                       # DERIVED_GENERATIVE — strategic descriptors
  mass_desire_ref:        "audience_model.desire.emotional_desire"   # a POINTER, not a copy
  awareness_ref:          "audience_model.landscape.awareness_state"
  sophistication_ref:     "audience_model.landscape.sophistication_state"
  identification_strategy: MIRROR | ASPIRATION | SHARED_ENEMY | INSIDER_KNOWLEDGE | NONE
  mechanism_depth:         NONE | NAMED | EXPLAINED | DIFFERENTIATED
  promise_strategy:        DIRECT | INTENSIFIED | REDEFINED | DEFERRED
  reason_to_believe_strategy: DEMONSTRATION | COMPOSITION | AUTHORITY | SOCIAL_PROOF
                            | MECHANISM | NONE_AVAILABLE
  intensification_devices: [ CONCRETENESS | SPECIFICITY | SENSORY | CONTRAST | STAKES ]
  rationale:               "written, one paragraph"
```

`mass_desire`, `awareness_state`, `sophistication_state`, `current_belief` and `desired_belief` appear **as internal pointers, never as duplicated values**. There is therefore no way for the strategic layer to hold a different awareness state than the evidence layer — the failure Phase 1 §G.2 predicts when six sequential passes each restate the last.

INV-32 every `*_ref` in the projection resolves to a field of the same dossier version. INV-33 `mechanism_depth != NONE` requires the Product Truth tier to permit `MECHANISM_EXPLANATION`. INV-34 `reason_to_believe_strategy` must be `NONE_AVAILABLE` when no `VERIFIED` claim exists that the tier permits — the schema refuses to let a strategy assert proof the evidence layer does not have.

### L.3 Why one audience model in V1

The Master Prompt does not ask for segments and the diversity mechanism operates on hypothesis dimensions, not on audience segments. Introducing `segments[]` now would add a scoping dimension to every downstream reference for a capability nothing currently uses. The field `label` exists so that `segments[]` becomes an additive change (a list of the current object) rather than a restructuring. **Deferred, not designed out.**

---

## M. Hypothesis Pool Schema

**PURPOSE** — 20–30 falsifiable expectations, each traceable to evidence and each carrying the dimensional vector the rest of the pipeline depends on.
**CANONICAL OR DERIVED** — `DERIVED_GENERATIVE`, except `dimensions` (generative but constrained to registry values), `basis` refs (canonical references) and `prescreen` (deterministic + generative, see §U).
**OWNING COMPONENT** — `creative-strategist` via the Batch API (Phase 1 ADR-007).
**LIFECYCLE** — Generated once per campaign; hypotheses gain `status` as the compliance pre-screen and the diversity solver run. Re-versioned if the pool is regenerated after widened research.
**IDENTIFIER** — `(campaign_id, hypothesis_pool, version)`; each entry has a `HYPOTHESIS_ID`.

### M.1 Shape

```yaml
hypothesis_pool:
  campaign_id / version-block
  target_size: 25
  hypotheses:
    - hypothesis_id:    HYP-acme-3f8b21-017
      statement:        "If <audience/context>, then <predicted effect>, because <reason>."
      dimensions:                                   # ← the vector that travels the pipeline
        awareness_state:          PROBLEM_AWARE
        core_problem:             "…"               # free text, but see §M.3
        dominant_desire:          "…"
        current_belief:           "…"
        angle_mechanism:          MECHANISM | IDENTITY | CONTRAST | DEMONSTRATION
                                  | ORIGIN | OBJECTION_REFRAME | SITUATIONAL | PROOF
        psychological_hypothesis: <registry value from creative_taxonomy>
      predicted_effect:   "what we expect to observe, in creative-performance terms"
      falsification_condition: "what result would weaken or refute this"   # REQUIRED
      basis:
        insight_refs:      [ INS-acme-3f8b21-004 ]
        observation_refs:  [ OBS-magnesio-500-0042 ]   # ≥1 across the two lists
      claim_dependencies:  [ CLM-magnesio-500-0007 ]   # claims this argument would need
      required_territories:[ PROBLEM_CONTEXT, SITUATIONAL_NARRATIVE ]
      candidate_formats:   [ UGC, ANIMATION ]
      status:              CANDIDATE | SELECTED | REJECTED | DEFERRED
      rejection:           { reason_code, note } | null
      prescreen:           <§U.4>
  spread:                                            # DERIVED_DETERMINISTIC
    distinct: { awareness_state: 4, core_problem: 2, dominant_desire: 3,
                current_belief: 3, angle_mechanism: 5, psychological_hypothesis: 6 }
    cluster_warning: true                            # set when any dimension < target
```

### M.2 Audited out of the Master Prompt §21 list

| Dropped | Why |
|---|---|
| `segment` | The V1 Audience Model is singular (§L.3). Reintroduce with segments. |
| `counter_hypothesis` | Overlaps `falsification_condition` in practice and is rarely actionable at V1 scale. A rival explanation that matters belongs in `confounders_known` on the experiment, where it can be acted on. |
| `problem` / `desire` / `belief` / `awareness` / `angle` as separate top-level fields | Consolidated into `dimensions`, which is exactly the same information in the shape the solver, the duplicate detector and the future performance join all need. |
| `risk` | Duplicates `prescreen.verdict`. |
| `possible_formats` (as free text) | Became `candidate_formats`, validated against the format registry. |

**Kept and made mandatory:** `falsification_condition`. Phase 1 §N is explicit — *"No falsifier ⇒ not a hypothesis."* INV-35 enforces it, and it is the one field that most reliably separates a hypothesis from an opinion.

**Added:** `claim_dependencies[]` and `required_territories[]`. These make the compliance pre-screen (flow step 11) genuinely cheap: a hypothesis requiring `OUTCOME_PROMISE` under a T1 tier is rejected mechanically, before anything is written, at zero model cost.

### M.3 `core_problem` and `dominant_desire` are free text — deliberately

These cannot be a fixed registry: the whole point of research is to discover which problems exist in *this* market for *this* product. Making them an enum would force the strategist to map real findings onto pre-existing buckets, which is a quieter form of the fabrication §C.17 forbids.

The consequence is that "distinct values" needs a definition for the spread count. **Rule:** two hypotheses share a `core_problem` value when their normalised strings are equal (lowercased, accent-folded, whitespace-collapsed) **or** when the strategist explicitly links them via `core_problem_group` — an optional field the strategist may set to declare "these are the same problem stated differently". Counting is then deterministic, and the judgement of sameness is recorded rather than inferred by a matcher.

### M.4 Invariants

INV-35 `falsification_condition` is non-empty. INV-36 `basis.insight_refs` ∪ `basis.observation_refs` is non-empty. INV-37 every `claim_dependencies[]` entry resolves to an existing CLAIM (any status — a hypothesis may depend on a claim that is not yet verified; that is what the pre-screen surfaces). INV-38 `dimensions.psychological_hypothesis` and `angle_mechanism` are values from `creative_taxonomy` (§B.1). INV-39 `status: SELECTED` requires exactly one CONCEPT referencing this hypothesis.

---

## N. Concept Representation

**PURPOSE** — A selected hypothesis developed into a complete strategic idea, such that two creators executing it would produce recognisably the same argument (Phase 1 §O).
**CANONICAL OR DERIVED** — `DERIVED_GENERATIVE`, except `dimensions` (inherited, immutable) and `evidence_refs` (canonical references).
**OWNING COMPONENT** — `creative-strategist`.
**LIFECYCLE** — Created for each of the 10 selected hypotheses. Embedded in the Experiment Plan. Approved at Gate 2.
**IDENTIFIER** — `CONCEPT_ID`, addressed as `CMP-…/experiment_plan@v3#concepts[CON-acme-3f8b21-03]`.

```yaml
concept_id:          CON-acme-3f8b21-03
hypothesis_id:       HYP-acme-3f8b21-017          # 1:1, immutable
dimensions:          <inherited verbatim from the hypothesis; INV-40>
core_message:        "the single argument, one or two sentences"
promise:             "what the audience gets"
reason_to_believe:
  statement:         "why they should believe it"
  claim_refs:        [ CLM-… ]                 # ≥1 unless strategy is NONE_AVAILABLE
  territory:         COMPOSITION_STATEMENT     # must be in permitted_territories
product_role:        HERO | ENABLER | PROOF | BACKGROUND | ABSENT_UNTIL_RESOLUTION
belief_bridge:
  from:              "current belief"          # pointer-compatible with audience_model
  to:                "desired belief"
  via:               "the move that gets from one to the other"
format_fit:          [ { format: UGC, fit: STRONG|WORKABLE|POOR, note } ]
narrative_fit:       [ { narrative_pattern_id: NAR-confession,
                         fit: STRONG|WORKABLE|POOR, note } ]
evidence_refs:       [ OBS-…, INS-… ]
required_territories:[ CLAIM_TERRITORY ]       # DERIVED from the message + RTB
selection_status:    SELECTED | ALTERNATE | REJECTED
selection_rationale: "why this one, written by the strategist"
prescreen:           <§U.4>
```

**Concept is not Hypothesis** — the hypothesis states a testable expectation; the concept states the argument that would test it. **Concept is not Creative** — the concept is format-agnostic (it lists fits, it does not choose), while the creative commits to one format, one narrative pattern, one style and one script.

INV-40 `dimensions` is byte-identical to the source hypothesis's. If the argument requires different dimensions, it is a different hypothesis — the discriminator Phase 1 §O gives for Hook vs Concept applies here too. INV-41 `reason_to_believe.territory` ∈ `claim_freedom.permitted_territories`. INV-42 every `claim_refs[]` entry has `status: VERIFIED` at Gate 2, or the concept carries an explicit `prescreen.blocking_gap` naming the missing evidence. INV-43 `format_fit` may not be empty and must contain at least one `STRONG` or `WORKABLE` entry for a format present in the campaign's `format_mix`.

**No `risk` field.** Concept-level risk is the pre-screen verdict; duplicating it invites the two to disagree.

---

## O. Experiment Plan Schema

**PURPOSE** — The artefact Gate 2 approves: which ten concepts, why those ten, what is being tested, and what is held constant.
**CANONICAL OR DERIVED** — `concepts[]` are `DERIVED_GENERATIVE`; `diversity_audit` is `DERIVED_DETERMINISTIC`; `experiment_designs[]` are `DERIVED_DETERMINISTIC` in structure and `DERIVED_GENERATIVE` in `rationale`.
**OWNING COMPONENT** — Diversity solver (service) + Experiment Designer (orchestrator step + deterministic validator, Phase 1 ADR-023).
**LIFECYCLE** — Assembled after the hypothesis pool. Approved at Gate 2. **Never re-versioned to record what happened after Gate 2** — binding and validation live outside it (§O.6).
**IDENTIFIER** — `(campaign_id, experiment_plan, version)`.

### O.1 The forward-reference problem, and the split that fixes it

Revision 1 put `creative_id` and `locked_variable_values` inside the arms of an artefact approved at Gate 2 — and creatives are not written until Phase IV, *after* Gate 2. Its own walkthrough admitted it: *"creative_ids assigned in Phase IV."* That is a forward reference into an approved, hashed, immutable artefact, and there were only two ways to honour it, both bad: mutate the thing a human signed (destroying the hash binding), or re-version it (making the Gate 2 approval cover a version that no longer exists).

The split is between **what is decided** and **what is later true**:

| | **EXPERIMENT DESIGN** | **EXPERIMENT BINDING + LOCK VALIDATION** |
|---|---|---|
| Lives in | Experiment Plan (artefact, Gate 2) | Derived projection (§O.6) + `experiment.arm_binding` on each Creative |
| Contains | Hypotheses, scope, declared variable, locked variables, arms as `concept_id` + `creative_slot_key` + planned value, measurement plan, known confounders | `arm_key → creative_id@version`, the **actual** locked-variable values extracted from those creatives, the validation result |
| Exists at | Gate 2 | After Phase IV |
| Approved by | Gate 2 | Reviewed at Gate 3 as part of the release evidence |
| Mutable? | No — immutable artefact version | No — recomputed from creatives on demand |

Gate 2 therefore approves a **design**: *"we will test hook copy across two UGC creatives built from concept CON-…-03, holding these twelve variables constant."* That is a complete, reviewable, falsifiable statement, and it is entirely expressible without knowing which creative ends up in which arm.

### O.2 Shape

```yaml
experiment_plan:
  campaign_id / version-block
  concepts:        [ <§N> ]                          # the 10 selected, embedded
  alternates:      [ CON-… ]                         # ranked, for Gate 2 swaps
  creative_slots:                                    # what Phase IV must produce
    - { creative_slot_key: "slot-01", concept_id: CON-acme-3f8b21-03, format: UGC }
    - { creative_slot_key: "slot-02", concept_id: CON-acme-3f8b21-03, format: UGC }
    - …                                              # exactly batch.size slots
  diversity_audit: <§O.5>
  experiment_designs:
    - experiment_id:      EXP-acme-3f8b21-01
      hypothesis_ids:     [ HYP-acme-3f8b21-017, HYP-acme-3f8b21-022 ]
      scope:                                        # REQUIRED at design time
        product_id / category / market / audience_label / format / period_planned
      declared_variable:  HOOK_COPY
      locked_variables:   [ FORMAT, NARRATIVE_PATTERN, STYLE, AWARENESS_STATE,
                            ANGLE_MECHANISM, CORE_MESSAGE, PROMISE, RTB, OFFER,
                            DURATION_BAND, CTA_TYPE, VOICE_SPECIFICATION ]
      arms:
        - arm_key:                "a1"
          concept_id:             CON-acme-3f8b21-03
          creative_slot_key:      "slot-01"          # ← a promise, not a reference
          role:                   CONTROL | VARIANT
          planned_variable_value: "hook copy variant A — question-led"
        - arm_key:                "a2"
          concept_id:             CON-acme-3f8b21-03
          creative_slot_key:      "slot-02"
          role:                   VARIANT
          planned_variable_value: "hook copy variant B — confession-led"
      measurement_plan:
        primary_metric:    { name, numerator, denominator, source }   # §AB.3
        guardrail_metrics: [ { name, numerator, denominator, source } ]
        minimum_exposure:  { kind: IMPRESSIONS|SPEND|DAYS, value }
        decision_rule:     "written, unambiguous"
        planned_duration_days: 14
      confounders_known:  [ "Meta delivery optimisation allocates unevenly across ads
                             in one ad set (Phase 1 §P)" ]            # REQUIRED
      rationale:          "why this comparison is worth making"
```

**Four fields are now schema-invalid inside an Experiment Plan** (INV-106): `creative_id`, `locked_variable_values`, `lock_validation`, `evidence_level`. Each of them is a statement about something that does not exist when the plan is written — the first two about creatives, the third about a check that cannot run yet, the fourth about a result that arrives months later. Forbidding them at the schema level is what makes the forward reference impossible rather than merely discouraged.

`creative_slots[]` is a local-key list, not an identifier type: a slot is a promise the plan makes about what Phase IV will produce, and it dies with the plan version.

### O.3 The experiment-variable registry

`locked_variables[]` and `declared_variable` name dimensions from a registry, and each dimension resolves to a **specific field path on the Creative Record**, declared in `experiment_variables`:

```yaml
FORMAT:            execution.format
NARRATIVE_PATTERN: execution.narrative_pattern_id
STYLE:             execution.style_id
AWARENESS_STATE:   strategy.dimensions.awareness_state
HOOK_COPY:         hook.copy.text
CORE_MESSAGE:      strategy.core_message
DURATION_BAND:     execution.duration_band
CTA_TYPE:          script.cta.kind
OFFER:             strategy.offer_ref
```

Adding a testable variable is a config edit, not a schema migration (§P12). `declared_variable` and `locked_variables` are drawn from the same registry, and INV-44 requires them to be disjoint and to jointly cover every field path the registry declares — **"everything else is the same" is never implied; it is enumerated or the plan is invalid.** This check runs at Gate 2, because it needs only the registry and the design.

The field paths are also what makes the later extraction mechanical rather than interpretive (§O.6): the validator reads `execution.narrative_pattern_id` off each bound Creative Record. It never asks anything what it held constant.

### O.4 Variant — no separate object

Master Prompt §36 asks whether Variant needs an ID. **It does not.** A variant *is* `(creative_id, experiment_id, arm_key, planned_variable_value)`. The arm records what should differ, the binding records which creative filled it, and the lock validation proves what did not differ. Minting a `VARIANT_ID` would create a fourth place where "what changed" is recorded, and the fourth place would eventually disagree with the other three.
### O.5 Diversity model

**CANONICAL OR DERIVED** — `DERIVED_DETERMINISTIC` in full. No part of the diversity audit is written by a model.

```yaml
diversity_audit:
  status:  SATISFIED | INSUFFICIENT_EVIDENCE_FOR_DIVERSITY_TARGET | VALIDATION_FAILURE
  hard_constraints:
    - { id: FORMAT_MIX,          result: PASS|FAIL, detail: { required: {...}, achieved: {...} } }
    - { id: NO_NEAR_DUPLICATE,   result: PASS|FAIL, detail: { flagged_pairs: [...] } }
    - { id: WITHIN_CLAIM_TIER,   result: PASS|FAIL, detail: { violations: [CON-…] } }
    - { id: PRESCREEN_PASSED,    result: PASS|FAIL, detail: { blocked: [CON-…] } }
    - { id: TRACEABLE_PROVENANCE,result: PASS|FAIL, detail: { untraceable: [CON-…] } }
    - { id: FEASIBILITY_CEILING, result: PASS|FAIL, detail: { over_ceiling: [CON-…] } }
  diversity_targets:
    - dimension:        core_problem
      target:           4
      achieved:         2
      achieved_values:  [ "EXAMPLE_ONLY_A", "EXAMPLE_ONLY_B" ]
      met:              false
      limiting_factor:  "only 2 distinct core problems evidenced in research"
      supporting_observation_ids: [ OBS-…, OBS-… ]
      research_gap_ref: "research_dossier@v2#research_gaps[0]"
    - dimension: awareness_state
      target: 3  achieved: 4  achieved_values: [...]  met: true
      limiting_factor: null  supporting_observation_ids: [...]  research_gap_ref: null
  unmet_targets:      [ core_problem ]
  near_duplicate_pairs:
    - { pair: [CON-acme-3f8b21-03, CON-acme-3f8b21-08], shared_count: 4,
        shared_dimensions: [core_problem, dominant_desire, current_belief, angle_mechanism] }
  computed_by:        "diversity-solver@1.0.0"

# resolution is NOT stored here — it is derived from the Gate 2 decision (§V, Correction 6)
resolution:                                    # DERIVED_DETERMINISTIC from the gate log
  chosen:           ADDITIONAL_RESEARCH | RELAX_TARGET | REDUCE_BATCH_DIVERSITY
                    | REDUCE_BATCH_SIZE | null
  decided_at_gate:  GAT-acme-3f8b21-002 | null
  human_override_reason: "string | null"       # from the gate override's `reason`
```

**`resolution` moved out of the artefact.** Revision 1 stored the operator's chosen resolution inside the plan, which meant a Gate 2 relaxation changed the bytes of the artefact Gate 2 was approving — the circularity Correction 6 forbids. The resolution now lives where the decision lives: in the `GATE_DECISION`'s `overrides[]`. The plan states the *finding*; the gate states the *response*; the fold joins them. A diversity relaxation is therefore byte-neutral and can be recorded as `APPROVED_WITH_OVERRIDES` in a single decision, with no second gate round-trip.

**The two statuses that must never be confused:**

| Status | Meaning | Who resolves | Blocks Gate 2? |
|---|---|---|---|
| `VALIDATION_FAILURE` | A **hard constraint** failed. Format mix wrong, a concept outside the claim tier, a concept with no traceable provenance, a pre-screen block. | The system, by changing the selection — never by inventing evidence | Yes, and it is a `HARD_BLOCK` |
| `INSUFFICIENT_EVIDENCE_FOR_DIVERSITY_TARGET` | Every hard constraint passed. One or more **targets** could not be met because the evidence base does not contain that much distinct material. | A human at Gate 2, choosing one of four recorded options | No — it is surfaced as a decision, not a failure |

This is the data expression of Phase 1 §C.17. The solver has no field it can write to make an unmet target go away, and `achieved_values[]` plus `supporting_observation_ids[]` mean the operator can see exactly which two problems the research actually evidenced. `human_override_reason` is required for `RELAX_TARGET`, and the whole audit is copied into the Run Manifest so a later analysis can tell a genuinely diverse batch from a diverse-by-relaxation one (Phase 1 §Q).

INV-50 `status: SATISFIED` requires every hard constraint `PASS` and every target `met: true`. INV-51 a derived `resolution.chosen == RELAX_TARGET` requires a Gate 2 `overrides[]` entry of kind `DIVERSITY_TARGET_RELAXATION` with a non-empty `reason`; the resolution is never stored in the plan. INV-52 no field of `diversity_audit` may be written by a generative step.

### O.6 Experiment binding and lock validation

**CANONICAL OR DERIVED** — the binding *declaration* is `CANONICAL`, recorded on the Creative Record; the *resolution and validation* are `DERIVED_DETERMINISTIC`, recomputed on demand. **No new artefact and no new identifier.**

The audit's constraint was to represent the binding as data on an existing object or as a derived record, not as a ninth artefact. Both halves are used, each for what it is:

**1. The declaration lives on the Creative Record.** A creative states which slot it fills; that is a fact about the creative, known when it is written, and it belongs in the artefact whose lineage it is part of:

```yaml
# creative_record.experiment
experiment:
  experiment_id:      EXP-acme-3f8b21-01 | null    # null for creatives outside any experiment
  arm_key:            "a1" | null
  creative_slot_key:  "slot-01"
  role:               CONTROL | VARIANT | null
  plan_ref:           { ref: "CMP-acme-3f8b21/experiment_plan@v1", hash: "sha256:…" }
```

`plan_ref` pins the exact plan version the creative was built against, so a creative can never be silently re-attributed to a different design.

**2. The resolution and the check are a derived projection**, keyed by `(experiment_id, arm_key)`, computed by scanning creatives for their declarations:

```yaml
experiment_binding:                             # DERIVED_DETERMINISTIC — never stored canonically
  experiment_id:    EXP-acme-3f8b21-01
  plan_ref:         "CMP-acme-3f8b21/experiment_plan@v1"
  bound_at:         "2026-09-04T18:22:00Z"
  validator_version:"lock-validator@1.0.0"
  arms:
    - arm_key:          "a1"
      creative_slot_key:"slot-01"
      bound_creative:   { ref: "CRE-acme-3f8b21-07@v3", hash: "sha256:…" }
      actual_variable_value: "hook copy variant A — question-led"
      locked_variable_values:                   # EXTRACTED from the creative, per §O.3 paths
        FORMAT: UGC
        NARRATIVE_PATTERN: NAR-confession
        STYLE: STY-ugc-raw-handheld
        AWARENESS_STATE: PROBLEM_AWARE
    - arm_key: "a2" …
  binding_result:   COMPLETE | INCOMPLETE       # every arm bound exactly once?
  unbound_arms:     [ ]
  lock_validation:
    result:         SATISFIED | LOCK_VIOLATION
    violations:     [ { variable: NARRATIVE_PATTERN,
                        values: { a1: NAR-confession, a2: NAR-storytime } } ]
  declared_variable_actually_differs: true       # the mirror check — see below
```

The validation itself:

```
for v in design.locked_variables:
    values = { binding.arms[a].locked_variable_values[v] for a in arms }
    if len(values) != 1:  → LOCK_VIOLATION   (HARD_BLOCK on release)

d = design.declared_variable
if len({ arms[a].locked_variable_values_of(d) }) == 1:
    → declared_variable_actually_differs = false   (the experiment tests nothing)
```

Two properties make this real rather than aspirational. The values are **extracted from the Creative Records** by field path, so nothing can assert a lock it did not honour. And the mirror check — that the *declared* variable actually varies — catches the opposite failure, an "experiment" whose arms are identical, which Revision 1 could not detect at all.

**When it runs and what it blocks.** Binding is computed at the end of Phase IV and re-computed whenever a bound creative is re-versioned. A `LOCK_VIOLATION` is a **`HARD_BLOCK` on release** (INV-108) — not on Gate 2 approval, which happened before any creative existed. It is surfaced in the Gate 3 review alongside the packages, because Gate 3 is the first human checkpoint at which the question *"did we actually hold constant what we said we would?"* has an answer.

**Nothing mutates.** The Gate-2-approved Experiment Plan is untouched by any of this. If a violation must be fixed, the fix is a new **Creative** version — changing the creative that broke the lock — not an edit to the design a human signed.

### O.7 Invariants

INV-44 `declared_variable ∉ locked_variables`, and `{declared} ∪ locked` covers the full experiment-variable registry. Checked at Gate 2. INV-45 `evidence_level` is never stored on a design; it is assigned only when the folded experiment state is `ANALYZED`. INV-46 `scope` is non-null on every experiment design. INV-47 `confounders_known` is non-empty (the delivery-optimisation confounder is inserted by default and may be added to, never removed). INV-48 *(revised)* in a binding, each `creative_id` appears in at most one arm across the whole campaign, and each arm binds at most one creative. INV-49 *(revised)* `lock_validation.result == LOCK_VIOLATION` is a `HARD_BLOCK` on **release**, and prevents the folded experiment state reaching `LOCK_VALIDATED`. INV-106 an Experiment Plan version containing `creative_id`, `locked_variable_values`, `lock_validation` or `evidence_level` is schema-invalid. INV-107 every arm resolves `arm_key → creative_id@version` exactly once; `binding_result: INCOMPLETE` blocks release of any package in that experiment. INV-108 lock validation runs on bound creatives, never on the design.

---

## P. Creative Record Schema

**PURPOSE** — The complete strategic and creative representation of one execution. Phase 1 §Y collapsed thirteen proposed artefacts into this one object, so it must consolidate without becoming a flat five-thousand-field monolith.
**CANONICAL OR DERIVED** — Mixed, section by section; the table below labels each.
**OWNING COMPONENT** — `script-engine` Skill (strategy→visual_plan), Creative Critic (quality), `compliance-reviewer` (compliance.review), deterministic services (evidence, compliance.safety, feasibility, state).
**LIFECYCLE** — `DRAFT → VALIDATED → REVIEWED → LOCKED → RELEASED`, with bounded revision (§X).
**IDENTIFIER** — `CREATIVE_ID` + version.
**VERSIONING RULE** — New version on any content change. A revision loop (max 2, Phase 1 §G.12) produces v2, v3. `LOCKED` is a state, not a version — the locked version is `state: LOCKED` and nothing may be written to it thereafter.

### P.1 Canonical field map

```
creative_record
├── identity              CANONICAL          creative_id, version-block
├── lineage               CANONICAL          every upstream ID + version + hash
├── strategy              DERIVED_GENERATIVE inherited dimensions + message + tier
├── execution             DERIVED_GENERATIVE format, narrative, style, voice spec, duration
├── hook                  DERIVED_GENERATIVE strategy | copy | visual | audio  (§Q.1)
├── script                DERIVED_GENERATIVE beats + segments + speakers + cta (§Q.2)
├── visual_plan           DERIVED_GENERATIVE scenes + generation_units + continuity (§Q.3)
├── evidence              DERIVED_DETERMINISTIC claim bindings, qualifications, invariance
├── quality               DERIVED_GENERATIVE  critic verdict + four language checks
├── compliance            MIXED              safety (deterministic) + review (generative)
├── feasibility           DERIVED_DETERMINISTIC counts only
└── experiment            CANONICAL          arm-binding declaration (§O.6)
```

Eleven sections. Every one has a different owner, a different classification, or a different lifecycle — which is the test for whether a section earns its place. **`state` is not among them**: it is folded from the campaign event log (§G.0), because a state change is not a content change and must not cost a version.

### P.2 identity + lineage

```yaml
identity:
  creative_id:   CRE-acme-3f8b21-07
  <version-block per §G.2>

lineage:
  campaign_id / brand_id / product_id
  concept_id:            CON-acme-3f8b21-03
  hypothesis_id:         HYP-acme-3f8b21-017
  run_id:                RUN-20260904T1132Z-a91c4e
                         # experiment_id / arm_key live in `experiment` (§O.6), not here
  pinned_inputs:                                # duplicates version-block `inputs` in
    product_truth:       { ref: "…/product_truth@v2",    hash: "sha256:…" }
    research_dossier:    { ref: "…/research_dossier@v2", hash: "sha256:…" }
    experiment_plan:     { ref: "…/experiment_plan@v1",  hash: "sha256:…" }
    campaign_brief:      { ref: "…/campaign_brief@v1",   hash: "sha256:…" }
  knowledge:             { KNW-schwartz-persuasion: "sha256:…",
                           KNW-schwartz-language: "sha256:…",
                           KNW-narrative-library: "sha256:…",
                           KNW-cl-language-corpus: "sha256:…" }
  config:                # all nine registries of §B.1, hashed
                         { evidence_policy: "sha256:…", deny_list: "sha256:…",
                           narrative_library: "sha256:…", format_profiles: "sha256:…",
                           category_profiles: "sha256:…", creative_taxonomy: "sha256:…",
                           experiment_variables: "sha256:…", diversity_targets: "sha256:…",
                           tool_capability: "sha256:…" }
  skills:                { script-engine: "1.2.0", compliance-reviewer: "1.0.3" }
  models:                { draft: "claude-opus-5", critic: "claude-opus-5",
                           compliance: "claude-opus-5" }
  prompts:               { script_draft: "sha256:…", brilliance_pass: "sha256:…",
                           localisation: "sha256:…", critic: "sha256:…" }
```

`lineage` is the reason a performance result eighteen months from now can be attributed to what actually produced it (Phase 1 §U.4). Every entry is written at creation and **never back-filled** (INV-53).

### P.3 strategy + execution

```yaml
strategy:
  dimensions:           <inherited byte-identical from the concept; INV-40>
  core_message / promise / product_role
  reason_to_believe:    { statement, claim_refs: [CLM-…], territory }
  belief_bridge:        { from, to, via }
  audience_ref:         "research_dossier@v2#audience_model"
  persuasion:
    identification_strategy / mechanism_depth / promise_strategy
    reason_to_believe_strategy / intensification_devices
  claim_freedom_tier:   T1                      # copied from Product Truth, pinned
  permitted_territories:[ … ]                   # copied, pinned
  offer_ref:            "campaign_brief@v1#offer" | null

execution:
  format:               UGC                     # registry-validated
  narrative_pattern_id: NAR-confession
  style_id:             STY-ugc-raw-handheld
  voice_specification:  <§T.2>
  target_duration_s:    40
  duration_band:        SHORT_0_20 | MID_21_45 | LONG_46_90 | EXTENDED_91_PLUS
  pacing_intent:        SLOW_BUILD | STEADY | ESCALATING | RAPID
  language:             "es-CL"
  register:             COLLOQUIAL | NEUTRAL | FORMAL
```

`claim_freedom_tier` and `permitted_territories` are **copied and pinned**, not resolved live. A later Product Truth version that raises the tier must not retroactively make a locked creative's claims legal — the creative was written under the tier that existed when it was written.

`duration_band` exists because `target_duration_s: 40` and `target_duration_s: 41` are not different experimental treatments, and a locked variable comparison on raw seconds would produce spurious `LOCK_VIOLATION`s.

### P.4 evidence

```yaml
evidence:
  claim_bindings:                               # DERIVED_DETERMINISTIC
    - segment_ref:      "script.segments[s-014]"
      asserted_text:    "the exact clause that carries the claim"
      claim_id:         CLM-magnesio-500-0007
      claim_status:     VERIFIED
      required_class:   A2
      classes_present:  [ A2 ]
      territory:        COMPOSITION_STATEMENT
      result:           BOUND | UNRESOLVED | UNDER_CLASSED | TERRITORY_FORBIDDEN
  required_qualifications:
    - { claim_id: CLM-…, text: "the exact qualification wording",
        present_in: ["script.segments[s-015]"], result: PRESENT | MISSING }
  localisation_invariance:
    claim_set_before:   [ CLM-…, CLM-… ]        # captured after stage 6, before stage 7
    claim_set_after:    [ CLM-…, CLM-… ]        # recomputed on the final localised text
    qualifications_before: [ { claim_id, text } ]
    qualifications_after:  [ { claim_id, text } ]
    diff:               { added: [], removed: [], qualification_changed: [] }
    result:             INVARIANT | CLAIM_SET_CHANGED | QUALIFICATION_ALTERED
  negative_constraints: [ "never say X", "no white coats" ]   # from brief + brand + deny-list
  unsupported_language_scan:
    result:             PASS | FLAGGED
    flagged_segments:   [ { segment_ref, reason } ]
```

**Claim binding runs on the final localised text, not the draft.** Phase 1 §G orders localisation (stage 8) before claim→evidence (stage 10) precisely so that whatever the script actually says is what gets checked. `claim_set_before` is a stored snapshot taken between stages 6 and 7; storing the claim *set* rather than the whole earlier script keeps the artefact small while preserving the comparison that matters.

### P.5 quality, compliance, feasibility, experiment, state

```yaml
quality:                                        # DERIVED_GENERATIVE
  critic:
    verdict:            PASS | REVISE | REJECT_TO_HUMAN     # never HARD_BLOCK; INV-54
    findings:           [ { category, segment_ref, reasoning, suggested_change } ]
    reviewed_at / model / prompt_hash
  language_checks:                              # four enumerated checks, Phase 1 §H
    first_pass_comprehension: { result: PASS|REVISE|BLOCK, justification }
    ambiguity_risk:           { result: …, justification }
    spoken_naturalness:       { result: …, justification }
    visual_translatability:   { result: …, justification }
  revision_count:       1                       # max 2; then escalate (Phase 1 §G.12)

compliance:             <§U>

feasibility:                                    # DERIVED_DETERMINISTIC — counts only
  scene_count: 6
  generation_unit_count: 4
  speaker_count: 1
  requires_lipsync: true
  requires_hands_product_interaction: true
  continuity_span_count: 3
  distinct_locations: 1
  on_screen_text_blocks: 5
  longest_generation_unit_s: 12
  ceiling_source: "config/tool_capability@v1 (VENDOR_STATED)"
  result: WITHIN_CEILING | OVER_CEILING
  over_ceiling_reasons: []

experiment:                                     # the arm-binding DECLARATION (§O.6)
  experiment_id:      EXP-acme-3f8b21-01 | null
  arm_key:            "a1" | null
  creative_slot_key:  "slot-01"
  role:               CONTROL | VARIANT | null
  plan_ref:           { ref: "…/experiment_plan@v1", hash: "sha256:…" }

# NOTE: there is no `state` section. Creative state is DERIVED by folding
# CREATIVE_STATE_CHANGED events from the campaign log (§G.0, §X.4):
#   current: DRAFT | VALIDATED | REVIEWED | LOCKED | RELEASED
#            | REVISION_REQUESTED | REJECTED | SUPERSEDED
#   history: the event slice for this creative_id
#   locked_at / locked_hash: from the event that carried `to: LOCKED`
```

**Why `state` left the artefact.** A creative walking `DRAFT → VALIDATED → REVIEWED → LOCKED` changes no content. Revision 1 stored the state inside the versioned artefact, which forced a choice between rewriting an immutable version and cutting four versions of byte-identical content. Neither is acceptable; both were avoidable. The state is now four events and one version, and `state.history` is simply the creative's slice of the campaign event log — the same data, obtained by reading rather than by maintaining.

**No numeric score anywhere in `quality`.** Phase 1 ADR-011 rejected the twelve-field `0–10` `language_quality` vector; this is its replacement — four enumerated checks with a **required written justification** each. `feasibility` holds nine counts and two enums; every number is counted from the visual plan, none is scored.

### P.6 Invariants

INV-53 no `lineage` field may be written after `identity.version` is first persisted. INV-54 `quality.critic.verdict` and `compliance.review.verdict` enums exclude `HARD_BLOCK` at the schema level. INV-55 a `CREATIVE_STATE_CHANGED` event carrying `to: LOCKED` is refused unless `compliance.safety.overall == PASS`, `quality.critic.verdict == PASS`, `feasibility.result == WITHIN_CEILING`, and every `evidence.claim_bindings[].result == BOUND`. INV-56 a transition to `RELEASED` requires a Gate 3 `GATE_DECISION` whose `reviewed_artifacts[]` contains this creative at this exact `content_hash`. INV-57 `quality.revision_count <= 2`; a third revision request emits a `REVISION_REQUESTED` event with `escalated: true` and stops the loop.

---

## Q. Script / Hook / Storyboard Data Model

### Q.1 Hook — four addressable parts, one object

Master Prompt §28 requires the four parts to be individually addressable so a future experiment can change exactly one. They are four sibling keys under `hook`, addressed by fragment path — **not four files and not four IDs.**

```yaml
hook:
  strategy:                                     # decided BEFORE format (Phase 1 §G.3)
    entry_awareness:    PROBLEM_AWARE
    entry_device:       QUESTION | CONFESSION | PATTERN_INTERRUPT | CONTRADICTION
                        | DEMONSTRATION | STAKES | SOCIAL_PROOF | CURIOSITY_GAP
    belief_entry_point: "the belief the hook meets the viewer in"
    rationale:          "why this device for this awareness state"
  copy:
    text:               "exact spoken or written words"     # verbatim, no placeholders
    segment_ref:        "script.segments[s-001]"
    on_screen_text:     "string | null"
    claim_refs:         [ ]                     # usually empty; a claim in a hook is checked
  visual:
    description:        "what is on screen in the first beat"
    framing:            <SHOT_FRAMING>
    subject:            "who or what"
    product_presence:   NONE | BACKGROUND | HELD | IN_USE | HERO
    scene_ref:          "visual_plan.scenes[sc-01]"
  audio:
    delivery:           "tone, pace, emphasis"
    sfx:                [ "string" ]
    music_character:    "string | null"
    first_words_timing_s: 0.4
```

`hook.copy.text` is **the** hook copy; `script.segments[s-001].text` is the same string, and INV-58 requires them equal. The duplication is deliberate and validated: the hook must be addressable as a unit for experiments, and the script must be readable end to end without assembling it from fragments.

### Q.2 Script — shared core plus format extension

**Decision: one polymorphic model, constrained by a format profile.** Three separate schemas would make cross-format comparison (a real V1 need — the batch mixes 5/2/3) require three code paths, and a single schema with every format's fields would make two thirds of the fields meaningless for any given creative — the two failure modes Master Prompt §55 names.

```yaml
script:
  language: "es-CL"
  speakers:
    - { speaker_key: "sp1", role: PRESENTER | HOST | GUEST | NARRATOR,
        voice_specification_ref: "execution.voice_specification" }
  beats:                                        # persuasion beats (Phase 1 §G.5)
    - { beat_key: "b-hook", function: HOOK | PROBLEM | AGITATION | MECHANISM
                                    | PROOF | OBJECTION | BENEFIT | CTA,
        segment_refs: ["s-001","s-002"], intent: "what this beat must accomplish" }
  segments:
    - segment_key:      "s-014"
      order:            14
      beat_key:         "b-proof"
      kind:             VOICEOVER | DIALOGUE | REACTION | INTERRUPTION | PAUSE
                        | ON_SCREEN_TEXT_ONLY | SFX | VISUAL_BEAT
      speaker_key:      "sp1" | null
      turn_index:       3 | null                # PODCAST only
      text:             "the exact words, verbatim, no placeholders"
      on_screen_text:   "string | null"
      duration_estimate_s: 3.2
      claim_refs:       [ CLM-… ]
      qualification_refs:[ CLM-… ]              # qualifications this segment carries
      direction:        "performance note"
  cta:
    kind:               SHOP_NOW | LEARN_MORE | DM | LINK_IN_BIO | NONE
    text:               "exact CTA wording"
    segment_ref:        "script.segments[s-022]"
  totals:                                       # DERIVED_DETERMINISTIC
    segment_count: 22, estimated_duration_s: 41.6, word_count: 118
```

**Format profiles constrain the same schema** (`config/format_profiles/<format>.yaml`, versioned and hashed):

```yaml
format: PODCAST
speakers: { min: 2, max: 3, roles_allowed: [HOST, GUEST] }
segment_kinds_allowed: [ DIALOGUE, REACTION, INTERRUPTION, PAUSE, ON_SCREEN_TEXT_ONLY, SFX ]
requires_turn_index: true
requires_speaker_on: [ DIALOGUE, REACTION, INTERRUPTION ]
forbidden: [ VOICEOVER ]
```

```yaml
format: ANIMATION
speakers: { min: 0, max: 1, roles_allowed: [NARRATOR] }
segment_kinds_allowed: [ VOICEOVER, VISUAL_BEAT, ON_SCREEN_TEXT_ONLY, SFX ]
requires_turn_index: false
forbidden: [ DIALOGUE, REACTION, INTERRUPTION ]
human_likeness_allowed: false
```

Adding a fourth format is a new YAML file. No schema migration, no code change, no new object — which is what Master Prompt §24 asks for.

**Placeholders are schema-invalid.** `text` matching `/\[[^\]]*\]|<[^>]*>|TBD|XXX|\.\.\./` is rejected. Phase 1 §S's concrete test — *no line reading "Creator explains the benefit"* — becomes a validator, not an aspiration.

### Q.3 Storyboard / shot list — specified for a clip generator

Designed for AI video generation, not film production. Every field below is either consumable by a generation prompt, needed for continuity across a seam, or needed for QA against the package. Grip, lens, focal length, camera model, crew and scheduling fields are **deliberately absent** (Master Prompt §30).

```yaml
visual_plan:
  scenes:
    - scene_key:        "sc-03"
      order:            3
      generation_unit_key: "gu-02"
      t_start / t_end:  12.0 / 18.4
      subject:          "who or what is on screen"
      action:           "what happens, in one sentence a generator can act on"
      framing:          EXTREME_CLOSE | CLOSE | MEDIUM_CLOSE | MEDIUM | WIDE | OVER_SHOULDER
                        | POV | INSERT_PRODUCT | SCREEN_CAPTURE
      camera_movement:  STATIC | HANDHELD | PUSH_IN | PULL_BACK | PAN | TILT | ORBIT | WHIP
      dialogue_segment_refs: [ "script.segments[s-014]" ]
      product_presence: NONE | BACKGROUND | HELD | IN_USE | HERO
      on_screen_text:   { text, position: TOP|CENTER|BOTTOM, style_ref } | null
      performance_direction: "string | null"
      lighting:         NATURAL_DAY | NATURAL_WINDOW | INDOOR_WARM | INDOOR_COOL
                        | LOW_KEY | HIGH_KEY | MIXED
      transition_in:    CUT | MATCH_CUT | DISSOLVE | WHIP | JUMP_CUT
      audio:            { vo_present: bool, sfx: [ ], ambience: "string | null" }
      continuity_refs:  [ "ca-character-01", "ca-product-01" ]
  generation_units:
    - generation_unit_key: "gu-02"
      scene_keys:       [ "sc-03", "sc-04" ]
      duration_s:       11.8
      anchor_in:        { continuity_refs: [ … ], last_frame_intent: "string" }
      anchor_out:       { continuity_refs: [ … ], first_frame_intent: "string" }
      ceiling_s:        15                      # from config/tool_capability
      within_ceiling:   true
  continuity_anchors:
    - continuity_key:   "ca-character-01"
      kind:             CHARACTER | WARDROBE | PRODUCT | LOCATION | LIGHTING | VOICE | STYLE
      description:      "stable description a generator can hold across units"
      asset_refs:       [ AST-… ]               # e.g. the product image
      spans_units:      [ "gu-01", "gu-02", "gu-03" ]
```

**The duration ceiling is configuration, not a constant.** `config/tool_capability.yaml` carries `generation_unit_max_duration_s` together with `verification_status: VERIFIED | VENDOR_STATED | UNVERIFIED`. Phase 1 §0.2 records the ~15 s figure as vendor-stated and Phase 1 ADR-019 requires a capability spike before any integration. Hardcoding 15 would bake an unverified vendor claim into the schema; putting it in config with its verification status attached means the spike updates one file.

INV-59 every `generation_units[].duration_s <= ceiling_s`. INV-60 every scene belongs to exactly one generation unit and units partition the timeline without gaps or overlaps. INV-61 every `continuity_anchors[].spans_units` covering more than one unit must appear in the `anchor_out` of the earlier unit and the `anchor_in` of the later one — a continuity requirement that is not anchored at the seam is not a continuity requirement.
---

## R. Production Package Schema

**PURPOSE** — A locked, versioned, self-sufficient handoff contract. V1-Production must be able to produce the video without re-deciding anything and without resolving a single strategic reference.
**CANONICAL OR DERIVED** — **`DERIVED_DETERMINISTIC`, materialised.** Every field is a pure projection of one locked Creative Record version plus pinned registry entries. Nothing in a package originates here.
**OWNING COMPONENT** — Production Package assembler (service, Phase 1 §D).
**LIFECYCLE** — `DRAFT → LOCKED → RELEASED → SUPERSEDED | WITHDRAWN`.
**IDENTIFIER** — `PACKAGE_ID`, derived: `PKG-<creative-suffix>-v<n>`.
**VERSIONING RULE** — One package version per locked creative version. A new creative version produces a new package; the old package becomes `SUPERSEDED`.

### R.1 Duplicated vs referenced — the decision, stated per section

| Section | Treatment | Why |
|---|---|---|
| Full script (every segment's exact text) | **Duplicated in full** | The generator reads words; a reference would require resolution |
| Speakers, beats, CTA | **Duplicated** | Same |
| Scene plan, generation units, continuity anchors | **Duplicated in full** | This is the production instruction set |
| Style specification | **Duplicated in full**, plus `style_id` | A `style_id` alone would make the package non-self-sufficient; the ID is kept for the join |
| Voice specification | **Duplicated in full** | Same |
| Strategy summary (audience, awareness, angle, promise, RTB, product role) | **Duplicated, read-only** | So production understands *why*, and so QA can judge fidelity. Explicitly marked `read_only: true` |
| Negative constraints, required qualifications | **Duplicated in full** | Safety-critical; must not depend on a lookup succeeding |
| Claim→evidence report | **Duplicated as a table** (claim_id, statement, status, class, source title, locator) | Auditable at the package; the full source stays external |
| Asset payloads | **Referenced** — `asset_id` + `content_sha256` + `path` + `state` | Binaries are never inlined; the hash makes the reference verifiable |
| Source documents | **Referenced** — `source_id` + `snapshot_asset_id` | Same |
| Creative Record | **Referenced** — `creative_id@version` + `content_hash` | The reconstructibility anchor |
| Evidence Ledger, Research Dossier, Hypothesis Pool | **Referenced only** | Production has no use for them; including them would invite re-deciding |

### R.2 Shape

```yaml
production_package:
  package_id:           PKG-acme-3f8b21-07-v1
  <version-block>
  source_creative:      { ref: "CRE-acme-3f8b21-07@v3", hash: "sha256:…" }
  projector_version:    "package-assembler@1.0.0"        # required for reconstructibility
  lineage:              <copied verbatim from creative.lineage>
  strategy_readonly:                                     # read_only: true
    audience_summary / awareness_state / sophistication_state
    angle_mechanism / core_message / promise
    reason_to_believe / product_role / belief_bridge
    psychological_hypothesis
  execution:
    format / narrative_pattern_id / narrative_pattern_spec
    style_id / style_specification                       # full spec, duplicated
    voice_specification                                  # full spec, duplicated
    target_duration_s / duration_band / pacing_intent / language / register
  script:               <copied verbatim from creative.script>
  visual_plan:          <copied verbatim from creative.visual_plan>
  continuity_manifest:                                   # flattened for production
    - { continuity_key, kind, description, asset_refs, spans_units }
  segmentation_plan:
    units: [ { generation_unit_key, duration_s, scene_keys,
               anchor_in, anchor_out, ceiling_s } ]
    ceiling_source: "config/tool_capability@v1 (VENDOR_STATED)"
  assets:
    - { asset_id, role: PRODUCT_IMAGE|BRAND_MARK|STYLE_REFERENCE|PROOF_ASSET,
        content_sha256, path, state, rights_summary }
  constraints:
    negative_constraints: [ … ]
    required_qualifications: [ { claim_id, text, must_appear_in: [segment_ref] } ]
    claim_freedom_tier / permitted_territories
  reports:
    claim_evidence:
      - { claim_id, statement, status, required_class, classes_present,
          source_id, source_title, locator, segment_ref }
    safety_validation:  <copied from creative.compliance.safety>
    compliance_review:  <copied from creative.compliance.review>
    creative_qa:        <copied from creative.quality>
    feasibility:        <copied from creative.feasibility>
    routing_recommendation:
      suggested_order:  [ ANIMATION_FIRST | AS_SPECIFIED ]
      risk_notes:       [ "requires lipsync — capability UNVERIFIED (Phase 1 ADR-019)" ]
    experiment_binding: <copied from §O.6 for this creative's arm, if any>

# state is NOT a field. It is folded from PACKAGE_STATE_CHANGED events (§G.0, §X.5):
#   DRAFT | LOCKED | RELEASED | SUPERSEDED | WITHDRAWN
#   released_by_gate: from the event that carried `to: RELEASED`
```

### R.3 Reconstructibility

**The contract:** given `source_creative.ref` + `source_creative.hash` + `projector_version` + the pinned registry hashes, re-running the assembler produces a **byte-identical** package under the canonical serialization (§G.7). This is testable, and §AA specifies it as a CI check alongside the SQLite rebuild.

Two consequences that make it hold: the assembler is a pure function with no clock and no randomness (`created_at` is supplied by the caller, not read from the system clock inside the projection), and every registry entry the package inlines is pinned by hash in `lineage.config`.

INV-62 a package may not reference a creative whose folded state is not `LOCKED`. INV-63 a `PACKAGE_STATE_CHANGED` event carrying `to: RELEASED` requires a Gate 3 decision covering `source_creative` at exactly `source_creative.hash`, **and** — where the creative occupies an experiment arm — `binding_result: COMPLETE` with `lock_validation.result: SATISFIED` (INV-107, INV-108). INV-64 no field of a package may differ from its projection source; a re-projection mismatch is a `HARD_BLOCK` on release.

---

## S. Asset / Rights / Lineage Schema

**PURPOSE** — Every file the system holds or makes, with the rights position that governs whether it may ship, and the lineage that makes rights inheritance computable.
**CANONICAL, immutable record + asset event log.** Never versioned — a changed file is a new asset, and a changed *rights position* is an event.
**OWNING COMPONENT** — Asset Registry / ingestion service (Phase 1 §J).
**IDENTIFIER** — `ASSET_ID`, random-allocated (§E.4).

### S.1 Shape — immutable record, derived rights and state

```yaml
# --- immutable record, written once at ingestion ----------------------------
asset_id:           AST-7b31e0c9d4a2
asset_type:         PRODUCT_IMAGE | BRAND_MARK | BRAND_ASSET | REFERENCE_VIDEO
                    | VOICE_SAMPLE | STYLE_REFERENCE | GENERATED_IMAGE | GENERATED_CLIP
                    | FINAL_VIDEO | PROOF_ASSET | DOCUMENT | SOURCE_SNAPSHOT
path:               "relative/path/under/media-root"
original_filename:  "WhatsApp Video 2026-09-03 at 10.01.37 PM.mp4"
content_sha256:     "sha256:…"
bytes:              12874112
mime_type:          "video/mp4"
media:              { duration_s, width, height, fps, sample_rate_hz,
                      bitrate_kbps, channels }          # nulls where not applicable
origin:
  kind:             USER_UPLOAD | REPOSITORY | GENERATED | THIRD_PARTY_FETCH
  acquired_via:     "operator upload" | "repo at commit <sha>" | "web_fetch" | "<tool>"
  acquired_at:      "2026-09-04T11:35:02Z"
  source_id:        SRC-… | null                        # for SOURCE_SNAPSHOT
derived_from:       [ AST-… ]                            # acyclic; see §S.3
generation:                                              # only when origin.kind == GENERATED
  package_id / creative_id / generation_unit_key / run_id
  tool: "string" / model: "string" / attempt: 2
  prompt_hash: "sha256:…" / cost_usd: 0.42
  retry_reason: "string | null"
brand_id / product_id / tags[] / notes
registered_at / registered_by_run_id

# --- derived: initial state from origin.kind, then folded over asset events -
state:              USER_PROVIDED_UNVERIFIED | REFERENCE | AUTHORIZED
                    | GENERATED_DRAFT | PRODUCTION_ELIGIBLE | PRODUCTION
                    # initial value is a pure function of origin.kind (INV-65);
                    # there is NO creation event (INV-119)
state_history:      [ { from, to, actor, at, reason, conditions_met: [] } ]  # the event slice
rights:                                       # latest ASSET_RIGHTS_ATTESTED payload
  owner:            "string | null"
  rights_basis:     OWNED | LICENSED | CLIENT_SUPPLIED_WITH_WARRANTY | NONE | UNKNOWN
  licence:          "string | null"
  licence_document_asset_id: AST-… | null
  commercial_use:   PERMITTED | PROHIBITED | UNKNOWN
  territory:        [ "CL" ] | []
  expires_at:       "2027-01-01" | null
  consent:
    likeness:       NONE | RECORDED | VERIFIED | NOT_APPLICABLE
    voice:          NONE | RECORDED | VERIFIED | NOT_APPLICABLE
    consent_document_asset_id: AST-… | null
  attested_by:      "op-01" | null
  attested_at:      "2026-09-04T11:40:00Z" | null
rights_history:     [ … ]                     # every attestation, in order
```

The two events that move an asset — **there is no registration event**; writing the record is the registration:

```yaml
event_type: ASSET_RIGHTS_ATTESTED             # carries the WHOLE rights block
payload: { rights: { … }, attested_by: "op-01", basis_document_asset_id: AST-… }

event_type: ASSET_STATE_CHANGED
payload: { from: USER_PROVIDED_UNVERIFIED, to: AUTHORIZED,
           reason: "operator attestation, licence on file",
           conditions_met: [ RIGHTS_BASIS_PRESENT, COMMERCIAL_USE_PERMITTED,
                             TERRITORY_COVERS_MARKET, NOT_EXPIRED,
                             CONSENT_LIKENESS_NA, CONSENT_VOICE_NA ] }
```

An asset with **no events at all** is therefore fully defined: its state is `origin.kind`'s mapping and its rights fold to the no-permission default (INV-71). That is the common case — the fifteen files in `samples/` have no asset events, and are `REFERENCE` with no consent, exactly as intended.

**Rights are attested, never edited.** An operator who supplies a licence emits an attestation carrying the complete rights block; the fold takes the latest, and `rights_history` keeps every one. A liability record whose earlier state can be overwritten is not a liability record — Revision 1's editable `rights` block would have allowed exactly that, silently.

**Audited out:** `version` (assets are immutable; a re-render is a new asset with a `derived_from` edge), `licence`/`territory`/`expiry` as top-level fields (all inside the attested `rights` block, so a partial rights update is impossible), and `state` as a stored field (there is no default and no writer; §S.2).

### S.2 State machine with explicit transition conditions

```
    USER_PROVIDED_UNVERIFIED ──┐
                               ├──► AUTHORIZED ──► (usable as production input)
    REFERENCE ─────────────────┘         │
                                         │ used as input to generation
                                         ▼
                                  GENERATED_DRAFT
                                         │
                                         ▼
                                 PRODUCTION_ELIGIBLE
                                         │
                                         ▼
                                    PRODUCTION
```

| Transition | Required conditions — **all** must hold |
|---|---|
| *(ingest)* → `USER_PROVIDED_UNVERIFIED` | `origin.kind == USER_UPLOAD`. This is the **only** state an upload may enter. |
| *(ingest)* → `REFERENCE` | `origin.kind ∈ {REPOSITORY, THIRD_PARTY_FETCH}` |
| *(generate)* → `GENERATED_DRAFT` | `origin.kind == GENERATED`. The **only** state a generated asset may enter. |
| `USER_PROVIDED_UNVERIFIED → AUTHORIZED` | `rights.rights_basis ∈ {OWNED, LICENSED, CLIENT_SUPPLIED_WITH_WARRANTY}` · `rights.commercial_use == PERMITTED` · `attested_by` and `attested_at` non-null · territory covers the campaign market · `expires_at` null or in the future · if the asset depicts a person: `consent.likeness == VERIFIED` · if it carries a voice: `consent.voice == VERIFIED` |
| `REFERENCE → AUTHORIZED` | Same conditions, plus a resolvable `licence_document_asset_id` or `consent_document_asset_id` |
| `GENERATED_DRAFT → PRODUCTION_ELIGIBLE` | Every asset in `rights_root_set` (§S.3) is `AUTHORIZED` · no ancestor has `consent.likeness` or `consent.voice` other than `VERIFIED`/`NOT_APPLICABLE` · no ancestor's `rights.expires_at` is past · the creative's `compliance.safety.overall == PASS` · Video QA verdict `PASS` · `derived_from[]` fully resolvable |
| `PRODUCTION_ELIGIBLE → PRODUCTION` | Assigned to a creative **and** a Gate 3 `GATE_DECISION` released the package that produced it |

**Invalid transitions, enumerated so code can refuse them:** any transition into `AUTHORIZED` from `GENERATED_DRAFT` or later · any transition that skips a level (`REFERENCE → PRODUCTION_ELIGIBLE`, `USER_PROVIDED_UNVERIFIED → PRODUCTION`) · any backward transition except `PRODUCTION → PRODUCTION_ELIGIBLE` (withdrawal) and `* → REFERENCE` (never permitted; a downgrade is a new asset record) · any transition with an empty `reason` · any transition whose `conditions_met[]` does not list every condition in the table above.

Terminal: `PRODUCTION`. There is no delete; withdrawal is a recorded transition back to `PRODUCTION_ELIGIBLE` with a reason.

### S.3 Rights lineage

`derived_from[]` forms a DAG. Two derived functions answer Master Prompt §34's four questions without inspecting a filename:

```
rights_root_set(A)  = { X : X is a leaf reachable from A via derived_from }
rights_closure(A)   = { X : X reachable from A via derived_from }  ∪ {A}
```

| Question | Answered by |
|---|---|
| Which inputs contributed to this generated output? | `rights_closure(A) \ {A}` |
| Were they authorised? | `∀ X ∈ rights_closure(A) \ {A} : X.state == AUTHORIZED` |
| Did any include likeness? | `∃ X : X.rights.consent.likeness ∈ {NONE, RECORDED}` |
| Did any include voice? | `∃ X : X.rights.consent.voice ∈ {NONE, RECORDED}` |
| Did any permission expire? | `∃ X : X.rights.expires_at < today` |

The SQLite `asset_lineage` edge table (§Z) exists precisely so these are single recursive queries rather than a filesystem walk.

**Two derived conditions, both deterministic:**

- `RIGHTS_EXPIRED` — computed, not a state. Any asset whose closure contains an expired permission is reported expired; a `PRODUCTION` asset in that condition raises a `HARD_BLOCK` on further use and is surfaced to the operator. Modelling expiry as a *state* would require a scheduled job to mutate immutable records; modelling it as a *computation* requires only a date.
- `CONFOUNDED_BY_SHARED_SOURCE` — two assets whose `rights_root_set`s intersect may not be cited as independent evidence about one another (Phase 1 §K). This is what makes "Voice X performs well with Style Y" structurally unrepresentable as a causal finding when both derive from the same UGC clip, and it is checked at analysis time, not remembered.
- `SHARED_CONTENT_DIFFERENT_RIGHTS` — two asset records with equal `content_sha256` and differing `state` or `rights.owner` are flagged for operator resolution (§E.4).

### S.4 The fifteen current assets

All fifteen media files in `samples/` are `REFERENCE` with `rights.rights_basis: NONE` and `consent.voice: NONE`. Nothing generated from them can leave `GENERATED_DRAFT`. The three `ssstik.io_*` voice files additionally carry `tags: [no_cloning_source]`, enforced by INV-72. This is Phase 1 §J and §K expressed as data rather than as a rule someone must remember.

INV-65 an asset's initial state is a pure function of `origin.kind` on the record; there is no registration event and no writable initial-state field. INV-66 every `ASSET_STATE_CHANGED` event carries a non-empty `reason` and a complete `conditions_met[]`; `state_history` is the event slice and is never written directly. INV-67 `derived_from` is acyclic. INV-68 a transition to `PRODUCTION_ELIGIBLE` requires the full condition set in §S.2, evaluated against the folded state of every ancestor at the moment of the event. INV-69 a transition to `PRODUCTION` requires a Gate 3 decision reference in the event payload. INV-70 an asset with `origin.kind == GENERATED` must have a non-null `generation` block. INV-71 `rights.consent.*` has no default that permits use; an asset with no `ASSET_RIGHTS_ATTESTED` event folds to `NONE`. INV-72 an asset tagged `no_cloning_source`, or whose folded `consent.voice != VERIFIED`, may never appear as a `voice_specification.reference_assets[].use == CLONING_SOURCE`.

---

## T. Style / Voice Data Model

### T.1 Style Profile

**CANONICAL** (authored). Registry entity, not versioned as an artefact — a changed profile is a new `STYLE_ID` or an appended registry revision with its own hash. V1 ships **three** hand-authored profiles, one per format (Phase 1 ADR-012). No extraction pipeline is designed here.

```yaml
style_id:            STY-ugc-raw-handheld
name:                "Raw handheld UGC"
format_affinity:     [ UGC ]
abstraction_level:   ARCHETYPE | FAMILY        # SPECIFIC is invalid; INV-73
grammar:
  pacing:            { avg_shot_length_s: [1.5, 3.5], cut_frequency: HIGH }
  framing:           [ CLOSE, MEDIUM_CLOSE ]
  camera:            [ HANDHELD, PUSH_IN ]
  lighting:          [ NATURAL_WINDOW, INDOOR_WARM ]
  editing:           { jump_cuts: FREQUENT, b_roll: SPARSE, speed_ramps: NONE }
  caption_style:     { present: true, position: CENTER, emphasis: WORD_HIGHLIGHT }
  visual_energy:     LOW | MEDIUM | HIGH
  product_entry_ratio: 0.25        # position in the timeline as a ratio, not a beat
  performance_energy:  CONVERSATIONAL | ANIMATED | INTENSE
provenance:
  authored_by / reviewed_by / reviewed_at
  informed_by_asset_ids: [ AST-… ]             # recorded, NOT a rights edge (§AE Case E)
  cross_category_test:  PASS | FAIL            # "would this apply to an unrelated product?"
notes
```

`product_entry_ratio` is a ratio because Phase 1 §L insists style captures grammar, never substance — "product appears at 25 % of runtime" transfers across categories; "product appears after the DHT explanation" does not.

INV-73 `abstraction_level: SPECIFIC` is invalid. INV-74 `cross_category_test: FAIL` blocks the profile from use — a profile that only fits its source category has leaked content. INV-75 `grammar` may contain no claim, brand name, product name, price, offer or dialogue text.

**`informed_by_asset_ids` is not a `derived_from` edge.** Reading a reference video to author an abstract grammar does not create a rights derivative, provided the abstraction level and the cross-category test hold. This is the distinction that lets the nine `REFERENCE` sample videos be useful without contaminating every generated asset (§AE Case E).

### T.2 Voice Specification

**Embedded value object** in `creative.execution` and duplicated into the Production Package. There is **no `VOICE_ID` in V1-Core**: no sample in the repository is production-eligible, so a voice *catalogue* would be a catalogue of things that cannot be used (Phase 1 §K, ADR-013).

```yaml
voice_specification:
  country:              "CL"
  accent:               "chileno neutro" | "santiaguino" | …
  perceived_age_range:  [ 25, 35 ]
  perceived_gender_presentation: FEMININE | MASCULINE | NEUTRAL | UNSPECIFIED
  vocal_register:       LOW | MID | HIGH
  energy:               CALM | WARM | UPBEAT | INTENSE
  pace:                 SLOW | MEASURED | BRISK | RAPID
  tone:                 CONFIDING | AUTHORITATIVE | FRIENDLY | SKEPTICAL | PLAYFUL
  delivery_style:       CONVERSATIONAL | NARRATION | INTERVIEW | REACTIVE
  format_fit:           [ UGC ]
  reference_assets:                              # optional, tightly constrained
    - { asset_id: AST-…, use: DESCRIPTIVE_TARGET_ONLY }
  resolution:                                    # filled by V1-Production, null in V1-Core
    resolved_voice_asset_id: null
    resolved_at: null
```

`perceived_gender_presentation` describes a **desired vocal character for casting or synthesis**, not a person, and carries no other demographic inference. `use: CLONING_SOURCE` exists in the enum only so the validator can refuse it: INV-72 makes it unusable for every asset currently in the repository, and Phase 1 ADR-014 makes it a hard line for any TikTok-sourced sample regardless of future documentation.

A Voice Specification never binds a script to an audio file. V1-Production resolves it against whatever legitimately licensed source exists at that time and writes `resolution` on a **new** package version — it does not mutate the locked one.

---

## U. Compliance / HARD_BLOCK Model

Two objects, two owners, two enums that do not overlap. The separation is the whole point.

### U.1 SCRIPT_SAFETY_VALIDATION — deterministic

**`DERIVED_DETERMINISTIC`.** Owned by deterministic services. This is the **only** object in the system whose enum contains `HARD_BLOCK`.

```yaml
compliance:
  safety:
    validator_version:  "script-safety@1.0.0"
    policy_refs:        { evidence_policy: "sha256:…", deny_list: "sha256:…" }
    ran_at:             "2026-09-04T15:02:11Z"
    ran_on:             { creative_version: 3, script_hash: "sha256:…" }
    checks:
      - check_id:       "SSV-CLAIM-001"
        family:         CLAIM_EVIDENCE_BINDING
        result:         PASS | HARD_BLOCK | NOT_APPLICABLE
        rule_id:        "claim.unresolved"
        reason:         "segment s-014 asserts a composition statement with no bound claim"
        affected_field: "script.segments[s-014].text"
        required_remediation: "bind to a VERIFIED claim, or remove the assertion"
      - …
    overall:            PASS | HARD_BLOCK
    blocking_count:     0
```

**The five deterministic families** (Master Prompt §2.3, all present):

| Family | What it checks | Data it reads |
|---|---|---|
| `CLAIM_EVIDENCE_BINDING` | Every asserted claim in the final text resolves to a CLAIM with `status: VERIFIED` | `evidence.claim_bindings[]` |
| `MINIMUM_EVIDENCE_CLASS` | Each bound claim's `classes_present` satisfies the matrix for its `claim_type` | `config/evidence_policy` + CLAIM records |
| `LOCALISATION_CLAIM_INVARIANCE` | Claim set unchanged across stages 7–8, and every required qualification present verbatim | `evidence.localisation_invariance` |
| `DENY_LIST` | No match against the compliance deny-list | `config/deny_list` |
| `RIGHTS_AND_REQUIRED_ASSETS` | Every asset the script requires exists, is `AUTHORIZED`, and its lineage is clean | Asset Registry + `rights_closure` |

`config/deny_list.yaml` is authored, versioned and hashed:

```yaml
- rule_id: DL-ORGANIC-IMPERSONATION-001
  description: "Simulated Reddit thread, fabricated screenshot of organic content,
                or replicated platform-native UI presented as genuine"
  basis: "Phase 1 F3; schwartz_persuasion_framework.md §15"
  severity: HARD_BLOCK
  applies_to: [ script.segments[].text, script.segments[].on_screen_text,
                visual_plan.scenes[].on_screen_text, visual_plan.scenes[].action ]
- rule_id: DL-META-APPROVED-001
  description: "Any assertion that Meta has approved, pre-approved or endorsed the ad"
  basis: "Phase 1 §R — never store META_APPROVED"
  severity: HARD_BLOCK
```

### U.2 COMPLIANCE_REVIEW — judgement

**`DERIVED_GENERATIVE`.** Owned by the `compliance-reviewer` Skill. Its verdict enum **does not contain `HARD_BLOCK`** — not by convention, at the schema level, so a model cannot emit one even if it tries (Phase 1 ADR-032).

```yaml
  review:
    reviewer:           { skill: "compliance-reviewer", version: "1.0.3",
                          model: "claude-opus-5", prompt_hash: "sha256:…" }
    reviewed_at:        "2026-09-04T15:06:40Z"
    reviewed_on:        { creative_version: 3, script_hash: "sha256:…" }
    verdict:            LOW | MEDIUM | HIGH_RISK | POLICY_REVIEW_REQUIRED
    findings:
      - { finding_id: "f1", category: IMPLIED_CLAIM | AMBIGUITY | TESTIMONIAL
                             | BEFORE_AFTER | NATIVE_FORMAT_FIT | CATEGORY_SENSITIVE
                             | QUALIFICATION_SUFFICIENCY | URGENCY_SCARCITY,
          affected_field: "script.segments[s-009].text",
          reasoning: "written",
          suggested_remediation: "written" }
    policy_sources:                              # fetched at review time, never cached
      - { url, title, fetched_at, content_sha256 }
    human_adjudication:
      decision:         ACCEPTED | OVERRULED | REVISION_REQUIRED | null
      by / at / reasoning
      gate_id:          GAT-acme-3f8b21-007
```

INV-76 `review.verdict` may not be `HARD_BLOCK`; the value is absent from the enum. INV-77 `verdict ∈ {HIGH_RISK, POLICY_REVIEW_REQUIRED}` requires a `human_adjudication` with a `gate_id` before `state: RELEASED`. INV-78 `policy_sources` is non-empty and every `fetched_at` is within the same run — Phase 1 ADR-018 forbids caching policy text into the design, and this makes staleness visible. INV-79 the string `META_APPROVED` may not appear as a value anywhere in the system; it is deny-listed and schema-invalid as a verdict. INV-80 `safety.overall == HARD_BLOCK` cannot be cleared by any gate decision — only by a new creative version whose re-run of the same validator returns `PASS`.

### U.3 The two block classes, as data

| | `HARD_BLOCK` | `HIGH_RISK` / `POLICY_REVIEW_REQUIRED` |
|---|---|---|
| Field | `compliance.safety.checks[].result` | `compliance.review.verdict` |
| Written by | Deterministic service | Model, then human adjudication |
| Cleared by | A new creative version that changes the underlying state | `human_adjudication.decision` recorded against a gate |
| Recorded in Run Manifest | `rejections[]` with `kind: HARD_BLOCK` | `rejections[]` with `kind: ESCALATION` |
| Overridable by approval | **No** | **Yes — that is its purpose** |

Both are recorded in `rejections[]` either way, which is what later makes the false-block rate measurable and therefore what would make automating a gate defensible (Phase 1 §R).

### U.4 The concept pre-screen

The cheap concept-level filter (flow step 11) writes a compact object onto each hypothesis and concept:

```yaml
prescreen:
  ran_at / validator_version
  deterministic:
    required_territories_permitted: PASS | HARD_BLOCK
    claim_dependencies_satisfiable:  PASS | HARD_BLOCK | UNRESOLVED
    deny_list_match:                 PASS | HARD_BLOCK
    blocking_gap:  { missing_claim_ids: [], forbidden_territories: [] } | null
  judgement:
    verdict:   LOW | MEDIUM | HIGH_RISK | POLICY_REVIEW_REQUIRED
    reasoning: "written"
```

A hypothesis requiring `OUTCOME_PROMISE` under a `T1` tier is killed here at the cost of one comparison, not at the cost of a full script — which is the entire economic argument for running compliance twice (Phase 1 §G.5).

---

## V. Human Gate Model

**PURPOSE** — An auditable record of a human decision bound to exact artefact versions.
**CANONICAL, immutable.** Append-only. Never edited, never deleted, never superseded — a changed mind is a **new** decision record.
**OWNING COMPONENT** — Gate service.
**IDENTIFIER** — `GATE_ID`, scope-ordinal in `(GAT, campaign)`: `GAT-<campaign-suffix>-<NNN>`, allocated as `max + 1` over the campaign's existing gate decisions under the single-writer rule (§E.1.1).

```yaml
gate_id:            GAT-acme-3f8b21-007
campaign_id / run_id
gate_type:          G1_TRUTH | G2_CONCEPTS | G3_RELEASE
opened_at / decided_at
reviewer:           { name, identifier, kind: HUMAN }
reviewed_artifacts:                              # REQUIRED, binds by hash
  - { ref: "CRE-acme-3f8b21-07@v3", type: creative_record, hash: "sha256:9f3c…" }
  - { ref: "PKG-acme-3f8b21-07-v1", type: production_package, hash: "sha256:22ab…" }
decision:           APPROVED | APPROVED_WITH_OVERRIDES | CHANGES_REQUESTED | REJECTED
comments:           "free text"
overrides:                                       # BYTE-NEUTRAL adjudications only (§V.2)
  - kind:           DIVERSITY_TARGET_RELAXATION | POLICY_RISK_ACCEPTANCE
                    # exactly two kinds. No override raises a claim-freedom tier (INV-120).
    target:         "experiment_plan@v1#diversity_audit.diversity_targets[core_problem]"
    reason:         "REQUIRED — written"
required_changes:                                # only with decision: CHANGES_REQUESTED
  - { target_ref, change, blocking: true }
authorized_changes:                              # only with decision: CHANGES_REQUESTED
  - { target_ref, change, rationale }             # what the reviewer permits, pre-agreed
adjudications:                                   # answers to HIGH_RISK / POLICY_REVIEW
  - { finding_ref: "CRE-acme-3f8b21-07@v3#compliance.review.findings[f1]",
      decision: ACCEPTED | OVERRULED | REVISION_REQUIRED, reasoning }
```

### V.0 Approval and change are mutually exclusive

Revision 1 allowed `APPROVED_WITH_OVERRIDES` to authorise a modification that produced a new artefact version, then required a second decision on that version. The result was a record that read *"approved"* attached to bytes the reviewer had just asked to change — an artefact simultaneously approved and pending change. The rule is now sharp:

> **If a gate decision causes the reviewed artefact's bytes to change, the decision is `CHANGES_REQUESTED`.**
> **`APPROVED_WITH_OVERRIDES` is reserved for adjudications that leave the reviewed bytes untouched.**

| Outcome | Decision | Then what |
|---|---|---|
| Nothing to change; sign off | `APPROVED` | Campaign advances |
| Accept a `HIGH_RISK` finding as-is; relax a diversity target | `APPROVED_WITH_OVERRIDES` | Campaign advances. The override is the record of the acceptance; **no new version** |
| Swap a concept; correct a Product Truth field; rewrite a line | `CHANGES_REQUESTED` + `required_changes[]` / `authorized_changes[]` | A **new artefact version** is produced, then a **new decision** reviews and approves *that* version and hash |
| Stop | `REJECTED` | Terminal for the artefact |

The two byte-neutral cases work because their outputs live outside the artefact: a diversity relaxation is recorded in the gate's `overrides[]` and joined by the derived `resolution` (§O.5); a policy-risk acceptance is recorded in `adjudications[]` and read by the release check (INV-84). Neither writes into the plan or the creative — which is precisely what makes them byte-neutral, and it is why moving `diversity_audit.resolution` out of the Experiment Plan was a prerequisite for this correction rather than an unrelated tidy-up.

`CONCEPT_SWAP` is therefore **removed from the override kinds**: swapping a concept changes the Experiment Plan's bytes, so it is a `required_changes` entry under `CHANGES_REQUESTED`, and the resulting `experiment_plan@v2` gets its own decision.

INV-109 makes the rule mechanical: a decision of `APPROVED` or `APPROVED_WITH_OVERRIDES` with a non-empty `required_changes` or `authorized_changes` is schema-invalid. **No artefact can be simultaneously approved and required to change.**

### V.1 Staleness — how "approving V3 must not silently approve V4" works

A gate decision binds `(ref, hash)` pairs. A derived function answers coverage:

```
covers(gate, artefact_version) :=
    ∃ e ∈ gate.reviewed_artifacts : e.ref == artefact.ref
                                  ∧ e.hash == artefact.content_hash
```

If a creative is re-versioned after Gate 3, no decision covers the new version, so the transition to `RELEASED` is refused (INV-56) and the package cannot be released (INV-63). The condition is surfaced as **`APPROVAL_STALE`** — a derived report listing every artefact whose latest version is not covered by any decision. It is a computation, not a state, so it is always current and never needs a job to maintain it.

### V.2 What a gate may and may not do

| Action | Decision class | Representable? |
|---|---|---|
| Sign off with nothing to change | `APPROVED` | Yes |
| Accept a `LOW`/`MEDIUM` risk | `APPROVED_WITH_OVERRIDES` | Yes — `adjudications[].decision: ACCEPTED`, bytes untouched |
| Adjudicate `HIGH_RISK` / `POLICY_REVIEW_REQUIRED` | `APPROVED_WITH_OVERRIDES` | Yes — same |
| Relax a diversity target (G2) | `APPROVED_WITH_OVERRIDES` | Yes — `overrides[].kind: DIVERSITY_TARGET_RELAXATION`, `reason` required, resolution derived (§O.5) |
| **Release a regulated-category creative above T2** | — | **No. Removed in V1** — the creative was generated under a pinned T2 and no T3 creative exists to release (§I.5, INV-120) |
| Correct a Product Truth field (G1) | `CHANGES_REQUESTED` | Yes — then a new Product Truth version by an `OPERATOR` actor, then a new G1 decision on it |
| Swap a concept (G2) | `CHANGES_REQUESTED` | Yes — `required_changes[]`, then `experiment_plan@v2`, then a new G2 decision |
| Send a creative back for revision (G3) | `CHANGES_REQUESTED` | Yes — then a new creative version, then a new G3 decision |
| **Approve while requiring a change** | — | **No.** INV-109. |
| **Approve past a `HARD_BLOCK` leaving state unchanged** | — | **No — there is no field that expresses it.** INV-80. |
| **Raise a claim-freedom tier** | — | **No.** Tier is a pinned input to generation, not a review outcome. INV-120. |

The last three rows are the design points, and they are the same point three times: **a gate decides about what was produced; it cannot change the conditions under which it was produced.** A `HARD_BLOCK` is unrepresentable — no override kind exists for it, and `safety.overall` is recomputed from the artefact rather than stored as an approvable opinion. An approval that demands a change is unrepresentable because the two field groups cannot coexist. And a tier raise is unrepresentable because the pipeline that would have used the higher tier already ran.

**The override enum is exactly two kinds:** `DIVERSITY_TARGET_RELAXATION` and `POLICY_RISK_ACCEPTANCE`. Both are byte-neutral, both record a human accepting something the system correctly reported, and neither changes an input the generation already consumed.

INV-81 `reviewed_artifacts` is non-empty and every entry carries a `hash`. INV-82 *(rev.)* `decision: APPROVED_WITH_OVERRIDES` requires ≥ 1 override or adjudication, each with a written reason, and every `overrides[].kind` must be byte-neutral (INV-110). INV-83 a gate decision is never mutated; corrections are new records at a higher scope ordinal. INV-84 every `HIGH_RISK` / `POLICY_REVIEW_REQUIRED` finding on a released creative has a matching `adjudications[]` entry. INV-109 `APPROVED` and `APPROVED_WITH_OVERRIDES` require empty `required_changes` and `authorized_changes`; `CHANGES_REQUESTED` requires at least one of them non-empty. INV-110 `CONCEPT_SWAP` and any other byte-changing outcome may not appear as an override kind. INV-120 no gate decision may raise a claim-freedom tier; the `overrides[].kind` enum contains no value capable of it, and the regulated cap has no override path.

---

## W. Run Manifest

**PURPOSE** — Reconstruct what the system knew, consulted, decided and rejected, under which versions of every input and instruction.
**CANONICAL (the head and the events) + DERIVED (the manifest).** **Outside the eight artefact families** (§D.1).
**IDENTIFIER** — `RUN_ID`.

Revision 1 described the Run Manifest as an "append-only record" and then had it accumulate steps, sources, decisions, rejections, gates, errors, retries, cost and outputs for the entire length of a run, while `status` and `ended_at` were overwritten. That is a mutable document, not a record. It splits into two canonical parts and one derived view.

### W.1 The RUN head — immutable, written once at start

Everything below is known before the first model call, and none of it changes:

```yaml
run_id:             RUN-20260904T1132Z-a91c4e
campaign_id / product_id / brand_id
started_at:         "2026-09-04T11:32:00Z"
onboarding_level:   1
resumed_from_run_id: RUN-… | null
actor:              { kind: RUNTIME, credential_identity: "svc-orchestrator@org" }
inputs:
  campaign_brief:   { ref: "CMP-acme-3f8b21/campaign_brief@v1", hash: "sha256:…" }
  provided_assets:  [ { asset_id, content_sha256 } ]
pinned:                                       # the reproducibility contract
  knowledge:        { KNW-schwartz-persuasion: "sha256:…", … }
  config:           # all nine registries of §B.1
                    { evidence_policy: "sha256:…", deny_list: "sha256:…",
                      narrative_library: "sha256:…", format_profiles: "sha256:…",
                      category_profiles: "sha256:…", creative_taxonomy: "sha256:…",
                      experiment_variables: "sha256:…", diversity_targets: "sha256:…",
                      tool_capability: "sha256:…" }
  skills:           { product-intelligence: "1.1.0", market-intelligence-cl: "1.0.2",
                      creative-strategist: "1.3.0", script-engine: "1.2.0",
                      compliance-reviewer: "1.0.3" }
  prompts:          { <name>: "sha256:…" }
  models:           { product_intelligence: "claude-opus-5", hypothesis_pool: "claude-opus-5",
                      script_draft: "claude-opus-5", critic: "claude-opus-5" }
  cost_ceiling_usd: 120
```

A resumed run is a **new** run head with `resumed_from_run_id` set — which is why nothing here ever needs updating, and why the pinned versions of a resumed run are honestly allowed to differ from the original's.

### W.2 The run event log — everything that then happens

```yaml
RUN_STATUS_CHANGED     { from: RUNNING, to: AWAITING_GATE | COMPLETED | FAILED | ABORTED }
RUN_STEP_COMPLETED     { step_id: "E1#012", stage: EVIDENCE_EXTRACTION, mode: GENERATIVE,
                         model: "claude-opus-5", status: OK|RETRIED|FAILED,
                         input_refs: [SRC-…], output_refs: [EXT-…],
                         tokens: { input: 18240, output: 2110, cache_read: 51200 },
                         cost_usd: 0.31, started_at, ended_at }
RUN_DECISION           { stage, decision, rationale, alternatives_rejected: [ … ] }
RUN_REJECTION          { stage, kind: HARD_BLOCK | ESCALATION | PRESCREEN
                                | LOCK_VIOLATION | DIVERSITY_TARGET_UNMET
                                | LEDGER_RECONCILIATION | BINDING_INCOMPLETE,
                         item_ref, rule_id, reason, remediation }
RUN_ERROR              { step_id, kind, message }
RUN_RETRY              { step_id, attempt, reason }
```

**No `RUN_STATUS_CHANGED { PENDING → RUNNING }`.** Writing the RUN head *is* starting the run, so the fold begins at `RUNNING` and only transitions away from it are events. `PENDING` is gone from the state machine entirely (§X.2) — it described a moment at which no run record existed.

**Three run event types were removed as duplicates** (§G.0): `RUN_SOURCE_CONSULTED` (the evidence log's `SOURCE_ACCESSED` already carries `run_id`, and first acquisitions are SOURCE records with `created_by_run_id`), `RUN_COST_RECORDED` (cost is on the step event), and `RUN_OUTPUT_WRITTEN` (every artefact carries `created_by_run_id`, so `outputs[]` is a scan, not a second copy).

### W.3 The manifest — derived, and what a human actually reads

```yaml
run_manifest:                        # DERIVED_DETERMINISTIC — head ⊕ events ⊕ records
  <the entire RUN head>
  status:             RUNNING | AWAITING_GATE | COMPLETED | FAILED | ABORTED
  ended_at:           from the terminal RUN_STATUS_CHANGED
  steps:              [ … ]                   # RUN_STEP_COMPLETED events, in order
  sources_consulted:  [ … ]                   # SOURCE records with created_by_run_id == run_id
                                              # + SOURCE_ACCESSED events with this run_id;
                                              # quality_class joined at read time
  decisions:          [ … ]
  rejections:         [ … ]
  gates:              [ { gate_id, gate_type, decision, at } ]   # from GATE_DECISION records
  errors / retries:   [ … ]
  cost:               { by_stage, total_input_tokens, total_output_tokens,
                        total_usd, ceiling_usd, ceiling_breached }  # summed from steps
  outputs:            [ { ref, hash, type } ]  # artefacts with created_by_run_id == run_id
  artefact_versions:  { product_truth: "…@v2", research_dossier: "…@v2",
                        hypothesis_pool: "…@v1", experiment_plan: "…@v1",
                        creatives: [ "CRE-…@v3", … ], packages: [ … ],
                        meta_test_plan: "…@v1" }   # scanned by created_by_run_id
```

**`sources_consulted[].quality_class` is joined at read time, not stored** — the class is derived from the pinned evidence policy (§J.2), so a manifest rendered today under a corrected policy shows the corrected class *and* the policy hash that was in force during the run. Both facts stay available, which is the point of pinning.

**`rejections[]` is not optional and not a debug log.** It is the record of what the system refused to produce and why — the only way to later measure a false-block rate, and the difference between a compliance layer that is a control and one that is decoration (Phase 1 §W).

**`decisions[]` stores summaries, never reasoning traces.** `decision` + `rationale` + `alternatives_rejected` are written statements produced *as output*, not extracted from a model's thinking. INV-87 forbids any field whose content is a chain-of-thought transcript.

INV-85 every artefact carries `created_by_run_id`, and `outputs[]` is derived by scanning artefacts for that run — **no event duplicates the fact**. INV-86 a folded `COMPLETED` requires a terminal `RUN_STATUS_CHANGED` and every step event in a terminal status. INV-87 no persisted field may contain model reasoning traces. INV-88 `cost.ceiling_breached: true` requires a folded `status ∈ {FAILED, ABORTED}` or an operator override recorded in a `RUN_DECISION`.

---

## X. State Machines

Eight machines. Every one is small on purpose: a state exists only where a transition changes what the system is permitted to do.

**All eight states are derived, none is stored.** A state's *initial* value is a pure function of the entity's own record; every later value is that value folded with the entity's events (§G.0). No entity has a creation event, so a record with no events is already in a well-defined state. Each machine below specifies **which events may legally be appended from which folded state**, and an illegal transition is refused at append time rather than discovered later in a record someone edited. "Actor" is the component permitted to emit the event — and for CAMPAIGN and EXPERIMENT the driver is a **GATE_DECISION record**, not an event.

### X.1 CAMPAIGN

```
INTAKE ──► TRUTH_ESTABLISHED ──► CONCEPTS_APPROVED ──► PACKAGES_RELEASED
   │              │                     │                      │
   └──────────────┴─────────────────────┴──────────────────────┴──► ABANDONED (terminal)
```

**Campaign state folds over `GATE_DECISION` records directly — there is no campaign-state event.** The Campaign Brief establishes `INTAKE`; every advance is the existence of a covering decision record.

| Transition | Driven by | Condition |
|---|---|---|
| *(record written)* → `INTAKE` | The Campaign Brief | Initial state; no event |
| `INTAKE → TRUTH_ESTABLISHED` | `GATE_DECISION` record | A `G1_TRUTH` decision with `APPROVED` covering the current Product Truth version |
| `TRUTH_ESTABLISHED → CONCEPTS_APPROVED` | `GATE_DECISION` record | A `G2_CONCEPTS` decision covering the current Experiment Plan version |
| `CONCEPTS_APPROVED → PACKAGES_RELEASED` | `GATE_DECISION` record | A `G3_RELEASE` decision covering every package |
| `* → ABANDONED` | Operator | A `GATE_DECISION` with `REJECTED`, or an explicit operator record with a reason |

**Invalid:** any forward transition without a covering gate decision; any backward transition (a campaign that must redo research produces new artefact versions, not a state rewind).

### X.2 RUN

```
RUNNING ──► AWAITING_GATE ──► (new run) ──► COMPLETED (terminal)
   │
   ├──► FAILED (terminal)
   └──► ABORTED (terminal)
```

**`PENDING` is gone.** The RUN head is written when the run starts, so a run that exists is running; `PENDING` described a moment at which no record existed, which is not a state of anything. Five states, not six.

`AWAITING_GATE` is a real state, not a pause: the runtime is headless and a gate can take days (Phase 1 §D.1). A run resumed after a gate is a **new** run head with `resumed_from_run_id` set — the earlier run stays `AWAITING_GATE` forever, which is an accurate description of what happened to it.

### X.3 CLAIM

```
UNVERIFIED ──► VERIFIED ──┐
     │  ▲                 │
     │  └── DISPUTED ◄────┤
     ▼                    ▼
  REJECTED (t)        SUPERSEDED (t)
```

| Transition | Actor | Condition |
|---|---|---|
| `UNVERIFIED → VERIFIED` | Claim verifier (deterministic) | `CLAIM_STATUS_ASSERTED` with `result: SATISFIED` under a named `policy_ref` |
| `* → DISPUTED` | Ledger writer | One `CLAIM_DISPUTED` event naming both claims; the fold sets `DISPUTED` on each |
| `DISPUTED → VERIFIED` | Claim verifier | A `CLAIM_SUPERSEDED` on the conflicting claim, then a fresh `CLAIM_STATUS_ASSERTED` |
| `* → SUPERSEDED` | Ledger writer | `CLAIM_SUPERSEDED` naming the replacement |
| `* → REJECTED` | Operator or verifier | `CLAIM_REJECTED` with a recorded reason |

**Terminal:** `REJECTED`, `SUPERSEDED`. **Only `VERIFIED` may bind to a script line** (INV-26). A re-verification under a newer evidence policy is a **new** `CLAIM_STATUS_ASSERTED` event, so the history shows both the old and the new judgement rather than replacing one with the other.

### X.4 CREATIVE

```
DRAFT ──► VALIDATED ──► REVIEWED ──► LOCKED ──► RELEASED (t)
  ▲          │             │            │
  │          ▼             ▼            ▼
  └── REVISION_REQUESTED ──┴────────────┴──► REJECTED (t)
                                        └──► SUPERSEDED (t)
```

| Transition | Actor | Condition |
|---|---|---|
| `DRAFT → VALIDATED` | Safety validator | `safety.overall == PASS` (all five families) |
| `VALIDATED → REVIEWED` | Orchestrator | Critic `PASS`, compliance review present, feasibility `WITHIN_CEILING`, storyboard complete |
| `REVIEWED → LOCKED` | Lock service | INV-55; the event payload carries `locked_hash` |
| `LOCKED → RELEASED` | Gate service | A `G3_RELEASE` decision covering this exact hash, and — if the creative fills an experiment arm — a `SATISFIED` lock validation (INV-108) |
| `VALIDATED\|REVIEWED → REVISION_REQUESTED` | Critic or reviewer | `revision_count < 2`; else escalate |
| `REVISION_REQUESTED → DRAFT` | Orchestrator | Emitted against the **new** version; the superseded version stays `REVISION_REQUESTED` |
| `LOCKED → SUPERSEDED` | Orchestrator | A later version of the same creative reaches `LOCKED` |

**Invalid:** `DRAFT → LOCKED` (skips validation); `LOCKED → DRAFT` (a locked version is immutable — revision creates a new version); any write to a `LOCKED` version.

Note that state is per `(creative_id, version)`: `subject_ref` on a `CREATIVE_STATE_CHANGED` event carries the version, so v2 being `DRAFT` and v1 being `SUPERSEDED` are two folds, not a contradiction.

### X.5 PRODUCTION PACKAGE

```
DRAFT ──► LOCKED ──► RELEASED ──► SUPERSEDED (t)
                         └──────► WITHDRAWN (t)
```

`DRAFT → LOCKED` requires the source creative to be `LOCKED` and the re-projection to match byte-for-byte. `LOCKED → RELEASED` requires a covering Gate 3 decision. `WITHDRAWN` exists because a released package may need to be pulled (expired rights, policy change) without pretending it was never released.

### X.6 ASSET

Six states, transitions and conditions in §S.2. **Terminal:** `PRODUCTION`. The only backward transition is `PRODUCTION → PRODUCTION_ELIGIBLE` (withdrawal, recorded). Note that no transition ever lowers an asset's rights position — a downgrade is a new asset record, because rewriting a rights position would destroy the audit trail that the position is for.

### X.7 EXPERIMENT

Revision 1 ordered this `DESIGNED → VALIDATED → APPROVED`, which required lock validation to pass *before* Gate 2 — impossible, since no creative exists then. The corrected order follows the actual timeline (§O.6):

```
DESIGNED ──► APPROVED ──► BOUND ──► LOCK_VALIDATED ──► RUNNING ──► ANALYZED (t)
    │           │           │              │              │
    └───────────┴───────────┴──────────────┴──────────────┴──► INVALIDATED (t)
```

**Four of the five transitions are derived, not evented** — which is why `EXPERIMENT_STATE_CHANGED` was removed and only `EXPERIMENT_INVALIDATED` remains. An experiment's state is almost entirely a *consequence* of things recorded elsewhere.

| Transition | Driven by | Condition |
|---|---|---|
| *(record written)* → `DESIGNED` | The Experiment Plan version | Initial state; no event |
| `DESIGNED → APPROVED` | `GATE_DECISION` record | A `G2_CONCEPTS` decision covering the Experiment Plan version. Checks available at this point: INV-44, INV-46, INV-47 |
| `APPROVED → BOUND` | Binding projection | Every arm resolves to exactly one `creative_id@version` (`binding_result: COMPLETE`, INV-107) |
| `BOUND → LOCK_VALIDATED` | Lock validator (projection) | `lock_validation.result == SATISFIED` **and** `declared_variable_actually_differs == true` |
| `* → INVALIDATED` | `EXPERIMENT_INVALIDATED` event | A `LOCK_VIOLATION` the operator chooses not to fix, or an arm abandoned — the one transition that is a decision rather than a derivation |
| `LOCK_VALIDATED → RUNNING → ANALYZED` | Future performance layer | Out of V1 scope |

A package whose creative sits in an arm cannot be released while the experiment is short of `LOCK_VALIDATED` (INV-63). `RUNNING` and `ANALYZED` belong to the future performance layer; they exist now so that `evidence_level` has exactly one legal place to be assigned (INV-45) and so no back-fill is ever needed.

### X.8 HUMAN GATE

```
PENDING ──► DECIDED (t)          + derived condition: STALE
```

A gate decision record is immutable once written. `STALE` is **not a state** — it is the derived `covers()` computation of §V.1, always current, never maintained.

---

## Y. Validation Invariants

The complete minimum set future implementation must enforce: **120 invariants**, grouped by family. Each is deterministic — every one can be checked by code against stored data, with no model in the loop.

**Numbers are stable identifiers, not a scoreboard.** Across the two correction passes, twenty-nine invariants were revised in place and twenty were added; none was renumbered, because an invariant number will end up in code, in a rejection record and in a run manifest, and silently re-pointing it would corrupt every historical `rejections[]` entry that cites it. Revised entries are marked *(rev.)*. A retired number would never be reused; none was retired in this pass. **120 is a consequence of the design, not a target** — the correct number is whatever the minimum sufficient enforcement set turns out to be.

### Y.1 Campaign brief and intake

| # | Invariant | Enforced at |
|---|---|---|
| INV-01 | `sum(format_mix.values()) == batch.size` | Intake |
| INV-02 | Every `provided_assets[]` entry resolves to a registered ASSET | Intake |
| INV-03 | At onboarding level 1, ≥ 1 asset has `asset_type: PRODUCT_IMAGE` | Intake |
| INV-04 | Every `diversity_targets` value is an integer ≤ `batch.size` | Intake |
| INV-05 | No Campaign Brief field is written by a generative step | Write gate |

### Y.2 Identity

| # | Invariant | Enforced at |
|---|---|---|
| INV-06 | No model output may contain an identifier field; IDs are attached by the allocator after validation | Every generative step |
| INV-07 | Every ID matches its declared format pattern | Allocator, write gate |
| INV-08 *(rev.)* | A scope-ordinal is `max(existing ordinal in that entity namespace within that scope) + 1` — never a log-entry count; ordinals are monotonic, never reused, and no counter file exists | Allocator |
| INV-117 | Scope-ordinal allocation and the canonical write of the record bearing it are **one atomic operation**, performed under a **single writer per `(namespace, scope)`**. Concurrent allocation within one scope is forbidden in V1 and must be serialised by the orchestrator | Allocator, orchestrator |
| INV-118 | An ordinal is never reused, including after rejection, deletion or a failed write; gaps are permanent | Allocator |
| INV-09 | No identifier is derived from a filename, a filesystem path or a database row number | Allocator |
| INV-10 | Every reference resolves to an existing record; dangling references are rejected on write | Write gate, index build |
| INV-11 | Every artefact and fragment reference carries an explicit `@v<n>`; unversioned references are schema-invalid | Write gate |
| INV-12 | No stored reference resolves through a `latest` pointer | Write gate |

### Y.3 Epistemic states and Product Truth

| # | Invariant | Enforced at |
|---|---|---|
| INV-13 | `coverage` and `claim_freedom` are rejected if present in a model's output | Product Truth write |
| INV-14 *(rev.)* | `tier == T0` — identity **not established** — halts the run; no hypothesis, concept or creative may be created under that version. An `OBSERVED` identity is established and does not halt | Claim-freedom resolver |
| INV-15 *(rev.)* | Every `Fact` obeys F-R1…F-R9 | Schema + write gate |
| INV-16 *(rev.)* | A `Fact` with `state: VERIFIED` citing a `CLM-*` requires that claim's **folded** `status == VERIFIED` | Write gate |
| INV-17 | A fact about label wording and a fact about the product are separate fields with separate states | Schema |
| INV-89 *(rev.)* | A regulated `category_profile` caps the tier at T2 **unconditionally in V1**; no gate, override or human decision may lift it | Claim-freedom resolver |
| INV-90 | `coverage.<dimension>.state` equals the deterministic weakest-link roll-up; a mismatch is a rebuild error | Coverage service, index verify |
| INV-111 | An `INFERRED` fact may carry basis refs and must carry a note; it may never substantiate a claim, bind to a script line, raise a coverage dimension, or be promoted without a new artefact version at the required evidence class | Schema, safety validator |
| INV-113 | `T2` and `T3` require `coverage.identity.state == VERIFIED`; `T1` requires `OBSERVED` or better | Claim-freedom resolver |
| INV-114 | `PRICE_OFFER` is permitted only when `coverage.commercial.state == VERIFIED` | Claim-freedom resolver |

### Y.4 Evidence ledger

| # | Invariant | Enforced at |
|---|---|---|
| INV-18 | An OBSERVATION's `source_id` equals its EXTRACTION's `source_id` | E3 |
| INV-19 *(rev.)* | A folded `status: VERIFIED` requires a `CLAIM_STATUS_ASSERTED` event carrying `result: SATISFIED` and a named `policy_ref` | Claim verifier |
| INV-20 *(rev.)* | A SOURCE **deriving** to class A1/A2/B has a resolvable `snapshot_asset_id` | Ledger writer, index verify |
| INV-21 | Every OBSERVATION has `locator_origin` and a resolvable `extraction_id`; **every locator must appear in that extraction's `citation_set` or `quoted_spans`** | E3 reconciliation |
| INV-22 | An EXTRACTION with `schema_enforced: true` or `citations_enabled: false` is invalid | E1 writer |
| INV-23 | `kind: CUSTOMER_LANGUAGE` requires non-empty `verbatim` | E3 |
| INV-24 | `customer_language.audience_hint.state ∈ {OBSERVED, UNKNOWN, NOT_COLLECTED}` | Schema |
| INV-25 *(rev.)* | A dispute is one `CLAIM_DISPUTED` event naming both claims; the fold marks both `DISPUTED`, and an asymmetric dispute is unrepresentable | Ledger writer |
| INV-26 | A `DISPUTED`, `UNVERIFIED`, `REJECTED` or `SUPERSEDED` claim may not bind to a script line | Safety validator |
| INV-27 | An INSIGHT with empty `basis_observation_refs` is invalid | Dossier write |
| INV-28 | An insight's `statement` may not be identical to a single observation's `verbatim` | Dossier write |
| INV-29 *(rev.)* | An insight records `observation_count`, `distinct_source_count`, `source_classes_present` and `counter_evidence_count`, all computed from its refs. **No strength grade, tier or score is stored on an insight, and no field may be derived from a raw source count** | Dossier write |
| INV-104 | `source_id` is deterministic over `(locator_root, content_sha256)`; two records sharing content with different locators are distinct and both retained | Ledger writer |
| INV-105 | `owner_relationship` and `quality_class` are derived on every build and never accepted as written values | Source classifier, index build |

### Y.5 Audience and strategy

| # | Invariant | Enforced at |
|---|---|---|
| INV-30 *(rev.)* | `awareness_state` and `sophistication_state` may hold `INFERRED` **only** with non-empty `refs` and a note naming the inferential step | Schema |
| INV-112 | A bare inference (`INFERRED` with empty `refs`) is invalid on `awareness_state`, `sophistication_state` and every sensitive field — inference from category age, category convention or stereotype alone is refused | Schema |
| INV-31 | No audience field encodes ethnicity, religion, health status, sexual orientation, disability or precise age | Schema |
| INV-32 | Every `persuasion_projection.*_ref` resolves within the same dossier version | Dossier write |
| INV-33 | `mechanism_depth != NONE` requires the tier to permit `MECHANISM_EXPLANATION` | Dossier write |
| INV-34 | `reason_to_believe_strategy` is `NONE_AVAILABLE` when no permitted `VERIFIED` claim exists | Dossier write |

### Y.6 Hypothesis, concept, experiment

| # | Invariant | Enforced at |
|---|---|---|
| INV-35 | `falsification_condition` is non-empty | Pool write |
| INV-36 | `basis.insight_refs ∪ basis.observation_refs` is non-empty | Pool write |
| INV-37 | Every `claim_dependencies[]` entry resolves to an existing CLAIM | Pool write |
| INV-38 | `angle_mechanism` and `psychological_hypothesis` are registry values | Schema |
| INV-39 | `status: SELECTED` requires exactly one CONCEPT referencing this hypothesis | Plan write |
| INV-40 | A Concept's and a Creative's `dimensions` are byte-identical to the source hypothesis's | Plan / creative write |
| INV-41 | `reason_to_believe.territory ∈ claim_freedom.permitted_territories` | Plan write |
| INV-42 | Every concept `claim_refs[]` entry is `VERIFIED` at Gate 2, or a `prescreen.blocking_gap` names the missing evidence | Pre-screen |
| INV-43 | `format_fit` contains ≥ 1 `STRONG`/`WORKABLE` entry for a format in the campaign mix | Plan write |
| INV-44 | `declared_variable ∉ locked_variables`, and their union covers the experiment-variable registry | Experiment designer, Gate 2 |
| INV-45 *(rev.)* | `evidence_level` is never stored on a design; it is assigned only when the folded experiment state is `ANALYZED` | Schema |
| INV-46 | `scope` is non-null on every experiment design | Schema |
| INV-47 | `confounders_known` is non-empty | Experiment validator |
| INV-48 *(rev.)* | In a binding, each `creative_id` fills at most one arm campaign-wide, and each arm binds at most one creative | Binding projection |
| INV-49 *(rev.)* | `lock_validation.result == LOCK_VIOLATION` is a `HARD_BLOCK` on **release** and prevents the folded experiment state reaching `LOCK_VALIDATED` | Lock validator, release check |
| INV-50 | `diversity_audit.status: SATISFIED` requires every hard constraint `PASS` and every target `met` | Diversity solver |
| INV-51 *(rev.)* | A derived `resolution.chosen == RELAX_TARGET` requires a Gate 2 override of kind `DIVERSITY_TARGET_RELAXATION` with a written reason; the resolution is never stored in the plan | Gate service |
| INV-106 | An Experiment Plan version containing `creative_id`, `locked_variable_values`, `lock_validation` or `evidence_level` is schema-invalid | Schema |
| INV-107 | Every arm resolves `arm_key → creative_id@version` exactly once; `binding_result: INCOMPLETE` blocks release of every package in that experiment | Binding projection, release check |
| INV-108 | Lock validation runs on bound creatives, never on the design, and additionally asserts that the declared variable actually differs across arms | Lock validator |
| INV-52 | No `diversity_audit` field is written by a generative step | Write gate |

### Y.7 Creative, script, visual plan

| # | Invariant | Enforced at |
|---|---|---|
| INV-53 | No `lineage` field is written after the version is first persisted; no strategic feature is back-filled | Write gate |
| INV-54 | `quality.critic.verdict` and `compliance.review.verdict` enums exclude `HARD_BLOCK` | Schema |
| INV-55 *(rev.)* | A `CREATIVE_STATE_CHANGED` to `LOCKED` is refused unless safety `PASS`, critic `PASS`, feasibility `WITHIN_CEILING`, and every claim binding `BOUND` | Lock service |
| INV-56 *(rev.)* | A transition to `RELEASED` requires a Gate 3 decision covering this exact `content_hash` | Gate service |
| INV-57 | `revision_count <= 2`; the third request escalates instead of looping | Orchestrator |
| INV-58 | `hook.copy.text == script.segments[hook.copy.segment_ref].text` | Creative write |
| INV-59 | Every `generation_units[].duration_s <= ceiling_s` from the tool-capability config | Feasibility service |
| INV-60 | Scenes partition the timeline without gaps or overlaps; each belongs to exactly one generation unit | Feasibility service |
| INV-61 | Every multi-unit continuity anchor appears in the earlier unit's `anchor_out` and the later unit's `anchor_in` | Feasibility service |
| INV-91 | No `script.segments[].text` or `on_screen_text` contains a placeholder token | Script validator |
| INV-92 | Every segment's `kind`, `speaker_key` and `turn_index` satisfy the format profile | Script validator |
| INV-93 | Claim binding runs on the final localised text, not on any earlier draft | Safety validator |

### Y.8 Production package

| # | Invariant | Enforced at |
|---|---|---|
| INV-62 *(rev.)* | A package may not reference a creative whose **folded** state is not `LOCKED` | Assembler |
| INV-63 *(rev.)* | A transition to `RELEASED` requires a Gate 3 decision covering `source_creative.hash`, **and** — where the creative fills an arm — `binding_result: COMPLETE` with `lock_validation: SATISFIED` | Gate service, release check |
| INV-64 | Re-projection from `source_creative` + `projector_version` is byte-identical; a mismatch is a `HARD_BLOCK` | CI check, release |

### Y.9 Assets and rights

| # | Invariant | Enforced at |
|---|---|---|
| INV-65 *(rev.)* | An asset's initial state is a pure function of `origin.kind` on the record; there is no registration event and no writable initial-state field | Ingestion, fold |
| INV-66 *(rev.)* | Every `ASSET_STATE_CHANGED` event carries a non-empty `reason` and a complete `conditions_met[]`; `state_history` is the event slice and is never written directly | Registry |
| INV-67 | `derived_from` is acyclic | Registry |
| INV-68 *(rev.)* | A transition to `PRODUCTION_ELIGIBLE` requires the full five-part condition set, evaluated against every ancestor's folded state at event time | Registry |
| INV-69 *(rev.)* | A transition to `PRODUCTION` requires a Gate 3 decision reference in the event payload | Registry |
| INV-70 | `origin.kind == GENERATED` requires a non-null `generation` block | Registry |
| INV-71 *(rev.)* | `rights.consent.*` has no permissive default; an asset with no attestation event folds to `NONE` | Schema, fold |
| INV-72 | An asset tagged `no_cloning_source`, or with `consent.voice != VERIFIED`, may never be a `CLONING_SOURCE` | Safety validator |
| INV-94 | A `PRODUCTION` asset may not descend from any input that is not `AUTHORIZED` | Registry, safety validator |
| INV-95 | Two assets whose `rights_root_set`s intersect may not be cited as independent evidence about one another | Analysis layer |

### Y.10 Style and voice

| # | Invariant | Enforced at |
|---|---|---|
| INV-73 | `abstraction_level: SPECIFIC` is invalid | Schema |
| INV-74 | `cross_category_test: FAIL` blocks the profile from use | Style registry |
| INV-75 | A style `grammar` contains no claim, brand name, product name, price, offer or dialogue | Style registry |

### Y.11 Compliance and gates

| # | Invariant | Enforced at |
|---|---|---|
| INV-76 | `review.verdict` may not be `HARD_BLOCK` | Schema |
| INV-77 | `HIGH_RISK` / `POLICY_REVIEW_REQUIRED` requires a `human_adjudication` with a `gate_id` before release | Gate service |
| INV-78 | `policy_sources` is non-empty and fetched within the same run | Compliance reviewer |
| INV-79 | `META_APPROVED` may not appear as a stored value anywhere | Schema + deny-list |
| INV-80 | A `HARD_BLOCK` cannot be cleared by any gate decision — only by a new version that re-runs the validator to `PASS` | Gate service |
| INV-81 | `reviewed_artifacts` is non-empty and every entry carries a hash | Gate service |
| INV-82 *(rev.)* | `APPROVED_WITH_OVERRIDES` requires ≥ 1 override or adjudication, each with a written reason, and every override kind must be byte-neutral | Gate service |
| INV-83 | A gate decision is never mutated | Gate service |
| INV-84 | Every `HIGH_RISK`/`POLICY_REVIEW_REQUIRED` finding on a released creative has a matching adjudication | Release check |
| INV-109 | `APPROVED` and `APPROVED_WITH_OVERRIDES` require empty `required_changes` **and** empty `authorized_changes`; `CHANGES_REQUESTED` requires one of them non-empty. **No artefact is ever simultaneously approved and required to change** | Schema, gate service |
| INV-110 | `CONCEPT_SWAP`, or any other outcome that alters the reviewed artefact's bytes, may not appear as an override kind | Schema |

### Y.12 Runs, storage, index

| # | Invariant | Enforced at |
|---|---|---|
| INV-85 *(rev.)* | Every artefact carries `created_by_run_id`; a run's `outputs[]` is derived by scanning artefacts for that run, and **no event duplicates the fact** | Manifest fold |
| INV-86 *(rev.)* | A folded `COMPLETED` requires a terminal `RUN_STATUS_CHANGED` and every step event in a terminal status | Fold, run closer |
| INV-87 | No persisted field contains model reasoning traces | Write gate |
| INV-88 | `cost.ceiling_breached: true` requires a failed/aborted run or a recorded operator override | Cost governor |
| INV-96 *(rev.)* | Every artefact version **and every entity record** is immutable on write; an in-place modification is a repository integrity failure | Write gate, CI |
| INV-97 | `content_hash` recomputed over the canonical serialization equals the stored value | CI check |
| INV-98 | Every SQLite column traces to a documented canonical field path or a documented fold | Index builder |
| INV-99 | A full rebuild from the canonical root produces a byte-identical database content set | CI check |
| INV-100 | SQLite contains no value absent from the canonical store | Index verify |
| INV-101 | **No canonical record or artefact contains a field that is rewritten after it is written.** Anything that changes over time is an event payload, and its current value is a fold | Write gate, CI |
| INV-102 *(rev.)* | Domain events are append-only; `(log, event_seq)` is assigned by the append operation and never reused or reordered. **`event_seq` numbers events only** — it is never a source of entity identity, and atomic append is not a substitute for scope-ordinal allocation (INV-117) | Event writer |
| INV-103 | Every derived current state is reproducible by folding its log in `event_seq` order with a pure function; a fold that depends on wall-clock time or external state is invalid | Index builder, CI |
| INV-115 | Every configuration reference resolves to one of the nine registries of §B.1; an implicit or unlisted config dependency is a defect | Schema, run start |
| INV-116 *(rev.)* | No mutable allocator state exists anywhere in the canonical store; every ordinal is recomputed from the records that bear it | CI check |
| INV-119 | Entity creation is represented by the immutable entity record alone. **No domain event may duplicate a creation fact**; events represent subsequent change only | Schema, write gate, CI |
| INV-120 | No gate decision may raise a claim-freedom tier. The `overrides[].kind` enum contains no value capable of it, and a regulated category's T2 cap has no override path in V1 | Schema, gate service |

*Numbers INV-01 … INV-120 are all assigned, with no gaps and no duplicates. Twenty-nine were revised across the two correction passes and are marked* (rev.)*; none was retired, and no number was reassigned.*

---

## Z. SQLite Projection Model

**SQLite is `INDEX_ONLY`.** It exists to answer queries the filesystem answers badly: recursive lineage, cross-object joins, full-text retrieval, and the eventual performance join. It is not designed by normalising JSON — every table below is justified by a query the system actually needs.

**The event model changes what the index is *for*, and makes it more valuable, not less.** Under Revision 1, current state was read straight off a record. It is now a fold, and folding four logs on every question would be intolerable in a filesystem. So the index builder performs the fold **once, at build time**, and materialises current state as ordinary columns: `claims.status`, `assets.state`, `assets.rights_*`, `creatives.state`, `packages.state`, `experiments.state`, `campaigns.state`, `sources.access_count`, `runs.status`. Those columns are `INDEX_ONLY` in the strictest sense — every one is reproducible from its record's initial state replayed over its events, and INV-103 requires the fold to be pure.

**The fold has three inputs, not one.** The initial state comes from the **entity record** (no creation events exist), subsequent change comes from the **event log**, and for campaigns and experiments some transitions come from **`GATE_DECISION` records** and the binding projection. A builder that read only `domain_events` would produce campaigns permanently stuck at `INTAKE`.

### Z.1 Tables

| # | Table | Source canonical object | Index purpose (the query it serves) | Primary join key | Fields indexed | Fields **not** duplicated |
|---|---|---|---|---|---|---|
| 1 | `products` | Product registry + latest Product Truth | "which products exist, at what tier, with which coverage gaps" | `product_id` | `brand_id`, `category_profile_id`, `claim_freedom_tier`, `product_truth_version` | The `facts` tree, all `Fact` objects |
| 2 | `campaigns` | Campaign Brief | "campaigns for this product, their state and format mix" | `campaign_id` | `product_id`, `brand_id`, `market`, `state`, `batch_size` | Constraints, offer, notes |
| 3 | `runs` | RUN head ⊕ run event fold | "which run produced this artefact; cost and status by campaign" | `run_id` | `campaign_id`, `status` (folded), `started_at`, `ended_at` (folded), `total_usd` (folded) | `steps[]`, `decisions[]`, full pinned maps |
| 4 | `sources` | SOURCE ⊕ derived class ⊕ access fold | "sources by quality class and market; find every occurrence of one document" | `source_id` | `quality_class` (derived), `owner_relationship` (derived), `market`, `content_sha256`, `locator_root`, `access_count` (folded), `policy_ref` | `prose`, snapshot bytes |
| 5 | `observations` | OBSERVATION | "observations supporting this claim/insight; customer language by platform and stage" | `observation_id` | `source_id`, `extraction_id`, `subject_type`, `kind`, `platform`, `purchase_stage`, `market` | `locator` detail beyond kind |
| 6 | `claims` | CLAIM ⊕ evidence event fold | "which claims are VERIFIED at which class; what a creative depends on" | `claim_id` | `product_id`, `claim_type`, `status` (folded), `required_class`, `classes_present`, `verification_result`, `policy_ref`, `superseded_by` | `statement` full text (kept, it is short) |
| 7 | `claim_disputes` | `CLAIM_DISPUTED` events | "which claims conflict, on what basis" | `(claim_a, claim_b)` | both ids, `basis_observation_refs` | `note` |
| 8 | `claim_evidence` | CLAIM.`evidence_refs` | Edge table: claim ⋈ observation ⋈ source, for class roll-ups | `(claim_id, observation_id)` | both | — |
| 9 | `insights` | Research Dossier `insights[]` | "which observations underpin which hypothesis, transitively" | `insight_id` | `campaign_id`, `domain`, `observation_count`, `distinct_source_count`, `source_classes_present`, `counter_evidence_count`, `dossier_version` | `reasoning` |
| 10 | `hypotheses` | Hypothesis Pool | "spread across dimensions; which hypotheses were rejected and why" | `hypothesis_id` | `campaign_id`, the six `dimensions`, `status`, `prescreen_verdict` | `statement`, `predicted_effect`, `falsification_condition` |
| 11 | `concepts` | Experiment Plan `concepts[]` | "selected concepts and their hypothesis lineage" | `concept_id` | `campaign_id`, `hypothesis_id`, `selection_status`, `product_role` | `core_message` detail beyond the string |
| 12 | `creatives` | Creative Record ⊕ campaign event fold | **The DNA table.** "every creative with its full strategic feature vector, ready to join to performance" | `creative_id` | `campaign_id`, `concept_id`, `hypothesis_id`, `experiment_id`, `arm_key`, `creative_slot_key`, `run_id`, `product_id`, `brand_id`, the six `dimensions`, `format`, `narrative_pattern_id`, `style_id`, `duration_band`, `cta_kind`, `offer_ref`, `claim_freedom_tier`, `hook_entry_device`, `mechanism_depth`, `identification_strategy`, `state` (folded), `version`, `content_hash` | Script text, scenes, findings |
| 13 | `experiments` | Experiment design ⊕ binding ⊕ event fold | "what was tested, what was locked, at what evidence level" | `experiment_id` | `campaign_id`, `declared_variable`, `state` (folded), `binding_result`, `lock_result`, `evidence_level`, `scope_*` | `measurement_plan` detail |
| 14 | `experiment_arms` | Design arms ⊕ binding projection | "which creative filled which arm, and did the locks hold" | `(experiment_id, arm_key)` | `concept_id`, `creative_slot_key`, `role`, `planned_variable_value`, `bound_creative_id`, `bound_creative_version`, `lock_result` | `locked_variable_values` (kept as JSON text for audit) |
| 15 | `assets` | Asset record ⊕ asset event fold | "assets by state, rights position, expiry; find by hash" | `asset_id` | `asset_type`, `state` (folded), `content_sha256`, `rights_basis` (folded), `commercial_use` (folded), `expires_at` (folded), `consent_likeness` (folded), `consent_voice` (folded), `brand_id`, `product_id` | Media binaries; `state_history` and `rights_history` live in `domain_events` |
| 16 | `asset_lineage` | `derived_from[]` | **Recursive rights closure.** "which inputs produced this output; is any ancestor unauthorised or expired" | `(asset_id, parent_asset_id)` | both | — |
| 17 | `packages` | Production Package ⊕ event fold | "which package projects which creative version; release state" | `package_id` | `creative_id`, `creative_version`, `state` (folded), `released_by_gate` (folded) | The entire package body |
| 18 | `gates` | GATE_DECISION | "which decisions exist, of what kind, with what outcome" | `gate_id` | `campaign_id`, `gate_type`, `decision`, `decided_at`, `reviewer_id`, `override_kinds` | Comments, adjudication reasoning |
| 19 | `gate_coverage` | `GATE_DECISION.reviewed_artifacts[]` | **The `covers()` query.** "is this exact artefact hash approved; which artefacts are `APPROVAL_STALE`" | `(gate_id, ref)` | `ref`, `hash`, `artifact_type` | — |
| 20 | `domain_events` | All four event logs | "every **subsequent change** to this entity, in order; who did it and why" — the audit query, and the input to every fold. Creation is not here: it is the entity's own row (INV-119), so a full history is `domain_events` ∪ the record ∪, for campaigns and experiments, `gates` | `(log, event_seq)` | `event_type`, `subject_ref`, `occurred_at`, `actor_id`, `run_id` | `payload` (kept as JSON text; queried by extraction, not normalised) |
| 21 | `observations_fts` | OBSERVATION `verbatim` + `statement` | **FTS5.** Retrieval over customer language and research text | `observation_id` | `verbatim`, `statement` (separate columns) | Everything else |
| — | `index_meta` | The index itself | Rebuild contract (§AA) | — | — | — |

### Z.2 Tables deliberately **not** created

| Rejected | Why |
|---|---|
| `brands` | One row per brand; `brand_id` as a column on `products` and `creatives` answers every query. A table would be a foreign-key ceremony with no query behind it. |
| `styles` | Three rows, read from three YAML files. A join against three rows is not a query problem. |
| `narrative_patterns` | Same. |
| `product_truth_facts` (one row per field) | This is normalising JSON because normal forms exist. Nothing queries a single fact across products; the coverage roll-up is already on `products`. |
| `script_segments` | 10 creatives × ~22 segments = 220 rows to serve no current query. Add it when script-level retrieval is a real need, and add it to FTS at the same time. |
| `run_steps` | `RUN_STEP_COMPLETED` events are rows in `domain_events`; cost and status roll-ups are folded onto `runs`. A dedicated table would duplicate the event log. |
| `source_access_events`, `claim_events`, `asset_events`, `run_events` | Four tables where one `domain_events` table with an `event_type` discriminator answers every query, including the cross-entity one ("everything that happened in run X"). |
| `learnings`, `performance`, `meta_ads`, `publications` | No data exists. Interfaces are specified in §AB and built when there is something to put in them. |

**Twenty-two objects: 20 relational tables, one FTS5 virtual table, one metadata table.** Revision 1 counted 18 while leaving `gate_coverage` implicit inside the `gates` row — an undercount, corrected here rather than preserved. The correction pass added `domain_events` and `claim_disputes` and made `gate_coverage` explicit; nothing was added for symmetry.

### Z.3 Full-text search — audited

**FTS5 over observations only, in V1.** `verbatim` and `statement` are separate FTS columns so a search can be restricted to *what a customer actually said* rather than to E2's normalisation — which is the whole reason the two fields exist (§J.4).

**Not indexed:** raw binary assets (never), full source documents (they live as snapshot assets on disk; the observation carries the quoted span, which is what retrieval actually needs), script text (deferred — 10 creatives do not need search), claim statements (short, reachable by join, and `claims` is small).

The rule for adding an FTS table later: **index the text a human or a Skill will search by meaning, never text that exists only to be re-read in full.** A full source document belongs on disk with a locator, because retrieving 40 pages to answer a question the observation already answers is a cost with no benefit.

---

## AA. SQLite Rebuild Contract

```
   canonical filesystem (git-tracked JSON artefacts + records + event logs + YAML config)
                    │
                    │  1. enumerate:  every artefact version, every entity record,
                    │                 every event log, every config file
                    │  2. manifest:   sorted [ relative_path, content_sha256 ]
                    │  3. hash:       sha256 over the manifest rendering
                    ▼
            index builder (pure function, versioned)
              · load records      · fold event logs in event_seq order
              · derive classes    · compute projections
                    │
                    ▼
                 SQLite
```

### AA.1 `index_meta`

```yaml
index_schema_version:   5                 # bumped when a table or column changes
builder_version:        "index-builder@1.3.0"
fold_version:           "state-fold@1.0.0"    # bumped when any fold's semantics change
built_at:               "2026-09-04T16:10:22Z"
canonical_root_commit:  "git sha of the working tree at build time"
source_manifest_hash:   "sha256:…"        # the hash of step 3 above
event_log_heads:                          # last event_seq folded, per log
  { evidence: 417, asset: 63, campaign: 88, run: 1204 }
artefact_count:         { product_truth: 2, creatives: 13, packages: 10, … }
record_count:           { sources: 41, observations: 318, claims: 22, assets: 27, … }
event_count:            { evidence: 417, asset: 63, campaign: 88, run: 1204 }
status:                 BUILDING | VALID | STALE | FAILED
last_verify:            { at, result: MATCH | MISMATCH, mismatches: [] }
```

`event_log_heads` makes staleness cheap in the common case: if every log's head is unchanged and the manifest hash is unchanged, the index is current. It also permits an **incremental fold** later — appending events past a recorded head — without changing the contract, because a full rebuild must still produce the same result (INV-99).

### AA.2 Staleness and verification

- **Staleness** is detected by recomputing the source manifest hash and comparing. It is a cheap read of file metadata plus hashes, not a rebuild.
- **Verification** is the real guarantee: `rebuild --verify` builds into a temporary database and diffs the content of every table against the live one. A mismatch means either a canonical artefact or record was edited in place (INV-96, INV-101), an event log was reordered or truncated (INV-102), or a fold is not pure (INV-103). All four are integrity failures, and all four should fail CI.
- **A missing database is not an error.** `status` absent ⇒ build. This is the entire response to "SQLite was deleted" (§AE Case J).
- **A mismatch on a folded column is now the sharpest integrity signal in the system.** Under Revision 1 a hand-edited `claim.status` in a JSON file was undetectable — the file *was* the truth. Now the truth is the log, so an edited status simply loses to the fold on the next build, and the diff names the record.

### AA.3 What SQLite may and may not hold

**May hold:** derived joins, materialised roll-ups (coverage counts, dimension spreads), **every folded current state**, derived source classes, the experiment binding and lock result, FTS indexes, the recursive lineage closure, cached `covers()` results for gate staleness.

**May not hold:** any artefact body not present on disk, any record or event not present on disk, any operator decision, any gate decision, any generated text. (There is no allocator counter to exclude — none exists anywhere.) INV-100 states it; `rebuild --verify` proves it.

**Test for a proposed column:** *if the database were deleted right now, could this column be reproduced exactly?* If not, the value belongs in a canonical file and the column is a bug.

---

## AB. Future Performance / Learning Interfaces

Nothing here is built in V1. The obligation is that the current model makes it possible without back-filling.

### AB.1 The join, end to end

```
creatives.creative_id
   └── publications (future)  creative_id · package_id · meta_ad_id · post_id
                              · ad_set_id · campaign_external_id · published_at
          └── performance (future)  meta_ad_id · post_id · date · metric_name
                                    · numerator_value · denominator_value · value
                 └── experiment_arms.creative_id → experiments.experiment_id
                        └── learnings (future)
```

**`meta_ad_id` and `post_id` are separate `EXTERNAL_REFERENCE` fields and are never collapsed.** Social proof attaches to the post, not to the ad, so the Creative ⟷ Meta Ad relationship is genuinely many-to-many and the Post ID technique depends on the distinction (Phase 1 §O, ADR-030).

### AB.2 The feature vector recorded at creation, never back-filled

Present on `creatives` from the moment the Creative Record is first written: `campaign_id`, `product_id`, `brand_id`, `concept_id`, `hypothesis_id`, `experiment_id`, `arm_key`, `run_id`, the six `dimensions`, `format`, `narrative_pattern_id`, `style_id`, `duration_band`, `cta_kind`, `offer_ref`, `claim_freedom_tier`, `hook_entry_device`, `mechanism_depth`, `identification_strategy`, `promise_strategy`, `reason_to_believe_strategy`, `register`, plus the pinned versions of Product Truth, Research Dossier, knowledge, skills, prompts and models.

INV-53 forbids writing any of these after the version is persisted. Phase 1 §U states the reason plainly: *reconstructions become fiction.*

### AB.3 Metric definitions are data, with explicit formulas

```yaml
metric:
  name:        hold_rate
  numerator:   video_plays_15s
  denominator: video_plays_3s          # explicit — never "impressions or 3s views"
  source:      meta_api
  defined_at:  "2026-09-04"
```

Every metric referenced in a `measurement_plan` resolves to one of these. Phase 1 F5 showed the source corpus contradicting itself about what Hold Rate means inside one sentence; storing the formula rather than the name makes that class of error impossible to inherit.

**No threshold is stored anywhere in V1.** There is no field for a Hook Rate target, and adding one requires a design change, not a config edit (Phase 1 ADR-017).

### AB.4 Learning interface — defined, not built

```yaml
learning_id:            LRN-…
statement:              "what was learned"
scope:                  { product_id, category, market, audience_label, format, period }
evidence_level:         A | B | C | D
experiment_refs:        [ EXP-… ]
creative_refs:          [ CRE-… ]
performance_period:     { from, to }
confounders_carried:    [ … ]                # inherited from the experiment
contradicted_by:        [ LRN-… ]            # level D exists so confidence can fall
created_at / last_validated_at
```

`scope` is mandatory at every level (Phase 1 ADR-025). `evidence_level` is assigned at analysis, from `experiments.state == ANALYZED` — never at design. Level `D` exists so a learning can lose confidence, which a store that only accumulates cannot represent.

---

## AC. Future Production Interfaces

### AC.1 The boundary

| Concept | V1-Core or V1-Production? | Where it lives |
|---|---|---|
| Generation units | **V1-Core** | `creative.visual_plan.generation_units[]` — feasibility needs them, and the package must carry them |
| Continuity anchors | **V1-Core** | `creative.visual_plan.continuity_anchors[]` |
| Duration ceiling | **V1-Core config** | `config/tool_capability.yaml` with `verification_status` |
| Tool routing recommendation | **V1-Core** (advisory only) | `package.reports.routing_recommendation` |
| Tool routing *decision* | V1-Production | `asset.generation.tool` |
| Generation attempts, retries, retry reason | V1-Production | `asset.generation` + a future `generation_attempts` ledger |
| Generation cost | V1-Production | `asset.generation.cost_usd` |
| Output asset | V1-Production | ASSET with `origin.kind: GENERATED` |
| Voice resolution | V1-Production | `voice_specification.resolution` on a **new** package version |

The rule: **V1-Core records what must be true of the output; V1-Production records what actually happened.** Anything that is a fact about an attempt belongs to the attempt.

### AC.2 No unverified capability is assumed

`config/tool_capability.yaml` carries `verification_status: VERIFIED | VENDOR_STATED | UNVERIFIED` per capability, and the feasibility service records `ceiling_source` including that status. Lipsync and multi-speaker consistency are `UNVERIFIED` (Phase 1 §0.2), so `package.reports.routing_recommendation.risk_notes[]` carries that fact into production rather than letting a Podcast package imply a capability exists. Phase 1 ADR-019 requires a capability spike; this design ensures the spike updates one config file rather than a schema.

### AC.3 What is deliberately absent

No `generation_attempts` table, no retry-policy object, no cost-governor schema, no assembly manifest, no Higgsfield-specific field anywhere in the domain model. The tool identifier is a string on the asset's `generation` block, because a vendor-specific structure would have to be redesigned the moment the vendor is different from what Phase 1 could verify.
---

## AD. Data Walkthrough

**Purpose: detect missing relationships, not to produce an ad.** No product claim is invented. Every content value is `EXAMPLE_ONLY` or a structural placeholder. No file is created by this walkthrough.

**Input:** one product image + a brand name. **Market:** Chile. **Batch:** 10 = 5 UGC / 2 Podcast / 3 Animation.

### AD.0 Registration (before any run)

```
BRD-example                       operator-registered
PRD-example-producto-a            operator-registered, category_profile_id: CAT-generic
AST-1a2b3c4d5e6f                  immutable record: origin.kind USER_UPLOAD
                                  → state USER_PROVIDED_UNVERIFIED, derived from
                                    origin.kind alone. NO registration event
                                    (INV-65, INV-119)
                                  no rights attestation ⇒ folds to
                                  rights_basis UNKNOWN, consent.* NONE (INV-71)
                                  asset event log for this asset: EMPTY
```

The first structural finding: **the campaign can proceed on an unverified image.** Product Truth only needs to *observe* it. Nothing derived from it can ship until attested (§S.2) — a scheduling problem, not a blocker.

### AD.1 Intake

```
CMP-example-7c2d10                RANDOM-allocated (§E.1.2): the campaign id cannot
                                  be an ordinal within a scope it is creating
                                  campaign_brief@v1  (CANONICAL INPUT)
                                  → campaign state INTAKE, derived from the record
RUN-20260904T1132Z-a91c4e         RUN head written once: inputs + all nine config
                                  hashes + skills + prompts + models + cost ceiling
                                  → run state RUNNING, derived from the head.
                                    NO start event (INV-119); run event log EMPTY
  format_mix { UGC:5, PODCAST:2, ANIMATION:3 }   → INV-01 checks 5+2+3 == 10 ✓
  provided_assets [AST-1a2b3c4d5e6f]             → INV-02, INV-03 ✓
```

### AD.2 Phase I — Truth

```
step  vision analysis of AST-1a2b3c4d5e6f
      → OBS-producto-a-0001  kind FACT_STATEMENT   subject PRODUCT
        verbatim "<visible form>"     locator { kind: URL_SPAN, … }
        locator_origin E1_QUOTE       extraction_id EXT-a91c4e-001
      → OBS-producto-a-0002  label text, OBSERVED about the label

step  web research on the brand
      SRC-4f9a2c81d0b7 = sha256(locator_root ⏎ content_sha256)   ← occurrence identity
                           locator_root https://…  publisher_declared "…"
                           derived: owner_relationship MANUFACTURER → class A2
                           snapshot_asset_id AST-…  (INV-20)
      evidence@0001  SOURCE_ACCESSED  { source_id: SRC-4f9a…, at: … }
      EXT-a91c4e-003 (E1: citations ON, schema OFF)  ← persisted proof
      E2 → candidate observations (EPHEMERAL)
      E3 → OBS-producto-a-0003 … 0011   every locator ∈ EXT citation_set (INV-21)

step  claim formation
      CLM-producto-a-0001  claim_type PRODUCT_IDENTITY  (immutable record)
        evidence@0007  CLAIM_STATUS_ASSERTED
          { status: VERIFIED, required_class: A2, classes_present: [A2],
            result: SATISFIED, policy_ref: "config/evidence_policy@v4" }
          → folded status VERIFIED
      CLM-producto-a-0002  claim_type INGREDIENT_LIST
        no assertion event → folded status UNVERIFIED   (label not legible)

step  product_truth@v1
      facts.identity.product_name  { VERIFIED,  refs [CLM-producto-a-0001] }
      facts.visual.form_factor     { OBSERVED,  refs [OBS-producto-a-0001] }
      facts.composition.ingredients{ UNKNOWN,   note "label partly legible; no spec sheet" }
      coverage.identity      { state VERIFIED,     counts {...}, gaps [...] }
      coverage.composition   { state UNKNOWN,      gaps [ingredients, concentration] }
      coverage.outcomes      { state NOT_COLLECTED, gaps [...] }
      claim_freedom { tier T1, identity_basis VERIFIED,
                      permitted_territories [OBSERVABLE_ATTRIBUTE, CATEGORY_CONTEXT,
                      PROBLEM_CONTEXT, SITUATIONAL_NARRATIVE, IDENTITY_LIFESTYLE,
                      PRODUCT_INTERACTION] }
                      # PRICE_OFFER absent: coverage.commercial is UNKNOWN (INV-114)
```

**The two branches that must be shown, because the cold start depends on which one fires:**

| Branch | Result |
|---|---|
| **Brand research returns nothing.** Identity rests on the image alone: `product_name` and `category` are `OBSERVED`, not `VERIFIED`. | `identity_established` is **true** — `OBSERVED` counts. Tier computes to **T1**, `identity_basis: OBSERVED`, and the campaign proceeds on exactly the six evidence-safe territories above. `T2`/`T3` remain unreachable until identity is verified (INV-113), so no composition, mechanism or outcome claim can be attempted. **This is the minimum-input path, and it produces ten ads.** |
| **The image is illegible or the product is ambiguous.** `coverage.identity.state` is `UNKNOWN`, or a `required_for_identity` field is unresolved. | `identity_established` is **false** → **T0** → INV-14 halts the run and requests input. No hypotheses, no concepts, no scripts. |

Revision 1 collapsed these two branches into one and halted on both, which would have refused every product the web has never heard of. The cold start is productive *or* it stops — and it stops only when it does not know what the product **is**, never merely because it cannot corroborate it.

```
GAT-example-7c2d10-001   G1_TRUTH   reviewed_artifacts
                      [ { ref "PRD-example-producto-a/product_truth@v1",
                          hash "sha256:…" } ]
                      decision APPROVED      → campaign INTAKE → TRUTH_ESTABLISHED
```

### AD.3 Phase II — Market

```
~12 sources     SRC-…   classes: 1×A2 (brand), 3×B, 4×C (marketplace), 4×D (social)
~14 extractions EXT-a91c4e-004 … 017
~61 observations  of which 38 kind CUSTOMER_LANGUAGE   (verbatim REQUIRED, INV-23)
                  each with platform, register, purchase_stage, audience_hint(OBSERVED|UNKNOWN)

research_dossier@v1
  market_snapshot        Fact-shaped, most fields OBSERVED or UNKNOWN
  competitive_field      competitor_observation_refs → 9 observations (class E)
  customer_language      observation_refs → 38   spread{by_platform, by_purchase_stage}
  audience_model         awareness_state { PROBLEM_AWARE, INFERRED,
                                            refs [OBS-…, OBS-…, OBS-…],
                                            note "read from review vocabulary and the
                                                  explanation depth buyers ask for" }
                                            ← legal under revised INV-30: basis cited.
                                              Empty refs would be invalid (INV-112).
                         sophistication_state { STAGE_2, OBSERVED, refs [OBS-…] }
                         core fields Fact-shaped, evidence-linked or UNKNOWN
  persuasion_projection  pointers into audience_model + 5 strategy enums
  insights               INS-example-7c2d10-001 … 009   each ≥1 basis observation (INV-27)
                         basis { observation_count, distinct_source_count,
                                 source_classes_present, counter_evidence_count }
                         ← counts only; no strength grade (INV-29)
  research_gaps          [ { dimension core_problem, distinct_problems_evidenced 2 } ]
```

**`research_gaps` is written here, by a deterministic counter — before anything downstream needs it.** That is the relationship the walkthrough exists to check: the diversity solver two phases later must be able to cite *why* a target is unmet, and it can only do that if the count was taken at research time.

### AD.4 Phase III — Hypotheses, concepts, experiment

```
hypothesis_pool@v1     HYP-example-7c2d10-001 … 025      (Batch API)
                       each: dimensions{6} + falsification_condition (INV-35)
                              + basis refs (INV-36) + claim_dependencies
                              + required_territories
  spread.distinct      { awareness_state 4, core_problem 2, dominant_desire 3,
                         current_belief 3, angle_mechanism 5, psychological_hypothesis 6 }
  cluster_warning      true            ← core_problem 2 < target 4

prescreen (per hypothesis)
  4 hypotheses require OUTCOME_PROMISE → not in T1 permitted_territories
    → prescreen.deterministic.required_territories_permitted HARD_BLOCK
    → status REJECTED, recorded in run.rejections[] kind PRESCREEN
  → 21 survive, at the cost of 21 set comparisons and zero model calls

diversity solver
  hard_constraints    all PASS
  targets             core_problem  target 4  achieved 2  met false
                      limiting_factor "only 2 distinct core problems evidenced"
                      supporting_observation_ids [OBS-…]
                      research_gap_ref "research_dossier@v1#research_gaps[0]"
  status              INSUFFICIENT_EVIDENCE_FOR_DIVERSITY_TARGET
                      (NOT ValidationFailure — every hard constraint passed)

experiment_plan@v1
  concepts            CON-example-7c2d10-01 … 10   dimensions inherited (INV-40)
  alternates          CON-…-11, 12
  creative_slots      slot-01 … slot-10, each { concept_id, format }
  diversity_audit     as above; NO resolution field (it lives in the gate, §O.5)
  experiment_designs  EXP-example-7c2d10-01  declared_variable HOOK_COPY
                                          locked_variables [11 registry entries]
                                          arms a1 { concept CON-…-03, slot-01, CONTROL,
                                                    planned "question-led" }
                                               a2 { concept CON-…-03, slot-02, VARIANT,
                                                    planned "confession-led" }
                      EXP-example-7c2d10-02  declared_variable NARRATIVE_PATTERN
                                          arms a1..a3 → slot-04, slot-05, slot-06
                      ← NO creative_id anywhere; NO locked_variable_values;
                        NO lock_validation; NO evidence_level  (INV-106)
                      (4 slots sit outside any experiment — recorded as such
                       rather than pretended into one)
  meta_test_plan@v1   derived: ad-set structure, metric definitions with formulas,
                      confounders_known incl. delivery-optimisation, NO thresholds

GAT-example-7c2d10-002   G2_CONCEPTS
                      reviewed_artifacts [ experiment_plan@v1 hash, hypothesis_pool@v1 hash ]
                      decision APPROVED_WITH_OVERRIDES
                      overrides [ { kind DIVERSITY_TARGET_RELAXATION,
                                    target "experiment_plan@v1#diversity_audit…core_problem",
                                    reason "EXAMPLE_ONLY — accepted for first batch;
                                            additional research scheduled" } ]
                      required_changes []   authorized_changes []      ← both empty (INV-109)
                      ← the GATE_DECISION record IS the fact. No
                        GATE_DECISION_RECORDED event (INV-119)
  campaign state folds over gate decision records:
                      TRUTH_ESTABLISHED → CONCEPTS_APPROVED
                      derived resolution { chosen RELAX_TARGET,
                                           decided_at_gate GAT-example-7c2d10-002 }
                      ← joined from the gate; experiment_plan@v1 is untouched (INV-51)
```

**The Revision 1 finding is gone, and that is the point.** Revision 1's walkthrough discovered that a diversity relaxation changed the plan's bytes, forcing `experiment_plan@v2` and a second Gate 2 decision to cover it — an artefact approved at v1 while v2 was the one being used. Two corrections remove the problem at its root rather than papering it: `diversity_audit.resolution` is derived from the gate rather than stored in the plan (§O.5), and approval is now byte-neutral by definition (§V.0). One decision, one plan version, no circularity.

Had the reviewer instead **swapped a concept** — a byte-changing outcome — the decision would have been `CHANGES_REQUESTED` with `required_changes[]`, producing `experiment_plan@v2` and then a second, clean `APPROVED` decision covering v2's hash. Approved and change-required are never the same record.

### AD.5 Phase IV — Creatives ×10

```
CRE-example-7c2d10-01 … 10
  execution.format    5×UGC, 2×PODCAST, 3×ANIMATION   ← INV-01 mix satisfied
  script              format profile constrains segment kinds and speakers:
                        UGC       1 speaker, VOICEOVER|DIALOGUE
                        PODCAST   2 speakers, turn_index required, REACTION/INTERRUPTION
                        ANIMATION 0-1 NARRATOR, VISUAL_BEAT, no DIALOGUE
  hook                strategy | copy | visual | audio     hook.copy.text == s-001.text
  evidence.claim_bindings   run on the FINAL localised text
       CRE-…-04 asserts a composition statement → territory not in T1
         → SSV family CLAIM_EVIDENCE_BINDING result HARD_BLOCK
         → creative stays DRAFT; run.rejections[] kind HARD_BLOCK
         → resolution: rewrite the line (state change), not an approval
  quality.critic      PASS ×9, REVISE ×1 → v2 → PASS   revision_count 1
  compliance.review   LOW ×8, MEDIUM ×2                 (never HARD_BLOCK, INV-76)
  feasibility         UGC 4-5 generation units, PODCAST 9-11, ANIMATION 3-4
                      longest unit ≤ ceiling from config/tool_capability (VENDOR_STATED)
  visual_plan         scenes partition the timeline (INV-60);
                      continuity anchors bridge every seam (INV-61)
  experiment          CRE-…-01 declares { EXP-…-01, arm a1, slot-01, CONTROL,
                                          plan_ref experiment_plan@v1 + hash }
                      CRE-…-02 declares { EXP-…-01, arm a2, slot-02, VARIANT, … }

  state (folded, NOT stored — campaign event log):
    campaign@0011  CREATIVE_STATE_CHANGED  CRE-…-01@v1  DRAFT → VALIDATED
    campaign@0014  CREATIVE_STATE_CHANGED  CRE-…-01@v1  VALIDATED → REVIEWED
    campaign@0019  CREATIVE_STATE_CHANGED  CRE-…-01@v1  REVIEWED → LOCKED { locked_hash }
    → four events, ONE artefact version. Revision 1 would have needed four
      versions of identical content, or an in-place write.

experiment binding (DERIVED, after Phase IV — §O.6)
  EXP-example-7c2d10-01
    a1 → CRE-example-7c2d10-01@v1   a2 → CRE-example-7c2d10-02@v1
    binding_result COMPLETE                                    (INV-107)
    locked_variable_values EXTRACTED from each creative by field path
    lock_validation SATISFIED
    declared_variable_actually_differs true   ← hook.copy.text differs across arms
  → experiment state folds APPROVED → BOUND → LOCK_VALIDATED
```

### AD.6 Packaging and release

```
PKG-example-7c2d10-01-v1 … PKG-example-7c2d10-10-v1
  source_creative { ref CRE-…@v1|v2, hash }   projector_version "package-assembler@1.0.0"
  script, scene plan, continuity, style spec, voice spec  → duplicated in full
  reports.experiment_binding                  → the §O.6 projection for this arm
  assets, sources, creative record            → referenced by id + hash
  campaign@0031  PACKAGE_STATE_CHANGED  DRAFT → LOCKED  (re-projection identical, INV-64)

GAT-example-7c2d10-003  G3_RELEASE
  reviewed_artifacts  10 creatives + 10 packages, each with content_hash
                      + the experiment binding + lock validation reports
  adjudications       2 MEDIUM findings ACCEPTED with reasoning
  decision            APPROVED     required_changes [] authorized_changes []
  → PACKAGE_STATE_CHANGED ×10  LOCKED → RELEASED     (INV-63: binding COMPLETE,
                                                      lock SATISFIED, hash covered)
  → CREATIVE_STATE_CHANGED ×10 LOCKED → RELEASED
  → campaign CONCEPTS_APPROVED → PACKAGES_RELEASED   (folded over gate records)
  → run@0312  RUN_STATUS_CHANGED  RUNNING → COMPLETED
  → folded manifest: outputs[] = 24 artefact versions found by scanning for
                     created_by_run_id == this run (no per-output event)
```

### AD.7 Object and ID census for one campaign

| Object | Count | IDs minted |
|---|---|---|
| Brand, Product | 1, 1 | registered beforehand |
| Campaign, Run | 1, 1 | `CMP`, `RUN` |
| Assets | 1 + ~13 source snapshots | `AST` ×14 |
| Sources | ~13 | `SRC` ×13 |
| Evidence extractions | ~17 | `EXT` ×17 (scope-ordinal) |
| Observations | ~61 | `OBS` ×61 (scope-ordinal) |
| Claims | ~22 | `CLM` ×22 (scope-ordinal) |
| Insights | ~9 | `INS` ×9 (scope-ordinal) |
| Hypotheses | 25 | `HYP` ×25 (scope-ordinal) |
| Concepts | 12 (10 + 2 alternates) | `CON` ×12 (scope-ordinal) |
| Experiments | 2 | `EXP` ×2 (scope-ordinal) |
| Creatives | 10 (11 versions) | `CRE` ×10 (scope-ordinal) |
| Packages | 10 | `PKG` ×10 (**pure-derived**) |
| Gate decisions | 3 | `GAT` ×3 (scope-ordinal) |
| **Artefact versions written** | ~24 | — |
| **Domain events appended** | ~340 | none — `(log, event_seq)` |

Event volume by log, for one campaign, after the creation events were removed:

| Log | Events | Made of |
|---|---|---|
| `evidence` | ~25 | ~22 claim status assertions, ~1 dispute, ~2 re-accesses. First acquisitions are SOURCE records, not events |
| `asset` | ~3 | Attestations and promotions only; the 14 registrations are records |
| `campaign` | ~55 | ~34 creative transitions, ~20 package transitions. The 3 gate decisions are records |
| `run` | ~260 | ~200 `RUN_STEP_COMPLETED`, ~40 decisions, ~10 rejections, ~10 errors/retries. No start event, no cost events, no output events |

All are single-line appends to four files. **Appending is not the same as allocating**: an append needs atomicity, an ordinal needs serialisation, and §E.1.1 handles the second separately.

**Three structural findings, each resolved rather than noted.** Revision 1's walkthrough surfaced the Gate-2-override versioning circularity (§AD.4) — resolved by Corrections 3 and 6. Revision 2's surfaced the Experiment Plan's forward references, which is why `creative_slots[]` and the binding projection exist. This pass surfaces the third: three of the objects in this census were being written twice — once as a record and once as a creation event — and the walkthrough is the place where that shows up as literal duplication on the page. None of the three findings required a new artefact or a new identifier type.

---

## AE. Edge Case Validation

| Case | What catches it | Mechanism |
|---|---|---|
| **A — Only image + unknown brand details** | **The campaign proceeds.** Identity observed from the image is identity: `identity_established` is true, so the tier is **T1** with `identity_basis: OBSERVED` (INV-113), and the six evidence-safe territories are open — observable attributes, category context, the audience's problem, situational narrative, identity/lifestyle, product interaction. `PRICE_OFFER` is withheld unless commercial coverage is `VERIFIED` (INV-114). `composition`, `mechanism`, `outcome`, `timeframe`, `numeric` and `comparative` all stay forbidden because T2/T3 require verified identity *and* verified evidence. Nothing is guessed: category knowledge enters only as `INFERRED`, which F-R6 bars from claims and from raising any coverage dimension. **T0 fires only when the product is not identified at all** — an illegible image or an unresolved required identity field — and then INV-14 halts and requests input. Revision 1 halted on both branches; that was the bug Correction 5 fixed. |
| **B — Health product, manufacturer-only efficacy evidence** | The source derives to **A2** from `owner_relationship: MANUFACTURER`, computed from its own domain — regardless of what it says about itself (INV-105). `claim_type: MEDICAL_EFFICACY` requires **A1** with no `CONTEXT_ONLY` fallback, so no `CLAIM_STATUS_ASSERTED` event can carry `SATISFIED` and the claim folds to `UNVERIFIED`. Any script line asserting it fails `MINIMUM_EVIDENCE_CLASS` ⇒ **`HARD_BLOCK`**. Separately, `category_profile.regulated: true` caps the tier at **T2 with no override path** (INV-89, INV-120), so the pre-screen kills those hypotheses before a script exists and no reviewer can revive them at Gate 3. Three independent controls, and this is exactly Phase 1 F2 reproduced as a test. Note the fourth: if a later `evidence_policy` edit reclassified that publisher, the claim's verification event still records the policy it was judged under, so `rebuild --verify` surfaces the change instead of silently re-blessing the claim. |
| **C — Two external sources dispute the same claim** | Both observations are recorded (nothing is overwritten). Two CLAIM records exist, and **one** `CLAIM_DISPUTED` event names both; the fold marks both `DISPUTED`, so an asymmetric dispute is not merely forbidden but unrepresentable (INV-25). **INV-26** bars a `DISPUTED` claim from binding to a script line, so the dispute cannot be resolved by whichever source was read last. Both surface at Gate 1 in the Product Truth review. If the two sources are byte-identical documents hosted by different parties, they remain **two SOURCE records** with different classes (INV-104) rather than collapsing into one — which is the case Revision 1's content-only `source_id` would have silently merged. |
| **D — User-supplied voice without documented consent** | The record's `origin.kind: USER_UPLOAD` derives `USER_PROVIDED_UNVERIFIED`, and with no `ASSET_RIGHTS_ATTESTED` event the fold gives `consent.voice: NONE` (INV-71 — no permissive default; an asset with an empty event log is fully defined and fully unauthorised). Promotion to `AUTHORIZED` requires `consent.voice == VERIFIED` (§S.2), so it stays unauthorised. **INV-72** bars it from being a `voice_specification.reference_assets[].use: CLONING_SOURCE`. If it were used as a generation input anyway, the output is born `GENERATED_DRAFT` and cannot reach `PRODUCTION_ELIGIBLE` because an ancestor is not `AUTHORIZED` (INV-68, INV-94). Five layers now, because the rights position is also **append-only**: someone who later attests consent cannot erase the period during which there was none, and `rights_history` keeps the original absence on the record. |
| **E — Reference video used only for abstract style** | The Style Profile records `provenance.informed_by_asset_ids`, which is **not** a `derived_from` edge (§T.1). No lineage edge is created, so nothing generated under that style inherits the video's `REFERENCE` state. The safeguards are `abstraction_level ∈ {ARCHETYPE, FAMILY}` (INV-73), `cross_category_test: PASS` (INV-74), and INV-75 barring any claim, brand, product, price or dialogue from the grammar. If the profile fails the cross-category test, it is blocked from use — content leaked in and it is no longer style. |
| **F — Research supports two core problems, target is four** | `research_gaps` already recorded `distinct_problems_evidenced: 2` at research time. The solver reports `status: INSUFFICIENT_EVIDENCE_FOR_DIVERSITY_TARGET` with `achieved_values`, `limiting_factor`, `supporting_observation_ids` and `research_gap_ref`. This is **structurally distinct** from `VALIDATION_FAILURE`, which is reserved for hard-constraint breaches. The solver has no writable field that would make the target met, so fabrication is not a cheaper path than reporting (Phase 1 §C.17). The resolution is recorded in the **Gate 2 decision**, not written back into the plan (§O.5), so accepting the shortfall is byte-neutral: one `APPROVED_WITH_OVERRIDES` decision with a written reason (INV-51), no second gate round-trip, and the finding stays legible in the plan version the reviewer actually read. A later analysis joins plan and gate to tell diverse from diverse-by-relaxation. |
| **G — Chile localisation accidentally strengthens a claim** | Three controls, and the honest limit is stated. **(1)** Claim binding runs on the *final localised text* (INV-93), so a strengthened statement must re-bind; if it now asserts more than any `VERIFIED` claim permits, `CLAIM_EVIDENCE_BINDING` ⇒ `HARD_BLOCK`. **(2)** `LOCALISATION_CLAIM_INVARIANCE` diffs `claim_set_before` against `claim_set_after`; any addition, removal or qualification change ⇒ `HARD_BLOCK`. **(3)** Every required qualification must appear **verbatim** in the localised script (`required_qualifications[].result: MISSING` ⇒ `HARD_BLOCK`); a translated qualification is legal only via a human-approved `qualification_translations` entry on the claim. **Limit, stated plainly:** rewording that intensifies *within* the same bound claim and drops no qualification is not caught deterministically. It reaches `compliance.review` as `HIGH_RISK` judgement, and it is named in §AF as a residual risk. |
| **H — Creative updated after Gate 3 approval** | The Gate 3 decision binds `(ref, content_hash)`. A new creative version has a new hash, so `covers()` returns false: **INV-56** refuses the `RELEASED` transition, **INV-63** blocks the package's release, and the derived `APPROVAL_STALE` report lists the artefact. The old released package stays `RELEASED` and the new one sits `LOCKED` awaiting a decision — the system never silently swaps what a human approved. Under Correction 6 the follow-up is unambiguous too: the change was authorised by a `CHANGES_REQUESTED` decision, and the new version needs its own `APPROVED` decision. There is no path where one record both approves and requests. |
| **I — Experiment variant accidentally changes two variables** | The lock validator extracts `locked_variable_values` **from the bound Creative Records**, using the field paths in `experiment_variables` — it never reads an assertion about what was held constant, and the plan is now structurally incapable of carrying such an assertion (INV-106). Any locked variable with more than one distinct value across arms ⇒ `lock_validation.result: LOCK_VIOLATION` ⇒ **`HARD_BLOCK` on release** (INV-49, INV-108), blocking every package in that experiment. INV-44 additionally rejects a design whose declared plus locked variables do not cover the registry — "everything else is the same" is never implied. **And the mirror case is now caught too**: if the *declared* variable turns out identical across arms, `declared_variable_actually_differs: false` flags an experiment that tests nothing — a failure Revision 1 could not detect. |
| **J — SQLite is deleted completely** | Nothing is lost. `index_meta` is absent ⇒ `status` treated as build-required ⇒ the builder enumerates the canonical root, folds the four event logs in `event_seq` order, and rebuilds every current state along with every projection. INV-100 guarantees no value existed only in the database, INV-103 guarantees the folds are pure, and `rebuild --verify` is the CI check that keeps both true rather than assumed. The cost is a rebuild; the loss is zero. The event logs make this *stronger* than in Revision 1: current state is no longer a stored value that could have drifted from its history — it is derived from the history every time. |

---

## AF. Data Architecture Risks

| # | Risk | Level | Mitigation in this design | Residual |
|---|---|---|---|---|
| R1 | **Semantic claim intensification during localisation** that changes no claim reference and drops no verbatim qualification | **MEDIUM** | Re-binding on the final text, set diff, verbatim qualification check | Real. Reaches judgement, not determinism. §AE Case G |
| R2 | **A thin evidence base producing ten dimensionally-distinct but rhetorically identical concepts** | **MEDIUM** | Dimension spread audit, near-duplicate pairwise check, `research_gaps` | Semantic sameness is caught only by Gate 2's human read (Phase 1 §Q.4) |
| R3 | **Config drift** — the **nine** registries of §B.1 carry enforcement weight, and `evidence_policy` now *retroactively* determines source classes | **MEDIUM** | Hashed into every run head and every artefact's `inputs[]`; each claim's verification event records the policy it was judged under, so `rebuild --verify` surfaces any verification a policy edit has invalidated | A bad edit is attributable and detectable, not prevented. Config files need review discipline |
| R12 | **Fold-purity drift** — a fold that quietly depends on wall-clock time or on read order would make current state non-reproducible | **MEDIUM** | INV-103 requires purity; `rebuild --verify` diffs a fresh fold against the live index and fails CI on mismatch | The check must actually run; a fold bug is invisible until a rebuild happens |
| R13 | **Event-log volume** — ~1,770 events per campaign, dominated by `RUN_STEP_COMPLETED` | LOW | Four append-only files, one line per event; the index folds them once per build and can fold incrementally from `event_log_heads` | Log files grow monotonically; a very long-running account will eventually want rotation, which is a Phase 3+ concern |
| R14 | **A creative bound to an arm and then re-versioned** silently invalidates a completed lock validation | LOW | The binding is derived, so it is recomputed on the next build and `INV-107`/`INV-108` re-fire before release | Requires the binding to be recomputed rather than cached past a creative change |
| R4 | **`Fact` proliferation** — 60+ Fact objects per Product Truth is a lot of structure for a model to fill correctly | MEDIUM | Category profiles mark irrelevant fields `NOT_APPLICABLE` before generation; the model fills a narrowed projection | At level 1, most facts will be `UNKNOWN`/`NOT_COLLECTED`, which is correct but verbose |
| R5 | **`core_problem` free text defeating the spread count** | MEDIUM | Normalised string equality plus an explicit `core_problem_group` the strategist may set | Two phrasings of one problem counted as two unless the strategist groups them. Recorded, not inferred |
| R6 | **Immutability producing version sprawl** — a typo costs a version | LOW–MEDIUM | Accepted deliberately (§G.4) | ~24 artefact versions per campaign; a busy campaign may reach 40. Manageable in git |
| R7 | **Ledger scoped to product, but market research is campaign-specific** | LOW–MEDIUM | Observations carry `subject.type` and `market`; reuse across campaigns is opt-in by query, not automatic | A second campaign in a different market on the same product shares an ID space. DATA_ADR-003 records the tradeoff |
| R8 | **Package duplication drifting from the Creative Record** | LOW | The package is a pure projection; re-projection must be byte-identical (INV-64), checked in CI | Depends on the assembler staying pure — no clock, no randomness |
| R9 | **`locked_variable_values` extraction depending on config paths that drift from the schema** | LOW | `experiment_variables` paths are validated against the Creative Record schema at load | A renamed field silently breaks a lock check unless the validation runs |
| R10 | **FTS over `statement` being mistaken for FTS over customer speech** | LOW | `verbatim` and `statement` are separate FTS columns; INV-23 requires `verbatim` for customer language | A careless query could still search the wrong column |
| R11 | **Gate staleness computed rather than stored** | LOW | `covers()` is always current by construction | Requires the check to actually run before release; INV-56/63 place it on the release path |

**Not a risk this design carries:** silent evidence fabrication (E1/E2/E3 + INV-21), rights inferred from possession (§S.2), rights history overwritten by a later attestation (§S.1), a model raising an irreversible block (P10, INV-54/76), numeric confidence theatre (none exists — including on insights, after Correction 7), back-filled strategic features (INV-53), forward references into approved artefacts (INV-106), an artefact that is both approved and pending change (INV-109), a counter desynchronised from its data (INV-116), or unrecoverable index loss (§AA).

---

## AG. Simplification Pass

Applied after the first complete draft. The design is smaller than it was.

### AG.1 Objects removed

| Removed | Became |
|---|---|
| `ANGLE` object | `hypothesis.dimensions.angle_mechanism` + the angle block |
| `VARIANT` object | `(creative_id, experiment_id, arm_key, variable_value)` |
| `HOOK` ×4 objects | Four sibling keys under `creative.hook`, addressed by fragment path |
| `BRAND_SNAPSHOT` artefact | A section of Product Truth |
| `CUSTOMER_LANGUAGE_CORPUS` object | Observations with `kind: CUSTOMER_LANGUAGE` |
| `CREATIVE_DNA` object | A deterministic projection materialised as columns on `creatives` |
| `PERSONA` / `SEGMENT` objects | One Audience Model with a `label` field for later extension |
| `VOICE_PROFILE` object | `voice_specification`, embedded |
| `EVIDENCE_LEDGER` as an object | A store containing four record types |
| `MARKET_SNAPSHOT`, `PERSUASION_CONTEXT`, `OBJECTIONS`, `DESIRES`, `BELIEFS`, `ALTERNATIVES`, `SOPHISTICATION`, `AWARENESS` as artefacts | Fields of two embedded objects in the Research Dossier |

Twelve standalone sections in Master Prompt §17 became **two embedded objects, one addressable list, and two reference lists.**

### AG.2 Identifiers removed

Ten: `ANGLE_ID`, `VARIANT_ID`, `HOOK_ID` ×4, `SEGMENT_ID`, `SCENE_ID`, `BEAT_ID`, `ARM_ID`, `BRAND_SNAPSHOT_ID`, `CUSTOMER_LANGUAGE_ID`, `PERSONA_ID`, `CREATIVE_DNA_ID`. All replaced by the fragment-reference grammar (§E.5).

### AG.3 Fields removed from Master Prompt proposals

| Object | Dropped | Why |
|---|---|---|
| `Fact` | `source_refs` (merged into `refs`), `notes` → `note` | Two reference lists guarantee drift |
| `CLAIM` | `risk`, `qualification_required`, `commercial_use`, `version` | Duplicated truth, or computable, or the wrong storage regime |
| `HYPOTHESIS` | `counter_hypothesis`, `segment`, `risk`, and five dimension fields hoisted into `dimensions` | Overlap, unused capability, duplicated verdict |
| `CONCEPT` | `risk` | Duplicates `prescreen.verdict` |
| `ASSET` | `version`, top-level `licence`/`territory`/`expiry` | Assets are immutable; partial rights updates must be impossible |
| `SOURCE` | `document_index`, raw API envelope fields | Request-ordering artefacts, meaningless later |
| Coverage | Any aggregate score | Fake precision; the per-dimension state plus counts is what drives decisions |
| Everything | Every `0-1`, `0-10`, `0-100` field | Not one survives |

### AG.4 States removed

- Coverage `COMPLETE | PARTIAL | ABSENT` → the epistemic enum plus counts.
- Field state `PENDING_VERIFICATION` → `CLAIM.status: UNVERIFIED`.
- Field state `ABSENT` → a *value*, not a state.
- Asset `RIGHTS_EXPIRED` state → a derived date comparison.
- Gate `STALE` state → a derived `covers()` computation.
- Creative pipeline states compressed from ten to eight (`SAFETY_VALIDATED`+`CRITIC_PASSED`+`COMPLIANCE_REVIEWED`+`PLANNED` → `VALIDATED`+`REVIEWED`).
- **Every stored state field** → a fold over the event log. Eight state machines, zero stored state columns in the canonical store (Correction 1).
- Insight `strength: DIRECT | INDIRECT` → four measured counts (Correction 7).

### AG.5 SQLite tables removed

Six: `brands`, `styles`, `narrative_patterns`, `product_truth_facts`, `script_segments`, `run_steps`. Each was removable because no current query needed it and every one of them was normalising JSON rather than solving a query problem. The correction pass added three (`domain_events`, `claim_disputes`, and `gate_coverage` made explicit) and declined four more (`source_access_events`, `claim_events`, `asset_events`, `run_events` — one discriminated table serves them all). Result: **22 objects, not 25 and not 32.**

### AG.6 The correction pass, as a simplification

Four of the eight corrections made the design **smaller**, not larger:

| Correction | Net effect |
|---|---|
| 1 — event log | Removed `state`, `state_history`, `rights` mutation and eleven accumulating manifest fields from six object schemas; added **one** event envelope and four logs. Removed the last mutable object in the store |
| 3 — experiment binding | Removed four fields from the Experiment Plan; added no artefact and no identifier |
| 6 — gate semantics | Removed one override kind (`CONCEPT_SWAP`) and moved `diversity_audit.resolution` out of the plan entirely |
| 7 — insight strength | Removed an enum and the arbitrary rule that produced it |

Corrections 2, 4, 5 and 8 added precision without adding objects: one extra field on `SOURCE`, one relaxed rule on `Fact`, one clearer tier boundary, one consolidated taxonomy file that replaced an undeclared dependency.

### AG.7 What was kept despite the pressure to cut

Complete word-for-word scripts · storyboards and shot lists · the Evidence Ledger and claim→evidence binding · the six-value epistemic enum · the four-record epistemic separation (Source/Observation/Insight/Hypothesis) · Concept/Creative/Variant/Ad separation · the four-way hook split · the separate critic · the persisted E1 extraction record · `rejections[]` · version pinning of every input.

These are the reason the system is a Creative Experimentation OS rather than an ad generator (Phase 1 §Y). The E1 extraction record in particular looks like overhead until the first time someone asks whether a locator was real.

---

## AH. Phase 2 Decision Log

| ID | Question | Recommendation | Rationale | Trade-off | Status |
|---|---|---|---|---|---|
| DATA_ADR-001 **(rev.)** | Storage regimes | **Three: versioned artefacts, immutable entity records, append-only domain events.** Current state is a fold; nothing is rewritten in place | Revision 1's two regimes could not express change without mutating something it called immutable | A fold to run at index time; one more concept to learn | PROPOSED |
| DATA_ADR-002 | Versioning scheme | **Monotonic integer + content hash** | Integer orders for humans; hash identifies and binds approvals | Semver's expressiveness forgone | PROPOSED |
| DATA_ADR-003 | Evidence Ledger scope | **Product-scoped, with `subject.type` and `market` on every record** | Claims about a product are reusable across campaigns; a campaign-scoped ledger would re-mint IDs for the same fact and break future joins | Market research for a second market shares the product's ID space | PROPOSED |
| DATA_ADR-004 | **Brand Snapshot location** | **A section of Product Truth, not the Research Dossier** | Same procedure, same shape, produced pre-Gate-1 by `product-intelligence`; the dossier does not exist yet at that point in the flow | Diverges from Master Prompt §4's suggestion | **ACCEPTED — approved by the user in the external audit pass** |
| DATA_ADR-005 | Insight storage | **Embedded in the Research Dossier, addressable by ID** | Born there, consumed by hypotheses, meaningless alone | Citing an insight pins a dossier version | PROPOSED |
| DATA_ADR-006 | Concept storage | **Embedded in the Experiment Plan** | Master Prompt §4 item 5; concepts are what Gate 2 approves | Same version-pinning consequence | ACCEPTED_FROM_PHASE_1 |
| DATA_ADR-007 | Sub-object identity | **Fragment references, not minted IDs** | Removes 10 ID types; version is mandatory in every reference | Local keys may be renumbered between versions | PROPOSED |
| DATA_ADR-008 | Missing-data enum | **Six values; `ABSENT` is a value, `PENDING_VERIFICATION` is a claim status** | Minimum set that keeps "not researched" distinct from "verified absence" | Writers must choose correctly among six | PROPOSED |
| DATA_ADR-009 | Coverage representation | **Epistemic state (weakest link) + counts + gaps; no aggregate** | A score averages a missing price with missing efficacy evidence | No single number for a dashboard | PROPOSED |
| DATA_ADR-010 **(rev.)** | Source identity | **`SOURCE_ID` = `sha256(locator_root ⏎ content_sha256)` — occurrence identity. `content_sha256` remains the separate content-dedup key. `ASSET_ID` stays random-allocated** | Content-only identity collapsed a regulator-hosted and a manufacturer-hosted copy of the same bytes into one record, destroying the A1/A2 distinction by an identifier choice. Provenance and content are now separate fields, not one hash | Two sources with identical bytes appear twice; consumers who want dedup group on `content_sha256` | PROPOSED |
| DATA_ADR-011 | E1 output persisted | **Yes — `EVIDENCE_EXTRACTION` is a canonical record** | Without it, "the locator came from E1" is unprovable after the run | Storage cost; one more record type | PROPOSED |
| DATA_ADR-012 | Script polymorphism | **Shared core + format profile config** | Adding a format is a YAML file, not a migration | The profile loader becomes load-bearing | PROPOSED |
| DATA_ADR-013 | Package duplication | **Full duplication of production-facing content; references for assets, sources and the creative** | Self-sufficiency is the contract; binaries and evidence bodies are not | Package size; drift risk answered by INV-64 | PROPOSED |
| DATA_ADR-014 **(replaced)** | **Gate decision that changes the artefact it reviewed** | **A decision that changes the reviewed bytes is `CHANGES_REQUESTED` with `required_changes[]` / `authorized_changes[]`; a new version is produced; a new decision approves that exact version and hash. `APPROVED_WITH_OVERRIDES` is reserved for adjudications that leave the bytes untouched** — exactly two kinds after Correction 9: policy-risk acceptance and diversity relaxation. **No artefact is ever both approved and required to change** (INV-109) | The original formulation let one record read "approved" while demanding a change. Moving `diversity_audit.resolution` out of the plan (§O.5) made the common override genuinely byte-neutral, so the clean rule costs nothing | A byte-changing gate outcome always costs a second decision record — which is the correct price for an unambiguous audit trail | **ACCEPTED — user rejected the original DATA_ADR-014 and specified this replacement** |
| DATA_ADR-015 | Serialization | **JSON canonical; YAML for authored config; Markdown for review** | Determinism and schema support beat readability where a hash binds an approval | Raw script JSON is unpleasant to read; the render answers it | PROPOSED |
| DATA_ADR-016 | Schema strategy | **Pydantic v2 → generated JSON Schema; model-facing schemas are narrowed projections** | One definition, two consumers; IDs and derived fields removed from model-facing schemas | Couples the schema layer to Python | PROPOSED |
| DATA_ADR-017 **(rev.)** | Policy as data | **Exactly nine registries, listed once in §B.1: `evidence_policy`, `deny_list`, `narrative_library`, `format_profiles`, `category_profiles`, `creative_taxonomy`, `experiment_variables`, `diversity_targets`, `tool_capability`.** Every config reference resolves to this list (INV-115) | Revision 1 said "six" in one place and listed eight in another, and referenced a ninth (`psych_hypotheses`) that appeared in no list — an implicit dependency. `creative_taxonomy` absorbs it along with angle mechanisms, hook devices and claim territories | Nine files carrying enforcement weight (R3); one more file than the implicit eight | PROPOSED |
| DATA_ADR-018 | Duration ceiling | **Config with `verification_status`, never a constant** | Phase 1 §0.2 records ~15 s as vendor-stated; ADR-019 requires a spike | Feasibility depends on a file being correct | ACCEPTED_FROM_PHASE_1 |
| DATA_ADR-019 **(rev.)** | SQLite projection size | **22 objects: 20 relational + 1 FTS + 1 metadata, each justified by a query** | Six candidate tables removed for having no query behind them; `domain_events` and `claim_disputes` added by Correction 1; `gate_coverage` made explicit rather than left implicit inside `gates` | Some future query will need a rebuild-with-new-schema | PROPOSED |
| DATA_ADR-020 | FTS scope | **Observations only in V1 (`verbatim` and `statement` as separate columns)** | Customer language is the retrieval need that exists; scripts and sources are not | Script search deferred | PROPOSED |
| DATA_ADR-021 **(rev.)** | Immutability strictness | **Immutable on write, not on first reference — and now without exception, because state changes cost an event rather than a version** | Reference counting on a filesystem store is a distributed-state problem. Revision 1's strictness was only affordable once state left the artefact | A typo costs a version; a state change does not | PROPOSED |
| DATA_ADR-022 | Audience segmentation | **One Audience Model in V1, with a `label` field** | Nothing currently consumes segments; the field makes it additive later | A genuinely two-segment campaign needs the extension first | PROPOSED |
| DATA_ADR-023 | Learning / performance | **Interfaces defined, tables not created** | Building against imagined data | The first ingestion will refine the interface | ACCEPTED_FROM_PHASE_1 |
| DATA_ADR-024 | `core_problem` as free text | **Free text + optional `core_problem_group`** | An enum would force real findings into pre-existing buckets — a quiet fabrication | Spread counting depends on normalisation or explicit grouping | PROPOSED |
| **DATA_ADR-025** | **Event envelope granularity** | **One typed `DOMAIN_EVENT` envelope with an `event_type` discriminator, across four scoped logs — not four event record types and not four identifier types** | The audit invited `SOURCE_ACCESS_EVENT` / `CLAIM_EVENT` / `ASSET_EVENT` / `RUN_EVENT`. One envelope covers every case, keeps the cross-entity query ("everything in run X") to a single table, and adds no ID | A `payload` whose schema varies by `event_type`; the discriminated union must be validated per type | **PROPOSED (new — audit)** |
| **DATA_ADR-026 (rev.)** | **Identifier allocation authority** | **Five authorities: registry, content-deterministic, random-allocated, scope-ordinal, pure-derived. A scope-ordinal is `max(existing in that namespace and scope) + 1`, allocated and written as one atomic operation under a single-writer-per-scope guarantee. `CAMPAIGN_ID` is random-allocated with a readable brand prefix. `PACKAGE_ID` alone is pure-derived** | "Derived handle" hid an allocation concern; "log-positional" then answered it with the wrong mechanism — `count(log)+1` is not concurrency-safe, and embedded entities are not log entries at all. `max+1` over the namespace is correct, and V1 forbids concurrent writers rather than pretending the problem away. `CAMPAIGN_ID` could not be campaign-scoped without circularity | Allocation is serialised per scope; concurrent campaign execution would need a lock, a CAS, or a move to random IDs. `CMP-acme-3f8b21` is less pretty than `CMP-acme-001` | **PROPOSED (rev. — final freeze pass)** |
| **DATA_ADR-027** | **Experiment binding representation** | **Declaration on the Creative Record (`experiment.arm_binding`); resolution and lock validation as a `DERIVED_DETERMINISTIC` projection keyed by `(experiment_id, arm_key)`. No ninth artefact, no new identifier** | Gate 2 approves a design; creatives exist only afterwards. The declaration is a fact about the creative and belongs with it; the validation is computed from artefacts and must never be stored where it could drift | The binding must be recomputed whenever a bound creative is re-versioned (R14) | **PROPOSED (new — audit)** |
| **DATA_ADR-028** | **`INFERRED` may carry basis refs** | **Yes. `refs` on an `INFERRED` fact are interpretive basis, not substantiation. Bare inference stays legal for genuinely conventional readings, and is forbidden on `awareness_state`, `sophistication_state` and every sensitive field** | Forbidding basis forced a false choice between discarding an interpretation's evidence and mislabelling it `OBSERVED`. The rule that matters — an inference may not substantiate a claim — is unchanged (F-R6) | Reviewers must read `state`, not just `refs`, to know whether a value is a fact or a reading | **PROPOSED (new — audit)** |
| **DATA_ADR-029** | **Insight strength** | **Removed. Replaced by `observation_count`, `distinct_source_count`, `source_classes_present`, `counter_evidence_count`** | `DIRECT` defined as "≥2 observations from ≥2 sources" turned a source count into an evidence grade. One A1 statement can support a direct reading; two class-D comments do not | A reviewer must interpret four counts instead of reading one label — which is the point | **PROPOSED (new — audit)** |
| **DATA_ADR-030** | **`T0` semantics** | **`T0` means identity is not established. `OBSERVED` identity qualifies as established and lands at `T1`; `T2`/`T3` still require `VERIFIED` identity** | Revision 1 halted whenever identity was not externally verifiable, which would have refused the system's own minimum input and contradicted Phase 1 §M | An observed-only identity carries slightly more downstream risk than a verified one — bounded by the six evidence-safe territories and recorded in `identity_basis` | **PROPOSED (new — audit)** |
| **DATA_ADR-031** | **Regulated-category ceiling** | **`regulated == true` caps the tier at T2 in V1 with no override path. `REGULATED_TIER_RELEASE` is removed. Regulated T3 is deferred to a future pre-creative regulatory workflow that produces an explicitly versioned effective-policy input consumed before concepts exist** | The tier is pinned onto a Creative at generation, and pre-screen, concept design and script generation all run under it. A Gate 3 override would be relabelling a T2 creative, not releasing a T3 one. Claim freedom is an input, not a review outcome | Regulated categories cannot make outcome claims in V1 at all, however good the evidence. Correct, and the future workflow is the place to change it | **PROPOSED (new — freeze pass)** |
| **DATA_ADR-032** | **Concurrency posture for identifier allocation** | **Single writer per `(namespace, scope)` is a V1 constraint, stated rather than assumed. Allocation and the canonical write are one atomic operation. Concurrent allocation within a scope is forbidden, not made safe** | `count(log)+1` was not concurrency-safe and atomic append does not make it so. Making it safe needs a lock, a CAS or a serialising service — none worth building for a single-operator V1. Recording the constraint keeps the later choice available | Concurrent campaign execution needs a mechanism decision before it is possible; the alternative (random ids for these entities) stays open | **PROPOSED (new — freeze pass)** |
| **DATA_ADR-033** | **Creation vs change** | **Entity creation is represented by the immutable entity record and nothing else. Domain events represent subsequent change only. No creation event exists anywhere** | `record + creation event` is a dual write across two files with no transaction available in a git-tracked store; either half can land alone. Deriving initial state from the record removes the failure mode instead of guarding it | The fold has three inputs (record, events, and gate decisions for campaign/experiment) rather than one; a builder reading only the event log would be wrong | **PROPOSED (new — freeze pass)** |

**No Phase 1 ADR is reopened.** DATA_ADR-006, 018 and 023 restate Phase 1 decisions in data terms and are marked `ACCEPTED_FROM_PHASE_1`. DATA_ADR-004 is `ACCEPTED` by user approval; DATA_ADR-014 was rejected in its original form and replaced with the user's specified rule. **Thirty-three ADRs in total.**

---

## AI. Phase 3 Handoff Requirements

Phase 3 owns repository design and migration. What it inherits from Phase 2, and what it must decide:

### AI.1 Phase 3 must decide

1. **Directory layout for the canonical store** — where campaigns, products, ledgers, event logs, config and rendered Markdown live. Phase 2 deliberately specifies no paths.
2. **Version file naming** — this design requires only that every version is separately addressable and never overwritten. `v1.json` / `v2.json` versus a `versions/` subdirectory is Phase 3's call.
3. **Event log file format and layout** — four logs, scoped `evidence` (per product), `asset` (global), `campaign` (per campaign), `run` (per run). **Phase 2 requires only that an append is atomic and that `event_seq` is the append position within its own log**; JSONL versus one file per event is Phase 3's call. That choice determines four things and only four: atomic append mechanics, `event_seq` allocation, replay/fold mechanics, and corruption/recovery characteristics.

   **It does not determine entity identifier allocation.** Entity scope-ordinals are not event-log positions and never read one. They are governed exclusively by §E.1.1, DATA_ADR-026, DATA_ADR-032, INV-08, INV-117 and INV-118 — `max(existing ordinal in that entity namespace and scope) + 1`, under the V1 single-writer-per-scope constraint. A Phase 3 decision about log layout cannot make entity identifiers safer or less safe.
4. **Media root and git-ignore boundaries** — the asset registry is git-tracked JSON; the payloads are not.
5. **Migration execution** of Phase 1 §I steps M1–M7, including the `knowledge/methodology/` quarantine and provenance front-matter.
6. **Where the nine config registries live**, and how their hashes are computed and pinned.
7. **Whether `PRE_FLIGHT_AUDIT.md` and the phase documents move** — Phase 2 recommends they do not.

### AI.2 Phase 3 inherits, unchanged

- The three storage regimes, the version block (§G.2) and the event envelope (§G.0).
- The canonical serialization rules (§G.7) — these determine every content hash and must not be altered casually.
- The identifier formats and the **five** allocation authorities — registry, content-deterministic, random-allocated, scope-ordinal, pure-derived (§E.1, §E.2, §E.3).
- **Two distinct atomicity requirements, which must not be conflated.** Revision 1 required "the allocator counter state must be canonical and crash-safe"; there is no counter now, but the guarantee did not simply move to the append operation — it split in two:

  **A. Domain events.** Appending an event is atomic, and `event_seq` is allocated by and belongs to the event log alone. It numbers events; it never numbers entities.

  **B. Scope-ordinal entity allocation.** Resolving `max + 1` and writing the canonical record that bears the ordinal is **one atomic operation**, performed under the single-writer-per-`(namespace, scope)` constraint (INV-117).

  **Atomic event append is not the mechanism that guarantees entity-ID uniqueness.** Two writers can each append perfectly well-formed events and still allocate the same ordinal; atomicity yields a valid file, serialisation yields a unique number. Phase 3 inherits both requirements and must satisfy them separately.
- The nine config registries of §B.1 as *content*, if not as location.
- The rebuild contract's requirement that a canonical root be enumerable with stable relative paths (§AA) — **this is the one place repository layout touches the data model**, because the source manifest hash is computed over relative paths.

### AI.3 Open items Phase 3 should carry forward, not resolve

- Whether a second market on the same product warrants splitting the ledger (R7, DATA_ADR-003).
- The `qualification_translations` mechanism for localised qualifications (§AE Case G) needs a concrete shape before the script engine is built in Phase 6.
- Event log rotation, if an account ever accumulates enough runs for the `run` log to become unwieldy (R13). Not a V1 concern.
- Whether the binding projection should be cached with an invalidation rule or always recomputed (R14). Phase 2 specifies "always recomputed"; a performance argument could revisit it once volumes are real.

*(The two items Revision 1 listed here as needing approval — DATA_ADR-004 and DATA_ADR-014 — were both resolved by the user in the external audit pass and are no longer open.)*

---

## AJ. External Audit Correction Pass

**Date:** 2026-09-04 · **Trigger:** external data-architecture audit · **Scope:** `docs/PHASE_2_DATA_ARCHITECTURE.md` only · **Phase 3 not started.**

Eight corrections were raised plus an identifier-terminology cleanup and two user decisions. **All eight are accepted.** Three (1, 3, 6) identified genuine internal contradictions — places where the document asserted a property it then violated. Two (2, 5) identified design errors with concrete failure cases. Two (4, 7) identified epistemically unsound rules. One (8) identified an inconsistency and an undeclared dependency.

### AJ.1 The two that mattered most

**Correction 1 was the most serious**, because it was a contradiction at the foundation. The document declared two storage regimes — versioned-immutable and append-only — and then required a `SOURCE` to grow, a `CLAIM` to change status, an `ASSET` to accumulate rights and states, a `RUN MANIFEST` to accrete nine field groups, and a `CREATIVE` to walk five states. Every one of those is an in-place rewrite of something called immutable, and every invariant that rests on immutability was therefore resting on nothing. The fix is one mechanism applied uniformly — immutable record plus append-only events plus a derived fold — and it turned out to *remove* structure rather than add it, including the last mutable object in the store.

**Correction 3 was the most consequential for the pipeline.** An Experiment Plan approved and hashed at Gate 2 contained `creative_id` and `locked_variable_values` for creatives that Phase IV had not yet written. The document's own walkthrough admitted it in a parenthesis. There were only two ways to honour that shape, and both broke a stated guarantee: mutate the artefact a human signed, or re-version it and leave the approval covering a version nobody used. Splitting *design* from *binding* dissolves the problem, and the binding needed no new artefact and no new identifier.

A general lesson worth recording, because it caught three of the eight: **a document can state a property and violate it in the same section without either statement looking wrong in isolation.** The check that finds these is mechanical — for every field, ask whether it changes over time, and whether anything in it can be known when it is written.

### AJ.2 Corrections and verdicts

| # | Correction | Verdict | Nature | Sections affected | DATA ADRs |
|---|---|---|---|---|---|
| 1 | Append-only lifecycle contradiction | **Accepted** | **Internal contradiction.** Six record types required mutation while being described as immutable or append-only | §A, §B (P4–P6, P12), §C.1–C.2, §D, §G.0 *(new)*, §G.1, §G.4, §J.1, §J.5, §J.8, §P.1, §P.5, §R.2, §S.1, §S.4, §V, §W, §X (all), §Y, §Z, §AA, §AD, §AE | 001 rev., 021 rev., **025 new** |
| 2 | Source identity collapses provenance | **Accepted** | **Design error with a concrete failure.** A regulator-hosted and a manufacturer-hosted copy of one PDF would have merged, destroying the A1/A2 distinction | §E.2, §E.3, §E.4, §J.1, §J.2, §J.8, §Z, §AD.2, §AE Case C | **010 rev.** |
| 3 | Experiment Plan forward references | **Accepted** | **Internal contradiction.** Gate-2-approved artefact referenced objects that do not exist until Phase IV | §C.1–C.2, §O.1–O.7, §P.2, §P.5, §R.2, §X.7, §Y.6, §Z, §AD.4–AD.6, §AE Case I | **027 new**, 019 rev. |
| 4 | `INFERRED` may have evidence basis | **Accepted** | **Epistemically unsound rule.** Forced a choice between discarding an interpretation's basis and mislabelling it as observation | §B (P15), §F.1, §F.2 (F-R3, F-R9), §F.3, §F.4, §I.4, §L.1 (INV-30), §Y.3, §Y.5, §AD.3 | **028 new** |
| 5 | Cold start must remain viable | **Accepted** | **Design error contradicting Phase 1 §M and the product's minimum input.** Observed-only identity halted the run | §A, §I.4, §I.5, §I.6, §Y.3, §AD.2, §AE Case A | **030 new** |
| 6 | Gate decision semantics | **Accepted** | **Internal contradiction.** A record could read "approved" while requiring a change | §O.5, §V.0 *(new)*, §V.2, §Y.11, §AD.4, §AE Cases F and H | **014 replaced** |
| 7 | Insight strength by source count | **Accepted** | **Evidence score in disguise.** A count determined a grade | §K.2, §K.3, §Y.4, §Z, §AD.3 | **029 new** |
| 8 | Config registry inconsistency | **Accepted** | **Inconsistency + undeclared dependency.** "Six" vs eight listed vs a ninth referenced but never listed | §A, §B.1 *(new)*, §B (P12), §C.1, §M.1, §P.2, §W.1, §Y.12, §AF R3, §AI | **017 rev.** |
| — | Identifier terminology ("derived handles") | **Accepted** | Mislabelling that concealed an allocation concern | §E.1, §E.2, §E.3, §E.6, §G.4, §AD.7, §AI.2 | **026 new** |
| — | DATA_ADR-004 (Brand Snapshot in Product Truth) | **Approved by user** | Decision | §I.1, §AH | 004 → `ACCEPTED` |
| — | DATA_ADR-014 (original form) | **Rejected by user** | Replaced by Correction 6 | §V.0, §AH | 014 replaced |

### AJ.3 DATA ADRs changed and added

**Revised (5):** 001 (three regimes), 010 (source occurrence identity), 017 (nine registries, named), 019 (22 projection objects), 021 (immutability affordable because state left the artefact).
**Replaced (1):** 014 (gate decision semantics).
**Status changed (1):** 004 `PROPOSED — REQUIRES APPROVAL` → `ACCEPTED`.
**Added (6):** 025 (one event envelope, not four types), 026 (allocation authorities; scope-ordinals), 027 (binding as declaration + projection), 028 (`INFERRED` may cite basis), 029 (insight counts, not grades), 030 (`T0` means unidentified).

**Total: 30 DATA ADRs after this pass** (33 after the final freeze pass, §AJ.8.3). No Phase 1 ADR was reopened.

### AJ.4 Invariant changes

| | Count |
|---|---|
| Before | 100 |
| Revised in place (number kept, text changed) | **26** — INV-08, 14, 15, 16, 19, 20, 25, 29, 30, 45, 48, 49, 51, 55, 56, 62, 63, 65, 66, 68, 69, 71, 82, 85, 86, 96 *(marked* (rev.) *in §Y)* |
| Added | **16** — INV-101 … INV-116 |
| Retired | **0** |
| Renumbered | **0** |
| After | **116** (the final freeze pass then takes it to 120 — see AJ.8) |

Numbers were deliberately **not** renumbered. An invariant number ends up in code, in a `rejections[]` entry and in a run manifest; re-pointing INV-49 at a different rule would silently corrupt every historical rejection citing it. Retired numbers would never be reused. **116 is a consequence, not a target** — the audit's point that "100 invariants is not a success criterion" is accepted, and the count moved because the rules did.

The sixteen additions, by correction: **1** → INV-101 (nothing rewritten in place), 102 (append-only ordering), 103 (fold purity), 116 (no mutable allocator state). **2** → INV-104 (occurrence identity), 105 (derived classification). **3** → INV-106 (no forward references), 107 (binding completeness), 108 (validation on bound creatives). **4** → INV-111 (inference may cite basis, never substantiate), 112 (no bare inference on awareness/sophistication/sensitive). **5** → INV-113 (tier/identity ladder), 114 (`PRICE_OFFER` conditional). **6** → INV-109 (approval and change mutually exclusive), 110 (override kinds byte-neutral). **8** → INV-115 (closed config list).

### AJ.5 Object and identifier count changes

| | Before | After | Why |
|---|---|---|---|
| Canonical artefact types | 8 | **8** | Unchanged. No correction required a ninth artefact — deliberately, per the audit's constraint |
| Canonical system records | 2 | **2** | Run head + Gate Decision (the manifest became a derived view over the head) |
| Canonical stores | 3 | **4** | Event Log added |
| First-class entity types | 19 | **20** | `DOMAIN_EVENT` added |
| Identifier types | 19 | **19** | **Unchanged.** Events use `(log, event_seq)`; the binding is keyed, not identified. Four invited event-ID types were declined |
| — of which pure-derived | 3 | **1** | `PACKAGE_ID` only; `GATE_ID` and `EXTRACTION_ID` reclassified as scope-ordinal |
| Config registries | 6 / 8 (inconsistent) | **9** | One authoritative list; `creative_taxonomy` absorbs the undeclared `psych_hypotheses` |
| SQLite projection objects | 18 (undercounted) | **22** | +`domain_events`, +`claim_disputes`, `gate_coverage` made explicit |
| Validation invariants | 100 | **116** | See AJ.4 (the final freeze pass takes it to 120) |
| State machines | 8 | **8** | Same eight; all now derived rather than stored, and EXPERIMENT reordered |
| Creative Record sections | 12 | **11** | `state` left the artefact |

### AJ.6 Remaining unresolved decisions

**None requiring user approval.** Both items Revision 1 flagged were resolved by the user in this pass: DATA_ADR-004 approved, DATA_ADR-014 rejected and replaced.

Four items remain open as **Phase 3+ engineering choices**, none of which changes a data contract:

1. Event log file format and layout (§AI.1 item 3) — Phase 2 constrains only atomicity and ordinal semantics.
2. Whether a second market on one product warrants splitting the Evidence Ledger (R7, DATA_ADR-003).
3. The concrete shape of `qualification_translations` for localised qualifications (§AE Case G) — needed before Phase 6.
4. Whether the binding projection is cached with invalidation or always recomputed (R14) — Phase 2 specifies always recomputed.

### AJ.7 Readiness after the second pass

Every one of the eight corrections was applied and traced through each section referencing the changed concept, not only the section defining it — which is why the correction table lists twenty-plus sections for Correction 1. The walkthrough and all ten edge cases were re-run; three (A, F, I) produced materially better outcomes. A subsequent external consistency audit then found three further structural issues and one count mismatch, recorded below.

---

### AJ.8 Final Freeze Correction Pass

**Date:** 2026-09-04 · **Trigger:** final external consistency audit · **Scope:** `docs/PHASE_2_DATA_ARCHITECTURE.md` only · **Phase 3 not started.**

Three structural issues and one editorial mismatch. **All four accepted.** Two (9, 11) are contradictions that Revision 2 *introduced* while fixing something else — the characteristic failure mode of a correction pass, and the reason a third audit was worth running. One (10) is a claim that was simply false. One (12) is a typo.

#### AJ.8.1 Corrections and verdicts

| # | Correction | Verdict | Nature |
|---|---|---|---|
| 9 | `REGULATED_TIER_RELEASE` is temporally impossible | **Accepted — removed entirely** | **Contradiction.** A Gate 3 override purported to raise a tier that had been pinned onto the Creative Record before generation. Pre-screen, concept design and script generation all ran under T2; there was no T3 creative to release, only a T2 creative being relabelled |
| 10 | ID allocation lacked real atomicity semantics | **Accepted — replaced with scope-ordinal + single-writer** | **False claim.** `count(log)+1` is not concurrency-safe: two writers both read `N`. Atomic append guarantees a well-formed file, not a unique number. Separately, `CAMPAIGN_ID` was circular (a campaign-scoped ordinal establishing the campaign scope) and embedded entities are not entries in any event log |
| 11 | Duplicated canonical creation events | **Accepted — creation events removed** | **Contradiction.** `record + creation event` is a dual write across two files with no transaction available; either half can land alone |
| 12 | AJ.3 said DATA_ADR-019 was "21 projection objects" | **Accepted — corrected to 22** | Editorial |

#### AJ.8.2 Sections affected

| Correction | Sections |
|---|---|
| 9 | §I.3, §I.5, §I.6, §V (override enum), §V.0, §V.2, §Y.3, §Y.11, §AE Case B, §AD.4, §AH |
| 10 | §A, §B (P6), §E.1, §E.1.1 *(new)*, §E.1.2 *(new)*, §E.2, §E.3, §G.4, §Y.2, §Y.12, §AD.1, §AD.7, §AI.1, §AI.2, §AH |
| 11 | §G.0, §G.1, §S.1, §S.2, §S.4, §V, §W.2, §W.3, §X (preamble, X.1, X.2, X.6, X.7), §Y.9, §Y.12, §Z, §AD.0, §AD.1, §AD.4, §AD.6, §AD.7, §AE Case D, §AH |
| 12 | §AJ.3 |

#### AJ.8.3 DATA ADR changes

**Revised (2):**
- **DATA_ADR-025** — event envelope: the envelope is unchanged, but the event *inventory* drops from 22 types to 16, and the envelope is now explicitly for change only.
- **DATA_ADR-026** — allocation authority: "log-positional" retired in favour of **scope-ordinal**; `max(namespace, scope) + 1` under a single-writer guarantee; `CAMPAIGN_ID` moved to random allocation.

**Added (3):**
- **DATA_ADR-031** — regulated categories are capped at T2 in V1 with **no override path**; regulated T3 is deferred to a future pre-creative regulatory workflow producing a versioned effective-policy input, not designed here.
- **DATA_ADR-032** — **single-writer per allocation scope** is a V1 constraint, recorded rather than assumed; concurrency would need a lock, a CAS or a move to random identifiers.
- **DATA_ADR-033** — **entity creation is the immutable record; domain events represent subsequent change only.** No creation event exists anywhere.

**Total: 33 DATA ADRs.** No Phase 1 ADR reopened.

#### AJ.8.4 Invariant changes

| | Count |
|---|---|
| Before this pass | 116 |
| Revised in place | **3** — INV-08 (ordinal is `max+1`, not a log count), INV-65 (initial asset state derives from the record), INV-85 (`outputs[]` derived by scanning artefacts), plus INV-89, INV-102 and INV-116 sharpened |
| Added | **4** — INV-117 (atomic allocate-and-write under a single writer per scope), INV-118 (ordinals never reused), INV-119 (no creation event may duplicate a record), INV-120 (no gate may raise a claim-freedom tier) |
| Retired | **0** |
| Renumbered | **0** |
| After | **120** |

Across both passes: 29 revised, 20 added, none retired, none renumbered.

#### AJ.8.5 Counts after the final freeze pass

| | Rev. 2 | Final | Why |
|---|---|---|---|
| Canonical artefact types | 8 | **8** | Unchanged |
| Canonical system records | 2 | **2** | Unchanged |
| Canonical stores | 4 | **4** | Unchanged |
| First-class entity types | 20 | **20** | Unchanged |
| Identifier types | 19 | **19** | Unchanged in count; reclassified — 5 registry, 1 content-deterministic, **3** random-allocated (`CAMPAIGN_ID` joins `RUN_ID`, `ASSET_ID`), **9** scope-ordinal, 1 pure-derived |
| Domain event types | 22 | **16** | Six removed as duplicates of canonical records |
| Config registries | 9 | **9** | Unchanged |
| SQLite projection objects | 22 | **22** | Unchanged; AJ.3's "21" was a typo |
| Validation invariants | 116 | **120** | See AJ.8.4 |
| State machines | 8 | **8** | Unchanged; RUN loses `PENDING` (6 states → 5) |

#### AJ.8.6 Final contradiction scan

Run explicitly against the seven checks the audit specified:

| # | Check | Result |
|---|---|---|
| 1 | Any regulated-category path above T2 | **None.** The CAP rule is unconditional; `T2`/`T3` gating is in one function; no gate action can reach it |
| 2 | Any ID depending on a scope that does not yet exist | **None.** `CAMPAIGN_ID` is random; every scope-ordinal is allocated inside a product, campaign or run that already exists |
| 3 | Any claim that `count(log)+1` is concurrency-safe | **None.** Replaced by `max+1` plus an explicit single-writer constraint, and the document now states that atomic append and unique allocation are different problems |
| 4 | Any immutable record whose creation is also an event | **None.** No creation event exists; §G.0 lists the initial state of every entity as a function of its record |
| 5 | Any current SQLite projection count other than 22 | **None.** The two remaining "18" mentions are explicitly labelled as Revision 1 history |
| 6 | Any remaining `REGULATED_TIER_RELEASE` | **None** outside the historical note recording its removal |
| 7 | Any `GATE_DECISION_RECORDED` / `ASSET_REGISTERED` representing creation | **None** outside the removal table in §G.0 |

#### AJ.8.7 Remaining unresolved decisions

**None requiring user approval.** DATA_ADR-004 was approved and DATA_ADR-014 replaced in the previous pass; this pass introduced no new question for the user.

Five items remain open as **Phase 3+ engineering choices**, none of which changes a data contract:

1. Event log file format and layout (§AI.1) — Phase 2 constrains only atomicity and ordinal semantics.
2. **How single-writer-per-scope is enforced** — an advisory lock file, a process-level mutex, or simply the orchestrator being a single process. Phase 2 states the constraint; Phase 5 picks the mechanism.
3. Whether a second market on one product warrants splitting the Evidence Ledger (R7, DATA_ADR-003).
4. The concrete shape of `qualification_translations` (§AE Case G) — needed before Phase 6.
5. Whether the binding projection is cached with invalidation or always recomputed (R14).

#### AJ.8.8 Freeze readiness

**Phase 2 is ready to freeze.**

All twelve corrections across three audit passes are applied. The seven-point contradiction scan is clean. No decision is waiting on the user. The design carries two acknowledged caveats, both stated in the body rather than buried: the index builder's fold is load-bearing and is the most test-worthy code in the system (§AJ.7), and identifier allocation is correct only under the single-writer constraint that V1 explicitly adopts (§E.1.1, DATA_ADR-032). Neither is a defect; both are choices with the alternative recorded.

Two things worth carrying into Phase 3 as posture rather than as tasks. First, **two of this pass's three structural findings were introduced by the previous pass** — Correction 1 created the duplicated creation events, and Correction 10's predecessor was written in the same pass that introduced it. A correction pass is itself a change that can go wrong, and the useful response is to keep re-running the scan rather than to trust that a fix stayed fixed. Second, all three structural findings were of the same shape: **a statement that was true in the section that made it and false somewhere else in the document.** The mechanical checks that catch these — for every field, does it change over time; for every identifier, does its scope exist yet; for every fact, is it written in more than one place — are cheap, and they belong in Phase 3's review of whatever it builds.

---

## Compliance with Phase 2 constraints

| Constraint | Status |
|---|---|
| `docs/PHASE_1_SYSTEM_DESIGN.md` read completely before designing | ✅ 1,795 lines, full |
| `PRE_FLIGHT_AUDIT.md` unmodified | ✅ Not opened for writing |
| Phase 1 Revision 2 treated as frozen | ✅ Two conflicts surfaced (§A) and resolved in Phase 2's favour where Phase 1 was authoritative; no Phase 1 ADR reopened |
| All three correction passes modified only `docs/PHASE_2_DATA_ARCHITECTURE.md` | ✅ |
| Final freeze pass: seven-point contradiction scan run | ✅ Clean (§AJ.8.6) |
| No production code | ✅ |
| No Claude Skills created | ✅ |
| No orchestrator implemented | ✅ |
| No Higgsfield integration | ✅ Capability treated as config with `verification_status` |
| No Meta API calls | ✅ |
| No performance ingestion | ✅ Interface only (§AB) |
| No repository files moved | ✅ |
| No Phase 3 migration | ✅ Handoff requirements only (§AI) |
| No runtime dependencies installed | ✅ |
| No SQLite database built | ✅ Projection designed, no DDL, no file |
| No final repository structure created | ✅ Phase 3 owns layout |
| No Python models, no schema files in final locations | ✅ Contracts expressed as JSON/YAML shapes in this document |
| Source/knowledge files unmodified | ✅ |
| Only `docs/PHASE_2_DATA_ARCHITECTURE.md` created | ✅ |
| Phase 3 not begun | ✅ |

**Phase 2 ends here, ready to freeze. Phase 3 is not authorised and has not been started.**
