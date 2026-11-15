# The skill pack

Nine skills. Each one answers one question that comes up again and again while the
curriculum is being built and taught, and each one is a procedure a machine could
follow rather than advice a reader has to interpret.

| Skill | Question it answers | Ships a script |
|-------|---------------------|-----------------|
| [module-note-author](module-note-author/SKILL.md) | How do I write a module note that passes the template? | No |
| [gate-keeper](gate-keeper/SKILL.md) | Is a module done, and exactly what failed? | No |
| [skill-and-agent-linter](skill-and-agent-linter/SKILL.md) | Are the agent and skill packs structurally valid? | Yes - `skill-and-agent-linter/scripts/lint_pack.py` |
| [curriculum-graph](curriculum-graph/SKILL.md) | What is the prerequisite graph, and is it acyclic? | Yes - `curriculum-graph/scripts/graph.py` |
| [issue-author](issue-author/SKILL.md) | How do the module tasks become ordered GitHub issues? | No |
| [project-brief-author](project-brief-author/SKILL.md) | How do I write a capstone brief with a real rubric? | No |
| [eval-harness-design](eval-harness-design/SKILL.md) | What does a defensible eval harness look like? | No |
| [glossary-keeper](glossary-keeper/SKILL.md) | Which term does the series mean by X? | No |
| [publish-github](publish-github/SKILL.md) | How do I ship this repo safely? | No |

## The shared SKILL.md format

Every skill is a directory under `skills/` that holds a `SKILL.md` and, optionally, a
`scripts/` directory. The format is a contract, and
`tools/validators/validate_skills.py` enforces it.

```markdown
---
name: <the directory name>
description: <one sentence, at least 40 characters, saying when to use this skill>
---

# <Title>

## When to use
## Inputs
## Procedure
## Outputs
## Verification
```

The rules:

- The frontmatter holds exactly two keys, `name` and `description`, and the `name`
  equals the directory name.
- The five level-two sections appear exactly once each and in that order, and each one
  has at least one line of content.
- Any `scripts/<name>.py` mentioned in the body exists inside that skill's directory.
- The skill directory holds nothing else at the top level.

The codes are stable and are never renumbered:

| Code | Meaning |
|------|---------|
| `SKL001` | a skill directory has no `SKILL.md`, or the pack README is missing |
| `SKL002` | the frontmatter is missing `name` or `description` |
| `SKL003` | the frontmatter carries a key other than `name` or `description` |
| `SKL004` | a required section is missing or has no content |
| `SKL005` | the required sections are not exactly once each, in order |
| `SKL006` | a referenced script does not exist inside the skill directory |
| `SKL007` | the frontmatter `name` does not match the directory name |
| `SKL008` | the description is shorter than 40 characters |
| `SKL009` | the skill directory holds a stray top-level file |

## Installing a skill into a harness

A skill is a directory, so installing one is a copy.

1. Copy the skill directory into the harness's skill directory, keeping its name:
   `cp -r skills/module-note-author <harness-skills-dir>/`.
2. Keep `SKILL.md` at the top of the copied directory and keep the `scripts/`
   directory beside it, so a script reference still resolves.
3. Make the scripts runnable with the interpreter the harness uses. For example:
   `python <harness-skills-dir>/skill-and-agent-linter/scripts/lint_pack.py --help`.
4. Make sure the harness reads the frontmatter. The `description` is what the harness
   matches against, so it must say *when* to use the skill, not what the skill is
   about.
5. Check the copy against the contract:
   `python skills/skill-and-agent-linter/scripts/lint_pack.py --repo .`.

A skill that is installed on its own, without the repository, still works as long as
its `scripts/` directory came with it. The skills that read repository files (the
curriculum, the validators) need the repository root.

## Checking the pack

```bash
python skills/skill-and-agent-linter/scripts/lint_pack.py --repo .
python tools/validators/run_all.py
```

The linter exits 0 when both packs are structurally valid and 1 when they are not.
`tools/validators/run_all.py` exits 0 when every contract in the repository holds.
