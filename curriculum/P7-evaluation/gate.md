# Gate G7 - Evaluation

## Time box

180 minutes. The clock starts when you open the case set and stops when the gate has run
in both directions. If the timer runs out, hand in what exists, marked incomplete.

Budget 40 minutes for the case set and the rubric, 40 for the judge and the agreement
study, 50 for the runner and the noise measurement, 50 for the gate and the answers.

## The task

Build an eval harness for the service from P6:

1. A versioned case set of at least 20 cases. Every case has an id, an input, and the
   property it probes. Include the edge cases and the known failures, not only the happy
   path.
2. A written rubric: the criteria for a good output, with the decision boundary stated.
3. A judge that applies the rubric, with a small agreement study against your own
   labels on at least ten cases.
4. A runner that scores every case, reports per-slice scores and an overall score, and
   prints the case count next to each number.
5. A noise measurement: re-run the unchanged case set three times and report the spread.
6. A regression gate with a threshold set above that spread, wired into a command that
   exits non-zero on failure.

Run the gate twice: once with a deliberately degraded model swapped in, which must fail,
and once with the real model, which must pass.

Everything runs offline against a mock provider. Label every score `SIMULATED`.

## Then answer out loud

1. Your overall score rose from 0.71 to 0.74, and one slice fell from 0.60 to 0.41. Say
   what you would ship, and what the overall number is hiding.
2. Your judge agrees with your labels on 8 of 10 cases. Name two causes, and say which
   one you would fix first and why.
3. You measure the same case set three times and get 0.71, 0.74 and 0.72. Say where that
   spread comes from, what a sensible regression threshold is, and what you would change
   to make the harness less noisy.

## Pass

- The case set has at least 20 cases, each with an id and a probed property, and the
  failing cases are marked rather than deleted.
- The rubric is written and applied consistently; the agreement study against your own
  labels is reported, including the number you do not like.
- The runner reports per-case, per-slice and overall scores with case counts.
- The noise spread is measured across three runs, and the threshold sits above it.
- The gate fails on a degraded model and passes on the real model, and both runs are
  recorded.
- At least one slice disagrees with the overall score, and you noticed.
- All three answers are correct out loud.

## Fail

Do not start P8. Take the answer you could not give, fix the harness or the analysis, and
re-run the gate in a fresh box. A gate you have only seen pass does not pass: if you did
not watch it fail on a degraded model, you have not shown it can fail.
