# Gate G2 - Data and Features

## Time box

120 minutes. The clock starts when you open the dataset and stops when the pipeline runs
end to end on all three splits and the audit is written. If the timer runs out, hand in
what exists, marked incomplete.

Budget 30 minutes for the dataset and the data dictionary, 30 for the split and the
balance report, 40 for the pipeline, and 20 for the audit.

## The task

Take one small labelled problem - your own, or a synthetic one you generate - and deliver:

1. A labelled dataset with a data dictionary: column, type, meaning, allowed values,
   source.
2. A split policy, reproducible from a seed or a time boundary, with the label
   distribution reported per split.
3. A leakage audit: a table of every feature, where it comes from, and whether it exists
   at prediction time. Remove at least one feature on the strength of the audit, and say
   which.
4. A feature pipeline that fits on the training split only, applies to every split, and
   serialises to one file.
5. A schema validation test that fails when a required column is missing.

Everything runs offline. Use a synthetic generator if you do not have a real dataset, and
label any generated figure `SIMULATED`.

## Then answer out loud

1. Your test score is 0.91 and your validation score is 0.89. A colleague says the split
   leaks. Name three concrete ways a split can leak, and say what you would look at in
   the data to tell them apart.
2. You fit the pipeline on the full dataset by mistake and the test score went *up*. Why
   does that happen, and why is the number worse rather than better?
3. You have a feature that is only populated after the outcome is known. Name two
   realistic sources of that pattern in an ordinary business, and say what you would
   replace the feature with.

## Pass

- The dataset rebuilds from source with one command, and the row count and label
  distribution are asserted in a test.
- The split is reproducible, and the per-split label distribution is written down.
- Every feature has a verdict in the leakage audit, and at least one feature was removed
  because of it.
- The pipeline fits on the training split only, serialises, and re-applies correctly to a
  held-out frame.
- The schema validation test fails when a column is removed.
- All three answers are correct out loud.

## Fail

Do not start P3. Take the answer you could not give, fix the code or the document that
goes with it, and re-run the gate in a fresh box. A leakage audit that lists every
feature as "fine" without a verdict for each one is a fail: P3 will produce a confident
score that nobody can defend.
