# AI Engineer Polymath

**One engineer. Ten domains. One shipped AI feature.**

A standalone curriculum series that takes an engineer from "I can call an API" to "I shipped an
AI feature that survived contact with users, budget and reality". Every module ends in a
**gate**: a time-boxed build that passes or the series stops. No notebooks, no toy prompts, no
"and now let's try it with LangChain".

The repository is both the curriculum and the toolchain that keeps it honest. The agents and
skills that teach the series live here, and the validators in `tools/validators/` check that
the teaching material still matches the contracts it claims to satisfy. The repository fails its
own CI when it drifts.

| | |
|---|---|
| Series | Polymath AI Engineer (`P0`-`P9`, `CAPSTONE`) |
| Modules | 10 + capstone, each with a gate (`G0`-`G9`, `GCAP`) |
| Total time | ~450 h of deliberate practice, plus a 60 h capstone |
| Stack | Python 3.12 · pytest · ruff · PyYAML · GitHub Actions |
| Cost rule | No paid API. Mock providers and free tiers only |
| Plan | [plan.md](plan.md) - the canonical implementation plan |
| Records | [decision log](docs/reviews/decision-log.md) · [change inventory](docs/reviews/change-inventory.md) · [prompts](docs/reviews/prompts.md) |

---

## Why this exists

Most AI curricula teach one slice: prompt engineering, or a framework, or a model card. A
production AI feature needs all of them at once, and it fails at the seam between them - the
schema that a model returns 3% of the time, the dataset with leakage, the eval that measures the
wrong thing, the bill nobody modelled.

"Polymath" is the argument that the engineer, not the model, is the unit of competence. An
engineer who owns P0 through P9 can take a feature from a vague request to a monitored,
measured, priced, rollback-able system.

## The modules

| Id | Module | Gate | You ship |
|----|--------|------|----------|
| P0 | [Engineering Spine](curriculum/P0-engineering-spine/module-note.md) | G0 | A typed service with retries, idempotency, a Postgres schema and a real test suite |
| P1 | [Math for ML](curriculum/P1-math-for-ml/module-note.md) | G1 | A numerically careful optimiser and gradient checks that catch a wrong derivative |
| P2 | [Data and Features](curriculum/P2-data-and-features/module-note.md) | G2 | A labelled dataset, a split policy, a leakage audit and a feature pipeline |
| P3 | [Classical ML](curriculum/P3-classical-ml/module-note.md) | G3 | A baseline and a tuned model, calibrated thresholds, an error analysis |
| P4 | [Deep Learning](curriculum/P4-deep-learning/module-note.md) | G4 | A reproducible training loop with checkpoints and regularisation |
| P5 | [LLM Mechanics](curriculum/P5-llm-mechanics/module-note.md) | G5 | A tokeniser, an attention implementation, a sampling harness with an eval |
| P6 | [LLM Application Engineering](curriculum/P6-llm-application-engineering/module-note.md) | G6 | A structured-output and tool-use service with guardrails |
| P7 | [Evaluation](curriculum/P7-evaluation/module-note.md) | G7 | An eval harness: offline suite, judge rubric, regression gate |
| P8 | [Production and Cost](curriculum/P8-production-and-cost/module-note.md) | G8 | A deployed service, dashboards, a cost model, a rollback plan |
| P9 | [Product and Delivery](curriculum/P9-product-and-delivery/module-note.md) | G9 | An AI product spec, a rollout plan, a price, a failure comms draft |
| CAPSTONE | [Polymath Capstone](curriculum/capstone/module-note.md) | GCAP | One shipped AI feature with an evidence bundle and a retrospective |

Full graph, prereqs and hours: [curriculum/curriculum.yaml](curriculum/curriculum.yaml).
Overview and how to use the series: [curriculum/overview.md](curriculum/overview.md).

## Capstone projects

| Project | Modules | Brief |
|---------|---------|-------|
| PJ1 | Retrieval QA service | [brief](projects/PJ1-retrieval-qa-service.md) |
| PJ2 | Support triage with human handoff | [brief](projects/PJ2-support-triage.md) |
| PJ3 | Eval-driven prompt and model release | [brief](projects/PJ3-eval-driven-release.md) |

Overview and how to pick one: [projects/overview.md](projects/overview.md).

## The agent pack

Six agents, one rule each, all in [agents/](agents/README.md):

| Agent | Job |
|-------|-----|
| `polymath-tutor` | Teaches a module. Never writes the learner's implementation |
| `polymath-reviewer` | Reviews learner work against the gate criteria |
| `polymath-quiz-master` | Writes quizzes with an answer key and a rubric |
| `polymath-curator` | Owns the curriculum graph and module drift |
| `polymath-project-supervisor` | Scopes capstones and judges submissions |
| `polymath-eval-auditor` | Designs eval harnesses and audits claims |

The skills that back them live in [skills/](skills/README.md).

## Quickstart

```bash
git clone https://github.com/aswathas/ai-engineer-polymath.git
cd ai-engineer-polymath
python -m pip install -e ".[dev]"
ruff check .
pytest -q
python tools/validators/run_all.py
```

`run_all.py` exits 0 when every contract holds and 1 when something drifted. `--json` prints a
machine-readable report. Every code is explained in
[docs/validator-reference.md](docs/validator-reference.md).

## Repository map

```
agents/      agent definitions (frontmatter + fixed sections)
skills/      skills, each a SKILL.md plus optional scripts
curriculum/  P0-P9 + capstone: module note, gate, resources
projects/    capstone briefs with acceptance criteria and rubrics
tools/       validators and the issue generator
tests/       pytest suite for the validators
docs/        ADRs, agent docs, validator reference, review records
```

## Contributing

Read [AGENTS.md](AGENTS.md) first - it holds the rules that override everything, including the
rule that matters most: **the learner writes the code, the agent never does**. Then read
[CONTRIBUTING.md](CONTRIBUTING.md) for the commit and review workflow. Every change is recorded
in [docs/reviews/](docs/reviews/decision-log.md) before it is pushed.

## What this cannot do

- It does not teach one framework. Frameworks change; the contracts do not.
- It does not run paid models. Every number from a mock provider is labelled `SIMULATED`.
- It does not replace building things. Reading the notes teaches you the shape, not the reflex.
- It does not cover every domain. It covers the ones that decide whether an AI feature works.
- It does not certify anybody. A gate is a self-assessment with a written record, nothing more.

## Licence

MIT - see [LICENSE](LICENSE).
