---
name: module-note-author
description: Use when writing or updating a curriculum module note so it matches the module-note section contract and passes the repository validators.
---

# Module Note Author

## When to use

Use this skill when a module note has to be written from scratch, or when an existing
`curriculum/<module>/module-note.md` has drifted away from the section contract or
from the module's entry in `curriculum/curriculum.yaml`.

The module note is the teaching document for a module. The learner reads it before
writing any code, and the gate is judged against it, so a vague note makes the gate
unfair. The rules that override everything else are in [AGENTS.md](../../AGENTS.md).

## Inputs

- The module id, for example `P3` or `capstone`.
- The module's entry in `curriculum/curriculum.yaml`: title, prerequisites, hours.
- The template at `curriculum/templates/module-note.md`, when it exists.
- The gate at `curriculum/<module>/gate.md`, when it exists.

## Procedure

1. Resolve the module directory name from the module id in `curriculum/curriculum.yaml`.
   The note lives at `curriculum/<module>/module-note.md`.
2. Read the module's entry in `curriculum/curriculum.yaml` and record its title,
   prerequisites and hours.
3. Read `curriculum/templates/module-note.md` if it exists. The template is the
   authority on the section names; the contract in step 4 is the fallback.
4. Write the six sections in this order, each with a non-empty body: *What*, *Why it
   comes here*, *What gets built*, *Acceptance criteria*, *The artifact*, *Notes*.
5. Write every acceptance criterion so that a second reader with no memory of the
   conversation can check it: name the artifact, the command or file to run, and the
   observable result that counts as done.
6. Make the *What gets built* section agree with the artifact named in *The
   artifact* section. One module ships exactly one artifact.
7. Run `python tools/validators/run_all.py` from the repository root.
8. Fix every issue the validators report, then run the command again until it exits 0.
9. Record the change in `docs/reviews/change-inventory.md` and, when the note encodes
   a choice rather than a fact, in `docs/reviews/decision-log.md`.

## Outputs

- `curriculum/<module>/module-note.md`, updated in place and never deleted.
- A row in `docs/reviews/change-inventory.md` for the edited file.
- An entry in `docs/reviews/decision-log.md` when a design choice was made.

## Verification

- `python tools/validators/run_all.py` exits 0 and reports no issue code.
- The note contains the six sections in the order above, each with content.
- Every acceptance criterion names an artifact and an observable result, and each one
  is reflected in the module's gate.
- The module's entry in `curriculum/curriculum.yaml` still matches the note's title
  and hours.
