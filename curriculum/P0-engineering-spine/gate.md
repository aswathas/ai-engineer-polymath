# Gate G0 - Engineering Spine

## Time box

120 minutes. The clock starts when you open the repository and stops when the suite is
green. If the timer runs out, stop anyway and hand in what you have, marked as incomplete:
an unfinished artifact with a stated gap is better than a rushed one with a hidden one.

Budget roughly 20 minutes for the retry wrapper and the idempotency key, 40 minutes for
the schema and the migrations, and the rest for the tests.

## The task

Build the smallest service that still has the properties the module asks for:

1. A typed request and response, validated at the edge, with a typed error for each
   failure the caller can act on.
2. A Postgres table for the domain, plus a migration that applies to an empty database
   and rolls back.
3. One unreliable dependency called through a single retry wrapper: bounded attempts,
   capped backoff, jitter, and no retry on a 4xx.
4. An idempotency key on the write, such that repeating a request with the same key
   returns the first result instead of writing a second row.
5. Tests: the domain under unit test, the boundary under a contract test, and one
   integration test against a real Postgres that proves the retry path does not write
   twice.

Everything runs offline. No network, no paid API.

## Then answer out loud

1. You retry a request because the dependency timed out, but you are not sure whether the
   dependency did the work. What in your code decides whether a second row appears, and
   why does a plain retry not solve it?
2. You chose to return a typed error instead of an HTTP status alone. What does a caller
   do differently because of that choice, and what breaks if you only return the status?
3. Your suite is green on your machine and fails on a colleague's. Name two causes that
   live inside the boundary you just built, and say which one your tests do not cover.

## Pass

- The suite runs offline, in under a minute, and is green.
- The strict type check passes with no `Any` on the public boundary.
- One test fails if you remove the idempotency key from the write path. You checked this
  by breaking it on purpose, not by reading the code.
- The migration applies to an empty database and rolls back.
- All three answers are correct out loud, without notes.

## Fail

Do not start P1. Say which of the three answers you could not give, fix that, and re-run
the gate in a fresh 120-minute box. A copied answer to question two is a fail even when
the code is perfect: P1 assumes you understand why idempotency is part of the design and
not a patch on top of it.
