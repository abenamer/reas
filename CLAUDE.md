# Claude instructions

Start at [standard/index.md](standard/index.md).
Apply the rules for the current task.

1. Identify domain invariants and legal states.
2. Use visible ports, named adapters, and one composition root for each executable.
3. For private projects, use [REAS-ARCH-003](standard/ports-and-adapters.md#reas-arch-003) before you select the architecture.
4. Record the project service life, not the duration of one execution.
5. Select idiomatic Rust and compiler safety before compilation speed.
6. If the hosted build cannot run Cargo, compile locally.
7. Run `cargo fmt`, `cargo check`, `cargo clippy`, and `cargo test` after each implementation step.
8. Update [project documentation](standard/documentation.md) with the code.
9. Use the [terminology table](standard/terminology.md).
10. Run `python scripts/check_docs.py` and `python -m unittest discover -s tests -v`.
11. Record the ASD-STE100 Issue 9 review separately from structural checks.
12. Do not claim passing tests or full language compliance without evidence.
