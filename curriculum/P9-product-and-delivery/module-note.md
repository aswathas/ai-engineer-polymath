# P9 - Product and Delivery

## What

The last module before the capstone is about the decisions that decide whether the feature
should exist at all. A model that scores well is not a product. A product needs a user, a
problem worth the cost, a price, a rollout that can be stopped, and a plan for the day it
fails in public.

Four deliverables: a product spec, a rollout plan, a price, and a failure communication
draft. Each one is a document you can be held to.

This module is where AI-specific product judgement appears. A traditional feature either
works or raises an error. A model-backed feature is *sometimes wrong*, and the product
question is what the interface does about that: what the user sees, what they can correct,
what the system does with the correction, and who carries the cost when it is wrong.

## Why it comes here

P8 gave you a deployed service with a dashboard, a cost model and a rollback. P9 turns
that into a promise to a user. The technical work is nearly done; the decisions that
remain are the ones with no default answer.

What breaks without this module:

- **A feature built for a problem nobody has.** The model is excellent and the usage is
  three requests a day, and nobody can say what the user would have done otherwise.
- **A rollout with no stopping condition.** The plan says "roll out to 100% over two
  weeks" and does not say what happens if the quality score falls, or who can stop it, or
  how fast.
- **A price that ignores the model.** A per-seat price on a product whose marginal cost
  is per request, and whose expensive path is the one your heaviest user takes.
- **An error with no product answer.** The model returns a wrong answer and the interface
  presents it with the same confidence as a right one. The user trusts it, and you find
  out from a complaint.
- **Silence after an incident.** The feature was wrong for four hours and nobody told
  anyone, because no one had written the message in advance. Users who found out from a
  forum are worse than users who were told.

## What gets built

- A product spec: the problem, the user, the non-goals, the user-visible behaviour, the
  failure behaviour, and the acceptance criteria.
- A rollout plan: phases, cohorts, the metric and the threshold that advance each phase,
  the kill switch, and who holds it.
- A price: unit economics per user segment, with the cost model from P8 plugged in.
- A failure communication draft: the message you would send if the feature is wrong for a
  defined period, written before it happens.

## Acceptance criteria

- The spec names the problem in the user's words, not the model's, and states at least
  three non-goals.
- The spec describes what the user sees when the model is uncertain or wrong, and what
  the user can do about it. "Show an error" is not enough; the interface has to support
  correction, and the correction has to feed something.
- The spec has acceptance criteria that a test could check, not adjectives.
- The rollout plan has at least three phases, with the metric, the threshold and the
  observation window for each, and the phases are written so that any phase can be
  stopped without the others.
- The kill switch is named, and one person is named as holding it.
- The price is computed from the P8 cost model per segment, and shows the margin at the
  assumed volume. If the margin is negative in a segment, you say so and price or
  restrict it.
- The failure communication draft says what broke, what was affected, what you did, and
  what you changed, in plain language and without blaming the model. It is dated and
  ready to send.
- Every figure in the price and the rollout plan is labelled `SIMULATED` when it comes
  from a mock provider.

## The artifact

Four documents: a spec, a rollout plan, a price and a failure message. Together they are
the artifact you take into a product review, and the one the capstone builds on.

Keep the evidence: the spec, the plan with its thresholds, the unit-economics sheet, and
the dated failure message draft.

## Notes

- Talk to users before you write the spec. The module assumes you did; if you did not,
  the spec is a guess with a nice structure.
- AI features are probabilistic, so the spec should describe a distribution of
  behaviour, not a single expected output. "Cites a source for every claim" is testable;
  "is accurate" is not.
- Price the segments that cost you money. The heaviest user is often a robot, and
  sometimes it is your most important customer.
- Write the failure message while nothing is on fire. Editing a message during an
  incident is how you publish something you regret.
- The gate for this module is [G9](gate.md). The time box is 150 minutes.
