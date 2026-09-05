# PHASE 3A — REPOSITORY & MIGRATION DESIGN
## Creative Experimentation OS — Chile

**Date:** 2026-09-04
**Revision:** 2 — external audit correction pass applied (see **§AI**). Twelve corrections raised, twelve accepted.
**Status:** Repository architecture and migration **design only**. No file moved, renamed, deleted or quarantined. No knowledge or source file modified. No Skill created. No code, no Pydantic models, no schemas, no SQLite database, no dependencies installed, no Higgsfield or Meta integration, no production data.
**Predecessors, both treated as FROZEN:** `docs/PHASE_1_SYSTEM_DESIGN.md` (Revision 2) · `docs/PHASE_2_DATA_ARCHITECTURE.md` (Revision 3, frozen at commit `59cbe49`).
**Historical source:** `PRE_FLIGHT_AUDIT.md` — read, not modified, not moved.
**Authorisation:** Phase 3A only. Phase 3B (migration execution) is **not** authorised and has not begun. Phase 4 has not begun.

**Language note:** written in English because the required section headers are in English, matching Phases 1 and 2. The *system* produces Spanish (`es-CL`) output.

**Reading order for the impatient:** §A (verdict) → §D (the tree) → §F–§I (the canonical store) → §W (tracked/ignored) → §Y (migration map) → §AG (what needs your approval) → §AI (what the audit changed).

---

## A. Executive Repository Verdict

### Is the frozen data architecture expressible as a repository one operator can maintain?

**Yes, and it needs fewer boundaries than the object count suggests.** Phase 2 carries 8 artefact types, 20 entity types, 19 identifiers, 9 config registries, 22 projection objects and 4 event logs. That inventory does *not* imply 20 directories. It implies **four allocation scopes** (product, campaign, run, global), **three storage regimes**, and **one axis that decides everything else: who writes the file, and can it be rebuilt.**

The proposed repository has **12 top-level directories**, of which **9 exist after Phase 3B** and 3 are reserved names created by the phases that own them (`.claude/` in Phase 4, `src/` and `tests/` in Phase 5).

### The four decisions that carry this design

**1. Top-level boundaries are drawn by write authority and rebuildability, never by domain noun.** There is no `claims/`, no `observations/`, no `creatives/` at the top level. A reader learns the repository by learning three questions: *does a human author it* (`config/`, `knowledge/`, `sources/`, `docs/`), *does the runtime write it as truth* (`store/`, `media/`), or *can it be thrown away and regenerated* (`var/`, `reviews/`)? Everything else is a consequence.

**2. `store/` is organised by allocation scope, and the scopes are Phase 2's, not invented here.** Its five children — `brands/`, `products/`, `campaigns/`, `runs/`, `assets/` — are exactly the scopes in which Phase 2 allocates ordinals and logs events. This makes the single-writer-per-`(namespace, scope)` constraint of §E.1.1 a *visible* property of the filesystem — a scope is a directory — rather than a rule someone must remember. It also avoids the directory-per-noun architecture the brief forbids: hypotheses, concepts, insights and observations get no directory because Phase 2 embeds or ledger-scopes them.

**3. The source manifest is every file under `store/` and `config/`, and both roots hold canonical files only.** Phase 2 §AA hashes a manifest of stable relative paths, and an exception list is exactly what makes such a rule rot. Revision 1 kept derived Markdown renders inside `store/` and paid for it with a requirement — *the renderer must be pure, or staleness becomes meaningless.* The audit was right that this is the wrong trade: a renderer upgrade would mark the index stale with no canonical data changed. Renders now live in a top-level `reviews/`, git-tracked as Phase 2 §G.7 requires and **outside the manifest**. The purity requirement survives as a reproducibility property of the renderer; it is no longer load-bearing for index staleness (§Q.3, REPO_ADR-019 revised).

**4. Every canonical path is a total function of identifiers.** `store/campaigns/CMP-acme-3f8b21/creatives/CRE-acme-3f8b21-07/v3.json` contains no human-chosen label, so **no canonical file ever needs renaming** and a rename can therefore never change domain identity. Where a path *does* carry meaning it is stated as a deliberate, narrow exception with in-file metadata behind it (§X.3), and there are exactly two.

### What this design refuses to do

- **No directory per entity type.** Twenty entity types, five scope directories.
- **No second home for any fact.** Narrative patterns live in `config/narrative_library.yaml` and nowhere else; Phase 1's proposed `knowledge/narrative/` is not created. The Chilean customer-language corpus is `OBSERVATION` records in the Evidence Ledger, not a knowledge directory; Phase 1's `knowledge/language/cl/` is not created. Source snapshots are `SOURCE_SNAPSHOT` assets under `media/`; Phase 1's `sources/external/` is not created. Three directories deleted from the design by reading Phase 2 (§AE, REPO_ADR-014, REPO_ADR-015).
- **No empty tree built on speculation.** `src/`, `tests/`, `tests/golden/<category>/` and `.claude/skills/` are *named* here and *created* by the phase that fills them.
- **No file identity.** A filename is a rendering of an identifier, never the source of one. The index builder reads the id from the file's content, and a path/content mismatch is an integrity failure (§AB check 14).
- **No history rewrite as a migration mechanism.** The 136 MB of media already in git history stays there. Rollback to the frozen Phase 2 commit is the safety net, and rewriting history destroys the safety net to save disk (REPO_ADR-017).

### The three risks this layout does not eliminate

1. **Media payloads become the only unbacked data in the system.** Phase 2 §AI.1 requires payloads to be git-ignored, and this design honours it. The consequence, stated plainly rather than buried: once `media/` is ignored, a new generated video exists in exactly one place on one machine. The registry knows its hash and can *detect* the loss; nothing prevents it. Mitigation is operator discipline plus a `media check` command, and that is not the same as a backup (§AD R1).
2. **Line-ending drift silently invalidates every config hash on a second computer.** Phase 2 §G.7 hashes authored YAML **over file bytes**. This machine has `core.autocrlf=true`; the current worktree happens to be LF, but a fresh clone on a second Windows machine would check out CRLF and produce different hashes for byte-identical policy. `.gitattributes` with `eol=lf` fixes it and is the single highest-value file in this migration (§AD R3, REPO_ADR-024).
3. **A placeholder registry reads as authored policy.** An empty `deny_list.yaml` blocks nothing. Mitigated by making placeholders fail closed (REPO_ADR-010), not by trusting that someone remembers to fill them in.

---

## B. Current Repository Inventory

Gathered read-only on 2026-09-04 from the working tree at `master` / `59cbe49`. **Nothing was mutated.** The PRE_FLIGHT inventory was not assumed current; this is a fresh enumeration.

### B.1 Current tree — meaningful entries only

```
creative-experimentation-os/                    32 tracked files · 142 MB worktree · 137 MB .git
├── PRE_FLIGHT_AUDIT.md                         22.6 KB   immutable historical snapshot
├── README.md                                    1.0 KB   describes a structure it calls "temporal"
├── docs/
│   ├── PHASE_1_SYSTEM_DESIGN.md               151.4 KB   frozen
│   └── PHASE_2_DATA_ARCHITECTURE.md           330.2 KB   frozen
├── knowledge/
│   ├── copywriting/schwartz/
│   │   ├── schwartz_persuasion_framework.md    22.3 KB   ← W1 RESOLVED, correct location
│   │   ├── schwartz_language_engine.md         17.5 KB
│   │   └── schwartz_integration_map.md          9.9 KB
│   └── methodology/                                      ← MISPLACED: raw + derived, all unverifiable
│       ├── modulo-1-estrategia-mercado.md      15.0 KB
│       ├── modulo-2-psicologia-persuasion.md   13.0 KB   ← git classifies as `-text` (see B.5)
│       ├── modulo-3-anuncios-estaticos.md      11.3 KB
│       ├── modulo-4-ugc-vsl-strategy.md        17.8 KB
│       ├── modulo-5-infraestructura-herramientas (1).md
│       │                                       13.0 KB   ← download artefact " (1)" in the name
│       ├── Dominio del Post ID_ ….pdf          99.2 KB   ← Google Docs export
│       ├── Escalamiento Creativo ….pdf         95.4 KB   ← Google Docs export
│       └── Metodología Evolve ….pdf            92.5 KB   ← Google Docs export, non-ASCII filename
├── samples/                                    132 MB    15 media files, all REFERENCE (Phase 2 §S.4)
│   ├── style-references/animation/ (3 × mp4)   29.7 MB
│   ├── style-references/podcast/   (3 × mp4)   18.0 MB
│   ├── style-references/ugc/       (3 × mp4)   44.9 MB
│   ├── voices/chile/female/         (3 × wav)  43.9 MB
│   └── voices/chile/male/           (3 × mp3)   1.4 MB   ← ssstik.io_*, `no_cloning_source`
└── sources/
    ├── original-books/
    │   ├── breakthrough-advertising-0887232981-9780887232985 (1)_compressed.pdf   2.7 MB
    │   └── _OceanofPDF.com_The_brilliance_breakthrough_-_Eugene_schwartz.pdf      6.3 MB
    └── methodology/                            EMPTY — untracked, git holds no empty directories
```

### B.2 Tracked vs untracked

| | Count | Notes |
|---|---|---|
| Tracked files | **32** | `git ls-files` |
| Files on disk | **32** | identical set — the worktree is clean, `git status` empty |
| Untracked files | **0** | |
| Empty directories | **1** | `sources/methodology/` — exists on disk, invisible to git |
| Generated files | **0** | nothing derived exists yet |
| `.gitignore` | **absent** | nothing is currently ignored |
| `.gitattributes` | **absent** | line endings and binary classification are left to heuristics |

### B.3 Binary-heavy content

| Class | Files | Bytes | Largest single file |
|---|---|---|---|
| Sample video (`.mp4`) | 9 | 92.6 MB | 18.3 MB |
| Sample audio (`.wav`, `.mp3`) | 6 | 45.3 MB | 18.3 MB |
| Book PDFs | 2 | 9.0 MB | 6.3 MB |
| Methodology PDFs | 3 | 0.29 MB | 99 KB |
| **Total binary** | **20** | **≈ 147 MB on disk (132 MB media + 9 MB books)** | |

All 15 media files were committed in the baseline commit `92ec3eb` and are therefore **already in git history**. `.git` is 136 MB of loose objects (never packed). No file exceeds GitHub's 100 MB hard limit or its 50 MB warning threshold, so the repository is pushable as-is; a `git gc` before the first push would compact the loose objects.

### B.4 Findings that change the design

| # | Finding | Consequence |
|---|---|---|
| 1 | **The three methodology PDFs are Google Docs exports** (`/Producer (Skia/PDF m154 Google Docs Renderer)`), not scans of published works | They are *not* raw upstream sources. They belong with the Markdown modules in quarantine, not in `sources/`. This settles the brief's §12 question about separating original PDFs from structured derivatives: **there is no original to separate** (REPO_ADR-013). |
| 2 | `core.autocrlf=true`, no `.gitattributes` | Latent cross-machine hash break for authored YAML, whose hash is taken over file bytes (§AD R3). |
| 3 | `core.ignorecase=true`, `core.symlinks=false` | Case-only path distinctions and symlink-based layouts are unavailable. Design accordingly (§AC). |
| 4 | 15 media files already in history at `92ec3eb` | Untracking them going forward does **not** delete them; `git checkout 92ec3eb -- samples/` recovers any of them. This removes the strongest objection to ignoring `media/` (§AD R1). |
| 5 | `git-lfs 3.7.1` is installed on this machine but **not configured in this repository** | No LFS assumption is made. The design stays LFS-compatible without requiring it (§O.6). |
| 6 | Python resolves only to the Windows Store stub; `ffmpeg` and `sqlite3` CLI are absent | Confirms Phase 1 PRE-01 still holds. **Every Phase 3B command in this document uses only `git`, `sha256sum` and POSIX shell**, all verified present. |
| 7 | 14 tracked paths contain spaces or parentheses; 1 contains a non-ASCII character (`Metodología`) | Tolerable but quoted everywhere in the migration commands (§Z). |
| 8 | Longest tracked relative path is 91 characters | Comfortable headroom under Windows `MAX_PATH`; a design budget is set at 120 (§AC). |
| 9 | `README.md` describes a "temporary" structure and states the project contains "no architecture design, Skills, or any Phase" | Factually stale since Phase 1. Rewriting it is a migration item, not cosmetics (§Y op 20). |

### B.5 One unexplained anomaly, recorded rather than guessed

`git ls-files --eol` reports `i/-text w/-text` for `knowledge/methodology/modulo-2-psicologia-persuasion.md` — git classifies it as non-text — while the other four modules report `i/lf w/lf`. The file was checked and is **valid UTF-8, contains zero NUL bytes, and uses LF endings**, so the usual causes do not apply. The cause is not established and is not worth establishing: an explicit `.gitattributes` entry (`*.md text eol=lf`) removes the heuristic from the picture entirely and makes the classification deterministic on every machine. Recorded here so that a future reader does not rediscover it as a mystery.

---

## C. Repository Design Principles

The repository-layer expression of Phase 1 §C and Phase 2 §B. Where a frozen principle already covers it, the reference is given rather than restated.

**RP1 — A top-level directory exists only if it answers "who writes this, and can it be rebuilt" differently from every other top-level directory.** Domain nouns do not earn directories; write authority and rebuildability do.

**RP2 — Every canonical path is a total function of identifiers.** No canonical path contains a title, a date, a version label chosen by a human, or a description. A path is therefore never renamed, and identity is never at risk from a rename (Phase 2 P6).

**RP3 — A filename is not an identifier.** The identifier lives inside the file. The path renders it for human navigation and for cheap enumeration. Any disagreement between the two is an integrity failure, and the file wins.

**RP4 — The canonical root is exactly what the rebuild enumerates.** `store/` and `config/` are the source manifest, with no exception list. Anything that must not be in the manifest must not be under those roots.

**RP5 — Derived and canonical never share a directory unless the derived thing is provably pure.** A derived render lives beside its scope only because a pure renderer makes it indistinguishable from canonical for hashing purposes; anything impure lives in `var/`.

**RP6 — If it has an `ASSET_ID`, it lives in `media/`. If it does not, it lives in `var/`.** This single rule separates registered payloads from generation scratch, working clips, caches and exports, and it needs no judgement call at write time.

**RP7 — Nothing ignored may be the only copy of a canonical *record*.** Payloads are the sole, explicit, approved exception, and they are exception enough that they get their own risk entry, their own check command and their own approval item.

**RP8 — Paths carry identity, never authority.** Where a path does carry policy — the quarantine directory and the two ingestion entry points — the policy is duplicated in in-file metadata, so the path is a convenience and a second line of defence, never the source of truth (§X.3).

**RP9 — A version is never overwritten, and the filesystem enforces it.** Writing artefact version *n* is a create-exclusive operation on a path that must not already exist. "Immutability on write" (Phase 2 P5) becomes an `O_CREAT|O_EXCL` failure rather than a code review.

**RP10 — Every path is relative and portable.** No canonical record contains an absolute path, a drive letter or a machine name. The media root is resolvable by configuration; everything else is repo-relative (§AC).

**RP11 — Reserve names, create directories.** A directory is created by the phase that puts a file in it. Empty scaffolding is a promise the repository cannot keep.

**RP12 — A structural constraint that can be expressed as a filesystem check should be.** "Exactly nine config registries" is `ls config/*.yaml | wc -l`. "No canonical file is ignored" is `git check-ignore`. Turning invariants into one-line commands is most of what a repository layout is *for*.

---

## D. Proposed Final V1 Tree

Directories marked **[Phase N]** are reserved names, not created by Phase 3B.

```
creative-experimentation-os/
│
├── .gitattributes                  line endings, binary classification      [tracked]
├── .gitignore                      root ignore rules                        [tracked]
├── .env.example                    credential names, never values           [tracked]
├── README.md                       what this repository is, rewritten       [tracked]
├── PRE_FLIGHT_AUDIT.md             immutable historical snapshot — DO NOT MOVE, DO NOT EDIT
│
├── docs/                           phase documents + operator documentation
│   ├── PHASE_1_SYSTEM_DESIGN.md            frozen
│   ├── PHASE_2_DATA_ARCHITECTURE.md        frozen
│   ├── PHASE_3_REPOSITORY_MIGRATION_DESIGN.md   this document
│   └── MIGRATIONS.md               append-only record of every path move     [new, Phase 3B]
│
├── config/                         THE NINE AUTHORED POLICY REGISTRIES — canonical
│   ├── evidence_policy.yaml                1
│   ├── deny_list.yaml                      2
│   ├── narrative_library.yaml              3
│   ├── format_profiles.yaml                4
│   ├── category_profiles.yaml              5
│   ├── creative_taxonomy.yaml              6
│   ├── experiment_variables.yaml           7
│   ├── diversity_targets.yaml              8
│   ├── tool_capability.yaml                9   ← exactly nine *.yaml at this level
│   ├── styles/                     authored registry entities, NOT a tenth registry
│   │   └── STY-<format>-<slug>.yaml        3 profiles, Phase 1 ADR-012
│   └── README.md                   the closed-list rule, stated where it is enforced
│
├── knowledge/                      DERIVED, PROVENANCE-TAGGED, RETRIEVABLE
│   ├── copywriting/schwartz/       ← W1 RESOLVED; not moved, not modified in Phase 3A
│   │   ├── schwartz_persuasion_framework.md
│   │   ├── schwartz_language_engine.md
│   │   └── schwartz_integration_map.md
│   └── _quarantine/                RESTRICTED RETRIEVAL — see README
│       ├── README.md               retrieval policy, in the directory it governs
│       └── methodology/            8 files, moved unmodified from knowledge/methodology/
│
├── sources/                        RAW, IMMUTABLE, NEVER EDITED
│   └── books/
│       ├── breakthrough-advertising.pdf
│       └── brilliance-breakthrough.pdf
│
├── store/                          ★ CANONICAL DATA ROOT — the system of record
│   ├── README.md
│   ├── brands/                     BRD-<slug>.json
│   ├── products/                   PRD-<brand>-<slug>/   … product scope
│   ├── campaigns/                  CMP-<brand>-<6hex>/   … campaign scope
│   ├── runs/                       RUN-<utc>-<6hex>/     … run scope
│   └── assets/                     AST-<12hex>.json      … global scope
│
├── media/                          BINARY PAYLOADS — git-ignored
│   ├── .gitignore                  ignore everything but itself and README   [tracked]
│   ├── README.md                                                             [tracked]
│   ├── <2hex>/AST-<12hex>.<ext>    registered payloads, id-addressed
│   └── _unregistered/              repository-origin files awaiting registration
│
├── incoming/                       INGESTION BOUNDARY — git-ignored
│   ├── .gitignore                                                            [tracked]
│   └── README.md                   how to drop a file without knowing any id [tracked]
│
├── var/                            DERIVED / REBUILDABLE / EPHEMERAL — git-ignored
│   ├── .gitignore                                                            [tracked]
│   ├── index/                      SQLite + wal/shm — rebuildable
│   ├── schemas/                    generated JSON Schema — regenerated
│   ├── cache/  tmp/  work/  logs/  exports/
│   └── README.md                                                             [tracked]
│
├── .claude/                        DEVELOPMENT ENVIRONMENT + SKILLS      [Phase 4]
│   └── skills/<skill-name>/SKILL.md            5 Skills, Phase 1 §E
│
├── src/                            FUTURE PYTHON CODE                    [Phase 5]
│   └── creative_os/{domain,validation,services,store,index,orchestrator,adapters,prompts,cli}/
│
└── tests/                          FUTURE TESTS                          [Phase 5+]
    └── {unit,integration,invariants,golden}/
```

**Eleven top-level directories.** Eight exist after Phase 3B (`docs`, `config`, `knowledge`, `sources`, `store`, `media`, `incoming`, `var`); three are reserved (`.claude`, `src`, `tests`).

---

## E. Top-Level Directory Responsibilities

| Directory | Purpose | Canonical? | Git tracked? | Owner (who writes it) | Examples |
|---|---|---|---|---|---|
| `docs/` | Phase documents, migration log, operator documentation | No — documentation about the system, not system data | **Yes** | Human (phases) | `PHASE_2_DATA_ARCHITECTURE.md`, `MIGRATIONS.md` |
| `config/` | The nine policy registries (§B.1 of Phase 2) plus authored registry entities | **Yes** — hashed into every run and every artefact's `inputs[]` | **Yes** | Human author, reviewed | `evidence_policy.yaml`, `styles/STY-ugc-raw-handheld.yaml` |
| `knowledge/` | Structured, derived, provenance-tagged knowledge retrieved into prompts | **Yes** — a knowledge file is a `KNOWLEDGE_ID` entity, hashed into the run head | **Yes** | Human author / a derivation pass, then human review | `schwartz_persuasion_framework.md`, `_quarantine/methodology/**` |
| `sources/` | Raw, immutable upstream documents. Never edited, never derived-in-place | No — provenance, not knowledge. Referenced by `source_files[]` | **Yes** | Human, by deposit | `books/breakthrough-advertising.pdf` |
| `store/` | **The canonical data root.** Every artefact version, entity record and event log | **Yes — this is the system of record** | **Yes** | Runtime (orchestrator) only; a human edits it only to repair, and the repair is visible in a diff | `campaigns/CMP-…/creatives/CRE-…-07/v3.json` |
| `media/` | Binary payloads for registered assets, plus files awaiting registration | No — the **Asset Registry record** is canonical; the payload is referenced | **No** | Runtime (ingestion, generation); operator via `incoming/` | `7b/AST-7b31e0c9d4a2.mp4` |
| `incoming/` | The one place an operator drops a file without knowing any identifier | No | **No** (directory tracked, contents ignored) | Operator | a product photo, a licence PDF |
| `var/` | Everything derived, rebuildable, cached, temporary or exported | No — **deleting it must cost only time** | **No** | Runtime | `index/creative_os.sqlite3`, `work/`, `exports/` |
| `.claude/` | Claude Code project configuration and the five Skills | No | **Yes** (except local settings) | Human (Phase 4) | `skills/script-engine/SKILL.md` |
| `src/` | Python 3.12+ runtime: models, services, index builder, orchestrator, adapters, prompts | No | **Yes** | Human (Phase 5+) | `creative_os/domain/creative.py` |
| `tests/` | Unit, integration, invariant and golden tests | No | **Yes** | Human (Phase 5+) | `invariants/test_inv_117.py` |

**Why each one survives the simplification pass** is answered in §AE. Two entries deserve their justification here because they are the ones a reviewer will challenge:

- **`sources/` holds two files.** It stays because the raw/derived boundary is a frozen Phase 1 architectural decision (§I), because Phase 1's provenance schema declares that `source_files: []` *empty or unresolvable ⇒ cannot be VERIFIABLE* — so a stable, tracked, resolvable path is what makes the Schwartz knowledge's `DERIVED_VERIFIABLE` tier a checkable claim rather than an assertion — and because merging it into `knowledge/` would place raw material of unexamined provenance next to curated derivatives, which is the exact confusion the boundary exists to prevent.
- **`incoming/` holds nothing yet.** It stays because it is a *provenance declaration*, not a convenience: a file entering through `incoming/` is registered with `origin.kind: USER_UPLOAD` and therefore lands in `USER_PROVIDED_UNVERIFIED`, while a file already in the repository is registered with `origin.kind: REPOSITORY` and lands in `REFERENCE` (Phase 2 §S.2). Those are different rights positions. Collapsing the two entry points would make the fifteen existing samples enter as uploads and silently contradict Phase 2 §S.4 (§P.2).

---

## F. Canonical Data Root

### F.1 The name

| Candidate | Verdict |
|---|---|
| `data/` | **Rejected.** Accurate but undifferentiating: caches, exports and the SQLite index are all "data" too, and the whole design turns on the boundary between what is truth and what is rebuildable. A name that does not draw that line invites files across it. |
| `workspace/` | **Rejected.** Connotes scratch space — the opposite of an immutable system of record. |
| `canonical/` | **Rejected.** Precise but adjectival; it reads as a qualifier looking for a noun, and every path in the system would start with a word the operator has to translate. |
| **`store/`** | **Accepted.** Phase 1 §V calls it the *artefact store*; Phase 2 §A counts *canonical stores*. It is the vocabulary the frozen documents already use, it is short (5 characters, and it prefixes every canonical path), and "is it in the store?" is the exact question the design wants an operator to ask. |

### F.2 The shape — scope, not noun

Phase 2 gives four event-log scopes (product, asset/global, campaign, run) and, in §E.3, an allocation scope for every ordinal identifier. Those two lists agree, and their union is the natural shape of the store:

| `store/` child | Scope it materialises | What lives in it | Ordinals allocated in it |
|---|---|---|---|
| `brands/` | Global registry | `BRD-<slug>.json` immutable records | — (registry authority) |
| `products/` | **Product** | Product record, Product Truth versions, the entire Evidence Ledger, the `evidence` event log | `OBS`, `CLM` |
| `campaigns/` | **Campaign** | Six campaign artefacts, creatives, packages, gate decisions, renders, the `campaign` event log | `INS`, `HYP`, `CON`, `EXP`, `CRE`, `GAT` |
| `runs/` | **Run** | The immutable RUN head, the `run` event log | `EXT` |
| `assets/` | **Global** | Asset Registry records (metadata only), the `asset` event log | — (random authority) |

**This is not a directory per noun.** Twenty first-class entity types map onto five directories, because Phase 2 embeds most of them: insights live inside the Research Dossier, concepts and experiments inside the Experiment Plan, hypotheses inside the Hypothesis Pool, and hooks, segments, scenes and arms are fragment paths (Phase 2 §E.5). The store has a directory exactly where Phase 2 has a scope, and nowhere else.

**The single-writer constraint becomes legible.** Phase 2 §E.1.1 forbids concurrent writers to one `(namespace, scope)`. Under this layout a scope *is* a directory, so the constraint reads "one writer per campaign directory, one writer per product directory" — which an operator can hold in their head, and which Phase 5 can enforce with an advisory lock file at the scope root (`store/campaigns/CMP-…/.writer.lock`). Phase 2 §AJ.8.7 item 2 leaves the mechanism to Phase 5; this layout makes the cheapest mechanism available without mandating it.

### F.3 Full store layout

```
store/
├── README.md
│
├── brands/
│   └── BRD-acme.json                              immutable entity record
│
├── products/
│   └── PRD-acme-magnesio-500/
│       ├── product.json                           immutable entity record
│       ├── product_truth/
│       │   ├── v1.json                            versioned artefact
│       │   └── v2.json
│       ├── ledger/                                the Evidence Ledger, product-scoped
│       │   ├── sources/SRC-4f9a2c81d0b7.json
│       │   ├── extractions/EXT-a91c4e-012.json
│       │   ├── observations/OBS-magnesio-500-0042.json
│       │   └── claims/CLM-magnesio-500-0007.json
│       ├── reviews/                               derived Markdown, pure, tracked
│       │   └── product_truth_v2.md
│       └── events.jsonl                           ← the `evidence` log
│
├── campaigns/
│   └── CMP-acme-3f8b21/
│       ├── campaign_brief/v1.json
│       ├── research_dossier/{v1.json,v2.json}
│       ├── hypothesis_pool/v1.json
│       ├── experiment_plan/{v1.json,v2.json,v3.json}
│       ├── meta_test_plan/v1.json
│       ├── creatives/
│       │   └── CRE-acme-3f8b21-07/{v1.json,v2.json,v3.json}
│       ├── packages/
│       │   └── PKG-acme-3f8b21-07-v1/v1.json
│       ├── gates/
│       │   └── GAT-acme-3f8b21-003.json           immutable entity record
│       ├── reviews/
│       │   ├── experiment_plan_v3.md
│       │   └── package_PKG-acme-3f8b21-07-v1_v1.md
│       └── events.jsonl                           ← the `campaign` log
│
├── runs/
│   └── RUN-20260904T1132Z-a91c4e/
│       ├── run.json                               immutable RUN head (§W.1)
│       └── events.jsonl                           ← the `run` log
│
└── assets/
    ├── 7b/AST-7b31e0c9d4a2.json                   registry record — metadata only
    └── events.jsonl                               ← the `asset` log (global)
```

**The campaign has no `campaign.json`.** Phase 2 §G.1 lists the immutable entity records — Source, Evidence Extraction, Observation, Claim, Asset, Gate Decision, Run head, Brand, Product — and Campaign is not among them. A campaign is created by writing `campaign_brief/v1.json`, and its state folds from gate decision records (§G.0). Adding a `campaign.json` would be a creation record duplicating a fact the brief already carries — precisely the dual-write that Phase 2 Correction 11 removed. The directory's existence is not a record; the brief is.

**Assets are sharded, ledger records are not.** `AST-` suffixes are random hex, so the first two characters shard evenly and keep any one directory small as the registry grows into the thousands; `media/` uses the identical shard so a record and its payload share a folder name (`store/assets/7b/AST-7b31e0c9d4a2.json` ↔ `media/7b/AST-7b31e0c9d4a2.mp4`). Observations and claims are ordinal-named and product-scoped — Phase 2 §AD.7 projects ~61 and ~22 per campaign — so a flat directory is correct for V1 and sharding them would buy nothing.

### F.4 Where a scope-ordinal reads its `max`

Phase 2 §E.1.1 requires `max(existing ordinal in that entity namespace and scope) + 1`, computed **from the records that bear it**. Under this layout the source differs by namespace, and getting it wrong is the kind of bug that costs an ordinal collision, so it is tabulated rather than left to inference:

| Namespace | Scope | Existing ordinals are read from | Enumeration |
|---|---|---|---|
| `OBS` | product | `store/products/<PRD>/ledger/observations/` | filenames |
| `CLM` | product | `store/products/<PRD>/ledger/claims/` | filenames |
| `EXT` | run | `store/runs/<RUN>/…` and the ledger's `extractions/` | filenames |
| `GAT` | campaign | `store/campaigns/<CMP>/gates/` | filenames |
| `CRE` | campaign | `store/campaigns/<CMP>/creatives/` | directory names |
| `INS` | campaign | **every version** of `research_dossier/` | file contents |
| `HYP` | campaign | **every version** of `hypothesis_pool/` | file contents |
| `CON`, `EXP` | campaign | **every version** of `experiment_plan/` | file contents |

Two rules follow, and both are load-bearing:

1. **Every version, not the latest.** `HYP-acme-3f8b21-017` may appear in `hypothesis_pool/v1.json` and be absent from `v2.json`. INV-118 forbids reuse, so the allocator reads the union across all versions. Reading only `latest` would reissue a retired ordinal — and `latest` is explicitly non-authoritative anyway (Phase 2 §G.5, INV-12).
2. **The allocator reads canonical files, never SQLite.** SQLite is `INDEX_ONLY` and may be stale, missing or mid-rebuild (Phase 2 §AA.2: *a missing database is not an error*). An allocator that trusted the index would double-allocate against a stale one. This is the repository-layer statement of Phase 2 P13 and it belongs in Phase 5's code review checklist.

**Nothing in this table reads an event log.** That is Phase 2 §AI.1 item 3's explicit warning honoured structurally: `event_seq` numbers events and never numbers entities, and no ordinal's source of truth is a `.jsonl` file.

---

## G. Versioned Artefact Layout

### G.1 The convention

| Candidate | Verdict |
|---|---|
| `product_truth.v1.json`, `product_truth.v2.json` (flat) | **Rejected.** Shorter, but enumerating the versions of one artefact becomes a glob over a directory holding several artefact families, and "what is the highest version" becomes a parse of filenames rather than a directory read. It also invites a sibling `product_truth.json` meaning "latest" — a mutable file the design must not have. |
| `versions/2/product_truth.json` | **Rejected.** One more directory level per version for no gain; the artefact type is already fixed by its parent. |
| **`product_truth/v1.json`, `product_truth/v2.json`** | **Accepted.** |

**Every versioned artefact identity is a directory; every version is `v<n>.json` inside it.** Uniform for singleton-per-scope artefacts (Product Truth, Campaign Brief, Research Dossier, Hypothesis Pool, Experiment Plan, Meta Test Plan) and for per-instance artefacts (Creative Record, Production Package), which nest one level deeper under `creatives/<CREATIVE_ID>/` and `packages/<PACKAGE_ID>/`.

Three properties earn it:

1. **Version enumeration is a directory listing**, which is also how the next version number is computed — one mechanism, matching §F.4's "read what exists".
2. **"No file is silently overwritten" becomes a filesystem guarantee.** Writing version *n* is `open(path, 'xb')` — create-exclusive — on `…/v<n>.json`. If the path exists the write fails. Phase 2 P5 stops being a policy and becomes an `EEXIST` (RP9).
3. **Everything under an artefact directory is canonical.** Derived renders go to the scope's `reviews/`, never inside the artefact directory, so "is this file authoritative?" is answered by its parent directory alone.

### G.2 Addressing

Phase 2 §E.5's addresses map onto paths by a total function, with no lookup:

| Phase 2 address | Path |
|---|---|
| `PRD-acme-magnesio-500/product_truth@v2` | `store/products/PRD-acme-magnesio-500/product_truth/v2.json` |
| `CMP-acme-3f8b21/experiment_plan@v3` | `store/campaigns/CMP-acme-3f8b21/experiment_plan/v3.json` |
| `CRE-acme-3f8b21-07@v3` | `store/campaigns/CMP-acme-3f8b21/creatives/CRE-acme-3f8b21-07/v3.json` |
| `config/evidence_policy@v4` | `config/evidence_policy.yaml` **whose header declares `version: 4`** (§J.2) |

The creative address omits its campaign, which the path needs. `CREATIVE_ID` is `CRE-<campaign-suffix>-<NN>` and `CAMPAIGN_ID` is `CMP-<brand-slug>-<6 hex>`, so the campaign is recoverable from the creative id by construction — `CRE-acme-3f8b21-07` → `CMP-acme-3f8b21`. Stated explicitly because a resolver that scanned all campaigns to find a creative would be a silent O(n) mistake.

A **fragment reference** (`…@v3#hook.copy`) never touches the filesystem beyond the version file: everything after `#` is a path into the parsed JSON. No fragment ever becomes a path segment.

### G.3 The one legibility hazard, named

`PACKAGE_ID` is `PKG-<creative-suffix>-v<n>` where `<n>` is the **creative's** version (Phase 2 §E.1). The package is itself a versioned artefact. So a valid path is:

```
store/campaigns/CMP-acme-3f8b21/packages/PKG-acme-3f8b21-07-v1/v1.json
                                          └── creative version ──┘  └ package version
```

Two different `v1`s, adjacent. This is inherited from a frozen, pure-derived identifier and cannot be renamed away. The alternative — naming package version files something other than `v<n>.json` — would break the uniform convention everywhere else to fix legibility in one place. **Kept, and documented here and in `store/README.md`.**

---

## H. Immutable Entity Record Layout

One record, one file, path derived from the identifier, written once with create-exclusive semantics.

| Record | Path | Identifier authority |
|---|---|---|
| `BRAND` | `store/brands/BRD-<slug>.json` | Registry |
| `PRODUCT` | `store/products/PRD-<brand>-<slug>/product.json` | Registry |
| `SOURCE` | `store/products/<PRD>/ledger/sources/SRC-<12hex>.json` | Content-deterministic |
| `EVIDENCE_EXTRACTION` | `store/products/<PRD>/ledger/extractions/EXT-<run>-<NNN>.json` | Scope-ordinal (run) |
| `OBSERVATION` | `store/products/<PRD>/ledger/observations/OBS-<slug>-<NNNN>.json` | Scope-ordinal (product) |
| `CLAIM` | `store/products/<PRD>/ledger/claims/CLM-<slug>-<NNNN>.json` | Scope-ordinal (product) |
| `ASSET` | `store/assets/<2hex>/AST-<12hex>.json` | Random |
| `GATE_DECISION` | `store/campaigns/<CMP>/gates/GAT-<campaign>-<NNN>.json` | Scope-ordinal (campaign) |
| `RUN head` | `store/runs/RUN-<utc>-<6hex>/run.json` | Random |

Three points where the layout does real work:

- **The Evidence Ledger is a directory, not a file.** Phase 2 §J calls it *"one store of immutable records, scoped to the product"* holding four record types. `ledger/` with four subdirectories is that sentence as a path. It also makes ledger reuse across campaigns automatic: a second campaign on the same product reads the same directory, which is the behaviour Phase 2 §J intends and DATA_ADR-003 leaves open for a second market.
- **`EXTRACTION_ID` is run-scoped but the record lives under the product.** `EXT-a91c4e-012` is allocated within run `a91c4e` (Phase 2 §E.3) but describes evidence about a product and outlives the run, so it is stored with the ledger and the run reaches it through the `run_id` field it already carries. The allocation scope and the storage scope differ here, and only here; recorded so that neither is "corrected" into the other.
- **A record's ordinal is zero-padded exactly as Phase 2 formats it** (`OBS-…-0042`, `GAT-…-003`, `CRE-…-07`), so lexical filename order equals numeric order and a directory listing is already sorted. Padding widths are Phase 2's, not chosen here.

---

## I. Domain Event Log Layout

### I.1 Physical representation — audited

Four logs (Phase 2 §G.0), one physical file per log instance:

| Log | Scope | Path |
|---|---|---|
| `evidence` | per product | `store/products/<PRODUCT_ID>/events.jsonl` |
| `campaign` | per campaign | `store/campaigns/<CAMPAIGN_ID>/events.jsonl` |
| `run` | per run | `store/runs/<RUN_ID>/events.jsonl` |
| `asset` | global | `store/assets/events.jsonl` |

Audited against the brief's nine criteria. Volumes are Phase 2 §AD.7's projection for one campaign: ~25 evidence, ~3 asset, ~55 campaign, ~260 run events.

| Criterion | **JSONL (one line per event)** | One file per event | Verdict |
|---|---|---|---|
| **Append atomicity on Windows** | One `WriteFile` on a handle opened `FILE_APPEND_DATA` appends without a separate seek. A single line well under the sector/buffer size is atomic in practice, and under V1's single-writer constraint (INV-117) there is no second writer to interleave with. | Trivially atomic — a new file has no shared state. | **Even.** Neither format supplies the guarantee that matters; the single-writer constraint does. Honest statement: JSONL's atomicity is *adequate under V1's constraint*, not unconditional. |
| **Git diffs** | An append is a one-line addition. A whole campaign's history is one readable file. | An append is a new file. Diffs are clean but the changed-file count per commit grows without bound. | **JSONL.** |
| **Merge conflict risk** | Two clones appending to the same log conflict on the final line — **visibly**. | Two clones writing `000417.json` conflict; two clones writing uuid-named files **both land silently**, producing two events claiming the same position or an ambiguous order. | **JSONL, and this is the strongest argument.** Concurrent writing to one scope is already forbidden (INV-117). The right property for a forbidden operation is that it *fails loudly*. A silent merge is the worse outcome. |
| **Corruption recovery** | A torn final line fails to parse and is truncated; every earlier line is intact and independently parseable. | A torn file is one lost event and leaves a **gap** in `event_seq`, which is harder to distinguish from a bug in the writer. | **JSONL.** |
| **Human inspection** | `tail`, an editor, `grep`. One file. | 340 files per campaign; inspection requires tooling. | **JSONL.** |
| **`event_seq` allocation** | `event_seq` = 1-based line number. Reading the count is a single sequential pass over one small file. | Requires listing and parsing a directory, then taking `max` — more expensive and more failure modes. | **JSONL.** |
| **Fold performance** | One sequential read of ≤ a few thousand short lines. | Hundreds of file opens per fold; on Windows, small-file open cost dominates. | **JSONL, decisively.** |
| **Future log rotation** | Rename to `events.0001.jsonl`, start a fresh `events.jsonl`, continue `event_seq` across segments. Naming reserved, rotation deferred (Phase 2 R13). | Rotation is a non-problem — but only because the directory was already the problem. | **JSONL.** |
| **Implementation complexity** | Open append, write one line, flush, `fsync`. | Allocate a name, avoid collisions, enumerate to fold. | **JSONL.** |

**Decision — JSONL. One file per log instance, one event per line.**

### I.2 The rules that make it a contract

1. **`event_seq` is the 1-based line number, and the log is dense.** Line *n* carries `event_seq: n`. A gap, a duplicate or a mismatch is an integrity failure, and the check is a one-pass scan (Phase 2 INV-102 made mechanical). One-file-per-event could not offer this; here, position *is* the number, so there is nothing to keep in step.
2. **`event_seq` numbers events and nothing else.** No entity ordinal is ever derived from a log (Phase 2 §AI.1 item 3, §F.4 above). The two mechanisms share no code and no file.
3. **Each line is compact canonical JSON**: UTF-8, no BOM, keys sorted lexicographically, no embedded newlines, compact separators, terminated by a single LF. This *refines* Phase 2 §G.7 where §G.7 is silent — §G.7's 2-space indent governs artefact files, and **an event carries no `content_hash`**, being addressed by `(log, event_seq)` (Phase 2 §E.6). **No existing hash changes.** The log file's own bytes are hashed only as part of the §AA source manifest, which hashes files, not events.
4. **Append, flush, `fsync`, then return.** The event is not considered appended until the flush returns.
5. **A log file is created empty by the write of the first event, never in advance.** Phase 2 §AD.0/§AD.1 are explicit that a fresh asset and a fresh run have *empty* event logs — an absent file and an empty file mean the same thing, and the fold treats both as zero events.
6. **Logs are git-tracked and canonical.** Phase 2 §G.0: *"if the log is lost, so is the history, which is why the log is canonical and git-tracked and the fold is not."*

---

## J. Config Registry Layout

### J.1 Location and the closed-list rule

```
config/
├── evidence_policy.yaml        deny_list.yaml            narrative_library.yaml
├── format_profiles.yaml        category_profiles.yaml    creative_taxonomy.yaml
├── experiment_variables.yaml   diversity_targets.yaml    tool_capability.yaml
├── styles/STY-<format>-<slug>.yaml
└── README.md
```

**The nine registries are exactly the nine `*.yaml` files at the top level of `config/`.** Phase 2 P12 closes the list and INV-115 makes a tenth implicit config dependency a *defect*. This layout turns that invariant into a filesystem check:

```bash
# Exactly nine, and exactly these nine.
ls config/*.yaml | wc -l                      # must equal 9
```

The check is worth more than the tidiness. An enforcement rule that appears in a new file is now visible as a count changing, in a diff, at review time — which is the only moment anyone would catch it.

`config/` top level is reserved for the nine. `README.md` is not YAML and `styles/` is a subdirectory, so neither disturbs the glob — chosen deliberately so the rule needs no exception list.

### J.2 Versioning and hashing — the mechanism Phase 2 left to Phase 3

Phase 2 writes references like `config/evidence_policy@v4` (§G.2) and pins nine hashes into every RUN head (§W.1), but specifies neither where `v4` comes from nor how the hash is taken. Phase 2 §AI.1 item 6 assigns both to Phase 3.

**Each registry file carries a header:**

```yaml
registry: evidence_policy
version: 4                    # monotonic integer, bumped by the author on any substantive edit
status: AUTHORISED            # or PLACEHOLDER_NOT_AUTHORISED
# … rules below …
```

- **`config/<name>@v<n>` resolves to** the file `config/<name>.yaml` whose header declares `version: <n>`.
- **The pinned hash is `sha256` over the raw file bytes**, per Phase 2 §G.7 item 3 — never over a re-serialisation, which sidesteps YAML round-trip non-determinism. This is precisely why `.gitattributes` is load-bearing rather than cosmetic: with `eol=lf` the bytes are identical on every machine; without it, a Windows clone hashes CRLF and every pinned config hash in every run head becomes machine-specific (§AD R3).
- **A forgotten bump is mechanically detectable.** If the file's hash changes while its declared `version` does not, an authoring error has occurred — checkable in CI with one comparison against the previous commit.
- **Historical versions live in git and are recoverable by hash.** `git rev-list --all` × `git cat-file` finds the blob matching a pinned hash, so a run's exact policy is reconstructible without adding a field to the frozen RUN head schema. Slow, exact, and it changes no Phase 2 contract.

### J.3 Placeholders fail closed

Phase 3B creates the nine files containing **only** the header, with `status: PLACEHOLDER_NOT_AUTHORISED` and no rules. An empty `deny_list.yaml` blocks nothing and an empty `evidence_policy.yaml` classifies every source as unknown — silent, permissive failure modes, both of which the design exists to prevent.

**A run must refuse to start if any registry it pins declares `status: PLACEHOLDER_NOT_AUTHORISED`.** The placeholder is a locked door, not an empty room. This adds a header field, not a data contract: Phase 2 specifies the *content* of the nine registries and leaves their file shape to Phase 3, and the check lives in the orchestrator's start-up path, alongside the pinning it already does.

Rule contents are **not** authored here. The brief permits minimal placeholders for layout explanation and prefers design-only examples; the header above is the whole placeholder.

### J.4 Style profiles are registry entities, not a tenth registry

Phase 2 §T.1 makes a Style Profile a **registry entity** — human-authored YAML, `STYLE_ID`, hashed, three of them in V1 (Phase 1 ADR-012) — and it is deliberately absent from the nine. It is also absent from the RUN head's pinned `config` map. Both are correct and both are preserved:

- Style profiles live at `config/styles/STY-<format>-<slug>.yaml`, beside the policy they sit closest to, in a **subdirectory** so the nine-file rule is untouched.
- A style profile is pinned **per artefact** through `inputs[]` (Phase 2 §G.2), which pins every input with a ref and a hash. It is not a tenth run-level config dependency, so INV-115 is not engaged. Recorded explicitly because "authored YAML that affects generation and is not one of the nine" is exactly the shape of thing INV-115 exists to catch, and the reason it is not a violation deserves to be written down rather than assumed.

---

## K. Source Architecture

```
sources/                        RAW · IMMUTABLE · NEVER EDITED · TRACKED
└── books/
    ├── breakthrough-advertising.pdf       text layer ✓   → schwartz_persuasion_framework.md
    └── brilliance-breakthrough.pdf        scan, no text layer → schwartz_language_engine.md
```

**Three decisions:**

1. **`sources/original-books/` → `sources/books/`, with the two files renamed to stable, portable names.** The current names carry download noise (`_OceanofPDF.com_`, `0887232981-9780887232985 (1)_compressed`) that no future reference should have to reproduce. The rename must happen **before** any knowledge front matter cites these paths (Phase 3C), which is one of the reasons M3 is separated out (REPO_ADR-026).
2. **`sources/methodology/` is removed, not populated.** It is empty and untracked. Its intended contents — the three methodology PDFs — are Google Docs exports of the same unverifiable corpus as the Markdown modules (§B.4 finding 1), so they go to quarantine, not to `sources/`. Moving them into `sources/` would assert that they are raw upstream material, which is the specific claim §B.4 disproves.
3. **`sources/external/` is not created.** Phase 1 §I proposed it for fetched research snapshots. Phase 2 §S supersedes that: a snapshot is an `ASSET` with `asset_type: SOURCE_SNAPSHOT`, referenced by `SOURCE.snapshot_asset_id`, and it lives in `media/` under an `ASSET_ID` like every other payload. Creating `sources/external/` would give snapshots two homes — a direct contradiction-scan failure (contradiction scan, check 1). Phase 2 is later and frozen; it wins.

**`sources/` stays git-tracked** at 9 MB. It is small, irreplaceable, and it is what makes `source_files: ["sources/books/breakthrough-advertising.pdf"]` a *resolvable* path on any clone — the condition Phase 1's provenance schema attaches to the `DERIVED_VERIFIABLE` tier.

---

## L. Structured Knowledge Architecture

```
knowledge/                      DERIVED · PROVENANCE-TAGGED · RETRIEVABLE · TRACKED
├── copywriting/schwartz/       unchanged path — W1 RESOLVED (Phase 1 §I)
│   ├── schwartz_persuasion_framework.md    DERIVED_VERIFIABLE     · open
│   ├── schwartz_language_engine.md         DERIVED_VISUAL_REVIEW  · open
│   └── schwartz_integration_map.md         DESIGN_INPUT           · excluded
└── _quarantine/
    ├── README.md
    └── methodology/                        CONVERSATIONAL_DERIVED_UNVERIFIABLE · research_only
```

**The Schwartz files do not move.** The brief instructs it, Phase 1 §I confirms the location is correct, and Phase 3A modifies nothing. Their differing provenance — `parsed_text` from a PDF with a text layer versus `visual_review` of a scan — is a **metadata** difference, not a location difference, and §M places it inside each file where a retrieval hit will carry it.

**Two directories from Phase 1 §I are not created, both superseded by Phase 2:**

| Phase 1 §I proposal | Not created because | Where the thing actually lives |
|---|---|---|
| `knowledge/narrative/` — authored narrative pattern library | Phase 2 §B.1 makes `narrative_library` **one of the nine config registries**. Two homes for `NARRATIVE_PATTERN_ID` would be a canonical object with two authoritative paths. | `config/narrative_library.yaml` |
| `knowledge/language/cl/` — grown Chile customer language corpus | Phase 2 §J.4 makes customer language an `OBSERVATION` with `kind: CUSTOMER_LANGUAGE`, in the product-scoped Evidence Ledger, indexed by FTS5 (§Z.3). It is *evidence*, with a source and a locator — not a knowledge document. | `store/products/<PRD>/ledger/observations/` |

Both are recorded rather than silently dropped: they are Phase 1 proposals that Phase 2's later, frozen data model absorbed, and a reader comparing the two documents deserves the reconciliation.

**What `knowledge/` therefore is, precisely:** documents that are *derived from sources, reviewed by a human, retrieved into a prompt, and hashed into a run*. Anything that is a closed enumeration is config; anything with a locator and a source is evidence. That test is what keeps the directory from becoming a junk drawer.

---

## M. Knowledge Provenance Architecture

### M.1 The four candidates

| Option | Verdict |
|---|---|
| **A — YAML front matter inside the Markdown** | **Accepted.** |
| B — Adjacent metadata file (`foo.md` + `foo.meta.yaml`) | **Rejected.** Two files that can be moved, copied or edited apart. A knowledge file whose provenance is one directory operation away from being lost is not provenance-tagged. |
| C — Central registry (`knowledge/registry.yaml`) | **Rejected.** A second authoritative location for a fact the file could carry itself, and a merge-conflict magnet as the corpus grows. It also inverts the property that matters: provenance must travel *with the content* into the prompt (Phase 2 P9), and a central file has to be joined at retrieval time — one more step that can be skipped. |
| D — Combination | **Rejected as authored duplication, accepted as derivation.** A central *index* is fine when it is **derived** — SQLite, or a generated listing in `var/` — and never authored. |

**Decision — Option A: YAML front matter, one file, no second authoritative copy.**

Phase 2 §G.7 item 3 already assumes it: *"YAML is used only where a human is the author — `config/*.yaml` and **knowledge front-matter**."* This is the smallest architecture that supports every required field, and it is the only one where losing provenance requires editing the file that contains the content.

### M.2 The block

Phase 1 §I's schema verbatim, at the top of every file under `knowledge/`:

```yaml
---
knowledge_id:           KNW-schwartz-persuasion
tier:                   DERIVED_VERIFIABLE | DERIVED_VISUAL_REVIEW
                        | CONVERSATIONAL_DERIVED_UNVERIFIABLE | DESIGN_INPUT | AUTHORED
source_files:           ["sources/books/breakthrough-advertising.pdf"]   # repo-relative, resolvable
derivation_method:      parsed_text | visual_review | authored | probable_llm_derived
derivation_confidence:  OBSERVED | INFERRED
machine_verifiable:     true
human_reviewed:         true
scope:                  general | category:<x> | niche:<x>
retrieval_policy:       open | research_only | excluded
contains_claims:        none | product_claims | health_claims
version:                1
created_at:             "2026-09-04"
---
```

Four properties of the mechanism:

- **`source_files[]` holds repo-relative paths**, so it is resolvable on any clone and by the source-manifest hash. Phase 1's rule — *empty or unresolvable ⇒ cannot be `VERIFIABLE`* — becomes a check: every path in every `source_files[]` must exist.
- **The hash is over the whole file bytes**, front matter included, matching Phase 2 §G.7 item 3 and the `knowledge` map pinned in the RUN head (§W.1). Editing provenance is therefore a visible change to what a run pinned, which is correct: a tier downgrade *should* invalidate nothing silently.
- **Section-granularity provenance is a second front-matter key, not a second file.** Phase 1 §I's structural finding — several modules mix cited material with unsourced model speculation under one heading style, e.g. the `[Ampliación Externa - Internet]` blocks — is handled by an optional `sections:` list mapping heading anchors to a tier override. Still one file, still one source of truth. This is migration step **M5** and belongs to Phase 3C, not 3B.
- **A derived index may exist; an authored one may not.** The retrieval layer may materialise `knowledge_id → tier → retrieval_policy` into SQLite for speed. If that index disappears it is rebuilt from front matter, which is the same contract every other projection has.

---

## N. Methodology Quarantine Design

### N.1 Destination

```
knowledge/_quarantine/methodology/        ← 8 files, moved unmodified
```

Phase 1 §I named this path and Phase 1 ADR-009 marks it *highest priority*. It is inherited, not re-litigated. The alternatives considered and rejected: `knowledge/legacy/` (describes age, not the problem — the problem is unverifiability, and new material can arrive equally unverifiable), `knowledge/unverified/` (accurate but reads as a staging area awaiting verification; this corpus's citations *cannot* be resolved, so nothing is pending), and a top-level `quarantine/` (removes it from `knowledge/`, which hides the fact that it is knowledge-shaped and would otherwise be retrieved).

`_quarantine` keeps the leading underscore from Phase 1: it sorts first, reads as non-ordinary, and is visible in every directory listing above the material it guards.

### N.2 Do the PDFs and the Markdown separate?

**No — they stay together, and the finding that settles it is new.** The three PDFs carry `/Producer (Skia/PDF m154 Google Docs Renderer)`: they are Google Docs exports, not scans of published works and not upstream documents. They are the same corpus in a different container, produced the same way, carrying the same unresolvable citations, the same niche-specific claims (PCOS hair-loss supplement, `es-CL`) and the same F2/F3 content Phase 1 classified as `NOT_SAFE_TO_HARDCODE`.

Splitting them — PDFs to `sources/`, Markdown to quarantine — would assert that the PDFs are raw upstream material whose derivatives are suspect. The evidence says the opposite: neither half has an upstream. Keeping all eight files in one directory keeps one retrieval policy over one corpus, which is also the only arrangement in which the policy is enforceable by path.

### N.3 Provenance and retrieval policy

Every quarantined file receives, in Phase 3C:

```yaml
tier:                  CONVERSATIONAL_DERIVED_UNVERIFIABLE
derivation_method:     probable_llm_derived
derivation_confidence: INFERRED          # authorship is inferred; unverifiability is established
scope:                 niche:pcos-hair-loss-supplement-cl
retrieval_policy:      research_only
contains_claims:       health_claims
source_files:          []                # empty ⇒ cannot be VERIFIABLE, by Phase 1's rule
```

**`research_only` means, precisely** (Phase 1 §I): a human may read it; `creative-strategist` may consult it for *structural* patterns — the 7-part UGC arc, the three testing methods, the pain→hope transition — under an explicit tier warning; **and the script engine may never retrieve it.** It supplies no claims, no benchmarks, no ingredient science and no CTA copy.

**Enforcement is two-layered, deliberately.**

1. **Metadata is the authority.** The retrieval service reads `retrieval_policy` from front matter and refuses anything not `open` in a script-generation context.
2. **The path is a second line of defence.** Any repository path containing a `_quarantine/` segment is refused by the script-generation retrieval path regardless of its metadata.

Two mechanisms for one rule is normally a smell. It is justified here because the failure mode is asymmetric: a missing front-matter block (a file added to the directory without one) would default to *permitted* under metadata alone, and the material in question contains unsupported health claims and a compliance deny-list violation (Phase 1 F2, F3). The path check fails closed for exactly the case the metadata check misses. `knowledge/_quarantine/README.md` states both, in the directory they govern.

### N.4 How future ingestion handles similar material

The general rule, since this corpus will not be the last: **material whose citations cannot be resolved enters `_quarantine/<topic>/` with `retrieval_policy: research_only`, regardless of format, regardless of who wrote it, and regardless of how useful it looks.** The quarantine follows from *unverifiability*, which is established by checking citations, not from *authorship*, which is inferred. If authorship were later established or refuted, `derivation_method` changes and `retrieval_policy` does not — Phase 1 §I's rule, preserved because it is the part that makes the classification stable.

---

## O. Asset / Media Architecture

### O.1 The separation that everything else depends on

**Binary payload ≠ Asset Registry record.** The record is canonical, git-tracked JSON at `store/assets/<2hex>/AST-<12hex>.json`. The payload is a git-ignored file at `media/<2hex>/AST-<12hex>.<ext>`. `ASSET.path` (Phase 2 §S.1) holds the media-root-relative path — `"7b/AST-7b31e0c9d4a2.mp4"` — never an absolute path, never a path outside the media root.

### O.2 The media root

```
media/                              MEDIA_ROOT · git-ignored · content tracked by hash, not by git
├── .gitignore                      *  !.gitignore  !README.md          [tracked]
├── README.md                                                            [tracked]
├── 7b/AST-7b31e0c9d4a2.mp4         registered payloads, sharded by id
├── 1a/AST-1a2b3c4d5e6f.jpg
└── _unregistered/                  repository-origin files awaiting registration (§P.2)
```

**Addressed by `ASSET_ID`, not by content hash.** Phase 2 §E.4 is explicit that two asset records may legitimately share bytes and differ in rights provenance — the same image supplied by the operator and also present in the repository — and that *rights attach to provenance, not to bytes*. Content-addressed storage would merge those two records onto one file, so deleting or replacing one would silently affect the other. Duplicating a few megabytes is the correct price for keeping two rights positions genuinely separate.

**Sharded by the first two hex characters of the id suffix**, matching `store/assets/`, so a record and its payload share a folder name and neither directory grows unbounded.

**All eleven `asset_type` values live in one flat namespace.** No `media/videos/`, no `media/voices/`, no `media/generated/`. Type, role, brand, product and state are fields on the record and columns in the index; encoding them in a path would create a second classification that can disagree with the first, and would require moving a file when a state changes — which is exactly the mutation the design forbids.

### O.3 Git treatment

| | Decision |
|---|---|
| `media/**` payloads | **Git-ignored.** Phase 2 §AI.1 item 4: *"the asset registry is git-tracked JSON; the payloads are not."* Inherited. |
| `media/.gitignore`, `media/README.md` | **Tracked**, so the directory exists on clone and explains itself. |
| The 15 existing samples | **Remain in git history** at `92ec3eb` after being untracked. Recoverable with `git checkout 92ec3eb -- samples/`. Not purged (REPO_ADR-017). |
| Git LFS | **Not adopted, not precluded.** `git-lfs 3.7.1` is installed on this machine but unconfigured here. Adopting it later requires only tracking patterns and a migration; nothing in this design assumes either state. |

### O.4 Checksums and missing-media behaviour

Every asset record carries `content_sha256` and `bytes` (Phase 2 §S.1), both canonical and git-tracked. That makes every failure mode of an ignored directory *detectable*, which is the most this design can honestly offer:

```bash
# Phase 5 delivers this as `creative-os media check`; the contract is defined now.
# For every asset record: does the payload exist, is its size right, does its hash match?
```

| Condition | Behaviour |
|---|---|
| Payload absent | Report `MEDIA_MISSING` with `asset_id` and expected path. **V1-Core does not halt** — Product Truth needs the *observation* already recorded, not a re-read of the file. |
| Payload present, hash mismatch | Report `MEDIA_CORRUPT`. This is an integrity failure: an immutable record's bytes changed underneath it. |
| Payload required as a **generation input** and missing | **Halt the run** with a named error. A production step cannot proceed on a file it cannot read, and inventing a substitute is the failure the whole rights model exists to prevent. |
| Extra file in `media/` with no record | Report `MEDIA_ORPHAN`. Never auto-registered — registration is a provenance decision (§P). |

### O.5 Local-machine portability, and the gap

`ASSET.path` is media-root-relative and the media root is resolved by configuration (`MEDIA_ROOT`, defaulting to `<repo>/media`). Nothing canonical contains a drive letter. So the whole payload tree can move to an external drive, a synced folder, or object storage without touching a single canonical record.

**The gap, stated rather than softened:** `git clone` on a second computer produces a complete, valid, fully rebuildable canonical store and **zero media payloads**. Every artefact, record, event, config and knowledge file arrives; every video, voice sample and image does not. Media transfer is an out-of-band copy the operator performs, and `media check` tells them whether it worked. This is the direct cost of Phase 2 §AI.1 item 4, and it is listed as risk R1 and as approval item 2.

### O.6 External-storage compatibility, without adopting one

Three future options remain open because nothing in the design depends on the current one:

| Option | What it would take | What it would not touch |
|---|---|---|
| Git LFS | `git lfs track "media/**"`, drop the ignore rule | No canonical record; `path` and `content_sha256` are unchanged |
| External drive / synced folder | Point `MEDIA_ROOT` elsewhere | Nothing — this is a single configuration value |
| Object storage | A resolver that maps `path` to a bucket key | Records still hold the same relative path; the resolver is an adapter |

No credential, bucket, remote or LFS server is assumed, configured or required by this design.

---

## P. Incoming / Ingestion Boundary

### P.1 The boundary

```
incoming/  ──►  validate  ──►  classify  ──►  normalise  ──►  register  ──►  media/<2hex>/AST-….<ext>
 (operator)     header,        asset_type,     sha256,        ASSET_ID,        store/assets/<2hex>/AST-….json
                size, codec    likely role     canonical name  record written
```

Phase 1 §J's ingestion pipeline, unchanged. Phase 3A designs the **boundary**, not the implementation.

**The operator never needs to know an identifier.** They drop a file into `incoming/`. Ingestion assigns the `ASSET_ID`, computes the hash, chooses the canonical name and moves the payload. `original_filename` is preserved in the record — Phase 1's answer to W7: *canonical names are assigned, not typed.* This is also why the fifteen existing media files need no manual renaming, ever (§P.3).

**Optional context without identifiers.** An operator may place a sidecar `<filename>.meta.yaml` next to a dropped file to declare brand, product, intended role or a rights basis. It is optional, it is read once at ingestion, and it is never canonical — the record is. This lets an operator supply context they *do* know without learning any part of the identifier scheme.

**Failures stay put.** A file that fails validation remains in `incoming/` beside a `<filename>.rejected.txt` naming the reason. Nothing is deleted, and no half-registered record is written.

### P.2 Two entry points, because provenance differs

This is the design's one deliberate use of a path to declare something other than identity, and it is load-bearing:

| Entry point | `origin.kind` | Initial state (Phase 2 §S.2) |
|---|---|---|
| `incoming/` | `USER_UPLOAD` | `USER_PROVIDED_UNVERIFIED` |
| `media/_unregistered/` | `REPOSITORY` | `REFERENCE` |

Phase 2 §S.4 requires all fifteen current samples to be `REFERENCE`. If they were registered through `incoming/`, they would enter as uploads and fold to `USER_PROVIDED_UNVERIFIED` — a different rights position, contradicting a frozen invariant. A second entry path is the cheapest way to keep the distinction, and Phase 2 §S.2 makes `origin.kind` the *only* determinant of the initial state, so the path must carry the declaration somewhere. It carries it here, once, at the boundary; after registration the payload moves to an id-derived path that carries nothing (RP8).

### P.3 How the fifteen samples eventually enter the registry

Without renaming a single file by hand, and **not in Phase 3B**:

1. **Phase 3B** moves `samples/**` to `media/_unregistered/`, preserving the current sub-structure and every filename, and untracks it. Content hashes are unchanged; no identifier is minted; no record is written.
2. **Phase 5+**, once the ingestion service, the Pydantic models and the validators exist, registers all fifteen with `origin.kind: REPOSITORY`, assigns `ASSET_ID`s, writes the records, and relocates the payloads to `media/<2hex>/AST-….<ext>`. `original_filename` preserves `WhatsApp Video 2026-09-03 at 10.01.37 PM.mp4` in the record.
3. The three `ssstik.io_*` voice files additionally receive `tags: [no_cloning_source]`, per Phase 2 §S.4 and INV-72.

**Why not register them in Phase 3B?** Writing fifteen canonical records by hand, before any writer service, any schema and any validator exists, would be creating production data with no mechanism to check it — and a malformed immutable record is not correctable in place. Phase 3B moves bytes; Phase 5 mints identity. `media/_unregistered/` exists to hold the gap between the two, and it is empty once registration has run.

---

## Q. Runtime / Derived / Cache Layout

```
var/                        DERIVED · REBUILDABLE · EPHEMERAL · fully git-ignored
├── .gitignore              *  !.gitignore  !README.md              [tracked]
├── README.md                                                        [tracked]
├── index/                  creative_os.sqlite3 (+ -wal, -shm)        rebuildable
├── schemas/                generated JSON Schema (2020-12)           regenerated
├── cache/                  fetch cache, prompt cache metadata        disposable
├── tmp/                    temp downloads, scratch                   disposable
├── work/                   generation attempts, working clips        disposable
├── logs/                   runtime logs                              disposable
└── exports/                operator deliverables (final videos, zips) copies
```

**`var/` may be deleted at any time and the only cost is time.** That is the entry criterion; anything failing it does not belong here.

### Q.1 SQLite

**Location `var/index/creative_os.sqlite3`. Git-ignored. Never committed.**

Audited, briefly, because Phase 2 §AA settles most of it: SQLite is `INDEX_ONLY`, holds nothing that cannot be rebuilt (P13, INV-100), is verified by `rebuild --verify`, and *a missing database is not an error* (§AA.2). A tracked binary that a rebuild can regenerate would produce a conflicting diff on every build for no benefit, and it would create the possibility — however remote — of someone treating a committed index as authoritative. Ignoring it makes that impossible rather than discouraged.

The `-wal` and `-shm` sidecars are covered by ignoring `var/` wholesale. `index_meta.canonical_root_commit` (Phase 2 §AA.1) records the git sha the index was built from, so a rebuilt index remains attributable without being tracked.

### Q.2 Generated schemas

**Location `var/schemas/`. Git-ignored. Regenerated on demand.**

Phase 2 §G.8 makes Pydantic v2 the single source of truth, generating JSON Schema. Tracking the generated output would create a second artefact that can drift, requiring a CI job to prove it has not — a guard against a problem that not tracking makes impossible. Schema review happens on the Pydantic model diff, which is more readable than a JSON Schema diff anyway.

The reproducibility objection — *"which schema was sent to the model during run X?"* — is answered without tracking: the schema is a pure function of the code at a commit, the code is git-tracked, and the run head pins skill versions. Checking out the commit and regenerating yields the exact schema. Recorded so the trade-off is visible rather than assumed away.

### Q.3 Derived Markdown renders are **not** in `var/`

Phase 2 §G.7 item 4 requires them **git-tracked**, so a Gate reviewer's rendered package cannot silently disagree with the artefact it projects. They therefore live inside the canonical root, beside the scope they describe:

```
store/products/<PRD>/reviews/product_truth_v2.md
store/campaigns/<CMP>/reviews/experiment_plan_v3.md
store/campaigns/<CMP>/reviews/creative_CRE-acme-3f8b21-07_v3.md
```

**And they are inside the source manifest, with no exception.** That is safe only because of a requirement this document adds explicitly: **the renderer must be pure.** No wall-clock timestamp, no absolute path, no run id, no hostname in a render's bytes. A pure render of an unchanged artefact reproduces byte-for-byte, so it never moves the manifest hash; only a genuine change to the artefact or a genuine change to the renderer does. If the renderer were impure, every gate render would mark the index stale, an operator would learn to ignore staleness, and the sharpest integrity signal in the system (Phase 2 §AA.2) would be gone.

Two consequences worth stating: a hand-edited render is caught by the manifest hash — which is the correct outcome for editing a derived file — and a renderer upgrade changes every render's bytes at once, which is a real change and should be one commit.

Every render carries `derived: true` and the ref and hash of its source artefact in front matter, and **a render may never contain a fact absent from its source JSON.**

### Q.4 Classification summary

| Location | Canonical | Derived | Ephemeral | Tracked | Externalisable |
|---|---|---|---|---|---|
| `store/**/*.json`, `**/events.jsonl` | ✅ | | | ✅ | No — this is the system of record |
| `store/**/reviews/*.md` | | ✅ pure | | ✅ | No |
| `config/*.yaml`, `config/styles/*.yaml` | ✅ | | | ✅ | No |
| `knowledge/**`, `sources/**` | ✅ | | | ✅ | No |
| `media/**` | | | | ❌ | **Yes** — LFS, external drive, object storage |
| `var/index/`, `var/schemas/` | | ✅ | | ❌ | N/A — rebuilt |
| `var/cache/`, `tmp/`, `work/`, `logs/` | | | ✅ | ❌ | N/A |
| `var/exports/` | | ✅ copies | ✅ | ❌ | Yes — but the registry + `media/` is the real copy |
| `incoming/**` | | | ✅ | ❌ | N/A |

---

## R. Claude / Skill Boundary

**Phase 3A decides the structural boundary only. No Skill is created, no `SKILL.md` is written, and no placeholder directory is scaffolded.**

```
.claude/
├── settings.json                     project settings for Claude Code        [tracked]
├── settings.local.json               machine-local overrides                 [IGNORED]
└── skills/                           [Phase 4 — created by Phase 4]
    ├── product-intelligence/SKILL.md
    ├── market-intelligence-cl/SKILL.md
    ├── creative-strategist/SKILL.md
    ├── script-engine/SKILL.md
    └── compliance-reviewer/SKILL.md
```

**The boundary is drawn by consumer, and it separates three things the brief warns against mixing:**

| Thing | Location | Why not elsewhere |
|---|---|---|
| **Skills** — the five procedural know-how documents (Phase 1 §E) | `.claude/skills/<name>/SKILL.md` | This is the conventional path both Claude Code and the Agent SDK resolve, so one location serves both the development environment and the automated runtime (Phase 1 §D.1). Their versions are pinned in the RUN head's `skills` map. |
| **Orchestration prompt templates** — hashed and pinned in `pinned.prompts` (Phase 2 §W.1) | `src/creative_os/prompts/` | They are **runtime inputs**, versioned and shipped with the code that sends them. Putting them under `.claude/` would mix development-environment configuration with reproducibility-critical runtime artefacts, and Phase 1 §D.1 is explicit that these are two different systems. |
| **Domain knowledge** — Schwartz, quarantine | `knowledge/` | A Skill is *procedure*; knowledge is *content retrieved into* a procedure. A Skill that embeds knowledge makes the knowledge unhashable and un-versionable, and it bypasses the retrieval policy that §N.3 enforces. |

**Three rules Phase 4 inherits** (repeated in §AH):

1. **No Skill embeds policy.** Every enforcement rule, taxonomy and threshold resolves to one of the nine config registries (Phase 2 P12, INV-115). A rule inside a `SKILL.md` is a tenth config dependency and therefore a defect.
2. **No Skill writes to `store/`.** Skills produce validated output; the orchestrator allocates identifiers and writes canonical files (Phase 2 INV-06 — *no model in the system may emit an identifier*).
3. **No Skill reaches `knowledge/_quarantine/`.** Enforcement is the retrieval layer's, not the Skill's prose (§N.3). A Skill that must be *told* not to read something is not protected.

---

## S. Future Python Code Boundary

**No code is created in Phase 3A, and `src/` is not scaffolded. The name and the boundary are decided; Phase 5 creates the directory.**

| Candidate | Verdict |
|---|---|
| `app/` | **Rejected.** Connotes a deployable application; this is a library plus a CLI plus an orchestrator. |
| `creative_os/` at the repository root | **Rejected.** A top-level importable package makes the repository root implicitly a `sys.path` entry, so tests can import a package that was never installed and pass against a layout that will not ship. |
| **`src/creative_os/`** | **Accepted.** The src-layout is the packaging default, it forces an installed (editable) package so imports match production, and it keeps the repository root legible — a reader sees `src/` and knows where code lives without a second question. `creative_os` is a valid Python identifier; `creative-experimentation-os` is not. |

**The boundary sketch — Phase 5 owns the detail. This is repository architecture, not implementation architecture:**

```
src/creative_os/
├── domain/          Pydantic v2 models — the single source of truth for every schema
├── validation/      the 120 invariants, as testable predicates
├── services/        deterministic services: coverage, claim-freedom, diversity solver,
│                    source classifier, feasibility, localisation invariance
├── store/           canonical I/O: artefact writer (create-exclusive), record writer,
│                    event-log append, scope-ordinal allocator, path resolver
├── index/           SQLite builder and the fold — the most test-worthy code in the system
├── orchestrator/    run loop, steps, human gates, cost governor
├── adapters/        external boundary: web, vision, Higgsfield, Meta, ffmpeg
├── prompts/         versioned prompt templates, hashed and pinned
└── cli/             operator entry points
```

Two boundaries deserve naming now because the repository layout depends on them:

- **`store/` is the only package that knows a path.** Every path convention in §F–§I lives behind it. No service, adapter or Skill constructs a canonical path, so a future layout change is one module's problem — which is what makes the migration-log discipline of §X affordable.
- **`adapters/` is the only package that talks to anything outside the repository.** Production adapters (Higgsfield, ffmpeg) and research adapters (web, vision) sit at the same boundary because they share one property: their availability and their cost are not the domain model's business.

---

## T. Future Schema Boundary

| | Location | Tracked | Rationale |
|---|---|---|---|
| **Pydantic v2 domain models — the source of truth** | `src/creative_os/domain/` | ✅ | Phase 2 §G.8. One definition, two consumers (runtime validation + generated schema), no hand-maintained drift. |
| **Generated JSON Schema (2020-12)** | `var/schemas/` | ❌ | Derived. Regenerated by a build step. See §Q.2. |
| **Model-facing narrowed schemas** | `var/schemas/model_facing/` | ❌ | Also generated, from the same models, by the narrowing projection Phase 2 §G.8 specifies — IDs, hashes, versions, `inputs[]` and every `DERIVED_DETERMINISTIC` field removed; `HARD_BLOCK` absent from every enum; `additionalProperties: false`. |

**The generated schema must never become a second source of truth**, and the layout is what enforces it: a file in `var/` cannot be edited to effect, because the next generation overwrites it. Tracking generated schemas would create a file a reviewer could plausibly edit — the drift Phase 2 §G.8 exists to prevent.

One boundary is defined by its absence: **evidence extraction (E1) has no schema at all** (Phase 2 §G.8, Phase 1 ADR-006/031 — citations and structured outputs are mutually exclusive). No file is generated for it, and its absence should be a documented expectation rather than a suspected omission.

**No schema is generated in Phase 3A.**

---

## U. Test Boundary

**Reserved, not created.** Phase 3B builds no test tree; empty directories with no tests add navigation cost and no value (RP11, §AE).

```
tests/
├── unit/             pure functions: coverage, claim-freedom, classifier, diversity
├── integration/      writer → log → fold → index, end to end on a temp store
├── invariants/       the 120 invariants of Phase 2 §Y, one test per invariant id
└── golden/           frozen inputs with reviewed expected outputs
    └── {beauty,food,tech,home,fashion}/     ← created when the first golden case exists
```

Three notes for the phase that builds this:

- **`invariants/` is named per invariant id** (`test_inv_117_single_writer.py`), so a Phase 2 invariant number maps to a test file without a lookup table. The 120 invariants are the specification; a test suite organised any other way loses the correspondence.
- **The fold is the highest-value target.** Phase 2 §AJ.7 names the index builder's fold as *the most test-worthy code in the system*, and §AA.2 makes `rebuild --verify` the mechanism. `integration/` owns it.
- **Golden categories are created one at a time.** Phase 1 §Y.6 cut the Golden Test Set from V1 entirely; the five category directories are reserved names, and creating five empty ones now would contradict the phase that removed them.

---

## V. Documentation Layout

| File | Decision | Reason |
|---|---|---|
| `PRE_FLIGHT_AUDIT.md` | **Stays at the repository root. Not moved, not edited, ever.** | It is an immutable historical snapshot, and every phase document cites it by that path. Moving it changes nothing about its content and breaks every reference — cost with no benefit. |
| `docs/PHASE_1_SYSTEM_DESIGN.md` | **Does not move.** | Phase 2 §AI.1 item 7 recommends the phase documents stay; they are cited by path across three documents and by commit messages. A `docs/archive/` split would create two classes of phase document, and the classification would need maintaining. |
| `docs/PHASE_2_DATA_ARCHITECTURE.md` | **Does not move.** | Same. |
| `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` | Stays where Phase 3A created it. | Same. |
| `docs/MIGRATIONS.md` | **New, created by Phase 3B.** | Append-only record of every path move: date, commit, from → to, reason. Required by §X because §AA hashes relative paths — a move changes the manifest hash even when content is identical, and this file is what makes that change explainable rather than alarming. |
| `README.md` | **Rewritten by Phase 3B.** | It currently describes a "temporary" structure and states the repository contains no architecture, no Skills and no Phase — false since Phase 1, and actively misleading to a second operator. |
| `docs/OPERATING.md` | Deferred to Phase 5. | An operating guide for a system with no runtime is fiction. |

**Phase documents are not moved into `store/`, are not converted, and are not tracked as knowledge.** They are documentation *about* the system, not data *of* it: nothing retrieves them, nothing hashes them into a run, and no artefact references them. They stay in `docs/` where a human looks for them.

---

## W. Git Tracked / Ignored Matrix

| Path / pattern | Canonical? | Tracked | Ignored | Externalisable | Reason |
|---|---|---|---|---|---|
| `store/**/v*.json` (artefact versions) | ✅ | ✅ | | ❌ | System of record. Git *is* the versioning mechanism (Phase 1 ADR-004). |
| `store/**/*.json` (entity records) | ✅ | ✅ | | ❌ | Immutable records; creation lives here (INV-119). |
| `store/**/events.jsonl` | ✅ | ✅ | | ❌ | *"the log is canonical and git-tracked and the fold is not"* (Phase 2 §G.0). |
| `store/**/reviews/*.md` | Derived (pure) | ✅ | | ❌ | Phase 2 §G.7 item 4 — a gate render must not silently disagree with its artefact. In the manifest; renderer must be pure (§Q.3). |
| `config/*.yaml` (the nine) | ✅ | ✅ | | ❌ | Hashed over file bytes into every run (§J.2). Exactly nine. |
| `config/styles/*.yaml` | ✅ | ✅ | | ❌ | Authored registry entities, pinned per artefact via `inputs[]` (§J.4). |
| `knowledge/**/*.md` | ✅ | ✅ | | ❌ | `KNOWLEDGE_ID` entities; hashed into the RUN head; provenance in front matter. |
| `knowledge/_quarantine/**` | ✅ | ✅ | | ❌ | Tracked **and** restricted. Tracking is not permission — retrieval policy is (§N.3). |
| `sources/books/*.pdf` | Raw | ✅ | | ❌ | 9 MB, irreplaceable, and what makes `source_files[]` resolvable on a clone. |
| `docs/**` | ❌ | ✅ | | ❌ | Documentation. |
| `.gitattributes`, `.gitignore`, `.env.example`, `README.md` | ❌ | ✅ | | ❌ | Repository contract. |
| `media/**` payloads | Referenced, not canonical | | ✅ | **✅** | Phase 2 §AI.1 item 4. Detectable by `content_sha256`, not preserved by git. |
| `media/.gitignore`, `media/README.md` | ❌ | ✅ | | ❌ | Make the directory exist on clone and explain itself. |
| `media/_unregistered/**` | | | ✅ | ✅ | Payloads awaiting registration; empty once Phase 5 has run. |
| `incoming/**` contents | ❌ | | ✅ | ❌ | Transient by definition. |
| `var/**` | ❌ | | ✅ | ❌ | Derived, rebuildable or ephemeral. Deleting it costs only time. |
| `var/index/*.sqlite3`(+`-wal`,`-shm`) | ❌ `INDEX_ONLY` | | ✅ | ❌ | Phase 2 P13, INV-100. A committed index could be mistaken for truth. |
| `var/schemas/**` | ❌ | | ✅ | ❌ | Generated from Pydantic; tracking creates drift to police (§T). |
| `.env` | — | | ✅ | ❌ | Secrets never enter git (§AC.4). |
| `.claude/settings.local.json` | ❌ | | ✅ | ❌ | Machine-local. |
| `.claude/settings.json`, `.claude/skills/**` | ❌ | ✅ | | ❌ | Shared project configuration and the five Skills (Phase 4). |
| `src/**`, `tests/**` | ❌ | ✅ | | ❌ | Source code (Phase 5+). |
| `**/__pycache__/`, `*.pyc`, `.venv/` | ❌ | | ✅ | ❌ | Build residue. |
| `Thumbs.db`, `desktop.ini`, `.DS_Store` | ❌ | | ✅ | ❌ | OS cruft; Windows and macOS both write it. |

**The check that makes this matrix real** — not a table someone has to honour, but a command:

```bash
git ls-files store config knowledge sources docs | xargs -r git check-ignore -v
```

It must print nothing. Anything it prints is canonical truth in an ignored path — RP7 violated, and the single most dangerous mistake this layout can make.

**No `.gitignore` or `.gitattributes` file is written in Phase 3A.** Their exact contents are drafted in §Z.2 for Phase 3B to apply.

---

## X. Path Stability Rules

Phase 2 §AA computes the source manifest over **sorted `[relative_path, content_sha256]` pairs**, and §AI.2 calls this *"the one place repository layout touches the data model."* Six rules follow.

**X.1 — A canonical path is a total function of identifiers.** No canonical path contains a title, a date, a description or any human-chosen label. Consequence: **no canonical file ever needs renaming**, so the largest source of manifest churn cannot arise (RP2).

**X.2 — Files are not IDs.** The identifier is inside the file; the path renders it. A rename never changes domain identity, and identity is never read from a path. **The index builder must read every identifier from file content, and a mismatch between path and content is an integrity failure** (§AB check 14). This is what makes a badly-performed manual repair *detectable* rather than silently authoritative.

**X.3 — Exactly two paths carry policy, and both are backed by in-file metadata.** `knowledge/_quarantine/` (retrieval policy, §N.3) and the two ingestion entry points (`origin.kind`, §P.2). Both duplicate an authoritative in-file field, so the path is a second line of defence and never the source of truth. There is no third, and adding one requires an ADR.

**X.4 — Registry slugs are chosen once and are immutable.** `BRAND_ID`, `PRODUCT_ID`, `STYLE_ID`, `NARRATIVE_PATTERN_ID` and `KNOWLEDGE_ID` are human-chosen at registration (Phase 2 §E.1). **Changing a slug creates a new entity; it is not a rename.** A brand that rebrands gets a new `BRAND_ID`, and the old one keeps its history. Two limits, set here because paths are built from them: brand slug ≤ 16 characters, product slug ≤ 24 (§AC.1).

**X.5 — Every move of a tracked file is recorded in `docs/MIGRATIONS.md`.** Date, commit, from → to, reason. Because the manifest hashes relative paths, a pure move changes the manifest hash while changing no content — the log is what turns an alarming hash change into an attributable one. This applies to Phase 3B and to every later structural change, including a future decision to shard the ledger directories.

**X.6 — Generated paths are constructed in exactly one place.** `src/creative_os/store/` owns every path convention in §F–§I. No service, adapter, Skill or script builds a canonical path by string concatenation. A layout change is then one module plus one migration-log entry, rather than a search across the codebase.

---

## Y. Migration Map

**Designed here. Not executed. No file has been moved, renamed, deleted or edited by Phase 3A.**

Every row below refers to a file verified present in the working tree on 2026-09-04 (§B). No file is invented.

### Y.1 Moves and renames

| # | Current path | Target path | Action | Reason | Risk | Validation |
|---|---|---|---|---|---|---|
| 1 | `sources/original-books/breakthrough-advertising-0887232981-9780887232985 (1)_compressed.pdf` | `sources/books/breakthrough-advertising.pdf` | `git mv` | Phase 1 M1. Removes download noise from a path that Phase 3C's `source_files[]` will cite. | **Low** | sha256 identical; `git log --follow` resolves |
| 2 | `sources/original-books/_OceanofPDF.com_The_brilliance_breakthrough_-_Eugene_schwartz.pdf` | `sources/books/brilliance-breakthrough.pdf` | `git mv` | Same. | **Low** | sha256 identical |
| 3 | `sources/methodology/` (empty, untracked) | — | `rmdir` | Empty; its intended contents are Google Docs exports that belong in quarantine (§B.4 finding 1). Git holds no empty directories, so nothing is committed. | **Low** | directory absent |
| 4 | `knowledge/methodology/` — 5 `.md` + 3 `.pdf` | `knowledge/_quarantine/methodology/` | `git mv` (directory) | Phase 1 M2 and ADR-009 — highest priority. **Unmodified**: path only. PDFs and Markdown stay together (§N.2). | **Low** | 8 files present; every sha256 identical; old path absent |
| 5 | `knowledge/_quarantine/methodology/modulo-5-infraestructura-herramientas (1).md` | `…/modulo-5-infraestructura-herramientas.md` | `git mv` | Strips the browser download artefact ` (1)` from a filename that will become a stable reference. | **Low** | sha256 identical |
| 6 | `samples/**` — 15 media files | `media/_unregistered/**` (sub-structure and filenames preserved) | `git mv` (directory) | Phase 2 §AI.1 item 4. Entering as `origin.kind: REPOSITORY` ⇒ `REFERENCE`, which requires an entry point that is *not* `incoming/` (§P.2). | **Medium** — the one asymmetric step (§AA.3) | 15 files present; every sha256 identical; `samples/` absent |
| 7 | `media/**` | — | `git rm -r --cached media` | Untrack payloads while leaving them on disk. Blobs stay in history at `92ec3eb` and remain recoverable (§O.3). | **Medium** — must run **after** move + verification | `git ls-files media` empty; files present on disk |
| 8 | `knowledge/copywriting/schwartz/*.md` | unchanged | **KEEP** | Correct location, confirmed by Phase 1 §I (W1 RESOLVED) and by the brief. Not moved, not modified. | — | sha256 identical to `59cbe49` |
| 9 | `PRE_FLIGHT_AUDIT.md`, `docs/PHASE_1…`, `docs/PHASE_2…`, `docs/PHASE_3…` | unchanged | **KEEP** | §V. Phase 2 §AI.1 item 7. | — | sha256 identical to `59cbe49` |

**27 files touched by moves; every one hash-identical afterwards.** Phase 3B performs no content edit on any pre-existing file except `README.md`.

### Y.2 New files created by Phase 3B

| # | Path | Purpose |
|---|---|---|
| 10 | `.gitattributes` | `eol=lf` for text, `binary` for media. Fixes the cross-machine config-hash break (§AD R3). |
| 11 | `.gitignore` | Root ignore rules (§Z.2). |
| 12 | `.env.example` | Credential **names**, never values (§AC.4). |
| 13 | `README.md` | **Rewritten.** The current text is stale and misleading (§B.4 finding 9). |
| 14 | `docs/MIGRATIONS.md` | The from → to map of this migration, as the first entry (§X.5). |
| 15 | `store/README.md` | The canonical root's layout and contract; creates the directory. |
| 16 | `config/README.md` + the nine placeholder `*.yaml` + `config/styles/README.md` | Establishes the closed-list rule where it is enforced; placeholders fail closed (§J.3). |
| 17 | `knowledge/_quarantine/README.md` | Retrieval policy stated in the directory it governs (§N.3). |
| 18 | `media/.gitignore` + `media/README.md` | Directory exists on clone; ignore rules local to what they govern. |
| 19 | `incoming/.gitignore` + `incoming/README.md` | The drop zone and how to use it without knowing an identifier. |
| 20 | `var/.gitignore` + `var/README.md` | Derived root; deleting it costs only time. |

### Y.3 Repository configuration

| # | Action | Reason |
|---|---|---|
| 21 | `git config core.autocrlf false`, then `git add --renormalize .` | Local config plus one normalisation commit, so `.gitattributes` governs from the first checkout onward (§AD R3). |

**21 migration operations.** 7 moves/removals affecting 27 files, 13 file creations (one of which rewrites `README.md`), 1 configuration change.

### Y.4 Explicitly **not** in Phase 3B

| Deferred item | To | Why |
|---|---|---|
| Provenance front matter on all 11 knowledge files (Phase 1 **M3**) | **Phase 3C** | It is authoring, not migration. Keeping 3B to moves makes its central validation — *every moved file's hash is unchanged* — crisp and total. Mixing edits into it destroys that. |
| Section-tagging the `[Ampliación Externa]` blocks (Phase 1 **M5**) | **Phase 3C** | Requires reading and judgement (Phase 1 rates it Medium risk). |
| Authoring the compliance deny-list (Phase 1 **M4**) | **Phase 4+** | Policy content, not layout. Until then it is a placeholder that fails closed (§J.3). |
| OCR decision for *The Brilliance Breakthrough* (Phase 1 **M6**) | Optional, unscheduled | The derived layer already declares the limitation. |
| Registering the 15 media files in the Asset Registry (Phase 1 **M7**) | **Phase 5+** | Requires the ingestion service, the models and the validators (§P.3). |
| Creating `src/`, `tests/`, `.claude/skills/` | Phases 4 and 5 | RP11. |

**Phase 3C is not authorised by this document and must be requested separately.**

---

## Z. Phase 3B Execution Plan

**Not executed. Proposed commands only, provided now that the structure is decided.** Every command uses only `git`, `sha256sum`, `mkdir`, `rmdir` and POSIX shell — all verified present on this machine (§B.4 finding 6). Nothing requires Python, `ffmpeg` or `sqlite3`.

### Z.1 Pre-migration

```bash
# 0. Clean tree is a precondition, not a suggestion.
git status --porcelain          # must print nothing
git rev-parse --abbrev-ref HEAD # expect: master
git rev-parse HEAD              # expect: 59cbe494cdaef3a716283534b3bbea511c3c614d

# 1. Tag the frozen Phase 2 state. This is the rollback target.
git tag -a phase-2-freeze 59cbe49 -m "Phase 2 data architecture frozen; Phase 3B baseline"

# 2. Record the pre-migration hash of every tracked file. This is the migration's proof.
git ls-files -z | xargs -0 sha256sum > /tmp/pre-migration-hashes.txt
wc -l < /tmp/pre-migration-hashes.txt        # expect: 32

# 3. Work on a branch. master stays reachable and untouched.
git switch -c phase-3b-migration
```

### Z.2 Line endings first

`.gitattributes` must land **before** any move, so every later commit is normalised.

```bash
git config core.autocrlf false

cat > .gitattributes <<'EOF'
# Text is LF in the repository and LF in the working tree, on every platform.
# Load-bearing: Phase 2 §G.7 hashes authored YAML over file bytes.
* text=auto eol=lf

*.json  text eol=lf
*.jsonl text eol=lf
*.yaml  text eol=lf
*.yml   text eol=lf
*.md    text eol=lf
*.py    text eol=lf
*.txt   text eol=lf

*.pdf  binary
*.mp4  binary
*.wav  binary
*.mp3  binary
*.jpg  binary
*.jpeg binary
*.png  binary
*.webp binary
*.sqlite3 binary
EOF

git add .gitattributes
git add --renormalize .
git commit -m "Pin line endings to LF via .gitattributes"
```

Then the root ignore file:

```bash
cat > .gitignore <<'EOF'
# Secrets
.env
.env.*
!.env.example

# Derived, rebuildable, ephemeral
var/

# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Claude Code machine-local settings
.claude/settings.local.json

# OS
Thumbs.db
desktop.ini
.DS_Store
EOF

printf 'ANTHROPIC_API_KEY=\nHIGGSFIELD_API_KEY=\nMETA_ACCESS_TOKEN=\nMEDIA_ROOT=\n' > .env.example
git add .gitignore .env.example
git commit -m "Add root ignore rules and credential template"
```

### Z.3 Moves — one commit per concern

```bash
# --- sources ---------------------------------------------------------------
mkdir -p sources/books
git mv "sources/original-books/breakthrough-advertising-0887232981-9780887232985 (1)_compressed.pdf" \
       "sources/books/breakthrough-advertising.pdf"
git mv "sources/original-books/_OceanofPDF.com_The_brilliance_breakthrough_-_Eugene_schwartz.pdf" \
       "sources/books/brilliance-breakthrough.pdf"
rmdir sources/original-books sources/methodology 2>/dev/null || true
git commit -m "Move original books to sources/books with stable names (M1)"

# --- quarantine ------------------------------------------------------------
mkdir -p knowledge/_quarantine
git mv knowledge/methodology knowledge/_quarantine/methodology
git mv "knowledge/_quarantine/methodology/modulo-5-infraestructura-herramientas (1).md" \
       "knowledge/_quarantine/methodology/modulo-5-infraestructura-herramientas.md"
git commit -m "Quarantine methodology corpus, unmodified (M2, ADR-009)"

# --- media, still tracked at this point ------------------------------------
mkdir -p media
git mv samples media/_unregistered
git commit -m "Move sample media under the media root, awaiting registration"
```

### Z.4 Verify the moves **before** untracking anything

```bash
git ls-files -z | xargs -0 sha256sum > /tmp/post-move-hashes.txt

# Compare hash sets, ignoring paths: every hash present before must still be present.
cut -d' ' -f1 /tmp/pre-migration-hashes.txt  | sort > /tmp/pre.h
cut -d' ' -f1 /tmp/post-move-hashes.txt      | sort > /tmp/post.h
diff /tmp/pre.h /tmp/post.h && echo "MOVES CLEAN: all 32 contents preserved"
```

**Do not proceed past a failure here.** This is the last point at which rollback is a single `git switch master`.

### Z.5 Untrack media — the asymmetric step

```bash
git rm -r --cached media -q
cat > media/.gitignore <<'EOF'
*
!.gitignore
!README.md
EOF
git add media/.gitignore
git commit -m "Untrack media payloads; registry JSON remains canonical"

git ls-files media          # expect only: media/.gitignore
ls media/_unregistered/voices/chile/male | wc -l    # expect 3 — files still on disk
```

### Z.6 Scaffold

```bash
mkdir -p store config/styles incoming var
# READMEs, the nine placeholder registries and the remaining .gitignore files
# are written here (contents per §J.3 and §Y.2), then:
git add -A
git commit -m "Scaffold canonical store, config registries, ingestion and runtime roots"
```

### Z.7 Documentation and merge

```bash
# README.md rewritten; docs/MIGRATIONS.md created with this migration as entry 001.
git add README.md docs/MIGRATIONS.md
git commit -m "Rewrite README for the Phase 3 structure; open the migration log"

# Run the full validation checklist (§AB). Only then:
git switch master
git merge --ff-only phase-3b-migration
git tag -a phase-3b-complete -m "Repository migration complete and validated"
```

### Z.8 Optional, after merge

```bash
git gc --aggressive --prune=now    # compacts 136 MB of loose objects; changes no commit
```

---

## AA. Rollback Plan

**Phase 3B must be reversible, and rollback must not depend on deleting anything.**

### AA.1 The target

`phase-2-freeze` → `59cbe494cdaef3a716283534b3bbea511c3c614d`, tagged before the first migration command (§Z.1 step 1). Everything Phase 2 froze is reachable from it, permanently.

### AA.2 The mechanism

All work happens on `phase-3b-migration`. `master` is never modified until the validation checklist passes, so rollback before the merge is:

```bash
git switch master               # master is still at 59cbe49
git branch -D phase-3b-migration   # only after deciding to abandon
```

After a merge, rollback is a **revert**, not a reset — the history stays intact and the reversal is itself attributable:

```bash
git revert --no-commit <merge-sha>
git commit -m "Revert Phase 3B migration; see docs/MIGRATIONS.md"
```

`git reset --hard phase-2-freeze` is available and is **not** recommended: on a shared branch it discards commits other clones may hold, and the design's whole posture is that destructive deletion is not the normal mechanism.

### AA.3 The one asymmetry, and how it is closed

`git rm --cached media` untracks payloads. A later `git revert` restores the *index entries* for `samples/**` but the physical files now live at `media/_unregistered/**`, so git will report them deleted from `samples/`. Restoring the physical files is one command, and it works because the blobs never left history:

```bash
git checkout phase-2-freeze -- samples/
```

Three properties keep this safe: the untracking step runs **last** (§Z.5), it runs only after the hash verification of §Z.4 has passed, and the blobs remain in history at `92ec3eb` regardless of what any later commit does. This is the concrete reason REPO_ADR-017 refuses a history purge: **the purge would destroy the mechanism that makes this rollback possible.**

### AA.4 What rollback cannot restore

Nothing, for Phase 3B as designed — every operation is a move, an untrack, or a new file, and all three are revertible. This property is a *consequence* of deferring M3/M5 to Phase 3C (§Y.4): a content edit to a knowledge file would be revertible in git but would have invalidated any hash pinned in the interim. Phase 3C must carry its own rollback design, and it should run when no pinned hashes exist yet — which is now.

---

## AB. Migration Validation Checklist

Every check below is mechanical and runnable with the tooling verified present (§B.4 finding 6). Phase 3B is not complete until all fifteen pass.

| # | Check | Command / criterion | Pass |
|---|---|---|---|
| 1 | Clean tree before starting | `git status --porcelain` prints nothing | ☐ |
| 2 | Zero missing tracked content | Hash-set diff of §Z.4 is empty — all 32 pre-migration contents still present | ☐ |
| 3 | Pure moves are hash-identical | Each of the 27 moved files: `sha256sum` equals its pre-migration value | ☐ |
| 4 | Expected new paths exist | `sources/books/{breakthrough-advertising,brilliance-breakthrough}.pdf`; `knowledge/_quarantine/methodology/` with 8 files; `media/_unregistered/` with 15 files; `store/`, `config/`, `incoming/`, `var/` | ☐ |
| 5 | Old paths absent | `samples/`, `knowledge/methodology/`, `sources/original-books/`, `sources/methodology/` all absent | ☐ |
| 6 | Rename detection survives | `git log --follow` resolves history for each renamed file | ☐ |
| 7 | **No canonical file is ignored** | `git ls-files store config knowledge sources docs \| xargs -r git check-ignore -v` prints **nothing** | ☐ |
| 8 | **No large runtime output is tracked** | No tracked file exceeds 1 MB (`git ls-files \| xargs -r ls -l`) — after untracking media the largest is `docs/PHASE_2_DATA_ARCHITECTURE.md` at 330 KB | ☐ |
| 9 | Media untracked but present | `git ls-files media` returns only `media/.gitignore`; all 15 payloads on disk with matching hashes | ☐ |
| 10 | Line endings uniform | `git ls-files --eol` shows `w/lf` for every text file and `-text` only for genuine binaries — including `modulo-2`, whose heuristic classification is now explicit (§B.5) | ☐ |
| 11 | **No duplicate canonical knowledge** | No basename appears both inside and outside `knowledge/_quarantine/`; each Schwartz file exists in exactly one location | ☐ |
| 12 | **No raw source silently promoted to trusted knowledge** | `sources/` contains only the two books; nothing moved from `sources/` into `knowledge/`; the three methodology PDFs are in `_quarantine/`, not `sources/` | ☐ |
| 13 | **Reference media retains reference-only status** | `store/assets/` is empty — no asset record exists, so nothing has been registered, attested or promoted. Phase 2 §S.4's fifteen `REFERENCE` assets remain unmade, which is the correct state before Phase 5 | ☐ |
| 14 | Path/content identity agreement | Vacuous now (`store/` is empty) — **but the check is defined and belongs to every later phase**: for every canonical file, the identifier in the path equals the identifier in the content (§X.2) | ☐ |
| 15 | Phase documents intact and readable | `sha256sum` of `PRE_FLIGHT_AUDIT.md`, `docs/PHASE_1_SYSTEM_DESIGN.md`, `docs/PHASE_2_DATA_ARCHITECTURE.md` identical to `59cbe49`; all render | ☐ |

Two structural checks that apply from Phase 3B onward and are stated here so they are not invented later:

| # | Check | Criterion |
|---|---|---|
| 16 | Config registry list is closed | `ls config/*.yaml \| wc -l` equals **9**, and the filenames match the whitelist of Phase 2 §B.1 exactly (§J.1) |
| 17 | No case-only path collisions | No two tracked paths are equal when lowercased — `core.ignorecase=true` makes such a pair unrepresentable on this machine and corrupting on a case-sensitive one (§AC.1) |

---

## AC. Windows / Portability Review

### AC.1 Windows

| Hazard | Status under this design |
|---|---|
| **`MAX_PATH` (260)** | Longest *designed* canonical path: `store/campaigns/CMP-<16>-<6hex>/creatives/CRE-<16>-<6hex>-NN/v10.json` ≈ **83 characters**. Repository root here is 42. Total ≈ 125. **Budget: canonical relative paths ≤ 120, repository root ≤ 100.** Enforced by the slug caps in X.4 (brand ≤ 16, product ≤ 24). `core.longpaths` is not set and is not needed. |
| **Case-insensitive filesystem** (`core.ignorecase=true`) | No path anywhere distinguishes two entities by case alone. Identifier prefixes are uppercase (`CMP-`, `CRE-`) and slugs lowercase, so paths are mixed-case but never case-*dependent*. Validation check 17. |
| **Symlinks unavailable** (`core.symlinks=false`) | The design uses none. No `latest` symlink — Phase 2 §G.5 makes `latest` a derived convenience anyway, and INV-12 forbids resolving a reference through it. |
| **Reserved device names** (`CON`, `PRN`, `AUX`, `NUL`, `COM1-9`, `LPT1-9`) | Checked, and one near-miss is worth recording: `CONCEPT_ID` is `CON-…`. Windows reserves the *exact* base name `CON` and `CON.<ext>`, not `CON-acme-3f8b21-03`, so no collision exists — **and in any case concepts are embedded in the Experiment Plan (Phase 2 §D.1) and get no file at all.** The hazard does not materialise on either count. |
| **Illegal characters** (`: * ? " < > \|`) | `RUN_ID` uses compact UTC (`RUN-20260904T1132Z-a91c4e`) with no colons — a Phase 2 format choice that happens to be filename-safe, noted so nobody "improves" it into ISO-8601 with separators. No designed path contains any illegal character. |
| **Trailing dots and spaces** | Forbidden in all designed names; all are ASCII `[A-Za-z0-9._-]`. Legacy filenames with spaces and one non-ASCII character survive the migration under quarantine, quoted in every command (§Z.3). |
| **Deep nesting** | Maximum designed depth is 5 below `store/` (`campaigns/<CMP>/creatives/<CRE>/v3.json`). The flat, scope-keyed layout of §F.2 is what keeps it there — a `brands/<b>/products/<p>/campaigns/<c>/…` hierarchy would have added ~45 characters and two levels to every path for information the identifiers already carry. |
| **Antivirus / sync interference** | Advisory: exclude `var/` and `media/` from real-time scanning and from OneDrive-style sync. Both hold large, frequently rewritten files, and a sync client that rewrites a file underneath a running index build is a corruption source. |

### AC.2 Portability between computers

| Requirement | How it is met |
|---|---|
| No absolute paths in canonical records | RP10. `ASSET.path` is media-root-relative; `source_files[]` is repo-relative; every artefact reference is a logical address (Phase 2 §E.5). No drive letter, no `C:\Users\…`, anywhere. |
| `clone` / `pull` / `push` work | Everything canonical is tracked text. Total tracked size after migration ≈ 700 KB plus 9 MB of books. History carries 136 MB of media blobs — one-time clone cost, no file over 100 MB, no GitHub limit engaged. |
| Byte-identical config hashes across machines | **`.gitattributes` with `eol=lf`.** Without it a second Windows clone under `core.autocrlf=true` produces CRLF and different hashes for byte-identical policy (§AD R3). This is the single most important line in the migration. |
| Machine-specific configuration stays local | `.env` (ignored), `.claude/settings.local.json` (ignored), `MEDIA_ROOT` (environment). |
| Media | **The known gap** (§O.5): a clone brings the complete canonical store and zero payloads. `media check` reports what is missing; the operator copies out of band. |
| SQLite | Never transferred. Rebuilt on each machine from the canonical store (Phase 2 §AA). A missing index is not an error. |

**GitHub setup is not solved here and is not required by anything in this design.** The repository is push-ready; whether and when to push is a separate decision.

### AC.3 Secrets

**No secret may enter canonical JSON, committed config YAML, documentation, a knowledge file, or a run manifest.**

| Item | Location |
|---|---|
| `.env.example` | **Tracked.** Names only: `ANTHROPIC_API_KEY`, `HIGGSFIELD_API_KEY`, `META_ACCESS_TOKEN`, `MEDIA_ROOT`. Never a value, never a placeholder that looks like one. |
| `.env` | **Ignored.** Per machine. Created by the operator. |
| `.claude/settings.local.json` | **Ignored.** |
| Runtime credential (Phase 1 §D.1, ADR-033) | Resolved by the SDK's credential chain from the environment. Not the operator's interactive session, never committed. |
| Credential *identity* | The RUN head records `actor.credential_identity` — an identity string such as `svc-orchestrator@org`, which is not a secret and is required for attribution (Phase 2 §W.1). The distinction between recording *who* and recording *what proves it* is the whole rule. |

**No secret, key, token or `.env` file is created by Phase 3A or Phase 3B.** A pre-commit secret scan is a reasonable Phase 5 addition and is not designed here.

---

## AD. Repository Risks

| # | Risk | Level | Mitigation | Residual |
|---|---|---|---|---|
| **R1** | **Media payloads are the only unbacked data in the system.** Once `media/` is ignored, a generated video exists in one place on one machine. | **HIGH** | `content_sha256` on every record makes loss *detectable*; `media check` reports missing and corrupt payloads; the 15 existing samples remain in git history. | **Real and accepted.** Detection is not backup. Requires an operator backup habit — approval item 2. |
| **R2** | **Line-ending drift invalidates config hashes across machines.** Authored YAML is hashed over file bytes; a CRLF checkout changes every hash. | **HIGH → LOW** | `.gitattributes` with `eol=lf`, `core.autocrlf=false`, applied as the first migration commit; validation check 10. | Low. An editor that writes CRLF against `.gitattributes` is caught on the next `git status`. |
| **R3** | **A placeholder registry reads as authored policy.** An empty `deny_list.yaml` blocks nothing. | **HIGH → LOW** | `status: PLACEHOLDER_NOT_AUTHORISED`; a run refuses to start against any placeholder it pins (§J.3). | Low. Fail-closed by construction. |
| **R4** | **The allocator reads a stale SQLite index instead of canonical files**, double-allocating an ordinal. | **MEDIUM** | §F.4 rule 2, stated as a repository-layer invariant for Phase 5; INV-118 makes reuse a violation; `rebuild --verify` surfaces the divergence. | Medium until Phase 5 code review enforces it. |
| **R5** | **An impure renderer makes staleness meaningless.** A timestamp in a render moves the manifest hash on every gate. | **MEDIUM → LOW** | §Q.3 states purity as a requirement; a render is regenerated and byte-compared in CI. | Low. |
| **R6** | **`media/_unregistered/` becomes permanent.** Files sit unregistered for months and the staging area becomes a second media convention. | **MEDIUM** | It is empty once Phase 5's registration runs; `media check` reports its contents as `MEDIA_ORPHAN`. | Medium — a scheduling risk, not a design one. |
| **R7** | **136 MB of history on first push / slow clones.** | **LOW** | No file exceeds GitHub limits; `git gc` compacts loose objects; the cost is one-time per clone. | Low. Accepted rather than fixed, because the fix destroys rollback (REPO_ADR-017). |
| **R8** | **Long brand or product slugs push paths toward `MAX_PATH`.** | **LOW** | Slug caps in X.4; path budget in AC.1. | Low. |
| **R9** | **Quarantine bypass** — a file lands in `_quarantine/` without front matter and defaults to permitted. | **MEDIUM → LOW** | Two-layer enforcement: metadata is authoritative, the path check fails closed for exactly the case metadata misses (§N.3). | Low. |
| **R10** | **A manual repair of a canonical file passes unnoticed.** | **LOW** | The store is git-tracked, so every edit is a diff; `rebuild --verify` catches folded-state divergence; check 14 catches path/content identity mismatch. | Low. Phase 2 §AA.2 already makes this the sharpest integrity signal in the system. |

---

## AE. Simplification Pass

Run against the brief's six questions: *Does V1 need this boundary? Does it protect canonical truth? Does it simplify Git, retrieval, production, testing?*

### AE.1 Removed before proposing

| Considered | Removed because |
|---|---|
| `knowledge/narrative/` (Phase 1 §I) | Phase 2 §B.1 makes `narrative_library` one of the nine config registries. Two homes for one object. |
| `knowledge/language/cl/` (Phase 1 §I) | Phase 2 §J.4 makes customer language an `OBSERVATION` in the Evidence Ledger, with a source and a locator. It is evidence, not a document. |
| `sources/external/` (Phase 1 §I) | Phase 2 §S makes a snapshot an `ASSET` with `asset_type: SOURCE_SNAPSHOT`, stored under `media/`. |
| `store/campaigns/<CMP>/campaign.json` | Campaign is not in Phase 2 §G.1's list of immutable entity records. The Campaign Brief creates it; a record would be the dual write Correction 11 removed. |
| A top-level `reviews/` root | Renders belong beside the scope they describe, and a pure renderer makes an exception list unnecessary (§Q.3). One fewer top-level directory and one fewer rule. |
| A top-level `schemas/` root | Generated output belongs in `var/` (§T). |
| A top-level `prompts/` root | Prompt templates are runtime inputs shipped with the code (§R). |
| `store/registry/` for style profiles | `config/styles/` is closer to the authoring workflow and does not disturb the nine-file rule (§J.4). |
| `media/{videos,audio,images,generated}/` | Type, role and state are record fields and index columns. A path-based classification can disagree with the record and would require moving files when state changes. |
| Sharding `observations/` and `claims/` | ~61 and ~22 per campaign (Phase 2 §AD.7). Sharding solves a problem V1 does not have, and any later change is a recorded migration. |
| Empty `src/`, `tests/`, `tests/golden/<category>/`, `.claude/skills/` | RP11. A directory is created by the phase that fills it. |
| `sources/methodology/` | Empty, and its intended contents belong in quarantine (§B.4 finding 1). |

**Twelve boundaries removed.** Three of them (`knowledge/narrative/`, `knowledge/language/cl/`, `sources/external/`) came from Phase 1 and were absorbed by Phase 2's later, frozen model — found by reading the two documents against each other rather than by taste.

### AE.2 Kept despite pressure to cut

| Kept | Why it survives |
|---|---|
| `sources/` (2 files) | The raw/derived boundary is frozen Phase 1 architecture, and a resolvable `source_files[]` path is what makes the `DERIVED_VERIFIABLE` tier checkable rather than asserted. |
| `incoming/` (empty) | It is a provenance declaration, not a convenience. Collapsing it into `media/_unregistered/` would give the fifteen samples the wrong `origin.kind` and contradict Phase 2 §S.4 (§P.2). |
| `media/_unregistered/` | The gap between "moved in Phase 3B" and "registered in Phase 5" is real and has to live somewhere legible. |
| `config/styles/` | Style profiles are authored YAML that is not one of the nine; giving them a subdirectory is what keeps the nine-file rule literal. |
| `var/` as a single root with six children | Six children of one ignored root cost nothing — they are never navigated, only written to — and merging them would put the SQLite index in the same directory as temp downloads. |
| The `ledger/` level inside a product | Phase 2 §J calls the Evidence Ledger *one store*; four sibling directories at the product root would lose that grouping and mix ledger records with artefacts. |

---

## Contradiction Scan

Run mechanically against the eleven checks the brief specifies.

| # | Check | Result |
|---|---|---|
| 1 | **No canonical object has two authoritative paths** | **Clean.** Narrative patterns: `config/narrative_library.yaml` only (`knowledge/narrative/` not created). Customer language: ledger observations only (`knowledge/language/cl/` not created). Source snapshots: `media/` as assets only (`sources/external/` not created). Style profiles: `config/styles/` only. Each artefact version: one `v<n>.json`, created exclusively. Renders are derived and marked. |
| 2 | **Raw source and structured knowledge are separated** | **Clean.** `sources/` holds two original books, tracked and never edited. `knowledge/` holds derived, provenance-tagged material. The three methodology PDFs go to `knowledge/_quarantine/` and *not* to `sources/`, because §B.4 establishes they are Google Docs exports of the derived corpus, not upstream documents. |
| 3 | **Binary payload and Asset Registry metadata are separated** | **Clean.** Record: `store/assets/<2hex>/AST-….json`, canonical, tracked. Payload: `media/<2hex>/AST-….<ext>`, ignored, referenced by media-root-relative `path` plus `content_sha256`. |
| 4 | **No ignored path contains unique canonical truth** | **One approved exception, named rather than passed.** `media/**` is ignored and holds payloads that exist nowhere else. Phase 2 §AI.1 item 4 requires it; the Asset Registry *record* — the canonical object — is tracked. Recorded as R1 and as approval item 2. No canonical **record**, artefact, event log or config file is in an ignored path (validation check 7). |
| 5 | **SQLite remains fully rebuildable** | **Clean.** `var/index/`, git-ignored, never committed. Every input it folds — records, event logs, gate decisions, config — is tracked under `store/` and `config/`. A missing database is not an error (Phase 2 §AA.2). |
| 6 | **Event log paths match their frozen scopes** | **Clean.** `evidence` per product, `campaign` per campaign, `run` per run, `asset` global — each `events.jsonl` sits at the root of the directory that *is* its scope (§I.1). |
| 7 | **Entity identifier allocation does not depend on event-log layout** | **Clean, and tabulated in §F.4.** Every ordinal reads canonical records — filenames for `OBS`/`CLM`/`EXT`/`GAT`/`CRE`, file contents across *all* versions for `INS`/`HYP`/`CON`/`EXP`. No entry reads a `.jsonl`. `event_seq` is a line number and numbers only events. |
| 8 | **All nine config registries have exactly one authoritative location** | **Clean.** `config/<name>.yaml`, one file each, enforced by `ls config/*.yaml \| wc -l == 9` plus a name whitelist (validation check 16). `config/styles/` is a subdirectory and does not disturb the glob. |
| 9 | **Relative-path design works on another computer** | **Clean for records; one known gap for payloads.** No absolute path in any canonical record. `.gitattributes` guarantees byte-identical config hashes. Media requires an out-of-band copy — stated in §O.5, R1 and approval item 2, not concealed. |
| 10 | **No existing source is moved in Phase 3A** | **Clean.** Zero files moved, renamed, deleted or edited. `git status` was clean at the start of this phase and is clean at its end, except for this document. Every move in §Y is designed and unexecuted. |
| 11 | **No Phase 4 Skill has been implemented** | **Clean.** No `.claude/` directory created, no `SKILL.md` written, no skill directory scaffolded. §R decides a boundary and names five directories that Phase 4 will create. |

**Two additional checks, run because Phase 2 §AJ.8.8 recommends re-running the scan rather than trusting a fix:**

| # | Check | Result |
|---|---|---|
| 12 | Does any Phase 3 decision alter a Phase 2 content hash? | **No.** JSONL line serialisation (§I.2 rule 3) governs event lines, which carry no `content_hash` and are addressed by `(log, event_seq)`. Artefact serialisation (§G.7) is untouched. Config hashing is *specified* where Phase 2 was silent, and `.gitattributes` makes the bytes it hashes stable rather than changing which bytes they are. |
| 13 | Does any Phase 3 decision reopen a frozen ADR? | **No.** Phase 1 ADR-004 (git-tracked JSON as system of record), ADR-009 (quarantine), ADR-012 (three style profiles), ADR-013/014 (voices), ADR-035 (asset states) and Phase 2 DATA_ADR-026/032/033 are all *implemented* by this layout, none reopened. The three Phase 1 §I directories not created are Phase 1 *proposals* superseded by Phase 2's frozen model, not ADRs. |

---

## AF. Repository ADRs

All `PROPOSED` unless inherited from a frozen Phase 1 or Phase 2 decision.

| ID | Question | Recommendation | Rationale | Trade-off | Status |
|---|---|---|---|---|---|
| **REPO_ADR-001** | Name of the canonical data root | **`store/`** | The vocabulary Phases 1 and 2 already use ("artefact store", "canonical stores"); short; makes "is it in the store?" the operator's question | `data/` would be more conventional for outsiders | PROPOSED |
| **REPO_ADR-002** | How the store is organised | **By allocation scope — `brands/`, `products/`, `campaigns/`, `runs/`, `assets/`** | The scopes are Phase 2's, not invented. Makes single-writer-per-scope a visible filesystem property; avoids directory-per-noun | Cross-scope queries need the index — which exists for exactly that | PROPOSED |
| **REPO_ADR-003** | Versioned artefact layout | **Directory per artefact identity; `v<n>.json` inside** | Version enumeration is a directory read; "no silent overwrite" becomes create-exclusive; everything under an artefact directory is canonical | One directory per artefact identity | PROPOSED |
| **REPO_ADR-004** | Event log physical representation | **JSONL, one file per log instance, `event_seq` = 1-based line number** | Wins 7 of 9 audit criteria (§I.1); the merge-conflict criterion favours it precisely because a forbidden concurrent write should fail loudly | Two clones appending conflict — which is the wanted behaviour | PROPOSED |
| **REPO_ADR-005** | Serialisation of an event line | **Compact canonical JSON, sorted keys, one line, LF-terminated** | Refines §G.7 where it is silent; an event has no `content_hash`, so no existing hash changes | A second serialisation profile to implement (two lines of code) | PROPOSED |
| **REPO_ADR-006** | Where a scope-ordinal reads its `max` | **Canonical files only, per the §F.4 table; never SQLite; across *all* artefact versions** | The index may be stale or absent (§AA.2); INV-118 forbids reuse, so the union across versions is required | Allocation reads several files instead of one query | PROPOSED |
| **REPO_ADR-007** | Location of the nine config registries | **`config/<name>.yaml`, exactly nine `*.yaml` at that level** | Matches Phase 2's `config/evidence_policy@v4` reference form 1:1; turns INV-115 into `ls \| wc -l` | Non-registry files must avoid the `.yaml` extension at that level | PROPOSED |
| **REPO_ADR-008** | How config versions and hashes are pinned | **`version:` header in the file; `sha256` over raw file bytes; history lookup by hash** | Answers Phase 2 §AI.1 item 6 without adding a field to the frozen RUN head; a forgotten bump is detectable | Recovering an old version is a history search, not a path | PROPOSED |
| **REPO_ADR-009** | Behaviour of an unauthored registry | **`status: PLACEHOLDER_NOT_AUTHORISED`; a run refuses to start against it** | An empty `deny_list.yaml` blocks nothing — silent and permissive is the worst failure mode available | The operator must author nine files before the first run | PROPOSED |
| **REPO_ADR-010** | Where Style Profiles live | **`config/styles/STY-….yaml`, pinned per artefact via `inputs[]`** | Authored YAML, close to policy, in a subdirectory so the nine-file rule is literal; not a tenth run-level dependency, so INV-115 is not engaged | Looks adjacent to the nine and needs the distinction stated | PROPOSED |
| **REPO_ADR-011** | Knowledge provenance mechanism | **YAML front matter only; no central authored registry** | Provenance must travel with content into the prompt (P9); losing it should require editing the file that carries the content | A corpus-wide query needs a derived index | PROPOSED |
| **REPO_ADR-012** | Section-granularity provenance | **An optional `sections:` key in the same front matter** | Phase 1 §I found modules mixing cited material with unsourced speculation; one file, one source of truth | Authoring cost per file (Phase 3C) | PROPOSED |
| **REPO_ADR-013** | Quarantine destination, and whether PDFs separate | **`knowledge/_quarantine/methodology/` — PDFs and Markdown together** | The three PDFs are Google Docs exports of the same derived corpus (§B.4); there is no upstream to separate. One directory, one retrieval policy, path-enforceable | The word "PDF" no longer implies "source" in this repository | PROPOSED |
| **REPO_ADR-014** | `knowledge/narrative/` and `knowledge/language/cl/` | **Not created — superseded by Phase 2** | Narrative patterns are a config registry; customer language is ledger observations. Either directory would be a second authoritative home | Phase 1 §I's tree is not reproduced literally | PROPOSED |
| **REPO_ADR-015** | `sources/external/` | **Not created — snapshots are assets** | Phase 2 §S: `asset_type: SOURCE_SNAPSHOT`, referenced by `SOURCE.snapshot_asset_id` | Same | PROPOSED |
| **REPO_ADR-016** | Media addressing | **`media/<2hex>/AST-<12hex>.<ext>` — id-addressed, sharded, ignored** | Two records may share bytes and differ in rights (§E.4); content-addressing would merge them. Rights attach to provenance, not to bytes | Duplicate bytes when one file is registered twice | PROPOSED |
| **REPO_ADR-017** | The 136 MB of media already in history | **Retained. No history rewrite.** | The frozen Phase 2 commit is the rollback target, and the media blobs are what make physical restoration possible (§AA.3). A purge destroys the safety net to save disk | Every clone carries 136 MB | **PROPOSED — needs user approval** |
| **REPO_ADR-018** | Ingestion entry points | **Two: `incoming/` ⇒ `USER_UPLOAD`; `media/_unregistered/` ⇒ `REPOSITORY`** | `origin.kind` is the sole determinant of an asset's initial state (§S.2), and the fifteen samples must fold to `REFERENCE` (§S.4). One entry point would produce the wrong rights position | A second directory, and one of the two path-carries-policy exceptions | PROPOSED |
| **REPO_ADR-019** | Derived Markdown renders | **Inside the canonical root at `<scope>/reviews/`, in the source manifest, renderer must be pure** | Phase 2 §G.7 requires them tracked; an exception list in the manifest rule would rot. Purity makes the exception unnecessary | The renderer acquires a hard requirement, testable by byte-comparison | PROPOSED |
| **REPO_ADR-020** | Derived / runtime root | **`var/`, fully git-ignored; SQLite at `var/index/`** | Deleting it must cost only time. A committed index could be mistaken for truth | Six ignored subdirectories, never navigated | PROPOSED |
| **REPO_ADR-021** | Generated JSON Schema | **`var/schemas/`, not tracked** | Tracking creates drift that needs a CI job to police; not tracking makes drift impossible. The schema is a pure function of a tracked commit | Reviewers see model diffs, not schema diffs | PROPOSED |
| **REPO_ADR-022** | Code root | **`src/creative_os/`, created in Phase 5** | src-layout forces an installed package so imports match production; `creative_os` is a valid identifier | One extra level | PROPOSED |
| **REPO_ADR-023** | Claude / Skill boundary | **`.claude/skills/` for the five Skills; runtime prompts under `src/creative_os/prompts/`; knowledge stays in `knowledge/`** | Skills are procedure, prompts are pinned runtime inputs, knowledge is retrieved content. Phase 1 §D.1 separates development environment from runtime | Skills sit in a tool-named directory | PROPOSED |
| **REPO_ADR-024** | Line endings | **`.gitattributes` with `eol=lf`; `core.autocrlf=false`; renormalise once** | Phase 2 §G.7 hashes authored YAML over file bytes; without this, a second Windows clone produces different hashes for identical policy | One normalisation commit touching every text file | **PROPOSED — highest priority** |
| **REPO_ADR-025** | Phase documents and `PRE_FLIGHT_AUDIT.md` | **Do not move** | Phase 2 §AI.1 item 7; cited by path across three documents; moving changes no content and breaks every reference | `docs/` mixes historical and current documents | **ACCEPTED (inherited from Phase 2)** |
| **REPO_ADR-026** | Scope of Phase 3B | **Moves and scaffolding only. Knowledge front matter (M3) and section tagging (M5) become Phase 3C** | Keeps 3B's central validation total — *every moved file's hash is unchanged* — and keeps rollback free of content edits | Knowledge files remain untagged until 3C is authorised | **PROPOSED — needs user approval** |
| **REPO_ADR-027** | Recording structural change | **`docs/MIGRATIONS.md`, append-only** | §AA hashes relative paths, so a pure move changes the manifest hash; the log makes that attributable rather than alarming | One file to maintain, forever | PROPOSED |
| **REPO_ADR-028** | Secrets | **`.env.example` tracked (names only); `.env` ignored; credential *identity* recorded, credential never** | Phase 1 §D.1 / ADR-033. Recording who acted is required; recording what proves it is forbidden | Per-machine setup step | PROPOSED |

**28 repository ADRs. No Phase 1 or Phase 2 ADR reopened.**

---

## AG. Decisions Requiring User Approval

Seven. Each is a genuine choice with a real cost, not a request to confirm something already settled.

| # | Decision | Recommendation | What you are accepting |
|---|---|---|---|
| **1** | **Canonical data root named `store/`** (REPO_ADR-001) | `store/` | Every canonical path begins `store/`. Changing it later is a one-command rename plus one migration-log entry, but it moves every path in the manifest. Cheapest to settle now. |
| **2** | **Media payloads are git-ignored** (REPO_ADR-016, Phase 2 §AI.1) | Accept, with a backup habit | A clone brings the complete canonical store and **zero media**. Loss becomes detectable, not prevented. This is the design's one accepted violation of "nothing ignored is the only copy" and it is inherited from Phase 2, not chosen here. |
| **3** | **Do not purge the 136 MB of media from git history** (REPO_ADR-017) | Do not purge | Every clone carries 136 MB. The alternative rewrites history, invalidates the frozen `59cbe49`, and destroys the mechanism that makes physical rollback possible (§AA.3). **If you want a purge, it must happen before the first push and before Phase 3B, and it needs its own authorisation.** |
| **4** | **Split M3/M5 out of Phase 3B into a separate Phase 3C** (REPO_ADR-026) | Split | Phase 3B stays a pure, fully hash-verifiable move. Knowledge files carry no provenance front matter until 3C is authorised — so the quarantine is enforced by path alone in the interim, which §N.3 designs for but which is one layer, not two. |
| **5** | **`.gitattributes` + `core.autocrlf=false` + one renormalisation commit** (REPO_ADR-024) | Do it, first | One commit touches the working-tree bytes of every tracked text file. Without it, config hashes differ between your two computers and the reproducibility contract silently fails. |
| **6** | **Reserve, do not scaffold: `src/`, `tests/`, `.claude/skills/`** (RP11) | Reserve | After Phase 3B the repository has eight top-level directories and no empty promises. The names are decided; the directories arrive with their first file. |
| **7** | **Slug caps — brand ≤ 16, product ≤ 24 characters** (X.4) | Accept | Keeps every canonical path under the 120-character budget on Windows. Registry slugs are immutable, so a cap that is too tight is expensive to discover later. |

**No decision in this document depends on GitHub, Git LFS, cloud storage, an API credential or an installed runtime.** All seven are answerable now.

---

## AH. Phase 4 Handoff Requirements

Phase 4 designs Skills. What it inherits and what it must respect:

### AH.1 Phase 4 inherits, unchanged

- **`.claude/skills/<skill-name>/SKILL.md`** as the location for the five Skills of Phase 1 §E — `product-intelligence`, `market-intelligence-cl`, `creative-strategist`, `script-engine`, `compliance-reviewer`. Phase 4 creates the directory.
- **The three rules of §R**, restated because each is a defect if broken: no Skill embeds policy (it belongs in one of the nine registries — INV-115); no Skill writes to `store/` or emits an identifier (INV-06); no Skill reaches `knowledge/_quarantine/`, and the enforcement is the retrieval layer's, not the Skill's prose.
- **Knowledge is retrieved, never embedded.** A retrieval hit carries `knowledge_id`, `tier` and `retrieval_policy` from front matter into the prompt (Phase 2 P9). A Skill that pastes Schwartz into its own body makes it unhashable, unversionable and unpinnable in the RUN head.
- **`schwartz_integration_map.md` is `DESIGN_INPUT` with `retrieval_policy: excluded`.** It is an architecture document about the other two and must not be retrieved at generation time (Phase 1 §D). Phase 4 may read it; no Skill may.
- **Skill versions are pinned in the RUN head** (`skills: { script-engine: "1.2.0" }`), so a Skill needs a version string and a discipline for bumping it.

### AH.2 Phase 4 must decide

1. Whether prompt templates are Skill resources or runtime files. This document places pinned prompt templates under `src/creative_os/prompts/` (§R) because they are hashed run inputs; if Phase 4 finds a Skill needs its own resources, they belong beside the `SKILL.md` and must be hashed into the same pinning.
2. The `SKILL.md` internal structure and where the Skill/orchestrator boundary falls for each of the five — Phase 1 §D already classifies every component, so this is application, not re-litigation.
3. How a Skill declares which knowledge resources it consumes, so the RUN head's `knowledge` map can be assembled from declarations rather than from observation.

### AH.3 What Phase 4 must not do

Create no directory under `store/`, `config/`, `media/` or `var/`. Author no config registry content. Move no file. Write no Python. Register no asset. The repository migration (Phase 3B) is a separate authorisation and, at the time of writing, has not been granted.

---

## Compliance with Phase 3A constraints

| Constraint | Status |
|---|---|
| `docs/PHASE_1_SYSTEM_DESIGN.md` read before designing | ✅ Full document, treated as frozen |
| `docs/PHASE_2_DATA_ARCHITECTURE.md` read before designing | ✅ Full document, treated as frozen |
| `PRE_FLIGHT_AUDIT.md` unmodified and not moved | ✅ Not opened for writing |
| Repository inspected read-only; PRE_FLIGHT inventory not assumed current | ✅ §B — fresh enumeration, 32 tracked files, sizes, config, history, PDF metadata |
| No repository migration executed | ✅ Designed in §Y–§Z, unexecuted |
| No file moved, renamed, deleted or quarantined | ✅ `git status` clean apart from this document |
| No knowledge file modified | ✅ |
| No source file modified | ✅ |
| No Skill created; no `.claude/skills/` implementation | ✅ Boundary only (§R) |
| No orchestrator implemented | ✅ |
| No Python application code | ✅ Boundary only (§S) |
| No Pydantic models | ✅ Location only (§T) |
| No SQLite database built | ✅ Location only (§Q.1) |
| No dependencies installed | ✅ |
| No Higgsfield integration | ✅ |
| No Meta API calls | ✅ |
| No production data created | ✅ No asset registered, no identifier minted |
| Phase 3B not started | ✅ |
| Phase 4 not started | ✅ |
| Only `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` created or modified | ✅ |
| Frozen Phase 2 constraints not reopened | ✅ Contradiction scan, checks 12–13 |
| Contradiction scan run against all eleven specified checks | ✅ Contradiction scan — clean, with one named and approved exception (check 4) |
| Simplification pass run | ✅ §AE — twelve boundaries removed |

**Phase 3A ends here. Phase 3B is not authorised and has not been started. Phase 4 is not authorised and has not been started.**
