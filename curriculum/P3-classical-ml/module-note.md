# P3 - Classical ML

## What

Classical machine learning is where you learn to be suspicious of your own model. The
methods are old and well understood, which is exactly why they are the right place to
learn the habits that still matter when the model is a language model: fit a baseline
before anything clever, tune against a validation set rather than the test set, turn
scores into thresholds you can defend, and look at the errors instead of the aggregate.

A baseline is not a formality. It is the number that tells you whether the model is
earning its complexity. A tuned model that loses to the majority-class rule is a model
you should not ship, whatever its architecture.

## Why it comes here

P2 gave you clean splits and a pipeline, which is exactly what makes a comparison
possible. P4 introduces networks with a hundred ways to overfit and no gradient-descent
sanity check; the habits from this module are what keep that from becoming a week of
tuning by hand.

What breaks without this module:

- **A model with no floor.** Without a baseline, a 0.84 F1 has no meaning. If the
  majority class scores 0.86, the model is worse than doing nothing.
- **A threshold picked by the default.** A classifier returns 0.62 and you decide that
  means "yes". In a cost-asymmetric problem that single choice moves more money than the
  entire model.
- **A confidence number that lies.** An uncalibrated model's probabilities are not
  frequencies. "0.9" on a class with a 20% base rate may mean the model has never been
  right about that class.
- **An error analysis that is really a data dump.** "Accuracy is 82%" tells you nothing
  about which 18% you lose, and the slice that matters most is the one nobody reports.
- **Hyperparameters tuned on the test set.** The test set becomes a validation set, its
  score becomes optimistic, and the gap to production arrives on launch day.

## What gets built

- Two baselines: a majority-class rule and a simple linear model on the P2 pipeline.
- Cross-validation over the training split, with a fixed seed.
- A hyperparameter search that touches the validation split only.
- Probability calibration, measured with a reliability diagram and a Brier score.
- A threshold chosen from a cost matrix, not from the default.
- An error analysis: a slice table by the features that matter to the business, plus a
  written list of the failures that surprise you and your hypotheses about them.

## Acceptance criteria

- Both baselines are trained and scored, and the tuned model is compared against them in
  one table with the metric you care about.
- Hyperparameters are selected on the validation split, and the test split is touched
  exactly once, at the end.
- Calibration is measured before and after, with a reliability diagram and a Brier score.
  You state whether calibration improved and by how much.
- The threshold is derived from an explicit cost or capacity matrix, and you report what
  happens to precision, recall and the volume of predictions at two other thresholds.
- The error analysis is a slice table: at least three slices that a business would
  recognise, with the sample count for each, so nobody reads a slice of four rows as a
  finding.
- At least one error class is written up with a hypothesis and a next experiment. "The
  model is bad" is not an error analysis.
- Every model is saved with its fitted pipeline, the seed, and the metrics, and can be
  reloaded and re-scored.

## The artifact

Two things side by side: a baseline and a tuned model, with the table that compares them,
a calibrated threshold with the reasoning behind it, and an error analysis that ends in
two concrete next experiments.

Keep the evidence: the comparison table, the reliability diagram before and after
calibration, the slice table, and the saved model file with its metrics attached.

## Notes

- Measure the baseline first and write the number down. You will want it later, when
  someone asks why the model is worth its cost.
- A threshold is a business decision wearing a technical costume. Write the cost matrix
  down with the people who own the consequences, not with the person tuning the model.
- Cross-validation on a small dataset is noisy. If the fold-to-fold spread is larger
  than the difference between two models, the comparison is not a result.
- Any number you take from a mock provider is labelled `SIMULATED`.
- The gate for this module is [G3](gate.md). The time box is 150 minutes.
