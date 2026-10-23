---
type: Engineering Standard
title: Core Rust
description: Type-driven Rust engineering rules.
tags: [rust, types, traits, ownership, async]
---

# Core Rust

## REAS-RUST-001 — Make invariants explicit
Use newtypes with private fields and smart constructors for domain values. Use `Option` for a value that can be absent. Use `Result` for an operation that can fail. Use an enum whose variants are exactly the legal cases, and match on it without a wildcard arm. Do not expose a public field or a setter that can make a domain value invalid.

## REAS-RUST-002 — Choose abstractions for clarity first, then check their cost
Choose the abstraction that makes the behavior clearest to a reader. Then check its runtime cost. Generics and `impl Trait` give static dispatch and have no runtime cost. Trait objects give dynamic dispatch. `Box<dyn Trait>` also adds a heap allocation; `&dyn Trait` does not. Cloning and allocation add cost. Use a costed option when it makes the code clearer, and write the reason in a comment. Do not remove a useful abstraction to shorten compilation.

## REAS-RUST-003 — Keep trait relationships simple
Write a blanket implementation only when the behavior is correct for every type that meets the bounds. Design so that the orphan rule and overlapping implementations do not block a later change. Do not give a type an inherent method with the same name as a trait method. The inherent method takes priority, and the compiler does not warn. Do not build a generic repository framework before a second concrete implementation exists.

## REAS-RUST-004 — Keep ownership obvious
Give each value one obvious owner. Borrow for short scopes. Do not use `Arc<Mutex<T>>` as a default. Never use `unsafe` to bypass the borrow checker. If lifetime annotations become hard to read, change the data model.

## REAS-RUST-005 — Handle errors explicitly
Return `Result` with a typed error from each operation that can fail. Propagate with `?`. Panic only for a bug, for example when an invariant that this crate already checked turns out to be false. Do not call `unwrap` on an `Option` or `Result` that can be `None` or `Err` at run time. When it cannot be `None` or `Err` at that point, use `expect` with a message that states why. Do not substitute a default value for a required input that is missing.

## REAS-RUST-006 — Compile after each small change
Run `cargo fmt --all`, `cargo check --workspace --all-targets`, `cargo clippy --workspace --all-targets -- -D warnings`, and `cargo test --workspace` when Cargo is available. Report only the checks that ran. If the hosted build cannot run Cargo, compile locally. Compilation speed is not a design objective.

## REAS-RUST-007 — Separate async work and CPU work
Do not run a long blocking computation on an async executor thread. Move it to `spawn_blocking`, a Rayon pool, or a bounded worker pool. Do not hold a `std::sync::Mutex` guard across an `.await`. Decide how each task stops on cancellation and on shutdown, and write that decision down.
