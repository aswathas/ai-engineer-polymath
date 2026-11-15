---
name: project-brief-author
description: Use when writing a capstone brief, so the project states a goal, the modules it exercises, and a rubric with weighted rows.
---

# Project Brief Author

## When to use

Use this skill when a capstone project needs a brief, or when an existing brief has no
rubric a judge could apply consistently.

## Inputs

- The project id, for example `PJ1`.
- The modules the project exercises.
- The capability the project has to demonstrate.
- The time budget for the build and who judges the submission.

## Procedure

1. Write the five sections in this order: *Goal*, *Modules exercised*, *Acceptance
   criteria*, *Evidence required*, *Rubric*.
2. Write the goal as one sentence naming the user, the job to be done and the
   observable outcome. A topic is not a goal.
3. List every module the project exercises and, for each one, state which capability
   from that module the project exercises. A module in the list that the project does
   not exercise is noise; remove it.
4. Write the acceptance criteria so that each one can be checked by a judge who did
   not watch the build.
5. List the evidence a submission must carry: the artifact, the eval output, the cost
   model, the rollback plan.
6. Write the rubric as a Markdown table with a header row and at least three rows.
   Give every row a criterion, a weight and a description of what full marks mean.
   The weights must add up to 100.
7. Name the judge and say whether it is a human, a model or a script, and state how a
   disagreement between two judges is resolved.
8. Run `python tools/validators/run_all.py` and fix what it reports.

## Outputs

- `projects/<project>.md`, the brief with the five sections and the rubric table.
- A row in `docs/reviews/change-inventory.md` for the edited file.

## Verification

- The brief has the five sections in the order above, each with content.
- The rubric is a Markdown table with at least three weighted rows whose weights sum
  to 100.
- Every acceptance criterion is checkable by a judge who did not watch the build.
- `python tools/validators/run_all.py` exits 0.
