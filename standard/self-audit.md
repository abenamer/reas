---
type: Audit Report
title: REAS self-audit
description: Revision-specific validation evidence and remaining limitations.
tags: [quality, documentation, audit]
---

# REAS self-audit

**Recorded validation: local checks passed on 2026-11-18 for the 1.5.0-draft worktree. Remote evidence for its commit is pending until the pull request checks run.**

The language review does not establish full ASD-STE100 compliance.
See the [language-review record](ste-review.md) for its scope and open checks.

## Local evidence: 2026-11-18

The local environment uses Python 3, Rust 1.99.1 from `rust-toolchain.toml`, `nightly-2026-10-23`, and cargo-fuzz 0.13.2.
The checks below ran on the 1.5.0-draft worktree before its first commit.
This local result has no immutable source commit and is not release evidence.

| Check | Outcome |
| --- | --- |
| `python scripts/check_docs.py` | Passed locally. |
| `python -m unittest discover -s tests -v` | Passed locally. |
| Adapter example: `cargo check`, `cargo test`, Clippy, rustfmt, all `--locked` | Passed locally, 12 unit tests. |
| Typestate example: same commands | Passed locally, three unit tests and four doctests. |
| Trust-boundary example: same commands | Passed locally, 24 unit tests, one doctest, two compile-fail doctests. |
| Trust-boundary example: nightly `cargo test --locked --doc` | Passed locally. Two compile-fail tests asserted expected diagnostic codes E0308 and E0277. |
| Trust-boundary fuzz target: `cargo fuzz build receive` | Passed locally on nightly-2026-10-23. |
| Trust-boundary fuzz target: `cargo fuzz run receive -- -max_total_time=30` | Passed locally on x86_64. 5,873,517 executions in 31 seconds from the two seed inputs, no crash, no artifact. The run grew the corpus to 66 inputs; only the two seeds are committed. |
| Fuzz crate: `cargo fmt --all -- --check` | Passed locally. |
| Trust-boundary differential test on aarch64 | Not run locally. The `rust-examples-arm64` workflow job runs it; its first result arrives with the pull request checks. |
| Dependency scan with `cargo deny` or `cargo audit` | Not run. Neither tool is installed in this environment, and the workflow does not yet include the job that REAS-SEC-001 requires. |
| Miri on the examples | Not run. The examples forbid `unsafe`, so REAS-SEC-004 requires no Miri job for them. |
| ASD-STE100 language review of `security.md`, REAS-TEST-003, and the new example | Not run. See the review record. |

## Historical evidence

[Actions run 9](https://github.com/abenamer/reas/actions/runs/39990157419) passed on 2026-10-23 at commit `63c9434d241d899ff9e91258d7584ad85c25a9a6`.
It tested the 1.3.0-draft code on `main`.
Its Rust job used Rust 1.99.1.

That run executed seven Python tests and seven adapter-example unit tests.
It also executed one typestate unit test and three typestate doctests.
Two of those doctests were compile-fail tests.
Formatting and Clippy passed for both examples.
That workflow did not run nightly diagnostic-code assertions or a separate `cargo check` command.

The former audit cited run 5 at `43f1d1a` as current-code evidence.
That run tested the earlier `TeamId(u32)` implementation.
It did not test the subsequent `NonZeroU32` implementation.
Neither historical run verifies the changed code in this revision.

## Local evidence: 2026-10-23

The local environment uses Python 3 and Rust 1.99.1.
The diagnostic-code test uses `nightly-2026-10-23`.
The checks below ran on the implementation worktree before its first commit.
This local result has no immutable source commit and is not release evidence.
The remote evidence section must identify a committed revision before a release.

| Check | Outcome |
| --- | --- |
| `python scripts/check_docs.py` | Passed locally. |
| `python -m unittest discover -s tests -v` | Passed locally, 36 test methods with additional parameterized cases. |
| Adapter example: `cargo test --locked` | Passed locally, 12 unit tests. |
| Typestate example: `cargo test --locked` | Passed locally, three unit tests and four doctests. |
| Typestate example: nightly `cargo test --locked --doc` | Passed locally. Three compile-fail tests include expected diagnostic codes. |
| Both examples: `cargo check --locked --all-targets` | Passed locally. |
| Both examples: `cargo clippy --locked --all-targets -- -D warnings` | Passed locally. |
| Both examples: `cargo fmt --all -- --check` | Passed locally. |
| Complete STE vocabulary and grammar review | Not run in full. See the review record. |
| Database adapter, persisted transitions, and transaction integration tests | Not run. These examples do not contain a database adapter. |

## Remote evidence for this revision

[Actions run 11](https://github.com/abenamer/reas/actions/runs/39995381881) passed on 2026-10-23.
Its source commit is `d746f9adae750e8810a57652878cea83dc465d7b` on `codex/reas-precision-ste-review`.
The job logs were inspected after execution.

| Job | Verified result |
| --- | --- |
| [docs](https://github.com/abenamer/reas/actions/runs/39995381881/job/120557440061) | The structural checker and all 36 Python test methods passed. |
| [rust-examples](https://github.com/abenamer/reas/actions/runs/39995381881/job/120557440283) | Rust 1.99.1 passed Cargo check, tests, formatting, and Clippy for both packages. Adapter tests: 12 passed. Typestate tests: three unit tests and four doctests passed. |
| [nightly-doctests](https://github.com/abenamer/reas/actions/runs/39995381881/job/120557440532) | Rust nightly-2026-10-23 passed four doctests. Three compile-fail tests asserted expected diagnostic codes. |

Run 11 verifies the files at that commit, not subsequent edits.
The follow-up audit and wording edits do not change the checker, tests, example code, lockfiles, or workflow.
Their structural validation ran locally again.
Use the pull request checks for the results of later committed text revisions.

## Limits

The [checker reference](checker.md) states the supported structural checks.
Its metadata checks do not establish the truth of verification claims.
Stable rustdoc does not assert expected error codes.
Nightly rustdoc asserts the presence of expected codes, not the absence of extra diagnostics.
Historical identifier reuse requires review of [the identifier record](rule-identifiers.md).
