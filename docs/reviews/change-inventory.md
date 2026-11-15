# Change Inventory

One row per changed file: what changed, why, how it was verified. Every tracked file appears
exactly once.

| File | What changed | Why | How verified |
|------|--------------|-----|--------------|
| `plan.md` | Added the canonical implementation plan: goal, architecture, global constraints, curriculum table, agent roster, skill roster, project briefs, validator code contract, test plan, CI plan, docs tree, target file tree, 14 tasks, definition of done, risks, approval gate | The user asked for Plan Mode with a canonical `plan.md` approved before implementation | Read back from disk; every section cross-checked against the four approved decisions D1-D4 |
| `docs/reviews/decision-log.md` | Added entry D1 (standalone curriculum series) with alternatives and the originating prompt | Commit discipline requires every decision to be documented with its prompt | `Get-Content` read-back; D1 matches the recorded user answer |
| `docs/reviews/prompts.md` | Added the inception prompt, the four-question questionnaire with the answers, and the approval gate | Commit discipline requires every prompt that shaped the work to be recorded | Read back from disk; quotes match the session transcript |
| `docs/reviews/change-inventory.md` | Created this inventory | Commit discipline requires one row per changed file | Read back from disk; rows match the files in this commit |
| `.gitignore` | Added ignore rules for Python artefacts, tool caches, `.env` and secret key files | A curriculum repo must never be able to swallow a key or a virtualenv | `git status --porcelain` after staging shows no ignored path tracked |
| `BUILDLOG.md` | Created the build log with the inception entry | Commit discipline requires a build log beside the docs tree | Read back from disk |
