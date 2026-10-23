# Changelog

## Unreleased

- Corrected the terminology table: lifetime, ownership, port, adapter, SQLx, finite-state machine. Added composition root, smart constructor, typed error, static and dynamic dispatch, coherence, orphan rule, inbound and outbound adapter, hosted build, and human-maintained code.
- Reworded rules that said something other than what they meant. REAS-RUST-002 now separates clarity from runtime cost. REAS-STATE-003 and REAS-DATA-002 now say "guard" transitions, not "enforce" them.
- Moved the async rule to REAS-RUST-007 and the security rule to REAS-SEC-001. Renumbered the evidence rule to REAS-TEST-002.
- Added REAS-ARCH-006 on passing ports as generic parameters.
- Extended the ports and adapters example with a CLI inbound adapter, a composition root, a smart constructor, and a typed repository error.
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
