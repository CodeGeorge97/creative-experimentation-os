---
knowledge_id: KNW-schwartz-integration
tier: DESIGN_INPUT
source_files: []
derivation_method: authored
derivation_confidence: OBSERVED
machine_verifiable: false
human_reviewed: true
scope: general
retrieval_policy: excluded
contains_claims: none
version: 1
created_at: "2026-09-05"
---
# Schwartz Integration Map
## How the two Schwartz knowledge layers connect to Creative Experimentation OS — Chile

---

## 1. Architecture decision

Do **not** create one monolithic `schwartz-skill`.

Create two reusable knowledge layers:

```text
SCHWARTZ PERSUASION FRAMEWORK
    “What argument should this ad make?”

SCHWARTZ LANGUAGE ENGINE
    “How should that argument be expressed clearly?”
```

They are consumed by existing Skills and orchestration steps.

---

## 2. Full pipeline

```text
PRODUCT IMAGE + BRAND
        ↓
PRODUCT INTELLIGENCE
        ↓
PRODUCT TRUTH + EVIDENCE LEDGER
        ↓
MARKET INTELLIGENCE CHILE
        ↓
OBSERVATIONS + CUSTOMER LANGUAGE
        ↓
AUDIENCE MODEL
        ↓
MASS DESIRE / AWARENESS / SOPHISTICATION
        ↓
BELIEF + IDENTIFICATION MAP
        ↓
20–30 CREATIVE HYPOTHESES
        ↓
ANGLE SCORING + DIVERSITY
        ↓
EXPERIMENT DESIGN
        ↓
FORMAT + NARRATIVE + STYLE
        ↓
SCHWARTZ PERSUASION PASS
        ↓
FIRST FULL SCRIPT
        ↓
BRILLIANCE LANGUAGE PASS
        ↓
CHILE LOCALIZATION
        ↓
SPOKEN NATURALNESS
        ↓
CREATIVE QA + COMPLIANCE
        ↓
PRODUCTION PACKAGE
```

---

## 3. Which component uses what

| OS component | Breakthrough Advertising | Brilliance Breakthrough |
|---|---|---|
| Product Intelligence | product performance / mechanism questions | none/minimal |
| Market Intelligence CL | mass desire, awareness, sophistication | customer language examples only |
| Audience Model | desire, identification, belief | none |
| Creative Strategist | major input | minor |
| Experiment Designer | competing persuasion hypotheses | language-variable tests when relevant |
| Hook System | awareness, sophistication, desire, belief entry | clarity, punch, implication |
| Script Engine | gradualization, mechanism, proof, intensification | sentence construction, flow, simplicity |
| Style Intelligence | identification, native-format credibility | visual/language rhythm interaction |
| Video Director | mechanism visualization, intensification | script-to-visual translation |
| Chile Localizer | preserve strategic function | preserve clarity while localizing |
| Compliance | reject unsupported claims/reframes | ambiguity audit |
| Performance Analyst | analyze by awareness/angle/mechanism/belief | analyze copy structure only as contextual variable |

---

## 4. Precedence / conflict resolution

If Schwartz suggests a stronger claim but the Evidence Ledger does not support it:

**Evidence wins.**

If a language rewrite sounds more memorable but changes the claim:

**Original verified meaning wins.**

If historical Schwartz examples conflict with current Meta policy:

**Current policy wins.**

If Schwartz suggests a category strategy but controlled account data repeatedly contradicts it:

**Account evidence wins**, while the framework may remain an exploration hypothesis.

---

## 5. New structured objects to add to V1

### A. `persuasion_context`

```json
{
  "mass_desire": "",
  "mass_desire_evidence_ids": [],
  "awareness_state": "",
  "awareness_confidence": 0.0,
  "sophistication_stage": 0,
  "sophistication_confidence": 0.0,
  "current_belief": "",
  "desired_belief": "",
  "identification_opportunity": "",
  "reason_to_believe": "",
  "mechanism_id": null
}
```

### B. `belief_bridge`

```json
{
  "starting_beliefs": [],
  "steps": [],
  "target_belief": "",
  "evidence_ids": [],
  "contradiction_risk": 0.0
}
```

### C. `language_quality`

```json
{
  "first_pass_comprehension": 0,
  "concreteness": 0,
  "mental_visualization": 0,
  "relationship_clarity": 0,
  "ambiguity_risk": 0,
  "concept_density": 0,
  "spoken_naturalness": 0,
  "rhythm": 0,
  "transition_quality": 0,
  "monotony_risk": 0,
  "caption_readability": 0,
  "visual_translation_potential": 0
}
```

### D. `persuasion_beat`

```json
{
  "beat_id": "B01",
  "function": "belief_bridge",
  "script_lines": [],
  "evidence_ids": [],
  "expected_viewer_reaction": ""
}
```

---

## 6. Updated complete script object

```yaml
creative_id: string
concept_id: string
experiment_id: string

strategy:
  audience_segment_id: string
  awareness_state: string
  sophistication_stage: integer
  mass_desire: string
  angle: string
  psychological_hypothesis: string
  current_belief: string
  desired_belief: string
  reason_to_believe: string

execution:
  format: UGC | PODCAST | ANIMATION
  narrative_pattern: string
  style_id: string
  voice_id: string
  duration_target: float

hook:
  strategy: string
  awareness_fit: float
  sophistication_fit: float
  copy: string
  visual: string
  audio: string

script:
  full_dialogue_or_voiceover: string
  persuasion_beats: []
  scenes: []

language_quality:
  first_pass_comprehension: integer
  concreteness: integer
  mental_visualization: integer
  ambiguity_risk: integer
  spoken_naturalness: integer
  transition_quality: integer

validation:
  product_truth: PASS | FAIL
  evidence: PASS | FAIL
  chile_naturalness: PASS | REVISE
  creative_qa: PASS | REVISE | BLOCK
  compliance: LOW | MEDIUM | HIGH | BLOCK
```

---

## 7. Updated Script Quality Gate

### Strategy
- Desire Alignment
- Awareness Alignment
- Sophistication Alignment
- Belief Alignment
- Identification Evidence
- Reason to Believe
- Mechanism Evidence
- Angle Alignment

### Copy / comprehension
- Hook Strength
- First-Pass Comprehension
- Specificity
- Concreteness
- Mental Visualization
- Relationship Clarity
- Sentence Clarity
- Momentum
- Rhythm
- Transition Quality
- Ambiguity Risk

### Spoken/local
- Spoken Naturalness
- Chile Naturalness
- Segment Fit
- Format Fit

### Production
- Visual Potential
- Script-to-Visual Translation
- Style Fit
- Production Feasibility

### Safety
- Product Truth
- Claim Evidence
- Comparison Support
- Compliance Risk

---

## 8. Updated 10-ad batch logic

The two books should **increase diversity**, not make all ten ads use the same “Schwartz formula.”

Example allocation logic:

```text
C01 — Problem Aware / identification entry / UGC
C02 — Solution Aware / failed alternatives / UGC
C03 — Solution Aware / mechanism / Animation
C04 — Product Aware / objection redefinition / UGC
C05 — Problem Aware / future-result intensification / UGC
C06 — High sophistication / belief reversal / Podcast
C07 — Product Aware / concentration-comparison / Podcast
C08 — Solution Aware / mechanism visualization / Animation
C09 — Problem Aware / visual metaphor / Animation
C10 — Most Aware / proof + offer / UGC
```

This is an example of diversity dimensions, not a fixed recipe.

---

## 9. How the books should affect experimentation

Store which framework element was used in the Creative DNA:

```yaml
schwartz_features:
  awareness_strategy: problem_aware
  sophistication_strategy: mechanism
  desire_strategy: intensification
  identification_strategy: none
  belief_strategy: gradualization
  redefinition_strategy: objection_flip
  mechanism_depth: moderate
  concentration_strategy: none
  native_format_strategy: ugc_native

language_features:
  concrete_language: high
  implication: low
  sentence_variation: medium
  visualizable_copy: high
```

Later performance analysis can ask:

- Did mechanism-led concepts outperform direct-promise concepts in this product/category?
- Did Problem-Aware hooks retain better than Product-Aware hooks?
- Did high-concreteness scripts outperform abstract scripts?

Do **not** conclude causality unless the experiment isolated the variable.

---

## 10. Required changes to candidate Skills

### `market-intelligence-cl`
Add outputs:
- mass desires
- awareness evidence
- sophistication evidence
- current beliefs
- identity language

### `creative-strategist`
Add:
- persuasion_context
- belief_bridge
- reason_to_believe
- mechanism depth decision

### `experiment-designer`
Add:
- awareness hypothesis
- belief framing hypothesis
- mechanism-depth hypothesis
- language clarity tests only when controlled

### `video-director`
Add:
- persuasion beats
- proof placement
- mechanism visualization
- concrete copy → shot mapping

### `chile-localizer`
Add hard constraint:
- preserve persuasion function and factual strength during localization

### `compliance-reviewer`
Add:
- redefinition deception check
- implication-as-hidden-claim check
- ambiguity check
- native-format impersonation check

### `performance-analyst`
Add fields from `schwartz_features` and `language_features` to Creative DNA joins.

---

## 11. What should remain outside the V1-Core

Do not add a giant external “psychology database” simply because these books expand the frameworks.

V1 should focus on:

- research
- evidence
- structured persuasion
- complete scripts
- language quality
- production readiness

Context/news intelligence remains later.

---

## 12. Implementation order

1. Add `persuasion_context` schema.
2. Add `belief_bridge` schema.
3. Update Creative Concept schema.
4. Update Script schema with persuasion beats.
5. Add `language_quality` schema.
6. Add Schwartz Strategy Pass to `creative-strategist` / script orchestration.
7. Add Brilliance Language Pass after first draft.
8. Update Chile Localizer invariants.
9. Update Creative QA.
10. Update Creative DNA for future performance learning.

---

## 13. Final architectural conclusion

The system should not become “more psychological” in a vague sense.

It should become **more explicit about four separate things**:

1. **Market reality** — what people already want, know and believe.
2. **Persuasion architecture** — how the concept bridges that reality to the product.
3. **Language engineering** — how the argument is made easy to hear, picture and remember.
4. **Experimentation** — whether those choices actually improve performance.

That separation keeps the Creative Experimentation OS rigorous instead of turning it into a collection of copywriting tricks.
