# REAS template: private project

Before you select the architecture, ask these questions:

1. Who will read and maintain the code?
2. What external systems does it use?
3. For how long must the project remain in use?
4. How likely are the boundaries to change?

Record the answers under [REAS-ARCH-003](../standard/ports-and-adapters.md#reas-arch-003).
Use a flat module layout for a private personal tool with no replaceable external dependency.
Record any other architecture exception in a decision document.
Keep domain behavior separate from I/O.
Apply the type-safety, testing, and documentation rules.
