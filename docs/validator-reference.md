# Validator reference

Every code a validator can report, what it means, and how to fix it. The codes are published
identifiers: they are asserted on by the test-suite, so a code is never renumbered or reused.
A new rule gets a new code in its own range.

Run everything:

```bash
python tools/validators/run_all.py
```

## SKEL - the shape of the repository

`tools/validators/validate_skeleton.py`

| Code | Meaning | Fix |
|------|---------|-----|
| `SKEL001` | A required root file is missing | Add the file listed in the message |
| `SKEL002` | A required directory is missing | Create the directory |
| `SKEL003` | A root file cannot be read or parsed | Fix the encoding or the syntax |
| `SKEL004` | `requires-python` does not demand 3.12 or newer | Set `requires-python = ">=3.12"` |
| `SKEL005` | The `dev` extra does not depend on pytest | Add `pytest>=8.0` to the extra |
| `SKEL006` | The `dev` extra does not depend on ruff | Add `ruff>=0.6` to the extra |
| `SKEL007` | The runtime does not depend on PyYAML | Add `PyYAML>=6.0` to the dependencies |
| `SKEL008` | `.gitignore` does not exclude `.env` | Add the `.env` line |
| `SKEL009` | `.gitignore` does not exclude the caches and the virtualenv | Add `__pycache__`, `.venv`, `.pytest_cache` |
| `SKEL010` | A required root file is empty | Write the document |

## AGT - the agent pack

`tools/validators/validate_agents.py`

| Code | Meaning | Fix |
|------|---------|-----|
| `AGT001` | A required section, an agent file or the pack README is missing | Add the section or the file |
| `AGT002` | Frontmatter is missing `name` or `description` | Add the key |
| `AGT003` | Frontmatter carries a key other than `name` and `description` | Remove the extra key |
| `AGT004` | The required sections are not in the required order, or one is repeated | Reorder to the fixed order |
| `AGT005` | The frontmatter `name` does not match the filename stem | Rename one of them |
| `AGT006` | The description is shorter than 40 characters | Write a real description |
| `AGT007` | The file is empty or not UTF-8 | Write the file |
| `AGT008` | A section exists but has no content under it | Write the content |

Required section order: `Role`, `Triggers`, `Hard Rules`, `Workflow`, `Output Contract`,
`Refusals`.

## SKL - the skill pack

`tools/validators/validate_skills.py`

| Code | Meaning | Fix |
|------|---------|-----|
| `SKL001` | A skill directory has no `SKILL.md`, or the pack README is missing | Add the file |
| `SKL002` | Frontmatter is missing `name` or `description` | Add the key |
| `SKL003` | Frontmatter carries a key other than `name` and `description` | Remove the extra key |
| `SKL004` | A required section is missing or has no content | Write the section |
| `SKL005` | The required sections are not in the required order, or one is repeated | Reorder to the fixed order |
| `SKL006` | A referenced script does not exist inside the skill directory | Add the script or drop the reference |
| `SKL007` | The frontmatter `name` does not match the directory name | Rename one of them |
| `SKL008` | The description is shorter than 40 characters | Write a real description |
| `SKL009` | The skill directory holds a stray top-level file | Move it into `scripts/` or delete it |

Required section order: `When to use`, `Inputs`, `Procedure`, `Outputs`, `Verification`.

## CUR - the module graph

`tools/validators/validate_curriculum.py`

| Code | Meaning | Fix |
|------|---------|-----|
| `CUR001` | `curriculum/curriculum.yaml` is missing, unparseable or has no `modules` list | Fix the manifest |
| `CUR002` | A module is missing a required field, or the field has the wrong type | Add `id`, `slug`, `dir`, `title`, `hours`, `prereqs`, `gate` |
| `CUR003` | Two modules share the same id | Give one module a new id |
| `CUR004` | A prereq names a module id that does not exist | Fix the id or add the module |
| `CUR005` | The prerequisite graph contains a cycle | Break the cycle |
| `CUR006` | Two modules share the same gate id | Give one module a new gate id |
| `CUR007` | A module directory, its `module-note.md` or its `gate.md` is missing | Create the file |
| `CUR008` | A note or gate is missing a section, has an empty one, or has them out of order | Restore the section order |
| `CUR009` | A module's prereq does not come earlier in the series order | Reorder the manifest |

Module note sections: `What`, `Why it comes here`, `What gets built`, `Acceptance criteria`,
`The artifact`, `Notes`.
Gate sections: `Time box`, `The task`, `Then answer out loud`, `Pass`, `Fail`.

## PRJ - the capstone briefs

`tools/validators/validate_projects.py`

| Code | Meaning | Fix |
|------|---------|-----|
| `PRJ001` | A brief is missing a required section, or cannot be read | Add the section |
| `PRJ002` | The sections are not in the required order | Reorder them |
| `PRJ003` | "Acceptance criteria" holds fewer than five checklist items | Write the criteria |
| `PRJ004` | "Modules exercised" names a module id that is not in the series | Fix the id |
| `PRJ005` | The rubric table holds fewer than three body rows | Write the rubric |
| `PRJ006` | The rubric weights do not sum to 100 | Fix the weights |
| `PRJ007` | The rubric table is missing a required column | Add `Criterion`, `Weight`, `What the evidence must show` |

## LNK - the Markdown links

`tools/validators/validate_links.py`

| Code | Meaning | Fix |
|------|---------|-----|
| `LNK001` | A relative link does not resolve to a file in the repository | Fix the path or create the file |
| `LNK002` | A relative link escapes the repository root | Point it back inside the repository |
| `LNK003` | A fragment anchor does not exist in the target document | Fix the anchor or add the heading |
| `LNK004` | A link points at a directory with no index document | Add `index.md` or link the file directly |

## REC - the documentation record

`tools/validators/validate_records.py`

| Code | Meaning | Fix |
|------|---------|-----|
| `REC001` | A required record file is missing or empty | Write the record |
| `REC002` | An inventory row names a file that does not exist | Fix or drop the row |
| `REC003` | An inventory row has an empty column or fewer than four columns | Fill the row |
| `REC004` | A tracked Markdown or Python file has no inventory row | Add the row |
| `REC005` | A decision log entry records no prompt | Add the "Prompt that produced it" section |
| `REC006` | A decision log entry records no date | Add the `**Date:**` line |

## VAL - the runner

`tools/validators/run_all.py`

| Code | Meaning | Fix |
|------|---------|-----|
| `VAL000` | A validator crashed | Read the traceback in the message and fix that validator |

`VAL000` is reported instead of aborting the run, so one broken rule cannot hide the others.
