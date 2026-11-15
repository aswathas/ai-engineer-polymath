"""Tests for the skill validator (``tools/validators/validate_skills.py``).

Every test builds its own fake repository inside ``tmp_path``. Nothing here depends on
``tests/conftest.py`` and nothing touches the real tree.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.validators.validate_skills import validate

DESCRIPTION = "Use when a fake skill is checked against the shared SKILL.md contract."

VALID_SKILL = f"""---
name: demo-skill
description: {DESCRIPTION}
---

# Demo Skill

## When to use

Use this skill when the fixture is mutated by a test.

## Inputs

- A module id.

## Procedure

1. Read the input.
2. Write the output.

## Outputs

- A written result.

## Verification

Run the validator and confirm it reports no issue.
"""


def build_repo(tmp_path: Path) -> Path:
    """Build a fake repository holding one valid skill.

    Returns the repository root. The cost is a handful of small file writes.
    """
    root = tmp_path / "repo"
    skill_dir = root / "skills" / "demo-skill"
    skill_dir.mkdir(parents=True)
    (root / "skills" / "README.md").write_text("# Skills\n", encoding="utf-8")
    (skill_dir / "SKILL.md").write_text(VALID_SKILL, encoding="utf-8")
    return root


def codes(issues: list) -> list[str]:
    """Return the issue codes of a validator run."""
    return [issue.code for issue in issues]


def skill_path(root: Path) -> Path:
    """Return the path of the fake skill's SKILL.md."""
    return root / "skills" / "demo-skill" / "SKILL.md"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Return a fake repository with one valid skill."""
    return build_repo(tmp_path)


def test_valid_pack_reports_no_issue(repo: Path) -> None:
    assert validate(repo) == []


def test_missing_skill_md_is_reported(repo: Path) -> None:
    skill_path(repo).unlink()
    issues = validate(repo)
    assert "SKL001" in codes(issues)
    assert any(issue.path == "skills/demo-skill/SKILL.md" for issue in issues)


def test_missing_pack_readme_is_reported(repo: Path) -> None:
    (repo / "skills" / "README.md").unlink()
    issues = validate(repo)
    assert "SKL001" in codes(issues)
    assert any(issue.path == "skills/README.md" for issue in issues)


def test_missing_frontmatter_key_is_reported(repo: Path) -> None:
    path = skill_path(repo)
    path.write_text(
        VALID_SKILL.replace("name: demo-skill\n", ""),
        encoding="utf-8",
    )
    issues = validate(repo)
    assert "SKL002" in codes(issues)


def test_extra_frontmatter_key_is_reported(repo: Path) -> None:
    path = skill_path(repo)
    path.write_text(
        VALID_SKILL.replace("name: demo-skill\n", "name: demo-skill\nversion: 1\n"),
        encoding="utf-8",
    )
    issues = validate(repo)
    assert "SKL003" in codes(issues)


def test_missing_section_is_reported(repo: Path) -> None:
    path = skill_path(repo)
    text = path.read_text(encoding="utf-8")
    start = text.index("## Verification")
    path.write_text(text[:start], encoding="utf-8")
    issues = validate(repo)
    assert "SKL004" in codes(issues)


def test_empty_section_is_reported(repo: Path) -> None:
    path = skill_path(repo)
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("## Outputs\n\n- A written result.\n", "## Outputs\n\n"),
        encoding="utf-8",
    )
    issues = validate(repo)
    assert "SKL004" in codes(issues)


def test_sections_out_of_order_are_reported(repo: Path) -> None:
    path = skill_path(repo)
    text = path.read_text(encoding="utf-8")
    procedure = "## Procedure\n\n1. Read the input.\n2. Write the output.\n\n"
    outputs = "## Outputs\n\n- A written result.\n\n"
    assert procedure in text
    assert outputs in text
    path.write_text(text.replace(procedure + outputs, outputs + procedure), encoding="utf-8")
    issues = validate(repo)
    assert "SKL005" in codes(issues)


def test_duplicate_section_is_reported(repo: Path) -> None:
    path = skill_path(repo)
    text = path.read_text(encoding="utf-8")
    path.write_text(text + "\n## Procedure\n\n1. Again.\n", encoding="utf-8")
    issues = validate(repo)
    assert "SKL005" in codes(issues)


def test_missing_script_reference_is_reported(repo: Path) -> None:
    path = skill_path(repo)
    path.write_text(
        VALID_SKILL.replace(
            "1. Read the input.",
            "1. Run `scripts/missing_tool.py` first.",
        ),
        encoding="utf-8",
    )
    issues = validate(repo)
    assert "SKL006" in codes(issues)


def test_existing_script_reference_is_accepted(repo: Path) -> None:
    scripts = repo / "skills" / "demo-skill" / "scripts"
    scripts.mkdir()
    (scripts / "helper.py").write_text("# helper\n", encoding="utf-8")
    path = skill_path(repo)
    path.write_text(
        VALID_SKILL.replace("1. Read the input.", "1. Run `scripts/helper.py` first."),
        encoding="utf-8",
    )
    assert validate(repo) == []


def test_name_mismatch_is_reported(repo: Path) -> None:
    path = skill_path(repo)
    path.write_text(VALID_SKILL.replace("name: demo-skill", "name: other-skill"), encoding="utf-8")
    issues = validate(repo)
    assert "SKL007" in codes(issues)


def test_short_description_is_reported(repo: Path) -> None:
    path = skill_path(repo)
    path.write_text(
        VALID_SKILL.replace(
            f"description: {DESCRIPTION}",
            "description: Too short.",
        ),
        encoding="utf-8",
    )
    issues = validate(repo)
    assert "SKL008" in codes(issues)


def test_byte_order_mark_does_not_hide_the_frontmatter(repo: Path) -> None:
    path = skill_path(repo)
    path.write_bytes(b"\xef\xbb\xbf" + VALID_SKILL.encode("utf-8"))
    assert validate(repo) == []


def test_stray_top_level_file_is_reported(repo: Path) -> None:
    (repo / "skills" / "demo-skill" / "notes.md").write_text("notes\n", encoding="utf-8")
    issues = validate(repo)
    assert "SKL009" in codes(issues)
    assert any(issue.path == "skills/demo-skill/notes.md" for issue in issues)


def test_malformed_frontmatter_does_not_raise(repo: Path) -> None:
    path = skill_path(repo)
    path.write_text(
        "---\nname: [unclosed\n---\n\n# Demo\n\n## When to use\n\nText.\n",
        encoding="utf-8",
    )
    issues = validate(repo)
    assert "SKL002" in codes(issues)


def test_unreadable_skill_file_does_not_raise(repo: Path) -> None:
    skill_path(repo).write_bytes(b"\xff\xfe\x00binary")
    issues = validate(repo)
    assert "SKL001" in codes(issues)


def test_missing_skills_directory_is_reported(tmp_path: Path) -> None:
    root = tmp_path / "empty"
    root.mkdir()
    issues = validate(root)
    assert "SKL001" in codes(issues)
