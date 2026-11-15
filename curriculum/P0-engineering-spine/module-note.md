# P0 - Engineering Spine

## What

The engineering spine is the part of AI work that never mentions AI. It is the typed
boundary, the retry, the idempotency key, the migration, the test that runs without a
network. It is boring, and it is the reason a model change reaches production without
taking the rest of the system with it.

This module is the foundation of the whole series. Every later module adds a component
that assumes you can land a change on a Friday and know what broke. If you cannot do that
here, you will spend P7 and P8 debugging a failure that was caused in P0.

Scope: one small service with one database, one dependency that can fail, and a test
suite that runs offline in under a minute.

## Why it comes here

An AI feature is a normal service with an expensive, non-deterministic component in the
middle. The non-deterministic part is where the attention goes, and it is where the least
defence lives. Everything else - retries, transactions, schema, typing - is what stops a
flaky model call from becoming a corrupted row.

What breaks without this module:

- **A retry becomes a double write.** The upstream call times out, the client retries, and
  the invoice is issued twice. An idempotency key is the difference between a retry and a
  duplicate, and you only get to add it cheaply before the table has rows in it.
- **A schema change becomes an outage.** Without migrations, every column add is a manual
  step someone runs at the wrong time.
- **A bug becomes unprovable.** Without tests, the only way to know a fix works is to
  deploy it and watch. Nobody can review "it looks right".
- **Types become decoration.** If the request body is `Any`, every consumer of the
  service has to re-check it, and the checks drift apart.

Later modules inherit whatever you skip here. P6 adds tool calls that mutate state; P7
adds an eval that must produce the same answer twice; P8 adds a deployment that has to be
revertible. All three assume the spine.

## What gets built

- A service with an explicit request and response type, validated at the edge.
- A Postgres schema for the domain, with migrations that apply from empty and roll back.
- One unreliable dependency, wrapped in a retry with bounded attempts and jittered backoff.
- Idempotency keys on every write that a retry can reach.
- A test suite: unit tests for the domain, a contract test for the boundary, one
  integration test that runs against a real Postgres.
- A typed error taxonomy so a caller can tell "try again" from "your request is wrong".

## Acceptance criteria

- The public API of the service has no `Any` in it, and the type checker passes in strict
  mode with no ignores on the boundary types.
- Every call to the unreliable dependency goes through one retry wrapper, with a maximum
  attempt count, a capped backoff, and jitter. No call site implements its own retry.
- Every write that can be reached by a retry takes an idempotency key, and sending the
  same key twice returns the first result instead of writing twice.
- There is a test that proves the no-double-write property, not a comment that claims it.
- Migrations apply to an empty database and roll back cleanly, and there is a test for
  both directions.
- The full suite runs offline, with no network access and no paid API, and finishes in
  under a minute.
- Failures return a typed error the caller can branch on, and a 4xx from the dependency is
  not retried while a 5xx or a timeout is.

## The artifact

A service another engineer could pick up on Monday: a repository with a clean history, a
schema in version control, a README that says how to run it, and a suite that fails when
the behaviour is wrong.

Keep the evidence next to it: the schema diff, the test output, one example request and
response for each error case, and a short note on what the service does when the
dependency is down. That note is the part reviewers actually read.

## Notes

- **Free tools only.** Postgres in Docker, or any local Postgres you already have. No
  paid service is needed or wanted in this module.
- **No secrets in the repo.** Keys come from environment variables. Keep a `.env.example`
  listing every variable name, and never commit the real file.
- **Mock the dependency, not the database.** The point of the integration test is to
  exercise the real transaction. Faking the database hides the bug you are here to avoid.
- **SIMULATED numbers.** Any latency, cost or throughput figure you invent for a mock
  provider must be labelled `SIMULATED` in the same breath as the number.
- The gate for this module is [G0](gate.md). The time box is 120 minutes.
