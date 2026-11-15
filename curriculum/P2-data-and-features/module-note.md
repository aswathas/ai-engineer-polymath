# P2 - Data and Features

## What

Data work is not preparation for the model. It is most of the model. A classifier does not
learn from your code; it learns from the rows you gave it, the rows you held out, and the
columns you built. Get this module wrong and every later number is a measurement of the
wrong thing.

The four deliverables are a labelled dataset, a split policy, a leakage audit and a feature
pipeline. They are separate because they fail separately. A good pipeline over a leaky
split still produces a number you cannot trust.

## Why it comes here

P1 gave you the machinery to fit a model. It says nothing about what to fit it to. P3
trains models, P4 trains networks, and both will happily reach a high score on a dataset
that has the answer leaking into a column. The score is the symptom; the leak is the
disease.

What breaks without this module:

- **A split that leaks.** A feature computed over the whole dataset before splitting, or a
  random split of time-ordered data, lets the model see the future. Test accuracy stays
  beautiful while production accuracy collapses, and the gap is invisible until launch.
- **A dataset that cannot be rebuilt.** If the rows came from a query you ran once and
  pasted into a CSV, nobody can reproduce the experiment, and nobody can extend it.
- **Features that only exist at training time.** A column the pipeline computes from
  labels, or one that is only populated after the fact, is a train-time phantom. It works
  perfectly offline and is missing at inference.
- **A class imbalance you never measured.** 95% negative data gives you a model that
  always says no, and an accuracy of 95% that hides it.
- **Silent distribution shift.** Nothing checks that today's rows look like the rows you
  trained on, so the model degrades one week after launch and nobody knows why.

## What gets built

- A labelled dataset, stored in version control or a reproducible export script, with a
  data dictionary: column name, type, meaning, allowed values, source.
- A split policy, written down: which rows go where, why, and how the split is
  reproducible from a seed or a time column.
- A leakage audit: a written list of every feature, where it comes from, and whether it
  is available at prediction time.
- A feature pipeline that fits on the training split only, applies the same
  transformations to every split, and is serialisable.
- A class-balance report and a decision about what to do about it.
- Basic data validation that fails loudly on a schema change.

## Acceptance criteria

- The dataset can be rebuilt from source with one command, and the row count and label
  distribution are asserted in a test.
- The split policy is documented and reproducible: the same seed or the same time
  boundary gives the same rows every time.
- Every feature in the pipeline is in the leakage audit with a verdict: available at
  prediction time, or removed. No feature is unmarked.
- The pipeline is fitted on the training split only. You can prove it: fit on the full
  data and the test score changes, and you know which direction and why.
- The feature pipeline runs as a single serialisable object, and applying it to a held-out
  frame uses the training statistics, not the held-out ones.
- Class balance is reported per split, and you have stated what you will do about an
  imbalance rather than discovering it later.
- A schema validation test fails when a required column is missing or a column changes
  type.

## The artifact

A dataset someone else can use without asking you a question: the rows, the label
definition, the data dictionary, the split policy, the leakage audit and the pipeline, all
in one place and all rebuildable.

Keep the evidence: the label distribution per split, the list of features you rejected as
leaky and why, the output of the schema validation test, and the seed or time boundary
your split uses.

## Notes

- Leakage audit is a written document, not a thought. Write the table before you write
  the pipeline; the pipeline then has to justify itself against it.
- Time-ordered data needs a time split. A random split on time-ordered data leaks the
  answer through the split itself.
- Target leakage sometimes looks like a feature you cannot get at inference time: a
  field filled in by the person who handled the ticket *after* the ticket was classified.
- Keep the raw data immutable. Every transformation lives in the pipeline, so it can be
  re-run when the transformation itself is wrong.
- The gate for this module is [G2](gate.md). The time box is 120 minutes.
