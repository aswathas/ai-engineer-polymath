"""Skeleton validator: the repository must have the shape the curriculum depends on.

Codes:

``SKEL001``  a required root file is missing
``SKEL002``  a required directory is missing
``SKEL003``  ``pyproject.toml`` is missing or unparseable
``SKEL004``  ``requires-python`` does not demand 3.12 or newer
``SKEL005``  the ``dev`` extra does not depend on pytest
``SKEL006``  the ``dev`` extra does not depend on ruff
``SKEL007``  the runtime does not depend on PyYAML
``SKEL008``  ``.gitignore`` does not exclude ``.env``
``SKEL009``  ``.gitignore`` does not exclude Python caches and virtualenvs
``SKEL010``  a required root file is empty
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from tools.validators.common import Issue, read_text

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

GITIGNORE_REQUIRED = (".env", "__pycache__", ".venv", ".pytest_cache")


def validate(repo_root: Path) -> list[Issue]:
    """Check the repository skeleton. Returns one issue per finding."""
    issues: list[Issue] = []

    for name in REQUIRED_FILES:
        path = repo_root / name
        if not path.exists():
            issues.append(Issue("SKEL001", name, "required root file is missing"))
            continue
        text = read_text(path)
        if text is None:
            issues.append(Issue("SKEL003", name, "file cannot be read as UTF-8 text"))
        elif not text.strip():
            issues.append(Issue("SKEL010", name, "required root file is empty"))

    for name in REQUIRED_DIRS:
        if not (repo_root / name).is_dir():
            issues.append(Issue("SKEL002", name, "required directory is missing"))

    issues.extend(_validate_pyproject(repo_root))
    issues.extend(_validate_gitignore(repo_root))
    return issues


def _validate_pyproject(repo_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    path = repo_root / "pyproject.toml"
    if not path.exists():
        return issues

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        issues.append(Issue("SKEL003", "pyproject.toml", f"cannot parse: {exc}"))
        return issues

    project = data.get("project", {})
    requires = str(project.get("requires-python", ""))
    if "3.12" not in requires:
        issues.append(
            Issue("SKEL004", "pyproject.toml", f"requires-python is {requires!r}, expected >=3.12")
        )

    dev = project.get("optional-dependencies", {}).get("dev", [])
    dev_names = {str(dep).split(">")[0].split("=")[0].split("[")[0].strip().lower() for dep in dev}
    if "pytest" not in dev_names:
        issues.append(Issue("SKEL005", "pyproject.toml", "the dev extra does not depend on pytest"))
    if "ruff" not in dev_names:
        issues.append(Issue("SKEL006", "pyproject.toml", "the dev extra does not depend on ruff"))

    runtime = project.get("dependencies", [])
    runtime_names = {
        str(dep).split(">")[0].split("=")[0].split("[")[0].strip().lower() for dep in runtime
    }
    if "pyyaml" not in runtime_names:
        issues.append(Issue("SKEL007", "pyproject.toml", "the runtime does not depend on PyYAML"))

    return issues


def _validate_gitignore(repo_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    path = repo_root / ".gitignore"
    if not path.exists():
        return issues

    text = read_text(path)
    if text is None:
        issues.append(Issue("SKEL003", ".gitignore", "file cannot be read as UTF-8 text"))
        return issues

    lines = {
        line.strip().rstrip("/")
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    }
    if ".env" not in lines:
        issues.append(Issue("SKEL008", ".gitignore", "does not exclude .env"))
    missing = [
        pattern
        for pattern in ("__pycache__", ".venv", ".pytest_cache")
        if pattern not in lines
    ]
    if missing:
        issues.append(
            Issue(
                "SKEL009",
                ".gitignore",
                f"does not exclude {', '.join(missing)}",
            )
        )
    return issues
