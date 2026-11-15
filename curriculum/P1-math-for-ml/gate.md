# Gate G1 - Math for ML

## Time box

150 minutes. The clock starts when you open a blank file and stops when the test suite is
green. If the timer runs out, hand in what exists, marked incomplete, and say which part
you did not reach.

The two halves are independent: 60 minutes for the optimiser and the loss curve, 60
minutes for the gradient check and the deliberately broken derivatives, 30 minutes for the
answers and the cleanup.

## The task

Build a numerically careful optimiser and prove it is correct:

1. A mean-squared-error loss on a small 2D dataset, with the derivative you derived, not
   one you copied.
2. Gradient descent on that loss, with a learning rate, a stopping rule based on the
   gradient norm, and a loss curve you can plot.
3. A finite-difference gradient checker that reports the relative error per parameter.
4. Three deliberately wrong derivatives - wrong sign, missing factor, swapped terms -
   that the checker catches. Each failure is a test, not a screenshot.
5. Guards on every division, logarithm and square root, each with a test.

Everything runs offline on plain arrays.

## Then answer out loud

1. Your loss became `NaN` on iteration 40 and not iteration 39. Name the two most likely
   causes in the code, and say which one your gradient check would *not* have caught.
2. You set the finite-difference step to `1e-12` and the check started failing with a
   relative error around `1e-4`. Explain what happens to the finite-difference estimate
   as the step shrinks, and what sets the floor.
3. A learning rate of `0.1` diverges and `0.01` crawls on the same problem. Describe the
   shape of the loss surface that produces both behaviours, and say which quantity you
   would look at to tell a diverging run from a stalling one.

## Pass

- The gradient check passes on the correct derivative, at three different step sizes, with
  a relative error below a stated tolerance.
- The three broken derivatives each fail the check, and the failing test names the cause.
- The loss decreases and the run stops on the gradient-norm threshold, not on a fixed
  iteration count.
- The guards are tested, and each guard test fails when you remove the guard.
- All three answers are correct out loud.

## Fail

Do not start P2. Take the specific answer you could not give, fix the code or the
explanation that goes with it, and re-run the gate in a fresh box. A gradient checker that
has never failed does not count as a checker - if you did not break a derivative on
purpose, the gate fails on that alone.
