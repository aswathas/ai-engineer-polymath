# P8 - Production and Cost

## What

Production is where the artifact from P0 meets the world. A model feature that works on
your machine has to survive concurrency, restarts, a bad release, and a month of traffic
that grows without warning. This module is about the four things you must have before you
call a feature shipped: a deployment, a dashboard, a cost model, and a rollback plan.

The cost model is not a finance exercise. It is a design constraint that arrives late
unless you build it early: a request that costs a cent is a different product from one
that costs a hundredth of a cent. Latency budgets, caching, model choice and prompt size
are all decisions made in the cost model.

The rollback plan is not pessimism. Every release will be a bad release eventually. The
plan is what keeps that event a ten-minute inconvenience instead of a week of archaeology.

## Why it comes here

P7 gave you a harness that tells you whether a change made the feature worse. P8 puts
that harness behind a deployment, so a bad change is caught in minutes rather than in
customer reports.

What breaks without this module:

- **A deployment you cannot undo.** The new prompt is live and the score has dropped,
  but there is no way back except a rebuild from a git tag nobody can find.
- **A dashboard that shows averages.** A p50 of 400ms hides a p99 of 20 seconds, and the
  p99 is where the complaints come from.
- **A cost that surprises you at the end of the month.** Traffic grew, the prompt grew
  with it, and nobody modelled the cost per request, so nobody knew the feature was
  losing money on its busiest day.
- **A change that cannot be isolated.** The new model and the new prompt and the new
  schema went out together, so when quality fell there was no way to tell which one did
  it.
- **No model version in the logs.** A regression appears in the logs and you cannot say
  which model produced the bad output, because the version was never recorded.

## What gets built

- A deployable service: a container, a health check, configuration from the environment,
  and a documented start command.
- Observability: structured logs with a request id, metrics for latency, errors, cost and
  quality, and traces across the model call.
- A dashboard with the numbers that matter: latency percentiles, error rate, cost per
  request, quality score, and the volume of each.
- A cost model: a formula for the cost of one request, from token counts and prices,
  with the inputs you control named and sized.
- A rollback plan: how you turn a release off, how long it takes, what you lose while it
  is off, and the health checks that tell you the rollback worked.
- A canary: a way to send a small share of traffic to the new version and compare.

## Acceptance criteria

- The service starts from a clean checkout with one documented command, and a health
  check endpoint reports readiness separately from liveness.
- Every request carries a request id through the logs, the metrics and the model call, so
  one user complaint can be traced end to end.
- The dashboard shows p50, p95 and p99 latency, the error rate, cost per request, the
  quality score from P7, and traffic volume. No averages where percentiles belong.
- The cost model is a formula with named inputs: tokens in, tokens out, model price,
  cache hit rate, and retry rate. You can plug in a new prompt and get a new number.
- Every model call in the logs records the model version and the sampling parameters.
- The rollback plan is written, timed and rehearsed: you have actually performed a
  rollback and written down how long it took.
- The canary sends a small share of traffic to the new version, and the comparison it
  makes is the one from P7's harness, not a vibe.
- Every cost or throughput figure comes from a mock provider and is labelled `SIMULATED`.

## The artifact

A service you can deploy, a dashboard someone can read at 8am, a cost model with a
formula in it, and a rollback plan you have rehearsed. Four artefacts, one page each.

Keep the evidence: the deployment command and its log, a screenshot or export of the
dashboard with a week of data, the cost model with one worked example, and the notes
from the rehearsal of the rollback, including how long it took.

## Notes

- Deploy to one place first. A single container on one host teaches more than a
  multi-region mesh, and P9 is where the rollout policy gets decided.
- Percentiles, not averages. Always.
- The cost model is only useful if it names the inputs you can change: prompt length,
  number of model calls per request, retry rate, cache hit rate.
- The rollback plan needs a health check that tells you the rollback worked. "It looks
  fine" is not a health check.
- The gate for this module is [G8](gate.md). The time box is 150 minutes.
