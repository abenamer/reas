---
type: Audit Report
title: REAS self-audit
description: Evidence and limits of the project's self-compliance checks.
tags: [quality, documentation, audit]
---

# REAS self-audit

**Status:** Structural validation, Rust example tests, and GitHub Actions pass. The formal ASD-STE100 review has not been done.

Each row reports one of three outcomes, as [REAS-TEST-002](validation.md) requires: passed, failed, or not run. "Passed" names the date and the commit or run. All "passed" rows below refer to the same evidence: a local run on 2026-10-23 with Rust 1.97.0 stable and Python 3, and GitHub Actions run 5 on branch `claude/zen-newton-74jyn8` at commit `43f1d1a`, which is the first run that contained the current examples and checker. Earlier runs on `main` tested earlier versions of the code and are not cited.

| Requirement | Check | Outcome |
| --- | --- | --- |
| OKF v0.2 concept frontmatter | `scripts/check_docs.py` | Passed. |
| Bundle index present with `okf_version: "0.2"` | `scripts/check_docs.py` | Passed. The presence check was added at `43f1d1a`. Before that commit the checker validated the index only when the file existed. |
| Unique rule identifiers | `scripts/check_docs.py` | Passed. |
| Local Markdown links | `scripts/check_docs.py` | Passed. External URLs are not checked. |
| Checker unit tests, seven cases | `python -m unittest discover -s tests` | Passed. |
| Typestate example: one unit test, one doctest, two `compile_fail` doctests | `cargo test` in `examples/typestate/` | Passed. Stable rustdoc does not check the pinned error codes, so the `compile_fail` tests prove that the snippets do not compile, not why. |
| In-memory adapter example, seven unit tests | `cargo test` in `examples/ports-and-adapters/` | Passed. The adapter is a `HashMap`. No database adapter is tested. |
| `cargo fmt --check` and `cargo clippy -D warnings` on both examples | `.github/workflows/docs.yml` | Passed. |
| Consistent technical terminology | `standard/terminology.md` | Not run. The table exists. No reviewer has checked every rule against it. |
| ASD-STE100 Issue 9 language rules | Review against the authorized standard | Not run. |

Structural validation does not prove STE compliance or engineering quality. Update this audit after each release or major documentation change.
