# Rust examples

Each subdirectory is an independent small Cargo package.

- [Ports and adapters](ports-and-adapters/) shows the full path from a CLI inbound adapter, through a use case and a port trait, to an in-memory outbound adapter. One composition root connects them. The domain uses a smart constructor, and the port returns a typed error.
- [Typestate](typestate/) shows a legal transition, a sealed state trait, and two `compile_fail` doctests with pinned error codes.

Run the tests, lints, and format check:

```bash
cargo test --manifest-path examples/ports-and-adapters/Cargo.toml
cargo test --manifest-path examples/typestate/Cargo.toml
cargo clippy --manifest-path examples/ports-and-adapters/Cargo.toml --all-targets -- -D warnings
cargo clippy --manifest-path examples/typestate/Cargo.toml --all-targets -- -D warnings
cargo fmt --manifest-path examples/ports-and-adapters/Cargo.toml --all -- --check
cargo fmt --manifest-path examples/typestate/Cargo.toml --all -- --check
```

Stable rustdoc accepts the error code after `compile_fail` but does not check it. Only nightly rustdoc fails the doctest when the code differs.

The [self-audit](../standard/self-audit.md) records when these commands last passed.
