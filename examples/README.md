# Rust examples

Each subdirectory is an independent Cargo package.
The examples commit `Cargo.lock` and use the root `rust-toolchain.toml`.

- [Ports and adapters](ports-and-adapters/) includes a CLI command function, use case, port trait, and in-memory outbound adapter.
  One composition root connects them.
  The tests include input boundaries, missing records, and repository failures.
- [Typestate](typestate/) includes two legal transitions and a sealed state trait.
  Three compile-fail doctests cover an invalid operation, an invalid state argument, and an attempted downstream state implementation.
- [Trust boundary](trust-boundary/) includes one inbound adapter that parses a length-prefixed frame with checked arithmetic, verifies its origin through a port before it parses the payload, and decodes a validated event type through serde `try_from`.
  A verification state makes the handler reject an unverified webhook at compile time.
  A SWAR checksum duplicates a scalar reference, with a differential test.
  The manifest forbids `unsafe`, denies unchecked arithmetic and indexing, and enables overflow checks in release.
  The `fuzz/` subcrate holds one libFuzzer target with a seed corpus.

The CLI example returns rendered text from a library function.
A CLI executable must also set the exit status for a failed command.
The examples do not include a database adapter, persisted transitions, transaction ownership, an async port, a message authentication code, output encoding, or a dependency scan.

Run the stable checks:

```bash
cargo check --locked --manifest-path examples/ports-and-adapters/Cargo.toml --all-targets
cargo check --locked --manifest-path examples/typestate/Cargo.toml --all-targets
cargo check --locked --manifest-path examples/trust-boundary/Cargo.toml --all-targets
cargo test --locked --manifest-path examples/ports-and-adapters/Cargo.toml
cargo test --locked --manifest-path examples/typestate/Cargo.toml
cargo test --locked --manifest-path examples/trust-boundary/Cargo.toml
cargo clippy --locked --manifest-path examples/ports-and-adapters/Cargo.toml --all-targets -- -D warnings
cargo clippy --locked --manifest-path examples/typestate/Cargo.toml --all-targets -- -D warnings
cargo clippy --locked --manifest-path examples/trust-boundary/Cargo.toml --all-targets -- -D warnings
cargo fmt --manifest-path examples/ports-and-adapters/Cargo.toml --all -- --check
cargo fmt --manifest-path examples/typestate/Cargo.toml --all -- --check
cargo fmt --manifest-path examples/trust-boundary/Cargo.toml --all -- --check
```

Stable rustdoc tests that a `compile_fail` snippet does not compile.
It does not test the expected error code.
The nightly job also tests the expected diagnostic codes:

```bash
rustup toolchain install nightly-2026-10-23 --profile minimal
cargo +nightly-2026-10-23 test --locked --manifest-path examples/typestate/Cargo.toml --doc
```

Nightly rustdoc fails a doctest when an expected error code is absent.
It can accept extra diagnostics.

Run the fuzz target with the pull-request budget from REAS-TEST-003:

```bash
cargo +nightly-2026-10-23 install cargo-fuzz --locked
cd examples/trust-boundary
cargo +nightly-2026-10-23 fuzz build receive
cargo +nightly-2026-10-23 fuzz run receive -- -max_total_time=30
```

The run reads the seed corpus in `fuzz/corpus/receive/` and writes new inputs there.
CI discards those inputs; a project that deploys the code must persist them.
The [self-audit](../standard/self-audit.md) identifies the code revision and commands for each recorded result.
