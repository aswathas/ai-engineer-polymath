# CAPSTONE rubric

## How a judge uses this

Judge the evidence, not the prose. Read the evidence bundle first: the eval output, the test run,
the cost model, the incident note. Score each criterion in the table below. The score is the
weighted sum out of 100.

Three rules for the judge:

1. A criterion with no evidence scores zero. Missing evidence is not weak evidence.
2. A number that no run in the evidence bundle backs does not count, however plausible it looks.
3. If the submission breaks a rule in the Disqualifying list, return that disqualification instead
   of a score.

The rubric is deliberately harsh on honesty. A submission that names its limits scores higher than
one that claims to have none.

## Rubric

| Criterion | Weight | What the evidence must show |
| --- | --- | --- |
| Correctness of the shipped feature | 20 | The feature working end to end, the test run that proves it, and the failure modes it was tested against. |
| Evaluation quality | 20 | A held-out set, metric definitions with thresholds, a baseline to compare against, and error analysis over the failures. |
| Reliability under failure | 20 | What happens when the provider, the network or the data degrades: retries, fallbacks, timeouts, and a rollback that has been rehearsed. |
| Cost model and efficiency | 15 | A per-unit cost model with the assumptions named, and the sensitivity of that cost to volume and to the choices made. |
| Documentation and operability | 15 | A runbook, a config reference, and a written reason for every non-obvious decision, so another engineer can run it. |
| Honesty about limits | 10 | The known failure modes, the cases the system refuses, and the regressions the eval would not catch. |

## Disqualifying

A submission is disqualified, not merely marked down, when any of these is true:

- **A paid API was used and not disclosed.** If a real paid provider was called and the fact is
  not stated plainly, the submission is out.
- **The eval measures the training data.** An eval whose test set overlaps its training set, or
  whose questions were written by looking at the answers, does not count as an eval.
- **No rollback plan.** A feature that cannot be reverted, with a written trigger and a step, is
  not shippable, so it cannot pass this gate.
- **A number published without the `SIMULATED` label.** Any figure taken from a mock provider.
- **A secret in the repository.** Any key, token or credential committed to the tree.
- **Work that was not done by the learner.** An implementation written by someone else breaks the
  rule in [AGENTS.md](../../AGENTS.md).
