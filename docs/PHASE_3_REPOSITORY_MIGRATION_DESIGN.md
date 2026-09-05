# PHASE 3A — REPOSITORY & MIGRATION DESIGN
## Creative Experimentation OS — Chile

**Date:** 2026-09-04
**Revision:** 5 — four external audit correction passes applied (see **§AI**): twelve design-level corrections; then seven final-executability corrections plus one operational update; then seven final micro-fixes; then two validation exit-status fixes plus one tooling-wording correction. Twenty-eight numbered corrections/fixes raised, twenty-eight accepted.
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

**3. The source manifest is defined by canonical file *class*, not by root membership — corrected in this pass (§AI.7 Fix 21).** Phase 2 §AA hashes a manifest of stable relative paths, and an exception list is exactly what makes such a rule rot. The first executability pass still said *"every file under `store/` and `config/`"*, and a final review caught what that literally implies: Phase 3B itself scaffolds `store/README.md`, `config/README.md` and `config/styles/README.md` as operator documentation, and none of the three is canonical system truth. "Every file under these roots" was never quite true the moment those files existed. The fix is not a path-by-path exception list — that is exactly the kind of rule the design refuses elsewhere — but a **structural class rule**, mechanical by file extension:

| Root | Canonical (in the manifest) | Not canonical (tracked, but excluded by class) |
|---|---|---|
| `store/` | every `*.json` (entity/artefact records) and every `*.jsonl` (event logs) | `README.md` and any other non-`.json`/`.jsonl` file |
| `config/` | the nine top-level `*.yaml` registries, and every `config/styles/*.yaml` registry entity | `README.md` and any other non-`.yaml` file |

The rule is *"a `.json` or `.jsonl` under `store/`, or a `.yaml` under `config/`"* — a file-extension test any implementation can run without a list of paths to check against, and one that never needs updating when a new `README.md` is added anywhere in either tree. Revision 1 also kept derived Markdown renders inside `store/` and paid for it with a requirement — *the renderer must be pure, or staleness becomes meaningless.* The audit was right that this was the wrong trade: a renderer upgrade would mark the index stale with no canonical data changed. Renders now live in a top-level `reviews/`, git-tracked as Phase 2 §G.7 requires and **outside the manifest** — which the class rule states without needing to say so separately, since nothing under `reviews/` is a `.json`/`.jsonl` under `store/` or a `.yaml` under `config/` in the first place. The purity requirement survives as a reproducibility property of the renderer; it is no longer load-bearing for index staleness (§Q.3, REPO_ADR-019 revised).

**4. Every canonical path is a total function of identifiers.** `store/campaigns/CMP-acme-3f8b21/creatives/CRE-acme-3f8b21-07/v3.json` contains no human-chosen label, so **no canonical file ever needs renaming** and a rename can therefore never change domain identity. Where a path *does* carry meaning it is stated as a deliberate, narrow exception with in-file metadata behind it (§X.3), and there are exactly two.

### What this design refuses to do

- **No directory per entity type.** Twenty entity types, five scope directories.
- **No second home for any fact.** Narrative patterns live in `config/narrative_library.yaml` and nowhere else; Phase 1's proposed `knowledge/narrative/` is not created. The Chilean customer-language corpus is `OBSERVATION` records in the Evidence Ledger, not a knowledge directory; Phase 1's `knowledge/language/cl/` is not created. Source snapshots are `SOURCE_SNAPSHOT` assets under `media/`; Phase 1's `sources/external/` is not created. Three directories deleted from the design by reading Phase 2 (§AE, REPO_ADR-014, REPO_ADR-015).
- **No empty tree built on speculation.** `src/`, `tests/`, `tests/golden/<category>/` and `.claude/skills/` are *named* here and *created* by the phase that fills them.
- **No file identity.** A filename is a rendering of an identifier, never the source of one. The index builder reads the id from the file's content, and a path/content mismatch is an integrity failure (§AB check 14).
- **No history rewrite as a migration mechanism.** The 136 MB of media already in git history stays there. Rollback is designed against named, tagged freeze commits (§Z.1, §AA) — `phase-2-freeze` as the older historical checkpoint and `phase-3a-freeze` as the normal migration baseline — and rewriting history would destroy both. Purging is deferred, not rejected outright (REPO_ADR-017).

### The four risks this layout does not eliminate

1. **Media payloads will eventually become the only unbacked data in the system, once a durable payload strategy exists and cutover happens.** Phase 2 §AI.1 requires *registered* payloads to be git-ignored in the target architecture, and this design honours that target. **It does not yet act on it**: the audit correctly found that untracking the fifteen current reference samples before any backup/LFS/sync mechanism exists would make cross-machine portability worse than it is today, so Phase 3B keeps them tracked and defers untracking to an explicit future Media Cutover (§O.3, §AD R1, REPO_ADR-016/017).
2. **Line-ending drift silently invalidates every config hash on a second computer.** Phase 2 §G.7 hashes authored YAML **over file bytes**. This machine has `core.autocrlf=true`; the current worktree happens to be LF, but a fresh clone on a second Windows machine would check out CRLF and produce different hashes for byte-identical policy. `.gitattributes` with `eol=lf` fixes it and is the single highest-value file in this migration (§AD R3, REPO_ADR-024).
3. **A placeholder registry reads as authored policy.** An empty `deny_list.yaml` blocks nothing. Mitigated by making placeholders fail closed (REPO_ADR-010), not by trusting that someone remembers to fill them in.
4. **A random-allocated identifier can, in principle, collide.** `CAMPAIGN_ID`'s suffix is only 6 hex characters. The frozen format is not reopened, but "cannot collide in practice" is not a write contract — the repository-layer contract is generate-and-retry under create-exclusive semantics (§F.5, REPO_ADR-029).

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

All 15 media files were committed in the baseline commit `92ec3eb` and are therefore **already in git history**. `.git` is 136 MB of loose objects (never packed). No file exceeds GitHub's 100 MB hard limit or its 50 MB warning threshold. **Operational update: the repository has since been pushed to a private GitHub remote (`origin`), with `master` tracking `origin/master`** — this section's original wording assumed no remote yet existed; `git gc` still compacts the loose objects, but "before the first push" is no longer an available window (§AI.7).

### B.4 Findings that change the design

| # | Finding | Consequence |
|---|---|---|
| 1 | **The three methodology PDFs are Google Docs exports** (`/Producer (Skia/PDF m154 Google Docs Renderer)`), not scans of published works | The metadata establishes only that these files were produced through Google Docs' export pipeline — **it does not, by itself, establish that no original document exists anywhere.** What it does establish, combined with Phase 1's own reading of the corpus: **no authoritative upstream source is present or resolvable in this repository, and the corpus's cited provenance cannot be verified from what the repository holds.** That is sufficient to keep the PDFs out of `sources/` (which is reserved for material whose provenance *is* resolvable) and to place them with the Markdown modules in quarantine instead (§AI Correction 11, REPO_ADR-013 revised). |
| 2 | `core.autocrlf=true`, no `.gitattributes` | Latent cross-machine hash break for authored YAML, whose hash is taken over file bytes (§AD R3). |
| 3 | `core.ignorecase=true`, `core.symlinks=false` | Case-only path distinctions and symlink-based layouts are unavailable. Design accordingly (§AC). |
| 4 | 15 media files already in history at `92ec3eb` | Untracking them going forward does **not** delete them; `git checkout 92ec3eb -- samples/` recovers any of them. This removes the strongest objection to ignoring `media/` (§AD R1). |
| 5 | `git-lfs 3.7.1` is installed on this machine but **not configured in this repository** | No LFS assumption is made. The design stays LFS-compatible without requiring it (§O.6). |
| 6 | Python resolves only to the Windows Store stub; `ffmpeg` and `sqlite3` CLI are absent | Confirms Phase 1 PRE-01 still holds. **Every Phase 3B command in this document runs under Git Bash, using `git` plus the standard Unix utilities bundled with it** — `sha256sum`, `mkdir`, `rmdir`, `find`, `grep`, `sort`, `comm`, `wc`, `cut`, `sed`, `diff`, `xargs`, `cat` — all verified present. **Corrected twice: first (§AI.7 Fix 24) from a false "POSIX shell" claim** — §Z.3's manifest-building code uses Bash arrays (`SRC=(...)`), Bash array expansion (`"${!SRC[@]}"`) and ANSI-C quoting (`$'\t'`), none of which is POSIX `sh` syntax — **and again (§AI.7.9 tooling wording correction, then extended in this pass) from a claim naming only `git` and `sha256sum`**, when §AB.1's executable checks alone add ten more external utilities. Nothing requires Python, `ffmpeg` or `sqlite3`. |
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

**RP4 — The source manifest is a file-*class* test, not a root-membership test, and needs no exception list (§AI.7 Fix 21).** Under `store/`, the manifest is every `*.json` and every `*.jsonl`. Under `config/`, it is every `*.yaml`. Nothing else under either root is a manifest input — not because it is named as an exception, but because it fails the class test by construction. `store/README.md`, `config/README.md` and `config/styles/README.md` are tracked repository documentation, exactly like a `README.md` anywhere else in the repository; they are simply never `.json`, `.jsonl` or `.yaml`, so the question of excluding them never arises as a special case. Anything derived, however faithfully, lives outside both roots regardless (§Q.3, §AI Correction 6) — `reviews/` fails the class test for an even more basic reason: it isn't `store/` or `config/` at all.

**RP5 — Derived-but-tracked material earns its own root when its write authority, canonicality and rebuildability all differ from its neighbours.** A file that is git-tracked (unlike `var/`), never authoritative (unlike `store/`), and mechanically reproducible from something that is (unlike `docs/`) is a third thing, not a variant of the other two, and gets its own top-level directory rather than borrowing one it doesn't quite fit (`reviews/`, §Q.3).

**RP6 — Directory placement follows registration state and write context, not merely the presence of an `ASSET_ID`.** A registered payload lives in `media/<2hex>/AST-<12hex>.<ext>`. A file awaiting registration lives in one of exactly two places depending on how it arrived — operator-supplied input in `incoming/`, repository-origin payload in `media/_unregistered/` (§P.2) — and never anywhere else. Runtime scratch and working media with no `ASSET_ID` and no path toward one lives in `var/`. The rule is not "has an id → `media/`, otherwise → `var/`"; it is "on a path toward registration → `incoming/` or `media/_unregistered/`; registered → `media/`; neither → `var/`" (§AI Correction 9).

**RP7 — Nothing ignored may be the only copy of a canonical *record*.** Payloads are the sole, explicit, approved exception, and they are exception enough that they get their own risk entry, their own check command and their own approval item.

**RP8 — Paths carry identity, never authority.** Where a path does carry policy — the quarantine directory and the two ingestion entry points — the policy is duplicated in in-file metadata, so the path is a convenience and a second line of defence, never the source of truth (§X.3).

**RP9 — A version is never overwritten, and the filesystem enforces it.** Writing artefact version *n* is a create-exclusive operation on a path that must not already exist. "Immutability on write" (Phase 2 P5) becomes an `O_CREAT|O_EXCL` failure rather than a code review.

**RP10 — Every path is relative and portable.** No canonical record contains an absolute path, a drive letter or a machine name. The media root is resolvable by configuration; everything else is repo-relative (§AC).

**RP11 — Reserve names, create directories.** A directory is created by the phase that puts a file in it. Empty scaffolding is a promise the repository cannot keep.

**RP12 — A structural constraint that can be expressed as a filesystem check should be.** "Exactly nine config registries" is `ls config/*.yaml | wc -l`. "No canonical file is ignored" is `git check-ignore --no-index` **over NUL-delimited paths** — corrected in this pass (§AI.7 Fix 22): `git check-ignore` **without** `--no-index` silently reports nothing for a path that is already tracked, even when that path matches an active ignore rule, which is exactly the case RP7 needs caught, not missed. Turning invariants into one-line commands is most of what a repository layout is *for*, provided the command actually tests the property named.

**RP13 — A random-allocated identifier's write path retries on collision; it never assumes one away.** Generating a candidate and creating its target path exclusively is the whole mechanism (§F.5); an `EEXIST` on that create is an ordinary, anticipated branch, not an integrity failure.

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
├── reviews/                        DERIVED · PURE · TRACKED · NOT in the source manifest
│   ├── products/<PRD>/product_truth_v2.md
│   └── campaigns/<CMP>/{experiment_plan_v3.md, creative_<CRE>_v3.md, …}
│
├── media/                          BINARY PAYLOADS — mixed tracking, see §O.3
│   ├── .gitignore                  ignore future untracked payloads only      [tracked]
│   ├── README.md                                                             [tracked]
│   ├── <2hex>/AST-<12hex>.<ext>    registered payloads, id-addressed          [future: ignored]
│   └── _unregistered/              repository-origin files awaiting registration
│       └── (Phase 3B: the 15 current samples — TEMPORARILY TRACKED, §AI Correction 7)
│
├── incoming/                       INGESTION BOUNDARY — git-ignored
│   ├── .gitignore                                                            [tracked]
│   └── README.md                   how to drop a file without knowing any id [tracked]
│
├── var/                            DERIVED / REBUILDABLE / EPHEMERAL — git-ignored
│   ├── .gitignore                  local to this directory, see §Q            [tracked]
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

**Twelve top-level directories.** Nine exist after Phase 3B (`docs`, `config`, `knowledge`, `sources`, `store`, `reviews`, `media`, `incoming`, `var`); three are reserved (`.claude`, `src`, `tests`). `reviews/` is new in this revision — split out of `store/` per the external audit's Correction 6 (§AI) so a renderer upgrade can never be mistaken for a canonical-data change.

---

## E. Top-Level Directory Responsibilities

| Directory | Purpose | Canonical? | Git tracked? | Owner (who writes it) | Examples |
|---|---|---|---|---|---|
| `docs/` | Phase documents, migration log, operator documentation | No — documentation about the system, not system data | **Yes** | Human (phases) | `PHASE_2_DATA_ARCHITECTURE.md`, `MIGRATIONS.md` |
| `config/` | The nine policy registries (§B.1 of Phase 2) plus authored registry entities | **Yes** — hashed into every run and every artefact's `inputs[]` | **Yes** | Human author, reviewed | `evidence_policy.yaml`, `styles/STY-ugc-raw-handheld.yaml` |
| `knowledge/` | Structured, derived, provenance-tagged knowledge retrieved into prompts | **Yes** — a knowledge file is a `KNOWLEDGE_ID` entity, hashed into the run head | **Yes** | Human author / a derivation pass, then human review | `schwartz_persuasion_framework.md`, `_quarantine/methodology/**` |
| `sources/` | Raw, immutable upstream documents. Never edited, never derived-in-place | No — provenance, not knowledge. Referenced by `source_files[]` | **Yes** | Human, by deposit | `books/breakthrough-advertising.pdf` |
| `store/` | **The canonical data root.** Every artefact version, entity record and event log | **Yes — this is the system of record** | **Yes** | Runtime (orchestrator) only; a human edits it only to repair, and the repair is visible in a diff | `campaigns/CMP-…/creatives/CRE-…-07/v3.json` |
| `reviews/` | Derived, pure, human-readable Markdown renders of gate-relevant artefacts | No — **derived**; regenerable from `store/`, never itself a source of a fact | **Yes** | Runtime (a pure renderer); never hand-edited | `campaigns/CMP-…/experiment_plan_v3.md` |
| `media/` | Binary payloads for registered assets, plus files awaiting registration | No — the **Asset Registry record** is canonical; the payload is referenced | **Mixed, temporarily** — the 15 current samples stay tracked through Phase 3B; future registered payloads are ignored from the Media Cutover onward (§O.3) | Runtime (ingestion, generation); operator via `incoming/` | `7b/AST-7b31e0c9d4a2.mp4` |
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
| `campaigns/` | **Campaign** | Six campaign artefacts, creatives, packages, gate decisions, the `campaign` event log | `INS`, `HYP`, `CON`, `EXP`, `CRE`, `GAT` |
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
│       └── events.jsonl                           ← the `evidence` log
│                                                   (derived render: reviews/products/PRD-acme-magnesio-500/product_truth_v2.md)
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
│       └── events.jsonl                           ← the `campaign` log
│                                                   (derived renders: reviews/campaigns/CMP-acme-3f8b21/{experiment_plan_v3.md, package_PKG-acme-3f8b21-07-v1_v1.md})
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
| `EXT` | **run** | **every** `store/products/*/ledger/extractions/EXT-<run-suffix>-*.json`, across **all** product ledgers | filenames, scanned by run suffix |
| `GAT` | campaign | `store/campaigns/<CMP>/gates/` | filenames |
| `CRE` | campaign | `store/campaigns/<CMP>/creatives/` | directory names |
| `INS` | campaign | **every version** of `research_dossier/` | file contents |
| `HYP` | campaign | **every version** of `hypothesis_pool/` | file contents |
| `CON`, `EXP` | campaign | **every version** of `experiment_plan/` | file contents |

Two rules follow, and both are load-bearing:

1. **Every version, not the latest.** `HYP-acme-3f8b21-017` may appear in `hypothesis_pool/v1.json` and be absent from `v2.json`. INV-118 forbids reuse, so the allocator reads the union across all versions. Reading only `latest` would reissue a retired ordinal — and `latest` is explicitly non-authoritative anyway (Phase 2 §G.5, INV-12).
2. **The allocator reads canonical files, never SQLite.** SQLite is `INDEX_ONLY` and may be stale, missing or mid-rebuild (Phase 2 §AA.2: *a missing database is not an error*). An allocator that trusted the index would double-allocate against a stale one. This is the repository-layer statement of Phase 2 P13 and it belongs in Phase 5's code review checklist.

**`EXT` is the one namespace where allocation scope and storage scope genuinely diverge, and it is worth stating precisely why the table above scans every product ledger rather than one.** Phase 2 §E.1 fixes the allocation scope as `(EXT, run)` — an extraction's ordinal is unique within the run that produced it — but the *record* is stored under the product it describes (§H), because an extraction outlives its run and a product's evidence is read by every future campaign on that product, not just the one whose run wrote it. A single run may legitimately touch more than one product (a multi-product campaign, or a re-run that revisits an earlier product), so **there is no one product ledger that is "the" run's extractions.** The external audit correctly rejected two tempting shortcuts: a duplicate run-local extraction registry (a second authoritative location for a fact the product ledger already carries — the exact dual-write Phase 2 Correction 11 removed) and reading SQLite (ruled out by rule 2 above, for the same reason as every other namespace). The only mechanism consistent with both frozen constraints is: **for run suffix `<run-suffix>`, glob `store/products/*/ledger/extractions/EXT-<run-suffix>-*.json` across every product ledger, validate that each matched record's own `run_id` field agrees with the run being allocated for, and take `max` of the matched ordinals `+ 1`.** The validation step matters because the glob matches on filename alone; a record whose `run_id` disagrees with its filename is a path/content mismatch and an integrity failure in its own right (§X.2), not a candidate for the `max`.

**Nothing in this table reads an event log.** That is Phase 2 §AI.1 item 3's explicit warning honoured structurally: `event_seq` numbers events and never numbers entities, and no ordinal's source of truth is a `.jsonl` file.

### F.5 Random-allocated identifiers must retry on collision, not merely avoid it

`CAMPAIGN_ID`, `RUN_ID` and `ASSET_ID` are random-allocated (Phase 2 §E.1), and Phase 2's own rationale for each is entropy-based — "cannot collide in practice." That is a statement about probability, not a write contract, and the external audit is right to reject it as one: `CAMPAIGN_ID`'s suffix is six hex characters (2^24 ≈ 16.7 million), which is comfortable for a single operator's lifetime campaign count but is not zero, and a repository design that never states what happens on the unlikely path has not actually designed for it.

**Nothing about the frozen identifier formats is reopened.** The fix is entirely at the write boundary, and it is the same shape RP9 already established for versioned artefacts:

```
generate candidate identifier
create-exclusive the target path (e.g. store/campaigns/<CANDIDATE>/campaign_brief/v1.json)
if the create-exclusive call fails with EEXIST:
    the candidate is already in use — generate a new candidate and retry
otherwise:
    the candidate is committed; proceed
```

Because every random-allocated identifier's canonical home is a path (`store/campaigns/<CAMPAIGN_ID>/`, `store/runs/<RUN_ID>/`, `store/assets/<2hex>/AST-<12hex>.json`), a collision is not a subtle data-integrity bug to guard against — it is an ordinary, anticipated `EEXIST` on an ordinary create-exclusive write, indistinguishable in mechanism from the check RP9 already requires for artefact versions. This belongs in the Phase 5 allocator's write contract (§S) as a normal branch, not an edge case.

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
3. **Everything under an artefact directory is canonical.** Derived renders go to the top-level `reviews/` root, never inside `store/` at all, so "is this file authoritative?" is answered by which of the two roots a path falls under — no exception list required (§Q.3).

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
- **`EXTRACTION_ID` is run-scoped but the record lives under the product.** `EXT-a91c4e-012` is allocated within run `a91c4e` (Phase 2 §E.3) but describes evidence about a product and outlives the run, so it is stored with the ledger and the run reaches it through the `run_id` field it already carries. The allocation scope and the storage scope differ here, and only here; recorded so that neither is "corrected" into the other. **A run may touch more than one product**, so allocating the next `EXT` ordinal means scanning every product ledger for that run suffix, never one — the full mechanism, and why a run-local registry is rejected, is in §F.4.
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
2. **`sources/methodology/` is removed, not populated.** It is empty and untracked. Its intended contents — the three methodology PDFs — carry the same unresolvable provenance as the Markdown modules (§B.4 finding 1): no authoritative upstream is present or resolvable in the repository for either. So they go to quarantine, not to `sources/`. Moving them into `sources/` would assert that they are raw upstream material with resolvable provenance, which §B.4 does not establish — and the correction is precisely to claim no more than the evidence shows (§AI Correction 11).
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
| **A — YAML front matter inside the Markdown** | **Accepted — for Markdown knowledge entities.** Corrected in this pass: this is a *conditional* acceptance, not an unconditional one (§M.3). |
| B — Adjacent metadata file (`foo.md` + `foo.meta.yaml`) | **Rejected for Markdown entities**, for the reason given below. **Accepted as the only workable mechanism for binary entities**, where Option A is not merely undesirable but physically impossible (§M.3, §AI.7 Correction 18). |
| C — Central registry (`knowledge/registry.yaml`) | **Rejected.** A second authoritative location for a fact the file could carry itself, and a merge-conflict magnet as the corpus grows. It also inverts the property that matters: provenance must travel *with the content* into the prompt (Phase 2 P9), and a central file has to be joined at retrieval time — one more step that can be skipped. |
| D — Combination | **Rejected as authored duplication, accepted as derivation.** A central *index* is fine when it is **derived** — SQLite, or a generated listing in `var/` — and never authored. |

**Decision — Option A for Markdown, Option B for binary, both governed by the same principle: one authoritative provenance record per knowledge entity, never two.**

Phase 2 §G.7 item 3 already assumes Option A for the case it can apply to: *"YAML is used only where a human is the author — `config/*.yaml` and **knowledge front-matter**."* This is the smallest architecture that supports every required field for a Markdown file, and it is the only one where losing provenance requires editing the file that contains the content.

**The reason Option B was rejected in the first pass does not apply to a binary file, and the external audit is right that the document had not yet reconciled the two.** Option B was rejected for Markdown because a sidecar *can* drift from the file it describes — it is one directory operation away from being lost, and nothing forces the two to move together. That objection presumes a third option exists that doesn't have the problem — front matter inside the file — and for Markdown, it does. **For a PDF, it does not: a PDF cannot carry a YAML block that the retrieval layer reads as its own provenance without altering the binary format itself, which this design will not do to files already frozen as immutable (§K).** With no in-file option available, the choice for a binary entity is not "sidecar vs. front matter" — it is "sidecar vs. no authoritative provenance record at all." A sidecar with a resolvable, hash-verified link to its payload is not the authored duplication Option C was rejected for; it is the *only* authored location a binary entity's provenance can occupy, which is a different claim (§M.3).

### M.1.1 The universal rule this whole section serves — corrected to be genuinely universal (§AI.7 Fix 23)

**Every retrievable knowledge entity requires exactly one valid, authoritative provenance record. Absent one, the entity is `NOT_RETRIEVABLE`.** This is the rule the design was always trying to state, and the first pass stated it correctly for one carrier and left it implicit — and therefore weaker — for the other: §M.3 makes a PDF with no valid sidecar fail-closed, but §M.2 as first written only said front matter "applies to" a Markdown entity, without saying what happens to a Markdown entity that lacks it. Read literally, a Markdown file added to `knowledge/` with a missing or malformed front-matter block had no stated fate — which, for a retrieval layer that must decide *something*, defaults to permitted by omission. That silent default is precisely the asymmetric failure mode §N.3 already refuses to accept for the quarantine path check, and there is no principled reason a Markdown entity should get a more forgiving default than a PDF gets.

**The rule, stated once, governing both carriers:**

| | Markdown knowledge entity | Binary (PDF) knowledge entity |
|---|---|---|
| Provenance carrier | In-file YAML front matter (§M.2) | `.meta.yaml` sidecar, bound by `payload_path` + `payload_sha256` (§M.3) |
| Valid record present | Retrievable, per its own `retrieval_policy` | Retrievable, per its own `retrieval_policy` |
| **No valid record present** | **`NOT_RETRIEVABLE`** — corrected; no longer an implicit default to permitted | **`NOT_RETRIEVABLE`** — as §M.3 always specified |

"Valid" means the same thing for both carriers: the record parses, declares the required fields of Phase 1 §I's schema, and — for a sidecar specifically — its `payload_path` resolves and its `payload_sha256` matches. A Markdown file with front matter that fails to parse, or that is missing a required field, is exactly as unretrievable as a PDF with no sidecar; the mechanism differs, the failure mode does not.

### M.2 The Markdown carrier, and the boundary it does not cross

**Every retrievable knowledge entity requires one valid authoritative provenance record (§M.1.1); for a Markdown entity, that record is in-file front matter.** This applies to every retrievable Markdown knowledge entity under `knowledge/` — and to nothing else that happens to live there. The distinction matters because this design also places operator documentation inside the same tree, at `knowledge/_quarantine/README.md` (§N.1), and the two are not the same kind of file:

| | A `KNOWLEDGE_ID` entity (e.g. `schwartz_persuasion_framework.md`) | An operator `README.md` under `knowledge/**` |
|---|---|---|
| Retrieval candidate | **Yes** — this is the whole point of the front matter | **No** — it exists to be read by a human maintaining the repository, never fetched into a prompt |
| Carries provenance front matter | **Required** | **Not required, and not meaningful** — it has no derivation method, no source files, no claims |
| Excluded from retrieval by | Its own `retrieval_policy` field, when not `open` | **Mechanically, by filename** — the retrieval layer excludes every `README.md` under `knowledge/` unconditionally, never by asking it to declare its own exclusion |

**A `README.md` is documentation about a directory, not a fact derived from a source, and requiring it to carry a `knowledge_id` and a `derivation_method` would be a category error — the same category error the brief's Correction 12 catches.** The retrieval layer's exclusion rule is filename-based specifically so that it does not depend on the file cooperating: a `KNOWLEDGE_ID` entity is excluded from retrieval by *declaring* `retrieval_policy: excluded` or similar in its own front matter (an affirmative, content-level fact); a `README.md` is excluded *structurally*, by never being a candidate in the first place, regardless of what it does or does not contain. This is the same fail-closed-by-construction posture already used for the quarantine path check (§N.3) — the mechanism does not trust the file to say the right thing about itself when the file's very shape already answers the question.

Phase 1 §I's schema, applied to every retrievable **Markdown** knowledge entity, verbatim at the top of the file — the PDF carrier is §M.3's sidecar, not this block:

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

Five properties of the mechanism — a fifth added in this pass to make §M.1.1's universal rule concrete for the Markdown carrier specifically:

- **`source_files[]` holds repo-relative paths**, so it is resolvable on any clone and by the source-manifest hash. Phase 1's rule — *empty or unresolvable ⇒ cannot be `VERIFIABLE`* — becomes a check: every path in every `source_files[]` must exist.
- **The hash is over the whole file bytes**, front matter included, matching Phase 2 §G.7 item 3 and the `knowledge` map pinned in the RUN head (§W.1). Editing provenance is therefore a visible change to what a run pinned, which is correct: a tier downgrade *should* invalidate nothing silently.
- **Section-granularity provenance is a second front-matter key, not a second file.** Phase 1 §I's structural finding — several modules mix cited material with unsourced model speculation under one heading style, e.g. the `[Ampliación Externa - Internet]` blocks — is handled by an optional `sections:` list mapping heading anchors to a tier override. Still one file, still one source of truth. This is migration step **M5** and belongs to Phase 3C, not 3B.
- **A derived index may exist; an authored one may not.** The retrieval layer may materialise `knowledge_id → tier → retrieval_policy` into SQLite for speed. If that index disappears it is rebuilt from front matter, which is the same contract every other projection has.
- **A Markdown file with no front matter, unparsable front matter, or a missing required field is `NOT_RETRIEVABLE` — corrected, per §M.1.1 (§AI.7 Fix 23).** This is not a new mechanism; it is the same fail-closed default §M.3 already applies to a PDF with no valid sidecar, now stated for the carrier that had, until this pass, no stated default at all.

### M.3 Binary knowledge entities — a sidecar is the provenance record, not a duplicate of one

**This subsection is new, added per the external audit's Correction 18.** The first pass's language — "front matter inside the Markdown," "every retrievable knowledge entity … receives … front matter" — was written as though every quarantined file were Markdown. It is not: of the 8 quarantined files, 5 are Markdown and **3 are PDF** (§B.4 finding 1). Requiring in-file YAML front matter of a PDF is not merely inconvenient, it is not executable — a PDF's bytes are not a text stream a retrieval layer can prepend a YAML block to without corrupting the format the file already is, and this design has separately committed to never editing these files' content (§N.1). The first pass had, without saying so, classified three PDFs as fully retrievable `KNOWLEDGE_ID` entities while simultaneously requiring a provenance mechanism those same three files cannot carry. That is the contradiction this subsection resolves.

**The fix preserves the one governing principle unchanged: one knowledge entity, one authoritative provenance record, never two.** It only changes *where* that record lives when the entity's payload cannot hold it itself.

| | Markdown knowledge entity | Binary (PDF) knowledge entity |
|---|---|---|
| Example | `schwartz_persuasion_framework.md` | `Dominio del Post ID_ Escalamiento y Prueba Social en Meta.pdf` |
| Provenance record | YAML front matter **inside** the file (§M.2) | A sidecar file, **`<payload-filename>.meta.yaml`**, beside the payload |
| Payload modified to carry provenance? | N/A — the front matter *is* part of the file | **No — never.** The PDF's bytes are untouched; the sidecar is a separate, new file |
| Authoritative provenance location | The file itself | The sidecar — **exactly one**, never the payload, never a central registry |
| Retrieval unit | One file | **The (payload, sidecar) pair, treated as one logical `KNOWLEDGE_ID` entity** by the retrieval layer |

**The sidecar schema** — every field Phase 1 §I's provenance schema requires, plus the two fields a sidecar needs that an in-file block does not (because a sidecar is a second file and must say which payload it describes and prove it still matches):

```yaml
# Dominio del Post ID_ Escalamiento y Prueba Social en Meta.pdf.meta.yaml
knowledge_id:           KNW-post-id-domain-escalation
payload_path:           "knowledge/_quarantine/methodology/Dominio del Post ID_ Escalamiento y Prueba Social en Meta.pdf"
payload_sha256:         "sha256:…"          # the PDF's own content hash — the sidecar's link to its payload
tier:                   CONVERSATIONAL_DERIVED_UNVERIFIABLE
source_files:           []                  # empty ⇒ cannot be VERIFIABLE, exactly as for a Markdown entity
derivation_method:      probable_llm_derived
derivation_confidence:  INFERRED
machine_verifiable:     false               # a PDF's structure is not parsed by the retrieval layer at all
human_reviewed:         true
scope:                  niche:pcos-hair-loss-supplement-cl
retrieval_policy:       research_only
contains_claims:        health_claims
version:                1
created_at:             "2026-09-04"
```

`payload_path` and `payload_sha256` are the two additions. Every other field is Phase 1 §I's schema, unchanged — the sidecar is not a different provenance vocabulary, only a different carrier for the same one.

**Validation, stated as checks because this is exactly the kind of rule that rots without one:**

1. **Exactly one sidecar per retrievable binary knowledge file.** A PDF with zero sidecars or more than one is invalid.
2. **`payload_path` must resolve** to an existing file, by the same rule as `source_files[]` (§M.2) — an unresolvable path is a broken provenance record, not a minor omission.
3. **`payload_sha256` must match** the current content hash of the file at `payload_path`. A mismatch means the payload changed since the sidecar was written — for a file this design treats as immutable, that should never happen, and a mismatch is an integrity failure, not a warning.
4. **A PDF with no valid sidecar is fail-closed: `NOT_RETRIEVABLE`.** This is the same posture as the quarantine path check (§N.3) — the default for a binary file the retrieval layer cannot otherwise classify is *excluded*, never *open by omission*.
5. **An orphan sidecar — one whose `payload_path` does not resolve, or which has no corresponding payload at all — is invalid** and is treated as a broken record requiring operator attention, not as harmless clutter.

**Why this is not the authored duplication that Option C (a central registry) was rejected for.** A central registry would hold provenance for every knowledge file *whether or not* that file could carry its own; the sidecar exists **only** for the subset of entities — exactly 3, currently — that structurally cannot hold their own provenance, and each sidecar describes exactly one payload. There is no world in which a Markdown entity gets a sidecar (its front matter already satisfies §M.2) and no world in which a PDF's provenance lives in two places at once. The count of authoritative provenance records equals the count of knowledge entities, one-to-one, regardless of which mechanism carries which.

**Sidecars are authored in Phase 3C, exactly like Markdown front matter — this changes no phase boundary, only the mechanism within it.** §N.3 is updated to reflect the sidecar for the 3 PDFs specifically; §Y.4's M3 entry now names both mechanisms.

---

## N. Methodology Quarantine Design

### N.1 Destination

```
knowledge/_quarantine/methodology/        ← 8 files, moved unmodified
```

Phase 1 §I named this path and Phase 1 ADR-009 marks it *highest priority*. It is inherited, not re-litigated. The alternatives considered and rejected: `knowledge/legacy/` (describes age, not the problem — the problem is unverifiability, and new material can arrive equally unverifiable), `knowledge/unverified/` (accurate but reads as a staging area awaiting verification; this corpus's citations *cannot* be resolved, so nothing is pending), and a top-level `quarantine/` (removes it from `knowledge/`, which hides the fact that it is knowledge-shaped and would otherwise be retrieved).

`_quarantine` keeps the leading underscore from Phase 1: it sorts first, reads as non-ordinary, and is visible in every directory listing above the material it guards.

### N.2 Do the PDFs and the Markdown separate?

**No — they stay together, and the finding that settles it is stated at the strength the evidence actually supports.** The three PDFs carry `/Producer (Skia/PDF m154 Google Docs Renderer)`: this establishes that they were produced through Google Docs' export pipeline, which rules out their being scans of a published work. **It does not, on its own, prove that no original document exists anywhere** — that would be a stronger claim than the metadata can carry, and the external audit is right to insist the wording not overreach it (§AI Correction 11). What the metadata *does* support, taken together with Phase 1's reading of the corpus's content: these three files carry the same unresolvable citations, the same niche-specific claims (PCOS hair-loss supplement, `es-CL`) and the same F2/F3 content Phase 1 classified as `NOT_SAFE_TO_HARDCODE` as the five Markdown modules. **No authoritative upstream source for any of the eight files is present or resolvable in this repository, and the corpus's cited provenance cannot be verified from what the repository holds.** That is sufficient to justify `CONVERSATIONAL_DERIVED_UNVERIFIABLE`, `research_only` and quarantine — it does not require, and this document does not claim, that no original exists in the world.

Splitting them — PDFs to `sources/`, Markdown to quarantine — would assert that the PDFs have resolvable upstream provenance that the Markdown lacks. Nothing in the repository supports that distinction. Keeping all eight files in one directory keeps one retrieval policy over one corpus, which is also the only arrangement in which the policy is enforceable by path.

### N.3 Provenance and retrieval policy

Every one of the **8 quarantined knowledge entities** receives, in Phase 3C, provenance carrying these values — **the 5 Markdown modules as in-file front matter (§M.2), the 3 PDFs as a `.meta.yaml` sidecar (§M.3)**, corrected in this pass from a single undifferentiated "front matter on all 8" statement that could not actually apply to the PDFs. `knowledge/_quarantine/README.md` is not one of the 8 — it is operator documentation, excluded from retrieval by filename per §M.2, and receives neither front matter nor a sidecar because neither applies to it (§AI Correction 12):

```yaml
tier:                  CONVERSATIONAL_DERIVED_UNVERIFIABLE
derivation_method:     probable_llm_derived
derivation_confidence: INFERRED          # authorship is inferred; unverifiability is established
scope:                 niche:pcos-hair-loss-supplement-cl
retrieval_policy:      research_only
contains_claims:       health_claims
source_files:          []                # empty ⇒ cannot be VERIFIABLE, by Phase 1's rule
```

For the 5 Markdown modules, these values sit in the file's own front matter block. For the 3 PDFs, they sit in each PDF's `.meta.yaml` sidecar (§M.3), alongside that sidecar's `payload_path` and `payload_sha256`. **The values themselves — and everything `research_only` means below — are identical across both mechanisms; only where they are recorded differs.**

**`research_only` means, precisely** (Phase 1 §I): a human may read it; `creative-strategist` may consult it for *structural* patterns — the 7-part UGC arc, the three testing methods, the pain→hope transition — under an explicit tier warning; **and the script engine may never retrieve it.** It supplies no claims, no benchmarks, no ingredient science and no CTA copy.

**Enforcement is two-layered, deliberately, for both mechanisms.**

1. **Metadata is the authority.** For a Markdown module, the retrieval service reads `retrieval_policy` from its own front matter — and, corrected in this pass (§M.1.1, §AI.7 Fix 23), a missing or invalid front-matter block is `NOT_RETRIEVABLE`, exactly as for a PDF. For a PDF, it reads the same field from that PDF's sidecar — a PDF with no valid sidecar is `NOT_RETRIEVABLE` by §M.3's fail-closed rule. **Both carriers now default to the same fail-closed outcome**; the first pass had, without saying so, given the Markdown carrier a more forgiving implicit default, which §M.1.1 removes.
2. **The path is a second line of defence.** Any repository path containing a `_quarantine/` segment is refused by the script-generation retrieval path regardless of its metadata — this check does not care whether the file's provenance is in-file or sidecar-carried, because it never inspects the file's content in the first place.

Two mechanisms for one rule is normally a smell. It is justified here because the failure mode being guarded against is asymmetric even though the *default* is now symmetric: a missing or invalid provenance record — front matter or sidecar — is fail-closed at the metadata layer (item 1), but the path check exists as a second, independent line of defence in case that layer is ever bypassed or misimplemented, and the material in question contains unsupported health claims and a compliance deny-list violation (Phase 1 F2, F3). The path check fails closed regardless of what the metadata layer decides, for either file format. `knowledge/_quarantine/README.md` states both, in the directory they govern.

### N.4 How future ingestion handles similar material

The general rule, since this corpus will not be the last: **material whose citations cannot be resolved enters `_quarantine/<topic>/` with `retrieval_policy: research_only`, regardless of format, regardless of who wrote it, and regardless of how useful it looks.** The quarantine follows from *unverifiability*, which is established by checking citations, not from *authorship*, which is inferred. If authorship were later established or refuted, `derivation_method` changes and `retrieval_policy` does not — Phase 1 §I's rule, preserved because it is the part that makes the classification stable.

---

## O. Asset / Media Architecture

**This section describes the target architecture — where a registered payload will ultimately live and how it is addressed. §O.3 states, separately and explicitly, that Phase 3B does not fully cut over to it: the fifteen media files currently in the repository stay tracked through Phase 3B, and untracking them is deferred to a named future Media Cutover once a durable payload strategy exists (§AI Correction 7). The target and the transition are two different questions, and conflating them was the error the external audit caught.**

### O.1 The separation that everything else depends on

**Binary payload ≠ Asset Registry record.** The record is canonical, git-tracked JSON at `store/assets/<2hex>/AST-<12hex>.json`. The payload — once registered and once the Media Cutover has happened — is a git-ignored file at `media/<2hex>/AST-<12hex>.<ext>`. `ASSET.path` (Phase 2 §S.1) holds the media-root-relative path — `"7b/AST-7b31e0c9d4a2.mp4"` — never an absolute path, never a path outside the media root.

### O.2 The media root

```
media/                              MEDIA_ROOT · target: git-ignored · content tracked by hash, not by git
├── .gitignore                      ignores FUTURE untracked payloads only    [tracked]
├── README.md                                                                 [tracked]
├── 7b/AST-7b31e0c9d4a2.mp4         registered payloads, sharded by id (post-cutover: ignored)
├── 1a/AST-1a2b3c4d5e6f.jpg
└── _unregistered/                  repository-origin files awaiting registration (§P.2)
    └── (Phase 3B: the 15 current samples land here, and remain TRACKED — §O.3)
```

**Addressed by `ASSET_ID`, not by content hash.** Phase 2 §E.4 is explicit that two asset records may legitimately share bytes and differ in rights provenance — the same image supplied by the operator and also present in the repository — and that *rights attach to provenance, not to bytes*. Content-addressed storage would merge those two records onto one file, so deleting or replacing one would silently affect the other. Duplicating a few megabytes is the correct price for keeping two rights positions genuinely separate.

**Sharded by the first two hex characters of the id suffix**, matching `store/assets/`, so a record and its payload share a folder name and neither directory grows unbounded.

**All eleven `asset_type` values live in one flat namespace.** No `media/videos/`, no `media/voices/`, no `media/generated/`. Type, role, brand, product and state are fields on the record and columns in the index; encoding them in a path would create a second classification that can disagree with the first, and would require moving a file when a state changes — which is exactly the mutation the design forbids.

### O.3 Git treatment — target architecture vs Phase 3B cutover, stated separately

**Target architecture (Phase 2 §AI.1 item 4, unchanged):** registered payloads are git-ignored; the Asset Registry record is the git-tracked canonical fact about them. This is the end state this design builds toward, and nothing below reopens it.

**Phase 3B does not reach that end state for the fifteen files already in the repository, and the external audit is why.** The original plan untracked `media/` immediately after the move (`git rm -r --cached media`). The audit found the sequencing wrong: this repository has no durable payload strategy yet — no Git LFS configuration, no synced folder, no external-drive backup, no object storage — and the user intends to work from more than one computer. Untracking the only copies of the fifteen reference samples *before* any of those exists would make cross-machine portability strictly worse than the status quo, where a plain `git clone` already reproduces them. A design whose migration step makes today's actual working pattern worse has sequenced the change wrong, independent of whether the target state is correct.

| | Phase 3B (this migration) | Future Media Cutover (separate, later, explicitly approved) |
|---|---|---|
| `media/_unregistered/**` — the 15 current samples | `git mv`'d from `samples/`, filenames and sub-structure preserved. **Remain tracked.** | `git rm --cached`, once a durable payload strategy is in place |
| `media/.gitignore` | Tracked; ignores *future* untracked payloads. Does not affect already-tracked files — git ignore rules never untrack what is already tracked. | Unchanged |
| `media/README.md` | Tracked; states the mixed interim condition plainly | Updated to describe the fully-ignored end state |
| Any newly generated or newly ingested payload | Also lands under `media/`; **also tracked** until the cutover, for the same portability reason | Ignored from creation, once a durable strategy exists |
| Durable payload strategy | **Not chosen.** Git LFS, a synced folder, an external-drive backup and object storage all remain open (§O.6) | One is chosen and configured as part of the cutover, not before |
| Git LFS | Installed on this machine (`git-lfs 3.7.1`) but **not configured**. Nothing in Phase 3B assumes it. | May be the mechanism the cutover adopts — not decided here |

**This is a migration-sequencing correction, not a reopening of the target Asset Registry contract.** Phase 2 §S and §AI.1 item 4 stand exactly as frozen; §O.1–O.2 above describe them unchanged. What changes is *when* the repository transitions from "payloads tracked because there is nothing better yet" to "payloads ignored because a real mechanism now holds them" — and that transition is named, deferred, and requires its own explicit approval (§AG, REPO_ADR-016/017 revised).

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

### O.5 Local-machine portability, and the gap — deferred by the sequencing fix in §O.3

`ASSET.path` is media-root-relative and the media root is resolved by configuration (`MEDIA_ROOT`, defaulting to `<repo>/media`). Nothing canonical contains a drive letter. So the whole payload tree can move to an external drive, a synced folder, or object storage without touching a single canonical record.

**The gap, stated rather than softened, applies from the Media Cutover onward — not from Phase 3B.** Once cutover happens, `git clone` on a second computer will produce a complete, valid, fully rebuildable canonical store and **zero media payloads** for anything registered after that point. Every artefact, record, event, config and knowledge file arrives; a video, voice sample or image registered post-cutover does not, unless the chosen durable strategy (Git LFS, a synced folder, object storage) also runs on that second machine. **Through Phase 3B, this gap does not exist for the fifteen current samples**, because they remain tracked (§O.3) — a plain clone reproduces them exactly as it does today. Media transfer for anything registered after cutover is an out-of-band copy the operator performs, and `media check` tells them whether it worked. This is the direct future cost of Phase 2 §AI.1 item 4's target state, and it is listed as risk R1 and as approval item 2 — both now scoped to *after* the cutover, not to Phase 3B.

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
var/                        DERIVED · REBUILDABLE · EPHEMERAL
├── .gitignore              owns the ignore policy for THIS directory  [tracked]
├── README.md                                                          [tracked]
├── index/                  creative_os.sqlite3 (+ -wal, -shm)        rebuildable
├── schemas/                generated JSON Schema (2020-12)           regenerated
├── cache/                  fetch cache, prompt cache metadata        disposable
├── tmp/                    temp downloads, scratch                   disposable
├── work/                   generation attempts, working clips        disposable
├── logs/                   runtime logs                              disposable
└── exports/                operator deliverables (final videos, zips) copies
```

**`var/` may be deleted at any time and the only cost is time.** That is the entry criterion; anything failing it does not belong here.

**The ignore rule lives locally, at `var/.gitignore`, not in the root `.gitignore` — and this is a correction from the first pass.** Revision 1 put a bare `var/` line in the root ignore file. The external audit caught the contradiction directly: this design requires `var/.gitignore` and `var/README.md` themselves to be tracked (they explain the directory to a fresh clone, per RP11 and §W), and a root rule ignoring the whole parent directory pre-empts that — an ignore rule on a directory hides everything under it from `git add`'s default walk, including files someone later tries to track deliberately. The fix is the same locality principle used everywhere else paths carry policy: `var/.gitignore` owns `var/`'s own contents —

```
*
!.gitignore
!README.md
```

— and the **root** `.gitignore` carries only rules that are genuinely repository-wide: secrets, Python build residue, Claude Code local settings, OS cruft. `media/.gitignore` and `incoming/.gitignore` already followed this pattern in the first pass; `var/` now matches them (§Z.2, §W, §AI Correction 4).

### Q.1 SQLite

**Location `var/index/creative_os.sqlite3`. Git-ignored. Never committed.**

Audited, briefly, because Phase 2 §AA settles most of it: SQLite is `INDEX_ONLY`, holds nothing that cannot be rebuilt (P13, INV-100), is verified by `rebuild --verify`, and *a missing database is not an error* (§AA.2). A tracked binary that a rebuild can regenerate would produce a conflicting diff on every build for no benefit, and it would create the possibility — however remote — of someone treating a committed index as authoritative. Ignoring it makes that impossible rather than discouraged.

The `-wal` and `-shm` sidecars are covered by ignoring `var/` wholesale. `index_meta.canonical_root_commit` (Phase 2 §AA.1) records the git sha the index was built from, so a rebuilt index remains attributable without being tracked.

### Q.2 Generated schemas

**Location `var/schemas/`. Git-ignored. Regenerated on demand.**

Phase 2 §G.8 makes Pydantic v2 the single source of truth, generating JSON Schema. Tracking the generated output would create a second artefact that can drift, requiring a CI job to prove it has not — a guard against a problem that not tracking makes impossible. Schema review happens on the Pydantic model diff, which is more readable than a JSON Schema diff anyway.

The reproducibility objection — *"which schema was sent to the model during run X?"* — is answered without tracking: the schema is a pure function of the code at a commit, the code is git-tracked, and the run head pins skill versions. Checking out the commit and regenerating yields the exact schema. Recorded so the trade-off is visible rather than assumed away.

### Q.3 Derived Markdown renders are **not** in `var/`, and — corrected — not in `store/` either

Phase 2 §G.7 item 4 requires them **git-tracked**, so a Gate reviewer's rendered package cannot silently disagree with the artefact it projects. Revision 1 placed them inside `store/`, beside the scope they describe, and made that safe by requiring the renderer to be pure — no wall-clock, no absolute path, no run id in a render's bytes — so an unchanged artefact renders byte-identically and never moves the source manifest hash.

**The external audit found the trade wrong, not the purity requirement.** Purity keeps an *unchanged artefact's* render stable, but it does nothing for a *renderer upgrade*: fixing a typo in the render template, or improving its formatting, legitimately changes every render's bytes at once even though not one canonical fact changed. Under Revision 1's placement, that upgrade would move the source manifest hash and mark the SQLite index stale — the exact false alarm Phase 2 §AA.2 exists to prevent, now triggered by a change to *presentation* rather than to *data*. An operator who learns that "stale" sometimes means "someone touched a template" has lost the signal.

**The fix is a boundary, not a rule.** Renders move to a new top-level root, **outside both `store/` and the source manifest entirely**:

```
reviews/
├── products/<PRD>/product_truth_v2.md
└── campaigns/<CMP>/{experiment_plan_v3.md, creative_CRE-acme-3f8b21-07_v3.md, package_PKG-…-v1_v1.md}
```

`reviews/` mirrors `store/`'s scope structure (`products/<PRD>/…`, `campaigns/<CMP>/…`) so a reviewer can find a render by the same path shape they'd use to find its source, but it is a **sibling** of `store/`, not a subdirectory — the source manifest walk that Phase 2 §AA defines over `store/` and `config/` never enters it (RP4).

**The renderer stays pure, for a different and smaller reason than before.** Purity is no longer load-bearing for index staleness — a renderer upgrade can now change every render's bytes in one commit with zero effect on `store/`'s manifest hash, exactly as it should. Purity remains valuable as an ordinary reproducibility property: given an artefact version and a renderer version, the render is a deterministic function of the two, so a hand-edited render is still caught (by regenerating and byte-comparing, not by a manifest hash) and a render can still never disagree with the artefact it projects.

Every render still carries `derived: true` and the ref and hash of its source artefact in front matter, and **a render may never contain a fact absent from its source JSON.**

### Q.4 Classification summary

| Location | Canonical | Derived | Ephemeral | Tracked | In source manifest | Externalisable |
|---|---|---|---|---|---|---|
| `store/**/*.json`, `**/events.jsonl` | ✅ | | | ✅ | ✅ — passes the class test (§AI.7 Fix 21) | No — this is the system of record |
| `store/README.md`, `config/README.md`, `config/styles/README.md` | ❌ — operator documentation | | | ✅ | **No — fails the class test by extension, not by a named exception** (§AI.7 Fix 21) | No |
| `reviews/**/*.md` | | ✅ pure | | ✅ | **No** — not under `store/` or `config/` at all | No |
| `config/*.yaml`, `config/styles/*.yaml` | ✅ | | | ✅ | ✅ — passes the class test | No |
| `knowledge/**`, `sources/**` | ✅ | | | ✅ | N/A — separate roots, not part of the `store`/`config` manifest | No |
| `media/**` | | | | **Mixed through Phase 3B** (§O.3) | N/A | Target: **Yes** — LFS, external drive, object storage |
| `var/index/`, `var/schemas/` | | ✅ | | ❌ | N/A | N/A — rebuilt |
| `var/cache/`, `tmp/`, `work/`, `logs/` | | | ✅ | ❌ | N/A | N/A |
| `var/exports/` | | ✅ copies | ✅ | ❌ | N/A | Yes — but the registry + `media/` is the real copy |
| `incoming/**` | | | ✅ | ❌ | N/A | N/A |

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
| `reviews/**/*.md` | Derived (pure) | ✅ | | ❌ | Phase 2 §G.7 item 4 — a gate render must not silently disagree with its artefact. **Outside** the source manifest — a sibling root to `store/`, not a subdirectory of it (§Q.3, corrected). |
| `config/*.yaml` (the nine) | ✅ | ✅ | | ❌ | Hashed over file bytes into every run (§J.2). Exactly nine. |
| `config/styles/*.yaml` | ✅ | ✅ | | ❌ | Authored registry entities, pinned per artefact via `inputs[]` (§J.4). |
| `store/README.md`, `config/README.md`, `config/styles/README.md` | ❌ — tracked documentation, not a manifest input | ✅ | | ❌ | **Corrected (§AI.7 Fix 21).** Excluded from the source manifest by the file-class rule (§A decision 3, RP4) — neither `.json`/`.jsonl` nor `.yaml` — never by being named as a path exception. |
| `knowledge/**/*.md` — Markdown knowledge entities (8: 3 Schwartz + 5 quarantined modules) | ✅ | ✅ | | ❌ | `KNOWLEDGE_ID` entities; hashed into the RUN head; provenance **in-file front matter** (§M.2). |
| `knowledge/_quarantine/methodology/*.pdf` — binary knowledge entities (3) | ✅ | ✅ | | ❌ | `KNOWLEDGE_ID` entities, corrected in this pass to a distinct row (§AI.7 Correction 18): the payload is unmodified; provenance lives in the sidecar below, never in-file. |
| `knowledge/_quarantine/methodology/*.pdf.meta.yaml` — provenance sidecars (3, one per PDF) | ✅ | ✅ | | ❌ | **New (§M.3, §AI.7 Correction 18).** The authoritative provenance record for its one named payload; `payload_path` + `payload_sha256` bind it to that payload; a PDF with no valid sidecar is `NOT_RETRIEVABLE`. |
| `knowledge/_quarantine/README.md` | ❌ — operator documentation, not a `KNOWLEDGE_ID` entity | ✅ | | ❌ | Excluded from retrieval **by filename**, not by its own declaration (§M.2, §AI Correction 12). Carries no provenance front matter and no sidecar — neither is meaningful for it. |
| `knowledge/_quarantine/**` | ✅ | ✅ | | ❌ | Tracked **and** restricted. Tracking is not permission — retrieval policy is (§N.3), enforced identically whether that policy is recorded in-file or in a sidecar. |
| `sources/books/*.pdf` | Raw | ✅ | | ❌ | 9 MB, irreplaceable, and what makes `source_files[]` resolvable on a clone. |
| `docs/**` | ❌ | ✅ | | ❌ | Documentation. |
| `.gitattributes`, `.gitignore`, `.env.example`, `README.md` | ❌ | ✅ | | ❌ | Repository contract. |
| `media/**` payloads (target state, post-cutover) | Referenced, not canonical | | ✅ | **✅** | Phase 2 §AI.1 item 4. Detectable by `content_sha256`, not preserved by git. |
| `media/_unregistered/**` — **the 15 current samples, through Phase 3B** | Referenced, not canonical | **✅ — temporarily** | | ✅ (already, via git history) | **Corrected (§AI Correction 7).** No durable payload strategy exists yet; untracking them now would make cross-machine portability worse than today. Untracked only at the future Media Cutover. |
| `media/.gitignore`, `media/README.md` | ❌ | ✅ | | ❌ | Make the directory exist on clone and explain itself; the ignore rule governs *future* payloads only through Phase 3B. |
| `incoming/**` contents | ❌ | | ✅ | ❌ | Transient by definition. |
| `var/**` | ❌ | | ✅ (via `var/.gitignore`, not the root file — §Q) | ❌ | Derived, rebuildable or ephemeral. Deleting it costs only time. |
| `var/index/*.sqlite3`(+`-wal`,`-shm`) | ❌ `INDEX_ONLY` | | ✅ | ❌ | Phase 2 P13, INV-100. A committed index could be mistaken for truth. |
| `var/schemas/**` | ❌ | | ✅ | ❌ | Generated from Pydantic; tracking creates drift to police (§T). |
| `.env` | — | | ✅ | ❌ | Secrets never enter git (§AC.4). |
| `.claude/settings.local.json` | ❌ | | ✅ | ❌ | Machine-local. |
| `.claude/settings.json`, `.claude/skills/**` | ❌ | ✅ | | ❌ | Shared project configuration and the five Skills (Phase 4). |
| `src/**`, `tests/**` | ❌ | ✅ | | ❌ | Source code (Phase 5+). |
| `**/__pycache__/`, `*.pyc`, `.venv/` | ❌ | | ✅ | ❌ | Build residue. |
| `Thumbs.db`, `desktop.ini`, `.DS_Store` | ❌ | | ✅ | ❌ | OS cruft; Windows and macOS both write it. |

**The check that makes this matrix real** — not a table someone has to honour, but a command, **corrected per §AI.7 Fix 22**:

```bash
git ls-files -z store config knowledge sources docs | xargs -0 -r git check-ignore --no-index -v
```

Two defects in the first pass's command, both silent: **(1)** `git check-ignore`, run without `--no-index`, does not evaluate ignore patterns against a path that is already tracked — it reports nothing for exactly the case this check exists to catch, which is a currently-tracked canonical path that *would* be ignored if newly added. Verified empirically: a tracked file matching an active `.gitignore` rule returns no match without `--no-index`, and the correct match with it. **(2)** `git ls-files | xargs` without NUL-delimiting splits on whitespace, corrupting any of the many paths in this repository containing a space (samples, quarantined files) — `git ls-files -z` paired with `xargs -0` addresses every path as one argument regardless of spaces, parentheses, or the one non-ASCII filename.

It must print nothing. Anything it prints is canonical truth in an ignored path — RP7 violated, and the single most dangerous mistake this layout can make.

**No `.gitignore` or `.gitattributes` file is written in Phase 3A.** Their exact contents are drafted in §Z.2 for Phase 3B to apply.

---

## X. Path Stability Rules

Phase 2 §AA computes the source manifest over **sorted `[relative_path, content_sha256]` pairs**, and §AI.2 calls this *"the one place repository layout touches the data model."* Six rules follow.

**X.1 — A canonical path is a total function of identifiers.** No canonical path contains a title, a date, a description or any human-chosen label. Consequence: **no canonical file ever needs renaming**, so the largest source of manifest churn cannot arise (RP2).

**X.2 — Files are not IDs.** The identifier is inside the file; the path renders it. A rename never changes domain identity, and identity is never read from a path. **The index builder must read every identifier from file content, and a mismatch between path and content is an integrity failure** (§AB check 14). This is what makes a badly-performed manual repair *detectable* rather than silently authoritative.

**X.3 — Exactly two paths carry policy, and both are backed by in-file metadata.** `knowledge/_quarantine/` (retrieval policy, §N.3) and the two ingestion entry points (`origin.kind`, §P.2). Both duplicate an authoritative in-file field, so the path is a second line of defence and never the source of truth. There is no third, and adding one requires an ADR.

**X.4 — Registry slugs are chosen once and are immutable.** `BRAND_ID`, `PRODUCT_ID`, `STYLE_ID`, `NARRATIVE_PATTERN_ID` and `KNOWLEDGE_ID` are human-chosen at registration (Phase 2 §E.1). **Changing a slug creates a new entity; it is not a rename.** A brand that rebrands gets a new `BRAND_ID`, and the old one keeps its history. Two limits, set here because paths are built from them: **brand slug ≤ 24 characters, product slug ≤ 32** — recalculated and loosened from the first pass's 16/24 by the external audit (§AI Correction 12); the full path arithmetic justifying this is §AC.1.

**X.5 — Every move of a tracked file is recorded in `docs/MIGRATIONS.md`.** Date, commit, from → to, reason. Because the manifest hashes relative paths, a pure move changes the manifest hash while changing no content — the log is what turns an alarming hash change into an attributable one. This applies to Phase 3B and to every later structural change, including a future decision to shard the ledger directories.

**X.6 — Generated paths are constructed in exactly one place.** `src/creative_os/store/` owns every path convention in §F–§I. No service, adapter, Skill or script builds a canonical path by string concatenation. A layout change is then one module plus one migration-log entry, rather than a search across the codebase.

---

## Y. Migration Map

**Designed here. Not executed. No file has been moved, renamed, deleted or edited by Phase 3A, except this document itself.**

Every row below refers to a file verified present in the working tree on 2026-09-04 (§B). No file is invented. **The validation column below states only what each row must satisfy; the staged mechanism that proves it — including why a whole-tree hash-set comparison is the wrong tool — is §Z.4/§AB, corrected per the external audit's Correction 2.**

### Y.1 Moves and renames

| # | Current path | Target path | Action | Reason | Risk | Validation |
|---|---|---|---|---|---|---|
| 1 | `sources/original-books/breakthrough-advertising-0887232981-9780887232985 (1)_compressed.pdf` | `sources/books/breakthrough-advertising.pdf` | `git mv` | Phase 1 M1. Removes download noise from a path that Phase 3C's `source_files[]` will cite. | **Low** | target sha256 == baseline source sha256; source path absent |
| 2 | `sources/original-books/_OceanofPDF.com_The_brilliance_breakthrough_-_Eugene_schwartz.pdf` | `sources/books/brilliance-breakthrough.pdf` | `git mv` | Same. | **Low** | Same |
| 3 | `sources/methodology/` (empty, untracked) | — | `rmdir` | Empty; its intended contents have no resolvable upstream provenance in the repository (§B.4 finding 1) and belong in quarantine, not `sources/`. Git holds no empty directories, so nothing is committed. | **Low** | directory absent |
| 4 | `knowledge/methodology/` — 5 `.md` + 3 `.pdf` (8 files) | `knowledge/_quarantine/methodology/` | `git mv` (directory) | Phase 1 M2 and ADR-009 — highest priority. **Unmodified**: path only. PDFs and Markdown stay together (§N.2). | **Low** | all 8 targets' sha256 == baseline; old path absent |
| 5 | `knowledge/_quarantine/methodology/modulo-5-infraestructura-herramientas (1).md` | `…/modulo-5-infraestructura-herramientas.md` | `git mv` | Strips the browser download artefact ` (1)` from a filename that will become a stable reference. Renames one of the 8 files already moved in row 4 — not an additional file. | **Low** | sha256 identical to that file's row-4 baseline |
| 6 | `samples/**` — 15 media files | `media/_unregistered/**` (sub-structure and filenames preserved) | `git mv` (directory) | Phase 2 §AI.1 item 4 (target architecture). Entering as `origin.kind: REPOSITORY` ⇒ `REFERENCE`, which requires an entry point that is *not* `incoming/` (§P.2). | **Low** — no longer the asymmetric step; see row 7 | all 15 targets' sha256 == baseline; `samples/` absent |
| ~~7~~ | ~~`media/**`~~ | ~~—~~ | ~~`git rm -r --cached media`~~ | **REMOVED from Phase 3B (§AI Correction 7).** No durable payload strategy exists yet; untracking the only copies of these 15 files now would make cross-machine portability worse than today. **The 15 files stay tracked** at their new path through Phase 3B. Untracking becomes a separate, later, explicitly-approved **Media Cutover** (§O.3, §AG decision 2). | — | — |
| 8 | `knowledge/copywriting/schwartz/*.md` | unchanged | **KEEP** | Correct location, confirmed by Phase 1 §I (W1 RESOLVED) and by the brief. Not moved, not modified. | — | sha256 identical to the Phase 3A freeze commit |
| 9 | `PRE_FLIGHT_AUDIT.md`, `docs/PHASE_1…`, `docs/PHASE_2…`, `docs/PHASE_3…` | unchanged | **KEEP** | §V. Phase 2 §AI.1 item 7. | — | sha256 identical to the Phase 3A freeze commit |

**25 files touched by moves** (2 books + 8 quarantine, one of which is also renamed in row 5 + 15 samples = 25) **and every one hash-identical afterwards. All 25 remain tracked.** Phase 3B performs no content edit on any pre-existing file except `README.md`. *(Revision 1 of this document stated 27 and one untrack operation on the 15 samples; both are corrected here — the count was arithmetic, the untrack was sequencing, per §AI Corrections 2 and 7.)*

### Y.2 New files created by Phase 3B

| # | Path | Purpose |
|---|---|---|
| 10 | `.gitattributes` | `eol=lf` for text, `binary` for media. Fixes the cross-machine config-hash break (§AD R3). |
| 11 | `.gitignore` | **Repository-wide rules only** — secrets, Python residue, Claude Code local settings, OS cruft. No longer contains `var/` (§AI Correction 4; see row 20). |
| 12 | `.env.example` | Credential **names**, never values (§AC.4). |
| 13 | `README.md` | **Rewritten.** The current text is stale and misleading (§B.4 finding 9). |
| 14 | `docs/MIGRATIONS.md` | The from → to map of this migration, as the first entry (§X.5). |
| 15 | `store/README.md` | The canonical root's layout and contract; creates the directory. |
| 16 | `reviews/README.md` | States that `reviews/` is derived, pure and outside the source manifest; creates the directory (§Q.3, new in this revision). |
| 17 | `config/README.md` + the nine placeholder `*.yaml` + `config/styles/README.md` | Establishes the closed-list rule where it is enforced; placeholders fail closed (§J.3). |
| 18 | `knowledge/_quarantine/README.md` | Retrieval policy stated in the directory it governs (§N.3). |
| 19 | `media/.gitignore` + `media/README.md` | Directory exists on clone; ignore rule governs *future* untracked payloads only — it does not and cannot untrack the 15 files already tracked under it (§O.3). |
| 20 | `incoming/.gitignore` + `incoming/README.md` | The drop zone and how to use it without knowing an identifier. |
| 21 | `var/.gitignore` + `var/README.md` | **The ignore policy for `var/` now lives here, not in the root file** (§AI Correction 4). `var/.gitignore` itself is tracked, which is exactly why the rule cannot also live one level up. |

### Y.3 Repository configuration

| # | Action | Reason |
|---|---|---|
| 22 | `git config core.autocrlf false`, then `git add --renormalize .` | Local config plus one normalisation commit, so `.gitattributes` governs from the first checkout onward (§AD R3). |

**22 migration operations.** 6 moves/removals affecting 25 files (down from 7/27 — Correction 7 removes the untrack step, Correction 2 corrects the arithmetic), 15 file creations (one of which rewrites `README.md`, one of which — `reviews/README.md` — is new in this revision), 1 configuration change.

### Y.4 Explicitly **not** in Phase 3B, and the mandatory phase order that follows

| Deferred item | To | Why |
|---|---|---|
| Provenance for all **11** knowledge entities — **8 as in-file front matter** (3 Schwartz Markdown files + 5 quarantined Markdown modules) **and 3 as `.meta.yaml` sidecars** (the 3 quarantined PDFs, which cannot carry in-file front matter — §M.3, §AI Correction 18). **Not** `knowledge/_quarantine/README.md`, which Phase 3B creates as operator documentation and which is excluded from this requirement by construction, never by its own declaration (Phase 1 **M3**, §AI Correction 12) | **Phase 3C** | It is authoring, not migration. Keeping 3B to moves makes its central validation — *every moved file's hash is unchanged* — crisp and total. Mixing edits into it destroys that. |
| Section-tagging the `[Ampliación Externa]` blocks (Phase 1 **M5**) | **Phase 3C** | Requires reading and judgement (Phase 1 rates it Medium risk). |
| Authoring the compliance deny-list (Phase 1 **M4**) | **Phase 4+** | Policy content, not layout. Until then it is a placeholder that fails closed (§J.3). |
| OCR decision for *The Brilliance Breakthrough* (Phase 1 **M6**) | Optional, unscheduled | The derived layer already declares the limitation. |
| Registering the 15 media files in the Asset Registry (Phase 1 **M7**) | **Phase 5+** | Requires the ingestion service, the models and the validators (§P.3). |
| **The Media Cutover** — untracking registered payloads once a durable strategy exists | **A separate, later, explicitly-approved step** | Not part of Phase 3B (§AI Correction 7); not yet scheduled to any phase, because the payload strategy itself is not yet chosen (§O.6). |
| Creating `src/`, `tests/`, `.claude/skills/` | Phases 4 and 5 | RP11. |

**Phase 3C is a required precondition for Phase 4, not an optional follow-on — corrected per the external audit's Correction 8.** Phase 4's Skill design assumes every knowledge retrieval hit already carries `knowledge_id`, `tier` and `retrieval_policy` (Phase 2 P9); those fields do not exist on any file until Phase 3C authors them. The sequence is therefore fixed:

```
PHASE 3A  → external audit + freeze                              (this document, this pass)
PHASE 3B  → execute the physical migration of §Y.1–Y.3            → external validation + freeze
PHASE 3C  → author knowledge provenance records
            (front matter for the 8 Markdown entities +
             .meta.yaml sidecars for the 3 binary/PDF entities — M3) +
            section-tag unsourced Markdown blocks (M5) +
            validate retrieval policies for both carriers          → external audit + freeze
PHASE 4   → Skills design                                          — may not start before Phase 3C is frozen
```

**Wording corrected per §AI.7 Fix 23:** "author knowledge provenance front matter" describes only 8 of the 11 knowledge entities. Phase 3C authors *provenance records*, in whichever of the two carriers a given entity's format requires (§M.1.1).

**Neither Phase 3B nor Phase 3C is authorised by this document.** Each requires its own explicit request, exactly as Phase 3B did not authorise itself here.

---

## Z. Phase 3B Execution Plan

**Not executed. Proposed commands only, provided now that the structure is decided.** The intended execution environment is **Git Bash plus the standard Unix utilities bundled with it** — `git`, `sha256sum`, `mkdir`, `rmdir`, `find`, `grep`, `sort`, `comm`, `wc`, `cut`, `sed`, `diff`, `xargs`, `cat` — all verified present on this machine (§B.4 finding 6). **Corrected in this pass (§AI.7.9), then extended in the following editorial pass to add `cat`: earlier revisions of this line named only `git`, `sha256sum`, `mkdir` and `rmdir`, which understated what §AB.1's executable checks actually call.** Nothing requires Python, `ffmpeg` or `sqlite3`. §Z.1 adds a preflight step that checks every one of these utilities with `command -v` before anything else runs.

**Execution shell — corrected in this pass (§AI.7 Fix 24).** Earlier revisions of this document called the requirement "POSIX shell." That is false: §Z.3's manifest-building code depends on Bash arrays (`SRC=(...)`, `TGT=(...)`), Bash's `"${!SRC[@]}"` index expansion, and ANSI-C quoting (`$'\t'`) for the tab-delimited manifest — none of which a generic POSIX `sh` (`dash`, a minimal `busybox sh`, and similar) is required to support. Stated plainly, for whoever runs these commands:

- **Bash / Git Bash — supported**, and the intended execution environment for every command block in §Z. On this machine, that is Git Bash.
- **PowerShell — do not paste these blocks directly.** PowerShell's syntax for arrays, conditionals, `read`, and quoting is different enough that a pasted Bash block will fail or, worse, partially execute with silently wrong semantics.
- **A generic POSIX `sh` — not guaranteed.** Some individual commands would work verbatim; the manifest-building code in §Z.3 specifically would not, because it is Bash-specific by construction, not by incidental style.

This is a documentation-accuracy correction, not a design change: nothing in §Z is rewritten into PowerShell, and no command's behaviour changes. The document simply now names the shell it already assumed correctly.

**This section has been revised twice: substantially by the first correction pass (Corrections 1–4 and 7), then at execution level by the final executability pass (Corrections 13–19, §AI.7). The first pass's four structural fixes still hold and are restated below; the second pass's corrections are woven into the commands themselves rather than summarised separately, since each fixes a specific step rather than a design-level structure:**

1. **Phase 3B branches from a Phase 3A freeze commit, not from `59cbe49` directly (Correction 1), and both freeze tags are now created idempotently (Correction 14).** `59cbe49` was the state *before* this document existed. Once this document is externally approved and committed, the tree at that new commit — containing the approved `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` — is the actual pre-migration baseline. `59cbe49` remains a real, older, named checkpoint (`phase-2-freeze`), but Phase 3B's clean-tree check, hash baseline and normal rollback target all move one freeze forward, to `phase-3a-freeze`. **This document does not know its own future commit hash and does not guess it** — every reference below uses the placeholder `<PHASE_3A_FREEZE_SHA>` until Phase 3A is actually committed and that value is known. **The precondition for making that commit is itself corrected (Correction 13): it no longer requires a clean tree before adding the very document being frozen — it requires that the *only* change in the tree is that document, checks that mechanically, commits, and only then checks for a clean tree.**
2. **Move validation is staged, not a whole-tree hash-set diff (Correction 2), and is now a genuinely executable manifest and loop, not a described comparison (Correction 19).** Comparing "every tracked file's hash before" against "every tracked file's hash after" cannot work once `.gitattributes` normalisation and new scaffold files are in the picture — normalisation can legitimately change bytes, and new files change the tracked-file count. The fix separates three questions that were conflated into one comparison: *did line-ending normalisation touch anything it must not have, checked at the committed-blob level, not the working tree* (§Z.2, revised again per Correction 15), *did each individual move preserve its content, verified by an explicit 25-row manifest and a single deterministic loop* (§Z.3–Z.4), and *are the new scaffold files what §Y.2 says they are* (§Z.5, checked by presence and structure, not by a pre-image that cannot exist for a new file).
3. **The merge strategy and the rollback strategy now agree (Correction 3).** A fast-forward merge (`--ff-only`) produces no merge commit, so `git revert <merge-sha>` in the old plan referred to a commit that does not exist under that strategy. The migration branch now merges with `--no-ff`, producing exactly one commit that represents the whole migration, tagged and revertible as a single unit.
4. **The 15 current samples are moved but not untracked (Correction 7).** §Z no longer contains a `git rm -r --cached media` step for the existing sample corpus. That untrack is deferred to a future, separately-approved Media Cutover (§O.3, §Y.1 row 7).
5. **`origin` now exists, and both freeze tags are published to it as an ordinary, non-destructive operational step** — recorded, not one of the numbered corrections, since it reflects a change in the world rather than a flaw in the design (§AI.7, operational update).

### Z.1 Freeze Phase 3A, then branch Phase 3B from that freeze

**Revised per the final executability pass's Corrections 13 and 14 (§AI.7).** The first pass's precondition — "clean tree before adding the approved document" — could never be satisfied, because the approved document *is* the pending change: this design document must itself be modified and committed to become frozen. The clean-tree requirement is correct, but it belongs **after** that commit, not before it. Separately, the first pass assumed `phase-2-freeze` already existed as a tag; it does not automatically, and the fix must not silently create or overwrite a tag that already points somewhere unexpected — a distinction between *the commit existing* and *the tag existing*, checked separately, for both freeze tags.

**Step −1 — tooling preflight, new in this pass (§AI.7.9 tooling wording correction).** Every external utility any command block in §Z or §AB.1 actually calls, checked with `command -v` before anything else runs. This is the mechanical form of the corrected claim above: not an assertion that these are present, but a check that stops before touching the repository if one is not.

```bash
required_commands="git sha256sum mkdir rmdir find grep sort comm wc cut sed diff xargs cat"
missing=0
for c in $required_commands; do
    command -v "$c" >/dev/null 2>&1 || { echo "STOP: required command not found: $c"; missing=1; }
done
[ "$missing" -eq 0 ] || { echo "Tooling preflight failed — do not proceed."; false; }
```

A failure here means stop before Step 0, not proceed and hope the missing utility is never actually called.

**Step 0 — make `phase-2-freeze` idempotent, and distinguish commit-existence from tag-existence:**

```bash
# COMMIT EXISTS: is the Phase 2 freeze commit itself present in this repository,
# independent of whether anything has ever pointed a tag at it?
if ! git cat-file -e 59cbe494cdaef3a716283534b3bbea511c3c614d^{commit} 2>/dev/null; then
    echo "STOP: expected Phase 2 commit 59cbe494cdaef3a716283534b3bbea511c3c614d is not present."
    exit 1
fi

# TAG EXISTS: a separate question. If the tag is already there, verify it — never retag it.
# phase-2-freeze is an ANNOTATED tag, so `git rev-parse phase-2-freeze` alone
# returns the TAG OBJECT's own SHA, not the commit it points at. Every
# comparison against a commit SHA must peel the tag with ^{commit} first
# (§AI.7 Fix 20) — comparing the unpeeled value here would never match.
if git rev-parse -q --verify refs/tags/phase-2-freeze >/dev/null 2>&1; then
    existing=$(git rev-parse "phase-2-freeze^{commit}")
    if [ "$existing" != "59cbe494cdaef3a716283534b3bbea511c3c614d" ]; then
        echo "STOP: phase-2-freeze exists but resolves to $existing, not the expected commit."
        echo "Never silently retag a conflicting tag — investigate before proceeding."
        exit 1
    fi
    echo "phase-2-freeze already exists and correctly resolves to the Phase 2 commit — nothing to do."
else
    git tag -a phase-2-freeze 59cbe494cdaef3a716283534b3bbea511c3c614d \
        -m "Phase 2 data architecture frozen; historical checkpoint"
    echo "phase-2-freeze created."
fi
```

**Step A — the precise pre-freeze precondition, then commit, then the clean-tree check (Correction 13):**

```bash
# Mechanical precondition: exactly one changed path in the ENTIRE working tree
# (tracked or untracked), and it must be this design document. Nothing else —
# no other tracked modification, no other untracked file of any kind.
status_lines="$(git status --porcelain)"
count="$(printf '%s\n' "$status_lines" | grep -c .)"
only_path="$(printf '%s\n' "$status_lines" | sed -n '1{s/^...//p}')"

if [ "$count" -ne 1 ] || [ "$only_path" != "docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md" ]; then
    echo "STOP: the working tree has changes beyond the design document. Investigate before freezing."
    printf '%s\n' "$status_lines"
    exit 1
fi
echo "Precondition satisfied: only docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md is changed."

git add docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md
git commit -m "Freeze Phase 3A repository & migration design (external audit corrections applied)"

# The clean-tree requirement belongs HERE — after the design document is
# committed, not before it was added:
git status --porcelain    # must now print nothing
```

**Then tag the freeze, idempotently — the same discipline as Step 0, applied to a tag whose target commit is now known because it was just made:**

```bash
git rev-parse HEAD               # → <PHASE_3A_FREEZE_SHA>, recorded for every reference below

if git rev-parse -q --verify refs/tags/phase-3a-freeze >/dev/null 2>&1; then
    # Again peeled: phase-3a-freeze will also be annotated (per the tag command
    # below), so its own SHA is a tag-object SHA, not the commit it points at.
    existing=$(git rev-parse "phase-3a-freeze^{commit}")
    head=$(git rev-parse HEAD)
    if [ "$existing" != "$head" ]; then
        echo "STOP: phase-3a-freeze already exists and resolves to $existing, not this freeze commit ($head)."
        echo "Never silently retag a conflicting tag — investigate before proceeding."
        exit 1
    fi
    echo "phase-3a-freeze already exists and correctly resolves to this freeze commit — nothing to do."
else
    git tag -a phase-3a-freeze -m "Phase 3A repository design frozen; Phase 3B baseline"
fi
```

`phase-2-freeze` (`59cbe49`) remains tagged as the older historical checkpoint — the data architecture's freeze point — and is never moved or retagged. `phase-3a-freeze` is the new, normal baseline for everything that follows.

**Operational — publish both freeze tags to `origin`, now that it exists (§AI.7).** This is an operator synchronisation step, not a canonical architecture dependency: Phase 3B does not require `origin` to exist and remains fully usable from a local-only clone. Verify the remote before pushing, and never force:

```bash
if git remote get-url origin >/dev/null 2>&1; then
    git push origin phase-2-freeze
    git push origin phase-3a-freeze
else
    echo "No 'origin' remote configured on this machine — both tags remain local only."
    echo "Publish them once a remote exists, on whichever machine created them."
fi
```

**Step B — Phase 3B's actual pre-migration checks, run against `phase-3a-freeze`:**

```bash
# 0. Clean tree is a precondition, not a suggestion — now genuinely satisfiable,
#    because the design document was committed in Step A above, not left pending.
git status --porcelain           # must print nothing
git rev-parse --abbrev-ref HEAD  # expect: master
git rev-parse HEAD                          # expect: <PHASE_3A_FREEZE_SHA>
git rev-parse "phase-3a-freeze^{commit}"    # expect: the same value — the tag, PEELED to a commit, must match HEAD

# 1. Confirm the older checkpoint is still reachable and untouched.
git rev-parse "phase-2-freeze^{commit}"     # expect: 59cbe494cdaef3a716283534b3bbea511c3c614d

# 2. Record the hash of every tracked file at the Phase 3A freeze. This is the
#    full-tree reference point for §AB check 15 (frozen-document integrity) —
#    it is NOT compared as a whole set against the post-migration tree (Correction 2).
git ls-files -z | xargs -0 sha256sum > /tmp/phase-3a-freeze-hashes.txt
wc -l < /tmp/phase-3a-freeze-hashes.txt        # expect: 33 (the 32 files enumerated in §B, plus this document)

# 3. Work on a branch. master stays at phase-3a-freeze and untouched throughout.
git switch -c phase-3b-migration
```

### Z.2 Line endings and the root ignore file — with the committed-blob frozen-document check the audit requires

`.gitattributes` must land **before** any move, so every later commit is normalised. **Revised per Correction 15 (§AI.7): the check must compare committed Git content, not working-tree bytes.** The first pass hashed the working tree before and after `git add --renormalize .` — but `--renormalize` operates on index-normalisation semantics, and a working-tree sha256 proves nothing about what actually lands in a commit. The only proof that matters is: does the blob at a given path differ between the commit at `phase-3a-freeze` and the commit produced by the normalisation step. **Four documents are protected, not three** — `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` itself was frozen in §Z.1 and must not be silently renormalised into different committed bytes either:

```bash
# --- Z.2a: frozen-document hashes of the COMMITTED BLOB at phase-3a-freeze --
for f in PRE_FLIGHT_AUDIT.md docs/PHASE_1_SYSTEM_DESIGN.md docs/PHASE_2_DATA_ARCHITECTURE.md \
         docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md; do
    printf '%s\t%s\n' "$f" "$(git show phase-3a-freeze:"$f" | sha256sum | cut -d' ' -f1)"
done > /tmp/frozen-docs-committed-before.tsv
cat /tmp/frozen-docs-committed-before.tsv
```

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

```bash
# --- Z.2b: frozen-document hashes of the COMMITTED BLOB at HEAD, AFTER the
#     normalisation commit — must be unchanged from Z.2a -----------------------
for f in PRE_FLIGHT_AUDIT.md docs/PHASE_1_SYSTEM_DESIGN.md docs/PHASE_2_DATA_ARCHITECTURE.md \
         docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md; do
    printf '%s\t%s\n' "$f" "$(git show HEAD:"$f" | sha256sum | cut -d' ' -f1)"
done > /tmp/frozen-docs-committed-after.tsv

diff /tmp/frozen-docs-committed-before.tsv /tmp/frozen-docs-committed-after.tsv \
    && echo "FROZEN DOCUMENTS UNCHANGED AT THE COMMITTED-BLOB LEVEL — safe to continue" \
    || { echo "STOP: normalisation altered the committed bytes of a frozen document. Investigate before proceeding." ; exit 1; }

# Equivalent, and useful as a second confirmation: an exact content diff between
# the two commits, restricted to these four paths, should be empty.
git diff --exit-code phase-3a-freeze HEAD -- \
    PRE_FLIGHT_AUDIT.md docs/PHASE_1_SYSTEM_DESIGN.md docs/PHASE_2_DATA_ARCHITECTURE.md \
    docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md \
    && echo "git diff confirms: no content change to any frozen document"
```

**These four files were already LF in the working tree at inventory time (§B.4), so this check is expected to pass trivially — but Correction 2 (and, more pointedly, Correction 15) is explicit that "expected to pass" and "verified to pass at the committed-blob level" are different claims, and only the second is acceptable for a frozen document.** A working-tree-only comparison would have passed even if `--renormalize` had produced a different commit than intended, because it never inspects what actually got committed. If either check ever fails, the correct response is to stop and diagnose — never to proceed and reconcile later.

Then the root ignore file — **repository-wide rules only, per Correction 4.** `var/` is deliberately absent; `var/.gitignore` owns that directory's own policy (§Q):

```bash
cat > .gitignore <<'EOF'
# Secrets
.env
.env.*
!.env.example

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
git commit -m "Add repository-wide ignore rules and credential template"
```

### Z.3 Move baseline — an explicit, machine-readable manifest of all 25 files (Correction 19)

**Captured after the `.gitattributes` commit and before any `git mv`.** Revised per Correction 19: the first pass's `find`-based baseline recorded hashes but not the `source_path` → `target_path` mapping in an executable form, leaving §Z.4's verification as a human-read comment rather than a real check. This pass builds the mapping as two explicit, parallel, 25-entry arrays — never a directory scan — precisely so that the 25 files (which include names with spaces, parentheses, and one non-ASCII character) are addressed by exact string, never by word-splitting or glob expansion:

```bash
SRC=(
  "sources/original-books/breakthrough-advertising-0887232981-9780887232985 (1)_compressed.pdf"
  "sources/original-books/_OceanofPDF.com_The_brilliance_breakthrough_-_Eugene_schwartz.pdf"
  "knowledge/methodology/Dominio del Post ID_ Escalamiento y Prueba Social en Meta.pdf"
  "knowledge/methodology/Escalamiento Creativo y Prueba Social en Meta Ads.pdf"
  "knowledge/methodology/Metodología Evolve para Testeo Creativo en Meta Ads.pdf"
  "knowledge/methodology/modulo-1-estrategia-mercado.md"
  "knowledge/methodology/modulo-2-psicologia-persuasion.md"
  "knowledge/methodology/modulo-3-anuncios-estaticos.md"
  "knowledge/methodology/modulo-4-ugc-vsl-strategy.md"
  "knowledge/methodology/modulo-5-infraestructura-herramientas (1).md"
  "samples/style-references/animation/WhatsApp Video 2026-09-03 at 10.00.56 PM.mp4"
  "samples/style-references/animation/WhatsApp Video 2026-09-03 at 10.02.18 PM.mp4"
  "samples/style-references/animation/WhatsApp Video 2026-09-03 at 10.54.06 PM.mp4"
  "samples/style-references/podcast/WhatsApp Video 2026-09-03 at 10.04.02 PM.mp4"
  "samples/style-references/podcast/WhatsApp Video 2026-09-03 at 10.04.04 PM.mp4"
  "samples/style-references/podcast/WhatsApp Video 2026-09-03 at 10.54.05 PM.mp4"
  "samples/style-references/ugc/WhatsApp Video 2026-09-03 at 10.01.37 PM.mp4"
  "samples/style-references/ugc/WhatsApp Video 2026-09-03 at 10.02.19 PM (1).mp4"
  "samples/style-references/ugc/WhatsApp Video 2026-09-03 at 10.02.19 PM.mp4"
  "samples/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.01.37-PM.wav"
  "samples/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.02.19-PM-_1_.wav"
  "samples/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.02.19-PM.wav"
  "samples/voices/chile/male/ssstik.io_1788494437870.mp3"
  "samples/voices/chile/male/ssstik.io_1788494482734.mp3"
  "samples/voices/chile/male/ssstik.io_1788494597329.mp3"
)

TGT=(
  "sources/books/breakthrough-advertising.pdf"
  "sources/books/brilliance-breakthrough.pdf"
  "knowledge/_quarantine/methodology/Dominio del Post ID_ Escalamiento y Prueba Social en Meta.pdf"
  "knowledge/_quarantine/methodology/Escalamiento Creativo y Prueba Social en Meta Ads.pdf"
  "knowledge/_quarantine/methodology/Metodología Evolve para Testeo Creativo en Meta Ads.pdf"
  "knowledge/_quarantine/methodology/modulo-1-estrategia-mercado.md"
  "knowledge/_quarantine/methodology/modulo-2-psicologia-persuasion.md"
  "knowledge/_quarantine/methodology/modulo-3-anuncios-estaticos.md"
  "knowledge/_quarantine/methodology/modulo-4-ugc-vsl-strategy.md"
  "knowledge/_quarantine/methodology/modulo-5-infraestructura-herramientas.md"
  "media/_unregistered/style-references/animation/WhatsApp Video 2026-09-03 at 10.00.56 PM.mp4"
  "media/_unregistered/style-references/animation/WhatsApp Video 2026-09-03 at 10.02.18 PM.mp4"
  "media/_unregistered/style-references/animation/WhatsApp Video 2026-09-03 at 10.54.06 PM.mp4"
  "media/_unregistered/style-references/podcast/WhatsApp Video 2026-09-03 at 10.04.02 PM.mp4"
  "media/_unregistered/style-references/podcast/WhatsApp Video 2026-09-03 at 10.04.04 PM.mp4"
  "media/_unregistered/style-references/podcast/WhatsApp Video 2026-09-03 at 10.54.05 PM.mp4"
  "media/_unregistered/style-references/ugc/WhatsApp Video 2026-09-03 at 10.01.37 PM.mp4"
  "media/_unregistered/style-references/ugc/WhatsApp Video 2026-09-03 at 10.02.19 PM (1).mp4"
  "media/_unregistered/style-references/ugc/WhatsApp Video 2026-09-03 at 10.02.19 PM.mp4"
  "media/_unregistered/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.01.37-PM.wav"
  "media/_unregistered/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.02.19-PM-_1_.wav"
  "media/_unregistered/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.02.19-PM.wav"
  "media/_unregistered/voices/chile/male/ssstik.io_1788494437870.mp3"
  "media/_unregistered/voices/chile/male/ssstik.io_1788494482734.mp3"
  "media/_unregistered/voices/chile/male/ssstik.io_1788494597329.mp3"
)

[ "${#SRC[@]}" -eq 25 ] && [ "${#TGT[@]}" -eq 25 ] || { echo "STOP: manifest arrays are not both length 25"; exit 1; }

: > /tmp/move-baseline.tsv
for i in "${!SRC[@]}"; do
    h="$(sha256sum "${SRC[$i]}" | cut -d' ' -f1)"
    printf '%s\t%s\t%s\n' "${SRC[$i]}" "${TGT[$i]}" "$h" >> /tmp/move-baseline.tsv
done

wc -l < /tmp/move-baseline.tsv    # expect: 25

# The media-only subset — the 15 entries whose source is under samples/ — is
# split out here, once, because §AA.3's rollback verification must compare
# against ONLY these 15, never against all 25 (Correction 16):
grep '^samples/' /tmp/move-baseline.tsv > /tmp/media-baseline.tsv
wc -l < /tmp/media-baseline.tsv   # expect: 15
```

This manifest — `source_path`, `target_path`, `sha256`, tab-separated — is the input to §Z.4's verification loop and to §AA.3's rollback check. **It is a temporary file in `/tmp`, not a canonical repository artefact**; it is never committed and carries no meaning once the migration it verifies is complete.

### Z.4 Moves, followed by one mechanical verification loop over the whole manifest (Correction 19)

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

# --- media, remains tracked through Phase 3B (Correction 7) ----------------
mkdir -p media
git mv samples media/_unregistered
git commit -m "Move sample media under the media root; remains tracked pending a durable payload strategy"
```

**A single deterministic verification loop, run once, over every one of the 25 rows in `/tmp/move-baseline.tsv` — not three separate spot-checks and not a human reading `sha256sum` output.** Reading each line whole with `IFS=$'\t' read -r`, rather than word-splitting, is what makes spaces, parentheses and the one non-ASCII filename (`Metodología…`) transparent to this loop: none of them contain a tab, so none of them can be misparsed.

```bash
fail=0
while IFS=$'\t' read -r src tgt want; do
    if [ -e "$src" ]; then
        echo "FAIL: source still present, should have been moved: $src"
        fail=1
        continue
    fi
    if [ ! -e "$tgt" ]; then
        echo "FAIL: target missing: $tgt"
        fail=1
        continue
    fi
    got="$(sha256sum "$tgt" | cut -d' ' -f1)"
    if [ "$got" != "$want" ]; then
        echo "FAIL: hash mismatch at $tgt (expected $want, got $got)"
        fail=1
    fi
done < /tmp/move-baseline.tsv

if [ "$fail" -ne 0 ]; then
    echo "STOP: one or more of the 25 moves failed verification. Do not proceed to §Z.5."
    exit 1
fi
echo "ALL 25 MOVES VERIFIED: source absent, target present, hash matches, for every row."

git ls-files media | wc -l    # expect: 15 — still tracked, deliberately (§O.3)
```

**This loop's exit status is the pass/fail signal, not a transcript for a human to read and judge.** Any single row's failure — a missing target, a present source, a mismatched hash — halts before scaffolding begins, and names exactly which of the 25 rows is wrong, without implicating the other 24. This is what Correction 19 means by "mechanical": the check must be able to run unattended and return a verdict, not merely print numbers next to each other for a human to eyeball.

### Z.5 Scaffold

```bash
mkdir -p store reviews config/styles incoming var
# READMEs, the nine placeholder registries and the remaining .gitignore files
# (var/.gitignore now included here, owning var/'s own ignore policy — Correction 4)
# are written here (contents per §J.3 and §Y.2), then:
git add -A
git commit -m "Scaffold canonical store, reviews, config registries, ingestion and runtime roots"
```

**New-file validation is presence and structure, never a pre-image comparison (Correction 2's closing point).** A file created in this step has no "before" state to diff against; §AB checks 4, 16 and the config-registry count check apply here.

### Z.6 Documentation and merge

```bash
# README.md rewritten; docs/MIGRATIONS.md created with this migration as entry 001.
git add README.md docs/MIGRATIONS.md
git commit -m "Rewrite README for the Phase 3 structure; open the migration log"

# Run the full validation checklist (§AB) against phase-3b-migration BEFORE merging. Only then:
git switch master
git merge --no-ff phase-3b-migration -m "Merge Phase 3B repository migration"
git tag -a phase-3b-complete -m "Repository migration complete and validated"
```

**The `--no-ff` merge is deliberate and required by the rollback design (Correction 3).** It produces exactly one commit representing the entire migration — every move, every scaffold file, every configuration change — which is what makes `git revert -m 1 <the merge commit>` in §AA a single, coherent, attributable reversal rather than an operation with nothing to point at.

### Z.7 Optional, after merge

```bash
git gc --aggressive --prune=now    # compacts 136 MB of loose objects; changes no commit
```

---

## AA. Rollback Plan

**Phase 3B must be reversible, and rollback must not depend on deleting anything. This section is revised per the external audit's Corrections 1 and 3 (§AI): the normal rollback target moves forward to the Phase 3A freeze, and the post-merge mechanism now matches the `--no-ff` merge strategy of §Z.6.**

### AA.1 The targets — two freeze commits, two different purposes

| Tag | Commit | What it represents | When rollback should target it |
|---|---|---|---|
| `phase-2-freeze` | `59cbe494cdaef3a716283534b3bbea511c3c614d` | The frozen Phase 2 data architecture, **before this repository design document existed** | Only if the repository design itself (this document) needs to be un-approved and redone — an older, historical checkpoint, not the normal case |
| `phase-3a-freeze` | `<PHASE_3A_FREEZE_SHA>` — recorded once this document is committed (§Z.1) | The approved Phase 3A design, **immediately before any physical migration** | **The normal rollback target for Phase 3B.** Everything this document specifies is reachable from it, and so is the approved design document itself |

**This corrects the first pass's central error:** requiring Phase 3B's clean-tree check to expect `HEAD == 59cbe49` cannot survive this document itself being committed and approved — the approval *is* a commit, and a "clean tree at `59cbe49`" precondition would be false the moment the thing it is a precondition for exists. Rollback normally returns to `phase-3a-freeze` precisely so the approved repository design is never lost as a side effect of undoing the physical migration.

### AA.2 The mechanism

All work happens on `phase-3b-migration`, branched from `phase-3a-freeze` (§Z.1). `master` is never modified until the validation checklist passes, so rollback before the merge is:

```bash
git switch master                    # master is still at <PHASE_3A_FREEZE_SHA>
git branch -D phase-3b-migration     # only after deciding to abandon
```

Physical-workspace cleanup for this pre-merge case is covered by AA.3 below — abandoning the branch does not, by itself, remove untracked or newly-created directories from the working tree.

**After the `--no-ff` merge, rollback is a single-parent revert of the one merge commit** — corrected from the first pass, which specified `git revert <merge-sha>` under a `--ff-only` strategy that produces no merge commit for that command to target:

```bash
git revert -m 1 <PHASE_3B_MERGE_COMMIT>
```

`-m 1` tells git which parent side represents "the mainline to revert back to" — `master` as it stood before the merge — which is the correct choice because `master` is the side with a single, linear ancestor chain; the migration's whole history lives on the merged-in side. The revert is one commit, it reverses the whole migration as a unit, and the reversal itself is attributable (`git log` shows it, and it is exactly what `docs/MIGRATIONS.md` should record).

`git reset --hard phase-3a-freeze` is available and is **not** recommended: on a shared branch it discards commits other clones may hold, and the design's whole posture is that destructive deletion is not the normal mechanism.

### AA.3 Restoring a clean physical workspace — before or after the merge, and never via `git clean -fdx`

**This subsection is new, added per Correction 3, and its media-verification step is further corrected per Correction 16 (§AI.7).** The prior pass compared all 25 baseline hashes against only the 15 media files actually present, a comparison that could never succeed; the fix (below) checks each of the 15 media rows against its own dedicated baseline. Two ordinary git operations are each, individually, insufficient to leave a clean workspace after abandoning or reverting Phase 3B: switching branches does not remove directories the migration created that git does not track the emptiness of, and a `git revert` restores tracked file *content* but does not, by itself, guarantee every stray untracked byproduct is gone. Four requirements shape the procedure below, stated before the commands so each command's purpose is legible:

- **Never lose media bytes.** The 15 samples are tracked through Phase 3B (§Z.4), so an ordinary `git switch`/`git revert` already restores their tracked content correctly — the risk is confined to untracked material that never existed before Phase 3B.
- **Verify hashes before relocating anything.** No physical move happens on the strength of "git says this is fine" alone; the hash check is the same discipline as §Z.4, applied in reverse.
- **Restore the pre-migration physical layout when abandoning 3B**, not merely the pre-migration tracked-file list.
- **Remove only paths this design's own scaffolding created**, and only after verifying they hold nothing unexpected — never a broad `git clean -fdx`, which would delete indiscriminately, including anything an operator placed in `incoming/` or generated into `var/` for reasons unrelated to the migration.

**Procedure — abandoning before the merge (branch still exists):**

```bash
# 1. Confirm what the branch actually changed, before touching anything physical.
git diff --stat phase-3a-freeze phase-3b-migration

# 2. Verify the 15 media files against ONLY their own baseline (Correction 16) —
#    /tmp/media-baseline.tsv, the 15-row subset of /tmp/move-baseline.tsv split
#    out in §Z.3, never the full 25-row manifest, and never as an unordered
#    hash set: each row's TARGET path is checked against ITS OWN recorded hash,
#    preserving the path ↔ hash mapping rather than merely comparing two sets.
fail=0
while IFS=$'\t' read -r src tgt want; do
    if [ ! -e "$tgt" ]; then
        echo "FAIL: expected media file missing: $tgt"
        fail=1
        continue
    fi
    got="$(sha256sum "$tgt" | cut -d' ' -f1)"
    if [ "$got" != "$want" ]; then
        echo "FAIL: hash mismatch at $tgt (expected $want, got $got)"
        fail=1
    fi
done < /tmp/media-baseline.tsv

if [ "$fail" -ne 0 ]; then
    echo "STOP: media verification failed. Do not proceed with abort/restore."
    exit 1
fi
echo "All 15 media files verified against media-baseline.tsv — safe to restore."

# 3. Return to master. The physical worktree still reflects phase-3b-migration's
#    state until checked out; switching branches restores the tracked files
#    samples/** used to be (git handles this because they were tracked at
#    phase-3a-freeze and remain tracked on phase-3b-migration, merely moved).
git switch master

# 4. Remove ONLY the scaffold directories this design's own commands created,
#    and only after confirming (via git status / a directory listing) that
#    they hold nothing but what Phase 3B put there.
for d in store reviews config incoming var; do
    [ -d "$d" ] && [ -z "$(git status --porcelain "$d")" ] && rmdir --ignore-fail-on-non-empty "$d" 2>/dev/null
done

# 5. Discard the branch.
git branch -D phase-3b-migration
git status --porcelain    # expect: nothing
```

**Procedure — reverting after the merge:**

```bash
git revert -m 1 <PHASE_3B_MERGE_COMMIT>
# The revert restores samples/** as tracked files at their pre-migration path
# and content (git reverses the git mv), and removes the scaffold files this
# design added. Untracked leftovers (a stray var/ cache directory, an operator
# file dropped in incoming/ after the migration) are NOT touched by a revert —
# check for them explicitly and remove deliberately, never with git clean -fdx:
git status --porcelain    # anything listed here is untracked and needs a human decision
```

**`git clean -fdx` is never used at any point in either procedure.** It does not distinguish a directory this migration created from one an operator has since used for something else, and the whole point of this subsection is that the two must never be conflated.

### AA.4 The one asymmetry that remains, and why it is now smaller than before

Deferring the media untrack out of Phase 3B (§AI Correction 7) removes what the first pass called "the one asymmetric step" almost entirely: through Phase 3B, the 15 samples stay tracked, so an ordinary revert already restores them correctly, with no separate `git checkout <tag> -- samples/` recovery step required. The asymmetry moves, not disappears — it becomes a property of the **future Media Cutover**, which is out of scope for this document and must carry its own rollback design when it is proposed (§AG decision 2).

### AA.5 What rollback cannot restore

Nothing, for Phase 3B as designed — every operation is a move, a new file, or (per §AA.3) a directory whose emptiness is verified before removal, and all are revertible. This property is a *consequence* of deferring M3/M5 to Phase 3C (§Y.4): a content edit to a knowledge file would be revertible in git but would have invalidated any hash pinned in the interim. Phase 3C must carry its own rollback design, and it should run when no pinned hashes exist yet — which is now.

---

## AB. Migration Validation Checklist

Every check below is mechanical and runnable with the tooling verified present (§B.4 finding 6), and every check that names a comparison names an actual executable comparison, not a description of one a human is expected to eyeball (§AI.7 Correction 19). Phase 3B is not complete until every check through 17 passes. **Checks 2 and 3 are revised twice** — first per Correction 2 (a whole-tree hash-set diff cannot survive normalisation or new scaffold files; both became per-file baseline checks), then per Corrections 15 and 19 (check 2 now compares *committed blobs*, not working-tree bytes, and protects **four** documents, not three; check 3 now names an actual executable verification loop, not a described comparison). **Checks 8 and 9 are revised per Correction 7 and, for check 8, again per Correction 17** — the 15 samples remain tracked through Phase 3B, so "untracked media" was never the right assertion for check 9; and check 8's first restatement ("no non-media tracked file exceeds 1 MB") was still wrong, because the two intentionally-tracked source books in `sources/books/` are 2.7 MB and 6.3 MB and are neither media nor an oversight.

| # | Check | Command / criterion | Pass |
|---|---|---|---|
| 1 | Clean tree before starting | `git status --porcelain` prints nothing, at `phase-3a-freeze` | ☐ |
| 2 | **Frozen documents unchanged by normalisation, at the committed-blob level — not the working tree** | §Z.2a/Z.2b's `git show phase-3a-freeze:<path>` vs `git show HEAD:<path>` hash pair matches, and the equivalent `git diff --exit-code` is empty, for all **four** protected documents: `PRE_FLIGHT_AUDIT.md`, `docs/PHASE_1_SYSTEM_DESIGN.md`, `docs/PHASE_2_DATA_ARCHITECTURE.md`, **and `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` itself** (§AI.7 Correction 15) | ☐ |
| 3 | **Each moved file matches its individual baseline, verified by the mechanical loop of §Z.4, not by eye** | For every one of the 25 `(source_path, target_path)` rows in `/tmp/move-baseline.tsv` (§Z.3): source path absent, target path present, target `sha256` equals that row's recorded hash — checked by an executable loop with a non-zero exit on any failure (§Z.4, Correction 19), never by a human reading `sha256sum` output side-by-side | ☐ |
| 4 | Expected new paths exist | `sources/books/{breakthrough-advertising,brilliance-breakthrough}.pdf`; `knowledge/_quarantine/methodology/` with 8 files; `media/_unregistered/` with 15 files, still tracked; `store/`, `reviews/`, `config/`, `incoming/`, `var/` | ☐ |
| 5 | Old paths absent | `samples/`, `knowledge/methodology/`, `sources/original-books/`, `sources/methodology/` all absent | ☐ |
| 6 | Rename detection survives | `git log --follow` resolves history for each renamed file | ☐ |
| 7 | **No canonical file is ignored, checked with `--no-index` so an already-tracked match is not silently missed (§AI.7 Fix 22)** | `git ls-files -z store config knowledge sources docs \| xargs -0 -r git check-ignore --no-index -v` prints **nothing**. NUL-delimited throughout, so no path with a space, parenthesis or the one non-ASCII filename is ever split | ☐ |
| 8 | **No *unexpected* large tracked file exists — checked against an explicit allow-list, not a blanket size rule (§AI.7 Correction 17)** | Every tracked file over 1 MB is one of exactly two allowed classes: **(a)** one of the 15 samples under `media/_unregistered/`, expected and temporary through Phase 3B (§O.3), or **(b)** one of the two intentionally-tracked source books under `sources/books/` — `breakthrough-advertising.pdf` (2.7 MB) and `brilliance-breakthrough.pdf` (6.3 MB), both raw and permanently tracked by design (§K). Any tracked file over 1 MB outside both classes fails this check. Among files not in either class, the largest is `docs/PHASE_2_DATA_ARCHITECTURE.md` at 330 KB | ☐ |
| 9 | **Media remains tracked, matching baseline, pending the Media Cutover** | `git ls-files media` lists `media/.gitignore`, `media/README.md`, and all 15 files under `media/_unregistered/`; every one of the 15 matches its §Z.3 baseline hash; **no `git rm --cached` has run against `media/`** | ☐ |
| 10 | Line endings uniform | `git ls-files --eol` shows `w/lf` for every text file and `-text` only for genuine binaries — including `modulo-2`, whose heuristic classification is now explicit (§B.5) | ☐ |
| 11 | **No duplicate canonical knowledge** | No basename appears both inside and outside `knowledge/_quarantine/`; each Schwartz file exists in exactly one location | ☐ |
| 12 | **No raw source silently promoted to trusted knowledge** | `sources/` contains only the two books; nothing moved from `sources/` into `knowledge/`; the three methodology PDFs are in `_quarantine/`, not `sources/`. **The wording justifying this rests only on what the metadata establishes** — that no authoritative upstream is present or resolvable in the repository — never on the stronger, unsupported claim that no original exists anywhere (§AI Correction 11) | ☐ |
| 13 | **Reference media retains reference-only status — corrected to allow `store/assets/` to be absent (§AI.7 Fix 25)** | **PASS if `store/assets/` does not exist, OR it exists and contains zero Asset Registry records and zero asset events.** Phase 3B's scaffold step (§Z.5) does not create `store/assets/` — RP11 forbids scaffolding an empty entity-scope directory just to satisfy a later check, and `mkdir -p store reviews config/styles incoming var` in §Z.5 names no `assets` subdirectory. The domain assertion this check protects is **no asset has been registered** — Phase 2 §S.4's fifteen `REFERENCE` assets remain unmade, which is correct before Phase 5 — not that a particular directory must exist. **Being tracked in git through Phase 3B is not registration** — a file's git-tracking state and its Asset Registry state are independent facts (§AI Correction 9) | ☐ |
| 14 | Path/content identity agreement | Vacuous now (`store/` is empty) — **but the check is defined and belongs to every later phase**: for every canonical file, the identifier in the path equals the identifier in the content (§X.2) | ☐ |
| 15 | Phase documents intact and readable, checked as committed blobs | `git show phase-3a-freeze:<path>` compared to the current committed content at `HEAD` for `PRE_FLIGHT_AUDIT.md`, `docs/PHASE_1_SYSTEM_DESIGN.md`, `docs/PHASE_2_DATA_ARCHITECTURE.md` (all three identical all the way back to `59cbe49`, since none of the three ever changes between any of the freezes) **and `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md`** (identical from `phase-3a-freeze` onward — it did change before that point, which is expected and fine); all four render | ☐ |
| 16 | **`reviews/` holds no canonical fact and sits outside the source manifest** | `reviews/` is empty of content at the end of Phase 3B (only `README.md`); nothing under it is referenced by `inputs[]` anywhere, because nothing referencing it exists yet — the check becomes load-bearing once Phase 5 starts writing renders (§AI Correction 6) | ☐ |
| 17 | **Phase 3C has not been started, and Phase 4 has not been started** | No provenance record exists on any knowledge entity yet — neither front matter on a Markdown file nor a `.meta.yaml` sidecar on a PDF (Phase 3C's job, §AI Correction 8, §AI.7 Fix 23); `.claude/skills/` does not exist | ☐ |

### AB.1 Executable commands for checks 1–17 (§AI.7 Fix 26)

**Every check above now has either a runnable command already given elsewhere in this document, or a runnable command below — no check in the Phase 3B list is left as prose a human must interpret.** Checks 1, 2 and 3 are not repeated here because §Z.1, §Z.2 and §Z.4 already give them as full executable blocks with a deterministic exit status; check 14 is intentionally **not** given a command, and is described plainly as such below, because the property it tests literally cannot be exercised before `store/` holds a first file — inventing a command against an empty directory would be theatre, not verification (Option B, per Fix 26, is the honest treatment for that one check only). Every other check gets an explicit block, each ending in an unambiguous pass/fail line.

**Revised per §AI.7.9 Fix 27: the block below is one unit with one aggregate exit status, not a sequence of independently-printed messages.** The first version of this block gave every check a `PASS`/`FAIL` *message*, but a message is not an exit status — `echo`, `printf` and `cat` all return 0 regardless of what they print, and with all seventeen-minus-four checks concatenated in one script, a later check's success could leave the shell's `$?` looking clean even after an earlier check printed `FAIL`. **`overall_fail` is declared once, at the top, and is set to `1` — never reset — the instant any check's own local failure is detected; the very last thing the block does is test `overall_fail` and emit exactly one aggregate line with `false`/`true` as its real, load-bearing exit status** (`false` rather than `exit 1`, so pasting this into an interactive Git Bash session reports failure without closing the shell):

```bash
overall_fail=0

# --- Check 4: expected new paths exist -------------------------------------
fail=0
for p in "sources/books/breakthrough-advertising.pdf" "sources/books/brilliance-breakthrough.pdf" \
         store reviews config incoming var; do
    [ -e "$p" ] || { echo "FAIL check 4: missing $p"; fail=1; overall_fail=1; }
done
[ -d knowledge/_quarantine/methodology ] && [ "$(find knowledge/_quarantine/methodology -type f | wc -l)" -eq 8 ] \
    || { echo "FAIL check 4: quarantine does not contain exactly 8 files"; fail=1; overall_fail=1; }
[ -d media/_unregistered ] && [ "$(find media/_unregistered -type f | wc -l)" -eq 15 ] \
    || { echo "FAIL check 4: media/_unregistered does not contain exactly 15 files"; fail=1; overall_fail=1; }
[ "$fail" -eq 0 ] && echo "PASS check 4"

# --- Check 5: old paths absent ----------------------------------------------
fail=0
for p in samples knowledge/methodology sources/original-books sources/methodology; do
    [ -e "$p" ] && { echo "FAIL check 5: old path still present: $p"; fail=1; overall_fail=1; }
done
[ "$fail" -eq 0 ] && echo "PASS check 5"

# --- Check 6: rename detection proves PRE-MIGRATION history is reachable, ---
#     not merely that the Phase 3B move commit exists (§AI.7.9 Fix 28).
#     For each row, resolve the last commit that touched the SOURCE path as
#     of phase-3a-freeze, then require that exact commit hash to appear in
#     the TARGET's own --follow history. A target whose --follow history
#     stops at the move commit and never reaches that pre-freeze commit has
#     NOT actually retained reachable pre-migration history, whatever its
#     own most recent commit looks like.
fail=0
while IFS=$'\t' read -r src tgt want; do
    pre_move_commit="$(git rev-list -1 phase-3a-freeze -- "$src")"
    if [ -z "$pre_move_commit" ]; then
        echo "FAIL check 6: no pre-migration commit found for source path: $src"
        fail=1; overall_fail=1
        continue
    fi
    if ! git log --follow --format='%H' -- "$tgt" | grep -qx "$pre_move_commit"; then
        echo "FAIL check 6: $tgt's --follow history does not reach pre-migration commit $pre_move_commit (source: $src)"
        fail=1; overall_fail=1
    fi
done < /tmp/move-baseline.tsv
[ "$fail" -eq 0 ] && echo "PASS check 6"

# --- Check 7: no canonical file is ignored (already given in §W, repeated for completeness) ---
out="$(git ls-files -z store config knowledge sources docs | xargs -0 -r git check-ignore --no-index -v)"
if [ -z "$out" ]; then
    echo "PASS check 7"
else
    echo "FAIL check 7:"; printf '%s\n' "$out"; overall_fail=1
fi

# --- Check 8: no unexpected large tracked file, checked against the two allowed classes ---
fail=0
while IFS= read -r -d '' f; do
    size=$(wc -c < "$f")
    [ "$size" -gt 1048576 ] || continue
    case "$f" in
        media/_unregistered/*) ;;                                             # class (a)
        sources/books/breakthrough-advertising.pdf) ;;                        # class (b)
        sources/books/brilliance-breakthrough.pdf) ;;                         # class (b)
        *) echo "FAIL check 8: unexpected large tracked file: $f ($size bytes)"; fail=1; overall_fail=1 ;;
    esac
done < <(git ls-files -z)
[ "$fail" -eq 0 ] && echo "PASS check 8"

# --- Check 9: media remains tracked, matching its own 15-row baseline ------
fail=0
tracked_media="$(git ls-files media)"
printf '%s\n' "$tracked_media" | grep -qx "media/.gitignore" \
    || { echo "FAIL check 9: media/.gitignore not tracked"; fail=1; overall_fail=1; }
printf '%s\n' "$tracked_media" | grep -qx "media/README.md" \
    || { echo "FAIL check 9: media/README.md not tracked"; fail=1; overall_fail=1; }
count="$(printf '%s\n' "$tracked_media" | grep -c '^media/_unregistered/')"
[ "$count" -eq 15 ] || { echo "FAIL check 9: expected 15 tracked files under media/_unregistered, found $count"; fail=1; overall_fail=1; }
while IFS=$'\t' read -r src tgt want; do
    got="$(sha256sum "$tgt" | cut -d' ' -f1)"
    [ "$got" = "$want" ] || { echo "FAIL check 9: hash mismatch at $tgt"; fail=1; overall_fail=1; }
done < /tmp/media-baseline.tsv
[ "$fail" -eq 0 ] && echo "PASS check 9"

# --- Check 10: line endings uniform -----------------------------------------
bad="$(git ls-files --eol | grep -v 'w/lf' | grep -v -- '-text')"
if [ -z "$bad" ]; then
    echo "PASS check 10"
else
    echo "FAIL check 10:"; printf '%s\n' "$bad"; overall_fail=1
fi

# --- Check 11: no duplicate canonical knowledge basename --------------------
comm -12 \
    <(find knowledge/_quarantine -type f -printf '%f\n' | sort) \
    <(find knowledge -type f -not -path 'knowledge/_quarantine/*' -printf '%f\n' | sort) \
    > /tmp/dupe-basenames.txt
if [ -s /tmp/dupe-basenames.txt ]; then
    echo "FAIL check 11: duplicate basenames:"; cat /tmp/dupe-basenames.txt; overall_fail=1
else
    echo "PASS check 11"
fi

# --- Check 12: source/quarantine placement ----------------------------------
fail=0
[ "$(find sources -type f | wc -l)" -eq 2 ] || { echo "FAIL check 12: sources/ does not hold exactly 2 files"; fail=1; overall_fail=1; }
find sources -type f -not -path 'sources/books/*' | grep -q . \
    && { echo "FAIL check 12: a file exists under sources/ outside sources/books/"; fail=1; overall_fail=1; }
[ "$(find knowledge/_quarantine/methodology -name '*.pdf' | wc -l)" -eq 3 ] \
    || { echo "FAIL check 12: quarantine does not hold exactly 3 PDFs"; fail=1; overall_fail=1; }
[ "$fail" -eq 0 ] && echo "PASS check 12"

# --- Check 13: store/assets/ absent OR present-and-empty (Fix 25) ----------
if [ ! -e store/assets ]; then
    echo "PASS check 13 (store/assets/ absent)"
else
    n="$(find store/assets -type f | wc -l)"
    if [ "$n" -eq 0 ]; then
        echo "PASS check 13 (store/assets/ present, empty)"
    else
        echo "FAIL check 13: store/assets/ contains $n files"; overall_fail=1
    fi
fi

# --- Check 14: NOT given a command — see note above; the property is vacuous
#     until store/ holds a first canonical file. Stated as a criterion for
#     every later phase to implement, not as a Phase 3B pass/fail line.
#     Deliberately does not touch overall_fail.

# --- Check 16: reviews/ holds nothing but its own README -------------------
n="$(find reviews -type f ! -name README.md | wc -l)"
if [ "$n" -eq 0 ]; then
    echo "PASS check 16"
else
    echo "FAIL check 16: reviews/ holds $n non-README file(s)"; overall_fail=1
fi

# --- Check 17: Phase 3C and Phase 4 have not started ------------------------
fail=0
grep -rl '^knowledge_id:' knowledge --include='*.md' 2>/dev/null | grep -q . \
    && { echo "FAIL check 17: front matter found — Phase 3C may have started"; fail=1; overall_fail=1; }
find knowledge -name '*.meta.yaml' 2>/dev/null | grep -q . \
    && { echo "FAIL check 17: a sidecar exists — Phase 3C may have started"; fail=1; overall_fail=1; }
[ -d .claude/skills ] && { echo "FAIL check 17: .claude/skills exists — Phase 4 may have started"; fail=1; overall_fail=1; }
[ "$fail" -eq 0 ] && echo "PASS check 17"

# --- Aggregate result — the ONE exit status that matters ---------------------
if [ "$overall_fail" -ne 0 ]; then
    echo "PHASE 3B VALIDATION FAILED"
    false
else
    echo "PHASE 3B VALIDATION PASSED"
    true
fi
```

**The exit status of this block, taken as a whole, is now the actual signal: `0` means every executable check in it passed; non-zero means at least one did not — regardless of what ran after it.** No individual `PASS` line printed earlier in the block can overwrite or hide an `overall_fail=1` set by an earlier check, because nothing resets `overall_fail` once set, and the final `if` reads its accumulated value rather than the exit status of whichever command happened to run last.

**Check 15 is likewise not repeated** — it is exactly §Z.2's committed-blob comparison, run once against the final state rather than around the normalisation commit specifically; the same block applies verbatim, and its own `exit 1` on mismatch (§Z.2) is deliberately a hard exit rather than an `overall_fail` flag, since it runs as its own standalone step at a specific point in §Z, not folded into this aggregate block.

Four structural checks that apply from Phase 5 onward and are stated here, at design time, so they are not invented later or discovered as a gap in code review:

| # | Check | Criterion |
|---|---|---|
| 18 | Config registry list is closed | `ls config/*.yaml \| wc -l` equals **9**, and the filenames match the whitelist of Phase 2 §B.1 exactly (§J.1) |
| 19 | No case-only path collisions | No two tracked paths are equal when lowercased — `core.ignorecase=true` makes such a pair unrepresentable on this machine and corrupting on a case-sensitive one (§AC.1) |
| 20 | **`EXT` allocation scans every product ledger, never one** | The allocator's `EXT` ordinal computation for a given run globs `store/products/*/ledger/extractions/EXT-<run-suffix>-*.json` and validates each match's `run_id` field — a code path that reads only the current product's ledger, or that reads a run-local registry, is a defect against §F.4 (§AI Correction 5) |
| 21 | **Every random-allocated identifier's writer retries on collision** | The write path for `CAMPAIGN_ID`, `RUN_ID` and `ASSET_ID` generates a candidate, attempts a create-exclusive write, and on `EEXIST` generates a new candidate rather than failing the operation or assuming the collision cannot occur — a writer with no retry branch is a defect against §F.5 (§AI Correction 10) |

---

## AC. Windows / Portability Review

### AC.1 Windows

| Hazard | Status under this design |
|---|---|
| **`MAX_PATH` (260)** | **Recalculated per §AI Correction 12**, against the actual deepest designed paths rather than a single representative one, because the external audit correctly declined to accept a looser cap without seeing the arithmetic. Four candidates, at brand ≤ 24 / product ≤ 32: campaign artefact `store/campaigns/CMP-<24>-<6hex>/creatives/CRE-<24>-<6hex>-NN/v10.json` ≈ 109 chars; **the binding constraint, a ledger record**, `store/products/PRD-<24>-<32>/ledger/observations/OBS-<32>-0000.json` ≈ **143 characters**; an extraction record ≈ 115 chars; a `reviews/` render ≈ 107 chars. Against this machine's repository root (43 chars): 43 + 143 = 186, **74 characters of headroom**. Against a pessimistic root — a longer username, or a path nested under a synced-folder or OneDrive prefix (≈ 100 chars): 100 + 143 = 243, **17 characters of headroom** — tight but positive. **Budget, revised: canonical relative paths ≤ 150, repository root ≤ 100.** Slug caps in X.4 (brand ≤ 24, product ≤ 32) are chosen to fit this budget with margin, not the reverse. `core.longpaths` is not set and is not needed at either cap. |
| **Case-insensitive filesystem** (`core.ignorecase=true`) | No path anywhere distinguishes two entities by case alone. Identifier prefixes are uppercase (`CMP-`, `CRE-`) and slugs lowercase, so paths are mixed-case but never case-*dependent*. Validation check 19. |
| **Symlinks unavailable** (`core.symlinks=false`) | The design uses none. No `latest` symlink — Phase 2 §G.5 makes `latest` a derived convenience anyway, and INV-12 forbids resolving a reference through it. |
| **Reserved device names** (`CON`, `PRN`, `AUX`, `NUL`, `COM1-9`, `LPT1-9`) | Checked, and one near-miss is worth recording: `CONCEPT_ID` is `CON-…`. Windows reserves the *exact* base name `CON` and `CON.<ext>`, not `CON-acme-3f8b21-03`, so no collision exists — **and in any case concepts are embedded in the Experiment Plan (Phase 2 §D.1) and get no file at all.** The hazard does not materialise on either count. |
| **Illegal characters** (`: * ? " < > \|`) | `RUN_ID` uses compact UTC (`RUN-20260904T1132Z-a91c4e`) with no colons — a Phase 2 format choice that happens to be filename-safe, noted so nobody "improves" it into ISO-8601 with separators. No designed path contains any illegal character. |
| **Trailing dots and spaces** | Forbidden in all designed names; all are ASCII `[A-Za-z0-9._-]`. Legacy filenames with spaces and one non-ASCII character survive the migration under quarantine, quoted in every command (§Z.4). |
| **Deep nesting** | Maximum designed depth is 5 below `store/` (`campaigns/<CMP>/creatives/<CRE>/v3.json`). The flat, scope-keyed layout of §F.2 is what keeps it there — a `brands/<b>/products/<p>/campaigns/<c>/…` hierarchy would have added ~45 characters and two levels to every path for information the identifiers already carry. |
| **Antivirus / sync interference** | Advisory: exclude `var/` and `media/` from real-time scanning and from OneDrive-style sync. Both hold large, frequently rewritten files, and a sync client that rewrites a file underneath a running index build is a corruption source. |
| **Execution shell for the §Z command blocks — corrected per §AI.7 Fix 24** | **Bash / Git Bash, not PowerShell, and not assumed to be a generic POSIX `sh` either.** §Z.3's manifest-building code uses Bash arrays, Bash's `${!SRC[@]}` index expansion, and `$'\t'` ANSI-C quoting — none of it valid PowerShell, and none of it guaranteed under a minimal POSIX `sh`. On this Windows machine, Git Bash (already installed alongside `git`) is the intended and verified environment (§B.4 finding 6). Pasting a §Z block into a PowerShell prompt will not run it correctly. |

### AC.2 Portability between computers

| Requirement | How it is met |
|---|---|
| No absolute paths in canonical records | RP10. `ASSET.path` is media-root-relative; `source_files[]` is repo-relative; every artefact reference is a logical address (Phase 2 §E.5). No drive letter, no `C:\Users\…`, anywhere. |
| `clone` / `pull` / `push` work | Everything canonical is tracked text, and — through Phase 3B — so are the 15 media samples (§O.3). Total tracked size after migration ≈ 700 KB of canonical text, plus 9 MB of books, plus ≈ 132 MB of temporarily-tracked media. History carries 136 MB of media blobs regardless — one-time clone cost, no file over 100 MB, no GitHub limit engaged. |
| Byte-identical config hashes across machines | **`.gitattributes` with `eol=lf`.** Without it a second Windows clone under `core.autocrlf=true` produces CRLF and different hashes for byte-identical policy (§AD R2). This is the single most important line in the migration. |
| Machine-specific configuration stays local | `.env` (ignored), `.claude/settings.local.json` (ignored), `MEDIA_ROOT` (environment). |
| Media | **Through Phase 3B, there is no gap**: the 15 current samples are tracked, so a plain `clone` reproduces them exactly, on any computer (§AI Correction 7). **The known future gap** (§O.5) applies only from the Media Cutover onward, for payloads registered after that point: a clone will bring the complete canonical store and zero of those payloads. `media check` will report what is missing; the operator copies out of band. |
| SQLite | Never transferred. Rebuilt on each machine from the canonical store (Phase 2 §AA). A missing index is not an error. |

**Operational update: `origin` now exists and `master` tracks `origin/master`.** GitHub setup was not solved by this design and was never required by it; the push has since happened as an ordinary operator action, independent of this document. Nothing in Phase 3B depends on `origin` — it remains usable from a bare local clone with no remote configured — but synchronisation steps for the freeze tags now assume it (§Z.1, step B; §AI.7).

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
| **R1** | **Media payloads will eventually be the only unbacked data in the system — once the Media Cutover happens.** | **HIGH, but not yet engaged** | **Revised per §AI Correction 7: the cutover itself is the mitigation, and it is deliberately not yet scheduled.** Through Phase 3B the 15 samples stay tracked (§O.3), so today's actual risk is unchanged from the status quo. `content_sha256` on every record makes future loss *detectable* regardless; `media check` reports missing and corrupt payloads once registration exists. | **Deferred, not accepted.** The risk becomes live only when a durable payload strategy is chosen and the cutover is separately approved — approval item 2, revised. |
| **R2** | **Line-ending drift invalidates config hashes across machines.** Authored YAML is hashed over file bytes; a CRLF checkout changes every hash. | **HIGH → LOW** | `.gitattributes` with `eol=lf`, `core.autocrlf=false`, applied as the first migration commit, with a **committed-blob** frozen-document integrity check either side of it — four documents, not three (§Z.2, twice-revised: §AI Correction 2, then §AI.7 Correction 15); validation checks 2 and 10. | Low. An editor that writes CRLF against `.gitattributes` is caught on the next `git status`. |
| **R3** | **A placeholder registry reads as authored policy.** An empty `deny_list.yaml` blocks nothing. | **HIGH → LOW** | `status: PLACEHOLDER_NOT_AUTHORISED`; a run refuses to start against any placeholder it pins (§J.3). | Low. Fail-closed by construction. |
| **R4** | **The allocator reads a stale SQLite index instead of canonical files**, double-allocating an ordinal. | **MEDIUM** | §F.4 rule 2, stated as a repository-layer invariant for Phase 5; INV-118 makes reuse a violation; `rebuild --verify` surfaces the divergence. Applies identically to the `EXT` cross-ledger scan of §F.4 (§AI Correction 5) and to the random-ID retry contract of §F.5 (§AI Correction 10) — validation checks 20–21. | Medium until Phase 5 code review enforces it. |
| **R5** | **A renderer upgrade is mistaken for a canonical-data change**, or vice versa. | **MEDIUM → LOW, and the mechanism changed** | **Revised per §AI Correction 6.** No longer solved by requiring the renderer to be pure and hoping that's enough — `reviews/` is now outside the source manifest entirely, so a renderer upgrade cannot move `store/`'s manifest hash regardless of purity. Purity is retained as an ordinary reproducibility property, checked by regeneration and byte-comparison, not by manifest staleness. | Low. |
| **R6** | **`media/_unregistered/` becomes permanent.** Files sit unregistered for months and the staging area becomes a second media convention. | **MEDIUM** | It is empty once Phase 5's registration runs; `media check` reports its contents as `MEDIA_ORPHAN`. | Medium — a scheduling risk, not a design one. |
| **R7** | **136 MB of history on clone — already realised, since `origin` now exists and the repository has been pushed.** | **LOW** | No file exceeds GitHub limits; `git gc` compacts loose objects; the cost is one-time per clone. **Revised: `origin` exists and `master` tracks `origin/master` — "before the first push" is no longer a valid window for any future decision, including a purge (§AI.7).** Because the 15 samples stay tracked through Phase 3B rather than being untracked, this risk's size is unchanged by this migration — it was already the cost of the existing history, not a cost this design adds (§AI Correction 7). | Low. Accepted rather than fixed, because the fix now requires a coordinated remote history rewrite and re-clone, not merely a local one (REPO_ADR-017, revised). |
| **R8** | **Long brand or product slugs push paths toward `MAX_PATH`.** | **LOW** | Slug caps in X.4 (recalculated to 24/32 per §AI Correction 12's re-evaluation); path budget in AC.1. | Low. |
| **R9** | **Quarantine bypass** — a file lands in `_quarantine/` without valid provenance. | **MEDIUM → LOW, and lower again after this pass** | Two-layer enforcement: metadata is authoritative and now fails closed for **both** carriers (§M.1.1, §AI.7 Fix 23 — a missing or invalid Markdown front-matter block is `NOT_RETRIEVABLE`, no longer an implicit default to permitted, exactly matching the sidecar rule); the path check remains a second, independent line of defence regardless of what the metadata layer decides (§N.3). | Low. The corrected default removes the specific gap this risk originally named — a missing-front-matter Markdown file no longer defaults to permitted even before the path check runs. |
| **R10** | **A manual repair of a canonical file passes unnoticed.** | **LOW** | The store is git-tracked, so every edit is a diff; `rebuild --verify` catches folded-state divergence; check 14 catches path/content identity mismatch. | Low. Phase 2 §AA.2 already makes this the sharpest integrity signal in the system. |
| **R11** | **A random-allocated identifier collides** — small but nonzero, especially for `CAMPAIGN_ID`'s 6-hex suffix. | **LOW** | **New, per §AI Correction 10.** The write contract is generate-and-retry under create-exclusive semantics (§F.5, RP13); a collision is an ordinary `EEXIST` branch, never assumed away. Validation check 21. | Low. The frozen identifier format is not reopened; only the write contract around it changes. |

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
| A top-level `schemas/` root | Generated output belongs in `var/` (§T). |
| A top-level `prompts/` root | Prompt templates are runtime inputs shipped with the code (§R). |
| `store/registry/` for style profiles | `config/styles/` is closer to the authoring workflow and does not disturb the nine-file rule (§J.4). |
| `media/{videos,audio,images,generated}/` | Type, role and state are record fields and index columns. A path-based classification can disagree with the record and would require moving files when state changes. |
| Sharding `observations/` and `claims/` | ~61 and ~22 per campaign (Phase 2 §AD.7). Sharding solves a problem V1 does not have, and any later change is a recorded migration. |
| Empty `src/`, `tests/`, `tests/golden/<category>/`, `.claude/skills/` | RP11. A directory is created by the phase that fills it. |
| `sources/methodology/` | Empty, and its intended contents belong in quarantine (§B.4 finding 1). |

**Eleven boundaries removed** — revised down from the first pass's twelve. *(A top-level `reviews/` root was listed here as removed in the first pass. The external audit's Correction 6 reinstated it: keeping renders inside `store/`'s manifest, even behind a purity requirement, let a renderer upgrade masquerade as a canonical-data change. `reviews/` now appears in §AE.2 instead, as a boundary that earns its keep rather than one this pass cut.)* Three of the eleven (`knowledge/narrative/`, `knowledge/language/cl/`, `sources/external/`) came from Phase 1 and were absorbed by Phase 2's later, frozen model — found by reading the two documents against each other rather than by taste.

### AE.2 Kept despite pressure to cut

| Kept | Why it survives |
|---|---|
| `sources/` (2 files) | The raw/derived boundary is frozen Phase 1 architecture, and a resolvable `source_files[]` path is what makes the `DERIVED_VERIFIABLE` tier checkable rather than asserted. |
| `reviews/` — **added in this pass, not removed by it** | Reinstated as a top-level root, not kept inside `store/` (§AI Correction 6). It earns the boundary RP5 sets: tracked (unlike `var/`), never authoritative (unlike `store/`), mechanically reproducible from something that is (unlike `docs/`) — a third combination of properties that no existing root already covers, and the specific failure it prevents (a renderer upgrade moving `store/`'s manifest hash) is worth one directory. |
| `incoming/` (empty) | It is a provenance declaration, not a convenience. Collapsing it into `media/_unregistered/` would give the fifteen samples the wrong `origin.kind` and contradict Phase 2 §S.4 (§P.2). |
| `media/_unregistered/` | The gap between "moved in Phase 3B" and "registered in Phase 5" is real and has to live somewhere legible — and, through Phase 3B, it holds tracked files rather than ignored ones (§O.3, §AI Correction 7), which does not change why the directory itself is needed. |
| `config/styles/` | Style profiles are authored YAML that is not one of the nine; giving them a subdirectory is what keeps the nine-file rule literal. |
| `var/` as a single root with six children, ignored via its own local rule | Six children of one root cost nothing — they are never navigated, only written to — and merging them would put the SQLite index in the same directory as temp downloads. The ignore rule living at `var/.gitignore` rather than the root file (§AI Correction 4) does not add a boundary, only relocates one that already existed. |
| The `ledger/` level inside a product | Phase 2 §J calls the Evidence Ledger *one store*; four sibling directories at the product root would lose that grouping and mix ledger records with artefacts. |

---

## Contradiction Scan

Run mechanically against the eleven checks the brief specifies.

| # | Check | Result |
|---|---|---|
| 1 | **No canonical object has two authoritative paths** | **Clean.** Narrative patterns: `config/narrative_library.yaml` only (`knowledge/narrative/` not created). Customer language: ledger observations only (`knowledge/language/cl/` not created). Source snapshots: `media/` as assets only (`sources/external/` not created). Style profiles: `config/styles/` only. Each artefact version: one `v<n>.json`, created exclusively. Renders are derived and marked. |
| 2 | **Raw source and structured knowledge are separated** | **Clean.** `sources/` holds two original books, tracked and never edited. `knowledge/` holds derived, provenance-tagged material. The three methodology PDFs go to `knowledge/_quarantine/` and *not* to `sources/`, because §B.4 establishes only that no authoritative upstream for them is present or resolvable in the repository — a claim about this repository's contents, not a claim that no original exists anywhere (§AI Correction 11). |
| 3 | **Binary payload and Asset Registry metadata are separated** | **Clean, and unaffected by the media-tracking deferral.** Record: `store/assets/<2hex>/AST-….json`, canonical, tracked. Payload: `media/<2hex>/AST-….<ext>`, target: ignored, referenced by media-root-relative `path` plus `content_sha256`. Whether the payload is *also* tracked in git through Phase 3B (§O.3) is a separate fact from whether it is *canonical* — it is not, either way; only the Asset Registry record is. |
| 4 | **No ignored path contains unique canonical truth** | **Clean, and the exception this check used to name no longer applies during Phase 3B.** `media/**`'s target state is ignored, and once the future Media Cutover happens it will hold payloads that exist nowhere else — that remains an approved, named exception (R1, approval item 2), but it is **not yet in effect**: through Phase 3B the 15 samples are tracked (§AI Correction 7), so there is currently no ignored path holding unique canonical truth at all. No canonical **record**, artefact, event log or config file is in an ignored path (validation check 7), now or after the cutover. |
| 5 | **SQLite remains fully rebuildable** | **Clean.** `var/index/`, git-ignored via `var/.gitignore` (§Q, corrected — not the root file), never committed. Every input it folds — records, event logs, gate decisions, config — is tracked under `store/` and `config/`. A missing database is not an error (Phase 2 §AA.2). |
| 6 | **Event log paths match their frozen scopes** | **Clean.** `evidence` per product, `campaign` per campaign, `run` per run, `asset` global — each `events.jsonl` sits at the root of the directory that *is* its scope (§I.1). |
| 7 | **Entity identifier allocation does not depend on event-log layout** | **Clean, and tabulated in §F.4–F.5.** Every ordinal reads canonical records — filenames for `OBS`/`CLM`/`GAT`/`CRE`, file contents across *all* versions for `INS`/`HYP`/`CON`/`EXP`, and — corrected — `EXT` reads across **every** product ledger for the run's suffix, never one (§AI Correction 5). No entry reads a `.jsonl`. `event_seq` is a line number and numbers only events. Random-allocated identifiers retry on collision at the write boundary rather than assuming one away (§F.5, §AI Correction 10). |
| 8 | **All nine config registries have exactly one authoritative location** | **Clean.** `config/<name>.yaml`, one file each, enforced by `ls config/*.yaml \| wc -l == 9` plus a name whitelist (validation check 18). `config/styles/` is a subdirectory and does not disturb the glob. |
| 9 | **Relative-path design works on another computer** | **Clean for records; the payload gap is real but no longer confused with Phase 3B.** No absolute path in any canonical record. `.gitattributes` guarantees byte-identical config hashes. **Through Phase 3B, the 15 tracked samples introduce no gap** — a plain clone reproduces them. The known future gap applies only to payloads registered after the Media Cutover (§O.5, §AI Correction 7), stated there and in R1, not concealed. |
| 10 | **No existing source is moved in Phase 3A** | **Clean.** Zero files moved, renamed, deleted or edited. `git status` was clean at the start of this phase and is clean at its end, except for this document. Every move in §Y is designed and unexecuted. |
| 11 | **No Phase 4 Skill has been implemented** | **Clean.** No `.claude/` directory created, no `SKILL.md` written, no skill directory scaffolded. §R decides a boundary and names five directories that Phase 4 will create. **Additionally clean per this pass:** Phase 4 is now explicitly gated on Phase 3C's completion, not merely on Phase 3B's (§AH, §AI Correction 8). |

**Two checks carried forward from the first pass, run because Phase 2 §AJ.8.8 recommends re-running the scan rather than trusting a fix:**

| # | Check | Result |
|---|---|---|
| 12 | Does any Phase 3 decision alter a Phase 2 content hash? | **No.** JSONL line serialisation (§I.2 rule 3) governs event lines, which carry no `content_hash` and are addressed by `(log, event_seq)`. Artefact serialisation (§G.7) is untouched. Config hashing is *specified* where Phase 2 was silent, and `.gitattributes` makes the bytes it hashes stable rather than changing which bytes they are. `reviews/`'s move outside the source manifest (§AI Correction 6) touches no Phase 2 hash either — renders never had a `content_hash` field to begin with (Phase 2 §E.6). |
| 13 | Does any Phase 3 decision reopen a frozen ADR? | **No.** Phase 1 ADR-004 (git-tracked JSON as system of record), ADR-009 (quarantine), ADR-012 (three style profiles), ADR-013/014 (voices), ADR-035 (asset states) and Phase 2 DATA_ADR-026/032/033 are all *implemented* by this layout, none reopened. The three Phase 1 §I directories not created are Phase 1 *proposals* superseded by Phase 2's frozen model, not ADRs. |

**Twelve further checks, run against the external audit's own closing cross-check (§AI) — the mechanical test for whether each of the twelve corrections actually landed, not merely whether it was discussed:**

| # | Check | Result |
|---|---|---|
| 14 | Any Phase 3B command that assumes `HEAD` is still `59cbe49` | **None.** §Z.1 branches from `phase-3a-freeze` (`<PHASE_3A_FREEZE_SHA>`); `59cbe49` is referenced only as the older, separately-tagged `phase-2-freeze` checkpoint (§AI Correction 1). |
| 15 | Any all-files hash-set comparison across normalisation or scaffolding | **None.** §Z.2 checks the three frozen documents individually, by name, before and after normalisation. §Z.3–Z.4 check each moved file individually against a targeted baseline. §Z.5's new files are validated by presence and structure, never against a pre-image (§AI Correction 2). |
| 16 | Any rollback command inconsistent with the merge strategy | **None.** §Z.6 merges with `--no-ff`; §AA.2's post-merge rollback is `git revert -m 1 <merge-sha>`, addressed at the one merge commit that strategy produces (§AI Correction 3). |
| 17 | Any ignored parent whose own `README`/`.gitignore` must be tracked | **None.** The root `.gitignore` no longer lists `var/`; `var/.gitignore` (tracked) owns `var/`'s contents locally, matching `media/` and `incoming/`'s existing pattern (§AI Correction 4). |
| 18 | Any `EXT` allocator that checks only one product ledger | **None.** §F.4 requires the glob across every product ledger for the run suffix, with `run_id` validated per match (§AI Correction 5); validation check 20. |
| 19 | Any derived review under the canonical manifest | **None.** `reviews/` is a sibling of `store/`, not a subdirectory, and is explicitly outside the `store`/`config` manifest walk (§Q.3, §AI Correction 6). |
| 20 | Any Phase 3B command untracking the current 15 samples | **None.** The `git rm -r --cached media` step is removed from §Z entirely; §Y.1 row 7 records its removal explicitly rather than silently dropping it (§AI Correction 7). |
| 21 | Any Phase 4 dependency on front matter before Phase 3C | **None.** §AH states the precondition explicitly and orders the phases; §Y.4 states the same order from the migration side (§AI Correction 8). |
| 22 | Any claim that all no-`ASSET_ID` files belong in `var/` | **None.** RP6 now names three destinations for a file without a registered `ASSET_ID` — `incoming/`, `media/_unregistered/`, or `var/` — distinguished by registration path, not merely by the id's absence (§AI Correction 9). |
| 23 | Any random-ID allocator with no collision/retry behaviour | **None.** §F.5 specifies generate-candidate/create-exclusive/retry-on-`EEXIST` for `CAMPAIGN_ID`, `RUN_ID` and `ASSET_ID`; validation check 21 (§AI Correction 10). |
| 24 | Any statement that Google Docs export metadata proves no upstream original exists | **None remaining.** Every instance (§B.4 finding 1, §K/§N, REPO_ADR-013, this scan's own check 2) now states only that no authoritative upstream is present or resolvable *in the repository*, and that the corpus's provenance cannot be verified from what the repository holds (§AI Correction 11). |
| 25 | Any operator `README.md` treated as a `KNOWLEDGE_ID` entity | **None.** §M.2 draws the boundary explicitly — a `README.md` under `knowledge/` is excluded from retrieval by filename, carries no provenance front matter, and is never asked to declare its own exclusion (§AI Correction 12); the §W matrix and §N.3 both name `knowledge/_quarantine/README.md` as the concrete instance. |

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
| **REPO_ADR-006** | Where a scope-ordinal reads its `max` | **Canonical files only, per the §F.4 table; never SQLite; across *all* artefact versions; and for `EXT` specifically, across *every* product ledger for the run suffix, never one** | The index may be stale or absent (§AA.2); INV-118 forbids reuse, so the union across versions is required. `EXT`'s storage scope (product) differs from its allocation scope (run), and a run may touch more than one product, so no single ledger is authoritative for a run's extractions (§AI Correction 5) | Allocation reads several files instead of one query; the `EXT` case reads across every product ledger, not just one | PROPOSED, revised |
| **REPO_ADR-007** | Location of the nine config registries | **`config/<name>.yaml`, exactly nine `*.yaml` at that level** | Matches Phase 2's `config/evidence_policy@v4` reference form 1:1; turns INV-115 into `ls \| wc -l` | Non-registry files must avoid the `.yaml` extension at that level | PROPOSED |
| **REPO_ADR-008** | How config versions and hashes are pinned | **`version:` header in the file; `sha256` over raw file bytes; history lookup by hash** | Answers Phase 2 §AI.1 item 6 without adding a field to the frozen RUN head; a forgotten bump is detectable | Recovering an old version is a history search, not a path | PROPOSED |
| **REPO_ADR-009** | Behaviour of an unauthored registry | **`status: PLACEHOLDER_NOT_AUTHORISED`; a run refuses to start against it** | An empty `deny_list.yaml` blocks nothing — silent and permissive is the worst failure mode available | The operator must author nine files before the first run | PROPOSED |
| **REPO_ADR-010** | Where Style Profiles live | **`config/styles/STY-….yaml`, pinned per artefact via `inputs[]`** | Authored YAML, close to policy, in a subdirectory so the nine-file rule is literal; not a tenth run-level dependency, so INV-115 is not engaged | Looks adjacent to the nine and needs the distinction stated | PROPOSED |
| **REPO_ADR-011** | Knowledge provenance mechanism | **YAML front matter for Markdown entities; a `.meta.yaml` sidecar for binary (PDF) entities that cannot carry in-file front matter; no central authored registry for either; a missing or invalid record on either carrier is fail-closed `NOT_RETRIEVABLE`** | Provenance must travel with content into the prompt (P9); losing it should require editing the file (or its sidecar) that carries the content. **Revised (§AI Correction 18): a PDF cannot hold a YAML block without corrupting the format, so a sidecar is not a rejected duplication here — it is the only place a binary entity's provenance can live. Revised again (§AI.7 Fix 23): the fail-closed default is now stated identically for both carriers, not only for the sidecar** | A corpus-wide query needs a derived index; the 3 PDF entities are retrieved as a `(payload, sidecar)` pair rather than a single file | PROPOSED, twice-revised |
| **REPO_ADR-012** | Section-granularity provenance | **An optional `sections:` key in the same front matter — for Markdown entities only; not applicable to a PDF sidecar, which describes the whole payload** | Phase 1 §I found modules mixing cited material with unsourced speculation; one file, one source of truth | Authoring cost per file (Phase 3C); the 3 quarantined PDFs get whole-payload provenance only, since PDF text is not section-addressable by this mechanism | PROPOSED, revised |
| **REPO_ADR-013** | Quarantine destination, and whether PDFs separate | **`knowledge/_quarantine/methodology/` — PDFs and Markdown together** | The three PDFs' export metadata, combined with the corpus's unresolvable citations, establishes that no authoritative upstream is present or resolvable in the repository for either format (§B.4) — not that no original exists anywhere (§AI Correction 11). One directory, one retrieval policy, path-enforceable | The word "PDF" no longer implies "source" in this repository | PROPOSED |
| **REPO_ADR-014** | `knowledge/narrative/` and `knowledge/language/cl/` | **Not created — superseded by Phase 2** | Narrative patterns are a config registry; customer language is ledger observations. Either directory would be a second authoritative home | Phase 1 §I's tree is not reproduced literally | PROPOSED |
| **REPO_ADR-015** | `sources/external/` | **Not created — snapshots are assets** | Phase 2 §S: `asset_type: SOURCE_SNAPSHOT`, referenced by `SOURCE.snapshot_asset_id` | Same | PROPOSED |
| **REPO_ADR-016** | Media addressing, and when payloads become ignored | **`media/<2hex>/AST-<12hex>.<ext>` — id-addressed, sharded; ignored **only from a future Media Cutover onward**, once a durable payload strategy exists. Through Phase 3B, the 15 current samples remain tracked** | Two records may share bytes and differ in rights (§E.4); content-addressing would merge them. Rights attach to provenance, not to bytes. **Revised (§AI Correction 7): untracking the only copies of the current samples before any durable strategy exists would make cross-machine portability worse than today** — the target architecture is unchanged, only its activation is deferred | Duplicate bytes when one file is registered twice; the repository carries ≈132 MB of tracked media until the cutover | PROPOSED, revised |
| **REPO_ADR-017** | The 136 MB of media already in history, and the timing of any untrack or purge | **Retained in history regardless. No history rewrite. Untracking the 15 current samples is deferred to a separate, later, explicitly-approved Media Cutover — not part of Phase 3B** | The frozen freeze commits are the rollback targets, and the media blobs are what make physical restoration possible (§AA.1–AA.2). A purge destroys the safety net to save disk. **Revised (§AI Correction 7):** the untrack timing is now a distinct decision from the no-purge decision. **Revised again (§AI.7, operational):** `origin` now exists and the repository has been pushed, so a purge is no longer a same-machine `git filter-repo` operation — it would require a separately-authorised coordinated remote history rewrite and re-clone across every machine tracking `origin`. The recommendation (no purge) is unchanged; the cost of reversing it has gone up | Every clone carries 136 MB regardless of the untrack decision; the tracked-but-not-cut-over state persists until the cutover is separately approved; a future purge decision now carries multi-machine coordination cost | **PROPOSED, revised — needs user approval (§AG decisions 2 and 3)** |
| **REPO_ADR-018** | Ingestion entry points | **Two: `incoming/` ⇒ `USER_UPLOAD`; `media/_unregistered/` ⇒ `REPOSITORY`** | `origin.kind` is the sole determinant of an asset's initial state (§S.2), and the fifteen samples must fold to `REFERENCE` (§S.4). One entry point would produce the wrong rights position | A second directory, and one of the two path-carries-policy exceptions | PROPOSED |
| **REPO_ADR-019** | Derived Markdown renders | **A new top-level `reviews/` root, sibling to `store/`, mirroring its scope structure but excluded entirely from the source manifest** | Phase 2 §G.7 requires them tracked. **Revised (§AI Correction 6): the first pass kept them inside `store/`'s manifest and relied on renderer purity to prevent false staleness — but a renderer *upgrade* legitimately changes every render's bytes while changing no canonical fact, and under the first pass that upgrade would still mark the index stale.** Moving renders outside the manifest removes the false alarm structurally rather than relying on purity to prevent it | One additional top-level directory (9 → the design still counts it as earning a boundary, per RP5) | PROPOSED, revised |
| **REPO_ADR-020** | Derived / runtime root, and where its ignore rule lives | **`var/`, fully git-ignored **via `var/.gitignore`, a locally-owned rule, not a root `.gitignore` entry**; SQLite at `var/index/`** | Deleting it must cost only time. A committed index could be mistaken for truth. **Revised (§AI Correction 4): a bare `var/` line in the root ignore file pre-empts tracking `var/.gitignore` and `var/README.md` themselves, which this design requires to be tracked.** Locality matches the pattern `media/` and `incoming/` already used | Six ignored subdirectories, never navigated; the root `.gitignore` now carries only genuinely repository-wide rules | PROPOSED, revised |
| **REPO_ADR-021** | Generated JSON Schema | **`var/schemas/`, not tracked** | Tracking creates drift that needs a CI job to police; not tracking makes drift impossible. The schema is a pure function of a tracked commit | Reviewers see model diffs, not schema diffs | PROPOSED |
| **REPO_ADR-022** | Code root | **`src/creative_os/`, created in Phase 5** | src-layout forces an installed package so imports match production; `creative_os` is a valid identifier | One extra level | PROPOSED |
| **REPO_ADR-023** | Claude / Skill boundary | **`.claude/skills/` for the five Skills; runtime prompts under `src/creative_os/prompts/`; knowledge stays in `knowledge/`** | Skills are procedure, prompts are pinned runtime inputs, knowledge is retrieved content. Phase 1 §D.1 separates development environment from runtime | Skills sit in a tool-named directory | PROPOSED |
| **REPO_ADR-024** | Line endings, and how the frozen documents are protected around the renormalisation commit | **`.gitattributes` with `eol=lf`; `core.autocrlf=false`; renormalise once; verify all four frozen documents' *committed blobs* — not working-tree bytes — are byte-identical immediately before and after** | Phase 2 §G.7 hashes authored YAML over file bytes; without this, a second Windows clone produces different hashes for identical policy. **Revised (§AI.7 Correction 15): a working-tree sha256 comparison proves nothing about what `git add --renormalize` actually commits** — the check must read `git show <commit>:<path>`, and it now protects `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` itself alongside the three pre-existing frozen documents | One normalisation commit touching every text file; four committed-blob comparisons instead of three working-tree ones | **PROPOSED — highest priority, revised** |
| **REPO_ADR-025** | Phase documents and `PRE_FLIGHT_AUDIT.md` | **Do not move** | Phase 2 §AI.1 item 7; cited by path across three documents; moving changes no content and breaks every reference | `docs/` mixes historical and current documents | **ACCEPTED (inherited from Phase 2)** |
| **REPO_ADR-026** | Scope of Phase 3B, and Phase 3C's relationship to Phase 4 | **Moves and scaffolding only. Knowledge front matter (M3) and section tagging (M5) become Phase 3C. Phase 3C is a mandatory precondition for Phase 4, not an optional follow-on** | Keeps 3B's central validation total — *every moved file's hash is unchanged* — and keeps rollback free of content edits. **Revised (§AI Correction 8): Phase 4 Skill design assumes retrieval hits carry `knowledge_id`, `tier` and `retrieval_policy`; those fields do not exist before Phase 3C authors them**, so the phase order is now fixed rather than merely sequential-by-convention | Knowledge files remain untagged until 3C is authorised; Phase 4 cannot begin planning against real metadata until 3C is frozen | **PROPOSED, revised — needs user approval** |
| **REPO_ADR-027** | Recording structural change | **`docs/MIGRATIONS.md`, append-only** | §AA hashes relative paths, so a pure move changes the manifest hash; the log makes that attributable rather than alarming | One file to maintain, forever | PROPOSED |
| **REPO_ADR-028** | Secrets | **`.env.example` tracked (names only); `.env` ignored; credential *identity* recorded, credential never** | Phase 1 §D.1 / ADR-033. Recording who acted is required; recording what proves it is forbidden | Per-machine setup step | PROPOSED |
| **REPO_ADR-029** | Collision handling for random-allocated identifiers | **Generate-candidate / create-exclusive / retry-on-`EEXIST`, for `CAMPAIGN_ID`, `RUN_ID` and `ASSET_ID`** | **New (§AI Correction 10).** "Cannot collide in practice" is a probability statement, not a write contract; `CAMPAIGN_ID`'s 6-hex suffix makes the residual probability small but not zero. The mechanism costs nothing beyond what RP9 already requires for artefact versions | None of substance — this is the same create-exclusive discipline already in use, applied to one more identifier class | PROPOSED |
| **REPO_ADR-030** | Pre-registration file placement, refining RP6 | **Three destinations for a file with no `ASSET_ID`, distinguished by registration path: operator-supplied → `incoming/`; repository-origin → `media/_unregistered/`; neither, and not headed toward registration → `var/`** | **New (§AI Correction 9).** The first pass's RP6 ("has an id → `media/`, else → `var/`") did not account for `incoming/` and `media/_unregistered/`, both of which intentionally hold pre-registration files that will never belong in `var/` | Three destinations to remember instead of two, but each maps to a distinct provenance declaration that already exists for other reasons (§P.2) | PROPOSED, revised (supersedes the first pass's RP6 statement) |
| **REPO_ADR-031** | Final slug-length caps | **Brand ≤ 24 characters, product ≤ 32** | **New (§AI Correction 12).** The first pass proposed 16/24 without showing why a looser cap would be unsafe. Recalculated against the binding path (a ledger record under `store/products/…/ledger/observations/…`) at 24/32: 143 characters, leaving 74 characters of headroom on this machine and 17 against a pessimistic root — both comfortably positive | Slightly longer worst-case paths than the first pass's caps, still well inside the Windows budget | PROPOSED |
| **REPO_ADR-032** | Knowledge-directory operator documentation | **A `README.md` under `knowledge/**` is not a `KNOWLEDGE_ID` entity: no provenance front matter, excluded from retrieval by filename, never by its own declaration** | **New (§AI Correction 12).** Requiring provenance metadata on a file that has no derivation, no source and no claims is a category error; excluding it structurally (by filename) rather than by asking it to self-declare matches the same fail-closed posture already used for the quarantine path check (§N.3) | The retrieval layer's exclusion list gains one more rule (filename `README.md`), alongside the `_quarantine/` path rule | PROPOSED |
| **REPO_ADR-033** | Provenance mechanism for a binary (PDF) knowledge entity | **A `<payload-filename>.meta.yaml` sidecar, carrying `payload_path` + `payload_sha256` plus every field the front-matter schema requires; the (payload, sidecar) pair is retrieved as one logical `KNOWLEDGE_ID` entity; a PDF with no valid sidecar is fail-closed `NOT_RETRIEVABLE`** | **New (§AI.7 Correction 18).** A PDF cannot carry in-file YAML front matter without corrupting its own format, and this design never edits a quarantined payload's bytes. The sidecar is not the "adjacent metadata file" option rejected for Markdown (§M.1) — it exists only for the 3 entities structurally unable to carry their own provenance, so the one-record-per-entity principle is preserved, not violated | Exactly one more file per binary entity (3 currently); the retrieval layer must validate a path+hash link rather than merely reading one file | PROPOSED |
| **REPO_ADR-034** | Whether a missing Markdown front-matter block defaults to retrievable or excluded | **`NOT_RETRIEVABLE` — identical to the already-decided PDF default. No knowledge entity is retrievable without a valid provenance record, regardless of which carrier its format requires** | **New (§AI.7 Fix 23).** The first pass stated a fail-closed default for the sidecar carrier (REPO_ADR-033) but left the front-matter carrier's failure mode unstated, which a retrieval layer must resolve somehow — and an unstated default resolves to permitted, the one outcome this design exists to prevent for exactly this kind of material (Phase 1 F2, F3) | None of substance — this is the same posture REPO_ADR-033 already adopted, made symmetric rather than newly invented | PROPOSED |

**34 repository ADRs — 28 from the first correction pass (6 revised there: 006, 016, 017, 019, 020, 026) plus 4 new there (029–032); the second (final-executability) pass added 1 new (033) and revised 3 (011, 012, 024); the third (final micro-fix) pass added 1 more new (034) and revised 011 and 012 again for the universal fail-closed rule. No Phase 1 or Phase 2 ADR reopened.**

---

## AG. Decisions Requiring User Approval

**Six, down from seven** — the external audit resolved the slug-cap question outright rather than leaving it open (§AI, this section's closing note), and revised the media decision's content without changing its count. Each remaining item is a genuine choice with a real cost, not a request to confirm something already settled.

| # | Decision | Recommendation | What you are accepting |
|---|---|---|---|
| **1** | **Canonical data root named `store/`** (REPO_ADR-001) | `store/` | Every canonical path begins `store/`. Changing it later is a one-command rename plus one migration-log entry, but it moves every path in the manifest. Cheapest to settle now. External audit: recommends approval. |
| **2** | **The 15 current media samples stay git-tracked through Phase 3B; untracking is deferred to a separate, later Media Cutover** (REPO_ADR-016/017, revised — §AI Correction 7) | Accept the deferral | **Revised from the first pass**, which asked you to accept ignoring media immediately. The audit found that untracking the only copies of these files before any durable payload strategy (Git LFS, external drive, object storage, or another) exists would make your cross-machine portability *worse* than a plain `git clone` gives you today. Accepting this decision commits to: media stays tracked and fully portable through 3B; a **separate future request** is required to choose a durable strategy and execute the cutover, and that request carries its own approval and its own rollback design (§AA.4). |
| **3** | **Do not purge the 136 MB of media from git history** (REPO_ADR-017) | Do not purge | Every clone carries 136 MB. The alternative rewrites history, invalidates the frozen freeze commits, and destroys the mechanism that makes physical rollback possible (§AA.1–AA.2). **`origin` now exists and the repository has already been pushed — the "before the first push" window this item originally offered no longer exists.** A purge is still possible, but it now requires a separately-authorised coordinated remote history rewrite (e.g. `git filter-repo` + force-push) and a re-clone on every other machine tracking `origin`, not merely a local operation. External audit: recommends no purge, for now. |
| **4** | **Split physical migration (Phase 3B) from knowledge-provenance authoring (Phase 3C), and treat Phase 3C as a mandatory precondition for Phase 4 — not an optional follow-on** (REPO_ADR-026, revised — §AI Correction 8) | Split, with the sequencing now fixed | Phase 3B stays a pure, fully hash-verifiable move; no file's content changes except `README.md`. Knowledge files carry no provenance front matter until 3C is authorised and run — so the quarantine is enforced by path alone in the interim (§N.3), one layer rather than two. **New in this revision:** Phase 4 may not start until Phase 3C is frozen, because Skill design assumes retrieval hits already carry `knowledge_id`, `tier` and `retrieval_policy`, and those fields do not exist before Phase 3C authors them. |
| **5** | **`.gitattributes` + `core.autocrlf=false` + one renormalisation commit, with an explicit frozen-document hash check either side of it** (REPO_ADR-024) | Do it, first | One commit touches the working-tree bytes of every tracked text file. Without it, config hashes differ between your two computers and the reproducibility contract silently fails. The added before/after check on `PRE_FLIGHT_AUDIT.md` and the two frozen phase documents (§Z.2) verifies rather than assumes that normalisation left them untouched. |
| **6** | **Reserve, do not scaffold: `src/`, `tests/`, `.claude/skills/`** (RP11) | Reserve | After Phase 3B the repository has nine top-level directories (`reviews/` is new — §AI Correction 6) and no empty promises. The names are decided; the directories arrive with their first file. |

**Resolved, no longer requiring your approval: slug caps.** The first pass proposed brand ≤ 16 / product ≤ 24 as an open question. The external audit asked for the arithmetic behind a looser alternative before accepting it, rather than a blind loosening — that arithmetic is now in §AC.1: the binding constraint is a ledger record path (`store/products/PRD-<brand>-<product>/ledger/observations/OBS-<product>-NNNN.json`), and at brand ≤ 24 / product ≤ 32 it reaches 143 characters, leaving 74 characters of headroom against this machine's repository root and 17 against a pessimistic one. Both are comfortably positive, so the looser values are adopted directly (X.4) rather than left open.

**No decision in this document depends on GitHub, Git LFS, cloud storage, an API credential or an installed runtime.** All six remaining items are answerable now.

---

## AH. Phase 4 Handoff Requirements

Phase 4 designs Skills. What it inherits and what it must respect:

**Phase 4 may not start until both Phase 3B and Phase 3C are frozen — corrected per the external audit's Correction 8.** The first pass treated Phase 3C (knowledge provenance authoring) as a follow-on that Phase 4 could proceed without. It cannot: §AH.1 below states that a retrieval hit carries `knowledge_id`, `tier` and `retrieval_policy` from its provenance record — front matter for a Markdown entity, a `.meta.yaml` sidecar for a PDF entity (§M.1.1, §M.3) — and neither carrier exists on any file until Phase 3C authors it: not the three Schwartz files, not the eight quarantined files (five Markdown, three PDF). A Phase 4 Skill designed against metadata that has not yet been written would be designed against a fiction. The mandatory order is therefore:

```
Phase 3A (this document, frozen) → Phase 3B (physical migration, frozen) → Phase 3C (provenance authoring, frozen) → Phase 4
```

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

Create no directory under `store/`, `config/`, `media/` or `var/`. Author no config registry content. Move no file. Write no Python. Register no asset. **Assume no knowledge provenance record — front matter or sidecar — that Phase 3C has not yet authored and frozen.** The repository migration (Phase 3B) and the knowledge provenance pass (Phase 3C) are each a separate authorisation and, at the time of writing, neither has been granted.

---

## AI. External Audit Correction Pass

**Date:** 2026-09-04 · **Trigger:** external repository-architecture audit · **Scope:** `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` only · **Phase 3B, 3C and 4 not started.**

Twelve corrections were raised. **All twelve are accepted.** Four (1, 2, 3, 7) identified genuine internal contradictions or sequencing errors — places where the document specified a mechanism that could not survive its own later consequences, or ordered an operation before its precondition existed. Three (4, 6, 9) identified design errors with concrete failure cases the first pass had not traced through. Two (5, 8) identified an unstated dependency between namespaces or between phases. One (10) identified an unproven safety claim. One (11) identified an overclaim not supported by the cited evidence. One (12) identified a category error in what the provenance requirement was made to cover.

### AI.1 The two that mattered most

**Correction 1 was the most structurally serious**, because it was a contradiction in the document's own precondition. Phase 3B's clean-tree check required `HEAD == 59cbe49` — the commit *before this design document existed*. But the document itself must be committed and approved before Phase 3B can reasonably begin, and that approval is a commit. The precondition was therefore false at the exact moment the document it gated became real. The fix — a second, later freeze tag (`phase-3a-freeze`) as the normal baseline, with `phase-2-freeze` demoted to an older historical checkpoint that remains reachable but is no longer what Phase 3B checks against — is the general shape every phase-gated document in this project should use from here on: **a design document that will itself be committed cannot name its own pre-commit state as its execution precondition.**

**Correction 7 was the most consequential for the user's actual situation.** The first pass correctly designed the *target* architecture (registered payloads git-ignored, detectable by hash) and then applied it to the *existing* fifteen files immediately, without checking whether doing so before any durable payload strategy existed would help or hurt. It would have hurt: untracking the only copies of those files, on a machine with no configured Git LFS, no synced backup and no object storage, would have made the user's stated intention — working from more than one computer — strictly harder to satisfy than a plain `git clone` already makes it today. The general lesson, worth carrying into every future migration this project designs: **a migration step can be correct as a target and wrong as a sequencing choice, and checking "does this step make today's actual working pattern worse" is a different question from "does this step match the target architecture," and both must be asked.**

### AI.2 Corrections and verdicts

| # | Correction | Verdict | Nature | Sections affected | REPO ADRs |
|---|---|---|---|---|---|
| 1 | Phase 3B must start from a Phase 3A freeze, not `59cbe49` directly | **Accepted** | **Contradiction** — the clean-tree precondition could not survive this document's own approval commit | §Z.1 (rewritten), §AA.1–AA.2, §AB checks 1, 3, 14, 15 | — (procedural; no ADR content changed) |
| 2 | Move-hash validation baseline was invalid across normalisation and scaffolding | **Accepted** | **Contradiction** — a whole-tree hash-set diff cannot survive bytes changing (normalisation) or the file count changing (scaffolding) | §Z.2, Z.3, Z.4, §Y.1, §AB checks 2–3, 15 | — |
| 3 | Rollback must match the merge strategy; pre-merge abort must restore the physical workspace | **Accepted** | **Contradiction** — `--ff-only` produces no merge commit for `git revert <sha>` to target | §Z.6, §AA (rewritten: AA.1–AA.5) | — |
| 4 | Root `var/` ignore rule pre-empted tracking `var/.gitignore`/`var/README.md` | **Accepted** | **Contradiction** — an ignored parent cannot have tracked children added to it by the normal `git add` path | §Q (intro), §Z.2, §Y.2 row 21, §W | REPO_ADR-020 revised |
| 5 | `EXTRACTION_ID` enumeration read one product ledger; a run may touch several | **Accepted** | **Design error, concrete failure case** — a multi-product run's `EXT` allocation would double-allocate or miss ordinals in the ledgers it didn't check | §F.4 (new subsection), §H, §AB check 20 | REPO_ADR-006 revised |
| 6 | Derived reviews inside the canonical manifest let a renderer upgrade masquerade as a data change | **Accepted** | **Design error, concrete failure case** — purity prevents a *stale-artefact* false positive but not a *renderer-upgrade* one | §A, §D, §E, §F.3, §G.1, §Q.3–Q.4, §W, contradiction scan checks 1, 12, 19 | REPO_ADR-019 revised |
| 7 | Untracking the current 15 samples before a durable payload strategy exists makes portability worse than today | **Accepted** | **Sequencing error with a concrete regression** — see §AI.1 | §A, §O.3–O.6, §Y.1 row 7, §Z (Z.4, Z.5 removed), §AA.4, §AC.2, §AD R1/R7, §AG decision 2 | REPO_ADR-016, 017 revised |
| 8 | Phase 4 depends on Phase 3C metadata that does not yet exist | **Accepted** | **Unstated cross-phase dependency** | §Y.4, §AH (new precondition statement) | REPO_ADR-026 revised |
| 9 | RP6 did not account for `incoming/` and `media/_unregistered/` as pre-registration destinations | **Accepted** | **Design error** — the stated rule ("has an id → `media/`, else → `var/`") had no branch for a file correctly living in neither | §C (RP6 rewritten), §AF | REPO_ADR-030 new |
| 10 | Random-allocated identifiers had no stated collision/retry behaviour | **Accepted** | **Unproven safety claim** — "cannot collide in practice" describes probability, not a write contract | §A, §F.5 (new subsection), §C (RP13 new), §AB check 21, §AD R11 | REPO_ADR-029 new |
| 11 | Google Docs export metadata was overstated as proof no upstream original exists | **Accepted** | **Overclaim** — the metadata supports a narrower, still-sufficient claim | §B.4 finding 1, §K, §N.2, §N.3, contradiction scan check 2 | REPO_ADR-013 revised |
| 12 | A knowledge-directory `README.md` was not distinguished from a `KNOWLEDGE_ID` entity | **Accepted** | **Category error** — operator documentation was implicitly required to carry provenance metadata that does not apply to it | §M.2 (new boundary statement), §N.3, §W, §Y.4 | REPO_ADR-032 new |

### AI.3 Migration-operation changes

| | First pass | This pass | Why |
|---|---|---|---|
| Moves/removals | 7, touching (claimed) 27 files | **6**, touching **25** files | Correction 7 removes the `git rm -r --cached media` step entirely; recounting the actual files named in §Y.1 corrects an arithmetic error the first pass carried (2 books + 8 quarantine + 15 samples = 25, not 27) |
| New-file creations | 11 (10 scaffold items covering ~13 files) | **12** (adding `reviews/README.md`) | `reviews/` is a new top-level root (Correction 6) and needs its own explanatory file |
| Configuration changes | 1 | 1 (unchanged) | The `.gitattributes`/`core.autocrlf` step is unaffected by these corrections in kind, only in the added frozen-document check around it |
| **Total operations** | **21** | **22** | Net: −1 removed step, +2 new-file items, arithmetic correction on the moves row |

### AI.4 Top-level directory-count changes

| | First pass | This pass | Why |
|---|---|---|---|
| Total top-level directories | 11 | **12** | `reviews/` added (Correction 6) |
| Existing after Phase 3B | 8 | **9** | `reviews/` is created in Phase 3B's scaffold step (§Z.5) |
| Reserved (created by a later phase) | 3 (`.claude/`, `src/`, `tests/`) | 3, unchanged | — |

### AI.5 Remaining user decisions

**Six**, down from seven (§AG) — the slug-cap question is resolved outright by the recalculation in §AC.1 rather than left open, per the audit's explicit instruction not to require approval on it. The six: (1) the name `store/`; (2) media stays tracked through Phase 3B, cutover deferred; (3) no history purge, for now; (4) Phase 3B/3C split with 3C now a mandatory Phase 4 precondition; (5) the `.gitattributes` normalisation commit, with its new frozen-document check; (6) reserve rather than scaffold `src/`, `tests/`, `.claude/skills/`.

### AI.6 Phase 3B readiness

**Phase 3A is ready to freeze.** All twelve corrections are applied; the mechanical checks the audit specified in its own closing cross-check (contradiction-scan checks 14–25) are clean; no check identifies a remaining instance of any of the twelve issues. Two things are worth carrying forward as posture, in the same spirit Phase 2's own correction passes recorded: first, **every one of these corrections was found by tracing a mechanism to its actual consequence** — what a precondition implies once the document itself is committed, what a validation strategy implies once new files exist, what a merge strategy implies for the revert command paired with it — rather than by inspecting a section in isolation; that is the check worth re-running on any future revision of this document, not a one-time audit artefact. Second, **Correction 7 is a reminder that "matches the target architecture" and "is the right sequencing" are different questions**, and a migration plan that answers only the first has not fully answered either.

**Phase 3B remains not authorised by this document.** Freezing Phase 3A (committing this corrected document and tagging `phase-3a-freeze`, per §Z.1 Steps 0 and A) is a necessary precondition for Phase 3B, not an authorisation of it — Phase 3B requires its own explicit request, exactly as before this pass.

### AI.7 Final Executability Pass

**Date:** 2026-09-04 · **Trigger:** final execution-level audit · **Scope:** `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` only · **Phase 3B, 3C and 4 not started.**

This pass is narrower in kind than §AI.1–AI.6: it does not revisit the repository architecture — no top-level directory changes name or purpose, no storage regime changes, no frozen Phase 1/2 decision is touched. Every one of its seven corrections concerns **whether the previous pass's own procedures could actually run**, not whether the design they implement is right. That distinction is itself worth naming: a document can pass a design-level audit — is the architecture sound, are the boundaries justified, are the trade-offs stated — and still contain commands that cannot execute, checks that compare the wrong things, or wording that stopped matching the operational world the moment a remote was added. This pass exists because the first correction pass, having just fixed twelve design-level issues, had not yet been checked at that more mechanical level.

**Seven corrections were raised. All seven are accepted.** One operational-state update (the GitHub remote) is recorded alongside them, since it produced textual corrections of the same shape — stale claims that no longer matched reality — even though it originates from outside the document rather than from an audit finding.

#### AI.7.1 The one that mattered most

**Correction 13 was the most structurally serious, because it repeated — in sharper form — the exact category of error Correction 1 had just fixed.** Correction 1 moved the clean-tree precondition from `59cbe49` to `phase-3a-freeze` so that the precondition would not contradict the act of committing this document. But the revised Step A still said *"clean tree before adding the approved document"* — and the approved document is this document, mid-edit, precisely the one file that must be added. The fix from Correction 1 relocated the problem one freeze commit later without noticing it was still the same problem: **a precondition that says "nothing changed yet" cannot gate the commit that is the first change.** The general lesson, worth carrying forward explicitly rather than treated as resolved: fixing a precondition by moving *which* commit it checks against does not, by itself, verify that the new check is satisfiable at the moment it actually needs to run. That has to be checked separately, and this pass is the result of checking it.

#### AI.7.2 Corrections and verdicts

| # | Correction | Verdict | Nature | Sections affected | ADRs |
|---|---|---|---|---|---|
| 13 | Phase 3A freeze precondition required a clean tree before adding the very document being frozen | **Accepted** | **Contradiction, recurrence of Correction 1's category** — see §AI.7.1 | §Z.1 (Step A rewritten: mechanical single-change precondition, commit, *then* clean-tree check) | — |
| 14 | `phase-2-freeze` assumed to exist; no idempotency or conflict discipline for either freeze tag | **Accepted** | **Unstated assumption with a real failure mode** — a second run of the same procedure could silently retag, or could halt on an already-satisfied precondition mistaken for a problem | §Z.1 (new Step 0; the freeze-tag step recast with the same discipline); distinguishes commit-existence from tag-existence explicitly | — |
| 15 | Frozen-document check compared working-tree bytes, which `git add --renormalize` does not govern | **Accepted** | **Insufficient verification** — proves nothing about committed content; also omitted the Phase 3A document itself from protection | §Z.2 (rewritten around `git show <rev>:<path>` and `git diff --exit-code`), §AB checks 2 and 15 | REPO_ADR-024 revised |
| 16 | Rollback's media-hash check compared 25 baseline hashes against 15 present files | **Accepted** | **Structural mismatch — the comparison could never succeed as specified** | §Z.3 (splits `media-baseline.tsv` from the full manifest), §AA.3 (rewritten to use only the 15-row subset, path-preserving) | — |
| 17 | "No non-media tracked file exceeds 1 MB" contradicted the two intentionally-tracked source books (2.7 MB, 6.3 MB) | **Accepted** | **Self-contradiction — the check was guaranteed to fail against the design's own stated tree** | §AB check 8 (rewritten as an explicit two-class allow-list) | — |
| 18 | YAML front matter cannot be applied to a PDF; 3 of the 8 quarantined knowledge entities are PDFs | **Accepted** | **Physical impossibility treated as a uniform requirement** — the design had, without saying so, required something three of its own files cannot do | §M.1 (Option B reconditioned), §M.3 (new — sidecar schema and validation), §N.3, §W, §Y.4 | REPO_ADR-011, 012 revised; REPO_ADR-033 new |
| 19 | Move verification was described in prose ("compare each line's hash") with no executable check | **Accepted** | **A checklist item claimed to be mechanical while requiring a human to eyeball output** | §Z.3 (explicit 25-entry array manifest), §Z.4 (executable verification loop, non-zero exit on failure), §AB check 3 | — |
| — | Operational: `origin` now exists, `master` tracks `origin/master` | **Recorded, not a correction** | Stale wording ("before the first push") no longer matched reality | §B.3, §A, §AD R7, §AG decision 3, REPO_ADR-017; §Z.1 (new: verify-remote-then-push-tags step) | REPO_ADR-017 revised |

#### AI.7.3 Validation changes

Every check in §AB now names an executable comparison, not a description of one — the property Correction 19 demanded of check 3 turned out to be worth re-checking for every other check in the list, and none of the others needed rewording to satisfy it; only check 3 had drifted into prose. Checks 2, 8 and 15 changed in substance (committed-blob comparison; explicit two-class allow-list; four protected documents instead of three). No check's *number* changed, and no check was added or removed from the two lists in §AB — this pass corrects what checks 2, 3, 8 and 15 assert and how they run, not how many checks exist.

#### AI.7.4 Knowledge-provenance mechanism for binary files — summary

§M gains a third subsection (§M.3) rather than a patched version of §M.2, because the mechanism genuinely differs by file type, not merely by degree: a Markdown entity's provenance lives in-file; a PDF's lives in a `.meta.yaml` sidecar bound to its payload by path and hash, fail-closed to `NOT_RETRIEVABLE` absent a valid one. The governing principle — one authoritative provenance record per knowledge entity — is unchanged; only its carrier varies by what the entity's own format can hold. This changes no phase boundary (sidecars are still authored in Phase 3C) and reopens no Phase 1/2 decision.

#### AI.7.5 Count changes

| | Before this pass | After this pass | Why |
|---|---|---|---|
| Repository ADRs | 32 | **33** | REPO_ADR-033 (sidecar mechanism) added; 011, 012 and 024 revised |
| Corrections accepted (cumulative across both passes) | 12 | **19** | 7 more, all accepted (§AI.7.2) |
| Knowledge-entity provenance mechanisms | 1 (front matter, stated as universal) | **2** (front matter for 8 Markdown entities, sidecar for 3 PDF entities) — entity count itself unchanged at 11 | Correction 18 |
| Migration operations, top-level directory count, remaining user decisions | Unchanged (21→22 and 11→12 already reflected in §AI.3–AI.5) | **Unchanged again by this pass** | None of the seven corrections adds, removes or renames a directory or a migration step; they correct how existing steps are checked and sequenced |

#### AI.7.6 Remaining user decisions

**Unchanged at six (§AG).** None of the seven corrections introduces a new decision requiring approval — each fixes a mechanism that was already implementing a previously-approved (or previously-pending) decision, not a decision itself. The operational GitHub update does not add a decision either: publishing already-created freeze tags to an already-existing remote is a synchronisation step, not an architectural choice, and Phase 3B's independence from `origin` is unchanged (§Z.1).

#### AI.7.7 Phase 3A final-freeze readiness

**Phase 3A is ready to freeze.** The final-executability cross-check's ten items are clean:

| # | Check | Result |
|---|---|---|
| 1 | Requiring a clean tree before adding the modified design document | **None remaining.** §Z.1 Step A's precondition now permits exactly that one change, commits it, and checks for a clean tree only afterward. |
| 2 | Assuming `phase-2-freeze` exists without checking | **None remaining.** §Z.1 Step 0 checks commit-existence and tag-existence separately and creates the tag only if absent, verifying rather than retagging if present. |
| 3 | Protecting only working-tree bytes during normalisation | **None remaining.** §Z.2 compares `git show <rev>:<path>` output — committed blobs — before and after, with a `git diff --exit-code` as a second, independent confirmation. |
| 4 | Omitting the frozen Phase 3A document from normalisation integrity checks | **None remaining.** All four documents — including `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` itself — are checked in §Z.2 and validated in §AB checks 2 and 15. |
| 5 | Comparing 25 move hashes against 15 media hashes | **None remaining.** §Z.3 splits `/tmp/media-baseline.tsv` (15 rows) from the full 25-row manifest; §AA.3 uses only the former, path-preserving. |
| 6 | Claiming no non-media tracked file exceeds 1 MB | **None remaining.** §AB check 8 now names an explicit two-class allow-list (15 media samples, 2 source books) rather than a single blanket assertion the design's own tree violates. |
| 7 | Requiring Markdown front matter directly on a PDF | **None remaining.** §M.3 gives the 3 quarantined PDFs a sidecar mechanism; §N.3, §W and §Y.4 all reflect the split. |
| 8 | Calling a manual hash inspection "mechanical" | **None remaining.** §Z.4's verification is a `while read` loop with a non-zero exit on any failure, over the explicit manifest built in §Z.3; §AB check 3 now names that loop rather than a described comparison. |
| 9 | Claiming the repository has not yet been pushed when `origin/master` now exists | **None remaining.** §B.3 and §A's push-related wording is corrected to state the push has already happened. |
| 10 | Telling the operator that history can still be purged "before the first push" | **None remaining.** Every instance (§A, §AD R7, §AG decision 3, REPO_ADR-017) now states that a purge would require a coordinated remote rewrite and re-clone, not a same-machine operation performed before an as-yet-unmade push. |

No decision in this pass required user approval that was not already open in §AG, and no new approval item was created. **Every Phase 3B validation described in §AB is now executable as written** — each names a specific command or loop with a defined pass/fail signal, not a description a human must interpret. ***This claim was, at the time this sentence was first written, an overclaim*** — a subsequent targeted review found that checks 4–13, 16 and 17 were still prose criteria rather than runnable commands, exactly the gap the claim above denied having. §AB.1 (added in the micro-fix pass immediately following this one, §AI.7.8 Fix 26) closes that gap with an executable block per check, and the sentence above is accurate only as of that addition — left here, corrected rather than deleted, because a false claim quietly fixed and left unremarked is worse than a false claim named as one.

**Phase 3B remains not authorised. Phase 3C remains not authorised. Phase 4 remains not authorised.**

### AI.7.8 Final Micro-Fix Pass (Fixes 20–26)

**Date:** 2026-09-04 · **Trigger:** final targeted execution review · **Scope:** `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` only · **Phase 3B, 3C and 4 not started.**

This pass is narrower again than §AI.7.1–AI.7.7: every one of its seven fixes corrects a specific command, a specific default, or a specific claim inside procedures the previous two passes already approved in shape. None changes what the repository looks like, what gets moved, or when. The through-line across all seven, worth stating once rather than seven times: **a mechanism can be exactly right in its stated intent and still be wrong in its literal execution** — an annotated tag peels differently than a lightweight one; a manifest rule stated as "every file under a root" is falsified the moment that root gets a `README.md`; a flag (`--no-index`) silently changes what a widely-used git command actually tests; a fail-closed rule stated for one file format and merely assumed for another is not actually stated for both; a claim of universal executability is only as true as the least-executable check in the list it describes.

#### Fixes applied and verdicts

| # | Fix | Verdict | Nature | Sections affected |
|---|---|---|---|---|
| 20 | Annotated tags verified with bare `git rev-parse <tag>`, compared directly against a commit SHA | **Accepted** | **Category confusion** — an annotated tag's own object SHA is not the commit it points at; verified empirically (§AI.7.8 evidence, below) that the unpeeled comparison would never match | §Z.1 (Step 0, the freeze-tag step, and Step B's preflight — all three peeled to `^{commit}`) |
| 21 | Source manifest defined as "every file under `store/`/`config/`" while both roots hold operator READMEs | **Accepted** | **Self-contradiction** — Phase 3B's own scaffold step creates the files the definition says cannot exist | §A decision 3, RP4, §Q.4, §W (new rows) |
| 22 | `git check-ignore` run without `--no-index`, and without NUL-safety | **Accepted** | **Silent false negative, verified empirically** — a tracked file matching an active ignore rule returns no match without `--no-index`, exactly the case RP7 exists to catch | RP12, §W's check command, §AB check 7 |
| 23 | Markdown provenance had no stated fail-closed default; only the PDF sidecar did | **Accepted** | **Asymmetric, unstated default** — an omission that resolves to the one outcome (permitted) this design exists to prevent | §M.1.1 (new), §M.2 (fifth property added), §N.3, §Y.4, §AH, REPO_ADR-011/012 revised, REPO_ADR-034 new, §AD R9 |
| 24 | Execution shell called "POSIX shell" while the commands use Bash-only syntax | **Accepted** | **Inaccurate environment claim** — Bash arrays, `${!arr[@]}`, and `$'\t'` are not POSIX `sh` | §B.4 finding 6, §Z introduction, §AC.1 (new row) |
| 25 | `store/assets/` required to be empty, when Phase 3B's own scaffold step never creates it | **Accepted** | **Self-contradiction** — RP11 and §Z.5's actual `mkdir -p` list disagree with the check's implicit assumption | §AB check 13 |
| 26 | §AI.7 claimed every Phase 3B validation was executable; most of checks 4–13, 16–17 were prose | **Accepted** | **Overclaim** — see the marked correction just above this subsection | New §AB.1 (executable block for every check not already given one in §Z) |

#### Evidence for Fixes 20 and 22, verified rather than asserted

Both fixes rest on git behaviour that is easy to state wrongly from memory, so both were checked against a real repository before being written into this document, not merely reasoned about:

- **Fix 20:** an annotated tag's `git rev-parse <tag>` returns the *tag object's* SHA; only `git rev-parse <tag>^{commit}` peels to the commit. Untested, this is exactly the kind of detail that looks obviously fine and silently is not.
- **Fix 22:** `git check-ignore -v <path>`, run **without** `--no-index`, was confirmed to print nothing for a path that is both tracked and matched by an active `.gitignore` rule — while `git check-ignore --no-index -v <path>` correctly reports the match. This means the original check (§W, §AB check 7, first two passes) could never have caught the exact failure mode it was written to catch.

#### Count changes

| | Before this pass | After this pass |
|---|---|---|
| Repository ADRs | 33 | **34** (REPO_ADR-034 added; 011, 012 revised again) |
| Corrections/fixes accepted (cumulative, all three passes) | 19 | **26** |
| Top-level directories, migration operations, remaining user decisions | Unchanged | **Unchanged** — every one of the seven fixes corrects a command, a default, or a claim, never a structural element |

#### Remaining user decisions

**Unchanged at six (§AG).** None of these seven fixes introduces a new decision — each corrects a mechanism implementing a decision already made or already open, exactly as the previous micro-pass's fixes did.

#### Phase 3A final-freeze readiness

**Phase 3A is ready to freeze.** The user's own ten-item cross-check is clean: no unpeeled tag comparison remains; the source-manifest definition is now a mechanical file-class rule with no self-contradiction against Phase 3B's own scaffold; every `check-ignore` invocation uses `--no-index` and NUL-safe piping; no knowledge carrier defaults to permitted on missing or invalid provenance; the shell requirement is stated as Bash / Git Bash, not POSIX `sh`, with PowerShell explicitly flagged as unsafe to paste into; `store/assets/` is allowed to be absent; and §AB.1 now gives every check in the Phase 3B list an executable form, with the one honest exception (check 14) named as such rather than silently left as prose and claimed otherwise.

**Phase 3B remains not authorised. Phase 3C remains not authorised. Phase 4 remains not authorised.**

### AI.7.9 Final Validation Exit-Status Patch (Fixes 27–28, plus a tooling-wording correction)

**Date:** 2026-09-04 · **Trigger:** final literal execution review · **Scope:** `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` only · **Phase 3B, 3C and 4 not started.**

Where §AI.7.8 made every check in §AB.1 *executable*, this pass makes the block's *result* trustworthy — a distinction the previous pass's own closing claim did not quite reach. A block that prints the right `PASS`/`FAIL` line for each check is not yet a validation gate: `echo`, `printf` and `cat` all exit 0 regardless of what they print, and seventeen-minus-four checks concatenated into one script means a later check's harmless success can leave the shell's own `$?` looking clean after an earlier check has already failed. Two of this pass's three items are corrections to §AB.1 itself; the third corrects an environment claim that undercounted its own dependencies.

#### Fixes applied and verdicts

| # | Fix | Verdict | Nature | Sections affected |
|---|---|---|---|---|
| 27 | AB.1 printed PASS/FAIL per check but had no single aggregate exit status; a later check's success could mask an earlier check's failure | **Accepted** | **The block's literal exit status did not match its printed content** — verified empirically (below): a `PASS` printed after a `FAIL` left the block's own exit code clean | §AB.1 (every check now sets a shared `overall_fail` on its own failure; the block ends with one aggregate `false`/`true`) |
| 28 | Check 6 confirmed `git log --follow` returned *something* for the target path, which is true even when history was never actually followed through the rename | **Accepted** | **Insufficient proof, verified empirically** — a broken migration (delete + unrelated new file at the target path) passed the old check 6 while genuinely lacking reachable pre-migration history | §AB.1 check 6 (rewritten to resolve the source's last pre-freeze commit via `git rev-list -1 phase-3a-freeze -- "$src"` and require that exact hash inside the target's own `--follow` history) |
| — | "Every Phase 3B command uses only `git` and `sha256sum`" understated the tooling §AB.1 itself introduced (`find`, `grep`, `sort`, `comm`, `wc`, `cut`, `sed`, `diff`, `xargs`) | **Corrected, not a numbered fix** | **Stale environment claim** — true when first written, false once §AB.1 existed | §B.4 finding 6, §Z introduction; a new tooling preflight added to §Z.1 |

#### Evidence for Fixes 27 and 28, verified rather than asserted

Consistent with this document's practice since §AI.7.8, both mechanisms were run against real shells and a real throwaway repository before being written down, not reasoned about from memory:

- **Fix 27:** a three-line script — `PASS`, then `FAIL … overall_fail=1`, then `PASS` again — was run to completion; its own `$?` was `1` only because the final `if` block tests the accumulated `overall_fail` and ends in `false`, not because any individual line's exit status survived to the end. Without that final aggregate step, the same script's natural exit status is `0`, matching the defect this fix names.
- **Fix 28:** a mock repository was built with a **broken** migration — the source file deleted, an unrelated new file created at the target path, no `git mv`, so git has no rename to detect. The **old** check (`git log --follow --oneline -- "$tgt" | grep -q .`) reported `PASS`, because the target's own move commit is non-empty output on its own. The **new** check correctly reported `FAIL`, because the resolved pre-freeze commit for the source path never appears in the target's `--follow` history. The same mock repository's genuine `git mv` case was also run and correctly reported `PASS` under the new check.

#### Count changes

| | Before this pass | After this pass |
|---|---|---|
| Repository ADRs | 34 | **34 — unchanged.** Both fixes correct §AB.1's own logic, not a design decision an ADR records |
| Corrections/fixes accepted (cumulative, all four passes) | 26 | **28**, plus one tooling-wording correction recorded alongside them |
| Top-level directories, migration operations, remaining user decisions | Unchanged | **Unchanged** |

#### Remaining user decisions

**Unchanged at six (§AG).** Neither fix, nor the tooling correction, introduces a new decision.

#### Phase 3A final-freeze readiness

**Phase 3A is ready to freeze.** The user's own six-item final check is clean: a `FAIL` anywhere in §AB.1 now makes the whole block return non-zero, verified by running it; no later `PASS` can mask an earlier `FAIL`, because `overall_fail` is never reset and the block's exit status is read from it, not from whatever ran last; check 6 now proves the target's history reaches a specific commit that existed for the source path *before* Phase 3B, not merely that `--follow` printed something; the tooling requirement now names every utility §Z and §AB.1 actually call, backed by a `command -v` preflight in §Z.1; Git Bash remains the documented and only assumed execution shell; and Phase 3B remains, as at every prior pass, not authorised.

**Phase 3B remains not authorised. Phase 3C remains not authorised. Phase 4 remains not authorised.**

---

## Compliance with Phase 3A constraints

| Constraint | Status |
|---|---|
| `docs/PHASE_1_SYSTEM_DESIGN.md` read before designing | ✅ Full document, treated as frozen |
| `docs/PHASE_2_DATA_ARCHITECTURE.md` read before designing | ✅ Full document, treated as frozen |
| `PRE_FLIGHT_AUDIT.md` unmodified and not moved | ✅ Not opened for writing |
| Repository inspected read-only; PRE_FLIGHT inventory not assumed current | ✅ §B — fresh enumeration, 32 tracked files, sizes, config, history, PDF metadata |
| No repository migration executed | ✅ Designed in §Y–§Z, unexecuted |
| No file moved, renamed, deleted or quarantined | ✅ `git status` clean apart from this document, before and after all four correction passes |
| No knowledge or source file modified | ✅ |
| No config file (`*.yaml`), `.gitignore` or `.gitattributes` created | ✅ Their exact content is drafted in §Z.2 and §Y.2 for Phase 3B to apply; none exists in the working tree yet |
| No repository file created | ✅ This micro-fix pass created nothing outside this document — the empirical git checks in §AI.7.8 that verified Fixes 20 and 22 ran in a throwaway repository, not this one |
| No migration command executed | ✅ §Z's commands, including all four passes' revised freeze, normalisation, preflight and verification steps, remain proposed text |
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
| Phase 3C not started | ✅ Explicitly ordered before Phase 4, not merely undated (§AH, §Y.4) |
| Phase 4 not started | ✅ |
| Only `docs/PHASE_3_REPOSITORY_MIGRATION_DESIGN.md` created or modified — through the design pass and all four correction passes | ✅ Empirical checks verifying Fixes 20, 22, 27 and 28 ran in throwaway repositories under `/tmp`, never in this repository |
| Frozen Phase 1 and Phase 2 constraints not reopened by any correction pass | ✅ Contradiction scan, checks 12–13; no Phase 1 or Phase 2 ADR listed as reopened in §AF |
| Contradiction scan re-run in full, including against the second pass's own closing cross-check | ✅ Contradiction scan, checks 1–25 — clean, with one named and approved future exception (check 4, not yet in effect) |
| Final executability cross-check (second pass) run against all ten of its own specified items | ✅ §AI.7.7 — clean |
| Final micro-fix cross-check (third pass) run against all ten of its own specified items | ✅ §AI.7.8 — clean |
| Final validation exit-status cross-check (fourth pass) run against all six of its own specified items | ✅ §AI.7.9 — clean |
| Simplification pass still holds after all four passes' additions | ✅ §AE — eleven boundaries removed (revised down from twelve: `reviews/` is reinstated, not cut, per Correction 6); it is justified against the same six questions in §A decision 3 and RP5, not exempted from them. No pass after the first adds a new top-level directory (§AI.7.5, §AI.7.8, §AI.7.9) |
| All twelve external-audit corrections from the first pass applied | ✅ §AI.1–AI.6 |
| All seven final-executability corrections from the second pass applied, plus the operational GitHub update recorded | ✅ §AI.7.1–AI.7.7 |
| All seven micro-fixes from the third pass applied | ✅ §AI.7.8 |
| Both validation exit-status fixes from the fourth pass applied, plus the tooling-wording correction recorded | ✅ §AI.7.9 |
| Every Phase 3B validation check names an executable comparison, not a described one, or is honestly described as not yet exercisable — and the block's own exit status is now trustworthy, not merely its printed lines | ✅ §AB, §AB.1, §AI.7.8–AI.7.9 — corrected from two successive overclaims, each identified and fixed within this same document |

**Phase 3A's correction passes end here. Phase 3B is not authorised and has not been started. Phase 3C is not authorised and has not been started. Phase 4 is not authorised and has not been started.**
