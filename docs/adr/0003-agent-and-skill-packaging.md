# ADR 0003 - Agents and skills are portable, at the repository root

- Status: accepted
- Date: 2026-11-15
- Deciders: aswathas
- Related: [plan.md](../../plan.md), [decision-log D4](../reviews/decision-log.md)

## Context

The series ships an agent pack and a skill pack. Those files have to be readable by whichever
harness a learner uses, and they have to be checkable: an agent without a fixed format drifts
within two edits, and a skill that points at a script that does not exist is worse than no
skill.

## Decision

Agents live in `agents/*.md`, skills in `skills/<name>/SKILL.md`, both at the repository root,
in a harness-neutral format:

- YAML frontmatter with exactly two keys, `name` and `description`.
- A fixed set of `##` sections, in a fixed order, each with content.
- `AGENTS.md` at the root carries the rules every harness reads.

A skill is installed by copying or symlinking its directory into the harness's skills
directory. There is no `.claude/` mirror.

## Consequences

- The packs work in any harness that reads Markdown skills, which is the point of a series
  about being a polymath engineer rather than a polymath prompt engineer.
- The format is a contract, so the validators can enforce it: `AGT002` catches a frontmatter
  key that should not be there, `AGT004` catches sections in the wrong order, `SKL006` catches
  a dangling script reference.
- One canonical copy means no mirror to keep in sync. Duplication would be a drift source, and
  removing drift sources is what the validator layer is for.
- A harness that needs its own native layout gets an adapter at install time, not a second
  copy in the repository.
