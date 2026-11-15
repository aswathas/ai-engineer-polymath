# Prompts

The prompts that shaped this work. The full conversation lives in the agent runtime session
record; this file keeps the decisive ones next to the code they produced.

---

## 2026-11-15 - Repository inception

**Prompt.**

> Continue the ai-engineer-polymath implementation. Create the complete repository, agents,
> skills, curriculum, projects, validators, tests, CI, documentation, commits, and public GitHub
> push. Follow Plan Mode until canonical plan.md is approved.

**Follow-up questionnaire** (four decisions, answered by the user).

1. *What is ai-engineer-polymath's role?* -> Standalone new curriculum series, independent of
   M0-M7. See decision D1.
2. *Where should the repo live?* -> `C:\Users\ADMIN\Projects\ai-engineer-polymath`, public
   `aswathas/ai-engineer-polymath`. See decision D2.
3. *Stack for validators and tests?* -> Python 3.12 + pytest, matching ai-lab modules. See
   decision D3.
4. *How should agents and skills be packaged?* -> Repo-root portable `agents/` and `skills/`
   with `SKILL.md`, plus `AGENTS.md`. See decision D4.

**Approval gate.** The user approves the canonical `plan.md` before any implementation task
starts. The plan file is the contract for scope, file tree, validator codes and commit units.

**Approval (second questionnaire).**

> Approve canonical plan.md and start implementation?
> - Approve - start T1 through T14, then push public
> - Do not approve - I want changes first

**Answer.** Approve - start T1 through T14, then push public.

**Work prompts issued to the build agents.** Four build agents ran in parallel, each with a
self-contained brief: one for the agent pack and its validator, one for the skill pack and its
validator, one for the curriculum and its validator, one for the capstone briefs and their
validator. Every brief stated the shared validator API, the exact error codes, the file ownership
(one writer per file), the verification command, and the rule that no agent runs a git command.
The brief texts are the substance of the four implementation commits
`feat: add the agent pack and the agent validator`,
`feat: add the skill pack and the skill validator`,
`feat: add the P0-P9 curriculum, the capstone module and the curriculum validator` and
`feat: add the capstone briefs, the capstone rubric and the project validator`.
