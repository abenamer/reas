---
type: Engineering Standard
title: Persistence and transactions
description: PostgreSQL boundaries, concurrency, and durable storage.
tags: [postgresql, sqlx, transactions]
---

# Persistence and transactions

## REAS-DATA-001 — Use explicit storage operations
Write a specific SQL query for each operation. Version each schema change as a migration. Map a SQLx row type to a separate domain type when their invariants differ. Enforce invariants with database constraints. Use parameterized queries. Add indexes on the columns that frequent queries filter or join on.

## REAS-DATA-002 — Set transaction boundaries
Put each multi-step write in one transaction. Guard workflow transitions against concurrent writers with a conditional update or a row lock, as [REAS-STATE-003](state-machines.md) describes. Do not hide SQL in a generic repository before a second concrete repository exists.

## REAS-DATA-003 — Keep data beyond the container lifecycle
Store PostgreSQL data in a named Docker volume. Keep independent backups and test the restore procedure. A container rebuild or recreate must not delete records. Never run `docker compose down -v` against a database you need. The `-v` flag deletes the volumes.

## REAS-DATA-004 — Make builds reproducible
For SQLx checked queries, commit the offline query metadata that `cargo sqlx prepare` writes to `.sqlx/`, and set `SQLX_OFFLINE=true` in the hosted build. Compilation must not require a developer's local database. Commit `Cargo.lock` for binary crates so that a release builds the same dependency set each time.
