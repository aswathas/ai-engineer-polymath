"""Shared pytest fixtures for the validator test-suite.

Every fixture builds a *fake* repository in ``tmp_path``. Only
``test_repo_passes_validators.py`` touches the real tree.

Fixture helpers live here so that each test file can stay focused on its own validator.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "GLOSSARY.md",
    "LICENSE",
    "BUILDLOG.md",
    "plan.md",
    "pyproject.toml",
    ".gitignore",
)

REQUIRED_DIRS = (
    "agents",
    "skills",
    "curriculum",
    "projects",
    "tests",
    "tools/validators",
    "docs/reviews",
    "docs/adr",
    ".github/workflows",
)

PYPROJECT = """\
[project]
name = "ai-engineer-polymath"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["PyYAML>=6.0"]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.6"]
"""

GITIGNORE = """\
__pycache__/
.venv/
.pytest_cache/
.ruff_cache/
.env
"""


def write(path: Path, text: str) -> Path:
    """Write text to a path, creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture
def fake_repo(tmp_path: Path) -> Path:
    """Return a minimal repository that satisfies the skeleton contract."""
    root = tmp_path / "repo"
    for name in REQUIRED_FILES:
        write(root / name, "placeholder content\n")
    write(root / "pyproject.toml", PYPROJECT)
    write(root / ".gitignore", GITIGNORE)
    for name in REQUIRED_DIRS:
        (root / name).mkdir(parents=True, exist_ok=True)
    return root
