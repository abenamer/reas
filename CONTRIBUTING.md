# Contributing

Give each proposed rule a stable identifier and the rule shape: Intent, Enforcement, Scope, Rules, optional Allowances, and Verification.
The checker rejects a rule without that shape in an Engineering Standard concept.
Name the check that enforces the rule in Verification; when a check can exist, add it, as [REAS-DOC-006](standard/documentation.md#reas-doc-006) specifies.
Include a correct example.
Add a counterexample when it explains a specific failure, and mark it as the counterexample.
Record the tradeoffs.
End each Engineering Standard concept with one Quality test question.

Do not reuse an identifier for a different requirement.
Follow the [identifier policy](standard/rule-identifiers.md) for historical references.
Update [the knowledge index](standard/index.md) when you add a concept.
Use the [terminology table](standard/terminology.md) for terms with a Rust-specific or REAS-specific meaning.

Run `scripts/check.sh all`; it is the one list of this repository's checks.
Record each check as passed, failed, errored, timed out, skipped, or not run.
Do the technical review before the [STE language review](standard/ste-review.md).
Do not report full compliance without evidence from the official rules and dictionary.
