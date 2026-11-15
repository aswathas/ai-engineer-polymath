# Gate G4 - Deep Learning

## Time box

180 minutes. The clock starts when you open the training script and stops when the
experiment log has its rows. If the timer runs out, hand in what exists, marked
incomplete.

Budget 60 minutes for the training loop and the seeding, 40 for checkpointing and
resume, 50 for regularisation and the comparison, 30 for the answers.

## The task

On a small dataset - a toy classification problem or a handful of images - build:

1. A training loop you wrote yourself: forward, loss, backward, update, step, with no
   high-level `fit` call.
2. Seeding for Python, NumPy and the framework, plus a fixed data order.
3. Checkpointing every N steps, containing the model state, the optimiser state and the
   step counter, and a resume path that restores all three.
4. A training history with separate train and validation curves.
5. Regularisation: weight decay on the weight matrices only, plus one more technique -
   dropout, early stopping or augmentation.
6. An experiment log with one row per run: seed, hyperparameters, and final metrics.

Everything runs offline, on CPU if you like. CPU is fine and is sometimes the better
teacher.

## Then answer out loud

1. Two runs with the same seed produced different training loss at step 100. Name three
   sources of that nondeterminism, and say which of them you can fix in a day.
2. Your validation loss turns up at step 900 while training loss keeps falling. Say what
   the model is doing, name two regularisers that would attack it, and say which one you
   would try first and why.
3. You resume from a checkpoint and the loss jumps up, then recovers over 50 steps.
   Explain the jump in terms of what a checkpoint that saved only the weights did not
   save, and say what you would change about the checkpoint format.

## Pass

- Two runs with the same seed produce identical printed metrics.
- An interrupted run resumed from the last checkpoint matches the uninterrupted run.
- The checkpoint holds the model, the optimiser and the step counter, and the history
  separates train and validation.
- The regularised run beats the unregularised run on the validation metric, and both are
  in the experiment log.
- You can point to the step where validation loss turned up.
- All three answers are correct out loud.

## Fail

Do not start P5. Take the answer you could not give, fix the loop or the experiment, and
re-run the gate in a fresh box. A training loop that only runs to completion on an
uninterrupted machine does not pass: P5's sampling harness and P7's eval harness both
depend on being able to stop and resume.
