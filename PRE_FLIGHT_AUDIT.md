# PRE-FLIGHT AUDIT

**Proyecto:** creative-experimentation-os
**Fecha de auditoría:** 2026-09-03
**Alcance:** verificación de disponibilidad, accesibilidad y clasificación del material. No incluye análisis de contenido, diseño de arquitectura ni ejecución de Phases.
**Estado del repositorio:** git inicializado, 1 commit (`92ec3eb — Baseline antes de Phase 1`), working tree limpio.

---

## 1. Executive Summary

**OVERALL PRE-FLIGHT STATUS: PASS WITH WARNINGS**

El proyecto contiene **29 archivos** distribuidos en cuatro categorías funcionales. Todo el material estructurado en Markdown es legible (UTF-8, sin corrupción), los 8 dominios metodológicos esperados están cubiertos, y los 15 archivos multimedia son contenedores válidos y accesibles.

**No existen blockers críticos.** PHASE 1 — FINAL AUDIT + SYSTEM DESIGN puede comenzar.

Se registran **7 advertencias no bloqueantes**, de las cuales tres merecen atención temprana:

1. Los tres documentos Schwartz están en `knowledge/copywriting/`, no en `knowledge/copywriting/schwartz/` (carpeta creada pero vacía).
2. Los tres samples de voz femenina son **pistas de audio extraídas de los tres videos UGC**, no grabaciones independientes (coincidencia exacta de duración verificada).
3. `sources/methodology/` está vacía: los PDFs metodológicos originales residen dentro de `knowledge/`, mezclando fuente cruda con conocimiento estructurado.

Adicionalmente, uno de los dos libros originales (*The Brilliance Breakthrough*) es un PDF escaneado sin capa de texto, por lo que el conocimiento derivado de él no puede reverificarse automáticamente contra su fuente.

---

## 2. Project Inventory

| Categoría | Archivos | Formatos | Estado |
|---|---|---|---|
| SOURCES — original books | 2 | PDF | Accesible (1 requiere OCR) |
| SOURCES — methodology | 0 | — | **Vacía** |
| STRUCTURED KNOWLEDGE — methodology | 8 | 5 MD + 3 PDF | Accesible / legible |
| STRUCTURED KNOWLEDGE — Schwartz | 3 | MD | Accesible / legible |
| CREATIVE REFERENCES — video | 9 | MP4 | Accesible / válidos |
| VOICES — audio | 6 | 3 WAV + 3 MP3 | Accesible / válidos |
| OTHER ASSETS | 1 | MD (`README.md`) | Accesible |
| **TOTAL** | **29** | | |

**Volumen total de media:** ~137 MB (video ~92 MB, audio ~45 MB).
**Duplicados exactos:** ninguno. Verificado por MD5 sobre los 29 archivos — 29 hashes únicos.

---

## 3. Source Documents

**Ubicación:** `sources/original-books/`

| Archivo | Tamaño | Páginas | Texto extraído | Estado |
|---|---|---|---|---|
| `breakthrough-advertising-0887232981-9780887232985 (1)_compressed.pdf` | 2.7 MB | 239 | 354.606 chars | **READABLE** |
| `_OceanofPDF.com_The_brilliance_breakthrough_-_Eugene_schwartz.pdf` | 6.3 MB | 149 | 0 chars | **UNREADABLE** |

**Diagnóstico del PDF ilegible:** cabecera `%PDF-1.4` válida, archivo no corrupto. Contiene 149 páginas compuestas exclusivamente por objetos `/Image` — es un **escaneo sin capa de texto**. `pdftotext` devuelve cero caracteres en todo el documento. Requeriría OCR para procesamiento automático.

**Nota relevante:** esta limitación ya está documentada dentro del propio conocimiento derivado. `schwartz_language_engine.md:6` declara explícitamente que la fuente es image-based y que la extracción se construyó por revisión visual directa. La limitación es **conocida y declarada**, no un defecto silencioso.

`sources/methodology/` — **carpeta vacía** (0 archivos). Ver §10.

---

## 4. Structured Knowledge

### 4.1 Metodología — Markdown (`knowledge/methodology/`)

| Archivo | Tamaño | Líneas | Encoding | Estado |
|---|---|---|---|---|
| `modulo-1-estrategia-mercado.md` | 15.0 KB | 106 | UTF-8 | READABLE |
| `modulo-2-psicologia-persuasion.md` | 13.0 KB | 114 | UTF-8 (CRLF) | READABLE |
| `modulo-3-anuncios-estaticos.md` | 11.3 KB | 124 | UTF-8 | READABLE |
| `modulo-4-ugc-vsl-strategy.md` | 17.8 KB | 133 | UTF-8 | READABLE |
| `modulo-5-infraestructura-herramientas (1).md` | 13.0 KB | 119 | UTF-8 | READABLE |

### 4.2 Metodología — PDF (`knowledge/methodology/`)

| Archivo | Tamaño | Páginas | Texto extraído | Estado |
|---|---|---|---|---|
| `Metodología Evolve para Testeo Creativo en Meta Ads.pdf` | 92 KB | 2 | 2.648 chars | READABLE |
| `Escalamiento Creativo y Prueba Social en Meta Ads.pdf` | 95 KB | 2 | 3.373 chars | READABLE |
| `Dominio del Post ID_ Escalamiento y Prueba Social en Meta.pdf` | 99 KB | 2 | 3.899 chars | READABLE |

Extracción UTF-8 verificada: los acentos y caracteres especiales se recuperan correctamente. No hay problemas de encoding ni de OCR en estos tres documentos.

### 4.3 Observación de clasificación

Los tres PDFs de §4.2 son **documentos fuente originales**, no conocimiento reestructurado, pero residen bajo `knowledge/`. Ver §9.

---

## 5. Schwartz Knowledge Status

### Verificación de presencia y legibilidad

| Archivo requerido | Presente | Tamaño | Líneas | Legibilidad |
|---|---|---|---|---|
| `schwartz_persuasion_framework.md` | Sí | 22.3 KB | 732 | READABLE |
| `schwartz_language_engine.md` | Sí | 17.5 KB | 732 | READABLE |
| `schwartz_integration_map.md` | Sí | 9.9 KB | 419 | READABLE |

Los tres archivos existen, son UTF-8 válido, no están vacíos y no presentan corrupción.

### Verificación de ubicación — DISCREPANCIA

**Ubicación requerida:** `knowledge/copywriting/schwartz/`
**Ubicación real:** `knowledge/copywriting/`

La carpeta `knowledge/copywriting/schwartz/` **existe pero está vacía**. Los tres documentos están un nivel por encima, directamente en `knowledge/copywriting/`.

Clasificado como **advertencia no bloqueante**: los archivos son accesibles y legibles en su ubicación actual; solo la ruta difiere de la especificación. No se ha movido ni modificado nada.

### Trazabilidad declarada

Ambos documentos técnicos declaran su fuente primaria en cabecera:

- `schwartz_persuasion_framework.md:4` → *Breakthrough Advertising* (PDF, edición traducida automáticamente). Fuente presente y READABLE.
- `schwartz_language_engine.md:4` → *The Brilliance Breakthrough* (PDF escaneado). Fuente presente pero UNREADABLE.

`schwartz_integration_map.md` es un documento de arquitectura de integración: define cómo se conectan las dos capas anteriores en lugar de derivar de un libro.

---

## 6. Methodology Status

### Cobertura de dominios esperados

| Dominio esperado | Cubierto | Fuente | Estado |
|---|---|---|---|
| Market strategy | Sí | `modulo-1-estrategia-mercado.md` | READABLE |
| Psychology / persuasion | Sí | `modulo-2-psicologia-persuasion.md` | READABLE |
| Static ads | Sí | `modulo-3-anuncios-estaticos.md` | READABLE |
| UGC / VSL | Sí | `modulo-4-ugc-vsl-strategy.md` | READABLE |
| Creative infrastructure | Sí | `modulo-5-infraestructura-herramientas (1).md` | READABLE |
| Creative testing | Sí | `modulo-5` §5.1 + PDF *Metodología Evolve* | READABLE |
| Meta scaling | Sí | PDF *Escalamiento Creativo y Prueba Social* | READABLE |
| Post ID | Sí | PDF *Dominio del Post ID* | READABLE |

**Los 8 dominios están cubiertos.** No se detectan huecos temáticos.

### Observaciones estructurales

- **Asimetría de formato:** cinco dominios llegan como Markdown estructurado (módulos 1–5) y tres como PDF narrativo (testing, scaling, Post ID). Los tres PDFs son considerablemente más breves (2 páginas cada uno) que los módulos Markdown.
- **Continuidad declarada:** el PDF de Post ID abre con *"En el Módulo 5 que acabamos de desarrollar…"*, lo que indica que los tres PDFs son continuación directa de la serie de módulos y no material independiente. Sugiere que existe una secuencia editorial única repartida en dos formatos.
- **Nicho identificado:** el material está anclado a un caso concreto (suplemento para caída capilar asociada a SOP, mercado chileno). Esto es contexto, no defecto.

### Fuentes mencionadas y ausentes

No se detecta ninguna fuente referenciada por el proyecto que falte, con una salvedad: los módulos Markdown contienen marcadores numéricos de cita (`[65, 70, 93]`, `1`, `2`) que apuntan a un corpus de referencia numerado que **no está presente en el repositorio**. No es bloqueante — el contenido es autosuficiente — pero las citas no son resolubles.

---

## 7. Video Reference Status

**Total:** 9 archivos MP4. Todos con cabecera `ftypmp42` válida. Cero archivos de tamaño nulo, cero corruptos, cero formatos incompatibles.

### UGC — `samples/style-references/ugc/`

| Archivo | Duración | Tamaño |
|---|---|---|
| `WhatsApp Video 2026-09-03 at 10.01.37 PM.mp4` | 58.5 s | 12.5 MB |
| `WhatsApp Video 2026-09-03 at 10.02.19 PM (1).mp4` | 95.3 s | 18.3 MB |
| `WhatsApp Video 2026-09-03 at 10.02.19 PM.mp4` | 75.0 s | 14.1 MB |

### Podcast — `samples/style-references/podcast/`

| Archivo | Duración | Tamaño |
|---|---|---|
| `WhatsApp Video 2026-09-03 at 10.04.02 PM.mp4` | 30.8 s | 2.6 MB |
| `WhatsApp Video 2026-09-03 at 10.04.04 PM.mp4` | 68.0 s | 6.6 MB |
| `WhatsApp Video 2026-09-03 at 10.54.05 PM.mp4` | 47.7 s | 8.9 MB |

### Animation — `samples/style-references/animation/`

| Archivo | Duración | Tamaño |
|---|---|---|
| `WhatsApp Video 2026-09-03 at 10.00.56 PM.mp4` | 67.9 s | 13.2 MB |
| `WhatsApp Video 2026-09-03 at 10.02.18 PM.mp4` | 50.0 s | 10.3 MB |
| `WhatsApp Video 2026-09-03 at 10.54.06 PM.mp4` | 40.7 s | 6.2 MB |

### Detección de anomalías

- **Duplicados:** ninguno. Los dos archivos `10.02.19 PM` en UGC son **archivos distintos** (MD5 distintos, 95.3 s vs 75.0 s). El sufijo `(1)` es un artefacto de colisión de descarga, no una copia.
- **Zero-byte:** ninguno.
- **Formatos incompatibles:** ninguno.
- **Sospechosos/corruptos:** ninguno.

### Muestra representativa seleccionada

**UGC (3 de 3):** los tres archivos. El rango 58–95 s cubre bien la variación de duración disponible.

**Podcast (2 de 3):** `10.04.04 PM.mp4` (68.0 s) y `10.54.05 PM.mp4` (47.7 s) — seleccionados por ser los de mayor duración, con separación suficiente para contrastar ritmo.

**Animation (2 de 3):** `10.00.56 PM.mp4` (67.9 s) y `10.02.18 PM.mp4` (50.0 s) — mismo criterio.

*No se han generado Style Profiles.*

---

## 8. Voice Sample Status

**Total:** 6 archivos. Todos con cabecera válida (`RIFF` para WAV, `ID3` para MP3). Cero archivos de tamaño nulo, cero corruptos.

### Female — `samples/voices/chile/female/`

| Archivo | Duración | Formato | Tamaño |
|---|---|---|---|
| `WhatsApp-Video-2026-09-03-at-10.02.19-PM-_1_.wav` | 95.3 s | WAV 48 kHz / 2 ch / 16-bit | 18.3 MB |
| `WhatsApp-Video-2026-09-03-at-10.02.19-PM.wav` | 74.8 s | WAV 48 kHz / 2 ch / 16-bit | 14.4 MB |
| `WhatsApp-Video-2026-09-03-at-10.01.37-PM.wav` | 58.5 s | WAV 48 kHz / 2 ch / 16-bit | 11.2 MB |

### Male — `samples/voices/chile/male/`

| Archivo | Duración | Formato | Tamaño |
|---|---|---|---|
| `ssstik.io_1788494482734.mp3` | ~47.5 s | MP3 128 kbps / 44.1 kHz / joint stereo | 761 KB |
| `ssstik.io_1788494437870.mp3` | ~33.3 s | MP3 **64 kbps** / 44.1 kHz / joint stereo | 267 KB |
| `ssstik.io_1788494597329.mp3` | ~22.0 s | MP3 128 kbps / 44.1 kHz / stereo | 352 KB |

### Hallazgo: las voces femeninas derivan de los videos UGC

Las tres duraciones WAV coinciden con las de los tres MP4 de UGC dentro del margen de redondeo:

| Video UGC | Duración video | WAV femenino | Duración WAV |
|---|---|---|---|
| `…10.01.37 PM.mp4` | 58.5 s | `…10.01.37-PM.wav` | 58.5 s |
| `…10.02.19 PM (1).mp4` | 95.3 s | `…10.02.19-PM-_1_.wav` | 95.3 s |
| `…10.02.19 PM.mp4` | 75.0 s | `…10.02.19-PM.wav` | 74.8 s |

Los nombres de archivo (`WhatsApp-Video-…`) refuerzan la conclusión: son **pistas de audio extraídas de los mismos tres videos UGC**, no grabaciones de voz independientes.

Implicaciones para fases posteriores:

- El corpus de voz femenina y el corpus de referencia UGC **no son fuentes independientes**. Cualquier validación cruzada entre "estilo UGC" y "voz femenina" sería circular.
- La asignación al folder `female/` **no ha sido verificada auditivamente** en esta auditoría. Se deriva del folder, no de análisis del contenido.
- La diversidad real de hablantes es desconocida: podrían ser una, dos o tres personas distintas.

### Asimetría técnica entre corpus

El corpus femenino es WAV sin comprimir a 48 kHz; el masculino es MP3 comprimido a 44.1 kHz, uno de ellos a 64 kbps. Para tareas sensibles a calidad de audio, los dos corpus no son comparables en condiciones iguales.

### Procedencia y derechos

Los tres archivos masculinos llevan el prefijo `ssstik.io_`, identificador de un servicio de descarga de TikTok. **No existe documentación de consentimiento, licencia ni derechos de uso** para ninguna de las seis muestras de voz, ni para los nueve videos de referencia. No se infiere ningún derecho de uso: esta auditoría solo registra la ausencia de documentación.

### Muestra representativa seleccionada

**Female (2):** `…10.02.19-PM-_1_.wav` (95.3 s) y `…10.01.37-PM.wav` (58.5 s) — las dos de mayor duración, procedentes de videos distintos.

**Male (2):** `ssstik.io_1788494482734.mp3` (47.5 s) y `ssstik.io_1788494597329.mp3` (22.0 s) — ambos a 128 kbps, descartando el de 64 kbps por calidad inferior.

*No se han generado Voice Profiles.*

---

## 9. File Quality / Duplicate Findings

### Duplicados exactos
Ninguno. Los 29 archivos producen 29 hashes MD5 únicos.

### Nombres de archivo colisionantes (contenido distinto)
- `WhatsApp Video 2026-09-03 at 10.02.19 PM.mp4` vs `… PM (1).mp4` en `ugc/` — archivos distintos con sufijo de colisión de descarga.

### Inconsistencias de nomenclatura
- `modulo-5-infraestructura-herramientas (1).md` conserva un sufijo `(1)` de descarga. No existe una versión sin sufijo; rompe la simetría con los módulos 1–4.
- Los archivos multimedia conservan nombres autogenerados de WhatsApp y de ssstik.io. No son descriptivos del contenido ni del criterio de clasificación.
- Convención mixta en `samples/`: los MP4 usan espacios, los WAV usan guiones para el mismo identificador base.
- `knowledge/methodology/` mezcla `kebab-case` (módulos MD) con títulos en prosa con espacios y guion bajo (PDFs).

### Archivos vacíos o de tamaño nulo
Ninguno.

### Extensiones inusuales
Ninguna. Todas las extensiones (`.md`, `.pdf`, `.mp4`, `.wav`, `.mp3`) corresponden al contenido real verificado por cabecera.

### Carpetas vacías
- `knowledge/copywriting/schwartz/` — vacía; su contenido esperado está un nivel arriba.
- `sources/methodology/` — vacía; su contenido esperado está en `knowledge/methodology/`.

### Archivos en ubicaciones inesperadas
- Los tres PDFs metodológicos en `knowledge/methodology/` son fuentes originales, no conocimiento reestructurado.
- Los tres documentos Schwartz en `knowledge/copywriting/` en lugar de `knowledge/copywriting/schwartz/`.

### Carpetas duplicadas anidadas
Ninguna, más allá de la relación `copywriting/` ↔ `copywriting/schwartz/` descrita arriba.

*No se ha corregido nada. Todo queda registrado sin intervención.*

---

## 10. Missing or Unexpected Sources

### Ausencias

| Elemento | Situación | Impacto |
|---|---|---|
| `sources/methodology/` | Vacía. Ningún documento fuente metodológico crudo. | No bloqueante — el conocimiento derivado está completo. |
| Capa de texto en *The Brilliance Breakthrough* | PDF escaneado, 0 caracteres extraíbles. | No bloqueante — el conocimiento derivado ya existe y declara la limitación. |
| Corpus de referencias numeradas de los módulos | Marcadores de cita presentes, fuentes no incluidas. | No bloqueante — el contenido es autosuficiente. |
| Documentación de derechos/consentimiento de voz y video | Inexistente. | No bloqueante para el diseño; relevante antes de cualquier uso productivo. |
| Metadatos de los samples (hablante, región, contexto) | Inexistentes. | No bloqueante — a resolver en la fase de perfilado. |

### Presencias inesperadas

- Repositorio git ya inicializado con un commit de baseline. No estaba especificado, pero es beneficioso: existe un punto de restauración previo a cualquier reorganización.
- Los tres PDFs metodológicos dentro de `knowledge/` en lugar de `sources/`.

---

## 11. Project Tree

```
creative-experimentation-os/
├── README.md
├── PRE_FLIGHT_AUDIT.md                      (este documento)
│
├── sources/
│   ├── methodology/                          [VACÍA]
│   └── original-books/
│       ├── breakthrough-advertising-…_compressed.pdf      239 pp · READABLE
│       └── _OceanofPDF.com_The_brilliance_breakthrough…pdf 149 pp · UNREADABLE (escaneo)
│
├── knowledge/
│   ├── methodology/
│   │   ├── modulo-1-estrategia-mercado.md                  READABLE
│   │   ├── modulo-2-psicologia-persuasion.md               READABLE
│   │   ├── modulo-3-anuncios-estaticos.md                  READABLE
│   │   ├── modulo-4-ugc-vsl-strategy.md                    READABLE
│   │   ├── modulo-5-infraestructura-herramientas (1).md    READABLE
│   │   ├── Metodología Evolve para Testeo Creativo….pdf    2 pp · READABLE
│   │   ├── Escalamiento Creativo y Prueba Social….pdf      2 pp · READABLE
│   │   └── Dominio del Post ID_ Escalamiento….pdf          2 pp · READABLE
│   └── copywriting/
│       ├── schwartz_persuasion_framework.md                READABLE   ← esperado en schwartz/
│       ├── schwartz_language_engine.md                     READABLE   ← esperado en schwartz/
│       ├── schwartz_integration_map.md                     READABLE   ← esperado en schwartz/
│       └── schwartz/                                       [VACÍA]
│
└── samples/
    ├── style-references/
    │   ├── ugc/         3 × MP4   58.5s · 75.0s · 95.3s
    │   ├── podcast/     3 × MP4   30.8s · 47.7s · 68.0s
    │   └── animation/   3 × MP4   40.7s · 50.0s · 67.9s
    └── voices/
        └── chile/
            ├── female/  3 × WAV   58.5s · 74.8s · 95.3s   ← audio extraído de ugc/
            └── male/    3 × MP3   22.0s · 33.3s · 47.5s   ← origen ssstik.io
```

---

## 12. Readiness Matrix

| Dimensión | Estado | Justificación |
|---|---|---|
| **METHODOLOGY_READY** | **PASS** | Los 8 dominios cubiertos. 5 módulos MD + 3 PDFs, todos legibles, sin corrupción ni problemas de encoding. |
| **SCHWARTZ_READY** | **PASS_WITH_WARNINGS** | Los 3 documentos presentes, íntegros y legibles. Ubicados en `knowledge/copywriting/` en lugar de `knowledge/copywriting/schwartz/`. |
| **VIDEO_SAMPLE_READY** | **PASS** | 9 MP4 válidos, 3 por categoría, sin duplicados ni corrupción. Muestra representativa seleccionable. |
| **VOICE_SAMPLE_READY** | **PASS_WITH_WARNINGS** | 6 archivos válidos y accesibles. El corpus femenino no es independiente de las referencias UGC; asimetría técnica entre corpus; sin documentación de derechos; etiquetas de género no verificadas. |
| **SOURCE_TRACEABILITY_READY** | **PASS_WITH_WARNINGS** | `Breakthrough Advertising` trazable y verificable. `The Brilliance Breakthrough` presente pero no verificable automáticamente (escaneo sin OCR). `sources/methodology/` vacía y PDFs fuente alojados en `knowledge/`. |

---

## 13. Critical Blockers

**NINGUNO.**

Ningún hallazgo impide comenzar PHASE 1 — FINAL AUDIT + SYSTEM DESIGN.

Criterio aplicado: un problema es crítico solo si el material necesario para diseñar el sistema está ausente, es inaccesible o es inutilizable. En este proyecto, todo el conocimiento estructurado es legible, los 8 dominios metodológicos están cubiertos, y existen muestras válidas y suficientes de video y voz en las tres categorías de estilo y los dos géneros.

Las discrepancias detectadas son de **ubicación, procedencia y nomenclatura**, no de disponibilidad.

---

## 14. Non-Blocking Warnings

| # | Advertencia | Ubicación | Momento recomendado de resolución |
|---|---|---|---|
| W1 | Documentos Schwartz fuera de `knowledge/copywriting/schwartz/`; la carpeta esperada está vacía. | `knowledge/copywriting/` | Phase 1 — decisión de estructura. |
| W2 | Los 3 samples de voz femenina son audio extraído de los 3 videos UGC, no fuentes independientes. Riesgo de validación circular entre Style Profile UGC y Voice Profile femenino. | `samples/voices/chile/female/` | Antes de generar Voice Profiles. |
| W3 | `sources/methodology/` vacía; los PDFs metodológicos originales residen en `knowledge/methodology/`, mezclando fuente cruda con conocimiento estructurado. | `sources/` ↔ `knowledge/` | Phase 1 — decisión de estructura. |
| W4 | *The Brilliance Breakthrough* es un escaneo de 149 páginas sin capa de texto. El conocimiento derivado en `schwartz_language_engine.md` no puede reverificarse automáticamente contra su fuente. Limitación ya declarada en el propio documento. | `sources/original-books/` | Solo si se requiere reverificación automática. |
| W5 | Sin documentación de consentimiento, licencia ni derechos de uso para las 6 muestras de voz ni los 9 videos. Los MP3 masculinos provienen de un descargador de TikTok. | `samples/` | Antes de cualquier uso productivo. |
| W6 | Asimetría técnica entre corpus de voz: femenino WAV 48 kHz sin comprimir vs masculino MP3 44.1 kHz, uno de ellos a 64 kbps. | `samples/voices/chile/` | Antes de análisis acústico comparativo. |
| W7 | Inconsistencias de nomenclatura: sufijos `(1)` residuales, nombres autogenerados no descriptivos, convenciones mixtas entre carpetas. | Transversal | Phase 1 — convención de nombres. |

---

## 15. Overall Pre-Flight Status

# PASS WITH WARNINGS

**Critical blockers:** 0
**Non-blocking warnings:** 7
**Archivos auditados:** 29
**Archivos ilegibles:** 1 (fuente escaneada, con conocimiento derivado ya disponible y limitación declarada)
**Archivos corruptos o vacíos:** 0
**Duplicados exactos:** 0

**PHASE 1 — FINAL AUDIT + SYSTEM DESIGN está habilitada para comenzar.**

Las siete advertencias deben trasladarse a Phase 1 como entradas de decisión, no como trabajo de corrección previo. Tres de ellas (W1, W3, W7) son decisiones de estructura que Phase 1 debería resolver por diseño en lugar de parchear ahora. W2 y W6 condicionan el diseño del subsistema de voz. W4 y W5 son restricciones a documentar, no defectos a reparar.

---

*Auditoría de solo lectura. No se modificó, movió, renombró ni eliminó ningún archivo del proyecto. El único archivo creado es este informe.*
