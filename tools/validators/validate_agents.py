"""Validator for the agent pack in ``agents/``.

Every agent file is a Markdown document with YAML frontmatter carrying exactly ``name`` and
``description``, and six required sections in a fixed order. The validator checks that
structure and nothing else: it does not judge whether an agent is well written, only whether
it can be loaded by a harness and obeyed as a contract.

Codes:

``AGT001``  a required section is missing, or a required agent file is missing
``AGT002``  frontmatter is missing a required key (``name`` or ``description``)
``AGT003``  frontmatter carries a key other than ``name`` or ``description``
``AGT004``  the required sections are not in the required order, or one is duplicated
``AGT005``  frontmatter ``name`` does not match the filename stem
``AGT006``  the description is shorter than 40 characters
``AGT007``  the file is empty or cannot be read as UTF-8 text
``AGT008``  a section exists but has no content under it

``agents/README.md`` is exempt from the agent-format rules; it only has to exist.

The validator never raises on a malformed file. Every failure is reported as an issue.
"""

from __future__ import annotations

import re
from pathlib import Path

from tools.validators.common import Issue, parse_frontmatter, read_text, relpath

AGENT_DIR = "agents"
README_NAME = "README.md"
REQUIRED_AGENTS = (
    "polymath-tutor",
    "polymath-reviewer",
    "polymath-quiz-master",
    "polymath-curator",
    "polymath-project-supervisor",
    "polymath-eval-auditor",
)
REQUIRED_SECTIONS = (
    "Role",
    "Triggers",
    "Hard Rules",
    "Workflow",
    "Output Contract",
    "Refusals",
)
FRONTMATTER_KEYS = frozenset({"name", "description"})
MIN_DESCRIPTION_LENGTH = 40

_HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<text>.+?)\s*$", re.MULTILINE)


def validate(repo_root: Path) -> list[Issue]:
    """Check the agent pack under ``repo_root``.

    Returns one :class:`~tools.validators.common.Issue` per finding, with a stable code and
    a repository-relative path. An empty list means the pack is structurally valid. The
    cost is one pass over the agent files; nothing here touches the network or the clock.
    """
    issues: list[Issue] = []

    agents_dir = repo_root / AGENT_DIR
    readme = agents_dir / README_NAME
    if not readme.exists():
        issues.append(
            Issue("AGT001", relpath(readme, repo_root), "the agent pack README is missing")
        )

    found: set[str] = set()
    for path in _iter_agent_files(agents_dir):
        if path == readme:
            continue
        found.add(path.stem)
        issues.extend(_validate_agent_file(path, repo_root))

    for stem in REQUIRED_AGENTS:
        if stem not in found:
            issues.append(
                Issue(
                    "AGT001",
                    f"{AGENT_DIR}/{stem}.md",
                    "a required agent file is missing",
                )
            )

    return issues


def _iter_agent_files(agents_dir: Path) -> list[Path]:
    """Return every agent Markdown file under ``agents_dir``, sorted.

    Returns an empty list when the directory does not exist. The cost is one directory
    walk.
    """
    if not agents_dir.is_dir():
        return []
    return sorted(p for p in agents_dir.rglob("*.md") if p.is_file())


def _validate_agent_file(path: Path, repo_root: Path) -> list[Issue]:
    """Check one agent file's frontmatter and section structure.

    Returns the issues found in that file. A file that cannot be read or is empty yields a
    single issue and is not checked further. The cost is one read of the file.
    """
    issues: list[Issue] = []
    rel = relpath(path, repo_root)

    text = read_text(path)
    if text is None:
        return [Issue("AGT007", rel, "the file cannot be read as UTF-8 text")]
    if not text.strip():
        return [Issue("AGT007", rel, "the file is empty")]

    try:
        meta, body = parse_frontmatter(text)
    except Exception:  # a malformed frontmatter block must not crash the validator
        meta, body = {}, text
    if not isinstance(meta, dict):
        meta = {}

    issues.extend(_check_frontmatter(meta, path, rel))
    issues.extend(_check_sections(body, rel))
    return issues


def _check_frontmatter(meta: dict[str, object], path: Path, rel: str) -> list[Issue]:
    """Check the frontmatter keys, the name, and the description length.

    Returns one issue per problem found. The cost is a constant number of comparisons.
    """
    issues: list[Issue] = []

    for key in sorted(FRONTMATTER_KEYS):
        if key not in meta:
            issues.append(Issue("AGT002", rel, f"frontmatter is missing the {key!r} key"))

    for key in sorted(str(k) for k in meta):
        if key not in FRONTMATTER_KEYS:
            issues.append(Issue("AGT003", rel, f"frontmatter carries the unexpected key {key!r}"))

    if "name" in meta:
        name = meta["name"]
        if not isinstance(name, str) or name != path.stem:
            issues.append(
                Issue(
                    "AGT005",
                    rel,
                    f"frontmatter name {name!r} does not match the filename stem {path.stem!r}",
                )
            )

    if "description" in meta:
        description = meta["description"]
        if not isinstance(description, str) or len(description.strip()) < MIN_DESCRIPTION_LENGTH:
            issues.append(
                Issue(
                    "AGT006",
                    rel,
                    f"the description is shorter than {MIN_DESCRIPTION_LENGTH} characters",
                )
            )

    return issues


def _check_sections(body: str, rel: str) -> list[Issue]:
    """Check that the six required sections exist once each, in order, with content.

    Returns one issue per problem found. The cost is one pass over the body's headings.
    """
    issues: list[Issue] = []
    blocks = _section_blocks(body)

    counts: dict[str, int] = {}
    for title, _lines in blocks:
        counts[title] = counts.get(title, 0) + 1

    for section in REQUIRED_SECTIONS:
        count = counts.get(section, 0)
        if count == 0:
            issues.append(Issue("AGT001", rel, f"the required section {section!r} is missing"))
        elif count > 1:
            issues.append(
                Issue(
                    "AGT004",
                    rel,
                    f"the section {section!r} appears {count} times, expected exactly once",
                )
            )

    expected = [section for section in REQUIRED_SECTIONS if counts.get(section, 0) == 1]
    actual = [
        title
        for title, _lines in blocks
        if counts.get(title, 0) == 1 and title in REQUIRED_SECTIONS
    ]
    if actual != expected:
        issues.append(
            Issue(
                "AGT004",
                rel,
                f"the required sections are out of order: found {actual}, expected {expected}",
            )
        )

    for title, lines in blocks:
        if title in REQUIRED_SECTIONS and not lines:
            issues.append(Issue("AGT008", rel, f"the section {title!r} has no content under it"))

    return issues


def _section_blocks(body: str) -> list[tuple[str, list[str]]]:
    """Split a body into its level-2 sections.

    Returns a list of ``(heading_text, content_lines)`` pairs in document order, where
    ``content_lines`` holds the non-empty, non-heading lines between that heading and the
    next heading of the same or higher level. The cost is one pass over the body.
    """
    matches = list(_HEADING_RE.finditer(body))
    blocks: list[tuple[str, list[str]]] = []
    for index, match in enumerate(matches):
        if len(match.group("hashes")) != 2:
            continue
        start = match.end()
        end = len(body)
        for later in matches[index + 1 :]:
            if len(later.group("hashes")) <= 2:
                end = later.start()
                break
        region = body[start:end]
        lines = [
            line
            for line in region.splitlines()
            if line.strip() and not _HEADING_RE.match(line)
        ]
        blocks.append((match.group("text").strip(), lines))
    return blocks
