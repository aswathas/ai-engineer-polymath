# AI Engineer Polymath — Canonical Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a public GitHub repository, `aswathas/ai-engineer-polymath`, that is a standalone AI-engineer curriculum series (10 modules + capstone) with the agent roster, skill pack, capstones, machine-checked validators, a pytest suite, CI, and the full documentation record.

**Architecture:** The repo is a *curriculum and toolchain* repository, not an application. Teaching content lives in `curriculum/` (one directory per module, each with a module note, a gate and a resource list). Machine-checkable contracts live in `tools/validators/` (pure Python, no network, one module per rule family, a single `run_all.py` entry point). The repo's own content is the fixture the validators check, so `pytest` and CI are self-hosting: the suite fails when the curriculum drifts from the contracts.

**Tech Stack:** Python 3.12 · `pytest` · `ruff` · `PyYAML` · GitHub Actions (ubuntu-latest, Python 3.12) · Markdown (GitHub-flavoured) · `gh` CLI for issues.

---

## Global Constraints

These apply to every task. Values are exact; do not substitute.

- Local path: `C:\Users\ADMIN\Projects\ai-engineer-polymath`
- Remote: `git@github.com:aswathas/ai-engineer-polymath.git` (HTTPS transport, `gh` account `aswathas`, visibility **public**)
- Python: **3.12+**. Dependencies: `pytest>=8.0`, `ruff>=0.6`, `PyYAML>=6.0`. No other runtime dependency. No paid API. No network calls in validators or tests.
- Module ids are `P0`–`P9` plus `CAPSTONE`. Gate ids are `G0`–`G9` plus `GCAP`. Slugs are lowercase-kebab. Directory names are `P<n>-<slug>` (e.g. `P5-llm-mechanics`).
- Validator API is fixed: every validator module exposes `validate(repo_root: Path) -> list[Issue]`; `Issue` is a dataclass with fields `code: str`, `path: str`, `message: str`; `run_all.py` exits `0` when every validator passes, `1` when any validator reports an issue, and `--json` prints a machine-readable report.
- Validator error codes are stable identifiers and are the contract the tests assert on: `SKEL001`–`SKEL010`, `AGT001`–`AGT008`, `SKL001`–`SKL009`, `CUR001`–`CUR009`, `PRJ001`–`PRJ007`, `LNK001`–`LNK004`, `REC001`–`REC006`.
- Agents live in `agents/` as Markdown with YAML frontmatter carrying exactly `name` and `description`. Required body sections, in order: `## Role`, `## Triggers`, `## Hard Rules`, `## Workflow`, `## Output Contract`, `## Refusals`.
- Skills live in `skills/<skill-name>/SKILL.md`. Frontmatter carries exactly `name` and `description`. Required body sections, in order: `## When to use`, `## Inputs`, `## Procedure`, `## Outputs`, `## Verification`. Any `scripts/` path mentioned in a skill body must exist inside that skill's directory.
- Teaching rule that governs every agent and every module note: **the learner writes the code; the agent never does.** After two requests for an implementation, an agent gives a worked trace instead.
- Documentation record is mandatory before push: `docs/reviews/decision-log.md`, `docs/reviews/change-inventory.md`, `docs/reviews/prompts.md`, `BUILDLOG.md`.
- Commits: conventional subject (`feat:`, `docs:`, `test:`, `ci:`, `chore:`), body of at least 20 characters explaining *what and why*, trailer `Co-Authored-By: MiniMax Code <noreply@minimax.ai>`. One meaningful unit per commit. Never amend a published commit.
- Push order: initial scaffold commit lands on `main` and is pushed; remaining work happens on `feature/polymath-v1` and lands via a pull request into `main`.

---

## 1. Decisions taken (from the user, 2026-11-15)

| # | Decision | Alternatives rejected | Prompt that produced it |
|---|----------|-----------------------|--------------------------|
| D1 | Standalone new curriculum series, independent of the AI Lab `M0`–`M7` repos | Umbrella over AI Lab; toolchain-only repo | "What is ai-engineer-polymath's role?" |
| D2 | Repo at `C:\Users\ADMIN\Projects\ai-engineer-polymath`, public `aswathas/ai-engineer-polymath` | Private-first; other local path | "Where should the repo live?" |
| D3 | Validator and test stack: Python 3.12 + pytest, matching the AI Lab modules | Node + vitest; mixed Python/Node | "Stack for validators and tests?" |
| D4 | Portable repo-root `agents/` and `skills/` (SKILL.md) plus `AGENTS.md` | Claude-native `.claude/` only; duplicated `.claude/` mirrors | "How should agents and skills be packaged?" |

Full entries with rationale land in `docs/reviews/decision-log.md`.

## 2. Curriculum shape

Ten modules, one capstone. Each module is a *spine with teeth*: the learner ships an artifact, not a notebook. Gates are time-boxed builds.

| Id | Slug | Title | Prereqs | Gate | Hours | Artifact the learner ships |
|----|------|-------|---------|------|-------|------------------------------|
| P0 | engineering-spine | Engineering Spine | — | G0 | 40 | Typed service with retries, idempotency, Postgres schema, tests |
| P1 | math-for-ml | Math for ML | P0 | G1 | 45 | Numerically careful optimiser and gradient checks |
| P2 | data-and-features | Data and Features | P1 | G2 | 40 | Labelled dataset, split policy, leakage audit, feature pipeline |
| P3 | classical-ml | Classical ML | P2 | G3 | 45 | Baseline + tuned model, calibrated thresholds, error analysis |
| P4 | deep-learning | Deep Learning | P3 | G4 | 50 | Training loop with reproducible seeds, checkpoints, regularisation |
| P5 | llm-mechanics | LLM Mechanics | P4 | G5 | 45 | Tokeniser, attention implementation, sampling harness with eval |
| P6 | llm-application-engineering | LLM Application Engineering | P5 | G6 | 50 | Structured-output + tool-use service with guardrails |
| P7 | evaluation | Evaluation | P6 | G7 | 45 | Eval harness: offline suite, judge rubric, regression gate |
| P8 | production-and-cost | Production and Cost | P7 | G8 | 40 | Deployable service, dashboards, cost model, rollback plan |
| P9 | product-and-delivery | Product and Delivery | P8 | G9 | 35 | AI product spec, rollout plan, pricing, failure comms |
| CAPSTONE | capstone | Polymath Capstone | P0–P9 | GCAP | 60 | One shipped AI feature spanning every module, with evidence |

Source of truth for the graph: `curriculum/curriculum.yaml` (validated for unique ids, existing prereqs, acyclicity, gate uniqueness, directory presence, and file presence).

## 3. Agents (6)

All in `agents/`, frontmatter = `name` + `description`, sections in the fixed order listed in Global Constraints.

| File | Name | One-line job | Hard-rule centre |
|------|------|--------------|------------------|
| `agents/polymath-tutor.md` | polymath-tutor | Teaches a module; never writes the learner's implementation | Worked trace after two insistences; quiz instead of code |
| `agents/polymath-reviewer.md` | polymath-reviewer | Reviews learner code and notes against gate criteria | Findings carry severity + evidence line; no silent rewrites |
| `agents/polymath-quiz-master.md` | polymath-quiz-master | Writes quizzes with answer key and rubric | Every quiz has ≥5 questions and a marked rubric |
| `agents/polymath-curator.md` | polymath-curator | Owns the curriculum graph, gates and drift between modules | Graph changes update `curriculum.yaml` and the module note |
| `agents/polymath-project-supervisor.md` | polymath-project-supervisor | Scopes capstones, writes briefs, judges submissions | Every brief states acceptance criteria and evidence required |
| `agents/polymath-eval-auditor.md` | polymath-eval-auditor | Designs eval harnesses and audits claims | No metric without a dataset and a baseline; mock numbers labelled `SIMULATED` |

## 4. Skills (9)

Each `skills/<name>/SKILL.md`, frontmatter = `name` + `description`, sections `When to use`, `Inputs`, `Procedure`, `Outputs`, `Verification`.

| Skill | Question it answers | Ships a script? |
|-------|---------------------|------------------|
| `module-note-author` | How do I write a module note that passes the template? | No |
| `gate-keeper` | Is a module done, and what exactly failed? | No (calls `tools/validators`) |
| `skill-and-agent-linter` | Are the agent and skill packs structurally valid? | Yes — `scripts/lint_pack.py` |
| `curriculum-graph` | What is the prerequisite graph, and is it acyclic? | Yes — `scripts/graph.py` |
| `issue-author` | How do the module tasks become ordered GitHub issues? | No (calls `tools/create_issues.py`) |
| `project-brief-author` | How do I write a capstone brief with a real rubric? | No |
| `eval-harness-design` | What does a defensible eval harness look like? | No |
| `glossary-keeper` | Which term does the curriculum mean by X? | No |
| `publish-github` | How do I ship this repo safely? | No (wraps `gh` + branch/push/PR) |

## 5. Capstone projects (3 briefs + the CAPSTONE module)

| Brief | Modules it exercises | Acceptance shape |
|-------|----------------------|------------------|
| `projects/PJ1-retrieval-qa-service.md` | P0, P2, P6, P7, P8 | Retrieval service with citation contract, offline eval, cost model |
| `projects/PJ2-support-triage.md` | P3, P6, P7, P9 | Classifier + human handoff, calibrated thresholds, rollout plan |
| `projects/PJ3-eval-driven-release.md` | P5, P7, P8, P9 | Prompt/model release pipeline with a regression gate that blocks bad releases |
| `curriculum/capstone/module-note.md` | P0–P9 | One feature, one repo, one evidence bundle, one retrospective |

## 6. Validators (8 modules + runner)

`tools/validators/common.py` holds `Issue`, `Result` and the shared helpers (`read_text`, `iter_markdown`, `frontmatter`, `relative_links`).

| Module | Codes | Checks |
|--------|-------|--------|
| `validate_skeleton.py` | SKEL001–010 | Required root files/dirs exist; `pyproject.toml` parses and declares the pinned deps; `.gitignore` covers secrets and caches |
| `validate_agents.py` | AGT001–008 | One file per agent, frontmatter exactly `name`+`description`, required sections present and in order, name matches filename, description non-trivial |
| `validate_skills.py` | SKL001–009 | `skills/<name>/SKILL.md` exists for every directory; frontmatter shape; required sections; `scripts/` references resolve; no skill directory is empty |
| `validate_curriculum.py` | CUR001–009 | `curriculum.yaml` parses; ids unique; prereqs exist; graph acyclic; gate ids unique; every module dir has `module-note.md` + `gate.md`; every prereq module precedes it |
| `validate_projects.py` | PRJ001–007 | Each brief has `## Goal`, `## Modules exercised`, `## Acceptance criteria`, `## Evidence required`, `## Rubric`; referenced module ids exist; rubric has ≥3 weighted rows |
| `validate_links.py` | LNK001–004 | Every relative Markdown link resolves to a file in the repo; anchors in-file exist; no link points outside the repo |
| `validate_records.py` | REC001–006 | `docs/reviews/decision-log.md`, `change-inventory.md`, `prompts.md` and `BUILDLOG.md` exist, are non-empty, and the change inventory has a row for every tracked Markdown/Python file |
| `run_all.py` | — | Runs every validator, prints a table, `--json` for machine output, exit 0/1 |

## 7. Tests (`tests/`, pytest)

- `tests/test_validators_skeleton.py` — missing root file, bad `pyproject`, secret in `.gitignore` coverage.
- `tests/test_validators_agents.py` — bad frontmatter, missing section, wrong section order, name/filename mismatch.
- `tests/test_validators_skills.py` — missing `SKILL.md`, dangling script reference, missing section.
- `tests/test_validators_curriculum.py` — unknown prereq, cycle detection, duplicate gate, missing module file.
- `tests/test_validators_projects.py` — missing rubric section, unknown module id, thin rubric.
- `tests/test_validators_links.py` — broken relative link, missing anchor, escaping link.
- `tests/test_validators_records.py` — missing inventory row, empty record file.
- `tests/test_repo_passes_validators.py` — runs every validator against the repository root; the repo must pass its own contracts.

Fixtures build a minimal fake repo in `tmp_path`, so tests never depend on the real tree except in the last file.

## 8. CI (`.github/workflows/`)

- `ci.yml`: `ubuntu-latest`, Python 3.12, install `.[dev]`, then `ruff check .`, `pytest -q`, `python tools/validators/run_all.py`.
- `docs-check.yml`: markdown link check by running `run_all.py` and `validate_links.py` only, on docs-changing pushes.
- `dependabot.yml`: pip and github-actions ecosystems, weekly.

## 9. Documentation tree

`README.md` (positioning, module table, quickstart, repo map, "what this cannot do"), `AGENTS.md` (repo rules), `CONTRIBUTING.md`, `BUILDLOG.md`, `GLOSSARY.md`, `plan.md` (this file), `docs/agents/{domain,issue-tracker,triage-labels}.md`, `docs/adr/0001-polymath-scope.md`, `docs/adr/0002-validator-stack.md`, `docs/adr/0003-agent-and-skill-packaging.md`, `docs/validator-reference.md` (every error code explained), `docs/reviews/{decision-log,change-inventory,prompts}.md`.

## 10. Target file tree

```
ai-engineer-polymath/
├── .github/workflows/{ci.yml,docs-check.yml}   .github/dependabot.yml
├── agents/{README.md,polymath-tutor.md,polymath-reviewer.md,polymath-quiz-master.md,
│           polymath-curator.md,polymath-project-supervisor.md,polymath-eval-auditor.md}
├── skills/{module-note-author,gate-keeper,skill-and-agent-linter,curriculum-graph,
│           issue-author,project-brief-author,eval-harness-design,glossary-keeper,
│           publish-github}/SKILL.md   (+ scripts/ where planned)
├── curriculum/
│   ├── overview.md   curriculum.yaml
│   ├── templates/{module-note.md,gate.md,resources.md}
│   ├── P0-engineering-spine/{module-note.md,gate.md,resources.md}
│   ├── P1-math-for-ml/{module-note.md,gate.md,resources.md}
│   ├── P2-data-and-features/{module-note.md,gate.md,resources.md}
│   ├── P3-classical-ml/{module-note.md,gate.md,resources.md}
│   ├── P4-deep-learning/{module-note.md,gate.md,resources.md}
│   ├── P5-llm-mechanics/{module-note.md,gate.md,resources.md}
│   ├── P6-llm-application-engineering/{module-note.md,gate.md,resources.md}
│   ├── P7-evaluation/{module-note.md,gate.md,resources.md}
│   ├── P8-production-and-cost/{module-note.md,gate.md,resources.md}
│   ├── P9-product-and-delivery/{module-note.md,gate.md,resources.md}
│   └── capstone/{module-note.md,gate.md,rubric.md}
├── projects/{overview.md,PJ1-retrieval-qa-service.md,PJ2-support-triage.md,PJ3-eval-driven-release.md}
├── tools/
│   ├── README.md   create_issues.py
│   └── validators/{__init__.py,common.py,validate_skeleton.py,validate_agents.py,
│                   validate_skills.py,validate_curriculum.py,validate_projects.py,
│                   validate_links.py,validate_records.py,run_all.py}
├── tests/{test_validators_skeleton.py,test_validators_agents.py,test_validators_skills.py,
│          test_validators_curriculum.py,test_validators_projects.py,
│          test_validators_links.py,test_validators_records.py,test_repo_passes_validators.py}
├── docs/{agents/{domain.md,issue-tracker.md,triage-labels.md},adr/0001-polymath-scope.md,
│         adr/0002-validator-stack.md,adr/0003-agent-and-skill-packaging.md,
│         reviews/{decision-log.md,change-inventory.md,prompts.md},validator-reference.md}
├── AGENTS.md  README.md  BUILDLOG.md  CONTRIBUTING.md  GLOSSARY.md  LICENSE  plan.md
├── pyproject.toml  .gitignore  conftest.py
```

---

## 11. Tasks (one commit per task, each independently verifiable)

| # | Task | Files | Verification | Commit |
|---|------|-------|--------------|--------|
| T1 | Repo scaffold + records | `pyproject.toml`, `.gitignore`, `conftest.py`, `README.md`, `AGENTS.md`, `LICENSE`, `docs/reviews/*`, `BUILDLOG.md` | `python -m pip install -e ".[dev]"` then `python -c "import tomllib;tomllib.load(open('pyproject.toml','rb'))"` | `chore: scaffold polymath curriculum repo` |
| T2 | Validator core + skeleton validator | `tools/validators/{__init__.py,common.py,validate_skeleton.py}` | `pytest tests/test_validators_skeleton.py -v` | `feat: add validator core and skeleton rules` |
| T3 | Agent validator + agent pack | `tools/validators/validate_agents.py`, `agents/*` | `pytest tests/test_validators_agents.py -v` | `feat: add agent pack and agent validator` |
| T4 | Skill validator + skill pack | `tools/validators/validate_skills.py`, `skills/*` | `pytest tests/test_validators_skills.py -v` | `feat: add skill pack and skill validator` |
| T5 | Curriculum validator + curriculum content | `tools/validators/validate_curriculum.py`, `curriculum/**` | `pytest tests/test_validators_curriculum.py -v` | `feat: add curriculum modules P0-P9 and capstone` |
| T6 | Project validator + capstone briefs | `tools/validators/validate_projects.py`, `projects/**`, `curriculum/capstone/rubric.md` | `pytest tests/test_validators_projects.py -v` | `feat: add capstone projects and rubric` |
| T7 | Link validator | `tools/validators/validate_links.py` | `pytest tests/test_validators_links.py -v` | `feat: add markdown link validator` |
| T8 | Record validator | `tools/validators/validate_records.py` | `pytest tests/test_validators_records.py -v` | `feat: add documentation record validator` |
| T9 | Runner + repo-self test | `tools/validators/run_all.py`, `tests/test_repo_passes_validators.py`, `tests/test_validators_records.py` | `python tools/validators/run_all.py` exits 0 | `feat: add validator runner and self-hosting test` |
| T10 | Docs + ADRs + glossary + contributing | `docs/**`, `GLOSSARY.md`, `CONTRIBUTING.md`, `README.md` refresh | `python tools/validators/run_all.py` exits 0 | `docs: complete curriculum documentation set` |
| T11 | CI workflows | `.github/workflows/*`, `.github/dependabot.yml` | `act`/manual read; YAML parses (`python -c "import yaml;yaml.safe_load(...)"`) | `ci: add github actions workflows` |
| T12 | Issue generator + issue tracker docs | `tools/create_issues.py`, `docs/agents/issue-tracker.md` | `python tools/create_issues.py --dry-run` | `feat: add curriculum issue generator` |
| T13 | Full local verification + BUILDLOG | `BUILDLOG.md`, `docs/reviews/change-inventory.md` | `ruff check . && pytest -q && python tools/validators/run_all.py` all clean | `chore: record full verification run` |
| T14 | Remote publish | remote, `main`, `feature/polymath-v1`, PR | `gh pr view` shows the PR, `git status` clean, `gh api repos/aswathas/ai-engineer-polymath` shows public | `docs: publish polymath curriculum repository` |

Execution strategy: T1 serially by the main agent; T3–T8 dispatched to parallel workers with **disjoint file ownership** (worker A owns `agents/` + `tests/test_validators_agents.py`, worker B owns `skills/` + its test, worker C owns `curriculum/` + its test, worker D owns `projects/` + its test); T2, T9–T13 by the main agent because they touch shared `tools/validators/common.py`. Every worker owns its files exclusively — one writer per file.

## 12. Definition of done

1. `ruff check .` clean.
2. `pytest -q` green, ≥60 tests.
3. `python tools/validators/run_all.py` exits 0 and reports every validator passing.
4. `docs/reviews/decision-log.md`, `change-inventory.md`, `prompts.md`, `BUILDLOG.md` current, and every tracked file has an inventory row.
5. `README.md`, `AGENTS.md`, `plan.md` present and consistent with the tree above.
6. GitHub repo `aswathas/ai-engineer-polymath` exists, **public**, with `main` carrying the scaffold and `feature/polymath-v1` merged via a pull request.
7. CI run on the PR is green.
8. No secrets, no `.env`, no paid API keys, no vendored binaries.

## 13. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Scope sprawl — 11 module directories of prose | Templates + validator enforce shape, not volume; module notes stay 40–90 lines |
| Validator self-reference breaks (repo fails its own rules) | `test_repo_passes_validators.py` runs in CI, so drift is caught at commit time |
| Parallel workers collide on shared files | Explicit disjoint ownership in the execution strategy; `tools/validators/common.py` is main-agent-only |
| Docs sprawl in the change inventory | The inventory validator fails CI when a row is missing, so it stays complete |
| Push rejected by branch protection or secret scanning | Push order fixed in Global Constraints; secret scan runs locally before push |

## 14. Approval gate

This plan is the canonical `plan.md`. Nothing is implemented until the user approves it. On approval the agent proceeds T1 → T14, then reports the PR URL, commit list, CI state and the verification output.

## 15. Implementation status (2026-11-15)

Approved and implemented. The plan was executed with two deviations, both recorded in
[docs/reviews/decision-log.md](docs/reviews/decision-log.md):

1. **Commit order.** The runner and the self-hosting test (T9) landed after the documentation
   and CI units (T10, T11), because the self-hosting test can only pass once the tree holds
   every required directory. The content of each unit is unchanged.
2. **Verification target.** Each commit was verified against its own committed tree (extracted
   with `git archive`), not against the working tree. See decision D5.

Final state: 7 validators, 0 issues; 95 pytest cases pass; `ruff check .` is clean; the issue
generator plans 80 issues across the eleven modules. See [BUILDLOG.md](BUILDLOG.md).
