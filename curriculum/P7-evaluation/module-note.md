# P7 - Evaluation

## What

Evaluation is the part of AI engineering that turns opinion into evidence. Before this
module, "the model got better" is a feeling. After it, it is a number with a dataset
behind it, a rubric, and a threshold that blocks a release when the number drops.

The module delivers a working harness with three parts. An **offline case set**: a fixed
set of inputs with the properties you care about, including the hard ones. A **judge
rubric**: a written standard for what a good answer looks like, and a judge - human or
model - that applies it consistently. A **regression gate**: a threshold in CI that fails
the build when quality drops.

The uncomfortable part is that a harness is only as good as its cases. A case set of ten
happy-path examples measures nothing but the happy path. The work is in the cases you did
not enjoy writing.

## Why it comes here

P6 built a service whose output is a judgement call, not a number: which summary is
better, whether the tool call was the right one, whether the answer is grounded in the
source. Without a measurement, every change to the prompt, the model or the schema is a
gamble with production as the table.

What breaks without this module:

- **A change shipped on faith.** The prompt was "improved", the demo looked better, and
  the failure rate on real traffic went up. Nobody can tell which change caused what.
- **An eval that measures the model, not the product.** The metric improved and the
  feature did not, because the eval scored the answer in isolation while the product
  shows the answer next to five other things.
- **A benchmark number that means nothing.** A public benchmark score is reported in a
  readme and never compared against the private case set that reflects your users.
- **A flaky harness.** The gate fails one run in ten, so the team learns to re-run it. A
  gate that cries wolf is a gate that is ignored, and the next real regression ships.
- **An LLM judge with no rubric.** Asked to "rate the quality" the judge drifts with the
  prompt order and its own mood. Scored against a written rubric, it becomes at least
  consistent, and testable.

## What gets built

- A case set: a versioned file of inputs with expected properties, covering the common
  cases, the edge cases, and the known failures of the current system.
- A rubric: written criteria for what a good output looks like, with the decision
  boundary spelled out.
- A judge, either a rubric applied by a model or a human, with a small agreement study
  against your own labels.
- A runner that executes the case set against the service and produces a score per case
  and per slice.
- A regression gate: a threshold, wired into CI, that fails on a quality drop and passes
  on a quality rise within noise.
- A noise estimate: how much the score moves when you re-run the same cases unchanged.

## Acceptance criteria

- The case set is versioned, and every case has an id, an input, and the property it is
  meant to probe. Cases are not deleted when they fail; they are marked.
- The rubric is written before the judge is configured, and every criterion is stated in
  a way that two people would apply the same way.
- The judge's agreement with your own labels is measured and reported. If it is poor, you
  say so, and the affected criteria are fixed or dropped.
- The runner reports a score per case, a score per slice, and an overall score, with the
  case count next to every number.
- You measured the noise: re-running the unchanged case set gives a score spread, and
  the regression threshold is set above that spread.
- The gate fails the build when a deliberately degraded model is swapped in, and passes
  when the real model is restored. You checked both directions.
- Slice scores are reported separately from the overall score, and at least one slice
  disagrees with the overall score in your data.

## The artifact

A harness somebody else can run: a command that takes the current service, runs the case
set, and prints a scorecard with an overall score, per-slice scores, the case count and
the noise band. Wired into CI as a gate.

Keep the evidence: the case set with its version, the rubric, the judge agreement study,
the noise measurement, and the two gate runs - the failing one and the passing one.

## Notes

- A case set of 20 cases that probe the right behaviours beats 500 cases that are
  variations of the same one. Write the cases you expect to fail first.
- Judge agreement is a number you should be allowed to be disappointed by. Report it.
- Keep the harness deterministic where you can: fixed seeds, fixed model version, fixed
  judge prompt, and a temperature of zero.
- Model versions drift. Pin what you can, and record the version in every scorecard.
- Any score from a mock provider is labelled `SIMULATED`.
- The gate for this module is [G7](gate.md). The time box is 180 minutes.
