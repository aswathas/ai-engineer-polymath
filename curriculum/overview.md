# AI Engineer Polymath - the series

Ten modules and one capstone. Each module ends in an artifact you ship and a gate you
pass. The series is built around one rule: **the learner writes the code**. An agent can
teach, quiz, review and check a gate; it does not hand you the implementation.

The order is fixed and it is not negotiable at random. Every module assumes the artifacts
of the ones before it, so the graph in [curriculum.yaml](curriculum.yaml) is the source of
truth, not this page.

## How to enter it

You need to be comfortable in Python: functions, classes, type hints, a virtual
environment, and a debugger. You do not need prior machine-learning experience, and you do
not need a GPU. The whole series runs on a laptop with free tools and a mock provider.

You do need the willingness to write tests. Half of this series is about the parts of AI
work that look like plain software engineering, and those parts are the ones that decide
whether your feature survives contact with production.

## The module table

| Id | Module | Hours | Needs | Gate | Artifact |
|----|--------|-------|-------|------|----------|
| [P0](P0-engineering-spine/module-note.md) | [Engineering Spine](P0-engineering-spine/module-note.md) | 40 | none | [G0](P0-engineering-spine/gate.md) | A typed service with retries, idempotency keys, a Postgres schema and a real test suite |
| [P1](P1-math-for-ml/module-note.md) | [Math for ML](P1-math-for-ml/module-note.md) | 45 | P0 | [G1](P1-math-for-ml/gate.md) | A numerically careful optimiser whose gradient checks catch a wrong derivative |
| [P2](P2-data-and-features/module-note.md) | [Data and Features](P2-data-and-features/module-note.md) | 40 | P1 | [G2](P2-data-and-features/gate.md) | A labelled dataset, a split policy, a leakage audit and a feature pipeline |
| [P3](P3-classical-ml/module-note.md) | [Classical ML](P3-classical-ml/module-note.md) | 45 | P2 | [G3](P3-classical-ml/gate.md) | A baseline and a tuned model, calibrated thresholds, an error analysis |
| [P4](P4-deep-learning/module-note.md) | [Deep Learning](P4-deep-learning/module-note.md) | 50 | P3 | [G4](P4-deep-learning/gate.md) | A reproducible training loop with seeds, checkpoints and regularisation |
| [P5](P5-llm-mechanics/module-note.md) | [LLM Mechanics](P5-llm-mechanics/module-note.md) | 45 | P4 | [G5](P5-llm-mechanics/gate.md) | A tokeniser, an attention implementation, a sampling harness with an eval |
| [P6](P6-llm-application-engineering/module-note.md) | [LLM Application Engineering](P6-llm-application-engineering/module-note.md) | 50 | P5 | [G6](P6-llm-application-engineering/gate.md) | A structured-output and tool-use service with guardrails |
| [P7](P7-evaluation/module-note.md) | [Evaluation](P7-evaluation/module-note.md) | 45 | P6 | [G7](P7-evaluation/gate.md) | An eval harness: offline case set, judge rubric, regression gate |
| [P8](P8-production-and-cost/module-note.md) | [Production and Cost](P8-production-and-cost/module-note.md) | 40 | P7 | [G8](P8-production-and-cost/gate.md) | A deployed service, dashboards, a cost model, a rollback plan |
| [P9](P9-product-and-delivery/module-note.md) | [Product and Delivery](P9-product-and-delivery/module-note.md) | 35 | P8 | [G9](P9-product-and-delivery/gate.md) | An AI product spec, a rollout plan, a price, a failure communication draft |
| [CAPSTONE](capstone/module-note.md) | [Polymath Capstone](capstone/module-note.md) | 60 | P0-P9 | [GCAP](capstone/gate.md) | One shipped AI feature spanning every module, with an evidence bundle and a retrospective |

## The gate rule

Every module ends with a gate: a time-boxed build, 90 to 180 minutes, followed by three
questions answered out loud. The build is the proof. The questions check that the learner
understands the decision they just made, so a lucky copy-paste does not pass.

**A failed gate blocks the next module.** The fix comes first. The series is a chain, and
skipping a link is how the rest of it stops making sense.

A gate is generous with format and strict with substance: any implementation counts, as
long as it is the learner's own, it runs, and it does what the module note says.

## The time model

The hours in the table are working hours, not calendar days. They cover reading, building,
reviewing and the gate. Plan on roughly twice the module hours in wall-clock time, because
the debugging is where the time goes.

Modules are not split into lectures and exercises. Each module note carries the teaching
inline: the "Why it comes here" section is the argument, and "What gets built" is the
syllabus. Read the note, build the artifact, run the gate.

Time is the only currency that cannot be bought here. If a module takes longer than its
box, cut scope deliberately and note what you cut. A smaller artifact that you understand
beats a bigger one you copied.

## How the capstones fit

The capstone is one shipped AI feature, not ten small projects. It starts only after the
P0-P9 gates are passed, and it has to touch every module: the service spine from P0, the
data and split policy from P2, the model or prompt from P4 and P5, the structured output
and tool calls from P6, the eval harness from P7, the deploy and cost model from P8, and
the rollout plan from P9.

The capstone ships with an evidence bundle - the artifacts of every module, in one place -
and a retrospective that says what broke, what the numbers were, and what you would do
differently. The rubric for it ships alongside the capstone note.

Three shorter project briefs live outside the module chain and are optional: they are for
a specific module combination when you want extra practice, not a substitute for a gate.

## How a learner proves progress

Proof is a set of artifacts, not a score. For each module, keep:

- the code for the artifact, in a repository with a readable history;
- the test output that shows the acceptance criteria were met;
- the numbers you measured, with anything from a mock provider labelled `SIMULATED`;
- the gate answer, written down: what you built, what broke, what you decided.

A learner proves progress when someone else can read the artifact, run the tests, and see
the same result. If that takes more than ten minutes of explanation, the artifact is not
finished yet.

The manifest ([curriculum.yaml](curriculum.yaml)) is the machine-readable version of this
page: module ids, order, prerequisites, gate ids and hours. It is validated on every
change, so it cannot drift away from the module directories without the build failing.

## The templates

- [Module note template](templates/module-note.md) - the six sections every module note has.
- [Gate template](templates/gate.md) - the five sections every gate has.
- [Resources template](templates/resources.md) - the three lists every module ships.
