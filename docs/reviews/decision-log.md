# Decision Log

One entry per decision with real alternatives. Oldest first. The prompt that produced the
decision is part of the entry, not a summary of it.

---

## D1 - Standalone curriculum series, independent of AI Lab M0-M7

**Date:** 2026-11-15

**Decision.** `ai-engineer-polymath` is a self-contained curriculum series with its own module
ids (`P0`-`P9`, `CAPSTONE`), its own gates (`G0`-`G9`, `GCAP`), its own repository and its own
validators. It does not wrap, extend or depend on the `ai-lab-m0-engineering` ... `ai-lab-m7-products`
repositories.

**Alternatives considered.**

- *Umbrella over AI Lab M0-M7.* Rejected: it would make this repo a navigation shell with no
  content of its own, and it would couple the polymath gates to module notes that live in a
  private Obsidian vault.
- *Toolchain-only repo (agents, skills, validators, CI).* Rejected: the value of a polymath
  curriculum is the cross-domain path, not the tooling around it.

**Prompt that produced it.**

> What is ai-engineer-polymath's role?
> - Umbrella over AI Lab M0-M7: curriculum, cross-module projects, shared agents/skills
> - Standalone new curriculum series, independent of M0-M7
> - Toolchain repo only: agents, skills, validators, CI (no curriculum content)

**Answer.** Standalone new curriculum series, independent of M0-M7.

**Consequence.** Module content is written from scratch. The AI Lab repos are a style reference
(voice, gate format, `docs/agents/` convention), not a dependency.

---

## D2 - Local path and public remote

**Date:** 2026-11-15

**Decision.** The repository lives at `C:\Users\ADMIN\Projects\ai-engineer-polymath` and is
published as the **public** repository `aswathas/ai-engineer-polymath` under the `gh` account
`aswathas`.

**Alternatives considered.**

- *Private first, flipped to public at the end.* Rejected: the user asked for a public push, and
  a private-then-public flip adds a state the repository never needs to be in.
- *Another local path.* Rejected: `Projects\` is where the other working repositories live.

**Prompt that produced it.**

> Where should the repo live?
> - C:\Users\ADMIN\Projects\ai-engineer-polymath, public aswathas/ai-engineer-polymath
> - Same path, private repo first, flip public on request
> - Different path (you type it)

**Answer.** `C:\Users\ADMIN\Projects\ai-engineer-polymath`, public `aswathas/ai-engineer-polymath`.

**Consequence.** The remote is created with `gh repo create --public`. Nothing secret may enter
the tree: the `.env` rule and the secret scan in the push checklist are the gate.

---

## D3 - Python 3.12 and pytest for the validator layer

**Date:** 2026-11-15

**Decision.** The validators, the test-suite and the CI all run on Python 3.12+ with `pytest`,
`ruff` and `PyYAML`. No other runtime dependency, no network access in a validator, no
JavaScript toolchain.

**Alternatives considered.**

- *Node 22 + TypeScript + vitest.* Rejected: it would put the curriculum's own tooling on a
  different stack from the modules it teaches, and the curriculum is Python-first.
- *Mixed Python and Node.* Rejected for v1: two toolchains double the CI surface for no gain
  in what the repository teaches.

**Prompt that produced it.**

> Stack for validators and tests?
> - Python 3.12 + pytest, matching ai-lab modules
> - Node 22 + TypeScript + vitest
> - Python validators plus a small Node tool

**Answer.** Python 3.12 + pytest, matching the AI Lab modules.

**Consequence.** `pyproject.toml` pins `requires-python = ">=3.12"`, the `dev` extra carries
`pytest` and `ruff`, and `SKEL004`-`SKEL007` fail the build if any of that drifts.

---

## D4 - Portable repo-root `agents/` and `skills/` plus `AGENTS.md`

**Date:** 2026-11-15

**Decision.** Agent definitions live in `agents/*.md` and skills live in
`skills/<name>/SKILL.md`, both at the repository root, with a portable frontmatter shape, plus
an `AGENTS.md` at the root that carries the rules every harness reads. No `.claude/` mirror.

**Alternatives considered.**

- *Claude-native `.claude/agents` and `.claude/skills`.* Rejected: it locks the curriculum to one
  harness, and the series is taught across harnesses.
- *Both, with a validator keeping the mirror in sync.* Rejected for v1: duplication is a drift
  source, and the whole point of the validator layer is to remove drift sources.

**Prompt that produced it.**

> How should agents and skills be packaged?
> - Repo-root portable agents/ and skills/ with SKILL.md, plus AGENTS.md
> - Claude-native .claude/agents and .claude/skills
> - Both: canonical root dirs plus .claude mirrors

**Answer.** Repo-root portable `agents/` and `skills/` with `SKILL.md`, plus `AGENTS.md`.

**Consequence.** The frontmatter shape is a contract: `name` and `description` and nothing
else, checked by `AGT002` and `SKL002`. The fixed section order is checked too, so a skill
reads the same way in every harness.

---

## D5 - Every commit is verified against its own tree

**Date:** 2026-11-15

**Decision.** Each commit is verified by extracting it with `git archive` into a temporary
directory and running the validators and the test-suite **there**, not in the working tree.

**Alternatives considered.**

- *Verify the working tree.* Rejected: the working tree contains the files of later commits, so
  a green run says nothing about the commit being made. The validators read the tree they ship
  with, which is the whole point of a self-hosting repository.
- *Verify only at the end of the branch.* Rejected: the end state would hide a broken
  intermediate commit, and the commit discipline asks for one meaningful unit per commit.

**Prompt that produced it.**

> Approve canonical plan.md and start implementation?
> - Approve - start T1 through T14, then push public

**Answer.** Approve - start T1 through T14, then push public.

**Consequence.** Every commit in the series carries a verification result for the tree that
commit contains. The last commits in the series are the first ones where the whole contract set
applies, because the earlier ones are partial builds: the skeleton validator requires directories
that later tasks create.

---

## D6 - Validator codes are frozen; a new rule gets a new code

**Date:** 2026-11-15

**Decision.** Once a validator code is published in
[docs/validator-reference.md](../validator-reference.md) and asserted on by a test, that code
keeps its meaning forever. A new rule takes a new code in the same family range. A code is
never renumbered and never reused for a different rule.

**Alternatives considered.**

- *Renumber codes when the rule set changes.* Rejected: a reader who bookmarked `AGT004` would
  silently get a different meaning, and the tests would have to change with it.
- *Use prose messages only.* Rejected: messages change with the wording; codes are what a test
  asserts on and what CI output greps for.

**Prompt that produced it.**

> Every decision spoken with an AI (including the prompt that produced it) -> docs/reviews/decision-log.md

**Consequence.** `SKEL001`-`SKEL010`, `AGT001`-`AGT008`, `SKL001`-`SKL009`, `CUR001`-`CUR009`,
`PRJ001`-`PRJ007`, `LNK001`-`LNK004` and `REC001`-`REC006` are now part of the repository's
public interface, the same way the agent and skill formats are.
