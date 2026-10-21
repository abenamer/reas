---
type: Engineering Standard
title: Human-navigable ports and adapters
description: Explicit architectural boundaries and traceable implementations.
tags: [architecture, rust, hexagonal]
---

# Human-navigable ports and adapters

## REAS-ARCH-001 — Make the code path visible
For public or human-maintained applications, favor ports and adapters with clear paths: inbound adapter → application use case → named port → concrete adapter. Show construction and wiring in one discoverable composition root. Prefer meaningful boundaries over forwarding layers.

## REAS-ARCH-002 — Keep dependencies directed inward
Domain logic does not depend on Axum, SQLx, HTTP, or Docker. Application code defines the ports it needs. Infrastructure implements outbound adapters. HTTP handlers translate transport data and delegate to application use cases.

## REAS-ARCH-003 — Select the architecture for private projects
Before adopting hexagonal architecture in private projects, ask who will read and maintain the code, what external systems it uses, how long it must remain operational, and how likely those boundaries are to change. Small personal tools may use simple modules.

## REAS-ARCH-004 — Avoid abstraction hiding concrete code
Use small, cohesive port traits only at genuine boundaries. Avoid nested factories, hidden dependency registration, redundant interfaces, and repeated layers that only forward calls. Name concrete adapters descriptively and make them easy to locate.

## REAS-ARCH-005 — Separate algorithms from infrastructure
Keep core business rules and mathematical operations pure where practical. Put HTTP serialization, SQLx row mapping, and third-party protocols in their adapters. Favor explicit constructor-based dependency wiring.

The [ports and adapters example](../examples/ports-and-adapters/) shows direct wiring of a repository port to a concrete adapter.
