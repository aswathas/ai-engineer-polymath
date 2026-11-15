# ADR 0002 - The validator layer is Python 3.12 with pytest

- Status: accepted
- Date: 2026-11-15
- Deciders: aswathas
- Related: [plan.md](../../plan.md), [decision-log D3](../reviews/decision-log.md)

## Context

The repository has to check its own contracts: the module graph must be acyclic, the agent and
skill packs must keep their format, every link must resolve, and every tracked file must have a
row in the change inventory. Those checks need a language, a test runner and a place to run in
CI.

The curriculum itself is Python-first, and the series teaches Python. A validator written in
another language would put the tooling of the course outside the course.

## Decision

Python 3.12 or newer, `pytest` for the test-suite, `ruff` for lint, and `PyYAML` as the only
runtime dependency. The validators live in `tools/validators/` and expose one contract:

```python
def validate(repo_root: Path) -> list[Issue]: ...
```

`run_all.py` discovers the validators, aggregates their findings, and exits `0` or `1`.
CI runs `ruff check .`, `pytest -q` and `python tools/validators/run_all.py`.

## Consequences

- One stack for the curriculum, the validators, the tests and the CI. A learner who knows the
  course stack can read the course tooling.
- No network access in any validator, no clock, no globals: a validator run on two machines
  produces the same findings, which is what makes the repository self-hosting.
- A new runtime dependency needs an ADR. `PyYAML` is the only one.
- Node-based tooling was rejected for v1: two toolchains double the CI surface for no gain in
  what the repository teaches.
