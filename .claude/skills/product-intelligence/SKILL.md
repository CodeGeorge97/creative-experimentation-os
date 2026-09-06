---
name: product-intelligence
description: >-
  Extracts evidence-grounded Product Truth and Brand Snapshot facts from
  prepared product, brand, visual, operator, and research evidence. Use when
  establishing or updating product truth before market research, especially
  from sparse inputs such as a product image and brand name.
metadata:
  version: "1.0.0"
  knowledge: "none"
---

# Product Intelligence

## Role

Convert prepared product and brand evidence into an epistemically explicit
Product Truth fact proposal and Brand Snapshot.

Extract only what the supplied evidence supports.

Never fill an evidence gap because a value seems likely.

Do not decide what advertising claims are permitted.

## Inputs

Reason only over inputs supplied by orchestration, such as:

- operator-provided product or brand information;
- prepared product-image observations;
- verbatim visible label text;
- prepared official-source product or brand research;
- prepared evidence classifications and references;
- detected conflicts between evidence items;
- applicable category-profile projections;
- an existing Product Truth projection when extending or correcting it.

Treat these as model-facing projections.

Never allocate IDs, hashes, versions, event sequence numbers, or storage paths.

This Skill has no runtime knowledge-resource dependency.

## Procedure

### 1. Separate evidence origins

Preserve what each input actually establishes.

- Operator input is an explicit operator assertion.
- Image evidence establishes only what is visibly observable.
- Label text establishes that the label states something.
- Label text alone does not establish that the statement is true.
- Research establishes only what the supplied evidence supports.
- Missing evidence does not establish absence.

Never collapse observation, interpretation, and verification.

### 2. Establish identity conservatively

Determine whether the supplied material describes one coherent product.

A clearly visible identity may remain `OBSERVED`.

External verification is not required merely to recognise an otherwise
unambiguous supplied product.

If identity is ambiguous, illegible, contradictory, or guess-dependent,
surface the unresolved identity.

Do not calculate T0, T1, T2, or T3.

### 3. Propose Product Truth facts

Reason over the Product Truth dimensions supplied by the architecture:

- identity;
- category;
- visual;
- composition;
- function;
- commercial;
- proof;
- restrictions;
- supplied category extensions.

Every proposed leaf follows the system Fact semantics:

- `value`;
- epistemic `state`;
- supplied evidence or basis references;
- `note` when uncertainty or inference requires explanation.

Do not create another epistemic vocabulary.

Do not produce numeric confidence scores.

### 4. Apply epistemic discipline

Use only these states when applicable:

- `VERIFIED`;
- `OBSERVED`;
- `INFERRED`;
- `UNKNOWN`;
- `NOT_COLLECTED`;
- `NOT_APPLICABLE`.

Do not promote a value because it is plausible.

For `INFERRED`, explain the inferential step.

For `UNKNOWN`, explain what was attempted when that information is supplied.

Do not turn a missing value into an assertion of absence.

Do not use one inference as substantiation for another fact.

When evidence cannot support a stronger state, preserve the weaker state.

### 5. Build the Brand Snapshot

Apply the same evidence discipline to:

- positioning;
- category context;
- claims made publicly;
- tone of voice;
- proof assets;
- official channels;
- known disputes.

Brand familiarity or category convention is not evidence.

Brand Snapshot remains part of Product Truth.

### 6. Preserve conflicts

When supplied evidence conflicts, do not silently choose one side.

Return:

- the competing supported statements;
- the nature of the conflict;
- what additional evidence could resolve it.

Do not determine canonical claim status.

### 7. Surface precise gaps

Return specific unresolved fields and evidence needs.

Prefer:

`ingredient concentration remains UNKNOWN`

over:

`product information is incomplete`.

Do not compute the coverage vector.

## Output Contract

Return semantic content only:

1. Product facts grouped by Product Truth dimension.
2. Brand Snapshot facts using the same Fact semantics.
3. Supplied evidence associations.
4. Explicit unresolved fields.
5. Notes for every inference.
6. Material evidence conflicts.
7. Concrete requests for additional evidence.

Do not return:

- canonical IDs;
- hashes;
- canonical versions;
- persisted artefacts;
- Evidence Ledger records;
- coverage calculations;
- claim-freedom tiers;
- permitted claim territories;
- Gate 1 decisions.

## Handoffs

After this Skill returns, orchestration and deterministic services own:

1. model-output validation;
2. canonical evidence-reference resolution;
3. Evidence Ledger writes;
4. Product Truth completeness computation;
5. claim-freedom resolution;
6. Gate 1 preparation.

When more visual or web evidence is needed, report the evidence need.

Do not invoke the capability yourself.

## Failure & Uncertainty

Remain conservative when:

- the product cannot be identified;
- several products or brands plausibly match;
- visible text is illegible;
- supplied sources conflict materially;
- a requested field has no evidentiary basis;
- a category-specific field cannot be interpreted from supplied context;
- a label statement cannot be distinguished from verified truth.

Valid outcomes include:

- `UNKNOWN`;
- `NOT_COLLECTED`;
- explicit conflict;
- evidence request;
- inability to establish identity.

A sparse Product Truth is preferable to an invented complete one.

## Boundaries

This Skill owns:

- Product Truth fact reasoning;
- Brand Snapshot reasoning;
- epistemic classification of proposed facts;
- conservative sparse-input reasoning;
- uncertainty and conflict reporting.

This Skill does not own:

- image-analysis capability;
- web-search capability;
- source-quality policy;
- persistence;
- canonical ID or version allocation;
- coverage computation;
- claim-freedom computation;
- compliance rules;
- Gate 1 approval;
- Chile market research;
- audience modelling;
- hypothesis generation;
- creative strategy;
- script writing.

If a task requires one of those responsibilities, hand it back to
orchestration or the owning component.
