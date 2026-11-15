"""Shared types and helpers for the polymath validators.

Nothing in here touches the network or the clock. A validator reads the repository, returns
issues, and exits. That keeps the whole validation layer reproducible on any machine.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"\A---\s*\n(?P<meta>.*?)\n---\s*\n", re.DOTALL)
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(?P<text>.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Issue:
    """One validation finding.

    ``code`` is a stable identifier such as ``AGT001``. Codes are the contract the test
    suite asserts on, so they are never renumbered once published.
    """

    code: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.code} {self.path}: {self.message}"


@dataclass
class Result:
    """The outcome of one validator run."""

    name: str
    issues: list[Issue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "ok": self.ok,
            "issues": [
                {"code": issue.code, "path": issue.path, "message": issue.message}
                for issue in self.issues
            ],
        }


def read_text(path: Path) -> str | None:
    """Return the file text, or ``None`` when it cannot be read as UTF-8."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def iter_markdown(root: Path, subdir: str | None = None) -> list[Path]:
    """Return every ``*.md`` file under ``root`` (optionally under ``subdir``), sorted."""
    base = root / subdir if subdir else root
    if not base.exists():
        return []
    return sorted(p for p in base.rglob("*.md") if p.is_file())


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """Split YAML frontmatter from the body.

    Returns ``({}, text)`` when there is no frontmatter block. A malformed block yields
    ``({}, body)`` with the raw block kept in the body so the caller can still report it.
    """
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    body = text[match.end() :]
    try:
        meta = yaml.safe_load(match.group("meta"))
    except yaml.YAMLError:
        return {}, text
    if not isinstance(meta, dict):
        return {}, body
    return meta, body


def headings(text: str) -> set[str]:
    """Return the anchor slugs a Markdown document defines."""
    slugs: set[str] = set()
    for match in HEADING_RE.finditer(text):
        slug = re.sub(r"[^\w\- ]", "", match.group("text").lower())
        slugs.add(re.sub(r"\s+", "-", slug.strip()))
    return slugs


def relative_links(text: str) -> list[str]:
    """Return the targets of relative Markdown links (no fragments, no URLs)."""
    targets: list[str] = []
    for match in LINK_RE.finditer(text):
        target = match.group("target").strip()
        if target.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        target = target.split("#", 1)[0]
        if target:
            targets.append(target)
    return targets


def relpath(path: Path, root: Path) -> str:
    """Return a repository-relative POSIX path, for stable messages."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()
