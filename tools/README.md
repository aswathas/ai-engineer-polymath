# Tools

The repository's own machinery. Everything here reads the tree and reports; nothing here
deploys, publishes or reaches the network.

## Validators

```
tools/validators/
    common.py               Issue, Result, and the shared parsing helpers
    validate_skeleton.py    SKEL001-SKEL010  the shape of the repository
    validate_agents.py      AGT001-AGT008    the agent pack format
    validate_skills.py      SKL001-SKL009    the skill pack format
    validate_curriculum.py  CUR001-CUR009    the module graph and the module notes
    validate_projects.py    PRJ001-PRJ007    the capstone briefs and rubrics
    validate_links.py       LNK001-LNK004    every relative Markdown link
    validate_records.py     REC001-REC006    the documentation record
    run_all.py              the runner
```

Every validator exposes the same entry point:

```python
def validate(repo_root: Path) -> list[Issue]: ...
```

`Issue` carries a stable `code`, the repository-relative `path` and a `message`. Codes are
published identifiers: they are documented in
[docs/validator-reference.md](../docs/validator-reference.md) and asserted on by the tests, so
they are never renumbered once a reader has seen them.

## Running them

```bash
python tools/validators/run_all.py              # human-readable table, exit 0 or 1
python tools/validators/run_all.py --json       # machine-readable report
python tools/validators/run_all.py --repo ../other-repo
```

A validator that crashes is reported as `VAL000` against that validator instead of aborting the
run, so one broken rule cannot hide the others.

## The issue generator

```bash
python tools/create_issues.py --dry-run     # print the planned issues
python tools/create_issues.py               # create what is missing
```

The generator reads the acceptance criteria out of the module notes and turns each one into a
GitHub issue, blocked by the previous one. It is idempotent by title, so running it twice does
not duplicate work.

## Adding a validator

1. Write `tools/validators/validate_<area>.py` with a `validate(repo_root)` function.
2. Give every finding a **new** code in its own range. Never reuse a published code.
3. Write `tests/test_validators_<area>.py` that asserts on those exact codes.
4. Add the codes to [docs/validator-reference.md](../docs/validator-reference.md).
5. Run `ruff check .`, `pytest -q` and `python tools/validators/run_all.py`.

The runner discovers every `validate_*.py` file, so a new validator is wired in by being
present.
