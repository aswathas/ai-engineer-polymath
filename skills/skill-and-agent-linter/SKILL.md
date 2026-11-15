---
name: skill-and-agent-linter
description: Use when checking that the agent pack and the skill pack are structurally valid, so frontmatter and section order are verified before a commit lands.
---

# Skill and Agent Linter

## When to use

Use this skill before a commit that touches `agents/` or `skills/`, and whenever the
question is whether the packs are structurally valid.

## Inputs

- The repository root, defaulting to the current directory.
- The pack directories `agents/` and `skills/`.

## Procedure

1. Run the shipped linter from the repository root:
   `python skills/skill-and-agent-linter/scripts/lint_pack.py --repo .`
2. Read the reported findings. Each finding names the file and the reason it was
   rejected.
3. For a skill, fix whichever part of the contract broke: the frontmatter (exactly
   `name` and `description`), the `name` matching the directory, the five required
   sections in order, a `scripts/` reference that does not resolve, or a stray file
   in the skill directory.
4. For an agent, fix the frontmatter (`name` matching the file stem, plus a
   `description`) or the agent section order.
5. Re-run the linter until it exits 0.
6. Run the repository validator as well: `python tools/validators/run_all.py`.

## Outputs

- A linter exit code of 0 (the packs are valid) or 1 (at least one finding).
- One line per finding: the file path and the reason it was rejected.

## Verification

- `python skills/skill-and-agent-linter/scripts/lint_pack.py --repo .` exits 0 on a
  clean pack and 1 when a file is malformed.
- `python tools/validators/run_all.py` exits 0 and reports no skill issue.
