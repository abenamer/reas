---
type: Engineering Standard
title: Validation, security, and evidence
description: Testing, security checks, and how to report results.
tags: [testing, security, evidence]
---

# Validation, security, and evidence

## REAS-TEST-001 — Test invariants and failures
Write unit tests for domain invariants and for each state transition. Test error paths and invalid inputs. Add property tests and seeded simulations when the input space is large. For a database adapter, test against the real database engine in a container, not against an in-memory substitute.

## REAS-TEST-002 — Report observable evidence
Do not claim that a build, test, migration check, STE review, or recovery passed unless you ran it. Report three outcomes separately: passed, failed, and not run. Record the date and the commit for each passed check.

## REAS-SEC-001 — Verify security properties
Validate all external input. Use parameterized queries. Keep credentials out of source code and logs. Set limits on request size, connection count, and run time. Review each `unsafe` block. Check dependencies for known vulnerabilities with `cargo audit` or `cargo deny`. Apply authentication and authorization to each endpoint that is not local-only.
