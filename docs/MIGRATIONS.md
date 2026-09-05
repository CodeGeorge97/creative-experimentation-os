# Repository Migration Log

This file is an append-only record of tracked repository path migrations.

A move is recorded even when file content is byte-identical because canonical
and referenced repository paths are part of the repository architecture.

## 001 — Phase 3B repository migration

Physical repository migration from the Phase 3A frozen layout to the Phase 3B
layout.

All 25 moved files were independently verified after migration: the original
path is absent, the destination exists, and the destination SHA-256 matches the
pre-migration baseline.

| Date | Commit | From | To | Reason |
|---|---|---|---|---|
| 2026-09-04 | `67467d89893113f9e693d5fa68cd7e9fec4d5cc1` | `sources/original-books/breakthrough-advertising-0887232981-9780887232985 (1)_compressed.pdf` | `sources/books/breakthrough-advertising.pdf` | Move original book into the stable sources/books layout; preserve bytes. |
| 2026-09-04 | `67467d89893113f9e693d5fa68cd7e9fec4d5cc1` | `sources/original-books/_OceanofPDF.com_The_brilliance_breakthrough_-_Eugene_schwartz.pdf` | `sources/books/brilliance-breakthrough.pdf` | Move original book into the stable sources/books layout; preserve bytes. |
| 2026-09-04 | `c15ab004797eb411fa98a384c72dfb012ce6ecdb` | `knowledge/methodology/Dominio del Post ID_ Escalamiento y Prueba Social en Meta.pdf` | `knowledge/_quarantine/methodology/Dominio del Post ID_ Escalamiento y Prueba Social en Meta.pdf` | Move methodology corpus into quarantine without modifying content. |
| 2026-09-04 | `c15ab004797eb411fa98a384c72dfb012ce6ecdb` | `knowledge/methodology/Escalamiento Creativo y Prueba Social en Meta Ads.pdf` | `knowledge/_quarantine/methodology/Escalamiento Creativo y Prueba Social en Meta Ads.pdf` | Move methodology corpus into quarantine without modifying content. |
| 2026-09-04 | `c15ab004797eb411fa98a384c72dfb012ce6ecdb` | `knowledge/methodology/Metodología Evolve para Testeo Creativo en Meta Ads.pdf` | `knowledge/_quarantine/methodology/Metodología Evolve para Testeo Creativo en Meta Ads.pdf` | Move methodology corpus into quarantine without modifying content. |
| 2026-09-04 | `c15ab004797eb411fa98a384c72dfb012ce6ecdb` | `knowledge/methodology/modulo-1-estrategia-mercado.md` | `knowledge/_quarantine/methodology/modulo-1-estrategia-mercado.md` | Move methodology corpus into quarantine without modifying content. |
| 2026-09-04 | `c15ab004797eb411fa98a384c72dfb012ce6ecdb` | `knowledge/methodology/modulo-2-psicologia-persuasion.md` | `knowledge/_quarantine/methodology/modulo-2-psicologia-persuasion.md` | Move methodology corpus into quarantine without modifying content. |
| 2026-09-04 | `c15ab004797eb411fa98a384c72dfb012ce6ecdb` | `knowledge/methodology/modulo-3-anuncios-estaticos.md` | `knowledge/_quarantine/methodology/modulo-3-anuncios-estaticos.md` | Move methodology corpus into quarantine without modifying content. |
| 2026-09-04 | `c15ab004797eb411fa98a384c72dfb012ce6ecdb` | `knowledge/methodology/modulo-4-ugc-vsl-strategy.md` | `knowledge/_quarantine/methodology/modulo-4-ugc-vsl-strategy.md` | Move methodology corpus into quarantine without modifying content. |
| 2026-09-04 | `c15ab004797eb411fa98a384c72dfb012ce6ecdb` | `knowledge/methodology/modulo-5-infraestructura-herramientas (1).md` | `knowledge/_quarantine/methodology/modulo-5-infraestructura-herramientas.md` | Move methodology corpus into quarantine without modifying content. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/style-references/animation/WhatsApp Video 2026-09-03 at 10.00.56 PM.mp4` | `media/_unregistered/style-references/animation/WhatsApp Video 2026-09-03 at 10.00.56 PM.mp4` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/style-references/animation/WhatsApp Video 2026-09-03 at 10.02.18 PM.mp4` | `media/_unregistered/style-references/animation/WhatsApp Video 2026-09-03 at 10.02.18 PM.mp4` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/style-references/animation/WhatsApp Video 2026-09-03 at 10.54.06 PM.mp4` | `media/_unregistered/style-references/animation/WhatsApp Video 2026-09-03 at 10.54.06 PM.mp4` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/style-references/podcast/WhatsApp Video 2026-09-03 at 10.04.02 PM.mp4` | `media/_unregistered/style-references/podcast/WhatsApp Video 2026-09-03 at 10.04.02 PM.mp4` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/style-references/podcast/WhatsApp Video 2026-09-03 at 10.04.04 PM.mp4` | `media/_unregistered/style-references/podcast/WhatsApp Video 2026-09-03 at 10.04.04 PM.mp4` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/style-references/podcast/WhatsApp Video 2026-09-03 at 10.54.05 PM.mp4` | `media/_unregistered/style-references/podcast/WhatsApp Video 2026-09-03 at 10.54.05 PM.mp4` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/style-references/ugc/WhatsApp Video 2026-09-03 at 10.01.37 PM.mp4` | `media/_unregistered/style-references/ugc/WhatsApp Video 2026-09-03 at 10.01.37 PM.mp4` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/style-references/ugc/WhatsApp Video 2026-09-03 at 10.02.19 PM (1).mp4` | `media/_unregistered/style-references/ugc/WhatsApp Video 2026-09-03 at 10.02.19 PM (1).mp4` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/style-references/ugc/WhatsApp Video 2026-09-03 at 10.02.19 PM.mp4` | `media/_unregistered/style-references/ugc/WhatsApp Video 2026-09-03 at 10.02.19 PM.mp4` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.01.37-PM.wav` | `media/_unregistered/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.01.37-PM.wav` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.02.19-PM-_1_.wav` | `media/_unregistered/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.02.19-PM-_1_.wav` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.02.19-PM.wav` | `media/_unregistered/voices/chile/female/WhatsApp-Video-2026-09-03-at-10.02.19-PM.wav` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/voices/chile/male/ssstik.io_1788494437870.mp3` | `media/_unregistered/voices/chile/male/ssstik.io_1788494437870.mp3` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/voices/chile/male/ssstik.io_1788494482734.mp3` | `media/_unregistered/voices/chile/male/ssstik.io_1788494482734.mp3` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
| 2026-09-05 | `072761cf81f807568ac7a2e7ba12aea7d49aaec5` | `samples/voices/chile/male/ssstik.io_1788494597329.mp3` | `media/_unregistered/voices/chile/male/ssstik.io_1788494597329.mp3` | Move repository-origin sample media under the media root pending future registration; preserve bytes and Git tracking. |
