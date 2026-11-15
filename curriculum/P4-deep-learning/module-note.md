# P4 - Deep Learning

## What

Deep learning is the part of the series where the model has enough freedom to fit
anything, including the noise in your validation set. The skill this module teaches is
control: you decide how much the model may fit, you can reproduce the run exactly, and
you can stop and resume without losing the run.

Three properties separate a training loop from a script that calls `fit`:

- **Reproducible.** Same seed, same data order, same numbers. If the run cannot be
  repeated, none of its results can be trusted or discussed.
- **Interruptible.** Checkpoints on a schedule, so a machine that dies at hour three does
  not cost you hour three.
- **Regularised.** The model is prevented from memorising the training set by something
  more deliberate than "we stopped when the validation score stopped moving".

## Why it comes here

P3 gave you the habits: baseline, validation split, held-out test, error analysis. P4 is
where those habits get tested, because a network will happily memorise a small dataset
and report a validation curve that looks like learning.

What breaks without this module:

- **A run you cannot reproduce.** Nondeterministic kernels, an unseeded shuffling order
  and an unrecorded data version mean the model in your README is not the model you
  measured. Two days later you cannot tell whether a change helped.
- **Overfitting that the loss curve hides.** Training loss keeps falling, validation loss
  turns up, and without a checkpointed history you find out three runs later.
- **A run killed by the laptop.** Four hours of training, no checkpoint, thermal shutdown,
  and the only copy was in memory.
- **Weight decay applied to the wrong tensors.** Regularisation that includes the bias
  and the normalisation parameters changes the model you think you are training.
- **Batch norm in the wrong place.** Putting normalisation after the residual connection
  instead of inside the block costs you accuracy and teaches you a false rule.

## What gets built

- A training loop you wrote: forward, loss, backward, update, step. No `model.fit`.
- Seeding for Python, NumPy and the framework, plus explicit control of the data order.
- A checkpoint writer and a resume path that restores the model, the optimiser state and
  the step counter.
- A training history: loss curves for train and validation, written to a file, that you
  can plot and read.
- Regularisation: weight decay on the right parameters only, dropout, early stopping,
  and one augmentation for your data type.
- A small experiment log: one row per run, with seed, data version, hyperparameters and
  the final metrics.

## Acceptance criteria

- Two runs with the same seed produce identical metrics to the precision you print.
  You checked this by running twice, not by assuming it.
- Killing the run mid-training and resuming from the last checkpoint reproduces the
  uninterrupted run's metrics. This is tested, not claimed.
- The checkpoint contains the model state, the optimiser state and the step counter, and
  a resume restores all three.
- The training history separates train and validation curves, and you can point to the
  step where validation loss turned up.
- Weight decay is applied to the weight matrices only, and you can show that the biases
  and normalisation parameters are unchanged by it.
- At least one regularisation technique measurably improves the validation score over the
  unregularised run, and the comparison is in the experiment log.
- The run stops early when validation loss stops improving, and the best checkpoint, not
  the last one, is what you keep.

## The artifact

A training loop you can point at and say: this run is reproducible, this is how it
resumes, this is how it knows to stop, and here is the history that shows what happened.

Keep the evidence: the two identical-seed runs side by side, the interrupted-and-resumed
comparison, the train and validation curves, and the experiment log with the
hyperparameter that won.

## Notes

- Reproducibility across machines is a stronger claim than reproducibility on one
  machine. State which one you have.
- A GPU makes training fast enough to try many wrong things. That is a liability in this
  module; the CPU is often the better teacher.
- If you use mixed precision, check that the loss did not silently become `NaN` on one
  step. Silent NaNs are the deep-learning version of the P0 guard.
- Any speed or throughput figure from a mock provider is labelled `SIMULATED`.
- The gate for this module is [G4](gate.md). The time box is 180 minutes.
