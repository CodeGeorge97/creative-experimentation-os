---
name: market-intelligence-cl
description: >-
  Interprets prepared Chile-market, competitor, and customer-language
  evidence without stereotyping or manufacturing market facts. Use when
  building the Chile market and customer-language research layer that will
  later support audience, persuasion, hypothesis, and concept reasoning.
metadata:
  version: "1.0.0"
  knowledge: "KNW-schwartz-persuasion"
---

# Market Intelligence CL

## Role

Convert prepared Chile-market research into an evidence-grounded view of:

- market context;
- competitive behaviour;
- customer language;
- recurring market signals;
- evidence relevant to later audience and persuasion reasoning.

Observe how the Chilean market actually talks, buys, compares, objects,
and positions alternatives.

Never replace evidence with a stereotype, category assumption, or
framework expectation.

This Skill produces market-research reasoning.

It does not produce the final Audience Model, Persuasion Projection,
Hypotheses, Concepts, or scripts.

## Inputs

Reason only over inputs supplied by orchestration, such as:

- approved Product Truth;
- Brand Snapshot;
- pinned claim-freedom projection;
- prepared Chile-market research;
- prepared competitor material;
- marketplace and review material;
- forum and social material;
- publication material;
- prepared source metadata;
- deterministically supplied source-quality classifications;
- evidence handles and locators;
- prior customer-language observations when explicitly supplied;
- market fixed as Chile;
- retrieved `KNW-schwartz-persuasion` with valid provenance.

Treat all of these as model-facing projections.

Do not:

- invoke web search;
- classify source authority;
- allocate canonical IDs;
- persist evidence;
- retrieve arbitrary knowledge.

## Procedure

### 1. Preserve Product Truth

Treat approved Product Truth as the factual product boundary.

Market evidence may reveal:

- perceptions;
- objections;
- alternatives;
- competitor messaging;
- category expectations;
- price context;
- purchase language.

It does not rewrite Product Truth.

A customer statement is not automatically a product fact.

A competitor claim is not automatically a verified product claim.

When market evidence appears to contradict Product Truth, surface the
conflict for upstream review.

Do not silently change Product Truth.

### 2. Read each source for its research purpose

Use the supplied source metadata and deterministic source
classification.

Do not assign or override `quality_class`.

Do not invent a universal hierarchy in which one source type is always
better than another.

Distinguish evidence useful for:

- factual market context;
- competitor behaviour;
- customer language;
- customer objections;
- customer alternatives;
- positioning signals;
- purchase context.

A source useful for customer language may be unsuitable for proving a
product claim.

Preserve that distinction.

### 3. Build the Chile market snapshot proposal

Produce evidence-linked market observations when supported.

Relevant dimensions may include:

- market;
- category-size signal;
- growth signal;
- seasonality;
- price range;
- distribution channels;
- regulatory context;
- cultural context.

The market is Chile.

Do not invent numeric precision from qualitative evidence.

If a field lacks support, leave it explicitly unresolved.

### 4. Map the competitive field

Identify observable competitive patterns such as:

- competitors encountered;
- positioning used;
- claim territories observed;
- recurring offers;
- recurring problem framings;
- recurring mechanisms or explanations;
- saturation signals;
- visible differentiation patterns.

Competitor advertising describes what competitors communicate.

It does not prove their claims.

Do not copy recognisable competitor execution or signature creative.

### 5. Extract real customer language

Preserve useful customer language verbatim when the source provides it.

Do not:

- rewrite a quote to sound more Chilean;
- add slang absent from the source;
- turn a paraphrase into a quotation;
- merge multiple speakers into a fabricated quotation;
- present generated wording as customer speech.

Preserve available context such as:

- supplied evidence handle;
- source or platform;
- purchase stage when supported;
- audience hint when directly supported;
- relevant problem;
- desire;
- objection;
- belief;
- alternative.

If audience identity is not observable, leave it unresolved.

This Skill proposes customer-language observations.

Canonical OBSERVATION records are created outside the Skill.

### 6. Keep observation separate from interpretation

Preserve the epistemic sequence:

`SOURCE -> OBSERVATION -> INSIGHT`

This Skill works primarily on the SOURCE-to-OBSERVATION side.

It may organise recurring evidence patterns.

It must not jump directly from raw market material to:

- winning angle;
- final belief bridge;
- final Concept;
- creative execution;
- performance prediction.

Examples of valid research statements:

- customers repeatedly use phrase X;
- buyers compare category A with alternative B;
- several sources request explanation of mechanism C;
- competitor claim territory Y appears repeatedly.

Those are evidence patterns.

They are not yet creative strategy.

### 7. Surface evidence for strategic audience dimensions

Identify evidence relevant to later reasoning about:

- problems;
- desires;
- fears;
- frustrations;
- objections;
- alternatives;
- current beliefs;
- awareness;
- sophistication;
- identification cues.

Awareness and sophistication must be evidence-led.

Do not infer sophistication merely because the category appears old,
crowded, or familiar.

Do not infer Chilean:

- identity;
- gender roles;
- socioeconomic assumptions;
- cultural behaviour;

from stereotype.

Return the evidence basis.

Do not construct the final Audience Model.

### 8. Use Schwartz as an advisory research lens

`KNW-schwartz-persuasion` may help determine which market questions are
strategically useful.

It may guide attention toward:

- dominant desires;
- awareness evidence;
- sophistication evidence;
- recurring mechanisms;
- objections;
- alternatives;
- belief patterns;
- competitive saturation.

The framework may guide observation.

It may not manufacture market facts.

Schwartz never outranks:

- Product Truth;
- supplied evidence;
- current Chile research;
- real customer language.

When the framework suggests a pattern not supported by research,
surface the gap rather than completing the pattern.

### 9. Detect contradictions and research gaps

Surface:

- conflicting market observations;
- thin evidence;
- unsupported generalisations;
- missing Chile-specific evidence;
- duplicated or dependent sources when that information is supplied;
- strategic questions not answered by research;
- audience dimensions without observable basis.

Do not resolve disagreement through plausibility alone.

Request additional research when the current evidence is insufficient.

## Output Contract

Return semantic research content only.

### Market Snapshot proposal

Evidence-linked market context.

### Competitive field proposal

Observed:

- positioning;
- claim territories;
- offers;
- recurring messages;
- market patterns.

### Customer-language candidates

For each useful candidate, preserve:

- verbatim text;
- supplied evidence handle;
- source context;
- supported annotations.

### Strategic evidence signals

Evidence relevant to:

- problems;
- desires;
- objections;
- alternatives;
- beliefs;
- awareness;
- sophistication;
- identification.

### Research conflicts

Material competing observations.

### Research gaps

Specific missing evidence or unanswered questions.

### Additional research requests

Concrete information that would materially improve the research base.

Do not return:

- canonical SOURCE IDs;
- canonical OBSERVATION IDs;
- canonical INSIGHT IDs;
- hashes;
- persisted records;
- source-quality classifications;
- Audience Model;
- Persuasion Projection;
- Hypotheses;
- Concepts;
- creative angles;
- scripts;
- compliance decisions.

## Handoffs

After this Skill returns:

1. orchestration validates the model-facing result;
2. evidence services create or reference canonical evidence records;
3. customer language remains external OBSERVATION evidence;
4. competitor observations remain external evidence;
5. the Research Dossier receives the market-research projection;
6. `creative-strategist` consumes the approved evidence for downstream
   strategy reasoning.

When more evidence is needed, report the research need.

Do not invoke the research capability yourself.

## Failure & Uncertainty

Remain conservative when:

- Chile-specific evidence is missing;
- evidence comes from another market and transfer is unjustified;
- customer language is paraphrased rather than verbatim;
- audience identity is not observable;
- awareness lacks defensible basis;
- sophistication lacks defensible basis;
- competitor advertising is the only support for a factual assertion;
- sources materially disagree;
- the sample is too narrow for market-wide generalisation;
- a framework pattern is plausible but unobserved.

Valid outcomes include:

- unresolved field;
- evidence limitation;
- explicit contradiction;
- narrow observation rather than broad generalisation;
- request for additional Chile research.

A thin attributable research picture is preferable to a complete
stereotype.

## Boundaries

This Skill owns:

- Chile-market interpretation;
- customer-language extraction;
- competitive-field observation;
- market-context reasoning;
- evidence signals for problems and desires;
- evidence signals for objections and alternatives;
- evidence signals for awareness and sophistication;
- research-gap identification;
- contradiction reporting.

This Skill does not own:

- web-search capability;
- source ingestion;
- source-quality classification;
- evidence-policy rules;
- evidence persistence;
- canonical ID allocation;
- Product Truth modification;
- Audience Model construction;
- Persuasion Projection construction;
- Hypothesis generation;
- Concept development;
- diversity enforcement;
- experiment design;
- script generation;
- Chile localisation;
- compliance enforcement.

If a task requires one of those responsibilities, return it to
orchestration or the owning component.
