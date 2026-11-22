# REAS agent instructions

Start at [Foundations](standard/foundations.md), then [the standard index](standard/index.md).
Load the rules that apply to the task; each rule's Scope says where it applies.
Keep domain behavior, states, ports, and adapters easy to locate.
For private projects, use the architecture questions in [REAS-ARCH-003](standard/ports-and-adapters.md#reas-arch-003).
Record the project service life, not the duration of one execution.

Run `scripts/check.sh all` before you report success; it is the one list of this repository's checks.
Report each check as passed, failed, errored, timed out, skipped, or not run, with its evidence.
Use the [self-audit](standard/self-audit.md) to distinguish current evidence from historical results.
Do not claim full STE compliance from a plain-language edit.

Report as an instrument gauge, as [REAS-FOUND-005](standard/foundations.md#reas-found-005) specifies: a routine pass needs its outcome and evidence reference; a finding needs what failed, why it matters, how sure the evidence is, whether it needs intervention, and what remains uncertain. A possible need for deeper work is a recommendation, not work you start. Never conceal a finding.
Propose a component's failure path under [REAS-FOUND-004](standard/foundations.md#reas-found-004); do not record or lower its consequence.

Do not weaken, skip, or delete a failing test before you classify it under [REAS-TEST-005](standard/validation.md#reas-test-005).
Do not decide product scope, security exposure, or the architecture of a private project.
When three consecutive approaches do not make a failing check pass, stop and report what you tried.
