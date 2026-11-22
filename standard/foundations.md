---
type: Engineering Standard
title: Foundations
description: Why this standard raises the floor for early-stage work and holds the ceiling, and the principles that follow.
tags: [foundations, principles, technical-debt, mvp]
updated: 2026-11-22
---

# Foundations

AI-assisted development changed the economics of writing software, and changed them for the better.
The practices this standard asks for used to cost days of work that an early-stage project could not spare: validated domain types, typed errors, tests that fail when behavior breaks, a production database engine from the first commit, documentation written in the same change, one visible composition root.
They now cost minutes to produce.
The bargain that justified most early shortcuts, correctness traded for time, no longer holds for this class of work.
This standard therefore grants no exception for a first version.

What became cheaper is producing code and exploring alternatives.
What did not become cheaper is reading code, verifying that it is correct, and migrating data and contracts once they exist.
So the standard raises its floor for early-stage work and holds its ceiling where it was.
Do not defer the engineering that is now cheap.
Do not add structure because it is cheap to generate.
The first version of a project is where this matters most, because every later version, and every agent that writes it, copies what the first version established.

The rest of the standard rests on three more stances that other concepts state in full:

- Evidence: a check is passed only when a cited run on a named revision shows it, as [REAS-TEST-002](validation.md#reas-test-002) specifies.
- Seams: the defects that survive type checking live where two correct pieces disagree, as [Security at seams](security.md) describes.
- Floor, not ceiling: the mechanical practices clear known failure classes so that judgment is free for what no tool watches, as [Native code](native-code.md) describes.

<a id="reas-found-001"></a>
## REAS-FOUND-001: Raise the floor, hold the ceiling

### Intent

The cost of sound engineering fell; the cost of owning unsound engineering did not.
A standard that still prices correctness in days of typing would license shortcuts that no longer save anything and would miss the one cost that grew: the reader's.

### Enforcement

Advisory.

### Scope

Applies to every decision about how much engineering a change deserves, in every project that adopts this standard, at every stage including the first version.
Does not apply to product scope, which the project's owner decides.

### Rules

Write responsibly from the first commit.
A minimum viable product limits product scope; it is not a license for engineering deficiencies in what is built.
Reduce scope by building fewer features, not by building the chosen features badly.

Treat the cost of producing code as near zero and the cost of reading, verifying, and migrating it as unchanged.
Do not defer a known engineering responsibility because it can be completed later.
Do not add a type, a trait, a layer, or a test because it is cheap to generate.
Add it because a recorded requirement or an existing responsibility needs it, as [REAS-ARCH-004](ports-and-adapters.md#reas-arch-004) and [REAS-RUST-003](core-rust.md#reas-rust-003) specify.

The floor is the set of practices whose cost fell: the rules of this standard.
The ceiling is judgment: which boundaries the domain actually has, which requirement will survive contact with users, which seam the tools do not watch.
The floor exists to free attention for the ceiling, not to replace it.

### Verification

- Review question: which shortcut in this change saves production time, and what does it cost the next reader?
- Review question: which structure in this change exists because it was cheap to generate rather than because a recorded requirement needs it?

<a id="reas-found-002"></a>
## REAS-FOUND-002: Avoid foreseeable rework

### Intent

Rework that the author could see coming is engineering effort spent twice and reviewed twice.
Its cost is not fixed at the moment of the shortcut: it grows with every feature written in the shortcut's image and with every agent that reads the shortcut as the intended design.

### Enforcement

Required.

### Scope

Applies to every design decision whose alternative is a known, maintainable implementation that is practical now.
Does not apply to a decision that rests on a requirement nobody has recorded; that decision stays reversible and is deferred.

### Rules

Do not knowingly choose a temporary or structurally deficient implementation to save initial effort when a maintainable implementation is practical and the requirement it serves is recorded.
A requirement is recorded when it appears in a decision document, in the answers to [REAS-ARCH-003](ports-and-adapters.md#reas-arch-003), or in the project's stated service life.
A requirement inferred from the code or from a guess about the future is not recorded, and building for it is speculative.

Weigh each decision by three costs over the recorded service life:

1. Its expected cost if the project reaches that life.
2. Its reversal cost: a decision that touches persisted data, a wire format, an identifier handed to another party, or the boundary between domain and I/O is costly to reverse.
3. Its propagation: a decision that later code will copy has a reversal cost that grows with every copy. A convention is a decision of this kind.

Make the decisions with high reversal or propagation cost deliberately and early.
Keep the others reversible and defer them without guilt.
Reversibility bounds the damage of a wrong guess; it is not a reason to choose a known-worse design.

Develop against the production database engine from the first commit when the engine is a recorded requirement, as [REAS-DATA-001](persistence.md#reas-data-001) specifies.
Keep domain behavior separate from I/O from the first commit, even in a flat module layout, because that separation is what keeps the later move to ports cheap.
Model domain values as validated types from the first commit, because a value passed as a bare string or integer is copied at every call site and becomes the most expensive refactoring in the project, as [REAS-RUST-001](core-rust.md#reas-rust-001) specifies.

### Allowances

A spike written to answer one question and deleted afterward is not a first version; record that it will be deleted, and delete it.

### Verification

- Review question: what foreseeable rework does this shortcut create, and what will it cost once the code that copies it exists?
- Review question: which recorded requirement does this structure serve? If none, why is it not speculative?
- Review question: which decision here is costly to reverse, and was it made deliberately?

<a id="reas-found-003"></a>
## REAS-FOUND-003: Make the first instance the template

### Intent

An agent reads the repository as the specification of intent and reproduces the patterns it finds.
A person does the same with less consistency.
The first implementation of any pattern is therefore not an instance; it is the template every later instance copies.

### Enforcement

Required.

### Scope

Applies to the first occurrence of any pattern in a repository: the first handler, the first repository adapter, the first domain type, the first test, the first error enum.
Does not apply to a later occurrence that follows an established pattern; that occurrence is reviewed against the template.

### Rules

Make the first instance small and correct before you make it complete.
One pure domain function with validated inputs, one adapter that owns its SQL, one test that fails when the behavior it names is removed: these cost little and set the pattern for everything after them.
Do not let the first instance carry the shortcut you plan to remove later; it will be copied before you remove it.
When you find that a copied pattern is wrong, fix the template and the copies in one change, as [REAS-DOC-006](documentation.md#reas-doc-006) specifies for defect classes, so that the next copy is of the fixed version.
Examples in documentation are instructions in the same way, as [REAS-DOC-003](documentation.md#reas-doc-003) specifies.

### Verification

- Review question: if this is the first instance of its pattern in the repository, is it the one you want copied?
- Review question: which existing instance did this change copy, and does that instance still represent the intended design?

## Quality test

Does this change defer any engineering that is now cheap, add any structure that only generation made cheap, or establish a pattern you would not want copied?
