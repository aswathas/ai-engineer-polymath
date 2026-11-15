# ADR 0001 - Polymath is a standalone curriculum series

- Status: accepted
- Date: 2026-11-15
- Deciders: aswathas
- Related: [plan.md](../../plan.md), [decision-log D1](../reviews/decision-log.md)

## Context

A family of repositories already exists under the `ai-lab` prefix: `ai-lab-m0-engineering`
through `ai-lab-m7-products`, each a module of an AI-engineering curriculum, with the teaching
material held in a separate private Obsidian vault.

The question for this repository was whether it should extend that family, wrap it, or stand on
its own.

## Decision

`ai-engineer-polymath` is a standalone series. It has its own module ids (`P0`-`P9`,
`CAPSTONE`), its own gate ids (`G0`-`G9`, `GCAP`), its own module notes, its own agent and
skill packs, and its own validators. It does not import from, depend on, or require the
`ai-lab` repositories.

The `ai-lab` repositories are a **style reference** - the voice of the module notes, the shape
of a gate, the `docs/agents/` convention - and nothing more.

## Consequences

- The series can be read, cloned and run without any private vault and without any sibling
  repository. A learner sees one repository, one rule, one set of contracts.
- Some conceptual ground is covered twice across the two families (the engineering spine
  appears in both). That is accepted: an independent series that depends on a private vault is
  not independent, and a curriculum that cannot be cloned whole cannot be checked by a
  validator.
- If the two series later converge, convergence is a decision to be taken with an ADR, not a
  side effect of shared file paths.
