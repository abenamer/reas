---
type: Technical Reference
title: REAS terminology
description: Project-specific technical terms for consistent documentation.
tags: [terminology, rust, ste]
---

# REAS technical terminology

These are project-specific technical terms, not a reproduction of the ASD-STE100 approved dictionary. A reviewer must check terms against the official issue before claiming compliance.

| Term | Meaning |
| --- | --- |
| Adapter | Concrete implementation that translates between an external system and a port. |
| Application use case | Operation that coordinates domain behavior and external dependencies. |
| Blanket implementation | Trait implementation that applies to all types satisfying its bounds. |
| Borrow | Temporary reference to a value without transfer of its ownership. |
| Cargo | Standard Rust build and package tool. |
| Crate | Rust compilation unit. |
| Domain | Types, invariants, and rules independent of infrastructure. |
| Finite-state machine | Defined states with permitted transitions. |
| Hexagonal architecture | Architecture that separates application core from adapters through ports. |
| Lifetime | Rust property that constrains how long references remain valid. |
| Newtype | Distinct type wrapping another type to express a semantic distinction. |
| OKF | Open Knowledge Format, a convention for linked Markdown knowledge. |
| Ownership | Rust responsibility for the lifetime of a value. |
| Port | Application-defined interface required from an adapter. |
| SQLx | Rust database library. |
| Typestate | Encoding permitted operations using types that represent state. |
| Zero-cost abstraction | Abstraction intended to have no additional runtime cost relative to equivalent lower-level code. |
