# Canonical Store

This directory is the canonical system-of-record root.

Canonical source-manifest inputs under this root are:
- *.json entity and artefact records
- *.jsonl event logs

README and other non-JSON documentation are not canonical manifest inputs.

Directories are created only when they contain real records; empty entity-scope
trees are not scaffolded in advance.

Versioned artefacts use v<n>.json files. There is no mutable "latest" file.
