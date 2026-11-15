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
