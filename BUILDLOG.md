# Build Log

Running record of what was built, how it was verified, and what the result was. Newest entry last.

---

## 2026-11-15 - Repository inception (plan only)

**What.** Created the local repository at `C:\Users\ADMIN\Projects\ai-engineer-polymath`, initialised
git on `main`, and wrote the canonical `plan.md` together with the documentation record
(`docs/reviews/decision-log.md`, `docs/reviews/prompts.md`, `docs/reviews/change-inventory.md`).

**Verification.** Files read back from disk; no code was written yet, so no test run applies.
The plan states the verification commands each implementation task must satisfy.

**Result.** Plan written, awaiting user approval. Implementation tasks T1-T14 do not start until
that approval lands.

---

## 2026-11-15 - Series implementation (T1-T13)

**What.** Built the whole series:

| Unit | What landed |
|------|-------------|
| Scaffold | `pyproject.toml` (Python 3.12 floor, `PyYAML` runtime, `pytest` and `ruff` in the dev extra), `LICENSE`, `conftest.py`, `README.md`, `AGENTS.md`, `GLOSSARY.md`, `CONTRIBUTING.md` |
| Validator core | `tools/validators/common.py` (`Issue`, `Result`, frontmatter and link parsing) and `validate_skeleton.py` with `SKEL001`-`SKEL010` |
| Agent pack | Six agents plus the pack README, `validate_agents.py` with `AGT001`-`AGT008`, 15 tests |
| Skill pack | Nine skills plus the pack README, two standalone scripts, `validate_skills.py` with `SKL001`-`SKL009`, 18 tests |
| Curriculum | `curriculum.yaml` with P0-P9 and the capstone, the overview, three templates, eleven module notes with their gates and resource lists, `validate_curriculum.py` with `CUR001`-`CUR009`, 16 tests |
| Capstones | Three briefs plus the project overview, the capstone rubric, `validate_projects.py` with `PRJ001`-`PRJ007`, 14 tests |
| Links and records | `validate_links.py` with `LNK001`-`LNK004` and 9 tests, `validate_records.py` with `REC001`-`REC006` and 8 tests |
| Runner | `run_all.py` with a table and a `--json` report, plus the self-hosting test that runs every validator against the repository itself |
| Docs and CI | Three ADRs, three agent documents, the validator reference, `ci.yml`, `docs-check.yml`, `dependabot.yml` |
| Work items | `tools/create_issues.py`, which reads the acceptance criteria out of the module notes |

**How it was verified.** Each commit was checked against the **committed tree**, not the working
tree: the commit was extracted with `git archive` into a temporary directory and the validators and
the test-suite were run there. This matters because the validators read the tree they are shipped
with, so running them against a working tree that already contains later commits would prove
nothing about the commit in question.

| Check | Command | Result |
|-------|---------|--------|
| Lint | `ruff check .` | clean |
| Tests | `python -m pytest -q` | 95 passed, 0 failed |
| Contracts | `python tools/validators/run_all.py` | 7 validators, 0 issues |
| Issue plan | `python tools/create_issues.py --dry-run` | 80 issues planned across 11 modules |

**Result.** The series is complete and self-hosting: the repository fails its own CI the moment
the curriculum, the packs or the records drift from the contracts they claim to satisfy.
