"""Tests for the link validator (``tools/validators/validate_links.py``)."""

from __future__ import annotations

from pathlib import Path

from tools.validators.validate_links import validate


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def codes(issues) -> list[str]:
    return [issue.code for issue in issues]


def test_valid_links_produce_no_issues(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    write(root / "docs" / "a.md", "# Title\n\n[to b](b.md)\n")
    write(root / "docs" / "b.md", "# Other\n")
    assert validate(root) == []


def test_broken_relative_link_is_reported(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    write(root / "docs" / "a.md", "[gone](missing.md)\n")
    issues = validate(root)
    assert "LNK001" in codes(issues)


def test_link_escaping_the_repository_is_reported(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    write(root / "docs" / "a.md", "[out](../../outside.md)\n")
    (tmp_path / "outside.md").write_text("# outside\n", encoding="utf-8")
    issues = validate(root)
    assert "LNK002" in codes(issues)


def test_missing_anchor_is_reported(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    write(root / "docs" / "a.md", "[anchor](b.md#nope)\n")
    write(root / "docs" / "b.md", "# Present\n")
    issues = validate(root)
    assert "LNK003" in codes(issues)


def test_existing_anchor_is_accepted(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    write(root / "docs" / "a.md", "[anchor](b.md#present)\n")
    write(root / "docs" / "b.md", "# Present\n")
    assert validate(root) == []


def test_duplicate_heading_anchor_is_accepted(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    write(root / "docs" / "a.md", "[anchor](b.md#present-1)\n")
    write(root / "docs" / "b.md", "# Present\n\n# Present\n")
    assert validate(root) == []


def test_directory_link_without_index_is_reported(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "docs" / "sub").mkdir(parents=True)
    write(root / "docs" / "a.md", "[dir](sub)\n")
    issues = validate(root)
    assert "LNK004" in codes(issues)


def test_directory_link_with_index_is_accepted(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    write(root / "docs" / "sub" / "index.md", "# Index\n")
    write(root / "docs" / "a.md", "[dir](sub)\n")
    assert validate(root) == []


def test_absolute_urls_are_ignored(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    write(
        root / "docs" / "a.md",
        "# Top\n\n[web](https://example.com/nope) [mail](mailto:a@b.c) [anchor](#top)\n",
    )
    assert validate(root) == []
