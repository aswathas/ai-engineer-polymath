# PJ1 - Retrieval QA service

## Goal

Answer questions over a customer's own documents. Every answer carries citations back to the
source passages, an offline eval says how often the answer is right, and a written cost model says
what one query costs.

This is not a chat toy. The service has to refuse when retrieval is weak instead of inventing an
answer, it has to be measurable with no network call, and it has to be operable by someone who did
not build it.

## Modules exercised

- P0 - Engineering Spine
- P2 - Data and Features
- P6 - LLM Application Engineering
- P7 - Evaluation
- P8 - Production and Cost

## Acceptance criteria

- [ ] A corpus of at least 40 documents is ingested into a chunk store with a documented chunking
      rule and a stable chunk id.
- [ ] Every answer returns the answer text plus the ids of the chunks it was built from; an answer
      with no supporting chunk is refused rather than guessed.
- [ ] The eval suite runs fully offline, with no API key and no network call, over at least 30
      held-out questions whose expected source documents are recorded.
- [ ] The report states a retrieval hit rate, a citation correctness rate and a refusal accuracy,
      each compared against a named baseline.
- [ ] The cost model gives a SIMULATED cost per query broken into retrieval calls, input tokens and
      output tokens, with the assumption behind every number written down.
- [ ] A refusal policy states the retrieval-confidence threshold, why that threshold was chosen,
      and what the user sees when it trips.
- [ ] Tests cover the chunker, the citation check, the refusal path and one end-to-end query
      against a fixture corpus.
- [ ] A runbook says how to deploy, how to roll back and what to watch in the first week.

## Evidence required

- The service source and the dependency list, plus the command that starts it.
- The test suite and its output, including one real failure that a test caught and turned green.
- The eval harness, the held-out question set with its expected source documents, and the eval
  report.
- The cost model as a table, with every figure marked SIMULATED and every assumption named.
- An incident note: one failure found during the build, what it cost, and the fix.
- A limitations section naming what the service does not handle and why.

## Rubric

| Criterion | Weight | What the evidence must show |
| --- | --- | --- |
| Answer and citation correctness | 25 | The eval report with per-metric numbers, the held-out set, and the baseline each number is compared against. |
| Evaluation quality | 25 | A held-out set that was not used for tuning, a named refusal rule, and error analysis over the failures. |
| Reliability and guardrails | 20 | The refusal path in code and in tests, structured-output validation, and the failure modes the service absorbs. |
| Cost model and efficiency | 15 | A per-query cost table with SIMULATED figures, the assumptions behind them, and what happens to cost as the corpus grows. |
| Documentation and honesty about limits | 15 | A runbook, an incident note, and a limitations section that names what the service cannot do. |
