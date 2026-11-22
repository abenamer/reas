# Changelog

## 1.8.0-draft: 2026-11-22

- Added [Foundations](standard/foundations.md) and the `REAS-FOUND` family. The concept opens by acknowledging that AI-assisted development changed the economics of writing software for the better, so the standard raises its floor for early-stage work and holds its ceiling: no exception for a first version, and no structure added because it is cheap to generate.
- REAS-FOUND-001 raises the floor and holds the ceiling. REAS-FOUND-002 forbids foreseeable rework, weighing decisions by expected cost over the service life, reversal cost, and propagation through later code. REAS-FOUND-003 makes the first instance of any pattern the template.
- REAS-ARCH-003 gains a sixth question on reversal and propagation and reframes its rationale from the cost of files to the cost of reading. REAS-RUST-001 states it has no first-version exception. REAS-ARCH-004 and REAS-RUST-003 state that ease of generation is not evidence of need. REAS-DATA-001 asks for the production database engine from the first commit when it is a recorded requirement.
- Terminology gains foreseeable rework, minimum viable product, recorded requirement, and service life. The index, README, CLAUDE.md, and AGENTS.md point to Foundations first.

## 1.7.0-draft: 2026-11-20

- Added [Native code](standard/native-code.md) and the `REAS-NATIVE` family. REAS-NATIVE-001 states the principle: crossing into unsafe, FFI, SIMD, or inline assembly changes the engineer's obligations, and the crossing itself triggers a standing response to bound, mark, and exercise the code. The practices are framed as a floor that clears mechanical failure classes so judgment can go to the seams no tool watches.
- REAS-NATIVE-002 bounds the unsafe surface with a committed per-crate baseline that only shrinks, currently enforced by `cargo geiger` in CI. REAS-NATIVE-003 states the confine-and-mark habit and cites REAS-SEC-004 for the mechanics. REAS-NATIVE-004 exercises native paths: fuzz targets on outside bytes, Miri on modules with unsafe, Miri-blind marks and sanitizer builds on named hardware for what Miri cannot execute.
- The Miri sentences of REAS-SEC-004 moved to REAS-NATIVE-004; the identifier policy records the split. REAS-SEC-001 and REAS-RUST-004 point to the new family.
- Terminology gains FFI, inline assembly, Miri, Miri-blind, native code, sanitizer, and target feature.
- The self-audit records the native surface of the examples: no unsafe, no FFI, one portable SWAR path, no CPU-gated path.

## 1.6.0-draft: 2026-11-20

- Gave every rule one shape: Intent, Enforcement as Required or Advisory, Scope with what the rule does not apply to, Rules, optional Allowances, and Verification naming the lint, CI job, or review question. Each Engineering Standard concept ends with a Quality test question. The checker enforces both.
- Added REAS-DOC-006: enforce with a check where a check can exist, with a floor, a planted-violation test, and shrink-only baselines.
- Added a retired-terms table to the terminology concept; the checker fails on a retired term outside the exempt documents. Added `updated` dates to every concept with freshness thresholds by type; a stale concept is a warning.
- Core Rust: REAS-RUST-005 now separates library errors from binary context. REAS-RUST-001 covers `#[non_exhaustive]` and `cargo semver-checks`. REAS-RUST-006 covers workspace lints and `#[expect]` over `#[allow]`. New REAS-RUST-008 on money and REAS-RUST-009 on documenting public items.
- Persistence: REAS-DATA-001 keeps serde and SQLx attributes off domain types. REAS-DATA-004 covers MSRV and feature powersets. New REAS-DATA-005 on idempotent consumers. REAS-STATE-003 names the fencing token.
- Validation: REAS-TEST-001 adds non-vacuity rules and mutation-aware test design. REAS-TEST-002 reports six outcomes. New REAS-TEST-004 on doubling only at ports and REAS-TEST-005 on failing-test triage.
- Security: REAS-SEC-001 covers build scripts and proc-macros as build-time code, dependency sources, and a design review for sensitive components. REAS-SEC-002 adds the validation order and two-level error feedback. REAS-SEC-003 covers linear-time regular expressions.
- Architecture: REAS-ARCH-004 names the storage-shaped port. REAS-ARCH-002 gains a dependency-graph check.
- Documentation: REAS-DOC-002 defines authority classes for committed files and the freshness rule. REAS-DOC-003 adds the rule-writing voice. REAS-DOC-004 adds requirement shapes.
- Added `scripts/check.sh` as the one list of this repository's checks; CI, the README, and the agent files point at it. CI gained an MSRV job, the fuzz crate's lint, and the documentation build with warnings denied.
- Examples declare `rust-version = "1.88"`, forbid `unsafe`, warn on missing docs, and document every public item. The trust-boundary tests assert exact error messages.
- CLAUDE.md and AGENTS.md gained negative scope and stopping conditions.

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
