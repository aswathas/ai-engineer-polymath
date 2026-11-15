"""Tests for the curriculum validator (``tools/validators/validate_curriculum.py``).

Every test builds a fake curriculum in ``tmp_path``: a two-module graph with the same shape
as the real one. The fixture lives in this file on purpose - the shared ``conftest.py``
belongs to the skeleton validator and this suite must stand on its own.
"""

from __future__ import annotations

from pathlib import Path

from tools.validators.validate_curriculum import validate

CURRICULUM_YAML = """\
series: polymath
version: 1
modules:
  - id: P0
    slug: alpha
    dir: P0-alpha
    title: Alpha
    hours: 40
    prereqs: []
    gate: G0
  - id: P1
    slug: beta
    dir: P1-beta
    title: Beta
    hours: 45
    prereqs:
      - P0
    gate: G1
"""

MODULE_NOTE = """\
# {module_id} - {title}

## What

One paragraph of real content for the {module_id} module.

## Why it comes here

Because {module_id} builds on the module before it.

## What gets built

A small service that does one thing.

## Acceptance criteria

- The service starts.
- The tests pass.

## The artifact

One artifact, checked in beside the code.

## Notes

No notes worth repeating.
"""

GATE = """\
# Gate {gate} - {title}

## Time box

120 minutes.

## The task

Build the thing from the module note, start to finish.

## Then answer out loud

1. What breaks without this?
2. Why this order?
3. How would you check it?

## Pass

The artifact exists and the three answers are correct.

## Fail

Do not start the next module. Fix this one and re-run the gate.
"""


def write(path: Path, text: str) -> Path:
    """Write text to a path, creating parent directories.

    Returns the path written. Costs one file write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def fake_repo(tmp_path: Path) -> Path:
    """Build a minimal but valid two-module curriculum repository.

    Returns the repository root. Costs a handful of small file writes.
    """
    root = tmp_path / "repo"
    write(root / "curriculum" / "curriculum.yaml", CURRICULUM_YAML)
    for module_id, gate, title, directory in (
        ("P0", "G0", "Alpha", "P0-alpha"),
        ("P1", "G1", "Beta", "P1-beta"),
    ):
        module_dir = root / "curriculum" / directory
        write(module_dir / "module-note.md", MODULE_NOTE.format(module_id=module_id, title=title))
        write(module_dir / "gate.md", GATE.format(gate=gate, title=title))
    return root


def yaml_path(root: Path) -> Path:
    """Return the path of the fake curriculum manifest.

    Returns the path. Costs nothing.
    """
    return root / "curriculum" / "curriculum.yaml"


def rewrite_yaml(root: Path, old: str, new: str) -> None:
    """Replace one snippet inside the fake curriculum manifest.

    Returns nothing. Costs one read and one write of the manifest.
    """
    path = yaml_path(root)
    text = path.read_text(encoding="utf-8")
    assert old in text, "fixture snippet not found"
    path.write_text(text.replace(old, new), encoding="utf-8")


def codes(issues) -> list[str]:
    """Return the issue codes in order.

    Returns a list of code strings. Costs one pass over the issues.
    """
    return [issue.code for issue in issues]


def test_valid_curriculum_has_no_issues(tmp_path: Path) -> None:
    """A well-formed two-module curriculum produces no findings at all."""
    assert validate(fake_repo(tmp_path)) == []


def test_missing_curriculum_yaml_is_reported(tmp_path: Path) -> None:
    """A missing manifest is CUR001 and stops the run."""
    root = fake_repo(tmp_path)
    yaml_path(root).unlink()
    issues = validate(root)
    assert "CUR001" in codes(issues)
    assert any(issue.path == "curriculum/curriculum.yaml" for issue in issues)


def test_unparseable_curriculum_yaml_is_reported(tmp_path: Path) -> None:
    """A manifest that is not valid YAML is CUR001, not an exception."""
    root = fake_repo(tmp_path)
    write(yaml_path(root), "series: polymath\nmodules: [\n")
    issues = validate(root)
    assert "CUR001" in codes(issues)


def test_yaml_without_modules_list_is_reported(tmp_path: Path) -> None:
    """A manifest with no modules list is CUR001."""
    root = fake_repo(tmp_path)
    write(yaml_path(root), "series: polymath\nversion: 1\n")
    issues = validate(root)
    assert "CUR001" in codes(issues)


def test_missing_module_field_is_reported(tmp_path: Path) -> None:
    """A module without a required field is CUR002."""
    root = fake_repo(tmp_path)
    rewrite_yaml(root, "    hours: 40\n", "")
    issues = validate(root)
    assert "CUR002" in codes(issues)
    assert any("hours" in issue.message for issue in issues)


def test_duplicate_module_id_is_reported(tmp_path: Path) -> None:
    """Two modules sharing an id is CUR003."""
    root = fake_repo(tmp_path)
    rewrite_yaml(root, "  - id: P1\n", "  - id: P0\n")
    issues = validate(root)
    assert "CUR003" in codes(issues)


def test_unknown_prereq_is_reported(tmp_path: Path) -> None:
    """A prereq naming a module that does not exist is CUR004."""
    root = fake_repo(tmp_path)
    rewrite_yaml(root, "      - P0\n", "      - P9\n")
    issues = validate(root)
    assert "CUR004" in codes(issues)


def test_prerequisite_cycle_is_reported(tmp_path: Path) -> None:
    """Two modules requiring each other is CUR005."""
    root = fake_repo(tmp_path)
    rewrite_yaml(root, "    prereqs: []\n", "    prereqs:\n      - P1\n")
    issues = validate(root)
    assert "CUR005" in codes(issues)


def test_duplicate_gate_id_is_reported(tmp_path: Path) -> None:
    """Two modules sharing a gate id is CUR006."""
    root = fake_repo(tmp_path)
    rewrite_yaml(root, "    gate: G1\n", "    gate: G0\n")
    issues = validate(root)
    assert "CUR006" in codes(issues)


def test_missing_module_directory_is_reported(tmp_path: Path) -> None:
    """A module whose directory does not exist is CUR007."""
    root = fake_repo(tmp_path)
    (root / "curriculum" / "P1-beta").rename(root / "curriculum" / "P1-gamma")
    issues = validate(root)
    assert "CUR007" in codes(issues)
    assert any(issue.path == "curriculum/P1-beta" for issue in issues)


def test_missing_module_note_is_reported(tmp_path: Path) -> None:
    """A module directory without module-note.md is CUR007."""
    root = fake_repo(tmp_path)
    (root / "curriculum" / "P0-alpha" / "module-note.md").unlink()
    issues = validate(root)
    assert "CUR007" in codes(issues)
    assert any(
        issue.path == "curriculum/P0-alpha/module-note.md" for issue in issues
    )


def test_missing_gate_file_is_reported(tmp_path: Path) -> None:
    """A module directory without gate.md is CUR007."""
    root = fake_repo(tmp_path)
    (root / "curriculum" / "P0-alpha" / "gate.md").unlink()
    issues = validate(root)
    assert "CUR007" in codes(issues)
    assert any(issue.path == "curriculum/P0-alpha/gate.md" for issue in issues)


def test_missing_section_is_reported(tmp_path: Path) -> None:
    """A module note without the 'The artifact' section is CUR008."""
    root = fake_repo(tmp_path)
    path = root / "curriculum" / "P0-alpha" / "module-note.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("## The artifact", "## Artifact"), encoding="utf-8")
    issues = validate(root)
    assert "CUR008" in codes(issues)
    assert any("The artifact" in issue.message for issue in issues)


def test_out_of_order_sections_are_reported(tmp_path: Path) -> None:
    """A module note whose sections are shuffled is CUR008."""
    root = fake_repo(tmp_path)
    path = root / "curriculum" / "P1-beta" / "module-note.md"
    text = path.read_text(encoding="utf-8")
    notes = "## Notes\n\nNo notes worth repeating.\n"
    assert notes in text
    path.write_text(notes + text.replace(notes, ""), encoding="utf-8")
    issues = validate(root)
    assert "CUR008" in codes(issues)
    assert any("out of order" in issue.message for issue in issues)


def test_empty_section_is_reported(tmp_path: Path) -> None:
    """A module note with an empty section is CUR008."""
    root = fake_repo(tmp_path)
    path = root / "curriculum" / "P0-alpha" / "module-note.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("## Notes\n\nNo notes worth repeating.\n", "## Notes\n\n"),
        encoding="utf-8",
    )
    issues = validate(root)
    assert "CUR008" in codes(issues)


def test_later_prereq_is_reported(tmp_path: Path) -> None:
    """A prereq that comes later in the series order is CUR009."""
    root = fake_repo(tmp_path)
    rewrite_yaml(
        root, "    hours: 40\n    prereqs: []\n", "    hours: 40\n    prereqs:\n      - P1\n"
    )
    rewrite_yaml(root, "    prereqs:\n      - P0\n", "    prereqs: []\n")
    issues = validate(root)
    assert "CUR009" in codes(issues)
    assert "CUR005" not in codes(issues)
