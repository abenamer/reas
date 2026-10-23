# REAS template — public or human-maintained project

Use ports and adapters. Put all wiring in one composition root. Define a port trait at each boundary where you expect to replace the implementation, and give each adapter a descriptive name. Make each operation easy to trace from inbound adapter to use case to outbound adapter.

Use domain types and explicit state transitions for invariants. Compile after each small change. Document decisions and operating procedures in OKF concepts, targeting ASD-STE100 without unverified compliance claims.
