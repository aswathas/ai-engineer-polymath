# PJ3 - Eval-driven prompt and model release

## Goal

Build a release pipeline for prompts and model choices where a regression gate blocks a change that
would degrade a named metric.

The pipeline is the deliverable. A prompt tweak that scores better on one slice and worse on
another must be rejected by the gate, not argued about in a chat window.

## Modules exercised

- P5 - LLM Mechanics
- P7 - Evaluation
- P8 - Production and Cost
- P9 - Product and Delivery

## Acceptance criteria

- [ ] A named metric suite with at least three metrics, each with a fixed definition, a threshold,
      and the reason that metric was chosen.
- [ ] A held-out eval set that the pipeline never tunes against, plus a separate dev set that it
      may use.
- [ ] A regression gate that fails the build when a named metric drops past its threshold, printing
      the failing metric, the baseline value and the new value.
- [ ] A worked example of a change the gate blocked, including the diff that triggered it.
- [ ] A comparison of at least two prompt variants or two model choices on the same suite, with the
      cost and latency of each recorded as SIMULATED figures.
- [ ] A release log recording every promoted and every blocked change, with the metric values at
      promotion time.
- [ ] A rollback procedure naming the trigger, the artefact that is restored and the check that
      confirms the rollback worked.
- [ ] Tests covering the metric computation, the threshold comparison and the gate's pass and fail
      paths.

## Evidence required

- The eval harness, the metric definitions and the thresholds, held in one place.
- The dev and held-out sets, with a note on how they were kept apart.
- The gate implementation and the CI configuration that runs it.
- The blocked-change example, with the printed failure output.
- The comparison table across prompt or model variants, with SIMULATED cost and latency figures.
- The release log and the rollback procedure.
- A short note on the limits of the suite: what it does not measure and which regressions it would
  miss.

## Rubric

| Criterion | Weight | What the evidence must show |
| --- | --- | --- |
| Regression gate integrity | 25 | The gate failing on a real degradation, printing the metric, the baseline and the new value, and the blocked-change example. |
| Metric and eval design | 25 | Fixed metric definitions, thresholds with a stated reason, a held-out set the pipeline never tunes against, and error analysis. |
| Cost and latency model | 15 | A comparison of variants with SIMULATED cost and latency figures and the assumptions behind them. |
| Release process and rollback | 20 | The release log, the promotion criteria, and a rollback procedure with a trigger and a verification step. |
| Documentation and honesty about limits | 15 | A note naming what the suite does not measure and which regressions it would miss. |
