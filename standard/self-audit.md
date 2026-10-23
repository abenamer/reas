---
type: Audit Report
title: REAS self-audit
description: Evidence and limits of the project's self-compliance checks.
tags: [quality, documentation, audit]
---

# REAS self-audit

**Status:** Structural validation, Rust example tests, and GitHub Actions pass. The formal ASD-STE100 review has not been done.

Each row reports one of three outcomes, as [REAS-TEST-002](validation.md) requires: passed, failed, or not run. "Passed" names the date and the commit or run.

| Requirement | Check | Outcome |
| --- | --- | --- |
| OKF v0.2 concept frontmatter | `scripts/check_docs.py` | Passed locally on 2026-10-23 at commit `43f1d1a`. Passed in GitHub Actions run 5 on `claude/zen-newton-74jyn8` at `43f1d1a`. Passed in GitHub Actions run 4 on `main` at `516a0b6`, 2026-10-21. |
| Bundle index present with `okf_version: "0.2"` | `scripts/check_docs.py` | Passed, same runs. The presence check was added on 2026-10-23. Before that date the checker only validated the index when the file existed. |
| Unique rule identifiers | `scripts/check_docs.py` | Passed, same runs. |
| Local Markdown links | `scripts/check_docs.py` | Passed, same runs. External URLs are not checked. |
| Checker unit tests | `python -m unittest discover -s tests` | Passed locally on 2026-10-23. Passed in run 4 on `main`. |
| Typestate example, including two `compile_fail` doctests | `cargo test` in `examples/typestate/` | Passed locally on 2026-10-23 with Rust 1.97.0 stable. Passed in run 4 on `main`. Stable rustdoc does not check the pinned error codes. |
| In-memory adapter example, seven unit tests | `cargo test` in `examples/ports-and-adapters/` | Passed locally on 2026-10-23 with Rust 1.97.0 stable. Passed in run 4 on `main`. |
| `cargo fmt --check` and `cargo clippy -D warnings` on both examples | `.github/workflows/docs.yml` | Passed locally on 2026-10-23. Passed in run 4 on `main`. |
| Consistent technical terminology | `standard/terminology.md` | Not run. The table exists. No reviewer has checked every rule against it. |
| ASD-STE100 Issue 9 language rules | Review against the authorized standard | Not run. |

Structural validation does not prove STE compliance or engineering quality. Update this audit after each release or major documentation change.
