# Gate G9 - Product and Delivery

## Time box

150 minutes. The clock starts when you open the spec template and stops when the failure
message is dated and ready to send. If the timer runs out, hand in what exists, marked
incomplete.

Budget 50 minutes for the spec, 40 for the rollout plan, 30 for the price, 30 for the
failure message and the answers.

## The task

Turn the deployed service from P8 into four documents:

1. A product spec: problem, user, non-goals, user-visible behaviour, failure behaviour,
   and acceptance criteria a test could check.
2. A rollout plan: at least three phases, each with the metric, the threshold and the
   observation window that advances it, plus a kill switch and the person holding it.
3. A price: unit economics per user segment, computed from the P8 cost model, with the
   margin shown at the assumed volume.
4. A failure communication draft: what broke, who was affected, what you did, what you
   changed. Dated, plain, ready to send.

Everything is a document. Label every figure that comes from the mock provider
`SIMULATED`.

## Then answer out loud

1. Your model is right 95% of the time and the product spec has to say what the user
   sees the other 5% of the time. Describe the interface you would build, and say what
   the user is able to do that they could not do before.
2. The rollout is at phase two of three, the quality score fell from 0.72 to 0.68, and
   your advance threshold was 0.70. Describe exactly what happens next, who decides, and
   how long it takes to stop.
3. One segment of users costs you 40 cents per request and another costs 0.2 cents. Name
   three ways to make the first segment profitable, and say which one you would try
   first and what it costs you in complexity.

## Pass

- The spec states the problem in the user's words, three non-goals, a failure behaviour,
  and acceptance criteria a test could check.
- The rollout plan has three phases with metrics, thresholds and observation windows, a
  named kill switch and a named holder.
- The price comes from the P8 cost model per segment, with margins, and any negative
  margin is addressed rather than hidden.
- The failure message is dated, plain, and answers the four questions.
- All three answers are correct out loud.

## Fail

Do not start the capstone. Take the answer you could not give, fix the document that
goes with it, and re-run the gate in a fresh box. A spec with no failure behaviour does
not pass: the capstone is judged on whether a shipped feature can survive contact with
users, and the failure path is where that is decided.
