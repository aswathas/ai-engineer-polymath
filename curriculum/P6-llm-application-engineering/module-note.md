# P6 - LLM Application Engineering

## What

The application layer is where a model becomes a feature. The model is a component with a
contract: it takes a prompt, it returns text or a tool call, and it does so at a cost, a
latency and a failure rate you did not choose. This module is about the engineering
around that component.

The deliverable is a service that returns structured output, can call tools, and holds
guardrails at every boundary. Structured output is the load-bearing idea: a model that
returns prose has to be parsed, and parsing prose is where a surprising share of AI
applications break. A schema turns the model's freedom into a contract you can validate.

Guardrails are not a wrapper around this. They are the set of decisions about what the
system is allowed to do when the model is wrong, and the model is wrong often enough that
those decisions are the product.

## Why it comes here

P5 showed you what is inside the model. P6 puts the model inside a system: prompts,
tools, schemas, retries, timeouts, caching, and the paths that must not call a model at
all.

What breaks without this module:

- **Free-text parsing.** "Sure! Here is the JSON: {...}" parses 97% of the time. The
  other 3% is an incident at 2am, and the fix is a schema with validation, not a better
  prompt.
- **A tool call that mutates the wrong thing.** The model asked to "delete the draft", the
  id resolved to a published document, and the tool did exactly what it was told. The
  tool interface needs narrowing, confirmation and an audit trail.
- **Prompt injection through user content.** Anything the model reads - a ticket, an
  email, a web page - is a potential instruction. Guardrails fail when the only defence
  is a sentence in the prompt.
- **Cost per request that nobody predicted.** Retries without idempotency, a context
  window that grows on every turn, and no cache turn a cheap feature into an expensive
  one. P8 models the cost; P6 is where you create it.
- **A service that fails when the provider fails.** No timeout, no fallback, no
  circuit-breaker: one slow upstream response becomes a queue that never drains.

## What gets built

- One endpoint: a typed request in, a typed validated response out.
- Structured output: a schema the response must satisfy, enforced by validation at the
  boundary, with a repair path for the failure case.
- At least two tools, each narrow and typed.
- A confirmation step for any mutating tool, with a human in the loop for the dangerous
  one.
- Guardrails: input validation and size limits, output validation, injection resistance,
  timeouts, bounded retries, and a deterministic fallback for the failure path.
- A cost and latency budget per request, measured on a mock provider and labelled
  `SIMULATED`.

## Acceptance criteria

- The service returns a schema-valid response or an explicit typed error. There is no
  third path where the caller receives prose it has to parse.
- The repair path is tested: an invalid model response is repaired within a bounded
  number of attempts, or fails with a typed error.
- Every tool has a typed input schema and a test for wrong arguments.
- A mutating tool requires confirmation; the dangerous one requires a human. Both are
  tested.
- Injection attempts are covered by tests: at least three hostile inputs, including one
  hidden in user-supplied content, and the expected behaviour is asserted.
- Every model call has a timeout, a bounded retry with backoff, and a fallback that does
  not call the model.
- The service refuses oversized inputs and never forwards an unbounded history.
- Cost and latency figures are `SIMULATED`, with the measurement method stated.

## The artifact

A service with one endpoint that a colleague can call with `curl`, plus the evidence that
it is safe to call: the schema, the tool contracts, the hostile-input tests, and the
fallback path.

Keep the evidence: the validation failure case and its repair log, the injection test
results, the fallback response, and the per-request cost and latency table with the
`SIMULATED` label.

## Notes

- Never trust the model to enforce a constraint you can enforce in code. The schema
  validates the output; the tool validates the arguments.
- Give a tool the narrowest scope that still does the job: "delete this document by id
  and version" beats "delete a document".
- Put the user content *after* the instructions, mark the boundaries explicitly, and
  treat everything in the content region as data, never as instruction.
- Cache on stable keys, and never cache a response that had a side effect.
- The gate for this module is [G6](gate.md). The time box is 180 minutes.
