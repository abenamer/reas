# Changelog

## 1.5.0-draft: 2026-11-18

- Added [Security at seams](standard/security.md): REAS-SEC-002 trust boundaries and validated types, REAS-SEC-003 sizes from outside data with checked arithmetic, REAS-SEC-004 confined unsafe code, REAS-SEC-005 duplicate implementations against a reference, and REAS-SEC-006 output encoding.
- Moved REAS-SEC-001 to the new concept and extended it with a CI dependency scan and a review of unsafe code in dependencies that read outside data. Its unsafe-code requirements moved to REAS-SEC-004; the split is recorded in the identifier policy.
- Added REAS-TEST-003 on fuzz targets, property assertions, persisted corpora, stage budgets, and architecture coverage. Retitled the validation concept to Validation and evidence.
- Extended REAS-STATE-002 with authentication and verification steps as states, and REAS-ARCH-003 with a fifth question on who can supply outside data. Each security rule scales by that exposure.
- Added the trust-boundary example: a length-prefixed frame parsed with checked arithmetic, a verification state that the handler requires, a validated event type through serde `try_from`, a SWAR checksum with a differential test, lint and overflow-check settings in the manifest, and a libFuzzer target with a seed corpus.
- CI runs the new crate on x86_64 and aarch64, and builds and runs the fuzz target for 30 seconds on nightly.
- Added terminology for checked arithmetic, corpus, differential test, exposure, full-width access, fuzz target, outside data, output context, reference implementation, scalar tail, seam, SIMD, trust boundary, and the verbs encode, fuzz, and sanitize.

## 1.4.0-draft: 2026-10-23

- Corrected Rust dispatch, allocation, lifetime, coherence, orphan-rule, ownership, and adapter terminology.
- Clarified private-project exceptions, use-case delegation, terminal error handling, and external-state validation.
- Added transaction ownership, concurrency outcomes, async-port bounds, SQLx metadata checks, and release-build requirements.
- Preserved current rule identifiers and documented the historical `REAS-TEST-002` reassignment.
- Replaced regex link matching with CommonMark parsing. Added fragment, index-reachability, metadata, and reserved-log checks.
- Added repository failure tests, numeric input boundary tests, per-transition tests, and a downstream sealing test.
- Pinned Rust toolchains and committed the example lockfiles. Added nightly expected-error-code tests.
- Split compound instructions and clarified the terminology policy. Recorded the Issue 9 language-review scope and open findings.
- Replaced the old current-code claim with revision-specific validation evidence in the self-audit.

## 1.3.0-draft — 2026-10-23

- Corrected the terminology table: lifetime, ownership, port, adapter, SQLx, finite-state machine. Added composition root, smart constructor, typed error, static and dynamic dispatch, coherence, orphan rule, inbound and outbound adapter, hosted build, and human-maintained code.
- Reworded rules that said something other than what they meant. REAS-RUST-002 now separates clarity from runtime cost. REAS-STATE-003 and REAS-DATA-002 now say "guard" transitions, not "enforce" them.
- Moved the async rule to REAS-RUST-007 and the security rule to REAS-SEC-001. Renumbered the evidence rule to REAS-TEST-002.
- Added REAS-ARCH-006 on passing ports as generic parameters.
- Extended the ports and adapters example with a CLI inbound adapter, a composition root, a smart constructor over `NonZeroU32`, and a typed repository error.
- Added a sealed state trait and pinned error codes to the typestate example.
- The documentation checker now requires `standard/index.md`.
- Updated the self-audit, README, and examples README to report that the Rust examples and GitHub Actions pass.

## 1.2.0-draft — 2026-10-21

- Established an OKF v0.2 knowledge bundle under `standard/`.
- Added domain, architecture, typestate, persistence, and documentation rules.
- Added documentation validation, unit tests, and GitHub Actions.
- Added a technical terminology list, an STE review plan, and a self-audit.
- Made human-navigable ports and adapters the preferred design for public and human-maintained software.
- Kept compilation time out of primary engineering priorities.

At this release, Rust example compilation and full ASD-STE100 conformance were not yet verified.
