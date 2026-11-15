# Domain Docs

How the skills in this repository consume the domain documentation.

## Before exploring, read these

- **`GLOSSARY.md`** at the repository root: the vocabulary of the series. Read it before
  naming a concept in an issue, a module note, a rubric or a test.
- **`curriculum/curriculum.yaml`**: the module graph - ids, prereqs, gates, hours.
- **`docs/adr/`**: read the ADRs that touch the area you are about to work in.

If any of these files do not exist, **proceed silently**. Do not flag their absence and do not
suggest creating them upfront. The `/glossary-keeper` skill creates them lazily, when a term or
a decision actually gets resolved.

## Use the glossary's vocabulary

When your output names a domain concept (an issue title, a rubric row, a hypothesis, a test
name), use the term as the glossary defines it. Do not drift to a synonym the glossary
explicitly avoids.

If the concept you need is not in the glossary yet, that is a signal: either you are inventing
language the series does not use (reconsider), or there is a real gap (note it for
`/glossary-keeper`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface the conflict explicitly instead of
silently overriding it.
