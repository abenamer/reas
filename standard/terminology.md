---
type: Technical Reference
title: REAS terminology
description: Project-specific technical terms for consistent documentation.
tags: [terminology, rust, ste]
---

# REAS technical terminology

These are project-specific technical terms. They are not a reproduction of the ASD-STE100 approved dictionary. A reviewer must check terms against the official issue before claiming compliance.

Rules in this standard use these terms with these meanings. When a rule uses a term that is not in this table, add the term here.

| Term | Meaning |
| --- | --- |
| Adapter | Concrete type that translates between an external system and the application. An inbound adapter calls a use case. An outbound adapter implements a port. |
| Application use case | Operation that coordinates domain behavior and the ports it needs. |
| Blanket implementation | Trait implementation for every type that meets its bounds, for example `impl<T: Display> Describe for T`. |
| Borrow | Shared (`&T`) or exclusive (`&mut T`) reference to a value. A borrow does not transfer ownership. |
| Cargo | Standard Rust build and package tool. |
| Coherence | Compiler rule that permits at most one implementation of a trait for a type. The orphan rule is part of coherence. |
| Composition root | The one place that constructs adapters and use cases and connects them. In a binary crate this is `main` or a function that `main` calls. |
| Crate | Rust unit of compilation and linking. |
| Domain | Types, invariants, and rules that do not depend on infrastructure. |
| Dynamic dispatch | Method selection at run time through a trait object. |
| Finite-state machine | A finite set of states, exactly one current state, and a defined set of permitted transitions. |
| Forwarding layer | A type or function that only calls another with the same arguments and adds no behavior. |
| Hexagonal architecture | Architecture that separates the application core from adapters through ports. REAS uses "ports and adapters" for the same idea. |
| Hosted build | A build that runs on a machine the developer does not control, for example a CI runner or an agent sandbox. |
| Human-maintained code | Code that people read, change, and review. REAS contrasts it with code that only an automated agent maintains. |
| Inbound adapter | Adapter that receives input from outside the application and calls a use case. Examples: an HTTP handler, a CLI command. |
| Lifetime | A named region of code for which a reference is valid. The borrow checker verifies that each use of the reference is inside that region. A lifetime is a generic parameter, not a runtime value. |
| Newtype | Distinct type that wraps one other type to give it a separate meaning, for example `struct TeamId(u32)`. |
| OKF | Open Knowledge Format, a convention for linked Markdown knowledge. |
| OKF concept | One Markdown file in the OKF bundle. Its YAML frontmatter includes `type`. |
| Orphan rule | Compiler rule: a crate can implement a trait for a type only if the crate defines the trait or the type. |
| Outbound adapter | Adapter that implements a port and calls an external system. Examples: a PostgreSQL repository, an HTTP client. |
| Ownership | The rule that each value has exactly one owner. When the owner goes out of scope, Rust drops the value. |
| Port | Trait that the application defines for a dependency it needs. An outbound adapter implements the port. REAS uses "port" for the outbound side only. For the inbound side, REAS uses "use case". |
| Smart constructor | Function that checks its input and returns a valid domain value or an error. The type's fields are private, so the smart constructor is the only way to make the value. |
| SQLx | Async Rust SQL library. It can check queries against a database at compile time. |
| Static dispatch | Method selection at compile time through generics or `impl Trait`. The compiler makes one copy of the code for each concrete type. |
| Trait object | A `dyn Trait` value. Calls through it use dynamic dispatch. |
| Typed error | An error enum or struct that the caller can match on. `Box<dyn Error>` and `anyhow::Error` are not typed errors in REAS. |
| Typestate | Encoding the state of a value in its type. An operation that is invalid in a state does not compile. |
| Zero-cost abstraction | Abstraction that has no additional runtime cost relative to equivalent lower-level code. The term says nothing about readability or compile time. |
