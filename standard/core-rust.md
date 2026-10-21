---
type: Engineering Standard
title: Core Rust
description: Type-driven, compiler-first Rust engineering.
tags: [rust, types, traits, ownership]
---

# Core Rust

## REAS-RUST-001 — Make invariants explicit
Use newtypes, private fields, smart constructors, `Option`, `Result`, and exhaustive enums to express domain constraints. Do not expose unchecked mutation that can invalidate a domain value.

## REAS-RUST-002 — Use zero-cost abstractions deliberately
Prefer concrete types, iterators, borrowing, and static dispatch where they make behavior clearer. Generics, trait objects, cloning, and allocations are allowed when justified. Do not optimize away useful abstractions only to shorten compilation.

## REAS-RUST-003 — Keep trait relationships coherent
Use blanket implementations only when behavior applies universally to the bounded types. Verify coherence, orphan rules, overlap, and method ambiguity. Avoid generic trait mazes and speculative repository frameworks.

## REAS-RUST-004 — Make ownership explicit
Prefer obvious ownership and scoped borrowing. Do not default to `Arc<Mutex<T>>`. Never add `unsafe` to bypass the borrow checker. Prefer a simpler data model to fragile lifetime relationships.

## REAS-RUST-005 — Handle errors explicitly
Use typed errors and `Result`; use `?` for propagation. Reserve panics for genuine programming errors. Avoid arbitrary `unwrap` and silent default values for missing required inputs.

## REAS-RUST-006 — Compile incrementally
Run `cargo fmt --all`, `cargo check --workspace --all-targets`, `cargo clippy --workspace --all-targets -- -D warnings`, and `cargo test --workspace` as appropriate. Report only executed checks. If a remote runner is constrained, compile locally; compilation speed is not a design objective.
