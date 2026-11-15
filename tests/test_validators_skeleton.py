"""Tests for the skeleton validator (``tools/validators/validate_skeleton.py``)."""

from __future__ import annotations

from pathlib import Path

from tools.validators.validate_skeleton import validate


def codes(issues) -> list[str]:
    return [issue.code for issue in issues]


def test_valid_repo_has_no_issues(fake_repo: Path) -> None:
    assert validate(fake_repo) == []


def test_missing_root_file_is_reported(fake_repo: Path) -> None:
    (fake_repo / "README.md").unlink()
    issues = validate(fake_repo)
    assert "SKEL001" in codes(issues)
    assert any(issue.path == "README.md" for issue in issues)


def test_missing_directory_is_reported(fake_repo: Path) -> None:
    import shutil

    shutil.rmtree(fake_repo / "agents")
    issues = validate(fake_repo)
    assert "SKEL002" in codes(issues)
    assert any(issue.path == "agents" for issue in issues)


def test_empty_root_file_is_reported(fake_repo: Path) -> None:
    (fake_repo / "AGENTS.md").write_text("   \n", encoding="utf-8")
    issues = validate(fake_repo)
    assert "SKEL010" in codes(issues)


def test_unparseable_pyproject_is_reported(fake_repo: Path) -> None:
    (fake_repo / "pyproject.toml").write_text("[project\nname =", encoding="utf-8")
    issues = validate(fake_repo)
    assert "SKEL003" in codes(issues)


def test_old_python_floor_is_reported(fake_repo: Path) -> None:
    path = fake_repo / "pyproject.toml"
    path.write_text(path.read_text(encoding="utf-8").replace(">=3.12", ">=3.9"), encoding="utf-8")
    issues = validate(fake_repo)
    assert "SKEL004" in codes(issues)


def test_missing_dev_dependencies_are_reported(fake_repo: Path) -> None:
    path = fake_repo / "pyproject.toml"
    path.write_text(
        path.read_text(encoding="utf-8").replace('dev = ["pytest>=8.0", "ruff>=0.6"]', "dev = []"),
        encoding="utf-8",
    )
    issues = validate(fake_repo)
    assert "SKEL005" in codes(issues)
    assert "SKEL006" in codes(issues)


def test_missing_runtime_dependency_is_reported(fake_repo: Path) -> None:
    path = fake_repo / "pyproject.toml"
    path.write_text(
        path.read_text(encoding="utf-8").replace('dependencies = ["PyYAML>=6.0"]', "dependencies = []"),
        encoding="utf-8",
    )
    issues = validate(fake_repo)
    assert "SKEL007" in codes(issues)


def test_gitignore_must_ignore_env(fake_repo: Path) -> None:
    path = fake_repo / ".gitignore"
    path.write_text(
        path.read_text(encoding="utf-8").replace(".env\n", ""), encoding="utf-8"
    )
    issues = validate(fake_repo)
    assert "SKEL008" in codes(issues)


def test_gitignore_must_ignore_caches(fake_repo: Path) -> None:
    path = fake_repo / ".gitignore"
    path.write_text(path.read_text(encoding="utf-8").replace(".venv/\n", ""), encoding="utf-8")
    issues = validate(fake_repo)
    assert "SKEL009" in codes(issues)
