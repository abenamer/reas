---
type: Engineering Standard
title: Human-navigable ports and adapters
description: Explicit architectural boundaries and traceable implementations.
tags: [architecture, rust, hexagonal]
---

# Human-navigable ports and adapters

## REAS-ARCH-001 — Make the code path visible
For public or human-maintained applications, use ports and adapters. Keep one path that a reader can follow: inbound adapter → application use case → port trait → the adapter that implements it. Construct and connect all adapters and use cases in one composition root. Do not add a forwarding layer.

## REAS-ARCH-002 — Keep dependencies directed inward
Domain code does not depend on frameworks, database drivers, transports, or deployment tooling. Examples: Axum, SQLx, HTTP, Docker. Application code defines the ports it needs. Outbound adapters implement those ports. Inbound adapters translate transport data and call application use cases.

## REAS-ARCH-003 — Select the architecture for private projects
Before you use ports and adapters in a private project, ask four questions. Who will read and maintain the code? What external systems does it use? How long must it run? How likely are the boundaries to change? A small personal tool can use a flat module layout with no port traits.

## REAS-ARCH-004 — Do not hide concrete code behind abstraction
Define a port trait only at a boundary where you expect to replace the implementation: a test double, a second backend, or a system outside your control. Do not add factories that build factories, service-locator or container-style registration, duplicate interfaces, or forwarding layers. Give each adapter a name that states what it adapts, for example `PostgresTeamRepository`.

## REAS-ARCH-005 — Separate rules from infrastructure
Keep business rules and mathematical operations as pure functions when you can. Put HTTP serialization, SQLx row mapping, and third-party API clients in adapters. Pass dependencies through constructors.

## REAS-ARCH-006 — Pass ports as generic parameters by default
Give a use case its port as a generic parameter, for example `FindTeam<R: TeamRepository>`. This is static dispatch, and the concrete adapter is visible in the use case's type at the composition root. Use `Box<dyn Port>` or `Arc<dyn Port>` when the implementation is selected at run time, or when generic parameters spread through many types and make them hard to read. State the choice in the composition root.

The [ports and adapters example](../examples/ports-and-adapters/) shows the full path from a CLI inbound adapter to an in-memory outbound adapter, with one composition root.
