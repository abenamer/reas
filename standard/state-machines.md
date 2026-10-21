---
type: Engineering Standard
title: State machines and typestate
description: Runtime states, typestate and transactional transitions.
tags: [rust, fsm, typestate]
---

# State machines and typestate

## REAS-STATE-001 — Model runtime states
Use enums for mutually exclusive workflow states. Define legal transitions explicitly and use exhaustive matching. Do not represent one state with unrelated Boolean flags.

## REAS-STATE-002 — Use typestate where it helps
Use typestate to prevent invalid compile-time operations, including staged construction and resource initialization. Keep type parameters understandable. Prefer a runtime enum for externally loaded or persisted state.

## REAS-STATE-003 — Protect persisted transitions
Enforce concurrent transitions with atomic database updates or transactions. Typestate alone cannot prevent stale reads or races.

See the [typestate example](../examples/typestate/).
