# CAPSTONE - Polymath Capstone

## What

One feature, shipped, in one repository, that exercises every module in the series. Not
ten small projects. One feature with a real user, a schema, a model or prompt, a
deployment, a price and a plan for the day it goes wrong.

The capstone is where the series stops being modules. Up to here, each artifact stood
alone: a service without a user, an eval harness without a product, a cost model without
a rollout. The capstone is the assembly, and the assembly is where the seams show. A
typed boundary that did not fit the tool interface. A split policy that did not survive
the live traffic. A threshold that was right in the notebook and wrong in the product.

What you ship is a feature plus an **evidence bundle**: every artifact from the ten
modules, in one place, in a state somebody else can read, and a **retrospective** that
says what broke and what you would change.

## Why it comes here

Every module in the series was written to be combined here. Each gate certifies that you
can build that piece; this module certifies that you can build the thing.

What breaks without it:

- **A portfolio of parts with no whole.** Ten artifacts that each pass their gate and
  cannot be assembled.
- **A feature that only works on the author's machine.** The hardcoded path, the missing
  migration, the prompt that assumed one dataset.
- **An argument you cannot support.** When someone asks why the feature should ship, the
  evidence bundle answers with artefacts instead of recollection.
- **No practice at the failure.** Every module has a fail branch. The capstone is where
  a learner has to have already met one.

## What gets built

A single AI feature that you choose, scoped so it can be shipped and narrow enough to
exercise every module:

- the service, its schema and its migrations (P0);
- the mathematics and the checks behind whatever the feature computes (P1);
- the dataset, the split policy, the leakage audit and the feature pipeline (P2);
- the baseline and the tuned model, or the prompt and its variant, with the threshold
  justified (P3);
- the reproducible training loop, if the feature trains anything (P4);
- the tokeniser, the attention implementation and the sampling harness, or the
  documented use of them (P5);
- the structured-output and tool-use service with its guardrails (P6);
- the eval harness with the case set, the rubric and the regression gate (P7);
- the deployment, the dashboards, the cost model and the rollback plan (P8);
- the spec, the rollout plan, the price and the failure message (P9);
- an evidence bundle and a retrospective.

## Acceptance criteria

- The feature runs from a clean checkout with one documented command, and the test suite
  passes offline.
- Every acceptance criterion from every module note is met by something in the evidence
  bundle, and the bundle lists them one by one with a pointer to where each is satisfied.
- The eval harness runs against the deployed service, not against a notebook, and the
  regression gate is wired into CI.
- The rollout plan names the phases, the thresholds and the kill switch, and the failure
  message is dated and ready to send.
- The retrospective states, for every module: what worked, what broke, what the numbers
  were, and what you would change. At least three entries are about something that
  genuinely surprised you.
- The numbers you quote come from a recorded run, not from memory, and anything from a
  mock provider is labelled `SIMULATED`.
- A reviewer who has not seen your work can read the bundle and understand the feature
  in ten minutes, including why it should ship.

## The artifact

A repository, a deployment, an evidence bundle and a retrospective. The bundle is the
deliverable that carries the weight: it is what makes your work checkable by somebody
else, and it is what the capstone rubric is applied to.

Keep the evidence: the bundle index, the scorecard from the eval harness, the cost model
with its worked example, the rollback rehearsal notes, the rollout plan, the dated
failure message, and the retrospective.

## Notes

- Choose a feature you can explain in one sentence; a paragraph means two.
- Reuse the artifacts from your gates. The point of the capstone is that they fit
  together, and rewriting them from scratch hides the seams you are supposed to find.
- Scope the *user* before the *model*. A feature with one user and a clear job is
  finishable; a feature with a market is not.
- The gate for this module is [GCAP](gate.md). The time box is 180 minutes. The
  capstone rubric ships alongside this note.
