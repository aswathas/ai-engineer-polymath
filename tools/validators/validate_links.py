"""Link validator: every relative Markdown link must resolve inside the repository.

Codes:

``LNK001``  a relative link does not resolve to a file in the repository
``LNK002``  a relative link escapes the repository root
``LNK003``  a fragment anchor does not exist in the target document
``LNK004``  a link points at a directory with no index document
"""

from __future__ import annotations

import re
from pathlib import Path

from tools.validators.common import Issue, iter_markdown, markdown_links, read_text, relpath

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".ruff_cache"}
INDEX_NAMES = ("index.md", "README.md", "readme.md")


def validate(repo_root: Path) -> list[Issue]:
    """Check every relative Markdown link under the repository root."""
    issues: list[Issue] = []
    root = repo_root.resolve()

    for path in iter_markdown(repo_root):
        if _skipped(path, root):
            continue
        text = read_text(path)
        if text is None:
            continue

        for target, fragment in markdown_links(text):
            if not target:
                # A pure anchor link points inside this document.
                if fragment and fragment not in _anchors(text):
                    issues.append(
                        Issue("LNK003", relpath(path, root), f"anchor #{fragment} not found in this file")
                    )
                continue

            resolved = (path.parent / target).resolve()
            if not _inside(resolved, root):
                issues.append(
                    Issue("LNK002", relpath(path, root), f"link escapes the repository: {target}")
                )
                continue

            if resolved.is_dir():
                if not any((resolved / name).is_file() for name in INDEX_NAMES):
                    issues.append(
                        Issue("LNK004", relpath(path, root), f"directory link has no index: {target}")
                    )
                continue

            if not resolved.exists():
                issues.append(
                    Issue("LNK001", relpath(path, root), f"link target does not exist: {target}")
                )
                continue

            if fragment and resolved.suffix.lower() == ".md":
                target_text = read_text(resolved)
                if target_text is not None and fragment not in _anchors(target_text):
                    issues.append(
                        Issue(
                            "LNK003",
                            relpath(path, root),
                            f"anchor #{fragment} not found in {target}",
                        )
                    )
    return issues


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _skipped(path: Path, root: Path) -> bool:
    parts = path.resolve().relative_to(root).parts
    return any(part in SKIP_DIRS for part in parts)


def _anchors(text: str) -> set[str]:
    """Return the GitHub-style anchors a Markdown document defines.

    Duplicate headings get the ``-1``, ``-2`` suffix GitHub adds, so a link to the second
    occurrence of a heading resolves.
    """
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for match in re.finditer(r"^#{1,6}\s+(?P<text>.+?)\s*$", text, re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", match.group("text").lower())
        slug = re.sub(r"\s+", "-", slug.strip())
        if not slug:
            continue
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")
    return anchors
