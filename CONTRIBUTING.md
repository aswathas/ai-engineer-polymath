# Contributing

The short version: read [AGENTS.md](AGENTS.md), make one meaningful change, verify it, record
it, commit it.

## Before you start

- Read [AGENTS.md](AGENTS.md). The rule that overrides everything: the learner writes the code.
- Check [curriculum/curriculum.yaml](curriculum/curriculum.yaml) for where your change belongs.
- If your change is a *choice* rather than a typo, it goes in
  [docs/reviews/decision-log.md](docs/reviews/decision-log.md) with the prompt that produced it.

## Verification, in this order

```bash
ruff check .
pytest -q
python tools/validators/run_all.py
```

All three must be clean. The third is the one that catches curriculum drift: it fails when a
module note and its gate disagree, when a skill points at a script that does not exist, or when
a link rots.

## What a change needs

| Change | Needs |
|--------|-------|
| New module or gate | Module note, gate, `curriculum.yaml` entry, resources list |
| New agent | File in `agents/` with the fixed sections, and an entry in `agents/README.md` |
| New skill | `skills/<name>/SKILL.md` with the fixed sections; any script it references must exist |
| New validator code | Stable code, tests that assert on that code, and a line in `docs/validator-reference.md` |
| New file of any kind | A row in [docs/reviews/change-inventory.md](docs/reviews/change-inventory.md) |
| New dependency | An ADR in `docs/adr/` |

## Committing

One meaningful unit per commit. Conventional subject, a body that says what and why, and the
co-author trailer:

```bash
git add <paths>
git commit -m "feat: add P3 module note and gate" \
  -m "Adds the P3 teaching note, its time-boxed G3 gate and the curriculum.yaml entry. Records the row in the change inventory and the choice in the decision log." \
  -m "Co-Authored-By: MiniMax Code <noreply@minimax.ai>"
```

Never amend a published commit. Fix a published mistake with a follow-up commit that says which
commit it repairs.

## Pushing

Branch first, then push, then open the pull request:

```bash
git checkout -b feature/<what-changed>
git push -u origin feature/<what-changed>
gh pr create --fill
```

Before the push, run the checker:

```bash
python <aswath-commit-discipline>/scripts/check_push.py --repo .
```

It is read-only and never blocks; it warns about the documentation gaps that a reviewer would
otherwise find.

## Style

- Prose in the voice of the series: direct, specific, no filler. Say what breaks without the
  thing being taught.
- Every public function in `tools/` has a docstring that says what it does, what it returns and
  what it costs.
- One writer per file. If work is parallelised, the file ownership is disjoint and explicit.
- No paid API calls, no vendored binaries, no secrets. Mock providers only, and every number
  from a mock is labelled `SIMULATED`.
