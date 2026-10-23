---
type: Engineering Standard
title: State machines and typestate
description: Runtime state enums, typestate, and guarded persisted transitions.
tags: [rust, fsm, typestate]
---

# State machines and typestate

## REAS-STATE-001 — Model runtime states
Use one enum for a set of mutually exclusive states. Do not encode that set with several Boolean flags. Write each legal transition as a function from one state to the next. Match on the enum without a wildcard arm.

## REAS-STATE-002 — Use typestate where it helps
Use typestate to reject invalid operations at compile time, for example a build step called out of order or a resource used before initialization. Bound the state parameter with a sealed trait so the set of states is closed. Keep the number of state parameters small. Use a runtime enum when the state comes from a file, a database, or a network. The compiler cannot know that state.

## REAS-STATE-003 — Guard persisted transitions
A persisted state can change between a read and a write. Guard each transition with a conditional update, for example `UPDATE ... WHERE state = $expected`, or with a row lock, for example `SELECT ... FOR UPDATE`. Typestate alone cannot prevent a stale read or a lost update.

See the [typestate example](../examples/typestate/).
