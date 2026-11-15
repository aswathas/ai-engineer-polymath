#!/usr/bin/env python3
"""Standalone linter for the agent pack and the skill pack.

Walks ``agents/`` and ``skills/`` under a repository root and checks the structural
contract of every file it finds. The script uses the standard library only and imports
nothing from the repository, so it can be run on its own::

    python skills/skill-and-agent-linter/scripts/lint_pack.py --repo .

What it checks:

* Skills: the ``SKILL.md`` exists, the frontmatter holds exactly ``name`` and
  ``description``, the name matches the directory, the description is long enough, the
  five required sections appear once each in order with content, every
  ``scripts/<name>.py`` reference resolves, and the directory holds nothing else.
* Agents: the file has frontmatter with a ``name`` matching the file stem and a
  description, and the agent sections appear in order. The expected agent sections
  default to *Role*, *Triggers*, *Hard rules*, *Workflow*, *Output contract* and
  *Refusals*; override them with ``--agent-sections``.

Exit codes: 0 when the packs are structurally valid, 1 when at least one finding was
reported.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SKILL_SECTIONS: tuple[str, ...] = (
    "When to use",
    "Inputs",
    "Procedure",
    "Outputs",
    "Verification",
)

AGENT_SECTIONS: tuple[str, ...] = (
    "Role",
    "Triggers",
    "Hard rules",
    "Workflow",
    "Output contract",
    "Refusals",
)

MIN_DESCRIPTION_LENGTH = 40
SKILL_FILENAME = "SKILL.md"
SCRIPTS_DIRNAME = "scripts"

SCRIPT_REF_RE = re.compile(r"(?<![\w\-/])scripts/[\w\-]+\.py")
_SECTION_RE = re.compile(r"^##\s+(?P<text>.+?)\s*$")
_FENCE_RE = re.compile(r"^\s*```")


@dataclass(frozen=True)
class Finding:
    """One structural problem found in the packs.

    ``code`` identifies the rule that was broken and ``path`` is the file it applies
    to, both relative to the repository root.
    """

    code: str
    path: str
    message: str

    def __str__(self) -> str:
        """Return the one-line rendering of the finding."""
        return f"{self.code} {self.path}: {self.message}"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Split simple YAML frontmatter from a Markdown body.

    Returns ``(metadata, body)``. A block that does not open with ``---`` on the first
    line yields empty metadata and the original text. Only flat ``key: value`` pairs
    are understood, which is all the packs use. The cost is one pass over the text.
    """
    text = text.removeprefix("\ufeff")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    meta: dict[str, str] = {}
    for index in range(1, len(lines)):
        line = lines[index]
        if line.strip() == "---":
            return meta, "\n".join(lines[index + 1 :])
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            continue
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return {}, text


def split_sections(body: str) -> list[tuple[str, list[str]]]:
    """Split a Markdown body into its level-two sections.

    Returns a list of ``(title, content lines)`` pairs in document order, ignoring
    headings inside fenced code blocks. The cost is one pass over the body.
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


def has_content(lines: list[str]) -> bool:
    """Return True when a section body holds at least one non-empty content line."""
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return True
    return False


def lint_skills(repo_root: Path, skills_dir: Path) -> list[Finding]:
    """Lint every skill directory under ``skills_dir``.

    Returns the findings for the whole skill pack, sorted by directory. The cost is
    one directory listing plus one read per SKILL.md.
    """
    findings: list[Finding] = []
    if not skills_dir.is_dir():
        return findings

    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        findings.extend(lint_skill(repo_root, skill_dir))
    return findings


def lint_skill(repo_root: Path, skill_dir: Path) -> list[Finding]:
    """Lint one skill directory.

    Returns the findings for that skill. The cost is one read of SKILL.md plus one
    directory listing.
    """
    findings: list[Finding] = []
    skill_file = skill_dir / SKILL_FILENAME
    rel = relative(skill_file, repo_root)

    if not skill_file.is_file():
        return [Finding("LINT001", rel, "the skill directory has no SKILL.md")]

    try:
        text = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return [Finding("LINT002", rel, "SKILL.md cannot be read as UTF-8 text")]

    meta, body = parse_frontmatter(text)
    findings.extend(lint_skill_frontmatter(meta, skill_dir.name, rel))
    findings.extend(lint_skill_sections(body, rel))
    findings.extend(lint_script_refs(body, skill_dir, rel))
    findings.extend(lint_stray_files(repo_root, skill_dir))
    return findings


def lint_skill_frontmatter(meta: dict[str, str], dir_name: str, rel: str) -> list[Finding]:
    """Lint the frontmatter of a skill.

    Returns the findings for the frontmatter: a missing or unexpected key, a name that
    does not match the directory, and a description that is too short. The cost is
    constant.
    """
    findings: list[Finding] = []

    name = meta.get("name")
    description = meta.get("description")

    if name is None:
        findings.append(Finding("LINT003", rel, "frontmatter is missing the 'name' key"))
    elif name != dir_name:
        findings.append(
            Finding(
                "LINT005",
                rel,
                f"frontmatter name '{name}' does not match the directory name '{dir_name}'",
            )
        )

    if description is None:
        findings.append(Finding("LINT004", rel, "frontmatter is missing the 'description' key"))
    elif len(description.strip()) < MIN_DESCRIPTION_LENGTH:
        findings.append(
            Finding(
                "LINT006",
                rel,
                f"the description is {len(description.strip())} characters, "
                f"expected at least {MIN_DESCRIPTION_LENGTH}",
            )
        )

    for key in sorted(key for key in meta if key not in ("name", "description")):
        findings.append(Finding("LINT007", rel, f"frontmatter carries the unexpected key '{key}'"))

    return findings


def lint_skill_sections(body: str, rel: str) -> list[Finding]:
    """Lint the required sections of a skill.

    Returns the findings for missing, empty, repeated or misordered sections. The
    cost is one pass over the body.
    """
    findings: list[Finding] = []
    sections = split_sections(body)

    by_title: dict[str, list[list[str]]] = {}
    first_index: dict[str, int] = {}
    for index, (title, content) in enumerate(sections):
        by_title.setdefault(title, []).append(content)
        first_index.setdefault(title, index)

    for title in SKILL_SECTIONS:
        entries = by_title.get(title)
        if not entries:
            findings.append(Finding("LINT008", rel, f"the required section '{title}' is missing"))
            continue
        if len(entries) > 1:
            findings.append(
                Finding(
                    "LINT009",
                    rel,
                    f"the required section '{title}' appears {len(entries)} times, expected once",
                )
            )
        if not has_content(entries[0]):
            findings.append(
                Finding("LINT008", rel, f"the required section '{title}' has no content")
            )

    indices = [first_index.get(title) for title in SKILL_SECTIONS]
    if all(index is not None for index in indices) and list(indices) != sorted(indices):
        findings.append(
            Finding(
                "LINT009",
                rel,
                "the required sections are not in the required order: " + ", ".join(SKILL_SECTIONS),
            )
        )

    return findings


def lint_script_refs(body: str, skill_dir: Path, rel: str) -> list[Finding]:
    """Lint the ``scripts/<name>.py`` references of a skill.

    Returns one finding per reference that does not exist inside the skill directory.
    The cost is one regex pass over the body plus one existence check per reference.
    """
    findings: list[Finding] = []
    seen: set[str] = set()
    for match in SCRIPT_REF_RE.finditer(body):
        reference = match.group(0)
        if reference in seen:
            continue
        seen.add(reference)
        if not (skill_dir / reference).is_file():
            findings.append(
                Finding(
                    "LINT010",
                    rel,
                    f"the referenced script '{reference}' does not exist in the skill directory",
                )
            )
    return findings


def lint_stray_files(repo_root: Path, skill_dir: Path) -> list[Finding]:
    """Lint the top level of a skill directory.

    Returns one finding per entry that is neither ``SKILL.md`` nor the ``scripts/``
    directory. The cost is one directory listing.
    """
    findings: list[Finding] = []
    try:
        entries = sorted(skill_dir.iterdir())
    except OSError:
        return findings

    for entry in entries:
        if entry.name == SKILL_FILENAME:
            continue
        try:
            is_dir = entry.is_dir()
        except OSError:
            is_dir = False
        if is_dir and entry.name == SCRIPTS_DIRNAME:
            continue
        findings.append(
            Finding(
                "LINT011",
                relative(entry, repo_root),
                "the skill directory may only contain SKILL.md and a scripts/ directory",
            )
        )
    return findings


def lint_agents(
    repo_root: Path,
    agents_dir: Path,
    agent_sections: tuple[str, ...],
) -> list[Finding]:
    """Lint every agent definition under ``agents_dir``.

    An agent file must have frontmatter with a ``name`` matching the file stem and a
    description, and must present the expected sections in order. The cost is one read
    per agent file.
    """
    findings: list[Finding] = []
    if not agents_dir.is_dir():
        return findings

    for agent_file in sorted(agents_dir.glob("*.md")):
        if agent_file.name.lower() == "readme.md":
            continue
        findings.extend(lint_agent(repo_root, agent_file, agent_sections))
    return findings


def lint_agent(repo_root: Path, agent_file: Path, agent_sections: tuple[str, ...]) -> list[Finding]:
    """Lint one agent definition file.

    Returns the findings for that agent. The cost is one read of the file.
    """
    findings: list[Finding] = []
    rel = relative(agent_file, repo_root)

    try:
        text = agent_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return [Finding("LINT012", rel, "the agent file cannot be read as UTF-8 text")]

    meta, body = parse_frontmatter(text)
    if not meta:
        findings.append(Finding("LINT013", rel, "the agent file has no YAML frontmatter"))

    name = meta.get("name")
    if name is None:
        findings.append(Finding("LINT014", rel, "frontmatter is missing the 'name' key"))
    elif name != agent_file.stem:
        findings.append(
            Finding(
                "LINT015",
                rel,
                f"frontmatter name '{name}' does not match the file stem '{agent_file.stem}'",
            )
        )

    description = meta.get("description")
    if description is None:
        findings.append(Finding("LINT016", rel, "frontmatter is missing the 'description' key"))

    findings.extend(lint_agent_sections(body, agent_sections, rel))
    return findings


def lint_agent_sections(body: str, agent_sections: tuple[str, ...], rel: str) -> list[Finding]:
    """Lint the sections of an agent definition.

    The section names are matched case-insensitively so that *Hard rules* and *Hard
    Rules* are the same section. Returns the findings for missing or misordered
    sections. The cost is one pass over the body.
    """
    findings: list[Finding] = []
    if not agent_sections:
        return findings

    sections = split_sections(body)
    positions: dict[str, int] = {}
    for index, (title, _) in enumerate(sections):
        positions.setdefault(title.lower(), index)

    indices: list[int] = []
    for title in agent_sections:
        index = positions.get(title.lower())
        if index is None:
            findings.append(Finding("LINT017", rel, f"the required section '{title}' is missing"))
            continue
        indices.append(index)

    if len(indices) == len(agent_sections) and indices != sorted(indices):
        findings.append(
            Finding(
                "LINT018",
                rel,
                "the required sections are not in the required order: "
                + ", ".join(agent_sections),
            )
        )
    return findings


def relative(path: Path, root: Path) -> str:
    """Return a repository-relative POSIX path for a message.

    Falls back to the absolute path when the file sits outside the root. The cost is
    two path resolutions.
    """
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the linter. The cost is constant."""
    parser = argparse.ArgumentParser(
        prog="lint_pack.py",
        description="Check that the agent pack and the skill pack are structurally valid.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="repository root (default: the current directory)",
    )
    parser.add_argument("--agents-dir", default="agents", help="agent pack directory")
    parser.add_argument("--skills-dir", default="skills", help="skill pack directory")
    parser.add_argument(
        "--agent-sections",
        default=",".join(AGENT_SECTIONS),
        help="comma-separated agent section names in the expected order",
    )
    parser.add_argument("--json", action="store_true", help="print the findings as JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the linter over a repository.

    Returns 0 when the packs are valid and 1 when at least one finding was reported.
    The cost is one directory listing per pack plus one read per definition file.
    """
    args = build_parser().parse_args(argv)
    repo_root = Path(args.repo).expanduser().resolve()

    agent_sections = tuple(
        name.strip() for name in args.agent_sections.split(",") if name.strip()
    )

    findings: list[Finding] = []
    findings.extend(lint_agents(repo_root, repo_root / args.agents_dir, agent_sections))
    findings.extend(lint_skills(repo_root, repo_root / args.skills_dir))

    if args.json:
        print(
            json.dumps(
                {
                    "ok": not findings,
                    "findings": [
                        {"code": finding.code, "path": finding.path, "message": finding.message}
                        for finding in findings
                    ],
                },
                indent=2,
            )
        )
    else:
        for finding in findings:
            print(finding)
        if findings:
            print(f"{len(findings)} finding(s).")
        else:
            print("OK: the agent pack and the skill pack are structurally valid.")

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
