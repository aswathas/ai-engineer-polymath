---
name: issue-author
description: Use when the curriculum tasks must become ordered GitHub issues, so every task is one issue and each issue is blocked by the one before it.
---

# Issue Author

## When to use

Use this skill when a module's tasks have to be turned into GitHub issues, or when the
existing issue list has drifted out of order.

## Inputs

- The module id, for example `P3`.
- The task list for the module: the acceptance criteria in
  `curriculum/<module>/module-note.md` and the steps in `curriculum/<module>/gate.md`.
- The repository slug, `aswathas/ai-engineer-polymath`.

## Procedure

1. Read the module's tasks and order them so that every task depends only on the
   tasks before it.
2. Write one issue per task. One task, one issue: never bundle two tasks into one
   issue, and never split one task across two issues.
3. Give each issue a title that states the outcome, not the activity: "Add the split
   policy to the dataset builder" beats "Work on data splitting".
4. Give each issue a body with the task, the acceptance criteria it carries, and the
   files it is expected to touch.
5. Block each issue by the previous one, so the tracker shows a single chain of
   dependencies and no two issues can be started at the same time.
6. Create the issues with the repository helper. Preview the plan first with
   `python tools/create_issues.py --module P3 --dry-run`, then run the same command
   without `--dry-run` to create the issues.
7. Read the created issue numbers back and confirm that the chain of blockers matches
   the order from step 1.

## Outputs

- One GitHub issue per task, in dependency order.
- Each issue blocked by the previous one.
- A record of the created issue numbers in `docs/reviews/change-inventory.md`.

## Verification

- The number of issues equals the number of tasks.
- Every issue except the first has exactly one blocker, and that blocker is the
  previous issue.
- `python tools/create_issues.py --module P3 --dry-run` prints the same plan as the
  created issues.
- Every issue body names the acceptance criteria it carries.
