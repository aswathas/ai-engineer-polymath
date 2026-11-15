"""Validator for the skill pack: every skill must satisfy the shared SKILL.md contract.

A skill is a directory under ``skills/`` holding a ``SKILL.md`` and, optionally, a
``scripts/`` directory. The contract is deliberately small so that a skill can be
read by a machine:

* YAML frontmatter with exactly two keys, ``name`` and ``description``.
* ``name`` equals the directory name.
* ``description`` is at least 40 characters long.
* Five level-two sections, each exactly once and in this order: *When to use*,
  *Inputs*, *Procedure*, *Outputs*, *Verification*, each with at least one
  non-empty content line.
* Every ``scripts/<name>.py`` mentioned in the body exists inside the skill directory.
* No other top-level file in the skill directory.

``skills/README.md`` is exempt from the format rules but must exist.

Codes:

``SKL001``  a skill directory has no SKILL.md (or the skill pack README is missing)
``SKL002``  frontmatter is missing a required key (name or description)
``SKL003``  frontmatter carries a key other than name/description
``SKL004``  a required section is missing, duplicated away, or has no content
``SKL005``  the required sections are not exactly once each in the required order
``SKL006``  a referenced script does not exist inside the skill directory
``SKL007``  frontmatter ``name`` does not match the directory name
``SKL008``  the description is shorter than 40 characters
``SKL009``  the skill directory contains a stray top-level file
"""

from __future__ import annotations

import re
from pathlib import Path

from tools.validators.common import Issue, parse_frontmatter, read_text, relpath

REQUIRED_SECTIONS: tuple[str, ...] = (
    "When to use",
    "Inputs",
    "Procedure",
    "Outputs",
    "Verification",
)

MIN_DESCRIPTION_LENGTH = 40

SKILL_FILENAME = "SKILL.md"
SCRIPTS_DIRNAME = "scripts"
PACK_README = "README.md"

#: A ``scripts/<name>.py`` reference. The lookbehind stops the match from firing on a
#: longer path such as ``skills/other/scripts/tool.py``, which is not a reference
#: relative to the skill that mentions it.
SCRIPT_REF_RE = re.compile(r"(?<![\w\-/])scripts/[\w\-]+\.py")

_SECTION_RE = re.compile(r"^##\s+(?P<text>.+?)\s*$")
_FENCE_RE = re.compile(r"^\s*```")


def validate(repo_root: Path) -> list[Issue]:
    """Check every skill in the pack against the SKILL.md contract.

    Returns one issue per finding, ordered by skill directory and then by check. It
    never raises: a malformed file is reported as an issue, not as an exception.
    """
    issues: list[Issue] = []

    skills_root = repo_root / "skills"
    readme = skills_root / PACK_README
    if not readme.is_file():
        issues.append(
            Issue("SKL001", relpath(readme, repo_root), "the skill pack README is missing")
        )

    for skill_dir in _skill_dirs(skills_root):
        issues.extend(_validate_skill_dir(repo_root, skill_dir))

    return issues


def _skill_dirs(skills_root: Path) -> list[Path]:
    """Return the skill directories under ``skills_root``, sorted by name.

    Returns an empty list when the directory is absent or unreadable. The cost is one
    directory listing.
    """
    try:
        entries = sorted(skills_root.iterdir())
    except OSError:
        return []
    return [entry for entry in entries if entry.is_dir()]


def _validate_skill_dir(repo_root: Path, skill_dir: Path) -> list[Issue]:
    """Check one skill directory. Returns the issues found inside it."""
    issues: list[Issue] = []
    skill_file = skill_dir / SKILL_FILENAME

    if not skill_file.is_file():
        issues.append(
            Issue(
                "SKL001",
                relpath(skill_file, repo_root),
                "the skill directory has no SKILL.md",
            )
        )
        return issues

    path = relpath(skill_file, repo_root)
    text = read_text(skill_file)
    if text is None:
        issues.append(Issue("SKL001", path, "SKILL.md cannot be read as UTF-8 text"))
        return issues

    # A byte-order mark written by a Windows editor would hide the frontmatter block
    # from the shared parser, so it is dropped before the file is parsed.
    text = text.removeprefix("\ufeff")
    meta, body = parse_frontmatter(text)
    issues.extend(_validate_frontmatter(meta, skill_dir.name, path))
    issues.extend(_validate_sections(body, path))
    issues.extend(_validate_script_refs(body, skill_dir, path))
    issues.extend(_validate_stray_files(repo_root, skill_dir))
    return issues


def _validate_frontmatter(meta: dict[str, object], dir_name: str, path: str) -> list[Issue]:
    """Check the frontmatter keys, the name and the description length.

    Returns one issue per broken rule; the code for each is SKL002 (missing key),
    SKL003 (unexpected key), SKL007 (name mismatch) or SKL008 (short description).
    """
    issues: list[Issue] = []

    name = meta.get("name")
    description = meta.get("description")

    if name is None:
        issues.append(Issue("SKL002", path, "frontmatter is missing the 'name' key"))
    elif not isinstance(name, str):
        issues.append(Issue("SKL002", path, "frontmatter 'name' is not a string"))

    if description is None:
        issues.append(Issue("SKL002", path, "frontmatter is missing the 'description' key"))
    elif not isinstance(description, str):
        issues.append(Issue("SKL002", path, "frontmatter 'description' is not a string"))

    for key in sorted(str(key) for key in meta if key not in ("name", "description")):
        issues.append(Issue("SKL003", path, f"frontmatter carries the unexpected key '{key}'"))

    if isinstance(name, str) and name != dir_name:
        issues.append(
            Issue(
                "SKL007",
                path,
                f"frontmatter name '{name}' does not match the directory name '{dir_name}'",
            )
        )

    if isinstance(description, str):
        length = len(description.strip())
        if length < MIN_DESCRIPTION_LENGTH:
            issues.append(
                Issue(
                    "SKL008",
                    path,
                    f"the description is {length} characters, "
                    f"expected at least {MIN_DESCRIPTION_LENGTH}",
                )
            )

    return issues


def _validate_sections(body: str, path: str) -> list[Issue]:
    """Check that the five required sections appear once each, in order, with content.

    Returns SKL004 for a missing or empty section and SKL005 for a section that is
    repeated or for sections that appear out of order.
    """
    issues: list[Issue] = []
    sections = _split_sections(body)

    by_title: dict[str, list[list[str]]] = {}
    first_index: dict[str, int] = {}
    for index, (title, content) in enumerate(sections):
        by_title.setdefault(title, []).append(content)
        first_index.setdefault(title, index)

    for title in REQUIRED_SECTIONS:
        entries = by_title.get(title)
        if not entries:
            issues.append(Issue("SKL004", path, f"the required section '{title}' is missing"))
            continue
        if len(entries) > 1:
            issues.append(
                Issue(
                    "SKL005",
                    path,
                    f"the required section '{title}' appears {len(entries)} times, expected once",
                )
            )
        if not any(_is_content(line) for line in entries[0]):
            issues.append(Issue("SKL004", path, f"the required section '{title}' has no content"))

    indices = [first_index.get(title) for title in REQUIRED_SECTIONS]
    if all(index is not None for index in indices):
        if list(indices) != sorted(indices):
            issues.append(
                Issue(
                    "SKL005",
                    path,
                    "the required sections are not in the required order: "
                    + ", ".join(REQUIRED_SECTIONS),
                )
            )

    return issues


def _validate_script_refs(body: str, skill_dir: Path, path: str) -> list[Issue]:
    """Check that every ``scripts/<name>.py`` reference exists inside the skill.

    Returns one SKL006 issue per missing script. The cost is one regex pass over the
    body and one existence check per distinct reference.
    """
    issues: list[Issue] = []
    seen: set[str] = set()
    for match in SCRIPT_REF_RE.finditer(body):
        reference = match.group(0)
        if reference in seen:
            continue
        seen.add(reference)
        if not (skill_dir / reference).is_file():
            issues.append(
                Issue(
                    "SKL006",
                    path,
                    f"the referenced script '{reference}' does not exist in the skill directory",
                )
            )
    return issues


def _validate_stray_files(repo_root: Path, skill_dir: Path) -> list[Issue]:
    """Check that the skill directory holds only SKILL.md and a scripts/ directory.

    Returns one SKL009 issue per stray entry. The cost is one directory listing.
    """
    issues: list[Issue] = []
    try:
        entries = sorted(skill_dir.iterdir())
    except OSError:
        return issues

    for entry in entries:
        if entry.name == SKILL_FILENAME:
            continue
        try:
            is_dir = entry.is_dir()
        except OSError:
            is_dir = False
        if is_dir and entry.name == SCRIPTS_DIRNAME:
            continue
        issues.append(
            Issue(
                "SKL009",
                relpath(entry, repo_root),
                "the skill directory may only contain SKILL.md and a scripts/ directory",
            )
        )
    return issues


def _split_sections(body: str) -> list[tuple[str, list[str]]]:
    """Split a Markdown body into its level-two sections.

    Returns a list of ``(title, content lines)`` pairs in document order. Headings
    inside fenced code blocks are ignored. The cost is one pass over the body.
    """
    sections: list[tuple[str, list[str]]] = []
    current_title: str | None = None
    current: list[str] = []
    in_fence = False

    for line in body.splitlines():
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            if current_title is not None:
                current.append(line)
            continue
        if not in_fence:
            match = _SECTION_RE.match(line)
            if match:
                if current_title is not None:
                    sections.append((current_title, current))
                current_title = match.group("text").strip()
                current = []
                continue
        if current_title is not None:
            current.append(line)

    if current_title is not None:
        sections.append((current_title, current))
    return sections


def _is_content(line: str) -> bool:
    """Return True when a body line counts as content rather than blank or a heading."""
    stripped = line.strip()
    return bool(stripped) and not stripped.startswith("#")
