# Rust examples

Each subdirectory is an independent small Cargo package.

- [Ports and adapters](ports-and-adapters/) shows a named repository port, an in-memory adapter, and explicit wiring.
- [Typestate](typestate/) shows a legal transition plus a compile-fail doctest.

To validate when Cargo is installed:

```bash
cargo test --manifest-path examples/ports-and-adapters/Cargo.toml
cargo test --manifest-path examples/typestate/Cargo.toml
```

Source examples are not verified as compiled until the commands run successfully.
