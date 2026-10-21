---
type: Engineering Standard
title: Documentation and knowledge structure
description: ASD-STE100 writing guidance and OKF v0.2 organization.
tags: [documentation, asd-ste100, okf]
sources:
  - id: ste
    resource: https://www.asd-ste100.org/
    title: ASD-STE100 official site
  - id: okf
    resource: https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md
    title: OKF v0.2 specification
---

# Documentation and knowledge structure

## REAS-DOC-001 — Target ASD-STE100
Write procedural and reference documentation with controlled terminology, direct steps, and clear grammar. Consult the official Issue 9 rules and approved vocabulary for compliance. Clear language alone does not establish compliance.

## REAS-DOC-002 — Keep an OKF knowledge bundle
Use Markdown and valid YAML frontmatter for concept files under `standard/`. Every concept requires `type`. Maintain a navigable `index.md` with `okf_version: "0.2"`. Keep local links valid, sources attributable, and generated or verified metadata factual.

## REAS-DOC-003 — Define technical terms
Use the [project terminology list](terminology.md) for precise Rust and architecture terms. Keep code identifiers, commands, and paths unchanged. Do not replace precise technical terms with inaccurate synonyms.

## REAS-DOC-004 — Document while implementing
Update domain, architecture, API, operation, and decision documents with the relevant code change. Keep instructions reproducible. Provide prerequisites, ordered steps, expected results, and recovery instructions where needed.

## REAS-DOC-005 — Validate independently
Run structural OKF, metadata, rule identifier, and link checks. Record STE language review separately. Automated structural validity does not prove technical accuracy or full STE compliance.
