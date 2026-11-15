# Gate G3 - Classical ML

## Time box

150 minutes. The clock starts when you load the P2 pipeline and stops when the tuned model
and the error analysis are written. If the timer runs out, hand in what exists, marked
incomplete.

Budget 30 minutes for the baselines, 40 for the search, 30 for calibration and the
threshold, 40 for the error analysis, 10 for the answers.

## The task

Using the pipeline, splits and dataset from P2:

1. Fit a majority-class baseline and a linear baseline. Score both on the test split.
2. Run a hyperparameter search on the training split with cross-validation, using a fixed
   seed. Record the search space and the selection rule.
3. Calibrate the tuned model's probabilities. Report a reliability diagram and a Brier
   score before and after.
4. Choose a threshold from an explicit cost matrix you write down. Report precision,
   recall and predicted volume at that threshold and at two others.
5. Produce a slice table over at least three business-meaningful slices, with sample
   counts, and write up one surprising error class with a hypothesis and a next
   experiment.
6. Save the fitted model with its pipeline, seed and metrics, and prove it reloads and
   re-scores to the same number.

Everything runs offline. Synthetic data is fine; label invented figures `SIMULATED`.

## Then answer out loud

1. Your tuned model scores better than the linear baseline on F1 but loses to it on the
   metric that actually matters for the business. Explain how that happens, and say
   which number you would put in front of the business owner.
2. You picked a threshold of 0.6. At 0.4 the recall rises and the review queue triples.
   Name the two different things that number is, and say which one belongs in the
   product requirement and which belongs in the model card.
3. A slice with four examples has a 100% error rate. A slice with four thousand has a
   2% error rate. Why is the first one more dangerous than it looks, and what would you
   do before reporting either?

## Pass

- The comparison table shows the baseline, the linear model and the tuned model on the
  same metric.
- The test split was scored once, after the search, and the search log shows the
  validation-only selection.
- Calibration is measured before and after, with a reliability diagram and a Brier score.
- The threshold comes from a written cost matrix, and two alternative thresholds are
  reported.
- The slice table has three slices with counts, and one error class is written up with a
  hypothesis and a next experiment.
- The saved model reloads and re-scores to the same number.
- All three answers are correct out loud.

## Fail

Do not start P4. Take the answer you could not give, fix the model or the analysis, and
re-run the gate in a fresh box. A tuned model with no baseline in the same table is an
automatic fail, however good the score looks.
