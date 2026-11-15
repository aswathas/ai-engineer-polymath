---
name: gate-keeper
description: Use when checking whether a curriculum module is finished, so every acceptance criterion is recorded with evidence and the verdict is pass or fail.
---

# Gate Keeper

## When to use

Use this skill when a learner claims a module is done, or when a gate needs a written
verdict before the series moves on. A gate passes or it fails; there is no partial
gate.

## Inputs

- The module id, for example `P3`.
- The gate file `curriculum/<module>/gate.md`.
- The module note `curriculum/<module>/module-note.md`.
- The learner's artifact and any evidence they produced.

## Procedure

1. Read `curriculum/<module>/gate.md` and extract the acceptance criteria as a
   numbered list. The gate is the contract; the note only explains it.
2. Read `curriculum/<module>/module-note.md` for the context each criterion assumes.
3. For each criterion, in order, decide whether the evidence shows it is satisfied.
4. Record the result of every criterion as `PASS` or `FAIL`, and copy the exact
   evidence into the record: a command and its output, a file path and the lines that
   show it, a quoted sentence from the learner.
5. Mark a criterion `PASS` only when evidence is present. Never mark a criterion
   passed on the learner's assurance, on intent, on a plan, or on partial output.
6. When a criterion fails, state what is missing and what evidence would close it.
7. Return the verdict: `pass` only when every criterion is `PASS`, otherwise `fail`.
   Name the failing criteria in the verdict.
8. Write the verdict and the per-criterion record back into
   `curriculum/<module>/gate.md` so the result is reviewable later.

## Outputs

- A per-criterion record: criterion, verdict, evidence.
- A single verdict of `pass` or `fail`, with the failing criteria named when it fails.
- An updated `curriculum/<module>/gate.md` holding the record.

## Verification

- Every criterion in the gate appears exactly once in the record.
- Every `PASS` carries evidence that another reader could re-check without asking the
  learner.
- The verdict is `fail` whenever any criterion is not `PASS`.
- No criterion was marked `PASS` without a quoted artifact or a recorded command
  output.
