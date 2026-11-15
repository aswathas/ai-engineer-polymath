# Gate GCAP - Polymath Capstone

## Time box

180 minutes. The clock starts when you open the evidence bundle index and stops when the
retrospective is written. If the timer runs out, hand in what exists, marked incomplete -
a partial bundle with a stated gap is worth more than a complete-looking one with a
missing piece.

The box is for the assembly and the proof, not for the building: the artefacts themselves
come from the module gates you already passed. Budget 45 minutes for the bundle index
and the assembly check, 45 for the end-to-end run and the scorecard, 45 for the
retrospective, and 45 for the answers and the cleanup.

## The task

Assemble the capstone and prove it holds together:

1. Pick one feature. Write the one-sentence version: for whom, doing what, replacing
   what.
2. Build the evidence bundle index: every acceptance criterion from every module note,
   listed one by one, each with a pointer to the artefact that satisfies it. Any
   criterion you cannot point to is either unmet or out of scope, and you say which.
3. Run the whole chain end to end from a clean checkout: the service starts, the test
   suite passes, the eval harness runs against the deployed service, and the scorecard
   is produced. Save the output.
4. Exercise the failure path: trigger the rollback and record what happened, or trigger
   the fallback and record it.
5. Write the retrospective: for every module, what worked, what broke, what the numbers
   were, and what you would change. At least three entries are about something that
   genuinely surprised you.

Everything runs offline or against a mock provider. Label all figures `SIMULATED`.

## Then answer out loud

1. Two of your modules disagreed when you assembled them - one assumed a synchronous
   call, the other assumed a batched one. Name the seam, say which side you changed, and
   say what that change cost you in latency or in money.
2. Your eval score on the assembled feature is lower than the score you measured module
   by module. Name two causes that are specific to assembly, and say which one you would
   chase first.
3. Someone offers to add a second feature to this repository next quarter. Name the one
   piece of your evidence bundle that would make that safe, and say why it is the one
   that matters.

## Pass

- The feature runs from a clean checkout with one documented command, and the offline test
  suite passes.
- The bundle index lists every module acceptance criterion with a pointer, and every
  unmet criterion is declared as unmet or explicitly out of scope.
- The end-to-end run is recorded: the service, the tests, the eval harness against the
  deployed service, and the scorecard.
- The failure path was exercised and recorded.
- The retrospective covers every module, with at least three genuine surprises named.
- A reviewer can understand the feature and the case for shipping it in ten minutes.
- All three answers are correct out loud.

## Fail

The capstone is not passed on the second attempt of the same build. Take the two or three
things the bundle cannot show, go and build them, and re-run the gate in a fresh box.
A capstone submitted with a missing criterion and no declaration of that gap is an
automatic fail: an undeclared gap is the one failure mode the whole series exists to
prevent.
