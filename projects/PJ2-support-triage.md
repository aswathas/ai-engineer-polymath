# PJ2 - Support triage with human handoff

## Goal

Classify inbound support tickets automatically, escalate the ambiguous ones to a human, and defend
every threshold with calibration evidence and a rollout plan that says what happens when the
classifier is wrong.

Automation without a handoff is a support incident waiting for a Tuesday. The deliverable is the
classifier *and* the policy wrapped around it.

## Modules exercised

- P3 - Classical ML
- P6 - LLM Application Engineering
- P7 - Evaluation
- P9 - Product and Delivery

## Acceptance criteria

- [ ] A labelled ticket set of at least 300 tickets with a documented labelling rule and a split
      policy that keeps near-duplicates on the same side of the split.
- [ ] A baseline classifier and a tuned classifier, both measured on the same held-out split, with
      the tuning decision written down.
- [ ] Probability calibration measured on the held-out split, with the reliability table or the
      calibration curve included.
- [ ] Two thresholds chosen from the calibration evidence, one for auto-answer and one for
      escalate, each with the precision or recall it buys and the error it costs.
- [ ] An escalation path naming the queue, the payload the human receives, the service-level
      target, and the case where a ticket is escalated with no classifier confidence at all.
- [ ] An eval suite that runs offline with no API key, reporting a false-escalation rate and a
      false-auto-answer rate, both against the baseline.
- [ ] A rollout plan with stages, entry and exit criteria per stage, a rollback trigger, and the
      customer-facing message used at each stage.
- [ ] Tests cover the labelling rule, the calibration computation, the threshold selection and the
      escalation payload.

## Evidence required

- The dataset builder, the labelled tickets, the split policy and the leakage check.
- The baseline and the tuned classifier with the training script and the recorded hyperparameters.
- The calibration report and the argument that picks each threshold.
- The offline eval suite and its output, every figure marked SIMULATED where it comes from a mock
  provider.
- The routing code and the escalation payload schema.
- The rollout plan with its stages, the rollback trigger and a draft of the failure communication.
- An error analysis of the ten worst wrong decisions and what each one would have cost.

## Rubric

| Criterion | Weight | What the evidence must show |
| --- | --- | --- |
| Calibration and threshold choice | 25 | A calibration measurement on the held-out split and the argument that picks each threshold from that evidence. |
| Escalation policy and handoff | 20 | The human queue, the payload, the service-level target, and the rule for escalating a low-confidence ticket. |
| Evaluation quality | 20 | A held-out split that was not used for tuning, both error rates reported against a baseline, and error analysis over the failures. |
| Reliability and monitoring | 15 | Tests over the routing logic, the drift check, and the alert that fires when the input distribution moves. |
| Rollout plan and failure communication | 20 | Staged rollout with entry and exit criteria, a rollback trigger, and the customer-facing message for each stage. |
