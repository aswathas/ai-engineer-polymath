# Glossary

The vocabulary of the series. One definition per term, and a term means one thing everywhere in
the curriculum. When a module needs a term that is not here yet, that is a signal: either the
module is inventing language the series does not use, or the series has a gap. Both get fixed
here before the term is used.

Terms are written so that a learner can be tested on them.

---

## Agent

A program that acts on the learner's behalf under hard rules. In this repository an agent is a
Markdown file in [agents/](agents/README.md) with a role, triggers, hard rules, a workflow, an
output contract and an explicit list of refusals.

**Not:** the learner's assistant in general. **Not:** a model. An agent here is a contract with
a prompt.

## Artifact

The thing the learner ships in a module or project. Every module names exactly one artifact and
lists acceptance criteria for it. An artifact is code, a dataset, a report, or a design
document - never a note about what the code would have done.

## Capstone

The final project of the series, spanning `P0`-`P9`, with its own gate `GCAP` and its own rubric.
See [curriculum/capstone/module-note.md](curriculum/capstone/module-note.md).

## Eval (evaluation harness)

A versioned set of cases, a metric, a baseline and a threshold, runnable on demand so that a
change can be judged instead of argued about. "It felt better" is not an eval.

## Gate

A time-boxed build that ends a module. A gate passes or the series stops; there is no partial
gate. Gates are named `G0`-`G9` for modules and `GCAP` for the capstone.

## Judge rubric

The written criteria a judge (human or model) applies to an artifact, with weights, so that two
judges can reach a comparable answer.

## Leakage

Information that reaches the training or evaluation data that would not be available at
prediction time. Leakage makes a metric a lie. Detecting it is part of P2 and checked again in
every gate that measures something.

## Module

One stage of the series: a module note, a gate, and a resource list. Modules are ordered by
prerequisite, never by topic, and the order is in
[curriculum/curriculum.yaml](curriculum/curriculum.yaml).

## Module note

The teaching document for a module: what it is, why it comes first, what gets built, and the
acceptance criteria. The template is
[curriculum/templates/module-note.md](curriculum/templates/module-note.md).

## Polymath

The engineer who can hold the whole stack - engineering, mathematics, data, classical ML,
deep learning, LLM mechanics, application engineering, evaluation, production, product - at
once. The series exists to build one.

## Guardrail

A rule that constrains what a system may do at runtime: a schema check, a tool allow-list, a
rate limit, a refusal. Guardrails are tested; they are not intentions.

## Regression gate

An eval threshold that blocks a release when quality drops below it. A regression gate that
cannot block anything is a report, not a gate.

## SIMULATED

The label on any number produced by a mock or fake provider. A `SIMULATED` number may be
printed in teaching material; it may never be presented as a real-world result.

## Split policy

The declared rule for dividing data into train, validation and test sets, including what is
grouped, what is time-based, and what is never touched until the final evaluation.

## Tool use

A model's call to an external function with typed arguments. Tool use is a contract: the
arguments are validated, the result is bounded, and the failure path is specified.

## Worked trace

The teaching form used instead of code when a learner insists on an implementation: inputs,
intermediate values, and the reasoning at each step. It teaches the method; the code is the
learner's job.
