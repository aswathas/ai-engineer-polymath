---
name: glossary-keeper
description: Use when a term in the series needs a single definition, or when a module uses a term the glossary does not yet define.
---

# Glossary Keeper

## When to use

Use this skill when a module introduces a term, when two modules appear to use the
same word for different things, or when a reader asks what the series means by a word.

The vocabulary of the series lives in `GLOSSARY.md` at the repository root. A term means
one thing everywhere in the curriculum.

## Inputs

- The term in question, exactly as it is used in the material.
- The modules, notes, gates or briefs that use the term.
- The current contents of `GLOSSARY.md`.

## Procedure

1. Read `GLOSSARY.md` and look for the term. Match on the heading, case-insensitively,
   not on a word that merely appears inside a definition.
2. If the term is already defined, quote the existing definition and point at the
   modules that use it. Do not rewrite a definition that is already correct.
3. If the term is not defined, read every place the series uses it before proposing a
   definition. A definition that fits one module and contradicts another is not a
   definition.
4. Write the definition in the house style: what the term means, then what it does
   not mean. Terms are written so that a learner can be tested on them.
5. Add the term to `GLOSSARY.md` in alphabetical position, with the same heading level
   and paragraph shape as its neighbours.
6. Do not invent synonyms. When a module uses a different word for a defined term, the
   module is wrong and is corrected to use the defined term; the glossary is not
   widened to cover both.
7. When a module uses a term the glossary does not define, flag the module and the
   term to the curriculum owner instead of silently adding a definition.
8. Record the change in `docs/reviews/change-inventory.md`.

## Outputs

- An updated `GLOSSARY.md` with at most one new term.
- A flag naming the module and the undefined term, when a term is missing.
- A row in `docs/reviews/change-inventory.md` for the edited file.

## Verification

- The term appears exactly once as a heading in `GLOSSARY.md`.
- The definition states what the term is and what it is not.
- No synonym was added: the number of headings in `GLOSSARY.md` grew by at most one.
- Every undefined term was reported rather than silently defined.
