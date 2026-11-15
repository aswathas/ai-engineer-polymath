# Gate G5 - LLM Mechanics

## Time box

180 minutes. The clock starts when you open the tokeniser and stops when the eval table
has its rows. If the timer runs out, hand in what exists, marked incomplete.

Budget 40 minutes for the tokeniser, 60 for attention and the causality test, 40 for the
sampler, 40 for the eval.

## The task

Build three things that work together:

1. A byte-pair-encoding tokeniser trained on your own corpus, with the merge table saved
   and a round-trip test over ordinary text, code, emoji and newlines.
2. An attention implementation: scaled dot-product attention with causal masking, plus
   multi-head attention. Include a test that changing a token at position *i* cannot
   change the output at any position before *i*, and a test that masked positions carry
   exactly zero weight.
3. A sampling harness with temperature, top-k and top-p, seeded so that the same seed
   and parameters give the same tokens.
4. An eval attached to the sampler: a small task with a known answer, run at greedy and
   at two temperatures, with the score for each.

Everything runs offline, on CPU. Use a small corpus of your own making; label invented
figures `SIMULATED`.

## Then answer out loud

1. Your prompt is 3,900 characters and the model truncates it. Explain what the token
   count depends on, why character count is a bad proxy, and what you would put in front
   of the user to make the limit visible.
2. The causality test fails only for the second head. Explain what that tells you about
   where the bug is, and why the first head passing does not rule out a shared cause.
3. Greedy decoding scores better than sampling at temperature 0.7 on your task. Name two
   reasons that could be true, and say how you would distinguish them with one more
   experiment.

## Pass

- The tokeniser round-trips on the test set, including emoji and code.
- The causality test passes, and the masked-weight test passes.
- The sampler is deterministic under a fixed seed.
- The eval table has a greedy row and two temperature rows, with an explanation of the
  direction of the change.
- All three answers are correct out loud.

## Fail

Do not start P6. Take the answer you could not give, fix the code or the explanation, and
re-run the gate in a fresh box. An attention implementation with no causality test does
not pass: P6 puts tool calls and structured output on top of this component, and a
mis-masked attention leaks information across the prompt boundary.
