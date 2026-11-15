# P5 - LLM Mechanics

## What

This module takes the transformer apart. Not the parts you read about in the news - the
parts that decide whether your application works: how text becomes tokens, how tokens
become predictions, and how a prediction becomes text you can ship.

You build three things. A tokeniser, so you know what the model actually sees and what a
token budget really costs. An attention implementation, so that "the context window" and
"the prompt" stop being abstractions. And a sampling harness with an eval attached, so
that "the model said something wrong" becomes a measurement instead of an anecdote.

The module ends where the temptation to skip ahead is strongest. You will be able to
compute things a hosted model does not let you compute: logits, per-token probabilities,
the cost of a context window in tokens, and the effect of a sampling parameter on a
specific output.

## Why it comes here

P4 gave you a training loop you control. P6 builds an application on top of a model you
do not control. Between the two sits this module, and it is where you learn the failure
modes of the component you are about to build products on.

What breaks without this module:

- **A prompt that is too long, diagnosed too late.** Without a tokeniser you guess at
  character counts and discover the truncation when the answer gets worse.
- **A structure that breaks silently.** JSON mode that emits invalid JSON, a schema
  violated in one field out of two hundred calls, and no way to tell whether the model or
  your parser is at fault.
- **Sampling you cannot control.** A temperature of 1.0 in production makes the same
  request return three different answers, and your eval harness cannot measure anything
  because the baseline moves.
- **Attention limits you do not know.** You build a prompt with 40,000 characters and do
  not know that you silently lost the middle.
- **"The model understands" as an untested belief.** Without implementing the forward
  pass yourself, every claim about what the model is doing is a story.

## What gets built

- A byte-pair-encoding tokeniser, trained on your own corpus, with the merge table saved
  and a round-trip test.
- An attention implementation: scaled dot-product attention, causal masking, multi-head
  attention, and the residual and normalisation blocks around it.
- A small decoder-only language model assembled from those pieces, small enough to train
  on your machine in minutes.
- A sampling harness: temperature, top-k and top-p, with the random seed controlled.
- An eval attached to the sampler: a small task with a known answer, so you can measure
  what the sampling parameters do instead of guessing.

## Acceptance criteria

- The tokeniser round-trips: `decode(encode(text)) == text` for a set of texts including
  emoji, newlines and code.
- You can state the token count of a given prompt exactly, and the count changes when
  you change the tokeniser, not the text.
- The attention implementation has a causality test: changing a token at position *i*
  cannot change the output at any position before *i*. This is tested, not asserted in a
  comment.
- Attention weights sum to one over the key axis, and the masked positions have weight
  exactly zero.
- The model can overfit a small batch, which proves the forward pass, the loss and the
  backward pass are consistent with each other.
- The sampler is deterministic under a fixed seed, and the same seed with the same
  parameters gives the same tokens.
- The eval shows a real effect: the sampling parameters change the score in a direction
  you can explain, and a greedy baseline beats sampling on the task you chose, or you
  explain why it does not.
- Every number you report from a mock or small model is labelled `SIMULATED`.

## The artifact

Three pieces that work together: a tokeniser, an attention implementation with tests,
and a sampling harness whose behaviour you have measured on a task with known answers.

Keep the evidence: the token counts for your own prompts, the causality test output, the
sample outputs at three temperatures, and the eval table.

## Notes

- Implement attention on plain arrays first, then check it against a framework
  implementation on the same inputs. The framework is the oracle, not the teacher.
- A small model on a tiny corpus is the point of this module. A model that memorises its
  training set is a *correct* model here.
- Perplexity is not a product metric. It belongs in your notes, not in your dashboard.
- The gate for this module is [G5](gate.md). The time box is 180 minutes.
