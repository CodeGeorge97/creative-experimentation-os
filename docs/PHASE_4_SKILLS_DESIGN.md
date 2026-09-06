# Phase 4 — Skills Design

**Status:** ACTIVE
**Phase:** 4
**Branch:** `phase-4-skills-design`
**Base freeze:** `phase-3c-complete`

---

## A. Purpose

Phase 4 defines the five procedural Skills of Creative Experimentation OS.

The five Skills are:

1. `product-intelligence`
2. `market-intelligence-cl`
3. `creative-strategist`
4. `script-engine`
5. `compliance-reviewer`

Phase 4 designs procedural know-how only.

It does not implement orchestration code, deterministic validation
services, storage writers, tools, production routing, or config policy.

---

## B. Skill Boundary

A Skill is procedural reasoning loaded into model context.

A Skill:

- receives prepared inputs from the orchestrator;
- applies reusable domain reasoning;
- returns structured generative output;
- preserves uncertainty explicitly;
- declares which knowledge resources it may consume.

A Skill does not:

- allocate or emit canonical identifiers;
- write canonical state to `store/`;
- author or embed policy;
- implement deterministic validation;
- own persistence;
- own tool capability;
- directly retrieve arbitrary knowledge files;
- access `knowledge/_quarantine/`;
- implement runtime orchestration.

Tools provide capability.

The orchestrator controls sequence, retries, gates, identifiers,
retrieval, persistence, and tool invocation.

Config registries own policy, thresholds, taxonomies, and enumerations.

Knowledge resources are retrieved into Skills; they are never copied
into Skill instructions.

---

## C. Physical Form

Each Skill will live at:

`.claude/skills/<skill-name>/SKILL.md`

Phase 4 creates only the five Skill directories and their `SKILL.md`
files after this design is accepted.

No Skill-specific scripts or reference files are required for V1.

Runtime orchestration prompt templates remain reserved for:

`src/creative_os/prompts/`

That directory is Phase 5 scope and is not created in Phase 4.

---

## D. SKILL.md Frontmatter Contract

Every Skill uses YAML frontmatter with:

```yaml
---
name: <skill-name>
description: >-
  <what the Skill does and when it should activate>
metadata:
  version: "1.0.0"
  knowledge: "<comma-separated KNOWLEDGE_ID values or none>"
---

---

## L. Skill Design 1 — `product-intelligence`

**Status:** PROPOSED
**Initial version:** `1.0.0`
**Runtime knowledge declaration:** `none`

### L.1 Role

`product-intelligence` converts prepared product, brand, visual, operator,
and research evidence into an epistemically explicit Product Truth fact
proposal and Brand Snapshot.

Its central responsibility is:

> extract what is actually supportable, preserve the distinction between
> observation and truth, and refuse to fill evidence gaps by inference.

Product facts and brand facts share this Skill because they use the same
reasoning procedure, the same `Fact` semantics, and the same principal
failure mode: confident invention from sparse evidence.

The Skill does not decide what claims advertising may make.

---

### L.2 Inputs

The orchestrator may supply:

- operator-provided product and brand information;
- prepared product-image observations from vision capability;
- verbatim visible label text;
- prepared official-source product or brand research;
- prepared evidence/source classifications;
- conflicts already detected between evidence items;
- the applicable category-profile projection when available;
- an existing Product Truth version when the task is an extension or
  correction rather than a cold start.

Inputs supplied to the Skill are model-facing projections.

They must not require the Skill to allocate canonical IDs, hashes,
versions, event sequence numbers, or storage paths.

`product-intelligence` has no runtime knowledge-resource dependency.

---

### L.3 Procedure

#### Step 1 — Separate evidence origins

Treat each input according to what it actually establishes:

- operator-provided facts are explicit operator assertions;
- image observations establish only what is visually observable;
- visible label text establishes that the label states something;
- label text alone does not establish that the statement is true;
- external research establishes only what the supplied evidence and
  source classification support;
- absence of evidence does not establish absence of the property.

Never collapse observation, interpretation, and verification.

#### Step 2 — Establish product identity conservatively

Determine whether the supplied material is sufficient to describe a
coherent product identity.

An identity directly visible in supplied material may remain
`OBSERVED`.

External verification is not required merely to recognise an otherwise
unambiguous supplied product.

If identity is ambiguous, illegible, contradictory, or depends on a
guess, surface the unresolved identity instead of selecting a candidate.

The Skill does not calculate T0/T1/T2/T3.

#### Step 3 — Produce Product Truth facts

Reason over the Product Truth dimensions defined by the data
architecture:

- identity;
- category;
- visual;
- composition;
- function;
- commercial;
- proof;
- restrictions;
- category extensions supplied by the applicable category profile.

Every proposed leaf uses the system `Fact` semantics:

- `value`;
- epistemic `state`;
- evidence/basis association supplied through model-facing handles;
- `note` when required to explain uncertainty or inference.

Do not create an alternative epistemic vocabulary.

Do not create numeric confidence scores.

#### Step 4 — Apply epistemic discipline

Use the supplied evidence to distinguish:

- `VERIFIED`;
- `OBSERVED`;
- `INFERRED`;
- `UNKNOWN`;
- `NOT_COLLECTED`;
- `NOT_APPLICABLE`.

Do not promote a fact merely because it is plausible.

For `INFERRED`, state the inferential step explicitly.

For `UNKNOWN`, state what was attempted and why the value remains
unresolved.

Do not turn a missing value into an assertion of absence.

Do not use an inferred interpretation as substantiation for another
fact.

If the prepared evidence state or source classification is
insufficient to justify a stronger state, preserve the weaker state.

#### Step 5 — Build the Brand Snapshot

Apply the same evidence discipline to:

- positioning;
- category context;
- claims made publicly;
- tone of voice;
- proof assets;
- official channels;
- known disputes.

Brand familiarity, category convention, or likely positioning is not
evidence.

The Brand Snapshot remains part of Product Truth.

#### Step 6 — Preserve conflicts

When supplied evidence conflicts, do not silently reconcile it.

Return:

- the competing supported statements;
- the nature of the conflict;
- what additional evidence would resolve it.

A conflict is an input to downstream evidence handling and Gate 1.

The Skill does not determine canonical claim status.

#### Step 7 — Surface gaps

Return specific unresolved fields and missing evidence needs.

Prefer a precise statement such as:

`ingredient concentration remains UNKNOWN`

over a general statement such as:

`product information is incomplete`.

The deterministic completeness service, not this Skill, computes the
coverage vector.

---

### L.4 Output Contract

The Skill returns a semantic proposal containing:

1. **Product facts**
   - Fact-shaped values grouped by Product Truth dimension.

2. **Brand Snapshot**
   - Fact-shaped brand values using the same epistemic discipline.

3. **Evidence associations**
   - model-facing evidence handles or locators supplied in the input;
   - never newly minted canonical identifiers.

4. **Unresolved fields**
   - explicit `UNKNOWN` and `NOT_COLLECTED` gaps.

5. **Inference notes**
   - explanation for every proposed `INFERRED` value.

6. **Conflict report**
   - competing statements that must not be silently collapsed.

7. **Evidence requests**
   - concrete additional information that could resolve important gaps.

The Skill does not return:

- canonical IDs;
- hashes;
- canonical versions;
- a persisted Product Truth artefact;
- Evidence Ledger records;
- coverage calculations;
- claim-freedom tiers;
- permitted claim territories;
- Gate 1 decisions.

Those belong to orchestration or deterministic services.

---

### L.5 Handoffs

After `product-intelligence` returns:

1. the orchestrator validates the model-facing result;
2. canonical evidence references are resolved outside the Skill;
3. the Evidence Ledger service performs its deterministic writes;
4. the Product Truth Completeness service derives the coverage vector;
5. the Claim Freedom resolver derives T0/T1/T2/T3 and permitted
   territories;
6. Gate 1 reviews Truth & Evidence before market research proceeds.

If additional visual analysis or web research is required,
`product-intelligence` reports the evidence need.

The orchestrator decides whether to invoke the relevant tool and whether
to call the Skill again with the new evidence.

---

### L.6 Failure & Uncertainty

The Skill must fail conservatively rather than invent when:

- the product cannot be identified from supplied information;
- multiple products or brands plausibly match the evidence;
- visible text is illegible;
- supplied sources conflict materially;
- a requested field has no evidentiary basis;
- a category-specific field cannot be interpreted without a category
  profile;
- the distinction between label statement and verified fact cannot be
  resolved.

Valid conservative outputs include:

- `UNKNOWN`;
- `NOT_COLLECTED`;
- explicit conflict;
- request for additional evidence;
- inability to establish product identity.

A sparse Product Truth is preferable to a complete-looking invented one.

---

### L.7 Boundaries

`product-intelligence` owns:

- reasoning from prepared evidence into Product Truth facts;
- Brand Snapshot reasoning;
- epistemic classification of its proposed facts;
- conservative handling of sparse evidence;
- explicit uncertainty, conflicts, and evidence needs.

It does not own:

- image analysis capability;
- web search capability;
- source-quality policy;
- Evidence Ledger persistence;
- canonical ID allocation;
- canonical version allocation;
- filesystem writes;
- coverage computation;
- claim-freedom computation;
- hard compliance rules;
- Gate 1 approval;
- Chile market research;
- audience modelling;
- hypothesis generation;
- creative strategy;
- script writing.

Those responsibilities remain with tools, deterministic services,
orchestration, config, human gates, or downstream Skills.

---

### L.8 Design Acceptance Criteria

The eventual `SKILL.md` is conformant only if:

1. it can operate from the minimum Product Image + Brand cold start
   without inventing missing product facts;
2. it distinguishes visible label statements from verified truth;
3. every uncertain field preserves an explicit epistemic state;
4. it treats Brand Snapshot and product facts with one evidence
   discipline;
5. it emits no canonical identifier;
6. it writes no persistent state;
7. it computes neither coverage nor claim freedom;
8. it contains no policy thresholds or category-profile content;
9. it requires no runtime knowledge resource;
10. it exposes ambiguity and conflicts rather than resolving them by
    plausibility.

---

## M. Skill Design 2 — `market-intelligence-cl`

**Status:** PROPOSED
**Initial version:** `1.0.0`
**Runtime knowledge declaration:** `KNW-schwartz-persuasion`

### M.1 Role

`market-intelligence-cl` converts prepared Chile-market research into an
evidence-grounded view of the competitive environment, customer
language, market context, and strategic market signals needed by later
reasoning.

Its central responsibility is:

> observe how the market actually talks, buys, compares, objects, and
> positions alternatives in Chile without substituting stereotype,
> category folklore, or framework assumptions for evidence.

The Skill may use the Schwartz Persuasion Framework to decide what
questions are strategically useful to ask of the evidence.

The framework may guide observation.

It may not manufacture market facts.

---

### M.2 Inputs

The orchestrator may supply:

- approved Product Truth;
- Brand Snapshot;
- claim-freedom projection;
- prepared Chile-market web research;
- prepared competitor material;
- prepared marketplace, review, forum, social, and publication content;
- prepared source metadata;
- deterministically derived source-quality classifications;
- evidence handles and locators;
- prior customer-language observations when explicitly supplied;
- campaign market fixed as Chile;
- retrieved `KNW-schwartz-persuasion` content carrying valid provenance.

Inputs are model-facing projections.

The Skill does not perform web-search capability itself.

The Skill does not classify source authority itself.

The Skill does not retrieve arbitrary knowledge.

---

### M.3 Procedure

#### Step 1 — Preserve the Product Truth boundary

Treat approved Product Truth as the factual product boundary.

Market research may reveal:

- customer perceptions;
- competitor claims;
- category expectations;
- price context;
- alternative solutions;
- purchase language;
- objections.

It does not rewrite Product Truth.

A competitor claim or customer statement about the product is not
automatically a product fact.

If market evidence appears to contradict Product Truth, report the
conflict for upstream review instead of silently changing the product
facts.

#### Step 2 — Read sources for their research purpose

Reason from the source material according to the purpose for which it
was supplied.

Use the deterministically supplied source metadata and classifications.

Do not invent or override a `quality_class`.

Do not create a universal ranking in which one source class is always
superior to another.

Distinguish at minimum between evidence useful for:

- factual market context;
- competitor behaviour;
- customer language;
- customer objections;
- customer alternatives;
- market-positioning signals.

When evidence is thin or one-source dependent, preserve that limitation.

#### Step 3 — Build the Chile market snapshot proposal

Produce evidence-linked observations for the Research Dossier market
snapshot where the supplied research supports them.

Relevant dimensions include:

- market;
- category-size signal;
- growth signal;
- seasonality;
- price range;
- distribution channels;
- regulatory context;
- cultural context.

The market is `CL`.

Do not invent a numeric market estimate when only qualitative evidence
exists.

Do not manufacture precision from incomplete sources.

Fields without sufficient basis remain explicitly unresolved.

#### Step 4 — Map the competitive field

Identify observable competitor patterns without treating advertising
claims as truth.

Capture, when supported:

- competitors encountered;
- positioning used;
- claim territories observed;
- recurring offers;
- recurring problem framings;
- recurring mechanisms or explanations claimed by competitors;
- saturation or repetition signals;
- visible differentiation patterns.

Competitor advertising describes what competitors communicate.

It does not substantiate their product claims.

Do not copy a competitor's recognisable creative execution or signature.

#### Step 5 — Extract real customer language

Identify useful customer-language material from the supplied evidence.

Preserve verbatim language exactly when the source provides it.

Do not:

- rewrite a quote to sound more Chilean;
- add slang that is absent from the source;
- turn a paraphrase into a quotation;
- merge several people into a fabricated quotation;
- present model-generated wording as customer language.

For each useful language observation, preserve available context such
as:

- evidence handle;
- platform or source context;
- purchase-stage context when supported;
- audience hint when directly supported;
- relevant problem, desire, objection, belief, or alternative.

If the audience identity is not observable, leave it unresolved.

The Skill proposes customer-language observations.

The orchestrator and evidence services create canonical OBSERVATION
records outside the Skill.

#### Step 6 — Separate observation from interpretation

Maintain the epistemic spine:

`SOURCE -> OBSERVATION -> INSIGHT`

This Skill works primarily on the SOURCE -> OBSERVATION side.

It may organise research signals and identify recurring evidence
patterns, but it must not convert those patterns into a fully formed
creative hypothesis.

Statements such as:

- people repeatedly use phrase X;
- buyers compare product category A with alternative B;
- several sources ask for explanation of mechanism C;

are research observations or pattern summaries.

Statements such as:

- therefore the winning angle is X;
- therefore this belief bridge should be used;
- therefore this format will outperform;

belong downstream.

#### Step 7 — Surface evidence for strategic audience dimensions

Use market evidence to surface support relevant to later reasoning
about:

- dominant desires;
- problems;
- objections;
- alternatives;
- current beliefs;
- awareness;
- sophistication;
- identity or identification cues.

Awareness and sophistication must be evidence-led.

Do not infer sophistication merely from the age or apparent maturity of
the category.

Do not infer Chilean identity, gender roles, socioeconomic assumptions,
or cultural behaviour from stereotype.

Return the observations and basis that downstream reasoning can use.

Do not construct the final Audience Model or Persuasion Context.

#### Step 8 — Use Schwartz as an advisory research lens

`KNW-schwartz-persuasion` may influence:

- which market questions deserve investigation;
- whether the evidence indicates different awareness conditions;
- whether repeated competitive mechanisms suggest saturation;
- which desires, beliefs, alternatives, or objections deserve closer
  inspection.

Schwartz never outranks:

- Product Truth;
- supplied evidence;
- current Chile market research;
- real customer language.

If the framework suggests a pattern that the research does not support,
report the evidence gap instead of completing the pattern.

#### Step 9 — Detect research gaps and contradictions

Surface:

- conflicting market observations;
- thin evidence;
- unsupported generalisations;
- missing Chile-specific evidence;
- sources that appear duplicated or dependent when that information is
  supplied;
- important audience questions not answered by current research;
- strategic dimensions with no observable basis.

Do not resolve disagreement through plausibility alone.

Request additional research when the current evidence cannot support a
useful market observation.

---

### M.4 Output Contract

The Skill returns a semantic research proposal containing:

1. **Market Snapshot proposal**
   - evidence-linked, Fact-shaped market context.

2. **Competitive field proposal**
   - observed positioning;
   - observed claim territories;
   - recurring market patterns;
   - evidence associations.

3. **Customer-language candidates**
   - verbatim text;
   - supplied evidence handle;
   - source/platform context;
   - supported contextual annotations.

4. **Strategic evidence signals**
   - evidence relevant to desire;
   - problem;
   - objections;
   - alternatives;
   - beliefs;
   - awareness;
   - sophistication;
   - identification.

5. **Research conflicts**
   - competing observations that should remain visible.

6. **Research gaps**
   - specific missing evidence or unanswered questions.

7. **Additional research requests**
   - concrete information that would materially improve the dossier.

The Skill does not return:

- canonical SOURCE IDs;
- canonical OBSERVATION IDs;
- canonical INSIGHT IDs;
- hashes;
- persistence records;
- source-quality classifications;
- Audience Model;
- Persuasion Context;
- hypotheses;
- concepts;
- creative angles;
- scripts;
- compliance decisions.

---

### M.5 Handoffs

After `market-intelligence-cl` returns:

1. the orchestrator validates the model-facing result;
2. evidence services create or reference canonical SOURCE,
   EVIDENCE_EXTRACTION, and OBSERVATION records;
3. customer-language observations remain external evidence records
   referenced by the Research Dossier;
4. competitor observations remain external evidence records referenced
   by the Research Dossier;
5. the Research Dossier receives the market and competitive research
   projection;
6. `creative-strategist` consumes the approved research evidence to
   construct the Audience Model, Persuasion Context, insights,
   hypotheses, and concepts.

If the research base is insufficient, the Skill requests additional
research.

The orchestrator decides whether and how to invoke web or other
research capabilities.

---

### M.6 Failure & Uncertainty

The Skill must remain conservative when:

- Chile-specific evidence is missing;
- supplied evidence comes from another market and cannot safely be
  transferred;
- customer language is paraphrased rather than verbatim;
- audience identity is not observable;
- awareness or sophistication lacks a defensible evidentiary basis;
- competitor advertising is the only basis for a factual claim;
- sources materially disagree;
- the available sample is too narrow to support a market-wide
  generalisation;
- a framework pattern appears plausible but is not observed.

Valid outputs include:

- unresolved market field;
- explicit evidence limitation;
- conflicting observations;
- narrow/local observation rather than broad generalisation;
- request for additional Chile research.

A thin but attributable research picture is preferable to a complete
stereotype.

---

### M.7 Boundaries

`market-intelligence-cl` owns:

- Chile-market interpretation from prepared evidence;
- customer-language extraction;
- competitive-field observation;
- market-context reasoning;
- evidence signals for awareness and sophistication;
- evidence signals for problems, desires, beliefs, objections, and
  alternatives;
- identification of research gaps and contradictions.

It does not own:

- web-search capability;
- source ingestion;
- source-quality classification;
- evidence-policy rules;
- canonical evidence persistence;
- canonical ID allocation;
- Product Truth modification;
- Audience Model construction;
- Persuasion Context construction;
- insight identifiers;
- hypothesis generation;
- concept selection;
- diversity enforcement;
- experiment design;
- script localisation;
- compliance enforcement.

Those responsibilities belong to tools, deterministic services,
orchestration, config, `creative-strategist`, `script-engine`, or human
gates.

---

### M.8 Design Acceptance Criteria

The eventual `SKILL.md` is conformant only if:

1. it treats Chile as a market to be observed rather than stereotyped;
2. it preserves customer language as real verbatim evidence;
3. it never turns competitor claims into product truth;
4. it uses supplied source classification without assigning its own;
5. it does not invent a universal source-quality ranking;
6. it surfaces evidence for awareness and sophistication rather than
   assuming them;
7. it uses Schwartz only as an advisory research lens;
8. it creates neither Audience Model nor Persuasion Context;
9. it creates no canonical evidence identifiers;
10. it owns no web-search or persistence capability;
11. it exposes thin evidence, conflicts, and research gaps explicitly;
12. it produces research inputs suitable for downstream
    `creative-strategist` reasoning.

---

## N. Skill Design 3 — `creative-strategist`

**Status:** PROPOSED
**Initial version:** `1.0.0`
**Runtime knowledge declaration:** `KNW-schwartz-persuasion`

### N.1 Role

`creative-strategist` converts approved Product Truth and market evidence
into an evidence-linked Audience Model, a strategic persuasion
projection, falsifiable creative hypotheses, qualitative strategic
judgement, and format-agnostic concepts.

It is the core reasoning Skill of the system.

Its central responsibility is:

> turn evidence into testable strategic arguments without collapsing
> observation, insight, hypothesis, concept, experiment, or creative
> execution into one another.

The Skill decides what is strategically worth saying and testing.

It does not decide what the system is mechanically allowed to persist,
select, validate, block, or execute.

---

### N.2 Inputs

The orchestrator may supply:

- approved Product Truth;
- Brand Snapshot;
- deterministic claim-freedom projection;
- permitted claim territories;
- Research Dossier market material;
- customer-language observations;
- competitor observations;
- approved or candidate research insights;
- evidence handles and canonical references in model-facing form;
- campaign objectives and constraints;
- requested hypothesis-pool size;
- requested format mix;
- available format-profile projections;
- narrative-pattern registry projection;
- creative-taxonomy projection;
- diversity-target projection when relevant to qualitative generation;
- prior experiment learnings when explicitly supplied and in scope;
- retrieved `KNW-schwartz-persuasion` with valid provenance.

The Skill does not retrieve arbitrary files.

The Skill does not read `KNW-schwartz-integration` at runtime.

The Skill does not use quarantined methodology knowledge.

---

### N.3 Procedure

#### Step 1 — Preserve upstream truth

Begin from approved Product Truth, evidence, and current market research.

Do not:

- create new product facts;
- strengthen an existing claim;
- turn competitor rhetoric into truth;
- replace real customer language with invented register;
- override unresolved evidence with strategic convenience.

Strategy begins inside the factual and claim-freedom boundary supplied by
upstream services.

If the desired argument requires unavailable evidence, expose that
dependency rather than quietly weakening or fabricating the premise.

#### Step 2 — Build one Audience Model

Construct a single V1 Audience Model from the supplied evidence.

Reason over:

- surface problem;
- deep problem;
- functional desire;
- emotional desire;
- identity desire;
- fear;
- frustration;
- objections;
- current belief;
- desired belief;
- alternatives;
- awareness state;
- sophistication state;
- purchase context;
- usage context;
- permitted broad life-stage signal when actually observed.

Every audience field remains Fact-shaped in semantic meaning:

- evidence-linked when supported;
- explicitly uncertain when unresolved;
- inferential only when a defensible evidence basis is supplied.

Do not create several personas or segments in V1.

Do not infer sensitive audience attributes.

#### Step 3 — Treat awareness and sophistication as evidence-linked readings

Awareness and sophistication are strategic interpretations of current
market evidence, not assumptions derived from category age.

If either is `INFERRED`, the reasoning must identify:

- the supporting observations;
- the inferential move;
- why the evidence supports that reading.

If that basis is absent, leave the field unresolved.

Do not choose the awareness state that would make a desired hook easier
to write.

#### Step 4 — Create the Persuasion Projection

Build the strategic projection from the Audience Model.

Evidence fields remain in the Audience Model exactly once.

The projection points to those fields rather than restating them.

Reason about strategic choices such as:

- identification strategy;
- mechanism depth;
- promise strategy;
- reason-to-believe strategy;
- intensification devices.

Provide a concise rationale for the strategic choices.

Do not duplicate:

- mass desire;
- awareness;
- sophistication;
- current belief;
- desired belief.

Those remain pointers to the evidence-bearing Audience Model.

#### Step 5 — Use Schwartz as advisory strategic reasoning

`KNW-schwartz-persuasion` may help reason about:

- belief bridges;
- identification;
- awareness fit;
- sophistication response;
- mechanism depth;
- alternative comparison;
- promise framing;
- reason-to-believe strategy;
- intensification choices.

It is advisory.

It may never override:

- Product Truth;
- Evidence Ledger state;
- claim freedom;
- current market research;
- real customer language;
- current compliance constraints;
- explicit brand constraints;
- controlled experiment evidence.

If framework advice conflicts with stronger evidence, follow the
stronger evidence and record the strategic consequence.

#### Step 6 — Derive explicit Insights without collapsing levels

Where the supplied observations justify interpretation, formulate
Insights that state the interpretation separately from its basis.

An Insight must remain traceable to observations.

Do not turn a raw customer quote directly into a creative concept.

Do not present an interpretation as though the source stated it.

Do not create an Insight merely to justify an idea already preferred.

#### Step 7 — Generate falsifiable hypotheses

Generate the requested hypothesis candidates from the Audience Model,
Persuasion Projection, Insights, and Observations.

Each hypothesis must express:

- audience or context;
- predicted creative effect;
- reason the effect is expected;
- falsification condition;
- evidence basis;
- dimensions;
- claim dependencies;
- required claim territories;
- candidate formats.

The hypothesis dimensions are:

- awareness state;
- core problem;
- dominant desire;
- current belief;
- angle mechanism;
- psychological hypothesis.

`core_problem` and `dominant_desire` remain research-derived free text.

Registry-backed dimensions use only values supplied through the
creative-taxonomy projection.

Every hypothesis requires at least one supporting Insight or
Observation.

No falsification condition means no valid hypothesis.

#### Step 8 — Keep hypotheses genuinely distinct

Generate candidates that represent different strategic explanations,
not cosmetic rewrites of the same idea.

Useful variation may come from differences in:

- awareness state;
- problem framing;
- desire;
- current belief;
- angle mechanism;
- psychological hypothesis;
- belief bridge;
- strategic reason-to-believe.

When two differently worded `core_problem` values are strategically the
same problem, explicitly mark that semantic grouping in the
model-facing result when the schema projection permits it.

Do not fabricate differences merely to satisfy a diversity target.

The deterministic diversity solver later measures actual spread.

#### Step 9 — Declare claim dependencies before concept writing

For every hypothesis, identify the claims and claim territories its
argument would require.

A hypothesis may depend on evidence that is not yet usable.

The Skill does not decide whether those dependencies pass the
deterministic compliance pre-screen.

Instead, make the dependency visible early enough for the pre-screen to
reject or defer the hypothesis before expensive creative work begins.

#### Step 10 — Qualitatively evaluate hypotheses

When the orchestrator asks for strategic evaluation, judge candidates
on reasons such as:

- strength of evidence basis;
- clarity of predicted effect;
- quality of the falsification condition;
- relevance to the Audience Model;
- usefulness of the belief bridge;
- differentiation of the argument;
- fit with available formats;
- fit with permitted claim territory;
- explanatory usefulness if tested.

Return written rationale.

Do not create fake numeric confidence or quality scores.

Do not perform the deterministic diversity selection.

Do not mark a hypothesis as finally selected unless the orchestrator
supplies the deterministic selection result or explicitly requests the
corresponding model-facing transition.

#### Step 11 — Develop selected hypotheses into Concepts

For hypotheses supplied as selected candidates, develop a
format-agnostic Concept.

Each Concept should define:

- the inherited hypothesis dimensions;
- core message;
- promise;
- reason to believe;
- product role;
- belief bridge;
- format fit;
- narrative-pattern fit;
- evidence basis;
- required claim territories;
- strategic selection rationale when requested.

A Concept is the argument that tests the Hypothesis.

It is not a finished ad.

The Concept must preserve the source hypothesis dimensions unchanged.

If the required argument needs different dimensions, it is a different
hypothesis rather than a modified concept.

#### Step 12 — Construct the belief bridge explicitly

For each Concept, articulate:

- `from` — the audience's current belief;
- `to` — the desired belief;
- `via` — the persuasive move intended to bridge them.

The bridge must be compatible with the Audience Model.

Do not create a new starting belief simply because it produces a more
dramatic concept.

A change in the starting belief implies a different strategic argument
and therefore a different Concept/Hypothesis path.

#### Step 13 — Evaluate format and narrative fit without committing execution

Assess candidate formats using qualitative fit such as:

- `STRONG`;
- `WORKABLE`;
- `POOR`.

Likewise assess available narrative patterns supplied by the registry.

Explain why the argument fits or conflicts with each useful option.

The Concept remains format-agnostic.

Do not:

- assign final format;
- assign final style;
- create a voice specification;
- write final hook copy;
- write a script;
- storyboard;
- create shot lists.

Those are downstream Creative/Script responsibilities.

#### Step 14 — Surface strategy gaps

Explicitly report when:

- the Audience Model is too weakly supported;
- no defensible belief bridge exists;
- the claim freedom supplied is too narrow for a proposed argument;
- a hypothesis lacks a falsifier;
- evidence does not support the desired awareness or sophistication
  reading;
- all candidates collapse onto substantially the same reasoning;
- no available format is workable;
- a concept requires evidence not currently usable.

Do not solve these gaps by invention.

---

### N.4 Output Contract

Depending on the orchestrator invocation, the Skill may return semantic
proposals for one or more of these layers:

1. **Audience Model**
   - one evidence-linked V1 audience object.

2. **Persuasion Projection**
   - strategic choices pointing to Audience Model evidence fields.

3. **Insights**
   - interpretations with explicit observation basis.

4. **Hypothesis candidates**
   - falsifiable statements;
   - dimensions;
   - predicted effect;
   - falsification condition;
   - evidence basis;
   - claim dependencies;
   - required territories;
   - candidate formats.

5. **Qualitative hypothesis evaluation**
   - written strategic rationale;
   - no fabricated numerical scores.

6. **Concept proposals**
   - core message;
   - promise;
   - reason to believe;
   - product role;
   - belief bridge;
   - format fit;
   - narrative fit;
   - evidence requirements;
   - selection rationale when requested.

7. **Strategy gaps**
   - evidence gaps;
   - unresolved audience fields;
   - unsupported dependencies;
   - collapsed strategic variation.

The Skill does not return:

- newly allocated canonical IDs;
- hashes or versions;
- deterministic spread counts;
- diversity pass/fail;
- final experiment selection;
- experiment IDs;
- experiment arms;
- locked-variable validation;
- final format assignment;
- final narrative assignment;
- style assignment;
- complete hook execution;
- scripts;
- storyboards;
- compliance hard blocks;
- persisted artefacts.

---

### N.5 Handoffs

The orchestrator may invoke `creative-strategist` in several bounded
reasoning passes using the same Skill procedure.

A typical sequence is:

1. build Audience Model + Persuasion Projection;
2. derive Insights where justified;
3. invoke hypothesis generation across the requested pool;
4. run deterministic compliance pre-screen;
5. request qualitative strategist evaluation for surviving hypotheses;
6. run deterministic diversity and selection services;
7. supply selected hypotheses back for Concept development;
8. assemble the Experiment Plan outside the Skill;
9. send the approved Concepts through Gate 2;
10. hand approved Concepts to `script-engine`.

The Batch API or equivalent batching mechanism belongs to orchestration,
not to the Skill.

The diversity solver owns constrained selection and spread auditing.

The Experiment Designer owns declared-variable and locked-variable
design plus deterministic validation.

---

### N.6 Failure & Uncertainty

The Skill must refuse strategic invention when:

- the evidence does not support an Audience Model field;
- awareness or sophistication would depend only on stereotype or
  category age;
- an Insight has no observation basis;
- a Hypothesis has no evidence basis;
- a Hypothesis has no falsification condition;
- a Concept requires product claims outside the supplied evidence
  boundary;
- the current belief is not supported;
- the desired belief would require an unsupported claim;
- a Reason to Believe does not exist;
- candidate arguments are cosmetic variants of one another;
- the available research cannot distinguish competing strategic
  explanations.

Valid conservative results include:

- `UNKNOWN` audience fields;
- evidence-gap report;
- deferred hypothesis;
- unsupported dependency;
- request for widened research;
- fewer valid strategic candidates than requested.

Strategic quantity never justifies fabricating evidence.

---

### N.7 Boundaries

`creative-strategist` owns:

- Audience Model reasoning;
- Persuasion Projection reasoning;
- evidence-grounded Insights;
- hypothesis generation;
- falsification reasoning;
- psychological and angle reasoning;
- belief bridges;
- qualitative hypothesis evaluation;
- Concept development;
- format-fit reasoning;
- narrative-fit reasoning;
- explicit strategy gaps.

It does not own:

- Product Truth;
- Chile research acquisition;
- web search capability;
- evidence persistence;
- source-quality classification;
- canonical ID allocation;
- config taxonomy authoring;
- compliance hard blocking;
- deterministic claim verification;
- deterministic diversity solving;
- deterministic final selection;
- experiment lock validation;
- final format assignment;
- final style assignment;
- final narrative assignment;
- script generation;
- localisation;
- production routing;
- human Gate 2 approval.

Those belong to upstream Skills, tools, deterministic services,
orchestration, config, downstream Skills, or human gates.

---

### N.8 Design Acceptance Criteria

The eventual `SKILL.md` is conformant only if:

1. it keeps Audience Model evidence separate from persuasion choices;
2. it builds one V1 Audience Model rather than fabricated personas;
3. awareness and sophistication are evidence-linked or unresolved;
4. Schwartz remains advisory and subordinate to stronger evidence;
5. every Insight preserves an observation basis;
6. every Hypothesis has both evidence basis and falsification condition;
7. hypothesis dimensions follow the canonical six-dimension vector;
8. it uses supplied taxonomy values without embedding the taxonomy;
9. it exposes claim dependencies before expensive creative writing;
10. it performs qualitative judgement without numeric confidence
    theatre;
11. it does not replace the deterministic diversity solver;
12. Concept dimensions remain identical to the source Hypothesis;
13. Concepts remain format-agnostic and contain fit rather than final
    execution assignments;
14. it does not design experiment locks or allocate experiment IDs;
15. it writes no script, storyboard, or production instruction;
16. it emits no canonical identifier and writes no persistent state.

---

## O. Skill Design 4 — `script-engine`

**Status:** PROPOSED
**Initial version:** `1.0.0`
**Runtime knowledge declaration:** `KNW-schwartz-persuasion,KNW-schwartz-language`

### O.1 Role

`script-engine` converts an approved, format-agnostic Concept into the
complete generative portion of a Creative Record:

- execution choices;
- hook strategy;
- persuasion beats;
- complete word-for-word script;
- Brilliance language refinement;
- Chile localisation and spoken naturalness;
- hook copy, visual, and audio execution;
- storyboard / shot list;
- continuity-aware visual plan.

Its central responsibility is:

> execute an approved strategic argument completely and concretely
> without changing what that argument means, strengthening its claims,
> or leaving production-facing placeholders.

The Skill writes creative execution.

It does not re-decide the hypothesis, audience, evidence boundary,
experiment, compliance policy, or production tool routing.

---

### O.2 Inputs

The orchestrator may supply:

- Gate-2-approved Concept;
- source Hypothesis dimensions;
- approved Audience Model reference/projection;
- approved Persuasion Projection;
- Product Truth projection;
- pinned claim-freedom tier;
- pinned permitted claim territories;
- verified claim candidates and required qualifications in model-facing
  form;
- campaign offer when applicable;
- brand constraints;
- negative creative constraints;
- campaign format mix;
- assigned or available format-profile projections;
- narrative-pattern registry projection;
- available Style Profile projections;
- available authorised asset projections;
- target duration;
- tool-capability projection needed for visual-plan constraints;
- customer-language observations relevant to Chile localisation;
- a voice-specification input or available voice constraints;
- retrieved `KNW-schwartz-persuasion`;
- retrieved `KNW-schwartz-language` when the Brilliance language pass is
  invoked.

The Skill receives prepared inputs.

It does not:

- retrieve arbitrary files;
- search the web itself;
- inspect `_quarantine`;
- resolve canonical IDs;
- determine asset rights;
- determine whether a claim is VERIFIED;
- calculate claim freedom.

---

### O.3 Procedure

#### Step 1 — Lock the approved strategic argument conceptually

Begin from the approved Concept.

Preserve:

- hypothesis dimensions;
- core message;
- promise;
- product role;
- reason to believe;
- belief bridge;
- evidence requirements;
- permitted claim territory.

Do not reinterpret the Concept into a new angle.

Do not change the starting audience belief.

Do not introduce a new promise.

Do not invent a stronger Reason to Believe.

If effective execution would require changing those elements, report a
revision need upstream rather than silently altering strategy.

The source Hypothesis dimensions remain inherited unchanged.

#### Step 2 — Establish Hook Strategy before execution format

Define the strategic hook entry before finalising execution details.

Reason about:

- entry awareness;
- entry device;
- belief entry point;
- why that entry device fits the approved strategic argument.

Hook Strategy is not yet exact copy.

It answers:

> where in the audience's current state should this creative begin?

Do not let a preferred visual style determine the awareness strategy.

A different belief entry point that changes the strategic argument
belongs upstream as a different Concept/Hypothesis path.

#### Step 3 — Choose execution fit from supplied options

When the orchestrator has not already fixed an execution assignment,
reason among the supplied valid options for:

- format;
- narrative pattern;
- style;
- target duration;
- pacing intent;
- language register;
- voice specification.

Use only supplied registry/profile choices.

Do not embed format, narrative, style, or voice taxonomies inside the
Skill.

Respect a user-fixed format mix or explicit execution assignment.

Style selection must support the argument rather than replace it.

Do not copy a reference creative's recognisable content, dialogue,
claims, brand elements, or proprietary signature.

#### Step 4 — Preserve the pinned evidence boundary

Treat supplied:

- claim-freedom tier;
- permitted territories;
- verified claim candidates;
- qualifications;
- brand constraints;
- negative constraints;

as execution boundaries.

The Skill may decide how to express an allowed idea.

It may not decide that a forbidden or unsupported territory should
become allowed.

Do not manufacture evidence because the Concept would sound stronger
with it.

If no usable Reason to Believe exists, preserve that absence or request
an upstream strategic revision.

#### Step 5 — Build the persuasion beat plan

Use the approved Concept and `KNW-schwartz-persuasion` to sequence the
argument into explicit persuasion beats.

Possible beat functions supplied by the script schema include:

- hook;
- problem;
- agitation;
- mechanism;
- proof;
- objection;
- benefit;
- CTA.

Each beat must have a clear communication purpose.

Schwartz may guide:

- argument sequence;
- proof placement;
- momentum;
- mechanism explanation;
- objection handling.

It remains subordinate to Product Truth, evidence, approved strategy,
current market research, real customer language, brand constraints,
and compliance boundaries.

Do not add a beat merely because a framework recommends one when the
evidence cannot support it.

#### Step 6 — Write the complete neutral-strategic script

Produce the full script word for word.

Before Chile localisation, write the strategic draft in clear,
natural, neutral Spanish.

Every spoken line must be actual copy.

Every on-screen-text line must be actual copy.

No placeholders.

Do not emit lines such as:

- `[creator explains benefit]`;
- `<insert proof>`;
- `TBD`;
- `XXX`;
- `...`;
- `show product here`.

Represent non-verbal actions through the appropriate segment or later
visual-plan field rather than hiding unwritten copy behind a
placeholder.

Preserve speaker attribution and dialogue order where required by the
selected format.

#### Step 7 — Keep the script structurally addressable

Construct the script as one readable whole with:

- speakers;
- persuasion beats;
- ordered segments;
- speaker assignment;
- format-appropriate segment kinds;
- on-screen text;
- performance direction;
- CTA wording.

Use the supplied format profile to respect format-specific structure.

Examples:

- Podcast may require multiple speakers and turn order;
- Animation may use narration and visual beats rather than dialogue;
- UGC may use presenter-led speech and product interaction.

The Skill reasons inside the supplied format profile.

It does not author or modify that profile.

#### Step 8 — Run the Brilliance language pass

Use `KNW-schwartz-language` only for the dedicated language-refinement
pass.

Improve the script for:

- first-pass comprehension;
- concreteness;
- relationship clarity;
- transitions;
- rhythm;
- spoken flow;
- caption readability;
- script-to-visual translatability;
- ambiguity detection.

The pass may improve expression.

It may not alter:

- product facts;
- claim scope;
- claim dependencies;
- qualifications;
- core promise;
- belief bridge;
- approved strategic meaning.

Produce an ambiguity report or equivalent semantic findings for
downstream review when language could imply more than the script states
directly.

`KNW-schwartz-language` is a language tool for this pass, not authority
to introduce new persuasion claims.

#### Step 9 — Localise to natural Chilean Spanish

After the strategic language pass, perform one distinct localisation +
spoken-naturalness pass.

Target:

- natural Chilean conversational Spanish;
- believable spoken rhythm;
- register appropriate to the assigned creative;
- vocabulary consistent with supplied real customer language where
  relevant;
- speakability rather than written-form elegance.

Naturalness is more important than forcing slang.

Do not:

- add Chilean slang merely to signal locality;
- stereotype Chilean speakers;
- invent customer expressions;
- exaggerate a claim during localisation;
- translate or paraphrase a required qualification when the supplied
  constraint requires exact wording.

Localisation changes expression, not meaning.

The deterministic localisation-invariance service later proves whether
the claim set and required qualifications stayed invariant.

#### Step 10 — Execute the Hook

After strategic hook choice and execution context are established,
produce the four hook components:

1. strategy;
2. copy;
3. visual;
4. audio.

The exact hook copy must also appear as the corresponding script
segment.

Hook execution may specify:

- exact spoken/written words;
- on-screen text;
- first visual beat;
- framing;
- subject;
- product presence;
- delivery;
- sound effects;
- music character;
- first-words timing intent.

Do not create an independent Hook object or identifier.

Hook parts remain addressable sections of the Creative.

#### Step 11 — Translate the script into a visual plan

Create a storyboard / shot list designed for downstream AI-video
generation and QA.

For each scene, specify only useful production-facing information such
as:

- order and timing;
- subject;
- concrete action;
- framing;
- camera movement;
- linked dialogue segments;
- product presence;
- on-screen text;
- performance direction;
- lighting intent;
- transition;
- audio intent;
- continuity references.

Do not add film-production metadata that downstream generation does not
need merely to make the plan appear professional.

The visual plan must express what happens clearly enough that a
generation system can act on it.

#### Step 12 — Plan continuity across generation units

When the supplied tool-capability projection requires segmentation,
organise scenes into generation units and identify continuity needs.

Reason about continuity for elements such as:

- character;
- wardrobe;
- product;
- location;
- lighting;
- voice;
- style.

Describe stable continuity anchors and what must carry across seams.

Use the supplied generation-duration capability.

Do not hardcode a vendor duration ceiling into the Skill.

Do not determine whether the plan passes the deterministic ceiling
validator.

If the requested execution cannot fit the supplied capability, expose
the feasibility problem for the orchestrator/service.

#### Step 13 — Preserve qualification placement

Where the supplied evidence projection requires exact qualifications,
place the required wording in appropriate script segments.

Do not:

- omit it for pacing;
- weaken it;
- hide it in an unrelated scene;
- silently rewrite it.

The deterministic evidence service later verifies qualification
presence on the final localised text.

#### Step 14 — Surface claim and language uncertainty before handoff

Before returning, identify:

- language that may contain an implied claim;
- ambiguous comparative wording;
- wording that might intensify a claim;
- unclear antecedents or relationships;
- a line that cannot be made natural without changing meaning;
- execution elements that require unavailable evidence;
- visual claims that may communicate more than the spoken copy;
- unresolved production feasibility needs.

Do not self-authorise questionable wording.

Expose it for deterministic validation, critic review, or
`compliance-reviewer`.

---

### O.4 Output Contract

The Skill returns the generative Creative proposal needed for these
Creative Record sections:

1. **Strategy projection**
   - inherited approved dimensions;
   - core message;
   - promise;
   - product role;
   - reason to believe;
   - belief bridge;
   - supplied pinned claim-freedom context.

2. **Execution**
   - format;
   - narrative pattern;
   - style;
   - voice specification;
   - target duration;
   - pacing intent;
   - language;
   - register.

3. **Hook**
   - strategy;
   - exact copy;
   - visual;
   - audio.

4. **Script**
   - speakers;
   - persuasion beats;
   - complete ordered segments;
   - exact spoken copy;
   - exact on-screen copy;
   - CTA;
   - performance direction.

5. **Language-pass findings**
   - ambiguity;
   - comprehension issues;
   - naturalness issues;
   - visual-translatability issues.

6. **Chile localisation**
   - final `es-CL` wording;
   - spoken-naturalness result/proposal;
   - no deliberate change to claim meaning.

7. **Visual plan**
   - scenes;
   - scene-to-script relationships;
   - generation-unit proposal;
   - continuity anchors;
   - production-facing directions.

8. **Execution gaps**
   - evidence dependency;
   - feasibility concern;
   - ambiguity;
   - required upstream revision.

The Skill does not return or decide:

- a new Hypothesis;
- a new Concept;
- canonical Creative ID;
- canonical version;
- hashes;
- persisted Creative Record;
- claim verification result;
- deterministic claim bindings;
- localisation-invariance result;
- hard compliance result;
- critic verdict;
- feasibility pass/fail;
- experiment lock result;
- Creative state;
- Production Package;
- production-tool routing.

---

### O.5 Handoffs

After `script-engine` returns:

1. the orchestrator validates the model-facing Creative proposal;
2. deterministic format/schema validation checks structural
   conformance;
3. claim-to-evidence binding runs on the final localised text;
4. required qualifications are checked;
5. localisation claim invariance is checked;
6. deterministic deny-list and safety validation run;
7. deterministic feasibility is derived from the visual plan;
8. the Creative Critic receives the validated creative in separate
   context;
9. bounded revision may return the creative to `script-engine`;
10. `compliance-reviewer` performs the judgement layer;
11. locking and Gate 3 remain outside the Skill.

The Skill never persists the Creative itself.

The orchestrator owns canonical creation and versioning.

---

### O.6 Failure & Uncertainty

The Skill must surface a failure or revision need when:

- the approved Concept cannot be executed without changing its meaning;
- no supplied format is workable for the Concept;
- a required claim has no usable supplied evidence;
- an exact qualification cannot be incorporated without contradiction;
- the requested duration cannot plausibly contain the required
  argument;
- localisation would require changing claim meaning;
- customer-language evidence is insufficient for a strongly local
  register;
- supplied style constraints conflict with the argument;
- a production requirement appears outside supplied tool capability;
- the storyboard requires continuity that cannot be described
  coherently;
- a visual treatment would imply a stronger claim than the script;
- natural wording remains materially ambiguous.

Valid conservative outcomes include:

- execution revision request;
- evidence request;
- format-fit failure;
- language ambiguity finding;
- upstream Concept revision request;
- feasibility concern.

Do not repair an upstream strategic or evidence defect by rewriting it
silently.

---

### O.7 Boundaries

`script-engine` owns:

- approved strategy-to-execution translation;
- Hook Strategy;
- format-fit execution reasoning when assignment is not fixed;
- narrative-pattern selection from supplied options;
- style-fit selection from supplied options;
- voice-specification reasoning;
- persuasion beats;
- complete scripts;
- Brilliance language refinement;
- Chile localisation;
- spoken naturalness;
- Hook Execution;
- storyboard / shot-list reasoning;
- continuity-aware visual planning;
- explicit execution gaps.

It does not own:

- Product Truth;
- market research;
- Audience Model creation;
- hypothesis generation;
- Concept redesign;
- canonical ID allocation;
- registry authoring;
- source-quality classification;
- claim verification;
- claim-freedom resolution;
- hard safety validation;
- localisation-invariance enforcement;
- deterministic feasibility verdict;
- Creative Critic;
- compliance judgement;
- experiment validation;
- persistent state;
- Production Package assembly;
- V1-Production routing;
- media generation.

Those responsibilities belong to upstream Skills, config, tools,
deterministic services, orchestration, `compliance-reviewer`, or human
gates.

---

### O.8 Knowledge-use Boundary

`KNW-schwartz-persuasion` may influence:

- persuasion-beat sequencing;
- proof placement;
- momentum;
- mechanism explanation;
- objection handling.

`KNW-schwartz-language` may influence the dedicated Brilliance language
pass and its ambiguity findings.

Neither resource may:

- create product facts;
- expand claim freedom;
- manufacture a Reason to Believe;
- override current market evidence;
- replace real Chile customer language;
- remove required qualifications;
- legitimise native-format impersonation;
- alter the approved Concept.

`KNW-schwartz-integration` remains excluded at runtime.

No quarantined knowledge is consumed.

---

### O.9 Design Acceptance Criteria

The eventual `SKILL.md` is conformant only if:

1. it inherits the approved Concept instead of re-deciding strategy;
2. source Hypothesis dimensions remain unchanged;
3. Hook Strategy precedes final execution choices;
4. it uses supplied format/narrative/style profiles rather than
   embedding their policy;
5. it produces complete word-for-word copy with no placeholders;
6. it uses one polymorphic script procedure constrained by the supplied
   format profile;
7. it keeps Hook strategy/copy/visual/audio separately addressable;
8. hook copy and the corresponding script segment express the same
   exact wording;
9. Schwartz Persuasion is advisory and evidence-subordinate;
10. Schwartz Language is restricted to the Brilliance language pass;
11. Chile localisation is a distinct pass after the neutral strategic
    draft;
12. localisation changes expression rather than claim meaning;
13. it exposes ambiguity that may contain hidden or intensified claims;
14. it produces a generator-usable storyboard / shot list;
15. it plans continuity without hardcoding tool-duration limits;
16. it does not perform deterministic claim binding;
17. it does not perform deterministic localisation-invariance checks;
18. it does not decide deterministic feasibility;
19. it does not emit a `HARD_BLOCK`;
20. it emits no canonical identifier and writes no persistent state;
21. it does not route or generate production media.

---

## P. Skill Design 5 — `compliance-reviewer`

**Status:** PROPOSED
**Initial version:** `1.0.0`
**Runtime knowledge declaration:** `KNW-schwartz-persuasion`

### P.1 Role

`compliance-reviewer` performs the judgement layer of creative
compliance.

Its central responsibility is:

> identify semantic, contextual, and presentation risks that cannot be
> reduced to deterministic rule matching, without pretending to make
> final legal, platform, or hard-block decisions.

The Skill reviews how a concept or creative may reasonably be
understood.

It does not re-run mechanical evidence checks.

It does not author compliance policy.

It does not emit `HARD_BLOCK`.

---

### P.2 Invocation Modes

The same Skill may be invoked in two bounded modes.

#### Mode A — Concept Pre-Screen Judgement

Runs before expensive script generation.

Reviews a Hypothesis or Concept for qualitative compliance risk after
deterministic checks have evaluated:

- required territories;
- claim dependencies;
- deny-list matches.

The purpose is to surface semantic risk early.

#### Mode B — Full Creative Review

Runs on the final Creative after:

- final Chile localisation;
- claim-to-evidence binding;
- qualification checks;
- localisation-invariance checks;
- deterministic deny-list / safety validation;
- deterministic feasibility;
- Creative Critic review as sequenced by orchestration.

The purpose is to review what the finished execution communicates,
including implied meaning created by words, visuals, sequencing, and
native-format presentation.

---

### P.3 Inputs

Depending on invocation mode, the orchestrator may supply:

- Hypothesis or Concept;
- final Creative proposal;
- approved Product Truth projection;
- pinned claim-freedom tier;
- permitted territories;
- verified claim and qualification projections;
- deterministic pre-screen result;
- deterministic script-safety result;
- localisation-invariance result;
- ambiguity findings from `script-engine`;
- Creative Critic findings when available;
- category-profile projection;
- brand constraints;
- current policy / legal source material fetched during the same run;
- policy-source metadata;
- relevant evidence handles;
- retrieved `KNW-schwartz-persuasion`.

The Skill receives current policy material as input.

It does not fetch or cache policy itself.

It does not retrieve arbitrary knowledge.

It does not consume `KNW-schwartz-language` directly.

Language ambiguity generated during the Brilliance pass is supplied as
input when relevant.

It never consumes quarantined knowledge.

---

### P.4 Procedure

#### Step 1 — Respect deterministic safety as a separate authority

Read the supplied deterministic safety output.

Do not:

- reproduce mechanical claim binding;
- reclassify source quality;
- override a deny-list result;
- clear a deterministic block;
- declare that an unresolved claim is acceptable;
- alter claim-freedom tier.

A deterministic `HARD_BLOCK` is not a judgement question.

If safety is blocked, the Skill may explain additional semantic risk,
but it cannot clear or downgrade the block.

#### Step 2 — Review the communication, not only literal sentences

Assess what a reasonable viewer could understand from the combined
creative.

Consider:

- spoken words;
- on-screen text;
- visual sequencing;
- demonstrations;
- captions;
- before/after juxtaposition;
- testimonials;
- comparative framing;
- urgency;
- scarcity;
- native-format cues;
- omission of material qualifications.

A statement may be risky even if no single sentence contains the full
claim.

Do not restrict review to keyword matching.

#### Step 3 — Detect implied claims

Look for cases where the creative communicates a claim indirectly.

Examples of semantic mechanisms include:

- juxtaposition;
- causal sequencing;
- visual demonstration;
- testimonial implication;
- comparison without explicit comparator;
- rhetorical questions that imply an answer;
- wording whose practical meaning exceeds its literal wording.

Ask:

> would stating the implied proposition directly require evidence or
> qualification that the supplied creative does not visibly carry?

If yes, create an `IMPLIED_CLAIM` finding.

The Skill does not itself bind the implied claim to evidence.

It surfaces the judgement for remediation or human review.

#### Step 4 — Review ambiguity as compliance risk

Use the supplied language ambiguity findings and independently inspect
the final creative.

Identify wording where:

- the actor is unclear;
- causality is unclear;
- scope is unclear;
- comparison scope is unclear;
- a qualification appears to attach to the wrong statement;
- a viewer could reasonably interpret a stronger promise than intended.

Ambiguity matters when one plausible reading enters a riskier claim
territory.

Do not treat stylistic ambiguity as a compliance issue unless it can
materially change meaning.

#### Step 5 — Review claim intensification

Compare the practical meaning of the final wording with the supplied
approved claim context.

Look for semantic intensification that may survive deterministic
claim-set comparison, such as:

- "may help" becoming practically communicated as "will";
- a limited benefit becoming an overall outcome;
- correlation being presented as causation;
- a composition statement becoming an efficacy implication;
- a qualified statement being framed as universal.

This is judgement.

Do not create a new evidence rule or numeric severity score.

#### Step 6 — Review qualification sufficiency in context

Mechanical services verify required qualification presence.

This Skill judges whether the qualification is communicated in a way
that reasonably qualifies the relevant claim.

Consider:

- proximity;
- visibility;
- spoken timing;
- relationship to the claim;
- whether other wording undermines the qualification;
- whether the overall creative leaves a materially different
  impression.

Do not declare a missing required qualification mechanically present.

If the deterministic check says `MISSING`, that result stands.

#### Step 7 — Review testimonials and demonstrations

When the supplied creative includes a testimonial, demonstration, or
personal-experience framing, inspect whether it may imply:

- typical results;
- guaranteed outcomes;
- unsupported efficacy;
- product characteristics not in Product Truth;
- hidden expert or authority status;
- a stronger claim than the speaker directly states.

Distinguish:

- a person's subjective experience;
- a general product assertion.

Do not treat one as automatic evidence for the other.

#### Step 8 — Review before/after communication

Evaluate literal and functional before/after presentations.

Risk may arise from:

- paired images;
- sequential shots;
- captions;
- transformation language;
- timing;
- editing that implies a product-caused change.

A before/after implication can exist even without those exact words.

Use current supplied policy sources when deciding whether the treatment
requires escalation.

Do not embed a permanent before/after rule in the Skill.

#### Step 9 — Review native-format fit versus impersonation

Distinguish legitimate use of a format's communication grammar from
deceptive presentation as genuine third-party or organic content.

Review whether the creative could reasonably impersonate:

- an authentic Reddit thread;
- a genuine platform post;
- editorial coverage;
- an independent review;
- unsolicited customer content;
- platform endorsement.

Native-feeling execution is not automatically deceptive.

The concern is misrepresentation of provenance or authenticity.

The Skill may flag `NATIVE_FORMAT_FIT`.

Deterministic deny-list rules remain separate and authoritative where a
known prohibited pattern matches.

#### Step 10 — Review category-sensitive communication

Use the supplied category profile and current policy material to inspect
risk that requires contextual judgement.

Examples may include:

- health-related implication;
- financial implication;
- age-sensitive framing;
- testimonial sensitivity;
- authority cues;
- transformation framing;
- comparative language.

Do not embed category policy in this Skill.

If the applicable policy cannot be confidently resolved from current
inputs, return `POLICY_REVIEW_REQUIRED`.

#### Step 11 — Review urgency and scarcity

Determine whether urgency or scarcity appears materially misleading.

Distinguish evidence-backed offer conditions from manufactured pressure.

Review:

- deadline wording;
- inventory claims;
- exclusivity;
- "only today";
- "last units";
- limited-batch framing;
- urgency implied through visual countdown or narration.

If current evidence does not establish the asserted scarcity or timing,
surface the issue.

Do not convert the finding into a deterministic `HARD_BLOCK`.

#### Step 12 — Use Schwartz only for deception-sensitive judgement

`KNW-schwartz-persuasion` may help inspect issues such as:

- redefinition becoming concealment;
- native-format technique becoming impersonation;
- persuasive implication exceeding support;
- mechanism or proof framing creating a stronger promise;
- reason-to-believe presentation becoming deceptive.

Schwartz remains advisory.

It does not override:

- Product Truth;
- Evidence Ledger state;
- deterministic safety;
- current policy material;
- current legal/platform requirements.

Historical technique is never authority over current policy.

#### Step 13 — Use current policy sources, not remembered policy

Base policy-sensitive judgement on the policy material supplied for the
current run.

For any finding that materially depends on current external policy,
ensure the result can be associated with the supplied policy-source
metadata.

Do not claim:

- "Meta approved";
- "Meta compliant";
- "guaranteed policy safe";
- "legally approved".

The Skill reviews risk.

It does not certify platform acceptance or legal approval.

#### Step 14 — Produce explainable findings

Every finding should identify:

- category;
- affected field or semantic area;
- reasoning;
- suggested remediation.

Supported finding categories are:

- `IMPLIED_CLAIM`;
- `AMBIGUITY`;
- `TESTIMONIAL`;
- `BEFORE_AFTER`;
- `NATIVE_FORMAT_FIT`;
- `CATEGORY_SENSITIVE`;
- `QUALIFICATION_SUFFICIENCY`;
- `URGENCY_SCARCITY`.

Use the supplied schema values.

Do not invent a second compliance taxonomy inside the Skill.

#### Step 15 — Assign the judgement verdict

Return one of:

- `LOW`;
- `MEDIUM`;
- `HIGH_RISK`;
- `POLICY_REVIEW_REQUIRED`.

Use written reasoning.

Do not produce a numeric risk score.

Do not emit:

- `PASS`;
- `FAIL`;
- `APPROVED`;
- `META_APPROVED`;
- `HARD_BLOCK`.

`HIGH_RISK` and `POLICY_REVIEW_REQUIRED` are escalation judgements, not
irreversible machine blocks.

Human adjudication occurs outside the Skill.

---

### P.5 Concept Pre-Screen Output

When invoked on a Hypothesis or Concept, return only the judgement
portion needed by the compliance pre-screen:

- verdict;
- concise reasoning;
- semantic risk findings when useful;
- remediation or evidence need when identifiable.

Do not rewrite the full Concept.

Do not perform:

- territory-permission comparison;
- claim-dependency satisfiability;
- deny-list matching.

Those are deterministic pre-screen checks.

A concept-level judgement does not replace the later full Creative
review.

---

### P.6 Full Creative Output Contract

For a full Creative review, return a semantic proposal containing:

1. **Verdict**
   - `LOW`;
   - `MEDIUM`;
   - `HIGH_RISK`;
   - `POLICY_REVIEW_REQUIRED`.

2. **Findings**
   - category;
   - affected field;
   - written reasoning;
   - suggested remediation.

3. **Policy-source associations**
   - only from policy sources supplied for the current run.

4. **Escalation rationale**
   - when human or specialist policy review is required.

The Skill does not return:

- `HARD_BLOCK`;
- deterministic safety checks;
- canonical finding IDs;
- reviewer timestamps;
- prompt hashes;
- canonical Creative version;
- human adjudication;
- Gate decision;
- Creative state;
- release approval.

Those are added or controlled outside the Skill.

---

### P.7 Handoffs

#### Concept Pre-Screen

After judgement:

1. deterministic pre-screen results and judgement are combined outside
   the Skill;
2. deterministic `HARD_BLOCK` conditions remove invalid candidates;
3. surviving risk findings are available to strategy and Gate 2;
4. `HIGH_RISK` or `POLICY_REVIEW_REQUIRED` may trigger human review or
   concept revision.

#### Full Creative Review

After judgement:

1. the orchestrator records the model-facing review result;
2. `LOW` or `MEDIUM` proceeds according to the surrounding gate logic;
3. `HIGH_RISK` or `POLICY_REVIEW_REQUIRED` requires human adjudication
   before release;
4. remediation requiring content change returns to `script-engine` and
   creates a new Creative version through orchestration;
5. deterministic safety is re-run on any new Creative version;
6. Gate 3 remains the human Production Release gate.

The Skill does not approve release itself.

---

### P.8 Failure & Uncertainty

Return `POLICY_REVIEW_REQUIRED` when:

- current policy material is missing;
- supplied policy sources conflict materially;
- category applicability is unclear;
- the creative enters a legally sensitive area outside the supplied
  rule context;
- the distinction between legitimate native format and impersonation
  cannot be resolved confidently;
- a qualification may be materially insufficient but the governing
  policy is unclear;
- a testimonial / before-after treatment requires specialist review;
- semantic claim intensification appears plausible but cannot be
  resolved from supplied evidence.

Do not resolve uncertainty by inventing policy.

Do not rely on remembered platform rules when current policy retrieval
was required.

---

### P.9 Boundaries

`compliance-reviewer` owns:

- implied-claim judgement;
- ambiguity-as-risk judgement;
- semantic claim-intensification review;
- testimonial judgement;
- before/after judgement;
- native-format-fit / impersonation judgement;
- category-sensitive judgement;
- qualification-sufficiency judgement;
- urgency/scarcity judgement;
- policy-sensitive written reasoning;
- remediation suggestions;
- escalation recommendations.

It does not own:

- policy authoring;
- policy fetching;
- deny-list authoring;
- deny-list matching;
- claim verification;
- source-quality classification;
- claim-freedom resolution;
- localisation-invariance enforcement;
- rights validation;
- deterministic asset checks;
- experiment lock validation;
- canonical ID allocation;
- Creative persistence;
- hard-block decisions;
- human adjudication;
- Gate 3 approval;
- platform approval;
- legal approval.

Those responsibilities remain with config, tools, deterministic
services, orchestration, or human reviewers.

---

### P.10 Knowledge-use Boundary

`KNW-schwartz-persuasion` may influence judgement about:

- deceptive redefinition;
- native-format impersonation;
- unsupported proof framing;
- implication that communicates a hidden claim;
- persuasive framing that conceals a material limitation.

It may not:

- define current Meta policy;
- define current law;
- override deterministic safety;
- expand claim freedom;
- excuse unsupported claims;
- clear a hard block;
- certify a creative as approved.

`KNW-schwartz-language` is not retrieved directly by this Skill.

Relevant ambiguity findings from the language pass are supplied through
the Creative review input.

`KNW-schwartz-integration` remains excluded at runtime.

No quarantined knowledge is consumed.

---

### P.11 Design Acceptance Criteria

The eventual `SKILL.md` is conformant only if:

1. it remains the judgement layer rather than duplicating deterministic
   safety;
2. it supports both concept pre-screen and full Creative review;
3. it never emits `HARD_BLOCK`;
4. it uses only `LOW | MEDIUM | HIGH_RISK |
   POLICY_REVIEW_REQUIRED` as review verdicts;
5. it detects implied claims beyond literal keyword matching;
6. it treats ambiguity as risk only when meaning may materially change;
7. it reviews semantic claim intensification that deterministic
   claim-set checks may miss;
8. it reviews qualification sufficiency in context without replacing
   mechanical presence checks;
9. it distinguishes native-format grammar from deceptive impersonation;
10. it relies on supplied current policy sources for policy-sensitive
    judgement;
11. it does not embed current platform or legal rules;
12. it never claims Meta approval or guaranteed compliance;
13. it uses Schwartz only as advisory deception-sensitive reasoning;
14. it consumes no quarantined knowledge;
15. it returns explainable findings with remediation;
16. `HIGH_RISK` and `POLICY_REVIEW_REQUIRED` escalate to humans rather
    than becoming irreversible model blocks;
17. it emits no canonical identifier and writes no persistent state.

---

## Q. Cross-Skill Boundary Audit

**Status:** PROPOSED PASS

This section audits the five Skill designs as one system.

The objective is not to prove that every Skill is individually useful.

The objective is to prove that no responsibility with one required
authority has accidentally gained two owners.

---

### Q.1 Single-Owner Reasoning Map

| Reasoning responsibility | Skill owner |
|---|---|
| Product Truth fact reasoning | `product-intelligence` |
| Brand Snapshot reasoning | `product-intelligence` |
| Chile market interpretation | `market-intelligence-cl` |
| Customer-language extraction | `market-intelligence-cl` |
| Competitive-field interpretation | `market-intelligence-cl` |
| Audience Model | `creative-strategist` |
| Persuasion Projection | `creative-strategist` |
| Insight reasoning | `creative-strategist` |
| Hypothesis generation | `creative-strategist` |
| Belief bridges | `creative-strategist` |
| Concept development | `creative-strategist` |
| Qualitative format/narrative fit at Concept level | `creative-strategist` |
| Strategy-to-execution translation | `script-engine` |
| Hook Strategy execution pass | `script-engine` |
| Persuasion beats | `script-engine` |
| Complete scripts | `script-engine` |
| Brilliance language pass | `script-engine` |
| Chile localisation | `script-engine` |
| Hook copy / visual / audio execution | `script-engine` |
| Storyboard / visual plan | `script-engine` |
| Semantic compliance judgement | `compliance-reviewer` |

No reasoning responsibility above has two primary Skill owners.

---

### Q.2 Deterministic Responsibilities — No Skill Owner

The following responsibilities are explicitly outside all Skills:

- canonical ID allocation;
- canonical version allocation;
- canonical hashing;
- persistence;
- filesystem writes;
- Evidence Ledger writes;
- Product Truth coverage computation;
- claim-freedom resolution;
- source-quality classification;
- source reconciliation;
- schema validation;
- deterministic concept pre-screen checks;
- diversity spread computation;
- constrained final selection;
- Experiment Plan structural assembly;
- declared-variable validation;
- locked-variable validation;
- experiment binding;
- claim-to-evidence binding;
- required-qualification presence validation;
- localisation claim invariance;
- deny-list matching;
- rights validation;
- asset-state validation;
- deterministic feasibility;
- Creative state folding;
- Production Package assembly;
- release eligibility;
- hard compliance blocking.

If any of these later appears as model authority inside a Skill, that is
a Phase 4 boundary regression.

---

### Q.3 Orchestrator Responsibilities — No Skill Owner

The orchestrator owns:

- pipeline sequence;
- invocation mode;
- context assembly;
- model-facing schema selection;
- knowledge retrieval;
- tool invocation;
- retries;
- batching;
- canonical identifier allocation;
- canonical version creation;
- persistence;
- deterministic-service invocation;
- Gate preparation;
- human-review routing;
- revision routing;
- run-event recording;
- policy-source retrieval;
- production routing in V1-Production.

A Skill may request evidence, research, capability, revision, or human
review.

A Skill does not invoke itself or another Skill as a subroutine.

There is no Master Skill.

---

### Q.4 Human Authorities — No Skill Replacement

The three frozen human gates remain:

1. Gate 1 — Truth & Evidence;
2. Gate 2 — Concepts & Experiment Plan;
3. Gate 3 — Production Release.

Skills prepare reasoning used by gates.

They do not approve their own durable outputs.

`compliance-reviewer` may escalate risk.

It does not approve release.

---

### Q.5 Epistemic Spine Audit

The Skill chain preserves:

`SOURCE -> OBSERVATION -> INSIGHT -> HYPOTHESIS -> CONCEPT -> EXPERIMENT -> CREATIVE`

Ownership across that chain is:

- SOURCE acquisition: tool/orchestration;
- OBSERVATION extraction: evidence pipeline, with research interpretation
  supported by `market-intelligence-cl`;
- INSIGHT: `creative-strategist`;
- HYPOTHESIS: `creative-strategist`;
- CONCEPT: `creative-strategist`;
- EXPERIMENT: orchestrator + deterministic services;
- CREATIVE generative execution: `script-engine`;
- compliance judgement: `compliance-reviewer`.

No Skill is authorised to collapse an upstream level into a downstream
one without the required intermediate semantics.

---

### Q.6 Product / Market Boundary Audit

`product-intelligence` establishes Product Truth and Brand Snapshot.

`market-intelligence-cl` may observe:

- what customers believe;
- what competitors claim;
- how alternatives are positioned.

It may not rewrite Product Truth.

A customer statement is not a product fact.

A competitor claim is not product evidence merely because it exists.

Any apparent contradiction with Product Truth is surfaced upstream.

**Result:** PASS.

---

### Q.7 Market / Strategy Boundary Audit

`market-intelligence-cl` provides evidence and customer language for:

- problems;
- desires;
- objections;
- alternatives;
- beliefs;
- awareness;
- sophistication.

It does not create the final Audience Model.

`creative-strategist` creates the evidence-linked Audience Model and
Persuasion Projection from that research.

**Result:** PASS.

---

### Q.8 Strategy / Execution Boundary Audit

`creative-strategist` creates a format-agnostic Concept.

The Concept defines the strategic argument and evaluates fit.

`script-engine` commits that approved argument to execution:

- format;
- narrative pattern;
- style;
- voice specification;
- hook execution;
- script;
- visual plan.

`script-engine` may not change the Hypothesis dimensions, current belief,
core promise, or belief bridge in order to make execution easier.

**Result:** PASS.

---

### Q.9 Execution / Compliance Boundary Audit

`script-engine` is the generator.

It may identify ambiguity or possible risk in its own language output,
but it does not grade its compliance.

`compliance-reviewer` reviews the resulting communication in separate
judgement context.

Deterministic safety remains a third, independent authority.

Therefore:

- generator != compliance judge;
- compliance judge != deterministic blocker.

**Result:** PASS.

---

### Q.10 HARD_BLOCK Authority Audit

No Skill owns `HARD_BLOCK`.

Only deterministic validation may produce irreversible `HARD_BLOCK`.

Model-facing compliance judgement is limited to:

- `LOW`;
- `MEDIUM`;
- `HIGH_RISK`;
- `POLICY_REVIEW_REQUIRED`.

A human may adjudicate a judgement escalation.

A human may not override a deterministic `HARD_BLOCK`.

The underlying defect must be corrected and validation re-run.

**Result:** PASS.

---

### Q.11 Creative Critic Boundary Audit

Creative Critic remains an orchestrator role with separate context.

It is not:

- a sixth Skill;
- a mode of `script-engine` that grades its own output;
- a mode of `compliance-reviewer`.

Its function is creative-quality criticism.

Compliance judgement remains separately owned.

**Result:** PASS.

---

### Q.12 Knowledge Consumption Audit

The five runtime declarations are:

| Skill | Runtime knowledge |
|---|---|
| `product-intelligence` | `none` |
| `market-intelligence-cl` | `KNW-schwartz-persuasion` |
| `creative-strategist` | `KNW-schwartz-persuasion` |
| `script-engine` | `KNW-schwartz-persuasion,KNW-schwartz-language` |
| `compliance-reviewer` | `KNW-schwartz-persuasion` |

Rules:

- `KNW-schwartz-integration` is never runtime knowledge;
- `_quarantine` is never declared;
- `script-engine` is the only Skill that directly retrieves
  `KNW-schwartz-language`;
- `compliance-reviewer` receives relevant ambiguity findings through
  its input rather than retrieving the language engine;
- Product Truth always outranks framework advice;
- current evidence always outranks framework assumptions.

**Result:** PASS.

---

### Q.13 Config Boundary Audit

Skills may consume projections from authored registries.

They may not author those registries.

The nine frozen config families remain external policy/data:

- `evidence_policy`;
- `deny_list`;
- `narrative_library`;
- `format_profiles`;
- `category_profiles`;
- `creative_taxonomy`;
- `experiment_variables`;
- `diversity_targets`;
- `tool_capability`.

A Skill instruction must not copy these registries into itself.

**Result:** PASS.

---

### Q.14 Tool Boundary Audit

The five Skills own no external capability.

Examples:

- vision remains a tool;
- web research remains a tool;
- current-policy retrieval remains a tool/orchestrator action;
- media generation remains V1-Production capability;
- asset inspection remains tool/service capability.

Skills reason over prepared tool results.

**Result:** PASS.

---

### Q.15 Persistence Boundary Audit

No Skill:

- writes `store/`;
- writes `reviews/`;
- writes SQLite;
- appends event logs;
- registers an asset;
- writes a canonical artefact;
- mutates an existing artefact;
- creates canonical IDs.

All Skill output is transient model-facing content until orchestration
validates and persists it.

**Result:** PASS.

---

### Q.16 Phase Boundary Audit

Phase 4 remains Skills Design.

Before implementation authorisation:

- `.claude/skills/` must remain absent;
- `src/` must remain absent;
- `tests/` must remain absent.

Phase 4 does not implement:

- runtime orchestration;
- deterministic services;
- Python;
- V1-Production;
- Higgsfield integration;
- Meta performance ingestion.

**Result:** PASS.

---

### Q.17 Cross-Skill Audit Verdict

The five proposed Skills have non-overlapping primary ownership:

1. `product-intelligence` — truth reasoning;
2. `market-intelligence-cl` — Chile market evidence reasoning;
3. `creative-strategist` — strategy reasoning;
4. `script-engine` — creative execution reasoning;
5. `compliance-reviewer` — compliance judgement.

Deterministic authority, orchestration authority, tool capability,
persistence authority, and human approval remain outside all five.

**CROSS-SKILL DESIGN VERDICT: PASS**
