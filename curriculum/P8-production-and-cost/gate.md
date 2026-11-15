# Gate G8 - Production and Cost

## Time box

150 minutes. The clock starts when you write the deployment command and stops when the
rollback rehearsal is written up. If the timer runs out, hand in what exists, marked
incomplete.

Budget 40 minutes for the deployment and the health checks, 40 for the observability and
the dashboard, 30 for the cost model, 40 for the rollback rehearsal and the answers.

## The task

Take the service from P6 and the harness from P7 and make them deployable:

1. A container image that starts from a clean checkout with one documented command, with
   a liveness check and a readiness check that are not the same endpoint.
2. Structured logs with a request id that flows through the model call, plus metrics for
   latency, errors, cost and quality.
3. A dashboard showing p50, p95 and p99 latency, error rate, cost per request, quality
   score and traffic volume.
4. A cost model: a formula for the cost of one request from token counts, model price,
   cache hit rate and retry rate, with one worked example.
5. A rollback plan, written and rehearsed: the trigger, the command, the expected
   duration, what is lost while it is off, and the health check that confirms it
   worked. You actually perform the rollback and write down how long it took.
6. A canary that sends a small share of traffic to a new version and compares it with
   the P7 harness.

Everything runs locally or against a mock provider. Label all cost and latency figures
`SIMULATED`.

## Then answer out loud

1. Your p50 latency is 400ms and your p99 is 18 seconds. Name two causes that fit this
   exact shape, and say which dashboard panel would separate them.
2. A release dropped the quality score from 0.72 to 0.55 and you do not know whether it
   was the prompt, the model version or the schema. Explain how you would have made
   that answerable with the deployment you built, and what you would change now.
3. Your cost model says a request costs 0.4 cents, and the busiest day of the month
   costs more than the whole feature is worth. Name three levers you can pull, in the
   order you would pull them, and say which one you would pull first.

## Pass

- The service starts from a clean checkout with one documented command, and the liveness
  and readiness checks are distinct.
- One request can be traced end to end by its request id.
- The dashboard shows percentiles, error rate, cost per request, quality score and
  volume.
- The cost model is a formula with named inputs and one worked example.
- The rollback was performed and written up, with a duration and a health check.
- The canary compares against the P7 harness.
- All three answers are correct out loud.

## Fail

Do not start P9. Take the answer you could not give, fix the deployment or the plan, and
re-run the gate in a fresh box. A rollback plan that was written but never rehearsed does
not pass: P9 asks you to promise a rollout to users, and a promise about a rollback you
have never performed is a guess.
