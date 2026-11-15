"""Tests for the project-brief validator (``tools/validators/validate_projects.py``).

The fixture builds a fake repository in ``tmp_path`` with one valid brief, then each test mutates
it. The shared ``tests/conftest.py`` fixture is deliberately not used here.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.validators.validate_projects import validate

VALID_BRIEF = """# PJ1 - Sample brief

## Goal

Ship one small thing that answers questions and refuses when it cannot.

## Modules exercised

- P0 - Engineering Spine
- P7 - Evaluation

## Acceptance criteria

- [ ] The service ingests a corpus.
- [ ] Every answer cites a chunk.
- [ ] The eval runs offline.
- [ ] The cost model is written down.
- [ ] The tests cover the refusal path.

## Evidence required

- The service source and the tests.
- The eval report and the cost model.

## Rubric

| Criterion | Weight | What the evidence must show |
| --- | --- | --- |
| Correctness | 40 | The eval report and the held-out set. |
| Evaluation quality | 35 | The metric definitions and the baseline. |
| Cost | 25 | The per-query cost table with SIMULATED figures. |
"""

VALID_RUBRIC = """# CAPSTONE rubric

## How a judge uses this

Read the evidence bundle, then score the table below.

## Rubric

| Criterion | Weight | What the evidence must show |
| --- | --- | --- |
| Correctness | 20 | The feature working end to end. |
| Evaluation quality | 20 | A held-out set and a baseline. |
| Reliability | 20 | Retries, fallbacks and a rehearsed rollback. |
| Cost | 15 | A per-unit cost model with the assumptions named. |
| Documentation | 15 | A runbook and a config reference. |
| Honesty about limits | 10 | The known failure modes and the refusals. |

## Disqualifying

- A paid API used and not disclosed.
- An eval that measures the training data.
- A missing rollback plan.
"""


def write(path: Path, text: str) -> Path:
    """Write text to a path, creating parent directories.

    Returns the path that was written. Costs one file write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture
def brief_repo(tmp_path: Path) -> Path:
    """Return a fake repository holding one valid brief.

    Costs one directory creation and one file write.
    """
    root = tmp_path / "repo"
    write(root / "projects" / "PJ1-sample.md", VALID_BRIEF)
    return root


def codes(issues: list) -> list[str]:
    """Return the issue codes of a list of issues.

    Returns the codes in order. Costs one pass over the list.
    """
    return [issue.code for issue in issues]


def test_valid_brief_produces_no_issues(brief_repo: Path) -> None:
    assert validate(brief_repo) == []


def test_missing_section_is_prj001(brief_repo: Path) -> None:
    path = brief_repo / "projects" / "PJ1-sample.md"
    text = path.read_text(encoding="utf-8")
    start = text.index("## Evidence required")
    end = text.index("## Rubric")
    path.write_text(text[:start] + text[end:], encoding="utf-8")
    issues = validate(brief_repo)
    assert "PRJ001" in codes(issues)
    assert any(
        issue.code == "PRJ001" and "Evidence required" in issue.message for issue in issues
    )
    assert any(issue.path == "projects/PJ1-sample.md" for issue in issues)


def test_out_of_order_sections_is_prj002(brief_repo: Path) -> None:
    path = brief_repo / "projects" / "PJ1-sample.md"
    text = path.read_text(encoding="utf-8")
    swapped = text.replace("## Goal", "## PLACEHOLDER", 1)
    swapped = swapped.replace("## Modules exercised", "## Goal", 1)
    swapped = swapped.replace("## PLACEHOLDER", "## Modules exercised", 1)
    path.write_text(swapped, encoding="utf-8")
    issues = validate(brief_repo)
    assert "PRJ002" in codes(issues)
    assert any(issue.code == "PRJ002" and "out of order" in issue.message for issue in issues)


def test_short_acceptance_checklist_is_prj003(brief_repo: Path) -> None:
    path = brief_repo / "projects" / "PJ1-sample.md"
    text = path.read_text(encoding="utf-8")
    trimmed = "\n".join(line for line in text.splitlines() if not line.startswith("- [ ] The eval"))
    path.write_text(trimmed + "\n", encoding="utf-8")
    issues = validate(brief_repo)
    assert "PRJ003" in codes(issues)
    assert any(issue.code == "PRJ003" and "4 checklist items" in issue.message for issue in issues)


def test_unknown_module_id_is_prj004(brief_repo: Path) -> None:
    path = brief_repo / "projects" / "PJ1-sample.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("- P7 - Evaluation", "- P42 - Nothing"), encoding="utf-8")
    issues = validate(brief_repo)
    assert "PRJ004" in codes(issues)
    assert any(issue.code == "PRJ004" and "P42" in issue.message for issue in issues)


def test_capstone_id_is_valid_without_curriculum_yaml(brief_repo: Path) -> None:
    path = brief_repo / "projects" / "PJ1-sample.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("- P7 - Evaluation", "- CAPSTONE - Final gate"), encoding="utf-8")
    assert "PRJ004" not in codes(validate(brief_repo))


def test_module_ids_come_from_curriculum_yaml_when_present(brief_repo: Path) -> None:
    write(
        brief_repo / "curriculum" / "curriculum.yaml",
        "modules:\n  - id: P0\n    slug: engineering-spine\n  - id: P2\n    slug: data\n",
    )
    path = brief_repo / "projects" / "PJ1-sample.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("- P7 - Evaluation", "- P2 - Data and Features"), encoding="utf-8")
    assert "PRJ004" not in codes(validate(brief_repo))


def test_thin_rubric_table_is_prj005(brief_repo: Path) -> None:
    path = brief_repo / "projects" / "PJ1-sample.md"
    text = path.read_text(encoding="utf-8")
    start = text.index("| Criterion | Weight |")
    trimmed = text[:start] + (
        "| Criterion | Weight | What the evidence must show |\n"
        "| --- | --- | --- |\n"
        "| Correctness | 60 | The eval report. |\n"
        "| Cost | 40 | The cost table. |\n"
    )
    path.write_text(trimmed, encoding="utf-8")
    issues = validate(brief_repo)
    assert "PRJ005" in codes(issues)
    assert any(issue.code == "PRJ005" and "2 body rows" in issue.message for issue in issues)


def test_weights_that_do_not_sum_to_100_is_prj006(brief_repo: Path) -> None:
    path = brief_repo / "projects" / "PJ1-sample.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("| Cost | 25 |", "| Cost | 20 |"), encoding="utf-8")
    issues = validate(brief_repo)
    assert "PRJ006" in codes(issues)
    assert any(issue.code == "PRJ006" and "95" in issue.message for issue in issues)


def test_missing_rubric_column_is_prj007(brief_repo: Path) -> None:
    path = brief_repo / "projects" / "PJ1-sample.md"
    text = path.read_text(encoding="utf-8")
    start = text.index("| Criterion | Weight |")
    trimmed = text[:start] + (
        "| Criterion | Score | What the evidence must show |\n"
        "| --- | --- | --- |\n"
        "| Correctness | 40 | The eval report. |\n"
        "| Evaluation quality | 35 | The metric definitions. |\n"
        "| Cost | 25 | The cost table. |\n"
    )
    path.write_text(trimmed, encoding="utf-8")
    issues = validate(brief_repo)
    assert "PRJ007" in codes(issues)
    assert any(issue.code == "PRJ007" and "Weight" in issue.message for issue in issues)


def test_capstone_rubric_weights_are_checked(brief_repo: Path) -> None:
    write(
        brief_repo / "curriculum" / "capstone" / "rubric.md",
        VALID_RUBRIC.replace("| Cost | 15 |", "| Cost | 10 |"),
    )
    issues = validate(brief_repo)
    assert "PRJ006" in codes(issues)
    assert any(issue.path == "curriculum/capstone/rubric.md" for issue in issues)


def test_valid_capstone_rubric_produces_no_issues(brief_repo: Path) -> None:
    write(brief_repo / "curriculum" / "capstone" / "rubric.md", VALID_RUBRIC)
    assert validate(brief_repo) == []


def test_malformed_brief_does_not_raise(brief_repo: Path) -> None:
    write(brief_repo / "projects" / "PJ2-broken.md", "# PJ2 - Broken\n\n## Rubric\n\n| |\n|---|\n")
    issues = validate(brief_repo)
    assert isinstance(issues, list)
    assert "PRJ001" in codes(issues)


def test_non_brief_markdown_is_not_validated(brief_repo: Path) -> None:
    write(brief_repo / "projects" / "overview.md", "# Capstone projects\n\nNo sections here.\n")
    assert validate(brief_repo) == []
