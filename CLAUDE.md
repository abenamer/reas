# Claude instructions

Start at [standard/index.md](standard/index.md).
Apply the rules for the current task.
Each rule states its Intent, Enforcement, Scope, Rules, and Verification; read the Scope before you apply it.

## Do

1. Identify domain invariants and legal states.
2. Use visible ports, named adapters, and one composition root for each executable.
3. For private projects, use [REAS-ARCH-003](standard/ports-and-adapters.md#reas-arch-003) before you select the architecture.
4. Record the project service life, not the duration of one execution.
5. Select idiomatic Rust and compiler safety before compilation speed.
6. If the hosted build cannot run Cargo, compile locally.
7. Run `cargo fmt`, `cargo check`, `cargo clippy`, and `cargo test` after each implementation step.
8. Update [project documentation](standard/documentation.md) with the code.
9. Use the [terminology table](standard/terminology.md).
10. For this repository, run `scripts/check.sh all`; it is the one list of checks.
11. Record the ASD-STE100 Issue 9 review separately from structural checks.
12. Report each check as passed, failed, errored, timed out, skipped, or not run, with its evidence.

## Do not

- Do not weaken, skip, retry to green, or delete a failing test before you classify it under [REAS-TEST-005](standard/validation.md#reas-test-005).
- Do not add a prose rule where a check can exist; add the check, as [REAS-DOC-006](standard/documentation.md#reas-doc-006) specifies.
- Do not decide product scope, security exposure, or the architecture of a private project; ask the maintainer.
- Do not claim passing tests or full language compliance without evidence.

## Stop and ask

- When three consecutive approaches do not make a failing check pass, stop and report what you tried.
- When a fix needs a change outside the files the task names, stop and report the scope.
- When a rule and a check disagree, stop and report both; do not change the check to match the rule.
