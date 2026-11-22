---
type: Audit Report
title: REAS self-audit
description: Current evidence that this repository meets its own checks, and one line per earlier revision.
tags: [quality, documentation, audit]
updated: 2026-11-22
---

# REAS self-audit

**Status: local checks passed on 2026-11-22 for the 1.9.0-draft worktree. Remote evidence for its commit is recorded below once the pull request checks run.**

This audit is an instrument reading, as [REAS-FOUND-005](foundations.md#reas-found-005) specifies.
It holds the current revision's evidence and one line per earlier revision.
Each row reports one of the six outcomes of [REAS-TEST-002](validation.md#reas-test-002).
The language review does not establish full ASD-STE100 compliance; see the [language-review record](ste-review.md).

## Current revision

| Check | Outcome | Evidence |
| --- | --- | --- |
| `scripts/check.sh docs`: documentation checker | Passed | PASS line; rule shape including Limits; zero freshness warnings |
| `scripts/check.sh docs`: checker unit tests | Passed | 62 tests, 0 failed, 0 skipped |
| `scripts/check.sh rust`: adapter example | Passed | check, 12 unit tests, Clippy, rustfmt, doc build |
| `scripts/check.sh rust`: typestate example | Passed | check, 3 unit tests, 4 doctests, Clippy, rustfmt, doc build |
| `scripts/check.sh rust`: trust-boundary example | Passed | check, 29 unit tests, 3 doctests, Clippy, rustfmt, doc build |
| `scripts/check.sh rust`: fuzz crate Clippy and rustfmt | Passed | stable toolchain |
| Mutation pass, trust-boundary example: `cargo mutants` | Passed | 69 mutants in 21 s: 52 killed, 16 unviable, 1 accepted survivor (`MAX_PAYLOAD_LEN`, non-contractual configuration, noted at the constant). The test double is excluded by `.cargo/mutants.toml`; its acceptance and rejection paths have their own tests. |
| `scripts/check.sh nightly`: expected diagnostic codes and the 30-second fuzz run | Not run locally this revision | No code under the nightly job changed; the CI job runs it on the pushed commit. |
| MSRV `cargo +1.88.0 check` | Not run locally this revision | No manifest or code outside tests changed; the `msrv` CI job runs it. |
| Differential tests on aarch64 | Not run locally | The `rust-examples-arm64` CI job runs them. |
| `cargo deny check`, `cargo vet check` | Not run | Not installed; the examples are not applications under REAS-SEC-001's scope. |
| Miri | Not run | Every example forbids `unsafe`; no native path exists. |
| ASD-STE100 language review of the 1.9.0-draft text | Not run | See the review record. |

## Path-to-job coverage

[REAS-DOC-006](documentation.md#reas-doc-006) forbids a zero-gated path.
Every job runs one subcommand of `scripts/check.sh`.

| Path group | Job | Check |
| --- | --- | --- |
| `standard/**`, root `*.md`, `templates/**` | `docs` | frontmatter, index reachability, rule shape and Limits, quality tests, retired terms, links, freshness |
| `scripts/check_docs.py`, `tests/**`, `requirements-docs.txt` | `docs` | the checker's unit tests, with a planted violation for each gate |
| `examples/*/src/**`, `examples/*/Cargo.toml`, `examples/*/Cargo.lock` | `rust-examples`, `rust-examples-arm64`, `msrv` | check, test, Clippy, rustfmt, doc build with warnings denied, on x86_64, aarch64, and Rust 1.88.0 |
| `examples/trust-boundary/fuzz/**` | `rust-examples`, `nightly-doctests` | Clippy and rustfmt on stable; build and a 30-second run on nightly |
| `examples/trust-boundary/.cargo/mutants.toml` | none | Read only by a local `cargo mutants` run; not a CI gate by design under REAS-TEST-001. |
| Compile-fail doctests | `nightly-doctests` | expected diagnostic codes asserted |
| Native paths | `rust-examples` | zero by construction: every example sets `unsafe_code = "forbid"`, no FFI, no CPU-gated path |
| `scripts/check.sh` | every job | a defect in the script fails every job |
| `.github/workflows/docs.yml` | none beyond its own execution | a syntax error fails every job; a wrong step name does not |
| `LICENSE-*`, `.gitignore`, `rust-toolchain.toml` | none | not asserted |

## Earlier revisions

Each line names the version, the Actions run that tested its implementation commit, and the outcome.
The run pages and Git history hold the per-job detail.

| Version | Run | Commit | Outcome |
| --- | --- | --- | --- |
| 1.8.0-draft | [run 28](https://github.com/abenamer/reas/actions/runs/45064945526) | `64bdf70` | Passed, five jobs |
| 1.7.0-draft | [run 24](https://github.com/abenamer/reas/actions/runs/44831443937) | `843b94d` | Passed, five jobs |
| 1.6.0-draft | [run 20](https://github.com/abenamer/reas/actions/runs/44820161148) | `f208fb5` | Passed, five jobs; first MSRV job |
| 1.5.0-draft | [run 16](https://github.com/abenamer/reas/actions/runs/44304113162) | `73ebe1d` | Passed, four jobs; first aarch64 and fuzz jobs |
| 1.4.0-draft | [run 11](https://github.com/abenamer/reas/actions/runs/39995381881) | `d746f9a` | Passed, three jobs |
| 1.3.0-draft | [run 9](https://github.com/abenamer/reas/actions/runs/39990157419) | `63c9434` | Passed, two jobs |

## Limits

The [checker reference](checker.md) states the supported structural checks.
Its metadata checks do not establish the truth of verification claims.
Stable rustdoc does not assert expected error codes; nightly rustdoc asserts their presence, not the absence of extra diagnostics.
The mutation pass establishes that one test distinguishes the code from each killed mutant; it says nothing about defects no mutation operator produces.
Historical identifier reuse requires review of [the identifier record](rule-identifiers.md).
