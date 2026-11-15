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
