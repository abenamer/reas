---
type: Engineering Standard
title: Persistence and transactions
description: PostgreSQL boundaries, concurrency, and durable storage.
tags: [postgresql, sqlx, transactions]
---

# Persistence and transactions

## REAS-DATA-001 — Use explicit storage operations
Prefer specific SQL queries and versioned migrations. Separate SQLx records from domain types where their invariants differ. Use constraints, indexes, and parameterized queries.

## REAS-DATA-002 — Establish transaction boundaries
Use atomic transactions for multi-step operations. Enforce concurrent workflow transitions through conditional updates or locking. Do not hide SQL semantics in a speculative generic repository.

## REAS-DATA-003 — Preserve data beyond containers
Use named Docker volumes for PostgreSQL persistence, plus independent backups and tested recovery procedures. Normal rebuilds and recreations must preserve records. Avoid `docker compose down -v` during routine maintenance.

## REAS-DATA-004 — Make builds reproducible
For SQLx checked queries, provide a build-time database or offline query metadata. Do not accidentally require a developer's private local database for compilation.
