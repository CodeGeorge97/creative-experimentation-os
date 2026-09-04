# PHASE 1 — FINAL AUDIT + SYSTEM DESIGN
## Creative Experimentation OS — Chile

**Date:** 2026-09-04
**Revision:** 2 — external audit correction pass applied (see **§AA**). Seven corrections raised, seven accepted.
**Status:** Architecture proposal. No code, no schemas, no migrations, no file reorganisation performed.
**Predecessor:** `PRE_FLIGHT_AUDIT.md` (immutable historical snapshot; W1 resolved by subsequent verification).
**Authorisation:** Phase 1 only. Phases 2–10 not started.

**Language note:** this document is written in English because the Master Prompt and its required section headers are in English. The *system* it describes produces Spanish-language output for Chile. A Spanish edition of this document can be produced on request.

---

## 0. What was actually read before concluding

| Input | Read | Depth |
|---|---|---|
| `PRE_FLIGHT_AUDIT.md` | Yes | Full |
| `knowledge/copywriting/schwartz/schwartz_persuasion_framework.md` | Yes | Full (732 lines) |
| `knowledge/copywriting/schwartz/schwartz_language_engine.md` | Yes | Full (732 lines) |
| `knowledge/copywriting/schwartz/schwartz_integration_map.md` | Yes | Full (419 lines) |
| `knowledge/methodology/modulo-1..5*.md` | Yes | Full (5 files) |
| `knowledge/methodology/*.pdf` (3) | Yes | Text-extracted, full |
| `samples/**` media | No | Metadata only, per Master Prompt §31. No Style Profiles, no Voice Profiles generated. |
| Higgsfield capability | Verified externally | See §T and §0.2 |
| Claude API / Skills / MCP capability | Verified against current docs | See §0.2 |
| Local runtime | Probed | See §0.3 — **new blocker** |

### 0.1 Five findings from the corpus that change the architecture

These are not restatements of the pre-flight audit. They come from reading the content, which the pre-flight audit explicitly did not do.

**F1 — `knowledge/methodology/` is not methodology. It is a single-client case study whose derivation is conversational and unverifiable.**

*Epistemic note (external audit correction, §AA):* the original wording asserted as fact that this corpus was "derived from a prior LLM conversation." The repository contains no authorship metadata that establishes this. The evidence below supports a strong inference, not a fact, and the document that insists observations are not conclusions must hold itself to that rule. Classification is therefore **`PROBABLE_LLM_DERIVED` / `CONVERSATIONAL_DERIVED_UNVERIFIABLE`**. The operational consequence — quarantine — is unchanged, because it follows from *unverifiability*, which is established, not from *authorship*, which is not.

Evidence (consistent with conversational derivation; not proof of it):
- `modulo-1-estrategia-mercado.md:97` ends a section by asking the reader a question: *"¿Deseas que realicemos una búsqueda en internet en este momento…?"*
- `Escalamiento Creativo y Prueba Social en Meta Ads.pdf` ends with *"🎯 3. Siguiente Paso Sugerido: ¿Te gustaría que redacte una guía paso a paso…?"*
- Every module carries citation markers (`[45, 50, 56]`) into a numbered source corpus that is **not in the repository**.
- The named upstream sources are themselves marketing documents (`25. IMAGE ADS AI PROMPTE (2).docx`, `26. Ads draft --> to script…docx`), not primary research.

Consequence: `sources/methodology/` is empty (audit W3) **not because the files were misplaced, but because the primary sources are not present in this project and the cited corpus cannot be resolved.** W3's recommended resolution changes from "move files" to "record that this knowledge is unverifiable and quarantine it accordingly." This is registered below as **W8**.

Whether the derivation was a chat session, a dictated draft or an edited transcript does not change the architecture. What matters, and what *is* established, is that no cited source in this corpus can be resolved from within the repository.

**F2 — The corpus states pharmacological claims as settled fact.**

`modulo-4-ugc-vsl-strategy.md` §4.2C asserts, without literature citation, that Saw Palmetto blocks 5-alpha-reductase, that Berberine HCl is *"comparable in clinical studies to prescription treatments like metformin, but without its severe digestive side effects"*, that Myo/D-Chiro-Inositol at 40:1 produces *"a notable reduction of androgens in only 3 months"*, and that Zinc Bisglycinate raises hepatic SHBG production. These are health claims about a supplement, sourced from ad-copy drafts.

Consequence: if this file is placed in a flat retrieval bucket that the script engine reads, **the system will emit unsupported medical claims on its first run.** This is the single largest data-poisoning risk in the repository, and it is invisible to a file-level audit.

**F3 — The corpus actively recommends deceptive practices that the Schwartz layer explicitly forbids.**

- `modulo-2` §2.4: *"UGC Sintético"* — recreating Reddit threads, simulated screenshots and simulated messaging reviews, explicitly because *"the brain mislabels them as organic content before the prefrontal cortex detects commercial intent."*
- `modulo-3` §3.5: phone-screen mockups imitating iPhone Notes, a viral tweet, or a TikTok comment thread, *"because it imitates the organic content the user consumes from their friends."*
- `modulo-4` §4.4: *"Nativización Visual"* — embedding TikTok native UI (search bar, comment boxes) to *"camouflage optimally with organic non-advertising content."*

`schwartz_persuasion_framework.md` §15 anticipates exactly this and corrects it: *"Do not impersonate journalism, fabricate editorial endorsement, fake news reports, or falsely imply independent coverage."*

Consequence: the two knowledge layers **contradict each other on a compliance-critical point.** A flat "psychology knowledge" bucket would resolve the contradiction by coin-flip. The architecture must encode precedence explicitly and give the compliance layer a hard deny-list. This finding alone justifies the Knowledge Provenance layer (§I).

**F4 — A named technique in the corpus is factually wrong.**

`modulo-5` §5.2 and `Dominio del Post ID_.pdf` instruct the operator to extract a **competitor's** Post ID via browser devtools and then use it via *"Usar publicación existente."* Meta's *Use Existing Post* requires a post owned by a Page the advertiser administers; you cannot run ads on another advertiser's post. The technique is real and useful **for your own posts** (social-proof consolidation across ad sets), and the corpus describes that half correctly. The competitor half is not executable.

Consequence: `PERFORMANCE_HEURISTIC` content cannot be trusted into an executable playbook without a verification gate. Confirms Master Prompt §17.

**F5 — The corpus's own KPI thresholds contradict each other, and one formula is self-contradictory.**

| Metric | `modulo-4` §4.4 | `modulo-5` §5.4 |
|---|---|---|
| Hook Rate | > 30 %–40 % | > 35 % |
| Hold Rate | > 15 %–20 % | > 25 % |
| Outbound CTR | > 1.5 %–2.0 % | > 1.5 % |

Worse, `modulo-4:122` defines Hold Rate as *"15-second plays divided by total **Impressions** or 3-second views (15s Video Views / 3s Views)"* — two incompatible denominators in one sentence. `modulo-5:109` uses only `15s / 3s`.

Consequence: this is direct, in-repository proof for Master Prompt §59. **No KPI threshold from this corpus may be hardcoded.** Additionally, the claim that ads running 60–90 days are *"by definition profitable"* (stated three times: `modulo-5` §5.2, and both scaling PDFs) is survivorship inference, not evidence.

### 0.2 External capability verification

Verified against current sources on 2026-09-04.

**Claude platform — VERIFIED.**
- **Claude Agent SDK** (`claude-agent-sdk` / `@anthropic-ai/claude-agent-sdk`) is Claude Code packaged as a library: agent loop, context management, built-in file/bash/search tools, MCP client, subagents, hooks, permissions. It supplies a *harness only* — you host it.
- **Agent Skills** are a distinct mechanism from **Managed Agents**. Skills are loadable procedural know-how; Managed Agents (beta) is a hosted surface where Anthropic runs the loop and a per-session sandbox, with versioned agent configs, session budgets, scheduled deployments and multi-agent rosters.
- **Structured outputs** are GA: `output_config: {format: {...}}` on `messages.create()`, plus `strict: true` on tool definitions with `additionalProperties: false`. This is the mechanism that makes every schema in this design enforceable rather than aspirational.
- **Citations** are GA: `citations: {enabled: true}` on a document block returns `cited_text` plus `page_location` / `char_location`, giving source-anchored provenance without building it.
- **⚠ The two are mutually exclusive in one request.** Structured outputs are documented as *"Incompatible with: Citations (returns 400 error)"* (`claude-api/shared/tool-use-concepts.md:510`). The first edition of this document proposed both as if they composed. **They do not.** Evidence acquisition must therefore be two model calls, not one — see §N and ADR-005/006/031. *(External audit Correction 1; §AA.)*
- **Message Batches** run asynchronously at 50 % cost — directly applicable to the 20–30 hypothesis pool.
- **Prompt caching** is prefix-match; the Schwartz layer (~50 KB, stable) is an ideal cached prefix.
- Current models: `claude-opus-5` ($5/$25 per MTok), `claude-sonnet-5` ($2/$10), `claude-haiku-4-5` ($1/$5).

**Higgsfield — PARTIALLY VERIFIED. Treat the rest as unverified.**

| Fact | Status |
|---|---|
| Public async REST API at `api.higgsfield.ai`; auth → submit → poll or webhook; outputs retained ≥ 7 days; Python/TS/cURL clients | **VERIFIED** (`docs.higgsfield.ai/docs`) |
| Hosted MCP server at `https://mcp.higgsfield.ai/mcp`, OAuth flow, no API key, works with Claude Code | **VERIFIED** (`higgsfield.ai/mcp`) |
| 30+ models routed (Soul, Cinema Studio, Flux, Seedream, Kling, Minimax Hailuo, Veo); images to 4K; **video up to ~15 seconds**; Soul character training for consistency | **VENDOR-STATED**, not independently confirmed |
| Exact MCP tool names and signatures | **UNVERIFIED** — docs are JS-rendered; not machine-readable at fetch time |
| Lipsync / talking-avatar / speech synthesis | **UNVERIFIED** — no official documentation found either way. **Do not design as if it exists.** |
| Multi-speaker podcast workflow | **UNVERIFIED — no evidence found.** |
| Per-model duration limits, continuity controls, per-generation cost | **UNVERIFIED** |

**The ~15-second ceiling is the single most consequential external fact in this document.** It is discussed in §T.

**Meta policy — NOT VERIFIED IN THIS PHASE.** Deliberately deferred: policy text must be fetched at review time, not cached into a design document that will age. See ADR-018.

### 0.3 Implementation prerequisite the pre-flight audit did not detect

The pre-flight audit assessed *content*. It did not assess *executability*. Probing the machine:

| Runtime | Status |
|---|---|
| `python` / `python3` / `py` | **NOT INSTALLED** |
| `node` / `npm` | **NOT INSTALLED** |
| `sqlite3` | **NOT INSTALLED** |
| `ffmpeg` / `ffprobe` | **NOT INSTALLED** |
| `git` | 2.55.0 |
| `pdftotext` | 4.06 |

Nothing in the proposed V1 — no script layer, no SQLite store, no media analysis, no Anthropic SDK call — can execute on this machine today. This does not block Phase 1 (design), and it does not retroactively invalidate the pre-flight verdict, which was scoped to material availability.

**Classification: `IMPLEMENTATION_PREREQUISITE` (PRE-01).** *Revised by external audit (§AA).* The original text called this a blocker on "Phase 2 onward," which was wrong: Phase 2 is Data Architecture — entity design, relationships, constraints, identifier rules. None of that requires an interpreter. Design work proceeds; only **execution** is gated.

| Phase | Gated by PRE-01? |
|---|---|
| Phase 2 — Data Architecture (design) | **No** |
| Phase 3 — Repository & Migration *design* | No |
| Phase 3 — Migration *execution* (`git mv`, front-matter) | Partially — git suffices; tooling helps |
| Phase 4 — Skills design | No |
| Phase 5 — Orchestrator **implementation** | **Yes** — Python |
| Phase 6 — Creative Engine | **Yes** — Python + SDK |
| Phase 7 — V1-Production | **Yes** — Python + ffmpeg |
| Phases 8–10 | **Yes** |

Required before the first phase that executes code: **Python 3.12+** (supplies `sqlite3` via stdlib) and **ffmpeg/ffprobe** (media analysis and assembly). Still the cheapest item on the critical path; simply not a reason to stop designing.

### 0.4 Warnings carried forward

| # | Status after Phase 1 |
|---|---|
| W1 | **RESOLVED** (verified independently). Treated as resolved throughout. |
| W2 | Open → addressed structurally in §K (`derived_from` lineage, not a written note). |
| W3 | Open → **reframed by F1**. The sources do not exist; migration alone cannot fix it. §I. |
| W4 | Open → generalised: *Brilliance* is one of **two** unverifiable-source knowledge bodies. §I. |
| W5 | Open → **escalated to HIGH risk** in §X. TikTok-sourced voices are a cloning-consent exposure, not a filing gap. |
| W6 | Open → moot for V1: no voice in this corpus is production-eligible. §K. |
| W7 | Open → deferred to Phase 3; naming is a migration concern, not an architecture concern. |
| **W8** | **NEW.** `knowledge/methodology/` is derived, unverifiable, single-niche, contains unsupported medical claims (F2), recommends non-compliant tactics (F3), contains at least one inexecutable procedure (F4) and self-contradictory benchmarks (F5). |

---

## A. Executive Architectural Verdict

### Is the overall system concept viable?

**Yes — the concept is sound and unusually well-specified. The V1-Core *scope* is not viable as written.** It is roughly two to three times larger than a first implementable increment, and one part of V1-Production rests on an unverified vendor capability.

The distinction matters: nothing here needs to be *rethought*. Several things need to be *sequenced*.

### What is strongest

1. **The epistemic spine.** `SOURCE → OBSERVATION → INSIGHT → HYPOTHESIS → CONCEPT → EXPERIMENT → CREATIVE → PERFORMANCE → LEARNING`, with the instruction never to collapse levels, is the most valuable idea in the entire specification. It is what separates this from an ad generator. It is also the part most likely to be abandoned under delivery pressure, so it must be enforced by schema and gate, not by discipline.
2. **The refusal to let frameworks outrank evidence.** The precedence chain (Product Truth → Evidence → Research → Customer Language → Experiments → Brand → Platform → Copywriting → Ideation) is correct, and — critically — the Schwartz documents *already agree with it internally* (`schwartz_persuasion_framework.md` §1, `schwartz_integration_map.md` §4). Two independent sources converging on the same precedence rule is a strong signal.
3. **The Model / Skill / Tool / Orchestrator / DB / FS / Script separation (§6) and the explicit rejection of "Master Skill calls sub-Skills" (§7).** This is the correct mental model and it is uncommon. Most systems of this shape fail precisely here.
4. **Product Image + Brand cold start as the *minimum*, not the aspiration.** Designing the degraded path first is the right order, and it forces the OBSERVED/VERIFIED/INFERRED/UNKNOWN discipline to be real rather than decorative.
5. **Separating Concept / Creative / Meta Ad, and Hook Strategy / Copy / Visual / Audio.** Without these, controlled hook testing is impossible and every performance learning is confounded from birth.

### What is weakest

1. **The knowledge corpus is contaminated, and the architecture as specified would ingest it uncritically.** F2, F3, F4 and F5 are all live. `knowledge/methodology/` cannot be a peer of the Schwartz layer in a retrieval index. This is the highest-priority correction in this document.
2. **V1-Core's output surface is over-specified.** §88 lists 26 artefacts. Most are not artefacts — they are *fields* of three or four objects. Format Assignments, Narrative Assignments, Style Assignments, Voice Assignments, Hooks, Chile Localization and Creative DNA are all properties of the Creative object. Producing them as separate documents creates seven opportunities for them to disagree with each other. See §Y.
3. **V1-Production's premise collides with the verified generation ceiling.** A ~15-second clip limit means "10 final videos" is a **segmentation-and-assembly** problem, not a generation problem. The corpus's own case study describes 30–45-second bodies and 2–3-minute VSLs — three to twelve clips each, with character, wardrobe, lighting and voice continuity across every cut. Podcast (two speakers, turn-taking, reaction shots, lipsync) is the hardest of the three formats and its enabling capability is **unverified**.
4. **Numeric confidence theatre.** The specification and the Schwartz documents together propose `0-1` confidences and `0-10` scores across roughly sixty fields (`awareness_confidence`, `stereotype_risk: 0-1`, a twelve-dimension `language_quality` vector, `contradiction_risk`, and so on). A language model will emit these fluently and they will mean nothing. Master Prompt §26 already warns against "a fake mathematical formula simply for sophistication"; the same warning applies to the framework documents' own schemas. See §Y.
5. **No runtime exists (§0.3),** and the automated runtime's API access and cost model are unprovisioned (§D.1). Cheap to fix, but absolute once execution starts.

### What must change

| # | Change | Rationale |
|---|---|---|
| C1 | Quarantine `knowledge/methodology/`; never retrieve it directly into script generation | F2, F3, F4, F5 |
| C2 | Encode precedence as an executable rule with a compliance deny-list, not as prose | F3 — two sources actively disagree |
| C3 | Collapse 26 batch artefacts to 8 artefact types | §Y |
| C4 | Split the 30-stage script pipeline into ~12 stages; mark each deterministic or generative | §G |
| C5 | 9 candidate Skills → 5 Skills + 4 non-Skill components | §E |
| C6 | Replace scalar confidences with enumerated states + a coverage vector | §M, §Y |
| C7 | Treat V1-Production as segmentation + assembly; stage the three formats by risk | §T |
| C8 | Git-tracked JSON as system of record; SQLite as a *derived* index | §V |
| C9 | 4 human gates → 3 | §R |
| C10 | Install a runtime before the first *executing* phase (Phase 5) | PRE-01 |

---

## B. Final Scope

### V1-Core — Creative Intelligence

**Input:** Product Image + Brand (Level 1) through Level 4.
**Output:** 10 approved Production Packages containing complete word-for-word scripts, storyboards, shot lists, Creative DNA and compliance reviews.

**IN SCOPE**

- Product Truth + Evidence Ledger, with OBSERVED / VERIFIED / INFERRED / UNKNOWN on every field
- Brand Snapshot
- Market + customer-language research for Chile, with source provenance and source-quality classification
- Audience Model and persuasion context (Schwartz strategy pass)
- Hypothesis Pool (20–30, heuristic target)
- Angle evaluation and concept selection (10)
- Diversity constraint satisfaction + audit
- Experiment Plan with declared variable and locked variables
- Format / narrative-pattern / style assignment
- Hook strategy, copy, visual, audio — separated
- **Complete word-for-word scripts.** Non-negotiable, retained in full.
- Brilliance language pass; Chile localisation with claim-invariance enforcement
- **Storyboards and shot lists.** Retained. Depth calibrated to what a short-clip generator can consume — see §S.
- Creative QA (generator ≠ judge)
- Compliance review, twice: a cheap pre-screen at concept stage and a full review at script stage
- Creative DNA records
- 10 Production Packages
- Meta Test Plan
- Run manifests (observability + reproducibility)

**OUT OF SCOPE for V1-Core**

- Any video generation
- Meta performance ingestion or analysis
- Context / news / macro intelligence
- Automated Style Profile extraction from video (see §L — three hand-authored profiles instead)
- Voice Profiles as production assets (see §K — none of the six samples is eligible)
- The Golden Test Set (§85)
- Static image ads (`modulo-3`'s subject; not in the §4 product vision)

**DEFERRED (interfaces preserved, implementations not built)**

- Performance layer; learning objects and freshness; exploration/validation/scaling modes; ad multiplication; diagnosis engine; context intelligence and its brand-safety classifier; multi-market beyond Chile; formats beyond UGC / Podcast / Animation

### V1-Production — Video Generation

**Input:** approved Production Packages. **Output:** final videos.

**IN SCOPE:** production router; format-specific routing; segmentation into ≤ generation-limit units; continuity data; generation via verified tool capability; Video QA against the Production Package; bounded retries with cost ceilings; assembly; naming.

**OUT OF SCOPE:** any re-invention of angle, concept, message, hook, script, narrative or awareness strategy. V1-Production executes; it does not decide. The only path back is a QA-triggered revision request into V1-Core.

**Staged by verified risk** — see §T. This is a sequencing recommendation, not a scope reduction; the target remains 10 videos.

### Future Performance Layer

Meta ingestion; Creative DNA ⋈ performance joins; experiment analysis; evidence levels; probable-diagnosis engine; learning store with scope and freshness. **V1's only obligation:** preserve the join keys and the experimental context (§U).

### Future Context Layer

Macro / search / social / news signals through `SIGNAL → EVIDENCE → CONSUMER IMPLICATION → PRODUCT RELEVANCE → CREATIVE HYPOTHESIS`, with a brand-safety classifier. **No V1 obligation beyond not making it impossible.** Phase 1 finds no compelling reason to accelerate it.

---

## C. Architecture Principles

1. **Provenance is not optional.** Every claim resolves to a source, or it is not a claim. Unresolvable → `UNKNOWN`, never a silent inference.
2. **Epistemic level is a field, not a tone.** Observation, insight, hypothesis and learning are different record types with different rules. Nothing is promoted between them implicitly.
3. **Deterministic where determinism is possible.** Diversity constraints, claim→evidence linking, experiment-variable isolation, ID generation, continuity propagation and schema validation are code. Reserve model reasoning for genuine judgement.
4. **The generator never grades itself.** Every generative stage that produces a durable artefact has a separate critic with a different prompt and a different context.
5. **Schemas are enforced, not requested.** Every structured artefact is produced under `output_config.format` or a `strict: true` tool. A model asked politely for JSON will eventually invent a field.
6. **Knowledge is tiered by verifiability, and the tier travels with the content.** A retrieval hit carries its provenance class into the prompt. See §I.
7. **Precedence is executable.** When two knowledge sources conflict, a rule decides — not the sampler.
8. **Prefer enumerations to scalars.** `evidence_strength: {DIRECT, INDIRECT, ABSENT}` beats `0.73`. Introduce a number only where something is genuinely counted.
9. **Assets carry rights state; possession proves nothing.** REFERENCE / AUTHORIZED / PRODUCTION, defaulting to REFERENCE, never inferred.
10. **Lineage prevents circular evidence.** Derived assets record their root. Two profiles sharing a root cannot be used as independent evidence about each other.
11. **Reproducibility means re-derivable, not re-runnable.** Every output records the versions of every input. Git provides this; do not rebuild it.
12. **Cost and retries are bounded at design time.** Every generative loop has a ceiling and an escalation path.
13. **Degrade explicitly.** Missing input narrows claim freedom and is reported; it never silently lowers quality.
14. **Human gates sit where information is cheapest to correct**, not where the work feels finished.
15. **Build the smallest thing that can learn.** A system that ships and records one clean experiment beats a complete architecture that never runs.
16. **Only deterministic checks may be irreversible.** A model may recommend, escalate or refuse to proceed; it may never raise a stop that a human cannot resolve. Conversely, a mechanical fact is not a matter for approval — it is resolved by changing the fact. *(Added — external audit Correction 5.)*
17. **Quality objectives never override evidence constraints.** Diversity, coverage and completeness are things to *optimise*, not conditions to *satisfy*. Any mechanism that can be satisfied by invention has been specified wrongly. *(Added — external audit Correction 4.)*

---

## D. Component Architecture

Classification per Master Prompt §6. "Primary type" is what the component *is*; the reason states why it is not the alternative.

### Knowledge resources (Filesystem — not Skills)

| Component | Type | Why |
|---|---|---|
| Schwartz Persuasion Framework | Filesystem resource (cached prompt prefix) | Reference material consumed by several Skills. `schwartz_integration_map.md` §1 and `schwartz_persuasion_framework.md` §25 both say explicitly: do not build a monolithic Schwartz Skill. Agreed. |
| Schwartz Language Engine | Filesystem resource | Same. Consumed by one pass, not a procedure of its own. |
| Schwartz Integration Map | Design input, **not runtime** | It is an architecture document about the other two. It informs this design; it should not be retrieved at generation time. |
| Narrative Pattern Library | Filesystem resource (structured) | A closed enumeration with metadata. Data, not know-how. |
| Chile Customer Language Corpus | FS resource + DB index | Written by research, read by localisation. Grows; must be queryable and segmented. |
| Methodology corpus (quarantined) | FS resource, **restricted tier** | See §I. Never in the script-generation retrieval path. |

### V1-Core pipeline

| Component | Primary type | Why not otherwise |
|---|---|---|
| **Campaign Intake** | Orchestrator step + Script | Fixed input validation. No reasoning. |
| **Product Intelligence** (incl. Brand Snapshot) | **Skill** | Genuine transferable procedure: extract structured truth from sparse/visual input without hallucinating, classify every field, know when to say UNKNOWN. |
| Product image analysis | Tool (vision call) | A capability invocation, not know-how. |
| Brand/product web research | Tool (`web_search` with domain controls) | External capability. |
| **Evidence Extraction (E1)** | Orchestrator step (model call, citations ON, no schema) | Source-grounded reading. Returns prose + citation blocks carrying `cited_text` and `page_location` / `char_location`. **Cannot** also emit strict JSON — see §N. |
| **Evidence Normalisation (E2)** | Orchestrator step (model call, schema ON, citations OFF) | Converts E1's citation-carrying output into strict ledger records. Input is E1's own output, not the source — so it cannot invent a locator that E1 did not produce. |
| **Evidence Ledger writer** | Script/Service | Append-only ledger with integrity rules. Deterministic. Rejects any record whose `locator` is absent from E1's citation set. |
| **Product Truth Completeness** | Script/Service | A coverage computation over a required-field set. Pure function. §M. |
| **Claim Freedom resolver** | Script/Service | Deterministic mapping from evidence state → permitted territory. Must be inspectable and identical every run. §M. |
| **Market Intelligence CL** | **Skill** | Domain know-how: where Chilean customer language actually lives, how to weight sources, how to avoid inventing a Chilean stereotype. |
| Source quality classifier | Script/Service (enum) | A lookup, not a judgement. |
| **Audience Model + Persuasion Context** | Orchestrator step inside Creative Strategist | Not a separate Skill: it is one structured reasoning pass over research output. The six "stages" in §40 are fields of one object. §G. |
| **Creative Strategist** | **Skill** | The core reasoning skill: hypotheses, angles, belief bridges, concepts, format/narrative fit. |
| Hypothesis Pool generation | Orchestrator step (Batch API) | 20–30 independent generations; non-latency-sensitive; 50 % cost via Batches. |
| Angle evaluation | Skill reasoning + Script constraints | Qualitative ranking by the Skill; hard constraints enforced by code. §Q. |
| **Diversity constraint solver** | **Script/Service** | Pairwise dimension overlap + minimum-spread constraints. Deterministic and explainable. Not a model's opinion. §Q. |
| **Experiment Designer** | **Orchestrator step + Validation Gate** | **Not a Skill.** Experiment integrity is constraint satisfaction. A model asked to design an experiment will produce a confounded one and describe it confidently. §E, §P. |
| **Compliance pre-screen** | Validation Gate | Cheap concept-level filter so you don't write ten scripts and block four. |
| **Script Engine** | **Skill** | Full scripts, persuasion beats, Brilliance pass, Chile localisation, format-specific dialogue, storyboard, shot list. |
| Claim→evidence linker | **Script/Service** | Every hard claim must resolve to a `claim_id` with status VERIFIED. Unresolved ⇒ BLOCK. Mechanical, and the most important safety check in the system. |
| Localisation invariance check | Script/Service | Diff claims pre/post localisation; any change ⇒ reject. Deterministic. |
| **Creative Critic** | **Orchestrator step** (separate model call) | Not a Skill — it is a role with a different context, using the same domain knowledge. |
| **Compliance Reviewer** | **Skill** (narrowed) + Validation Gate | Mechanical half is a gate; the residue (ambiguity, implication-as-hidden-claim, native-format impersonation) is genuine policy judgement. |
| **Production feasibility scorer** | Script/Service | Countable: scenes, speakers, lipsync need, hands, product interaction, continuity spans, clip count. §50. |
| **Production Package assembler** | Script/Service | Deterministic render of validated objects. |
| **Human Gates 1–3** | **Human Gate** | §R. |
| **Run manifest writer** | Script/Service | §W. |

### Storage

| Component | Type |
|---|---|
| Artefact store (Product Truth, Evidence, Concepts, Scripts, Packages, Run manifests) | **Filesystem, git-tracked JSON/YAML — system of record** |
| Media (images, video, audio, PDFs, generated output) | Filesystem (git-ignored, hashed, registry-tracked) |
| Query index (products, claims, concepts, creatives, experiments, assets, learnings) | **SQLite — derived, rebuildable** |
| Asset Registry | DB entity + FS payload |

### V1-Production (conceptual only)

| Component | Type |
|---|---|
| Production Router | Orchestrator step + Script |
| Scene segmenter (≤ generation limit) | Script/Service |
| Continuity manifest | Script/Service |
| Generation | **Tool / MCP** (Higgsfield MCP or REST) |
| Video QA | Orchestrator step (vision) + Script checks |
| Retry controller / cost governor | Script/Service |
| Assembly | Tool (ffmpeg) + Script |

### D.1 Development environment vs automated runtime *(added — external audit Correction 7)*

These are two different systems with two different access models, and the first edition did not separate them. Conflating them is a common and expensive mistake: it is easy to prototype an entire pipeline inside an interactive assistant session and only discover at deployment that the automated system has no credentials, no cost model and no way to run unattended.

| | **Development environment** | **Automated runtime** |
|---|---|---|
| **What** | Claude Code — this session | Claude Agent SDK (Python), self-hosted |
| **Used for** | Designing, writing and reviewing the system; authoring Skills; running migrations; debugging | Executing campaign runs unattended |
| **Who invokes** | A human, interactively | The orchestrator, programmatically |
| **Access model** | Interactive Claude subscription / session auth | **Requires its own programmatic API access** |
| **Cost model** | Covered by the interactive plan | **Per-token API billing against an organisation account** |
| **Availability** | Only while a human is at the terminal | Must run headless, including at Gate waits |

> **An interactive Claude Code subscription does not supply the programmatic API runtime for the deployed system.** They are separate entitlements. The automated runtime needs its own credential — an API key or an OAuth/service-account profile resolved by the SDK's credential chain — provisioned against an organisation with API access and a billing relationship.

**Consequences that must be planned before Phase 5 (Orchestrator):**

1. **Authentication** — the runtime needs a non-interactive credential and a place to keep it. Not the operator's personal session, and not committed to the repository. The credential's identity is also what the run manifest should record as the actor.
2. **Cost model** — every campaign run is metered API usage, distinct from anything the development environment consumes. §Y's cost levers (Batch API at 50 %, prompt-caching the ~50 KB Schwartz prefix, effort tuning per stage) apply to the *runtime*, not to development. A per-campaign cost ceiling and a per-batch budget belong in the orchestrator from the first version, not retrofitted (§66).
3. **Rate limits and failure modes** — an unattended 10-creative batch will encounter 429s and transient 5xx. Retry, backoff and resumability are runtime concerns the development environment never surfaces.
4. **Model pinning** — the runtime pins exact model IDs (`claude-opus-5`, etc.) into the run manifest (§W). The development environment's model is irrelevant to reproducibility; the runtime's is the whole point.
5. **Deployment target** — for V1, the operator's own machine is sufficient. This is a real decision with real consequences (the machine must be awake for a run to proceed), and it should be made deliberately rather than by default.

**Orchestrator host recommendation (unchanged):** the **Claude Agent SDK (Python)**, self-hosted. Rationale: the asset store is local (~137 MB of media), human gates are interactive, the filesystem *is* part of the architecture, and cost control is direct. Managed Agents is the natural migration target if and when this becomes a hosted multi-user service — it supplies versioned agent configs, session budgets, scheduled deployments and multi-agent rosters, all of which map cleanly onto later phases, and it moves the credential and deployment concerns above onto Anthropic's infrastructure. Not needed for V1. (ADR-002, ADR-003, ADR-033.)

---

## E. Skills Audit

A Skill is reusable procedural know-how loaded into a model's context. It is not a callable function, it cannot guarantee execution, and it cannot enforce a constraint. Anything that must *always* happen, or must be *verifiably* correct, is not a Skill. That single test drives most verdicts below.

| # | Candidate | Verdict | Reasoning |
|---|---|---|---|
| 1 | `product-intelligence` | **KEEP + MERGE** (absorbs Brand Intelligence) → `product-intelligence` | Product Truth and Brand Snapshot are the same procedure applied to two subjects: extract structured facts from sparse and partly visual input, classify every field by evidence state, refuse to infer. Same failure mode (confident hallucination), same guardrails, same output discipline. Two Skills would duplicate the guardrails and let them drift. |
| 2 | `market-intelligence-cl` | **KEEP** | Real, non-obvious, transferable domain know-how: where Chilean customer language actually lives, how to weight a marketplace review against a Reddit thread, how to avoid substituting stereotype for evidence. Per `schwartz_persuasion_framework.md` §26 it also owns mass-desire, awareness and sophistication *evidence* — correctly, because those must be observed, not assumed (`schwartz_persuasion_framework.md` §5: "Do not infer sophistication merely from category age"). |
| 3 | `creative-strategist` | **KEEP** — the system's core Skill | Owns hypothesis generation, persuasion context, belief bridge, angle reasoning, concept definition, format/narrative fit. This is where judgement genuinely lives. |
| 4 | `experiment-designer` | **NOT_A_SKILL** → Orchestrator step + deterministic Validation Gate | Experiment integrity is constraint satisfaction: given N creatives and one declared variable, verify every other declared dimension is identical. That is a comparison, and it must be *guaranteed*. A model will produce a confounded design and narrate it convincingly — the exact failure the system exists to prevent. The judgement half — *which* hypothesis deserves a test — is real and belongs to `creative-strategist`. |
| 5 | `style-intelligence` | **SPLIT** → (a) Style Analysis = Tool + Script; (b) Style Selection = reasoning inside `creative-strategist` / `script-engine` | Video → structured profile needs `ffprobe`, frame sampling and vision calls: capability, not know-how. Angle × Style fit is a paragraph of reasoning, not a Skill. Neither half justifies a standalone Skill. |
| 6 | `video-director` | **SPLIT + RENAME** → `script-engine` (V1-Core) and Production Router (V1-Production, non-Skill) | The name misleads: in V1-Core nothing is directed, it is *written*. The V1-Core deliverable — full scripts, persuasion beats, storyboards, shot lists, script-to-visual translation — is a writing Skill. The routing/generation half belongs to V1-Production and is orchestration, not know-how. |
| 7 | `chile-localizer` | **MERGE** into `script-engine` as a mandatory, distinct pass | The *pass* must stay separate — `schwartz_language_engine.md` §28 is right that neutral strategic Spanish should precede localisation. But a separate *Skill* means a separate call that can drift from the approved claims. Keeping it inside `script-engine` puts localisation next to the claim set it must not alter, and the invariance check is deterministic anyway. The Chilean language *corpus* remains a first-class knowledge resource. |
| 8 | `compliance-reviewer` | **KEEP (narrowed) + SPLIT** | Strip the mechanical half into a gate: every hard claim resolves to a VERIFIED `claim_id`, or BLOCK. What remains is genuine judgement — ambiguity as hidden claim, implication smuggling an unsupported promise (`schwartz_language_engine.md` §15), native-format impersonation (F3), category-sensitive claims. That residue is a Skill. |
| 9 | `performance-analyst` | **REMOVE from V1** (defer; preserve interface) | There is no performance data. Building it now means building against imagined data. Its only V1 obligation is that Creative DNA carries the join keys — which §U specifies. |

**Result: 9 candidates → 5 Skills.**

`product-intelligence` · `market-intelligence-cl` · `creative-strategist` · `script-engine` · `compliance-reviewer`

Plus 4 knowledge resources (Schwartz ×2, Narrative Pattern Library, Chile Language Corpus), and the deterministic services listed in §D. This satisfies §91.11 (avoid Skill proliferation) without pushing judgement into code.

---

## F. End-to-End V1-Core Flow

```
                    PRODUCT IMAGE + BRAND  (Level 1 … Level 4)
                                  │
                    ┌─────────────▼─────────────┐
                    │  0. CAMPAIGN INTAKE       │  script · validate · RUN_ID · onboarding level
                    └─────────────┬─────────────┘
                                  │
      ╔═══════════════════════════▼═══════════════════════════╗
      ║  PHASE I — TRUTH                                      ║
      ╠═══════════════════════════════════════════════════════╣
      ║  1. Product image analysis        tool (vision)       ║
      ║  2. Brand + product research      tool (web_search)   ║
      ║  3. Product Truth + Brand Snapshot  SKILL             ║
      ║  4. Evidence acquisition — THREE steps (§N.1)         ║
      ║     E1 extract   model · citations ON · no schema     ║
      ║     E2 normalise model · schema ON · citations OFF    ║
      ║     E3 write     service · locator reconciliation     ║
      ║  5. Completeness coverage vector  service             ║
      ║  6. CLAIM FREEDOM TIER  T0│T1│T2│T3   service         ║
      ╚═══════════════════════════╤═══════════════════════════╝
                                  │
                    ┌─────────────▼─────────────┐
                    │ ▲ HUMAN GATE 1 — TRUTH    │  blocking
                    │   correct / confirm UNKNOWN│
                    └─────────────┬─────────────┘
                                  │
      ╔═══════════════════════════▼═══════════════════════════╗
      ║  PHASE II — MARKET                                    ║
      ╠═══════════════════════════════════════════════════════╣
      ║  7. Chile market + competitor research   SKILL        ║
      ║  8. Customer Language Corpus (verbatim)  SKILL        ║
      ║  9. Audience Model + Persuasion Context  SKILL        ║
      ║     └ mass desire · awareness · sophistication ·      ║
      ║       current/desired belief · identification —       ║
      ║       ONE object, ONE pass, each field evidence-linked║
      ╚═══════════════════════════╤═══════════════════════════╝
                                  │
      ╔═══════════════════════════▼═══════════════════════════╗
      ║  PHASE III — HYPOTHESIS                               ║
      ╠═══════════════════════════════════════════════════════╣
      ║ 10. Hypothesis Pool 20–30    SKILL · Batch API (−50%) ║
      ║ 11. Compliance PRE-SCREEN    gate  ◄ cheap kill       ║
      ║ 12. Angle evaluation         SKILL (qualitative rank) ║
      ║ 13. DIVERSITY SOLVER → 10    service                  ║
      ║     hard constraints enforced · targets optimised     ║
      ║     └► INSUFFICIENT_EVIDENCE_FOR_DIVERSITY_TARGET     ║
      ║        surfaces at Gate 2 — never fabricates (§Q)     ║
      ║ 14. Experiment Plan          orchestrator + validator ║
      ║     └ declared variable · locked variables            ║
      ╚═══════════════════════════╤═══════════════════════════╝
                                  │
                    ┌─────────────▼─────────────┐
                    │ ▲ HUMAN GATE 2            │  blocking
                    │   CONCEPTS + EXPERIMENT   │  highest-leverage decision
                    └─────────────┬─────────────┘
                                  │
      ╔═══════════════════════════▼═══════════════════════════╗
      ║  PHASE IV — CREATIVE  (per concept ×10)               ║
      ╠═══════════════════════════════════════════════════════╣
      ║ 15. Format + Narrative Pattern + Style    SKILL       ║
      ║ 16. Hook STRATEGY (awareness-driven)      SKILL       ║
      ║ 17. Persuasion beat plan                  SKILL       ║
      ║ 18. FULL SCRIPT DRAFT (word-for-word)     SKILL       ║
      ║ 19. Brilliance language pass              SKILL       ║
      ║ 20. Chile localisation + spoken pass      SKILL       ║
      ║ 21. Hook EXECUTION copy/visual/audio      SKILL       ║
      ║ 22. CLAIM → EVIDENCE + CLASS  service ◄ HARD_BLOCK    ║
      ║ 23. Localisation invariance   service ◄ HARD_BLOCK    ║
      ║ 24. Deny-list match           service ◄ HARD_BLOCK    ║
      ║ 25. Creative Critic              separate call        ║
      ║        └─ REVISE ──► back to 18 (bounded, max 2)      ║
      ║ 26. Compliance review    SKILL ► LOW|MED|HIGH_RISK|   ║
      ║                                  POLICY_REVIEW_REQ'D  ║
      ║        (judgement only — cannot raise HARD_BLOCK)     ║
      ║ 27. Production feasibility       service              ║
      ║ 28. Storyboard + Shot List       SKILL                ║
      ║ 29. Creative DNA record          service              ║
      ╚═══════════════════════════╤═══════════════════════════╝
                                  │
      ╔═══════════════════════════▼═══════════════════════════╗
      ║ 30. Batch diversity audit (post-hoc)     service      ║
      ║ 31. Production Package assembly ×10      service      ║
      ║ 32. Meta Test Plan                       service      ║
      ║ 33. Run manifest                         service      ║
      ╚═══════════════════════════╤═══════════════════════════╝
                                  │
                    ┌─────────────▼─────────────┐
                    │ ▲ HUMAN GATE 3            │  blocking
                    │   PRODUCTION RELEASE      │  last stop before spend
                    └─────────────┬─────────────┘
                                  ▼
                    10 APPROVED PRODUCTION PACKAGES
                            → V1-PRODUCTION
```

Three structural points. **The deterministic checks (22–24) sit before the critic, not after** — there is no value in critiquing the craft of a script that is about to be hard-blocked for an unsupported claim. **Compliance runs twice** (11, 26): the pre-screen kills non-compliant *territories* at roughly 1/50th the cost of killing non-compliant *scripts*. **Every `HARD_BLOCK` in the flow is raised by a service, never by a Skill** (§R) — steps 22, 23 and 24 are code; steps 25 and 26 are judgement and can only escalate.

---

## G. Script Generation Architecture

### Audit of the proposed pipeline (§40)

The proposed 30-stage sequence is directionally right and structurally wrong in six specific ways.

**(1) Six stages that are one object.** `MASS DESIRE → AWARENESS → SOPHISTICATION → CURRENT BELIEF → DESIRED BELIEF → IDENTIFICATION` are listed as sequential stages. They are fields of a single frame — `schwartz_integration_map.md` §5A already models them as one `persuasion_context` object. Six sequential model calls to populate six fields of one object costs six times as much and invites the later fields to drift from the earlier ones. **Merge into one pass.**

**(2) `AUDIENCE PSYCHOLOGY` overlaps `MASS DESIRE`/`BELIEF` by roughly 70 %.** Master Prompt §20's Audience Model and §22's Schwartz context share desire, belief, objection and awareness. **Merge into the same pass**, with the Audience Model as the container and the persuasion context as its strategic projection.

**(3) `STYLE MATCH` is placed before `HOOK STRATEGY`.** This lets execution constrain strategy. `schwartz_persuasion_framework.md` §4 is explicit that the hook must be evaluated for *awareness fit*. **Reorder**, and split hook per §48: **Hook Strategy** (strategic, awareness-driven, before format) → format/narrative/style → **Hook Execution** (copy/visual/audio, after style). Master Prompt §48 already requires the separation; the pipeline did not reflect it.

**(4) `CHILE LOCALIZATION` then `SPOKEN NATURALNESS PASS` is duplicated reasoning.** Localising into Chilean conversational Spanish *is* the naturalness work; a second generative pass invites the model to re-touch the copy and drift. **Merge into one pass with two explicit checks** (register fit, then speakability), plus the deterministic claim-invariance diff.

**(5) `COMPLIANCE REVIEW` appears only once, at the end.** With ten full scripts already written, a block is maximally expensive. **Add a concept-level pre-screen.**

**(6) Four stages are missing entirely:**
- **Claim → Evidence binding** (deterministic; the system's core safety property)
- **Localisation invariance check** (deterministic)
- **Production feasibility** *before* storyboarding — otherwise you storyboard the impossible
- **SCRIPT LOCK** — an explicit, versioned, immutable transition after which V1-Production may not reinterpret anything

### Redesigned pipeline

| # | Stage | Mode | Notes |
|---|---|---|---|
| 1 | Strategic frame — Audience Model + Persuasion Context | Generative, 1 pass | Merges §40 stages 3–9. Every field evidence-linked or `UNKNOWN`. |
| 2 | Angle + hypothesis binding | Generative | Inherited from Gate 2; not re-decided. |
| 3 | **Hook Strategy** | Generative | Awareness- and belief-driven. Strategy only — no copy yet. |
| 4 | Format + Narrative Pattern + Style | Generative + constrained | Format may be user-fixed (5/2/3) or auto. Narrative chosen independently of format (§30). |
| 5 | Persuasion beat plan | Generative | `persuasion_beats[]` per `schwartz_persuasion_framework.md` §19 — the audit trail that later lets retention drops be mapped to message beats. |
| 6 | **Full script draft** | Generative | Word-for-word. Neutral strategic Spanish. No placeholders — ever. |
| 7 | **Brilliance language pass** | Generative | `schwartz_language_engine.md` §25. Scored **in the delivery language**, not on a translation. |
| 8 | **Chile localisation + spoken naturalness** | Generative, 1 pass | Register, rhythm, speakability. Naturalness > slang. |
| 9 | **Hook Execution** — copy / visual / audio | Generative | Separated for controlled hook testing (§48). |
| 10 | **Claim → Evidence link** | **Deterministic** | Every hard claim → VERIFIED `claim_id`, **and** its evidence class ≥ the §N minimum for that claim type (health/efficacy/comparative ⇒ A1; A2 alone is insufficient). Unresolved or under-classed ⇒ **`HARD_BLOCK`**. |
| 11 | **Localisation invariance** | **Deterministic** | Claim-set diff pre/post stages 7–8. Any claim added, strengthened or qualification dropped ⇒ **`HARD_BLOCK`**. |
| 12 | **Creative Critic** | Generative, separate context | `PASS | REVISE | REJECT_TO_HUMAN`. **Cannot emit `HARD_BLOCK`** (§R). REVISE loops to 6, **max 2 iterations**, then escalates. |
| 13 | **Compliance review** | Generative + gate | `LOW | MEDIUM | HIGH_RISK | POLICY_REVIEW_REQUIRED`. **Cannot emit `HARD_BLOCK`** — deny-list matching is a separate deterministic check. Never "META APPROVED". |
| 14 | **Production feasibility** | **Deterministic** | Clip count, speakers, lipsync need, continuity spans, hands/product interaction. |
| 15 | Storyboard + Shot List | Generative | Fields calibrated to a short-clip generator (§S), not to film production. |
| 16 | **SCRIPT LOCK** | **Deterministic** | Version stamped, hashed, immutable. Downstream reads only. |

### Explicit answers to the §G questions

- **When does persuasion architecture happen?** Stages 1–5, all *before* the first word of dialogue. `schwartz_persuasion_framework.md` §17 calls this the Schwartz Strategy Pass and places it before the first draft. Confirmed.
- **When is Schwartz consulted?** *Breakthrough* at stages 1–5 and again as a QA lens at 12. *Brilliance* only at stage 7, and as an ambiguity input to 13. Never as a source of claims.
- **When does Brilliance language engineering happen?** Stage 7 — after strategic meaning is stable and before localisation, exactly as `schwartz_language_engine.md` §18 and §28 prescribe.
- **When does Chile localisation happen?** Stage 8, after the argument is fixed. It may change lexis, syntax, register and rhythm. It may not change a claim, strengthen a promise, alter awareness strategy or drop a qualification — enforced deterministically at 11.
- **When does the Creative Critic run?** Stage 12, after the deterministic blocks. Different context, different prompt, no access to the generator's rationale.
- **When does compliance happen?** Twice: pre-screen at concept level (flow step 11) and full review at stage 13.
- **When does the script lock?** Stage 16, after compliance and feasibility. This is the V1-Core → V1-Production boundary (§S).

---

## H. Schwartz Integration

### Which components consume which document

| Document | Consumed by | May influence |
|---|---|---|
| `schwartz_persuasion_framework.md` | `market-intelligence-cl` (mass desire, awareness, sophistication *evidence*); `creative-strategist` (belief bridge, identification, mechanism depth, intensification selection, alternative comparison); `script-engine` (persuasion beats, proof placement, momentum); `compliance-reviewer` (redefinition-deception and native-format-impersonation checks) | Which questions are asked of the market; how the argument is sequenced; where proof is placed; how much mechanism is explained; which objection is reframed |
| `schwartz_language_engine.md` | `script-engine` stage 7 only; ambiguity report → `compliance-reviewer` | Sentence construction, concreteness, relationship clarity, transitions, rhythm, caption load, script-to-visual translation |
| `schwartz_integration_map.md` | **Design-time only. Not a runtime resource.** | This document. It is an architecture memo about the other two; retrieving it at generation time would inject stale schema proposals into the model's context. |

### What Schwartz may never override

Both framework documents already state this, which is the strongest reason to trust it (`schwartz_persuasion_framework.md` §1; `schwartz_integration_map.md` §4). Encoded as executable precedence:

```
1  PRODUCT TRUTH                 ── a claim absent here cannot be made
2  EVIDENCE LEDGER               ── a claim without a VERIFIED claim_id is blocked
3  PLATFORM / LEGAL COMPLIANCE   ── current policy beats historical technique
4  CURRENT MARKET RESEARCH       ── observed sophistication beats assumed stage
5  REAL CUSTOMER LANGUAGE        ── verbatim beats invented register
6  CONTROLLED EXPERIMENT RESULTS ── account evidence beats framework prediction
7  BRAND CONSTRAINTS             ── stated preference beats persuasive convenience
8  SCHWARTZ FRAMEWORKS           ── advisory reasoning layer
9  CREATIVE IDEATION
```

Specifically, Schwartz may **never**:
- introduce a mechanism not in Product Truth (`schwartz_persuasion_framework.md` §13: *"Never 'invent a unique mechanism' only because a sophisticated market supposedly needs one"*)
- justify a promise beyond the Evidence Ledger
- import historical identity or gender roles as current Chilean audience facts (§10, §24)
- authorise "camouflage" that impersonates editorial or organic content (§15) — **this is the rule that overrides F3**
- convert a redefinition into concealment of a material limitation (§12)
- supply a Reason to Believe that does not exist (§24 of the Master Prompt; §13 of the framework)
- use implication to smuggle in a claim that could not be stated directly (`schwartz_language_engine.md` §15)

### Recorded for later learning, not for control

Per `schwartz_integration_map.md` §9, Creative DNA records which framework elements were used (`awareness_strategy`, `sophistication_strategy`, `belief_strategy`, `mechanism_depth`, `concreteness`, …) so the future performance layer can ask whether mechanism-led concepts outperformed promise-led ones **in this account**. These are recorded as *features of the creative*, never as predictors. No causal claim without an isolated variable.

### One correction to the integration map

`schwartz_integration_map.md` §5C proposes a twelve-field `language_quality` vector scored 0–10, and §6 embeds it in the script object. **Rejected for V1.** Twelve fabricated scalars per script × 10 scripts is 120 numbers that will look rigorous and mean nothing. Replace with four enumerated checks — `first_pass_comprehension`, `ambiguity_risk`, `spoken_naturalness`, `visual_translatability` — each `PASS | REVISE | BLOCK` with a required written justification. Reintroduce granularity only if a real experiment ever tests a language variable in isolation. (ADR-011.)

---

## I. Source / Knowledge Architecture

### The core distinction, corrected

The Master Prompt (§80) frames this as raw sources vs structured knowledge. Reading the corpus shows that is **one axis short**. `knowledge/methodology/` is structured, derived, *and* unverifiable — it fits neither box. The missing axis is **verifiability**.

### Proposed final treatment

```
sources/                         RAW, IMMUTABLE, NEVER EDITED
├── books/                       breakthrough-advertising.pdf   (text layer ✓)
│                                brilliance-breakthrough.pdf    (scan, no text layer)
└── external/                    future: fetched research snapshots (hashed, dated)

knowledge/                       DERIVED, VERSIONED, PROVENANCE-TAGGED
├── copywriting/schwartz/        ← W1 RESOLVED; correct location confirmed
│   ├── schwartz_persuasion_framework.md   tier: DERIVED_VERIFIABLE
│   ├── schwartz_language_engine.md        tier: DERIVED_VISUAL_REVIEW
│   └── schwartz_integration_map.md        tier: DESIGN_INPUT (not runtime)
├── narrative/                   authored: narrative pattern library
├── language/cl/                 grown: Chile customer language corpus
└── _quarantine/methodology/     tier: CONVERSATIONAL_DERIVED_UNVERIFIABLE
                                 scope: single niche
                                 ← restricted retrieval; see below
```

### Knowledge Provenance classification

Every knowledge file carries front-matter that travels with any retrieval hit into the prompt:

```yaml
knowledge_id:      string
tier:              DERIVED_VERIFIABLE | DERIVED_VISUAL_REVIEW |
                   CONVERSATIONAL_DERIVED_UNVERIFIABLE |
                   DESIGN_INPUT | AUTHORED
source_files:      []            # empty or unresolvable ⇒ cannot be VERIFIABLE
derivation_method: parsed_text | visual_review | authored |
                   probable_llm_derived        # ← inference, not established
derivation_confidence: OBSERVED | INFERRED     # authorship is INFERRED unless
                                               #   repo metadata establishes it
machine_verifiable: bool
human_reviewed:    bool
scope:             general | category:<x> | niche:<x>
retrieval_policy:  open | research_only | excluded
contains_claims:   none | product_claims | health_claims
version / created_at
```

Applied to what exists:

| File | tier | derivation | scope | retrieval_policy |
|---|---|---|---|---|
| `schwartz_persuasion_framework.md` | DERIVED_VERIFIABLE | parsed_text | general | **open** |
| `schwartz_language_engine.md` | DERIVED_VISUAL_REVIEW | visual_review | general | **open** |
| `schwartz_integration_map.md` | DESIGN_INPUT | authored | general | **excluded** (design-time only) |
| `modulo-1 … modulo-5`, 3 PDFs | **CONVERSATIONAL_DERIVED_UNVERIFIABLE** | **`probable_llm_derived` (INFERRED)** | **niche: PCOS hair-loss supplement / CL** | **research_only** |

The quarantine follows from **unverifiability**, which is established (the cited corpus cannot be resolved), not from **authorship**, which is inferred. If authorship were later established or refuted, `derivation_method` would change and `retrieval_policy` would not.

**`research_only` means:** a human may read it; `creative-strategist` may consult it for *structural* patterns (the 7-part UGC arc, the three testing methods, the pain→hope transition) under an explicit tier warning; and **the script engine may never retrieve it.** It supplies no claims, no benchmarks, no ingredient science, no CTA copy.

This directly resolves W4 and generalises it: *Brilliance* is not uniquely unverifiable — it is simply the one the pre-flight noticed. The methodology corpus is in the same epistemic condition and carries far more risk, because unlike *Brilliance* it contains product claims (F2) and non-compliant tactics (F3).

### Claim classification applied to the methodology corpus

Per Master Prompt §2, sampled and classified:

| Content | Class |
|---|---|
| 7-part UGC narrative arc; Hook/Story/Problem/Discovery/Solution/Results/CTA | REUSABLE_METHODOLOGY *(structure only)* |
| Three testing methods (hook / visual / concept isolation) | REUSABLE_METHODOLOGY — the best material in the corpus |
| Post ID social-proof consolidation, **own posts only** | REUSABLE_METHODOLOGY |
| Post ID extraction from **competitor** ads → Use Existing Post | **NOT_SAFE_TO_HARDCODE** — inexecutable (F4) |
| Pain → Hope transition; pure pain repels | PSYCHOLOGICAL_HYPOTHESIS |
| Garden / weed-killer analogy; DHT / insulin / inflammation model | **NICHE_SPECIFIC_EXAMPLE** + EVIDENCE_REQUIRED_CLAIM |
| Five-ingredient pharmacology (Saw Palmetto, Inositol 40:1, Berberine≈metformin, Curcumin, Zinc→SHBG) | **NOT_SAFE_TO_HARDCODE** — unsupported health claims (F2) |
| Hook Rate > 35 %, Hold Rate > 25 %, CTR > 1.5 % | **CONFIGURABLE_BENCHMARK** — contradictory (F5); never a default |
| 60–90 days active ⇒ profitable | **NOT_SAFE_TO_HARDCODE** — survivorship inference |
| "UGC Sintético", simulated Reddit/screenshots, TikTok-UI nativisation | **NOT_SAFE_TO_HARDCODE — compliance deny-list** (F3) |
| Ugly-ads / raw aesthetic beats studio production | PERFORMANCE_HEURISTIC |
| COM-B, SDT, Zeigarnik, Pratfall, mirror neurons, narrative transportation | PSYCHOLOGICAL_HYPOTHESIS |
| "[Ampliación Externa - Internet]" sections (e.g. "80 % watch without sound") | **NOT_SAFE_TO_HARDCODE** — unsourced model output inside a sourced document |

That last row is a structural finding: **provenance must be tracked at section granularity, not file granularity.** Several modules mix cited material and unsourced model speculation in one file under one heading style.

### Migration plan — RECOMMENDED ONLY, NOT EXECUTED

Deferred to Phase 3 per Master Prompt §80 and §92.

| Step | Action | Risk |
|---|---|---|
| M1 | `git mv` the two book PDFs → `sources/books/` | Low |
| M2 | `git mv` `knowledge/methodology/**` → `knowledge/_quarantine/methodology/` **unmodified** | Low — path only |
| M3 | Add provenance front-matter to every knowledge file (no content edits) | Low |
| M4 | Author the compliance deny-list from F3 | Low |
| M5 | Section-tag the "[Ampliación Externa]" blocks as unsourced | Medium — requires reading |
| M6 | Decide on OCR for *The Brilliance Breakthrough* | Optional — the derived layer already declares the limitation |
| M7 | Normalise media filenames (W7) via the Asset Registry, preserving originals | Medium |

**No step is executed in Phase 1. No file has been moved, renamed, edited or deleted.**

---

## J. Asset Architecture

### Six states *(revised — external audit Correction 3)*

The first edition had three states and two holes in them: product assets were treated as *"brand-owned by assumption"* and generated assets were *"born PRODUCTION."* Both are inference from possession, which is the one thing §91.8 forbids. A user uploading a file establishes that they possess it, not that they hold rights to it — and a model generating a file establishes nothing at all about the file's fitness to ship.

```
   user upload                    repo / third party
        │                                │
        ▼                                ▼
 USER_PROVIDED_UNVERIFIED           REFERENCE
        │                                │
        └───────────┬────────────────────┘
                    │  rights documented + human approval
                    ▼
               AUTHORIZED ──────────┐
                    │               │ used as input to generation
                    │ assigned      ▼
                    │        GENERATED_DRAFT
                    │               │ rights + compliance + QA checks pass
                    │               ▼
                    │      PRODUCTION_ELIGIBLE
                    │               │ assigned to a creative + released at Gate 3
                    └───────────────┴──────► PRODUCTION
```

| State | Meaning | Permitted |
|---|---|---|
| **USER_PROVIDED_UNVERIFIED** | Uploaded by the operator. Provenance asserted, not evidenced. **Default for all uploads.** | Internal analysis; drives generation only after the operator attests rights |
| **REFERENCE** | Present in the repo. Rights unknown or absent. | Internal analysis; structural/style abstraction only |
| **AUTHORIZED** | Documented licence/consent, territory, expiry, commercial-use scope | Everything above, plus use as production input |
| **GENERATED_DRAFT** | Model output. **Default for every generated asset.** | Internal review and QA only. **Never delivered.** |
| **PRODUCTION_ELIGIBLE** | Passed rights inheritance, compliance and Video QA | May be assigned to a creative |
| **PRODUCTION** | PRODUCTION_ELIGIBLE **and** released at Gate 3 | Appears in delivered output |

Promotion is always an explicit recorded transition, never a default and never inferred.

**Rights inheritance for generated assets.** A generated asset cannot be cleaner than its inputs. `GENERATED_DRAFT → PRODUCTION_ELIGIBLE` requires **all** of:

1. every input asset is `AUTHORIZED` (a `REFERENCE` or `USER_PROVIDED_UNVERIFIED` input blocks promotion);
2. no input is a likeness or voice lacking consent (§K);
3. compliance verdict is not `HARD_BLOCK`;
4. Video QA verdict is `PASS`;
5. `derived_from[]` lineage is complete and resolvable.

This makes the W5 exposure structural: because the nine reference videos and six voice samples are `REFERENCE`, anything generated from them is permanently stuck at `GENERATED_DRAFT`. The system cannot accidentally ship a derivative of an undocumented asset — it is not a rule someone must remember, it is a state transition that cannot fire.

**Operator attestation is recorded, not trusted silently.** For `USER_PROVIDED_UNVERIFIED → AUTHORIZED`, the operator supplies a rights basis (owned / licensed / client-supplied-with-warranty) and it is written to the registry with attributor and timestamp. It is an audit trail and a liability record, not a verification.

**All 15 current media assets are REFERENCE.** None can become AUTHORIZED without documentation that does not exist (W5).

### Registry metadata

```yaml
asset_id / type / path / sha256 / bytes / duration / created_at
source:            { origin, acquired_via, acquired_at }
rights:            { owner, licence, consent_record, commercial_use,
                     territory, expires_at, evidence_path,
                     attested_by, attested_at, rights_basis }
state:             USER_PROVIDED_UNVERIFIED | REFERENCE | AUTHORIZED |
                   GENERATED_DRAFT | PRODUCTION_ELIGIBLE | PRODUCTION
state_history:     [ { from, to, actor, at, reason } ]   # promotion is auditable
derived_from:      [ asset_id ]         # ← lineage; see §K. Generated assets
                                        #   may have several inputs; all must
                                        #   be AUTHORIZED to promote.
brand_id / product_id / tags / notes
```

`derived_from` is not cosmetic. It is the mechanism that makes W2 structurally representable rather than a paragraph someone must remember.

### By class

| Class | V1 treatment |
|---|---|
| Style references (9 MP4) | REFERENCE. Abstract structure only, never content (§L). |
| Voices (6) | REFERENCE. None production-eligible (§K). |
| Product assets | **`USER_PROVIDED_UNVERIFIED` on upload.** Promotion to AUTHORIZED requires an explicit recorded rights attestation. A campaign may still *run* on an unverified product image — Product Truth only needs to observe it — but nothing derived from it ships until attested. |
| Brand assets | `USER_PROVIDED_UNVERIFIED` → AUTHORIZED once the brand relationship is documented |
| Creators | Deferred to V1-Production. A creator is a *rights relationship*, not a file. |
| Locations | Deferred. Metadata on generated assets only. |
| Generated assets | **Born `GENERATED_DRAFT`**, with full lineage to Package, Creative, Concept and Run. Promotion requires the five-condition check above. Never delivered directly from generation. |

### Ingestion (§79)

```
incoming/ ──► validate (header, size, codec) ──► classify (type, likely role)
          ──► normalise (hash, canonical name, no manual renaming)
          ──► register (asset_id, rights=UNDOCUMENTED,
                        state = USER_PROVIDED_UNVERIFIED if operator-supplied
                              | REFERENCE               if repo/third-party)
          ──► [optional] profile
```

Original filenames are preserved in metadata. This is the correct answer to W7: canonical names are *assigned*, not typed.

---

## K. Voice Architecture

### The three problems and their resolutions

**1. The female samples are the UGC audio tracks.** The pre-flight established this from exact duration matching (58.5 s, 95.3 s, 74.8/75.0 s) and filename form (`WhatsApp-Video-…`).

*Resolution — structural, not advisory.* Each derived asset records `derived_from: <ugc_asset_id>`. The system then enforces:

> **Lineage rule.** A Style Profile and a Voice Profile that resolve to the same `derived_from` root may not be cited as independent evidence for one another. Any analysis that joins them must be labelled `CONFOUNDED_BY_SHARED_SOURCE` and cannot produce a Level A or B learning.

This makes "Voice X performs well with Style Y" (Master Prompt §38) structurally unrepresentable as a causal finding, rather than a mistake someone must remember not to make.

**2. The male samples originate from a TikTok downloader (`ssstik.io_*`).** These are third-party voices with no consent record.

*Resolution.* Permanently ineligible for PRODUCTION_VOICE. They may be used **only as descriptive targets** — to characterise a desired accent, pace and energy for casting or synthesis parameters — **never as a cloning or voice-conversion source.** Cloning an identifiable person's voice without consent is both a rights exposure and, in most jurisdictions and under most TTS providers' terms, prohibited outright. This is a harder line than W5's "document before productive use" and it should be, because the failure mode is not a missing file — it is using a real person's voice without their knowledge.

**3. Quality asymmetry** (female WAV 48 kHz uncompressed vs male MP3 44.1 kHz, one at 64 kbps).

*Resolution.* Moot for V1: no sample is production-eligible, so no acoustic comparison will be made. Recorded as a normalisation requirement for whenever a real voice corpus is acquired: a `technical_quality` enum (`BROADCAST | ADEQUATE | REFERENCE_ONLY`) with 64 kbps classified `REFERENCE_ONLY`. Never compare across quality tiers.

### Voice Profiles are NOT built in V1

Nothing in the corpus can become a Production Voice, so profiling it produces an unusable catalogue. V1-Core assigns a **Voice Specification** — a described target (accent, perceived age band, energy, pace, register, format fit) — not a voice asset. V1-Production resolves that specification against whatever legitimately licensed voice source exists at that time.

This converts a rights problem into a scheduling problem, and it means V1-Core is not blocked on it.

### Schema when profiles are eventually built

```yaml
voice_id / asset_id / derived_from
country · accent · perceived_age_band · vocal_character
energy · pace · register
technical_quality:  BROADCAST | ADEQUATE | REFERENCE_ONLY
licence_status:     UNDOCUMENTED | LICENSED | OWNED
consent_status:     NONE | RECORDED | VERIFIED     # never inferred
eligible_state:     USER_PROVIDED_UNVERIFIED | REFERENCE | AUTHORIZED |
                    PRODUCTION_ELIGIBLE | PRODUCTION      # per §J
```

`consent_status` has no default that permits use. Absence is `NONE`.

---

## L. Style Intelligence Architecture

### Target pipeline (not built in Phase 1)

```
RAW VIDEO ─► technical extraction (ffprobe: duration, fps, resolution, audio)
          ─► shot segmentation (scene-change detection)
          ─► frame sampling (N keyframes)
          ─► vision analysis over samples ─► STYLE PROFILE (structured)
          ─► human review ─► STYLE REGISTRY
```

The first three steps are deterministic and cheap. Only the fourth needs a model. That split is why Style Analysis is a Script + Tool, not a Skill (§E #5).

### V1 recommendation: three hand-authored profiles, not an extraction pipeline

The registry needs to be *populated*, not *automated*. With nine reference videos across three categories, building an extraction pipeline to produce nine profiles is more expensive than authoring three archetypes by hand — one per format — reviewing them against the samples, and moving on.

Build the extraction pipeline when the style library needs to grow faster than a person can write it. Not before. (ADR-012.)

Consistent with Master Prompt §31: **no Style Profiles were generated in Phase 1**, and only file metadata was inspected.

### Style vs content separation

The rule (§33) is that the system extracts **audiovisual grammar**, never substance:

| Extract (grammar) | Never extract (content) |
|---|---|
| Shot lengths, cut frequency, pacing curve | Competitor claims |
| Framing, camera handling, movement | Script or dialogue |
| Lighting condition and quality | Brand names, product names |
| Caption style, placement, emphasis | Specific offers or prices |
| Energy arc, emotional progression | Narrative substance |
| Product-entry timing (as a *ratio*, not a script beat) | Mechanism explanations |
| Audio bed character, transition vocabulary | Testimonial content |

The clean test: **a Style Profile should be equally applicable to a product in an unrelated category.** If it is not, content has leaked in.

`schwartz_language_engine.md` §12 states the same principle for language — separate surface wording from structural device — which is reassuring convergence.

### One caution the specification does not raise

Style extraction from competitor ads sits adjacent to F3's territory. Adopting a format's *native grammar* is legitimate (`schwartz_persuasion_framework.md` §15: Native Format Fit). Reproducing a specific competitor's recognisable creative signature is not. The Style Profile schema should carry `abstraction_level` and the review should reject any profile so specific that it identifies its source.

---

## M. Product Cold Start

The hardest requirement in the specification: Product Image + Brand → Product Truth, without hallucination.

### What each input can legitimately yield

| Input | Yields | Evidence state |
|---|---|---|
| Product image — visible form | Format, container, approximate size, apparent category | **OBSERVED** |
| Product image — visible text | *That the label says X* | **OBSERVED** (about the label) |
| Product image — visible text | *That X is true* | **INFERRED at best** |
| Brand name alone | Nothing | **UNKNOWN** |
| Brand name + successful official-source research | Positioning, catalogue, stated claims, price | **VERIFIED** (source-anchored) |
| Brand name + marketplace/retailer research | Price, availability, review language | VERIFIED (weaker source class) |
| Category knowledge | Typical properties | **INFERRED — never promotable** |

### The distinction that prevents the classic failure

> **A claim printed on the packaging is an OBSERVED fact about the packaging, and an ATTRIBUTED claim about the product. It is never VERIFIED by being visible.**

"The label states 500 mg of magnesium bisglycinate" is an observation. "The product contains 500 mg of magnesium bisglycinate" is an attributed claim requiring independent corroboration before it can enter an ad as a hard claim. Collapsing these two is exactly how an image-driven system starts inventing product facts — and it is precisely the failure that F2 shows already happened once in this corpus, at a much larger scale.

### Rejecting the single completeness score

Master Prompt §10.1 asks for `PRODUCT_TRUTH_COMPLETENESS_SCORE` and warns against fake precision. **A single number is fake precision** — 62 % complete tells an operator nothing actionable, and it averages a missing price (trivial) with missing ingredient evidence (disqualifying).

**Proposed replacement: a coverage vector plus a derived claim-freedom tier.**

```yaml
coverage:
  identity:      VERIFIED | OBSERVED | INFERRED | UNKNOWN
  category:      …
  composition:   …
  mechanism:     …
  usage:         …
  outcomes:      …
  price_offer:   …
  differentiation: …
  brand_context: …
  proof_assets:  …
```

Reported as a ten-row table an operator can act on: each `UNKNOWN` is a specific, fixable gap.

### Claim Freedom tiers (deterministic function of coverage)

| Tier | Condition | Permitted | Forbidden |
|---|---|---|---|
| **T0** | Identity not VERIFIED | Nothing produced. Halt and request input. | Everything |
| **T1** | Identity VERIFIED; composition/outcomes UNKNOWN | Observable characteristics, situational storytelling, identity/lifestyle, problem context, product interaction, category-level framing | All product-performance claims, all mechanism claims, comparisons, numbers |
| **T2** | Composition VERIFIED; outcomes not | T1 + composition statements + mechanism *at the level the evidence supports* | Outcome promises, timeframes, efficacy numbers, superiority |
| **T3** | Outcomes VERIFIED with documented evidence | T2 + evidenced outcome claims with required qualifications | Anything beyond the specific evidenced scope |

**A Level 1 cold start lands in T1.** T1 is a genuinely productive territory — it is precisely where UGC identity, problem-context and situational storytelling live — so the system remains useful at minimum input, exactly as §9 requires. It simply cannot make performance claims, which is correct.

The tier is computed by code, is identical every run, and is recorded in the Run manifest. Concepts are generated *inside* the tier, not filtered afterwards — this is what makes graceful degradation real rather than a rejection loop.

### Fallback states

| Failure | Behaviour |
|---|---|
| Image unreadable / ambiguous | `identity: UNKNOWN` → **T0** → halt, request input. Never guess. |
| Brand research returns nothing | Proceed at T1 on image observations alone |
| Conflicting sources | Record **both** in the ledger; `status: DISPUTED`; disputed claims are not usable |
| Brand ambiguous (name collision) | Halt at Gate 1 with candidates for human disambiguation |
| Category triggers regulated-claim rules (health, financial) | Cap at T2 regardless of coverage until human review — the sharpest lesson from F2 |

---

## N. Evidence Architecture

### Entity relationships (conceptual — no SQL, per §92)

```
                    ┌──────────┐
                    │  SOURCE  │  url/path · type · quality class · date · accessed
                    └────┬─────┘
                         │ 1..n
                    ┌────▼────────┐
                    │ OBSERVATION │  verbatim/extracted · cited_text · locator
                    └────┬────────┘   "31 reviews mention difficult cleaning"
              ┌──────────┼──────────┐
         n..1 │                     │ n..1
     ┌────────▼──────┐     ┌────────▼──────┐
     │    INSIGHT    │     │     CLAIM     │  a factual assertion about the product
     └────────┬──────┘     └────────┬──────┘  status · strength · risk · commercial_use
              │ 1..n                │
     ┌────────▼──────┐              │ supports
     │  HYPOTHESIS   │◄─────────────┘
     └────────┬──────┘  testable · predicted effect · counter · falsifier
              │ 1..n
     ┌────────▼──────┐     ┌───────────────┐
     │    CONCEPT    │────►│   CREATIVE    │
     └───────────────┘     └───────┬───────┘
                                   │
                           ┌───────▼───────┐    ┌──────────┐
                           │  EXPERIMENT   │───►│ LEARNING │  scope · level · freshness
                           └───────────────┘    └──────────┘
```

### Promotion rules (the point of the whole structure)

| Transition | Requirement |
|---|---|
| Source → Observation | Locator required, and it must originate from stage E1's citation set (§N.1) — never from the normaliser. |
| Observation → Insight | ≥ 1 observation cited; interpretation stated separately from the observations |
| Insight → Hypothesis | Predicted effect **and** falsification condition. No falsifier ⇒ not a hypothesis. |
| Observation → Claim | Source-quality class ≥ threshold for the claim's risk level |
| Claim → usable in a script | `status: VERIFIED` **and** claim-freedom tier permits the territory |
| Experiment → Learning | Evidence level assigned; scope recorded; **never** promoted on correlation alone |

**No transition happens implicitly.** Every one is a recorded, reviewable act. This is the mechanism that enforces §5's "never collapse these epistemic levels."

### N.1 Two-stage evidence acquisition *(revised — external audit Correction 1)*

The first edition assumed a single model call could return citation-anchored evidence **and** validate against a strict schema. It cannot: structured outputs are documented as *"Incompatible with: Citations (returns 400 error)"* (`claude-api/shared/tool-use-concepts.md:510`). Building on that assumption would have failed at the first integration test, and — worse — the natural "fix" under delivery pressure is to drop citations and let a model narrate locators from memory, which silently destroys the provenance guarantee the whole system rests on.

Evidence acquisition is therefore **two logical stages, two model calls**:

```
        SOURCE DOCUMENT / PAGE / PDF
                    │
   ┌────────────────▼─────────────────────────────────┐
   │ E1 — EVIDENCE EXTRACTION                         │
   │ citations: { enabled: true }                     │
   │ output_config.format: ABSENT                     │
   │                                                  │
   │ → prose + citation blocks:                       │
   │     cited_text · document_index · document_title │
   │     page_location | char_location                │
   └────────────────┬─────────────────────────────────┘
                    │  E1 output is the ONLY input to E2
                    │  (the source is NOT re-read)
   ┌────────────────▼─────────────────────────────────┐
   │ E2 — EVIDENCE NORMALISATION                      │
   │ output_config.format: strict ledger schema       │
   │ citations: DISABLED                              │
   │                                                  │
   │ → observation[] · claim[] · locator · relation   │
   └────────────────┬─────────────────────────────────┘
                    │
   ┌────────────────▼─────────────────────────────────┐
   │ E3 — LEDGER WRITE (deterministic, no model)      │
   │ reconciliation gate:                             │
   │   every locator ∈ E1 citation set  else REJECT   │
   │   every cited_text ⊆ E1 cited_text  else REJECT  │
   └──────────────────────────────────────────────────┘
```

**Why E2 reads E1's output rather than the source.** If E2 were given the document again, it could produce a plausible page number for a claim E1 never cited — reintroducing exactly the fabrication the citation mechanism exists to prevent. Restricting E2 to a transcription-and-typing role means it *cannot* invent a locator, only mis-transcribe one, and E3 catches mis-transcription by set membership.

**E3 is deterministic and is the actual guarantee.** The reconciliation gate is code, not judgement: a ledger record whose `locator` is not in E1's citation set is rejected outright. This is what preserves `source_id`, `locator`, cited evidence and claim relationship without either capability having to do the other's job.

**Non-document sources.** Citations apply to document blocks. For web research, the locator comes from the `web_search` / `web_fetch` result (URL + retrieved title + `accessed_at`) and E1 quotes verbatim; the same E2/E3 split and the same reconciliation rule apply, with quoted-span containment substituting for page location.

**Cost note.** Two calls per source batch, not two per claim — E1 processes a document once and yields many observations. The added cost is small relative to what a single unverifiable locator would cost in a regulated-category ad.

### Evidence Ledger fields

Master Prompt §11's proposed fields are sound. Three additions:

- **`locator`** — page / char range / URL+span / timestamp, **plus `locator_origin: E1_CITATION | E1_QUOTE`**. Without it, "traceable" means "we know which document," which is not traceability. A record with no `locator_origin` cannot be written.
- **`disputed_by[]`** — conflicting sources must coexist. A ledger that silently keeps the last write is worse than no ledger.
- **`qualification_required`** — a claim may be usable *only with* an accompanying qualification. Storing the qualification alongside the claim prevents localisation from quietly dropping it (enforced at stage 11 of §G).

### Source quality — classes, not weights

Master Prompt §17 warns against arbitrary numeric weighting. Agreed. Ordered classes, and the *claim's* risk determines the required class:

*Revised — external audit Correction 2. Class A is split.*

```
A1  regulator · authoritative independent primary evidence ·
    peer-reviewed primary research · accredited third-party lab report
A2  official manufacturer / brand documentation · spec sheet ·
    certificate of analysis · official label · official price list
B   trusted secondary · industry body · established publication
C   marketplace listing · verified purchase reviews (aggregate)
D   social discussion · Reddit · TikTok comments · forums
E   competitor advertising claims
F   unattributed blog · unknown · AI-generated
```

**Why the split.** The first edition placed regulator evidence and manufacturer documentation in one interchangeable class. That is wrong in a specific and dangerous way: a manufacturer is an authoritative source **about its own product's composition** and an *interested* source **about that product's effects**. Collapsing them means a brand's own marketing PDF could substantiate a clinical-efficacy claim — which is precisely the failure already present in this repository (F2: `modulo-4` asserts Berberine is *"comparable in clinical studies to metformin"* on the authority of an ad-copy draft). One evidence class would have let the architecture reproduce the exact error it was designed to catch.

**A2 is sufficient for** — ingredients and composition · dimensions and weight · materials · usage instructions · official specifications · official price and offer terms · label wording · certifications *held* (the fact of holding one) · country of origin · packaging contents.

**A2 is NOT sufficient for** — clinical efficacy · medical or health outcomes · comparative superiority · safety conclusions · scientific performance claims · outcome timeframes · population-level effect sizes · "clinically proven" of any form. These require **A1**.

### Claim type determines the required class

| Claim type | Minimum class | Note |
|---|---|---|
| Product identity, composition, specification, price, label wording | **A2** | Manufacturer is authoritative about its own product |
| Certification *held* | **A2** (the certificate itself) | What the certificate *implies* is a separate claim |
| Category or contextual fact | B | |
| Market prevalence / adoption | B–C | Aggregate, never anecdote |
| **Health, medical or safety outcome** | **A1** | A2 alone ⇒ `HARD_BLOCK` (§R) |
| **Clinical efficacy, "clinically proven", effect size, timeframe** | **A1** | |
| **Comparative superiority** | **A1 for both sides** | Must evidence the competitor's limitation *and* this product's advantage (`schwartz_persuasion_framework.md` §14) |
| Numeric performance claim | **A1** | |
| Durability / longevity guarantee | A1 or A2 + test data | |
| Customer *language* and verbatim register | **D preferred** | See below |

- **Customer *language* — D is the correct and preferred source.** Real customer voice does not need to be authoritative to be authentic evidence of how people speak. Conflating source quality for *facts* with source quality for *language* would push the system toward the invented-Chilean-stereotype failure §14 and §15 warn about.
- Class E is evidence of *what competitors assert*, never of what is true.
- **A2 masquerading as A1 is a named failure mode.** A brand page citing "studies" without identifying them is A2, not A1. The ledger records `source_class` from the artefact actually retrieved, never from what that artefact claims about its own basis.

---

## O. Creative Hypothesis / Concept Architecture

Eight terms, eight distinct objects. Collapsing any pair breaks experimentation.

| Object | Definition | Cardinality | Test |
|---|---|---|---|
| **Hypothesis** | A testable expectation with a predicted effect and a falsification condition | 20–30 per campaign | *Can it be proven wrong?* If not, it is an opinion. |
| **Angle** | The strategic entry point into the market — which desire, which belief, which awareness state | Attribute **of** a hypothesis | *Does it name where the argument enters?* An angle is not an object of its own; it is the hypothesis's routing. |
| **Concept** | A selected hypothesis developed into a complete strategic idea: message, promise, RTB, product role, format fit | 10 selected | *Could two different creators execute it and produce recognisably the same argument?* |
| **Hook** | The entry mechanism. Four separable parts: strategy, copy, visual, audio | 1..n per creative | *Does changing it change the argument?* If yes, it is a new Concept, not a new Hook. |
| **Creative** | One specific audiovisual execution of one Concept | 1..n per Concept | *Is there a single script and a single production package?* |
| **Variant** | A creative differing in exactly **one** declared dimension | 0..n per Creative | *Is exactly one thing different, and is that recorded?* If more, it is a new Creative. |
| **Experiment** | A comparison with a declared variable, locked variables and a measurement plan | 1..n per campaign | *Can it answer "what changed?" and "what was held constant?"* |
| **Meta Ad** | A published entity in Meta with its own ad ID and, via Post ID, possibly shared social proof | 1..n per Creative | *Does it exist in Meta's system?* |

### Two boundaries that are easy to get wrong

**Hook vs Concept.** A new hook *copy* is not a new concept (§48). But a hook that enters through a *different awareness state* is a different argument, and therefore a different concept. The discriminator is: **does the belief bridge still start from the same current belief?** If not, it is a new Concept.

**Creative vs Variant vs Meta Ad.** One Concept → several Creatives (different formats). One Creative → several Variants (one dimension each). One Creative → several Meta Ads (different ad sets, and via Post ID possibly *the same* post ID across them). The Post ID technique means the Creative ⟷ Meta Ad mapping is genuinely many-to-many and the *social proof attaches to the post, not the ad* — which is why `META_AD_ID` and `POST_ID` must both exist and must not be collapsed. The specification's §55 list omits `POST_ID`; it should be added.

### Identifier hierarchy — 12 proposed, 8 needed for V1-Core

Keep: `BRAND_ID`, `PRODUCT_ID`, `CAMPAIGN_ID`, `HYPOTHESIS_ID`, `CONCEPT_ID`, `CREATIVE_ID`, `ASSET_ID`, `RUN_ID`.
Add at V1-Core: `CLAIM_ID` (the Evidence Ledger's key — arguably the most important ID in the system, and absent from §55).
Defer to their owning phase: `EXPERIMENT_ID` (created at Gate 2, so V1-Core), `STYLE_ID` (V1-Core, small), `VOICE_ID` (V1-Production — no production voices exist yet), `META_AD_ID` + `POST_ID` (performance layer).

---

## P. Experiment Architecture

### Representation

```yaml
experiment_id / campaign_id / created_at
hypothesis_ids:      []
declared_variable:   awareness_state | angle | hook_copy | hook_visual |
                     format | narrative_pattern | style | mechanism_depth | offer
locked_variables:    []          # everything else, enumerated explicitly
arms:
  - { arm_id, creative_id, role: control|variant, variable_value }
measurement_plan:    { primary_metric, guardrail_metrics, minimum_exposure,
                       decision_rule, planned_duration }
confounders_known:   []          # ← required, not optional
evidence_level:      A | B | C | D        # assigned at analysis, never at design
scope:               { product, category, market, audience, format, period }
```

**`locked_variables` must be enumerated, not implied.** "Everything else is the same" is how confounded experiments get written. The validator compares the declared locks across arms and fails the design if any differs.

### Evidence levels — accepted with two amendments

| Level | Meaning |
|---|---|
| **A — Controlled** | One variable isolated; locks verified; exposure sufficient; known confounders documented and bounded |
| **B — Correlational** | Multiple factors differ, or isolation could not be verified. Directional only. |
| **C — Signal** | Interesting but insufficient exposure or unclear attribution. Generates hypotheses, never conclusions. |
| **D — Contradicted** *(added)* | A prior learning that later evidence contradicts |

**Amendment 1 — add Level D.** Without it, a learning can only accumulate confidence, never lose it. Contradiction is information and must be storable.

**Amendment 2 — `scope` is mandatory on every level.** §70 is right that "UGC works" is worthless. Scope is what makes a learning re-findable and correctly re-applicable.

### The honest caveat about Level A on Meta

Meta's delivery optimisation does not split traffic evenly between ads in an ad set; it allocates toward predicted performers. So a naive 10-ads-in-one-ad-set comparison is **not** a controlled experiment — differences in outcome partly reflect the algorithm's allocation decisions, not audience response.

**Practical consequence:** most learnings this system produces will be **Level B**. That is fine, and it is far better than a system that labels them A. Design for B; reach for A only where the question justifies a dedicated structure (separate ad sets, budget floors, sufficient exposure), and record in `confounders_known` what the delivery algorithm is contributing.

Stating this in Phase 1 prevents the most likely long-term failure: a learning store full of confident, confounded conclusions.

### The four questions (§57)

The schema answers each directly: **What did we test?** `hypothesis_ids` + `declared_variable`. **What changed?** `arms[].variable_value`. **What was held constant?** `locked_variables`, verified. **What can we conclude?** Bounded by `evidence_level` + `scope`. **What can't we?** Everything in `confounders_known`. **What next?** Level C signals feed the next hypothesis pool.

---

## Q. Creative Diversity Architecture

### Reject the numeric diversity score for V1

A "diversity: 0.72" tells an operator nothing and cannot be argued with. Two mechanisms instead, both explainable.

### 1. Hard constraints vs diversity targets *(revised — external audit Correction 4)*

The first edition made every spread dimension an unconditional hard constraint. **That was a serious error.** A solver told it *must* produce ≥ 4 distinct core problems, given research that only evidences two, has one way to comply: the upstream strategist invents the missing two. The document's central safety property — never invent evidence — would have been defeated by its own diversity mechanism, and defeated *invisibly*, because the output would look admirably diverse.

Diversity is a **quality objective**. Evidence is a **constraint**. When they conflict, evidence wins — the same precedence the rest of the document applies everywhere else.

**HARD CONSTRAINTS** — never relaxed, because satisfying them requires no new evidence:

| Constraint | Basis |
|---|---|
| Format mix as specified (e.g. 5 UGC / 2 Podcast / 3 Animation) | User instruction; an execution choice, not an evidence claim |
| No near-duplicate pair (≥ 4 of 6 dimensions shared) | Prevents redundancy; needs no new evidence to satisfy — drop a concept, don't invent one |
| Every concept within the claim-freedom tier | Safety |
| Every concept passes the compliance pre-screen | Safety |
| Every concept traceable to ≥ 1 hypothesis and ≥ 1 observation | Provenance |
| Production feasibility within ceiling | Executability |

**DIVERSITY TARGETS** — desired, measured, reported, *relaxable*:

| Dimension | Target distinct values across 10 | Depends on |
|---|---|---|
| Awareness state | ≥ 3 | Research evidencing multiple awareness states |
| Core problem | ≥ 4 | Research evidencing distinct problems |
| Dominant desire | ≥ 3 | Research |
| Current belief bridged | ≥ 3 | Research |
| Angle mechanism | ≥ 4 | Product Truth + research |
| Psychological hypothesis | ≥ 4 | Research |
| Narrative pattern | ≥ 5 | **None — authored library.** Borderline hard; see below. |

Narrative pattern is the one target that depends on no research: the library is authored and any concept can be told several ways. It is nonetheless kept a *target*, because forcing a narrative pattern that fights its concept produces a worse ad than repeating a pattern that fits.

### 2. When a target cannot be met

The solver never fabricates. It returns:

```yaml
status: INSUFFICIENT_EVIDENCE_FOR_DIVERSITY_TARGET
unmet_targets:
  - dimension: core_problem
    target: 4
    achieved: 2
    achieved_values: [ ... ]
    limiting_factor: only 2 distinct problems evidenced in research
    supporting_observation_ids: [ ... ]
resolution_options:
  - ADDITIONAL_RESEARCH        # widen the evidence base, re-run
  - RELAX_TARGET               # human approval, recorded with reason
  - REDUCE_BATCH_DIVERSITY     # fewer concepts, each better grounded
  - REDUCE_BATCH_SIZE          # 10 → n, with rationale
```

This surfaces at **Gate 2** as an explicit decision, never as a silent degradation and never as an invention. `ADDITIONAL_RESEARCH` is the default recommendation: a thin evidence base is a research finding, and it is more valuable surfaced than papered over.

**Recorded in the Run manifest** either way, so a later performance analysis knows whether a batch was genuinely diverse or diverse-by-relaxation. A batch that met 4 of 7 targets is a different experimental object from one that met 7, and the learning store must be able to tell them apart.

Selection therefore maximises the strategist's qualitative ranking **subject to the hard constraints**, using target attainment as the objective — not as a feasibility condition.

`schwartz_integration_map.md` §8 offers an illustrative allocation (C01 Problem-Aware/identification/UGC … C10 Most-Aware/proof+offer/UGC) and correctly labels it *"an example of diversity dimensions, not a fixed recipe."* Treated exactly that way: it validates the dimension set, and is not a template.

### 3. Pairwise near-duplicate detection (hard constraint + post-selection audit)

For each of the 45 pairs, count shared values across {problem, desire, current belief, awareness, angle mechanism, narrative pattern}. **≥ 4 of 6 shared ⇒ flagged as a near-duplicate pair**, surfaced at Gate 2 with both concepts side by side.

Deterministic, explainable, and it produces a specific artefact a human can overrule with a reason.

### 4. Human read at Gate 2

Semantic duplication that survives both checks — ten concepts that differ on paper and say the same thing out loud — is caught by a person reading the ten core messages consecutively. No mechanism substitutes for this, and the batch is small enough that it costs minutes.

### The threat the specification underweights

The real duplication risk is not that the model produces ten similar concepts. It is that **the research phase produces a narrow evidence base**, and ten genuinely distinct concepts drawn from it are all variations on the two or three things the research found. Diversity must therefore be checked at the **hypothesis pool** stage too: if 30 hypotheses collapse into four clusters, the correct action is more research, not better selection. That check belongs before Gate 2, and it is cheap.

The hard-constraint/target split above is what makes this work. Under the first edition's design, a narrow evidence base was *invisible* — the solver was obliged to hit its spread numbers, so it would have been satisfied by fabrication and the operator would have seen a healthy-looking batch. Under the revised design, a narrow evidence base surfaces as `INSUFFICIENT_EVIDENCE_FOR_DIVERSITY_TARGET` with the limiting dimension named. **The diversity mechanism becomes a research-quality detector rather than a fabrication incentive** — which is what it should have been from the start.

---

## R. Human Review Architecture

### Four proposed gates → three

| Gate | Reviews | Verdict | Why here |
|---|---|---|---|
| **Gate 1 — Truth & Evidence** | Product Truth coverage vector, Evidence Ledger, claim-freedom tier, disputed claims | **KEEP — blocking** | Everything downstream inherits these errors, and this is the cheapest possible place to catch a hallucinated product fact. Reviewing ten scripts to discover the product was misidentified is the worst outcome the system can produce. |
| **Gate 2 — Concepts & Experiment Plan** | 10 selected concepts, diversity audit, near-duplicate flags, declared/locked variables, compliance pre-screen results | **KEEP — blocking** | Highest-leverage human judgement in the system. Market intuition is worth most here, and ten wrong bets are caught before ten full scripts are written. |
| ~~Gate 3 — Final Scripts~~ | | **MERGE into Gate 4** | Splitting adds a review cycle without adding information. The reviewer would need the storyboard and feasibility data to judge a script's viability anyway — so give them the whole Package once. |
| **Gate 3 — Production Release** *(was Gate 4)* | Complete Production Packages: scripts, storyboards, shot lists, compliance reviews, feasibility, claim-evidence report | **KEEP — blocking** | Last point before money is spent and before legal exposure becomes real. This is the signature that matters. |

**Result: 4 → 3.** Compliance review is an *input* to Gate 3, not a gate of its own — a review nobody reads is not a control.

### What each gate can do

| Action | G1 | G2 | G3 |
|---|---|---|---|
| Approve / Reject campaign | ✓ | ✓ | ✓ |
| Correct a field directly | ✓ | — | — |
| Swap a concept from the pool | — | ✓ | — |
| Send an individual creative back for revision | — | — | ✓ |
| Accept a `LOW` / `MEDIUM` risk verdict | — | ✓ | ✓ |
| Adjudicate `POLICY_REVIEW_REQUIRED` / `HIGH_RISK` | — | ✓ | ✓ |
| Relax a diversity target (recorded, §Q) | — | ✓ | — |
| Clear a **`HARD_BLOCK`** by changing the underlying state | ✓ | ✓ | ✓ |
| Approve past a **`HARD_BLOCK`** leaving state unchanged | ✗ | ✗ | ✗ |

### Two block classes *(revised — external audit Correction 5)*

The first edition had one non-overridable `BLOCK`, and it conflated two very different things. Making an LLM's *interpretation* irreversible is wrong twice over: it gives a probabilistic judgement the authority of a deterministic fact, and it creates a dead end an operator cannot resolve even when the model is simply mistaken about ambiguous policy language.

| | **`HARD_BLOCK`** | **`POLICY_REVIEW_REQUIRED` / `HIGH_RISK`** |
|---|---|---|
| **Produced by** | Deterministic code only | Model judgement, human judgement, or ambiguity |
| **Triggers** | Hard claim with no VERIFIED `claim_id` · claim's evidence class below the §N minimum (e.g. health claim on A2 alone) · missing rights/consent for a required asset · explicit deny-list violation (F3 synthetic-organic impersonation) · localisation altered a claim · unresolvable lineage | Ambiguous claim wording · implication possibly carrying an unstated claim · borderline testimonial or before/after usage · native-format fit approaching impersonation · category-sensitive framing · unclear qualification sufficiency |
| **Resolution** | **Change the underlying state**: supply evidence, obtain rights, remove the claim, rewrite the line. Then the check re-runs and passes on its own. | **Human adjudication** against current platform policy, recorded with reasoning |
| **Overridable by approval alone?** | **No** — and "no" is meaningful here, because the check is mechanical: there is nothing to disagree with | **Yes** — that is its entire purpose |
| **Escalates to** | Nobody. It is not a decision. | Gate 2 or Gate 3 |

**An LLM cannot raise a `HARD_BLOCK`.** Only deterministic checks can — §G stages 10, 11 and 14, plus the deny-list matcher and the §J rights checks. The `compliance-reviewer` Skill emits `LOW | MEDIUM | HIGH_RISK | POLICY_REVIEW_REQUIRED`; it never emits `HARD_BLOCK`. This is the direct consequence of §C.3 (deterministic where determinism is possible) applied to its own enforcement layer, and the first edition failed to apply it there.

**A `HARD_BLOCK` is not an appeal, it is a state description.** "This claim has no verified evidence" is not overturned by agreeing to proceed — it is overturned by producing the evidence. Which is why it is not human-overridable, and also why that is not a hardship: the remedy is always available and always specific. Every `HARD_BLOCK` names the exact missing artefact.

**Recorded either way.** Both classes write to the Run manifest's `rejections[]` (§W), with adjudications recorded against the reviewer. This is what later makes the false-block rate measurable — and therefore what makes automating a gate defensible rather than hopeful. (ADR-016 revised; ADR-032 added.)

### Configurable automation later

Once a golden test set exists (§85) and false-block/false-pass rates are measured, Gate 1 may become conditional (auto-pass at T3 with zero disputed claims) and Gate 2 conditional (auto-pass when spread constraints are satisfied with no near-duplicate flags). **Gate 3 should remain mandatory** while the system can produce regulated-category claims. Not automated in V1.

---

## S. Production Boundary

### The contract

V1-Core hands V1-Production a **locked, versioned, self-sufficient Production Package**. V1-Production may not re-decide anything (§62, §91). The only backward path is a QA-triggered revision request that re-enters V1-Core at stage 6 of §G.

### A Production Package must contain

**Identity & lineage** — `package_id`, `creative_id`, `concept_id`, `hypothesis_id`, `experiment_id`, `campaign_id`, `product_id`, `brand_id`, `run_id`, `script_version_hash`.

**Strategy (read-only context, so production understands *why*)** — audience segment, awareness state, sophistication, mass desire, angle, psychological hypothesis, current/desired belief, promise, reason to believe, product role.

**Script (complete)** — full word-for-word dialogue or voiceover; persuasion beats with the lines that carry each; on-screen text; captions with timing; CTA verbatim; **for Podcast: per-speaker attribution, turn boundaries, reactions, interruptions, pauses**.

**Execution spec** — format, narrative pattern, `style_id`, **voice specification** (not `voice_id` — §K), target duration, pacing intent.

**Scene plan** — per scene: `scene_id`, start/end, shot type, camera, subject, action, dialogue segment, product presence, on-screen text, performance direction, lighting, transition, audio, **continuity notes**.

**Continuity manifest** — character, wardrobe, product appearance, location, lighting, voice, style. This is what survives across clip boundaries and it is the single most important field group given the ~15-second ceiling (§T).

**Segmentation plan** — generation units within the tool's duration limit, with continuity anchors at each seam.

**Assets** — product images, brand assets, style reference, proof assets. Each with `asset_id` and state.

**Constraints** — **negative constraints** (what must never appear or be said), required qualifications, claim-freedom tier, compliance verdict with rationale.

**Reports** — claim→evidence report (every hard claim → `claim_id` → source), creative QA verdict, feasibility assessment, tool routing recommendation.

### Definition of Done

A Production Package is complete when a competent operator or tool can produce the video **without asking a single strategic question.** If production must decide what the ad is arguing, who it is for, or what it may claim, V1-Core has failed and the boundary has leaked.

The concrete test, from §41: no line reading "Creator explains the benefit." Every line is *the* line. No direction reading "Show the product." Every product appearance specifies when, how framed, what movement, what action, how long, and why.

---

## T. V1-Production Architecture

**Conceptual only. No integration implemented. No capability assumed.**

### The verified constraint that shapes everything

Higgsfield states **video generation up to ~15 seconds** (§0.2). The corpus's own case study describes 30–45-second bodies and 2–3-minute VSLs.

**Therefore V1-Production is a segmentation-and-assembly system, not a generation system.** A 45-second UGC ad is 3–5 generation units with character, wardrobe, product, lighting and voice continuity across every seam. This is the dominant engineering problem, and Master Prompt §64 already anticipates it — the verified duration figure confirms it is mandatory, not contingent.

### Routing by format

```
              APPROVED PRODUCTION PACKAGE
                        │
                ┌───────▼────────┐
                │ PRODUCTION     │  reads format · scene plan ·
                │ ROUTER         │  continuity · feasibility
                └───────┬────────┘
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
   ┌───────┐       ┌─────────┐      ┌──────────┐
   │  UGC  │       │ PODCAST │      │ ANIMATION│
   └───┬───┘       └────┬────┘      └────┬─────┘
       │                │                │
  single presenter  TWO speakers     no human likeness
  to-camera         turn-taking      object/motion driven
  continuity:       reaction shots   continuity:
   face·wardrobe    camera switching   style·palette·objects
   ·location        continuity ACROSS  visual metaphor
   ·product         speakers + lipsync
       │                │                │
       └────────────────┼────────────────┘
                        ▼
              SEGMENT ──► GENERATE ──► VIDEO QA
                              ▲            │
                              └── RETRY ◄──┤ (bounded, costed)
                                           ▼
                                  ASSEMBLE ──► FINAL VIDEO
```

### Risk assessment per format

| Format | Continuity burden | Critical dependency | Verified? | Risk |
|---|---|---|---|---|
| **Animation** | Style/palette/object consistency. **No human likeness, no lipsync.** | Image/video generation + voiceover | Generation ✓ · voiceover ✗ | **LOWEST** |
| **UGC** | One face, wardrobe, location, product across 3–5 clips | Character consistency (Soul) + speech/lipsync | Soul vendor-stated ✓ · **lipsync UNVERIFIED** | **MEDIUM** |
| **Podcast** | **Two** faces, two wardrobes, shared location, cross-speaker camera switching, reaction shots, turn-taking lipsync, over ~8–12 clips | Multi-character consistency + multi-speaker lipsync + shot/reverse-shot continuity | **UNVERIFIED — no evidence found** | **HIGHEST** |

### Recommendation: stage V1-Production by verified risk

The target remains 10 final videos. The recommendation concerns **order**, so that a capability gap is discovered on clip one rather than on package seven:

1. **Stage 1 — Animation.** Lowest continuity burden, no likeness or lipsync dependency. Proves segmentation, continuity propagation, QA and assembly end-to-end.
2. **Stage 2 — UGC.** Adds character consistency and lipsync. Highest strategic value (the corpus's whole method is UGC-centred) and the format most likely to be produced at volume.
3. **Stage 3 — Podcast.** Only after a **capability spike** confirms multi-speaker consistency and lipsync actually exist.

**Mandatory prerequisite before any V1-Production build:** a capability spike against Higgsfield's live API/MCP to establish — not assume — the tool inventory, per-model duration limits, whether speech/lipsync exists, whether multi-character consistency exists, continuity controls, and cost per generation. §63 requires this and the evidence in §0.2 shows why: the two capabilities Podcast depends on are precisely the two I could not verify. (ADR-019.)

**Fallback if lipsync is unavailable:** UGC and Podcast require a different pipeline — licensed human creators filmed to the approved script, with AI used for B-roll and assembly. This changes V1-Production's economics substantially and must be discovered by a spike, not by a failed batch.

---

## U. Future Performance Loop

V1 need not implement any of this. It must not make it impossible. The minimum obligations:

### 1. Join keys on every Creative DNA record

`creative_id` · `concept_id` · `hypothesis_id` · `experiment_id` · `campaign_id` · `product_id` · `brand_id` · `run_id` — plus, at publication time, `meta_ad_id` **and** `post_id` (they are different things, and social proof attaches to the post).

### 2. Feature dimensions recorded at creation, never back-filled

Awareness state, sophistication, angle mechanism, psychological hypothesis, belief strategy, mechanism depth, format, narrative pattern, `style_id`, hook strategy, hook copy/visual/audio identifiers, duration, CTA type, offer reference, claim-freedom tier, language features. Back-filled features are reconstructions, and reconstructions become fiction.

### 3. Experimental context travels with performance

A metric without `declared_variable`, `locked_variables` and `confounders_known` cannot become a learning. This is the interface that prevents §5's epistemic collapse once real numbers arrive and the temptation to conclude is strongest.

### 4. Version pinning

Every creative records the Product Truth version, market snapshot, knowledge versions, Skill versions, prompt versions and model ID in force when it was made — otherwise a learning cannot be attributed to what actually produced it.

### 5. Metric definitions stored explicitly, never assumed

F5 proved the corpus disagrees with itself about what Hold Rate even means (two denominators, one sentence). Every stored metric carries its formula:

```yaml
metric: hold_rate
numerator: video_plays_15s
denominator: video_plays_3s        # explicit — NOT "impressions or 3s views"
computed_at / source: meta_api
```

### 6. No thresholds in V1

No Hook Rate, Hold Rate or CTR target is stored as a default anywhere (§59, F5). Thresholds are computed later from the account's own distribution, per category, format, duration, placement and objective.

### Deferred and correctly so

Ingestion, diagnosis engine, learning store, freshness/decay, fatigue detection, exploration/exploitation allocation. Building them now means building against imagined data.

---

## V. Storage Decision

### Verdict: **ACCEPT Filesystem + SQLite, with one amendment.**

**Amendment: git-tracked JSON/YAML is the system of record. SQLite is a derived, rebuildable index.**

### Why the amendment

Master Prompt §82 requires versioning of a dozen artefact types, and §84 requires that any creative be reconstructible from what existed when it was made. **That is version control**, and git already does it correctly — content-addressed, tamper-evident, diffable, branchable, with full history.

Implementing artefact versioning inside SQLite means building `*_versions` tables, an "as-of" query layer, and a diff mechanism — reimplementing git, worse, and in a database with no merge story. Meanwhile a corrupted single-file database loses everything at once, whereas a corrupted JSON file loses one artefact and git still has its history.

So:

| Concern | Store | Rationale |
|---|---|---|
| Product Truth, Evidence Ledger, Concepts, Scripts, Packages, Run manifests, Experiment definitions | **Git-tracked JSON/YAML** | Versioning, diffing, reproducibility, auditability, human-readable review |
| Media binaries | Filesystem, git-ignored, content-hashed | Too large for git; registry holds the metadata |
| Cross-object queries, joins, performance analytics, learning retrieval | **SQLite (derived)** | Rebuildable from the artefact store at any time; losing it costs a rebuild, not data |
| Full-text over customer language | SQLite FTS5 | Fits naturally alongside |

The invariant: **SQLite must always be reconstructible from the filesystem.** If it ever holds data that exists nowhere else, the amendment has been violated.

### Practical notes

- **`sqlite3` is not installed** (§0.3). The Python standard library ships `sqlite3` as a module, so installing Python satisfies this; the CLI is a convenience.
- Schema design belongs to Phase 2 (§81, §92). **No tables designed here.**
- Postgres is unnecessary: single-user, single-machine, modest volume. Revisit only for concurrent multi-user access.

---

## W. Versioning / Reproducibility

### Minimum requirements

**Every durable artefact carries:** `version` (monotonic), `created_at`, `created_by_run_id`, `content_hash`, `supersedes` (previous version id), `inputs[]` (id + version of every input consumed).

**Every run produces a manifest:**

```yaml
run_id / campaign_id / started_at / ended_at / status
onboarding_level:   1|2|3|4
inputs:             { product_image_hashes[], brand, user parameters }
versions:
  product_truth · brand_snapshot · market_snapshot · audience_model
  knowledge:      { schwartz_persuasion, schwartz_language, narrative_lib,
                    cl_language_corpus }          # content hashes
  skills:         { product-intelligence, market-intelligence-cl,
                    creative-strategist, script-engine, compliance-reviewer }
  prompts:        { … }
  models:         { claude-opus-5, … }            # exact IDs
  style_library / compliance_ruleset
sources_consulted:  [ { source_id, url, accessed_at, quality_class } ]
decisions:          [ { stage, decision, rationale, alternatives_rejected } ]
rejections:         [ { stage, item, reason } ]   # ← what was BLOCKED and why
gates:              [ { gate, reviewer, verdict, at, overrides[] } ]
errors / retries:   [ … ]
cost:               { by_stage, total_tokens, total_usd }
outputs:            [ artefact ids + versions ]
```

### The standard: re-derivable, not re-runnable

An LLM pipeline is not bit-reproducible, and pretending otherwise is a false promise. The achievable and useful standard:

> **Given a `run_id`, it must be possible to reconstruct exactly what the system knew, what it consulted, what it decided, what it rejected, and under which versions of every input and instruction — even if re-running it would produce different words.**

That is what makes a creative decision explainable eighteen months later (§91.24), and it is enough to attribute a performance result to a cause.

### `rejections[]` deserves emphasis

Most pipelines log what they produced. Recording what was **blocked and why** is what turns the Evidence Ledger and the compliance layer from decoration into an auditable control — and it is the only way to later measure the false-block rate that would justify automating a gate (§R).

---

## X. Major Risks

Ranked within each class. Assessments reflect findings F1–F5 and §0.3.

### Technical

| Risk | Level | Notes |
|---|---|---|
| **No runtime installed** (Python, Node, SQLite, ffmpeg all absent) | **MEDIUM** *(was HIGH)* | Gates *execution* from Phase 5, not design from Phase 2. Cheapest item on the critical path. `IMPLEMENTATION_PREREQUISITE` PRE-01. |
| **Automated runtime has no provisioned API access or cost model** | **MEDIUM** | The interactive Claude Code entitlement does not supply it (§D.1). Discovering this at Phase 5 stalls the build. ADR-033. |
| ~~Citations + structured outputs assumed composable~~ | **RESOLVED** | Would have failed at first integration, and the tempting fix — drop citations — silently destroys provenance. Fixed by the E1/E2/E3 split (§N.1). |
| Continuity across ~15 s generation units for 30–60 s ads | **HIGH** | The dominant V1-Production engineering problem (§T) |
| Higgsfield tool inventory / lipsync / multi-speaker unverified | **HIGH** | Podcast depends on two capabilities I could not confirm exist |
| Orchestration complexity across ~16 stages × 10 creatives with bounded retries | MEDIUM | Mitigated by the deterministic/generative split |
| Assembly quality at clip seams | MEDIUM | Discoverable only by the spike |

### Data

| Risk | Level | Notes |
|---|---|---|
| **Methodology corpus contamination** — medical claims (F2), deceptive tactics (F3), inexecutable procedure (F4), contradictory benchmarks (F5) | **HIGH** | Would produce unsafe output on day one if retrieved naively. Mitigated by §I quarantine. |
| **Circular evidence** — female voices derived from UGC videos (W2) | MEDIUM | Mitigated structurally by `derived_from` + the lineage rule (§K), not by a note |
| Provenance tracked at file rather than section granularity | MEDIUM | Sourced and unsourced content coexist under one heading style |
| Missing citation corpus — module markers unresolvable | MEDIUM | Contributes to the UNVERIFIABLE tier |
| Evidence Ledger silently degrading into an unpopulated formality | MEDIUM | Mitigated by the `HARD_BLOCK` at §G stage 10 — a ledger that gates is a ledger that gets used |
| **Manufacturer documentation substantiating clinical claims** | **MEDIUM** *(newly named)* | The exact shape of F2. Mitigated by the A1/A2 split and the claim-type matrix (§N). Was invisible under a single class A. |
| **Diversity quota driving fabrication of pains, desires or beliefs** | **MEDIUM** *(newly named)* | Unconditional spread constraints made invention the cheapest compliance path, and the result would have *looked* healthy. Mitigated by the hard-constraint/target split and `INSUFFICIENT_EVIDENCE_FOR_DIVERSITY_TARGET` (§Q). |
| **Rights inferred from upload or generation** | **MEDIUM** *(newly named)* | "Brand-owned by assumption" and "born PRODUCTION" were both inference from possession. Mitigated by the six-state model and rights inheritance (§J). |

### LLM

| Risk | Level | Notes |
|---|---|---|
| **Hallucinated product claims at cold start** | **HIGH** | The system's defining failure mode. Mitigated by evidence states, claim-freedom tiers, the label/product distinction (§M), and the stage-10 BLOCK |
| **False precision** — ~60 fabricated 0–1 and 0–10 scores | **HIGH** | Produces confident nonsense that *looks* rigorous. Mitigated by enumerations (§C.8, ADR-011) |
| Generator grading its own work | MEDIUM | Mitigated by separate critic with separate context |
| **Model judgement creating an irreversible dead end** | **LOW** *(newly named, now mitigated)* | A single non-overridable `BLOCK` gave an LLM interpretation the finality of a mechanical fact. Mitigated by ADR-032: only deterministic services raise `HARD_BLOCK`. |
| Drift across a 16-stage chain — late stages contradicting early ones | MEDIUM | Mitigated by deterministic invariance checks at 10 and 11 |
| Cost drift on 10 creatives × critic × up to 2 revisions | MEDIUM | Mitigated by Batch API for the pool, caching for the knowledge prefix, hard retry ceilings |

### Media generation

| Risk | Level | Notes |
|---|---|---|
| Character/product fidelity failure across clips | **HIGH** | Central to UGC and Podcast |
| Unbounded retry spend | MEDIUM | Mitigated by max-retries + budget ceilings + escalation (§66) |
| Artefacts — hands, on-screen text, logos | MEDIUM | Video QA checks; some proportion will need manual review |
| Podcast infeasibility on current tooling | **HIGH** | Confront via spike before committing (§T) |

### Compliance

| Risk | Level | Notes |
|---|---|---|
| **Health/supplement claims in a regulated category** | **HIGH** | The corpus's own niche is health. F2 shows unsupported pharmacological claims already present in the knowledge base. |
| **Deceptive native-format impersonation** (fabricated Reddit threads, simulated screenshots, TikTok-UI camouflage) | **HIGH** | Actively recommended by the corpus (F3); explicitly forbidden by the Schwartz layer. Needs a hard deny-list. |
| Testimonial and before/after usage | MEDIUM | Category-sensitive; requires policy fetch at review time |
| Unverifiable comparative claims | MEDIUM | Concentration/comparison angles need evidence for both halves |
| Manufactured urgency/scarcity | LOW–MEDIUM | The corpus's "limited artisanal batches (real scarcity)" needs the word *real* enforced |

### Rights

| Risk | Level | Notes |
|---|---|---|
| **TikTok-sourced male voices** (`ssstik.io_*`) as a cloning source | **HIGH** | Voice cloning without consent — legal exposure plus provider ToS violation. Hard-blocked in §K. |
| Zero rights documentation on 15 media assets (W5) | **HIGH** | REFERENCE-only until documented; no inference from possession |
| Style extraction shading into competitor-signature copying | MEDIUM | Mitigated by `abstraction_level` + the cross-category test (§L) |

### Experimentation

| Risk | Level | Notes |
|---|---|---|
| **Meta delivery optimisation confounding every comparison** | **HIGH** | Structural, not fixable. Must be declared, not concealed. Most learnings will be Level B (§P). |
| Insufficient exposure — 10 creatives, modest budget, purchase objective | **HIGH** | Statistical power will frequently be inadequate for confident conclusions |
| Learning store accumulating confident but confounded conclusions | **HIGH** | The slowest and most damaging failure. Mitigated by mandatory `scope`, evidence levels, Level D |
| Variable leakage across arms | MEDIUM | Mitigated by the deterministic locked-variable validator |

### Overengineering

| Risk | Level | Notes |
|---|---|---|
| **26 artefacts, 12 ID types, 30 stages, ~60 scored fields for a system with zero users** | **HIGH** | The most likely reason this never ships. §Y. |
| Building the performance layer before any performance data exists | **HIGH** | Deferred |
| Style/voice profiling pipelines for corpora that cannot be used in production | MEDIUM | Replaced by three hand-authored profiles and a voice *specification* |
| Context/news intelligence | LOW | Correctly deferred by the specification itself |

---

## Y. Simplification Opportunities

Master Prompt §Y invites aggression. Each item below states what is cut and what is preserved, because scope is the user's decision, not mine.

### 1. 26 batch artefacts → 8 artefact types

Most §88 entries are **fields**, not documents. Format / Narrative / Style / Voice Assignments, Hooks, Chile Localization and Creative DNA are all properties of the Creative object. Emitting them as seven documents creates seven chances for them to disagree.

| Proposed artefact | Absorbs |
|---|---|
| 1. Campaign Brief | 1 |
| 2. Product Truth *(Evidence Ledger as its ledger)* | 2, 3 |
| 3. Research Dossier | 4, 5, 6, 7 |
| 4. Hypothesis Pool *(scoring inline)* | 8, 9 |
| 5. Experiment Plan *(selection + diversity audit inline)* | 10, 11, 12 |
| 6. **Creative Record ×10** *(script, storyboard, shot list, DNA, QA, compliance, all assignments)* | 13–25 |
| 7. Production Package ×10 *(production-facing render of #6)* | 25 |
| 8. Meta Test Plan | 26 |

**Nothing is lost.** Every field survives; it lives in one object instead of seven documents.

### 2. ~60 scored fields → ~15 enumerated states

Cut: `awareness_confidence: 0-1`, `sophistication_confidence: 0-1`, `stereotype_risk: 0-1`, `contradiction_risk: 0-1`, `product_fit: 0-1`, `inference_confidence: 0-1`, the twelve-field `language_quality` 0-10 vector, the twelve-field angle-scoring formula.
Keep: enumerated evidence states, `PASS|REVISE|BLOCK` verdicts, `LOW|MEDIUM|HIGH|BLOCK` risk, ordered source classes, evidence levels A–D, claim-freedom tiers T0–T3.
Rationale: every cut number is generated, not measured. Numbers should appear where something is counted — review counts, clip counts, spread counts, pairwise overlaps.

### 3. Angle scoring: 18 factors → qualitative rank + hard constraints

§26 lists eighteen factors and warns against a fake formula. Agreed — so do not build one. The strategist ranks qualitatively with written rationale; code enforces hard constraints (claim-freedom tier, feasibility ceiling, compliance pre-screen, diversity spread). Ranking is judgement; constraints are code.

### 4. Style Intelligence: extraction pipeline → 3 hand-authored profiles (§L)

### 5. Voice Profiles → Voice Specifications (§K)

Not deferral for convenience: no sample in the repository is production-eligible, so profiling them produces an unusable catalogue.

### 6. Cut from V1 entirely

`performance-analyst` · context/news intelligence and its brand-safety classifier · learning freshness and confidence decay · exploration/validation/scaling allocation modes · ad-multiplication logic · diagnosis engine · Golden Test Set · static image ads (`modulo-3`'s subject, absent from the §4 vision) · Style Registry as a queryable service · multi-market abstraction.

### 7. Identifiers: 12 → 8 + `CLAIM_ID` (§O)

### 8. Human gates: 4 → 3 (§R)

### 9. Script pipeline: 30 stages → 16 (§G)

### 10. Calibrate storyboard/shot-list depth — **not** cut

§41 and §90 make storyboards and shot lists non-negotiable, and they stay. But a shot list feeding a ~15-second clip generator needs different fields than a film shot list: continuity anchors and generation-unit boundaries matter enormously; grip and lens notes do not. Specify for the consumer. This is precision, not reduction.

### What must NOT be simplified

Complete word-for-word scripts (§41, §90) · storyboards and shot lists · the Evidence Ledger and claim→evidence blocking · the four evidence states · the epistemic separation · Concept/Creative/Variant/Ad separation · hook four-way separation · the separate critic · compliance review · run manifests and version pinning.

These are what make it a Creative Experimentation OS rather than an ad generator. Cutting any of them saves effort by removing the reason the system exists.

---

## Z. Architecture Decision Log

All `PROPOSED` unless the constraint is external and already binding.

| ID | Question | Recommendation | Rationale | Trade-off | Status |
|---|---|---|---|---|---|
| ADR-001 | Implementation language/runtime | **Python 3.12+** | Anthropic SDK, media tooling, `sqlite3` in stdlib, best ecosystem fit | Team may prefer TS | PROPOSED |
| ADR-002 | Orchestration host | **Claude Agent SDK (self-hosted)** | Local assets, interactive gates, filesystem is part of the architecture, direct cost control | Self-hosted ops burden | PROPOSED |
| ADR-003 | Managed Agents for V1? | **No — revisit at hosting** | Versioned configs, session budgets, scheduled deployments and multi-agent rosters fit later phases, not V1 | Migration cost later | PROPOSED |
| ADR-004 | System of record | **Git-tracked JSON/YAML; SQLite derived** | Git already solves §82/§84 correctly | Query paths need index rebuilds | PROPOSED |
| ADR-005 | Schema enforcement | **Structured outputs + `strict: true` on every artefact-producing call — EXCEPT evidence extraction (E1)** | Verified GA; converts schemas from aspiration to guarantee. E1 must run schema-free because citations and `output_config.format` cannot coexist. | Schema rigidity; one exception to reason about | **REVISED** |
| ADR-006 | Evidence provenance for documents | **Native `citations` in E1 only**, never in the same request as a schema | Documented as incompatible with structured outputs — 400 (`tool-use-concepts.md:510`) | Two calls instead of one | **REVISED** |
| ADR-007 | Hypothesis pool generation | **Batch API (50 % cost)** | 20–30 independent, non-latency-sensitive generations | Async latency | PROPOSED |
| ADR-008 | Knowledge in context | **Prompt-cache the Schwartz prefix** | ~50 KB stable across all creatives in a run | Cache invalidation discipline | PROPOSED |
| ADR-009 | **Methodology corpus treatment** | **Quarantine; `research_only`; never in script retrieval** | F2, F3, F4, F5 | Loses convenient patterns | **PROPOSED — highest priority** |
| ADR-010 | Compliance deny-list | **Hard-block synthetic-organic impersonation** | F3 vs `schwartz_persuasion_framework.md` §15 | Forgoes a tactic the corpus claims works | PROPOSED |
| ADR-011 | Numeric confidences | **Replace with enumerations** | ~60 generated scalars are false precision | Less granularity for future analysis | PROPOSED |
| ADR-012 | Style profiles | **3 hand-authored; no extraction pipeline in V1** | Cheaper than automating nine profiles | Manual growth | PROPOSED |
| ADR-013 | Voices | **Voice *Specification* in V1-Core; no Voice Profiles** | No sample is production-eligible | Defers voice matching | PROPOSED |
| ADR-014 | TikTok-sourced voices | **Never a cloning source; descriptive target only** | Consent absent; legal + ToS exposure | Loses the male reference set | **PROPOSED — hard line** |
| ADR-015 | Human gates | **3, not 4** | Merged script+production review adds no information | Slightly later script feedback | PROPOSED |
| ADR-016 | BLOCK overridable? | **Two classes.** `HARD_BLOCK` (deterministic) is not overridable by approval — only by changing the underlying state. `POLICY_REVIEW_REQUIRED` / `HIGH_RISK` (judgement) is adjudicated by a human and recorded. | An LLM interpretation must not be irreversible; a mechanical fact should not be arguable | Two states for reviewers to learn | **REVISED** |
| ADR-017 | KPI thresholds | **None stored in V1** | F5: the corpus contradicts itself | No out-of-box benchmarks | PROPOSED |
| ADR-018 | Meta policy | **Fetch at review time; never cache into design** | Policy ages faster than documents | Requires tool access at review | PROPOSED |
| ADR-019 | Higgsfield | **Capability spike before any integration build** | Lipsync and multi-speaker unverified (§0.2) | Delays V1-Production start | **PROPOSED — blocking for V1-Production** |
| ADR-020 | V1-Production order | **Animation → UGC → Podcast** | Ascending continuity burden and dependency risk | Podcast arrives last | PROPOSED |
| ADR-021 | Batch artefacts | **26 → 8 types** | Most are fields, not documents | Some reports need assembling for review | PROPOSED |
| ADR-022 | Diversity | **Split hard constraints from targets.** Format mix, duplicate prevention, tier and provenance are hard. Research-dependent spread dimensions are targets; unmet targets return `INSUFFICIENT_EVIDENCE_FOR_DIVERSITY_TARGET` to Gate 2. **Never fabricate to satisfy a quota.** | Unconditional spread constraints would have made fabrication the cheapest path to compliance | Batches may be less diverse — honestly so | **REVISED** |
| ADR-023 | Experiment design | **Not a Skill — orchestrator + deterministic validator** | Integrity must be guaranteed, not narrated | Less flexible design space | PROPOSED |
| ADR-024 | Skill count | **9 → 5** | §E | Fewer specialised contexts | PROPOSED |
| ADR-025 | Evidence levels | **A / B / C + D (contradicted); mandatory `scope`** | Learnings must be able to lose confidence | Extra analysis discipline | PROPOSED |
| ADR-026 | Meta delivery confounding | **Declare it; expect Level B** | Meta does not split traffic evenly | Weaker causal claims — honestly weaker | PROPOSED |
| ADR-027 | Runtime install | **Python + ffmpeg before the first *executing* phase (Phase 5), not before Phase 2** | §0.3 — Phases 2–4 are design and need no interpreter | Prerequisite must not be forgotten once design momentum builds | **REVISED — `IMPLEMENTATION_PREREQUISITE` (PRE-01)** |
| ADR-028 | Repository migration | **Recommended in §I; executed in Phase 3 only** | §80, §92 forbid Phase 1 reorganisation | Current layout persists meanwhile | **ACCEPTED (per instruction)** |
| ADR-029 | Static image ads | **Out of V1 scope** | `modulo-3`'s subject; absent from the §4 video vision | Loses a channel the corpus covers | PROPOSED |
| ADR-030 | `POST_ID` as a first-class identifier | **Add to the hierarchy** | Social proof attaches to the post, not the ad; §55 omits it | One more ID | PROPOSED |
| **ADR-031** | **Evidence acquisition topology** | **Three steps: E1 extract (citations, no schema) → E2 normalise (schema, no citations, reads E1 output only) → E3 deterministic ledger write with locator reconciliation** | Citations and structured outputs are mutually exclusive in one request. E2 reading only E1's output makes locator fabrication impossible rather than merely discouraged. | Two model calls per source batch; slightly higher latency and cost | **PROPOSED (new — audit)** |
| **ADR-032** | **Who may raise a `HARD_BLOCK`** | **Deterministic services only. No Skill and no model call may emit one.** `compliance-reviewer` and the Creative Critic escalate; they do not block. | A probabilistic judgement must not be irreversible; a mechanical check should not be negotiable | Some genuinely unacceptable creatives will pass to a human instead of being auto-stopped | **PROPOSED (new — audit)** |
| **ADR-033** | **Runtime access & cost model** | **Provision programmatic API access for the automated runtime, separate from the interactive Claude Code entitlement.** Non-interactive credential, org billing, per-campaign and per-batch budget ceilings, retry/backoff, pinned model IDs. | An interactive subscription does not supply the deployed system's runtime; discovering this at deployment is expensive | Requires an org API account and budget approval before Phase 5 | **PROPOSED (new — audit)** |
| **ADR-034** | **Evidence class granularity** | **Split class A into A1 (regulator / independent primary / peer-reviewed) and A2 (official manufacturer documentation). Claim type determines the minimum class; A2 never substantiates efficacy, medical outcome, comparative superiority, safety or scientific performance.** | One interchangeable class would let a brand's own PDF substantiate a clinical claim — reproducing F2 | More ledger discipline; some claims become harder to support, correctly | **PROPOSED (new — audit)** |
| **ADR-035** | **Asset state model** | **Six states.** Uploads default `USER_PROVIDED_UNVERIFIED`; generated assets default `GENERATED_DRAFT`; promotion to `PRODUCTION_ELIGIBLE` requires authorised inputs + consent + compliance + QA + resolvable lineage. | Possession and generation both establish nothing about rights | More state transitions to manage | **PROPOSED (new — audit)** |

---

## AA. External Audit Correction Pass

**Date:** 2026-09-04 · **Trigger:** external architecture audit · **Scope:** `docs/PHASE_1_SYSTEM_DESIGN.md` only · **Phase 2 not started.**

Seven corrections were raised. **All seven are accepted.** One (Correction 1) identified a factual error; three (3, 4, 5) identified design flaws where the architecture violated its own stated principles; two (2, 6) sharpened classifications that were too coarse; one (7) surfaced a deployment concern the document had not addressed. The epistemic correction is accepted and applied to F1.

### The one that mattered most

**Correction 4 — diversity quotas as unconditional hard constraints — was the most serious.** The first edition committed a solver to producing ≥ 4 distinct core problems, ≥ 3 awareness states and so on, regardless of what the research could evidence. Given a thin evidence base, the only way to satisfy that is for the upstream strategist to invent the difference. The document's central safety property — never invent evidence — would have been defeated by its own quality mechanism, and defeated invisibly, because a fabricated batch scores *better* on diversity than an honest one.

That is a general failure mode worth naming, and it is now principle §C.17: **any mechanism that can be satisfied by invention has been specified wrongly.** The same test was applied to the rest of the document; the coverage vector and claim-freedom tiers (§M) pass it, because an `UNKNOWN` field lowers the tier rather than inviting a guess.

### What each correction changed

| # | Correction | Verdict | Nature | Sections | ADRs |
|---|---|---|---|---|---|
| 1 | Citations ⊥ structured outputs | **Accepted** | **Factual error.** Documented as 400-incompatible (`tool-use-concepts.md:510`). Would have failed at first integration; the tempting fix — drop citations — silently destroys provenance. | §0.2, §D, §F, §N.1 | 005 R, 006 R, **031 new** |
| 2 | Class A too coarse | **Accepted** | Under-specification with a live precedent: F2 is exactly a manufacturer-grade source substantiating a clinical claim. A single class A would have let the architecture reproduce the error it was built to catch. | §N | **034 new** |
| 3 | Asset rights inferred | **Accepted** | Internal inconsistency. "Brand-owned by assumption" and "born PRODUCTION" both infer rights from possession, contradicting §91.8 and §C.9. | §J, §K | **035 new** |
| 4 | Diversity quotas | **Accepted** | **Design flaw — fabrication incentive.** See above. | §Q, §C, §F | 022 R |
| 5 | BLOCK semantics | **Accepted** | Category error: one non-overridable state conflated a mechanical fact with a model's interpretation. | §G, §F, §R | 016 R, **032 new** |
| 6 | Runtime blocker timing | **Accepted** | Over-broad gating. Phase 2 is design; design needs no interpreter. | §0.3, §X | 027 R |
| 7 | Dev environment vs runtime | **Accepted** | Omission. An interactive entitlement does not supply the deployed system's API access, billing or headless operation. | §D.1 | 002 note, **033 new** |
| — | F1 authorship overstated | **Accepted** | Stated an inference as fact. Corrected to `PROBABLE_LLM_DERIVED` / `CONVERSATIONAL_DERIVED_UNVERIFIABLE`; quarantine unchanged, because it rests on unverifiability, which is established. | §0.1, §I | — |

### Change log

**Revised**

- **§0.1 F1** — authorship downgraded to inference; consequence re-grounded on unresolvable citations rather than on derivation method.
- **§0.2** — added the citations/structured-outputs incompatibility with its source reference.
- **§0.3** — `BLOCK-01` → `IMPLEMENTATION_PREREQUISITE` **PRE-01**, with a per-phase gating table (design phases ungated; execution phases 5–10 gated).
- **§C** — principles **16** (only deterministic checks may be irreversible) and **17** (quality objectives never override evidence constraints) added.
- **§D** — Evidence Ledger writer split into **E1 / E2 / E3**.
- **§D.1** — **new subsection**: development environment vs automated runtime, with authentication, cost, rate-limit, model-pinning and deployment consequences.
- **§F** — flow updated for the E1/E2/E3 evidence steps, the diversity-target escape path, and the `HARD_BLOCK` steps (22–24) separated from judgement steps (25–26); downstream steps renumbered to 33.
- **§G** — stages 10 and 11 raise `HARD_BLOCK`; stage 10 additionally enforces the §N evidence-class minimum; stages 12 and 13 explicitly cannot raise one.
- **§I** — tier renamed `CONVERSATIONAL_DERIVED_UNVERIFIABLE`; `derivation_method: probable_llm_derived`; `derivation_confidence` added.
- **§J** — three asset states → **six**, with rights inheritance for generated assets and recorded operator attestation.
- **§K** — voice `eligible_state` aligned to the six-state model.
- **§N** — **§N.1 added** (two-stage acquisition + deterministic reconciliation); class **A split into A1 / A2**; claim-type → minimum-class matrix added; `locator_origin` added to the ledger.
- **§Q** — hard constraints separated from diversity targets; `INSUFFICIENT_EVIDENCE_FOR_DIVERSITY_TARGET` with four resolution options; subsections renumbered.
- **§R** — two block classes defined; gate action table revised; LLMs barred from raising `HARD_BLOCK`.
- **§X** — runtime risk HIGH → MEDIUM; four risks newly named (manufacturer-substantiated clinical claims, diversity-driven fabrication, rights inferred from upload/generation, irreversible model judgement); citations conflict marked RESOLVED; runtime access/cost risk added.
- **§Z** — ADR-005, 006, 016, 022, 027 revised.

**Added:** ADR-031 (evidence topology) · ADR-032 (who may raise `HARD_BLOCK`) · ADR-033 (runtime access & cost model) · ADR-034 (evidence class granularity) · ADR-035 (asset state model).

**Unchanged:** scope (§B) · Skills audit, 9 → 5 (§E) · Schwartz integration and precedence (§H) · quarantine decision and migration plan (§I) · cold start, coverage vector, claim-freedom tiers (§M) · concept taxonomy (§O) · experiment architecture and evidence levels A–D (§P) · three human gates (§R) · production boundary (§S) · V1-Production staging (§T) · performance interfaces (§U) · storage decision (§V) · versioning (§W) · simplifications (§Y).

**Not done:** no Phase 2 work. No schemas, Skills, migrations or implementation code. No file outside `docs/PHASE_1_SYSTEM_DESIGN.md` was created, moved, renamed or edited.

---

## Compliance with Phase 1 constraints

| Constraint | Status |
|---|---|
| Read `PRE_FLIGHT_AUDIT.md` before architecture work | ✅ |
| `PRE_FLIGHT_AUDIT.md` unmodified | ✅ Not opened for writing |
| W1 treated as RESOLVED | ✅ |
| W2–W7 considered architecturally | ✅ §I, §J, §K, §X — plus new W8 |
| No Skills created | ✅ |
| No schemas / DB tables / migrations | ✅ Conceptual field lists only; no DDL |
| No production code | ✅ |
| No repository reorganisation | ✅ Only `docs/` created |
| No files moved, renamed or edited | ✅ |
| No mass video analysis | ✅ Metadata only |
| No Style Profiles | ✅ |
| No Voice Profiles | ✅ |
| No Higgsfield integration | ✅ Capability verification only |
| Only `docs/` created | ✅ |
| Source-derived claims distinguished from architecture decisions | ✅ Sources cited by file and section throughout |
| External capabilities verified where possible; unverified labelled | ✅ §0.2 |
| Architecture challenged where warranted | ✅ §A, §E, §G, §Y, and F1–F5 |
| External audit corrections 1–7 + epistemic correction applied | ✅ §AA |
| Only `docs/PHASE_1_SYSTEM_DESIGN.md` modified in the correction pass | ✅ |

**Phase 1 ends here. Phases 2–10 are not authorised and have not been started.**
