"""Tests for the records validator (``tools/validators/validate_records.py``)."""

from __future__ import annotations

from pathlib import Path

from tools.validators.validate_records import validate


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def codes(issues) -> list[str]:
    return [issue.code for issue in issues]


def build_repo(root: Path) -> Path:
    write(root / "docs" / "reviews" / "decision-log.md", "## D1 - Thing\n\n**Date:** 2026-01-01\n\nPrompt.\n")
    write(root / "docs" / "reviews" / "prompts.md", "# Prompts\n\n## A prompt\n\n> hello\n")
    write(root / "docs" / "reviews" / "change-inventory.md", "| File | What | Why | How |\n")
    write(root / "BUILDLOG.md", "# Build Log\n")
    write(root / "README.md", "# Readme\n")
    return root


def test_missing_record_file_is_reported(tmp_path: Path) -> None:
    root = build_repo(tmp_path / "repo")
    (root / "BUILDLOG.md").unlink()
    issues = validate(root)
    assert "REC001" in codes(issues)


def test_empty_record_file_is_reported(tmp_path: Path) -> None:
    root = build_repo(tmp_path / "repo")
    (root / "BUILDLOG.md").write_text("   \n", encoding="utf-8")
    issues = validate(root)
    assert "REC001" in codes(issues)


def test_row_naming_a_missing_file_is_reported(tmp_path: Path) -> None:
    root = build_repo(tmp_path / "repo")
    (root / "docs" / "reviews" / "change-inventory.md").write_text(
        "| File | What | Why | How |\n"
        "| `README.md` | text | reason | proof |\n"
        "| `ghost.md` | text | reason | proof |\n",
        encoding="utf-8",
    )
    issues = validate(root)
    assert "REC002" in codes(issues)


def test_row_with_empty_column_is_reported(tmp_path: Path) -> None:
    root = build_repo(tmp_path / "repo")
    (root / "docs" / "reviews" / "change-inventory.md").write_text(
        "| File | What | Why | How |\n| `README.md` | text | reason |  |\n", encoding="utf-8"
    )
    issues = validate(root)
    assert "REC003" in codes(issues)


def test_undocumented_file_is_reported(tmp_path: Path) -> None:
    root = build_repo(tmp_path / "repo")
    write(root / "docs" / "extra.md", "# Extra\n")
    issues = validate(root)
    assert "REC004" in codes(issues)


def test_documented_file_is_accepted(tmp_path: Path) -> None:
    root = build_repo(tmp_path / "repo")
    write(root / "docs" / "extra.md", "# Extra\n")
    (root / "docs" / "reviews" / "change-inventory.md").write_text(
        "| File | What | Why | How |\n"
        "| `README.md` | text | reason | proof |\n"
        "| `docs/extra.md` | text | reason | proof |\n"
        "| `BUILDLOG.md` | text | reason | proof |\n"
        "| `docs/reviews/decision-log.md` | text | reason | proof |\n"
        "| `docs/reviews/prompts.md` | text | reason | proof |\n"
        "| `docs/reviews/change-inventory.md` | text | reason | proof |\n",
        encoding="utf-8",
    )
    issues = validate(root)
    assert "REC004" not in codes(issues)


def test_decision_without_prompt_is_reported(tmp_path: Path) -> None:
    root = build_repo(tmp_path / "repo")
    (root / "docs" / "reviews" / "decision-log.md").write_text(
        "## D1 - Thing\n\n**Date:** 2026-01-01\n", encoding="utf-8"
    )
    issues = validate(root)
    assert "REC005" in codes(issues)


def test_decision_without_date_is_reported(tmp_path: Path) -> None:
    root = build_repo(tmp_path / "repo")
    (root / "docs" / "reviews" / "decision-log.md").write_text(
        "## D1 - Thing\n\nPrompt that produced it.\n", encoding="utf-8"
    )
    issues = validate(root)
    assert "REC006" in codes(issues)
