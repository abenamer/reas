# Claude instructions

Start at [standard/index.md](standard/index.md). Follow relevant rules, not every rule by default.

1. Identify domain invariants and legal states.
2. For public or human-maintained code, prefer explicit ports, named concrete adapters, and transparent composition-root wiring.
3. For private projects, ask concise questions about maintainers, interfaces, lifetime, and readership before recommending hexagonal architecture.
4. Prefer idiomatic Rust and compiler safety to faster compilation. Use local compilation if the hosted build cannot run Cargo.
5. Compile in small increments. Run `cargo fmt`, `cargo check`, `cargo clippy`, and `cargo test` when available.
6. Update [OKF knowledge](standard/documentation.md), use [project terminology](standard/terminology.md), and target ASD-STE100 Issue 9.
7. Run `python scripts/check_docs.py`. Never claim verified STE compliance or passing tests without evidence.
