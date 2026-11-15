# P1 - Math for ML

## What

The mathematics you need is a small subset: vectors and matrices as data, the chain rule,
probability as the language of uncertainty, and optimisation as the engine. You do not need
a proof of anything. You need enough of each to look at a training run and know why it
diverged, why the loss went flat, and why two implementations of the same model give
different numbers.

The module is built around one tool: **the gradient check**. You compare an analytic
derivative against a finite-difference approximation. If they disagree, the code is wrong.
This is the single highest-value habit in machine learning, because every training bug
looks identical from the outside - the loss goes to NaN, or it does not move.

## Why it comes here

P2 scales features and splits data, and both choices are justified with statistics. P4
writes a training loop and backpropagation by hand. P5 implements attention, which is
matrix multiplication and a softmax. All of them assume you can reason about gradients and
numbers without stopping to look up a formula.

What breaks without this module:

- **A silent wrong derivative.** You get a training loss that decreases and a model that
  is worse than a linear baseline. Nothing errors. The model simply learned the wrong
  thing, and no amount of hyperparameter search finds it.
- **A NaN loss.** Division by zero, a `log` of a negative number, a `sqrt` of a negative
  variance. With the mathematics in place you can see the cause in the formula; without
  it you grep for a `NaN` that was there since the first commit.
- **Features that silently dominate.** A feature in the millions and one in the hundreds
  means the optimiser follows the first one and ignores the second. You conclude the
  second feature is useless.
- **A learning rate chosen by vibes.** Without the shape of the loss surface in mind,
  every configuration looks like a coin flip.

## What gets built

- Vector and matrix operations you write yourself, on plain arrays, so the arithmetic is
  visible.
- A mean-squared-error loss and its derivative, derived rather than copied.
- Gradient descent and stochastic gradient descent, with a learning-rate schedule.
- A finite-difference gradient checker, with a sensible step size and a tolerance.
- A small linear-regression problem solved by gradient descent, not by a closed form.
- Numerical guards: `float64`, an epsilon where you divide, and checks that inputs are in
  range before you take a logarithm.

## Acceptance criteria

- The gradient checker passes for every parameter of the model, with a relative error
  below a stated tolerance at several step sizes, not only the default one.
- **The gradient check catches a wrong derivative.** You deliberately break the derivative
  in three ways - a wrong sign, a missing factor, a swapped pair of terms - and the
  checker reports each one. A checker that has never failed has not been tested.
- The loss decreases over training, and the run stops when the gradient norm falls below
  a threshold rather than at a hard-coded iteration count.
- With a learning rate ten times too large, the run diverges in a way you can explain
  from the update rule. With a learning rate ten times too small, it crawls. You can name
  both from the loss curve.
- The implementation uses `float64`, and the finite-difference step is small enough for
  the tolerance to hold but not so small that the result is dominated by float error.
- Every division, logarithm and square root in the code has a guard, and each guard has a
  test that exercises it.

## The artifact

An optimiser you would be willing to put inside a training loop: one function that takes
gradients and steps, one function that checks gradients, and a test suite where the
gradient check is the loudest test in the file.

Keep the evidence: the gradient-check output for the broken-derivative cases, the loss
curves for the too-large and too-small learning rates, and the tolerance you chose with
the reason you chose it.

## Notes

- Write the arithmetic in plain NumPy or plain Python first. A framework will hide the
  thing you are trying to learn here.
- The finite-difference step size is a real decision. Too large and the approximation
  error dominates; too small and floating-point noise dominates. Pick one, justify it in
  a comment, and record it with the tolerance.
- Any performance or cost figure you produce from a mock provider is labelled `SIMULATED`.
- The gate for this module is [G1](gate.md). The time box is 150 minutes.
