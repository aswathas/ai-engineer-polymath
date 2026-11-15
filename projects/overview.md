# Capstone projects

## What a capstone project is

Three briefs. Each one is shippable work, not an exercise: the learner writes the code, the agent
reviews it. A brief is a contract with four parts - a goal, the modules it exercises, the acceptance
criteria, and the evidence a submission must contain - plus the rubric the submission is judged
with.

A brief is not a rewrite of a module. A module teaches one thing. A brief makes you decide what to
build when nothing tells you what to build next.

## How to pick one

Pick the project whose problem you would rather own for a weekend:

- **PJ1** if you want retrieval, citations and an eval you can run offline. Modules P0, P2, P6, P7, P8.
- **PJ2** if you want a classifier, calibrated thresholds and a human handoff. Modules P3, P6, P7, P9.
- **PJ3** if you want a release pipeline that can block its own authors. Modules P5, P7, P8, P9.

Pick by the module you found hardest. If it was P2, take PJ1. If it was P7, take PJ3.

## Shared acceptance rules

These apply to every brief in this folder. They are not negotiable:

- **Free tier only.** No paid API. Mock providers and free tiers only.
- **SIMULATED labels.** Every number that comes from a mock provider is labelled `SIMULATED`. A
  number without that label is not published.
- **No secrets.** Keys come from environment variables. Nothing sensitive lands in the repository.
- **Tests are part of the deliverable.** A submission without a passing test suite is not a
  submission.
- **Evidence is part of the deliverable.** The code is half. The eval output, the cost model and
  the written limits are the other half.
- **The learner writes the code.** The agent reviews, explains and questions. See
  [AGENTS.md](../AGENTS.md).

## Estimated hours

| Brief | Estimated hours | Modules exercised |
| --- | --- | --- |
| [PJ1 - Retrieval QA service](PJ1-retrieval-qa-service.md) | 60 | P0, P2, P6, P7, P8 |
| [PJ2 - Support triage with human handoff](PJ2-support-triage.md) | 55 | P3, P6, P7, P9 |
| [PJ3 - Eval-driven prompt and model release](PJ3-eval-driven-release.md) | 50 | P5, P7, P8, P9 |

Those are working hours for someone who has finished the modules named in the brief. The final
CAPSTONE gate is a separate 60-hour project spanning P0 to P9, judged with
[the capstone rubric](../curriculum/capstone/rubric.md).

## Where to look next

- The series map and the module list: [README.md](../README.md)
- The terms this folder uses: [GLOSSARY.md](../GLOSSARY.md)
- How the curriculum is planned: [plan.md](../plan.md)
- How to contribute a change: [CONTRIBUTING.md](../CONTRIBUTING.md)
- How the build was recorded: [BUILDLOG.md](../BUILDLOG.md)
