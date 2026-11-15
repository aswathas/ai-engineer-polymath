"""Records validator: the documentation record must cover the code it documents.

Codes:

``REC001``  a required record file is missing or empty
``REC002``  an inventory row names a file that does not exist in the repository
``REC003``  an inventory row has an empty column
``REC004``  a tracked Markdown or Python file has no row in the change inventory
``REC005``  a decision log entry does not record the prompt that produced it
``REC006``  a decision log entry does not record a date
"""

from __future__ import annotations

import re
from pathlib import Path

from tools.validators.common import Issue, read_text, relpath

RECORD_FILES = (
    "docs/reviews/decision-log.md",
    "docs/reviews/change-inventory.md",
    "docs/reviews/prompts.md",
    "BUILDLOG.md",
)

CODE_GLOBS = ("tools/**/*.py", "tests/**/*.py", "conftest.py")
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".ruff_cache"}
ROW_RE = re.compile(r"^\|\s*`(?P<path>[^`]+)`\s*\|(?P<rest>.*)$")
ENTRY_RE = re.compile(r"^##\s+(?P<title>.+)$", re.MULTILINE)


def validate(repo_root: Path) -> list[Issue]:
    """Check the review records against the tree they describe."""
    issues: list[Issue] = []

    texts: dict[str, str] = {}
    for name in RECORD_FILES:
        path = repo_root / name
        if not path.is_file():
            issues.append(Issue("REC001", name, "record file is missing"))
            continue
        text = read_text(path)
        if text is None or not text.strip():
            issues.append(Issue("REC001", name, "record file is empty"))
            continue
        texts[name] = text

    inventory = texts.get("docs/reviews/change-inventory.md")
    if inventory is not None:
        issues.extend(_check_inventory_rows(repo_root, inventory))
        issues.extend(_check_inventory_coverage(repo_root, inventory))

    log = texts.get("docs/reviews/decision-log.md")
    if log is not None:
        issues.extend(_check_decision_entries(log))

    return issues


def _inventory_rows(inventory: str) -> list[tuple[str, list[str]]]:
    rows: list[tuple[str, list[str]]] = []
    for line in inventory.splitlines():
        match = ROW_RE.match(line.strip())
        if not match:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append((match.group("path"), cells))
    return rows


def _check_inventory_rows(repo_root: Path, inventory: str) -> list[Issue]:
    issues: list[Issue] = []
    for path, cells in _inventory_rows(inventory):
        if not (repo_root / path).exists():
            issues.append(
                Issue("REC002", "docs/reviews/change-inventory.md", f"row names a missing file: {path}")
            )
        if len(cells) < 4 or any(not cell for cell in cells[1:]):
            issues.append(
                Issue(
                    "REC003",
                    "docs/reviews/change-inventory.md",
                    f"row for {path} has an empty column or fewer than four columns",
                )
            )
    return issues


def _tracked_files(repo_root: Path) -> list[str]:
    files: list[str] = []
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root).as_posix()
        if any(part in SKIP_DIRS for part in path.relative_to(repo_root).parts):
            continue
        if path.suffix == ".md" or rel in {"conftest.py"}:
            files.append(rel)
        elif path.suffix == ".py" and rel.startswith(("tools/", "tests/")):
            files.append(rel)
    return files


def _check_inventory_coverage(repo_root: Path, inventory: str) -> list[Issue]:
    documented = {path for path, _ in _inventory_rows(inventory)}
    issues: list[Issue] = []
    for rel in _tracked_files(repo_root):
        if rel in documented:
            continue
        issues.append(
            Issue(
                "REC004",
                "docs/reviews/change-inventory.md",
                f"no inventory row for {rel}",
            )
        )
    return issues


def _check_decision_entries(log: str) -> list[Issue]:
    issues: list[Issue] = []
    entries = list(ENTRY_RE.finditer(log))
    for index, match in enumerate(entries):
        start = match.end()
        end = entries[index + 1].start() if index + 1 < len(entries) else len(log)
        body = log[start:end]
        title = match.group("title").strip()
        if "Prompt that produced it" not in body:
            issues.append(
                Issue("REC005", "docs/reviews/decision-log.md", f"entry '{title}' records no prompt")
            )
        if "**Date:**" not in body:
            issues.append(
                Issue("REC006", "docs/reviews/decision-log.md", f"entry '{title}' records no date")
            )
    return issues
