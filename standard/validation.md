---
type: Engineering Standard
title: Validation and evidence
description: Incremental compiler, security, test, and documentation validation.
tags: [testing, security, build]
---

# Validation and evidence

## REAS-TEST-001 — Test invariants and failures
Write domain unit tests, state-transition tests, deterministic seeded simulations, boundary tests, and property tests when useful. Test errors and invalid inputs. For external dependencies, use integration tests against realistic infrastructure.

## REAS-TEST-002 — Separate async work and CPU work
Do not execute long blocking calculations on async executor threads. Use bounded workers, Rayon, or `spawn_blocking` where appropriate. Avoid holding blocking locks across `.await`. Design cancellation and shutdown deliberately.

## REAS-TEST-003 — Verify security properties
Validate external inputs, use parameterized queries, protect credentials, apply resource limits, review `unsafe`, and check dependencies for known vulnerabilities. Apply authentication and authorization whenever local-only assumptions do not hold.

## REAS-TEST-004 — Report observable evidence
Do not claim builds, tests, migration checks, STE conformance, or recoveries passed unless actually checked. Differentiate checks not run from checks that failed. Keep releases reproducible.
