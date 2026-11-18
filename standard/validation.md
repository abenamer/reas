---
type: Engineering Standard
title: Validation and evidence
description: Tests, fuzzing, and evidence for reported results.
tags: [testing, fuzzing, evidence]
---

# Validation and evidence

<a id="reas-test-001"></a>
## REAS-TEST-001: Test invariants and failures

Write unit tests for domain invariants and each state transition.
Do tests for error paths and invalid inputs.
Use a failing test double for error propagation tests through a port.
Use property tests when generated inputs can exercise an invariant.
Use simulations for behavior that depends on sequences of events.
Record the seed when a simulation fails.
Use that seed to reproduce the failure.

For a database adapter, use a container with the production database engine for integration tests.
Do not use an in-memory adapter as evidence for database behavior.
Add a compile-fail test for an attempted downstream implementation of each sealed state trait.

<a id="reas-test-002"></a>
## REAS-TEST-002: Report observable evidence

Report a check as passed only when execution evidence shows that result.
Report passed, failed, and not run as separate outcomes.
For each passed check, record the date and commit or immutable workflow run.
For evidence from a different environment, identify the source and the commands that ran.
Do not apply a passing result to code that changed after that execution.

<a id="reas-test-003"></a>
## REAS-TEST-003: Fuzz each adapter that reads outside bytes

Write one fuzz target for each inbound adapter and each parser that reads outside bytes.
Call the adapter's public entry point with the fuzzer's bytes.
Assert properties in the target.
A target that only checks for the absence of a panic finds fewer defects.
Assert these properties where they apply:

- The adapter returns a value or a typed error.
- A parsed value encodes back to the input bytes.
- Each duplicate implementation returns the same result as its reference, as [REAS-SEC-005](security.md#reas-sec-005) specifies.
- The adapter rejects an input above the resource limit before it allocates.

Build each target with `cargo fuzz`.
Keep debug assertions and overflow checks enabled in the fuzz build.

Persist the corpus.
Commit a seed corpus with at least one valid input for each target.
Store the corpus that CI finds in artifact storage or a corpus repository.
Start the next run from that corpus.
Minimize the corpus on a schedule.
Record each crash artifact as a bug and add a regression test.

Set a time budget for each stage and record it in the workflow file:

- Pull request: a short run for each target, for example 30 to 60 seconds, from the persisted corpus.
- Nightly: a longer run, for example 30 minutes for each target.
- Release: a run from the full corpus, for example several hours, before the release is cut.

Run the targets on each CPU architecture and target-feature set that the code deploys to.
SIMD paths and endianness differ between them.
A private tool that reads no bytes from another party can record an exception for the budgets and the architecture matrix in an architecture decision.

Verification:

- CI: one fuzz job for each stage, with the budget in the workflow file.
- Review question: which inbound adapter has no target, and why?

The [trust-boundary example](../examples/trust-boundary/) includes one target with a seed corpus.
Its nightly CI job builds the target and runs it for 30 seconds on x86_64.

## Moved rules

<a id="reas-sec-001"></a>
REAS-SEC-001 moved to [Security at seams](security.md#reas-sec-001) in 1.5.0-draft.
The identifier and its purpose did not change.
