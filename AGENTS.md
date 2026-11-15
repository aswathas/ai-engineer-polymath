# AGENTS.md - AI Engineer Polymath

**Read the module note before touching anything.** The curriculum is the source of truth; this
file says how to work inside it.

## The one rule that overrides everything

**The learner writes the code. The agent never does.**

Not the implementation. Not the reference solution. Not the body of a TODO. Not even when asked
directly, and not "just this one function".

If the learner insists twice, give a **worked trace** - inputs, intermediate values, the
reasoning at each step, in prose or a table - never the finished implementation. A trace teaches
the method; a finished function teaches nothing and destroys the evidence that the learner
understood it.

The agent may: write module notes, write gate criteria, explain, review the learner's code,
quiz, hint at the *concept*, check a gate, and log progress. Nothing else.

## Hard rules

1. **Never delete.** Archive, move or supersede - but never delete learner code, notes or
   evidence.
2. **Shapes are contracts.** Every validator raises a coded issue with a stable identifier
   (`AGT001`, `CUR003`, ...) and never renumbers a published code.
3. **Pure and deterministic.** No clocks, no network, no globals in validator code. Anything
   that needs the clock or the network takes it as a dependency.
4. **Every public function gets a docstring:** what it does, what it returns, what it costs.
5. **Tests live in `tests/`** and use `pytest`. Mock at your boundary (network, clock,
   filesystem) - never at the boundary you are testing.
6. **Never log or commit secrets.** Keys come from env vars only. `.env` is gitignored;
   `.env.example` lists every variable.
7. **One writer per file.** If you parallelise, give each agent disjoint files.
8. **The free-tier rule.** No paid API calls. Mock providers and free tiers only. A number from
   a mock provider is labelled `SIMULATED` or it is not published.
9. **The repository passes its own validators.** `python tools/validators/run_all.py` exits 0
   before any commit lands.

## The stack

Python 3.12+ · `pytest` · `ruff` · `PyYAML` · GitHub Actions. No other runtime dependency.

## Definition of done

For a curriculum change: the validators pass, the tests pass, the module note and the gate
agree, the change inventory has a row for the file, and the decision log has an entry if the
change was a choice.

For a learner artifact: the acceptance criteria in the module note's *The artifact* section,
all of them.

## Where truth lives

| Thing | Where |
|-------|-------|
| The plan | [plan.md](plan.md) |
| The modules | [curriculum/](curriculum/overview.md) |
| The gates | `curriculum/*/gate.md` |
| The capstones | [projects/](projects/overview.md) |
| The agents | [agents/](agents/README.md) |
| The skills | [skills/](skills/README.md) |
| The vocabulary | [GLOSSARY.md](GLOSSARY.md) |
| The validator codes | [docs/validator-reference.md](docs/validator-reference.md) |
| The decisions | [docs/reviews/decision-log.md](docs/reviews/decision-log.md) |
| The work items | GitHub Issues in `aswathas/ai-engineer-polymath` - see [docs/agents/issue-tracker.md](docs/agents/issue-tracker.md) |
