# The agent pack

Six agents that work the curriculum with a learner. They are plain Markdown files, so they
load into any harness that reads agent definitions from a directory, and they follow one
rule that overrides all of their individual rules: **the learner writes the code, the agent
never does.**

## The roster

| Agent | Job | Hard-rule centre |
|-------|-----|------------------|
| [polymath-tutor](polymath-tutor.md) | Teaches a module: explains concepts, hints, quizzes, and gives a worked trace instead of an implementation | After two requests for code, deliver a worked trace - inputs, intermediate values, reasoning - and never a solution |
| [polymath-reviewer](polymath-reviewer.md) | Reviews learner code and notes against a module's published gate criteria | Every finding carries a severity, a path:line reference, and the reason it matters; no silent rewrites |
| [polymath-quiz-master](polymath-quiz-master.md) | Writes module quizzes with an answer key and a marked rubric | At least five questions, an answer key, a marked rubric, and every question tied to a concept the module states |
| [polymath-curator](polymath-curator.md) | Owns the curriculum graph: prerequisites, gate definitions, hours, and drift | A graph change updates [curriculum.yaml](../curriculum/curriculum.yaml) and the module note together |
| [polymath-project-supervisor](polymath-project-supervisor.md) | Scopes the capstones, writes the briefs, judges the submissions | Every brief states acceptance criteria and the evidence required; judging uses the published rubric only |
| [polymath-eval-auditor](polymath-eval-auditor.md) | Designs eval harnesses and audits performance claims | No metric without a dataset and a baseline; judges calibrated against human labels; mock numbers labelled `SIMULATED` |

## The shared file format

Every agent file is a Markdown document with YAML frontmatter and six required sections.

```markdown
---
name: polymath-tutor
description: <one sentence, at least 40 characters, describing when to use this agent>
---

# <Title>

## Role
## Triggers
## Hard Rules
## Workflow
## Output Contract
## Refusals
```

The contract is machine-checked by `tools/validators/validate_agents.py`:

- **Frontmatter carries exactly two keys**, `name` and `description`. Nothing else.
- **`name` equals the filename stem.** The file `agents/polymath-tutor.md` must declare
  `name: polymath-tutor`.
- **`description` is at least 40 characters** and says when to use the agent, not what it is.
- **The six sections appear exactly once each, in the order above.** No section may be
  missing, renamed, duplicated or reordered.
- **Every section has content.** A heading with nothing under it is a failure, not a stub.

The validator reports these codes, and the codes never change once published:

| Code | Meaning |
|------|---------|
| `AGT001` | A required section is missing (or a required agent file is missing) |
| `AGT002` | Frontmatter is missing `name` or `description` |
| `AGT003` | Frontmatter carries a key other than `name` or `description` |
| `AGT004` | The required sections are not in the required order |
| `AGT005` | Frontmatter `name` does not match the filename stem |
| `AGT006` | The description is shorter than 40 characters |
| `AGT007` | The file is empty |
| `AGT008` | A section exists but has no content under it |

## Installing an agent into a harness

Each agent file is self-contained: it declares its own name, when to use it, and how it
behaves. Installing one is a file copy.

1. **Find the harness's agents directory.** Common locations are `.claude/agents/` for
   Claude Code, `.agents/` for Codex, `.cursor/agents/` for Cursor, or an `agents/`
   directory inside your own project. Any directory the harness scans for `*.md` agent
   definitions works.
2. **Copy the file in.**

   ```powershell
   Copy-Item .\agents\polymath-tutor.md -Destination .\.claude\agents\polymath-tutor.md
   ```

3. **Or symlink it**, so that edits in this repository take effect without a second copy:

   ```powershell
   New-Item -ItemType SymbolicLink -Path .\.claude\agents\polymath-tutor.md -Target .\agents\polymath-tutor.md
   ```

4. **Start a new session** and trigger the agent with one of its triggers, for example
   "teach me P3" for the tutor or "does this pass the gate?" for the reviewer.

Install only the agents you want. The six are independent: each one reads the curriculum
notes and gates, and none of them needs another to be installed first.

## Where the rules come from

The behaviour these files encode is the same behaviour the repository itself is built
under, stated in [AGENTS.md](../AGENTS.md) and in the glossary of terms the curriculum uses.
The one rule that overrides everything is unchanged here: after two requests for an
implementation, an agent gives a **worked trace** - inputs, intermediate values, reasoning -
instead of code. No agent in this pack writes a reference solution, a finished function, or
the body of a TODO, and no agent deletes learner work.
