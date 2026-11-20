# REAS template: public or human-maintained project

Use ports and adapters.
Construct dependencies in one composition root for each executable.
Declare port traits at replaceable external boundaries.
Name each concrete adapter for the system that it adapts.
Make each operation easy to trace from its inbound adapter to its outbound adapter.

Use domain types and explicit state transitions for invariants.
State each requirement in a decision document as "When <trigger>, the system shall <response>" or one of its variants in [REAS-DOC-004](../standard/documentation.md#reas-doc-004).
Compile after each implementation step.
Keep decisions and operating procedures in OKF concepts.
Do the technical review before the ASD-STE100 Issue 9 language review.
Record the scope and result of each review.
