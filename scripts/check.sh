#!/usr/bin/env bash
# The one place that lists this repository's checks (REAS-DOC-006).
# CI, the README, CLAUDE.md, and the examples README all point here.
#
#   scripts/check.sh docs     documentation checker and its unit tests
#   scripts/check.sh rust     stable Cargo checks for every example crate
#   scripts/check.sh nightly  expected-error-code doctests and the fuzz target
#   scripts/check.sh all      docs and rust
#
# Each command prints the exact command it runs, so a report can name it.
set -euo pipefail
cd "$(dirname "$0")/.."

CRATES=(examples/ports-and-adapters examples/typestate examples/trust-boundary)
NIGHTLY=nightly-2026-10-23

run() { printf '\n$ %s\n' "$*"; "$@"; }

docs() {
  run python3 scripts/check_docs.py
  run python3 -m unittest discover -s tests -v
}

rust() {
  for crate in "${CRATES[@]}"; do
    run cargo check --locked --manifest-path "$crate/Cargo.toml" --all-targets
    run cargo test --locked --manifest-path "$crate/Cargo.toml"
    run cargo clippy --locked --manifest-path "$crate/Cargo.toml" --all-targets -- -D warnings
    run cargo fmt --manifest-path "$crate/Cargo.toml" --all -- --check
    RUSTDOCFLAGS="-D warnings" run cargo doc --locked --manifest-path "$crate/Cargo.toml" --no-deps
  done
  # The fuzz crate is outside --all-targets of its parent (REAS-DOC-006: no zero-gated path).
  run cargo clippy --locked --manifest-path examples/trust-boundary/fuzz/Cargo.toml --all-targets -- -D warnings
  run cargo fmt --manifest-path examples/trust-boundary/fuzz/Cargo.toml --all -- --check
}

nightly() {
  run cargo "+$NIGHTLY" test --locked --manifest-path examples/typestate/Cargo.toml --doc
  run cargo "+$NIGHTLY" test --locked --manifest-path examples/trust-boundary/Cargo.toml --doc
  # REAS-TEST-003 pull-request budget: 30 seconds from the seed corpus.
  (cd examples/trust-boundary && run cargo "+$NIGHTLY" fuzz build receive)
  (cd examples/trust-boundary && run cargo "+$NIGHTLY" fuzz run receive -- -max_total_time=30)
}

case "${1:-all}" in
  docs) docs ;;
  rust) rust ;;
  nightly) nightly ;;
  all) docs; rust ;;
  *) echo "usage: scripts/check.sh {docs|rust|nightly|all}" >&2; exit 2 ;;
esac
printf '\nPASS: %s\n' "${1:-all}"
