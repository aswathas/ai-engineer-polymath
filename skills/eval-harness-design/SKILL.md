---
name: eval-harness-design
description: Use when an evaluation harness is being designed, so every metric is bound to a dataset, a baseline, a threshold and a regression gate.
---

# Eval Harness Design

## When to use

Use this skill when an eval harness is being designed, reviewed or criticised, and
whenever a metric claim is made without a dataset behind it.

## Inputs

- The capability under test and the change the harness must be able to judge.
- The dataset the harness runs on, and how it was split.
- The baseline the current system achieves on that dataset.
- The judge, human or model, and the rubric it applies.

## Procedure

1. Write the case set: the cases, their inputs, and the expected observable behaviour
   for each. A case without an expected result is not a case.
2. Name the split policy and state what is grouped, what is time-based and what was
   never touched until the final evaluation. Check the case set against that policy
   for leakage.
3. Choose one primary metric and say what a larger value means. Add a secondary metric
   only when it changes a decision.
4. Record the baseline: the metric value the current system produces on the same case
   set, together with the command that produced it.
5. Set the threshold: the metric value below which the change is rejected. The
   threshold is a number, not an intention.
6. Write the judge rubric: the criteria a judge applies, the weights and the scale.
   Say how a human judge and a model judge are reconciled on the same cases.
7. Define the regression gate: the command that runs the suite, the exit code that
   blocks a release, and where the result is recorded.
8. Run the harness end to end once against the baseline and confirm it reproduces the
   baseline value. A harness that cannot reproduce its own baseline is not a harness.

## Outputs

- An eval harness definition: case set, metric, baseline, threshold, judge rubric and
  regression gate.
- A recorded baseline value with the command that produced it.
- A regression gate that can block a release.

## Verification

- Every metric names its dataset, its baseline and its threshold. A metric without a
  dataset and a baseline is rejected.
- The threshold is a number the current system already meets or exceeds.
- The regression gate exits non-zero on a regression, demonstrated by running it
  against a deliberately broken case.
- Every number produced by a mock provider is labelled `SIMULATED`.
