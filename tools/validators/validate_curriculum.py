"""Curriculum validator: the module graph, the module notes and the gates must agree.

The curriculum is a graph, not a folder of prose. ``curriculum/curriculum.yaml`` is the source
of truth for the module order, the prerequisite edges, the gate ids and the directory each
module lives in. Everything else - the module note, the gate, the resource list - has to
agree with that graph or the series lies to the learner about what comes next.

Codes:

``CUR001``  ``curriculum.yaml`` is missing, unparseable, or has no ``modules`` list
``CUR002``  a module is missing a required field (id, slug, dir, title, hours, prereqs, gate)
``CUR003``  two modules share the same id
``CUR004``  a prereq names a module id that does not exist
``CUR005``  the prerequisite graph contains a cycle
``CUR006``  two modules share the same gate id
``CUR007``  a module directory or one of its required files (module-note.md, gate.md) is missing
``CUR008``  a module note or gate file is missing a required section or has them out of order
``CUR009``  a module's prereq does not come earlier in the series order

The validator never raises. A malformed file becomes an issue, never an exception: the
series has to stay readable even while it is being edited.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from tools.validators.common import Issue, read_text, relpath

CURRICULUM_YAML = "curriculum/curriculum.yaml"
CURRICULUM_DIR = "curriculum"

REQUIRED_FIELDS = ("id", "slug", "dir", "title", "hours", "prereqs", "gate")
STRING_FIELDS = ("id", "slug", "dir", "title", "gate")

MODULE_NOTE_SECTIONS = (
    "What",
    "Why it comes here",
    "What gets built",
    "Acceptance criteria",
    "The artifact",
    "Notes",
)

GATE_SECTIONS = (
    "Time box",
    "The task",
    "Then answer out loud",
    "Pass",
    "Fail",
)

SECTION_RE = re.compile(r"^##\s+(?P<text>.+?)\s*$", re.MULTILINE)


def validate(repo_root: Path) -> list[Issue]:
    """Validate the curriculum graph against the module notes and gates.

    Reads ``curriculum/curriculum.yaml`` and every module directory it names. Returns one
    :class:`Issue` per finding, sorted by code and then path, and never raises: a file that
    cannot be parsed or read is reported as an issue instead of an exception.
    """
    issues: list[Issue] = []

    data = _load_curriculum(repo_root, issues)
    if data is None:
        return issues

    raw_modules = data.get("modules")
    if not isinstance(raw_modules, list) or not raw_modules:
        issues.append(Issue("CUR001", CURRICULUM_YAML, "has no 'modules' list"))
        return issues

    modules = _read_modules(raw_modules, issues)
    known_ids = _check_unique_ids(modules, issues)
    _check_unique_gates(modules, issues)
    _check_prereqs(modules, known_ids, issues)
    _check_cycle(modules, known_ids, issues)
    _check_module_files(repo_root, modules, issues)

    issues.sort(key=lambda issue: (issue.code, issue.path, issue.message))
    return issues


def _load_curriculum(repo_root: Path, issues: list[Issue]) -> dict[str, Any] | None:
    """Read and parse ``curriculum/curriculum.yaml``.

    Returns the parsed mapping, or ``None`` after appending a ``CUR001`` issue when the file
    is missing, unreadable or not a YAML mapping. Costs one file read.
    """
    path = repo_root / CURRICULUM_YAML
    if not path.is_file():
        issues.append(Issue("CUR001", CURRICULUM_YAML, "curriculum.yaml is missing"))
        return None

    text = read_text(path)
    if text is None:
        issues.append(Issue("CUR001", CURRICULUM_YAML, "cannot be read as UTF-8 text"))
        return None

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        issues.append(Issue("CUR001", CURRICULUM_YAML, f"cannot be parsed as YAML: {exc}"))
        return None

    if not isinstance(data, dict):
        issues.append(Issue("CUR001", CURRICULUM_YAML, "top level is not a mapping"))
        return None
    return data


def _read_modules(raw_modules: list[Any], issues: list[Issue]) -> list[dict[str, Any]]:
    """Normalise the raw ``modules`` list into per-module dictionaries.

    Every module that is a mapping is kept, even when a field is bad, so that one broken
    entry does not hide the rest of the graph. Returns the normalised list and appends one
    ``CUR002`` issue per missing or ill-typed field. Costs one pass over the list.
    """
    modules: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_modules):
        if not isinstance(raw, dict):
            issues.append(
                Issue("CUR002", CURRICULUM_YAML, f"module #{index + 1} is not a mapping")
            )
            continue

        label = f"module '{raw.get('id', index + 1)}'"
        missing = [name for name in REQUIRED_FIELDS if name not in raw]
        if missing:
            issues.append(
                Issue(
                    "CUR002",
                    CURRICULUM_YAML,
                    f"{label} is missing required field(s): {', '.join(missing)}",
                )
            )

        for name in STRING_FIELDS:
            value = raw.get(name)
            if name in raw and (not isinstance(value, str) or not value.strip()):
                issues.append(
                    Issue(
                        "CUR002",
                        CURRICULUM_YAML,
                        f"{label} field '{name}' must be a non-empty string",
                    )
                )

        hours = raw.get("hours")
        if "hours" in raw and (isinstance(hours, bool) or not isinstance(hours, int)):
            issues.append(
                Issue("CUR002", CURRICULUM_YAML, f"{label} field 'hours' must be an integer")
            )

        prereqs = raw.get("prereqs")
        if "prereqs" in raw and (
            not isinstance(prereqs, list)
            or not all(isinstance(item, str) and item.strip() for item in prereqs)
        ):
            issues.append(
                Issue(
                    "CUR002",
                    CURRICULUM_YAML,
                    f"{label} field 'prereqs' must be a list of module ids",
                )
            )

        entry: dict[str, Any] = {"_index": index, "_label": label}
        entry.update({name: raw.get(name) for name in REQUIRED_FIELDS})
        modules.append(entry)
    return modules


def _module_id(entry: dict[str, Any]) -> str | None:
    """Return a module's id when it is a usable string, otherwise ``None``."""
    value = entry.get("id")
    if isinstance(value, str) and value.strip():
        return value
    return None


def _module_prereqs(entry: dict[str, Any]) -> list[str]:
    """Return the module's prereq ids, ignoring entries that are not usable strings."""
    prereqs = entry.get("prereqs")
    if not isinstance(prereqs, list):
        return []
    return [item for item in prereqs if isinstance(item, str) and item.strip()]


def _check_unique_ids(modules: list[dict[str, Any]], issues: list[Issue]) -> dict[str, int]:
    """Check that module ids are unique.

    Returns a mapping of module id to its position in the series list, keeping the first
    occurrence of each id. Appends one ``CUR003`` issue per repeated id. Costs one pass.
    """
    known: dict[str, int] = {}
    for entry in modules:
        module_id = _module_id(entry)
        if module_id is None:
            continue
        if module_id in known:
            issues.append(
                Issue("CUR003", CURRICULUM_YAML, f"module id '{module_id}' is used twice")
            )
            continue
        known[module_id] = entry["_index"]
    return known


def _check_unique_gates(modules: list[dict[str, Any]], issues: list[Issue]) -> None:
    """Check that gate ids are unique.

    Appends one ``CUR006`` issue per module that reuses a gate id already seen. A repeated
    gate id means two modules share one pass mark, which silently corrupts progress
    tracking. Costs one pass over the modules.
    """
    seen: dict[str, str] = {}
    for entry in modules:
        gate = entry.get("gate")
        if not isinstance(gate, str) or not gate.strip():
            continue
        if gate in seen:
            issues.append(
                Issue(
                    "CUR006",
                    CURRICULUM_YAML,
                    f"gate id '{gate}' is shared by module '{seen[gate]}' and "
                    f"module '{_module_id(entry)}'",
                )
            )
            continue
        seen[gate] = _module_id(entry) or gate


def _check_prereqs(
    modules: list[dict[str, Any]], known_ids: dict[str, int], issues: list[Issue]
) -> None:
    """Check that every prereq exists and comes earlier in the series order.

    Appends a ``CUR004`` issue for a prereq naming an unknown id, and a ``CUR009`` issue
    for a prereq that appears later in the series list. Costs one pass over the modules.
    """
    for entry in modules:
        module_id = _module_id(entry)
        for prereq in _module_prereqs(entry):
            if prereq not in known_ids:
                issues.append(
                    Issue(
                        "CUR004",
                        CURRICULUM_YAML,
                        f"module '{module_id}' requires unknown module '{prereq}'",
                    )
                )
                continue
            if known_ids[prereq] >= entry["_index"]:
                issues.append(
                    Issue(
                        "CUR009",
                        CURRICULUM_YAML,
                        f"module '{module_id}' requires '{prereq}', which does not come "
                        f"earlier in the series order",
                    )
                )


def _check_cycle(
    modules: list[dict[str, Any]], known_ids: dict[str, int], issues: list[Issue]
) -> None:
    """Check that the prerequisite graph is acyclic.

    Walks the edges depth first and reports every module that takes part in a cycle with
    one ``CUR005`` issue. Costs one traversal of the graph.
    """
    edges: dict[str, list[str]] = {}
    for entry in modules:
        module_id = _module_id(entry)
        if module_id is None:
            continue
        edges[module_id] = [
            prereq for prereq in _module_prereqs(entry) if prereq in known_ids
        ]

    state: dict[str, int] = {}
    cycle_nodes: set[str] = set()

    def visit(node: str, stack: list[str]) -> None:
        state[node] = 0
        stack.append(node)
        for neighbour in edges.get(node, []):
            if state.get(neighbour) == 0:
                start = stack.index(neighbour)
                cycle_nodes.update(stack[start:])
            elif neighbour not in state:
                visit(neighbour, stack)
        stack.pop()
        state[node] = 1

    for node in edges:
        if node not in state:
            visit(node, [])

    for node in sorted(cycle_nodes):
        issues.append(
            Issue(
                "CUR005",
                CURRICULUM_YAML,
                f"module '{node}' takes part in a prerequisite cycle",
            )
        )


def _check_module_files(
    repo_root: Path, modules: list[dict[str, Any]], issues: list[Issue]
) -> None:
    """Check that every module directory holds a well-formed module note and gate.

    Appends a ``CUR007`` issue for a missing directory or file, and a ``CUR008`` issue for
    a missing, empty or misordered section. Costs two file reads per module.
    """
    for entry in modules:
        directory = entry.get("dir")
        if not isinstance(directory, str) or not directory.strip():
            continue

        module_dir = repo_root / CURRICULUM_DIR / directory
        if not module_dir.is_dir():
            issues.append(
                Issue(
                    "CUR007",
                    relpath(module_dir, repo_root),
                    "module directory is missing",
                )
            )
            continue

        note_path = module_dir / "module-note.md"
        if not note_path.is_file():
            issues.append(
                Issue("CUR007", relpath(note_path, repo_root), "module note is missing")
            )
        else:
            issues.extend(
                _check_sections(note_path, MODULE_NOTE_SECTIONS, repo_root, "module note")
            )

        gate_path = module_dir / "gate.md"
        if not gate_path.is_file():
            issues.append(
                Issue("CUR007", relpath(gate_path, repo_root), "gate file is missing")
            )
        else:
            issues.extend(
                _check_sections(gate_path, GATE_SECTIONS, repo_root, "gate")
            )


def _check_sections(
    path: Path, expected: tuple[str, ...], repo_root: Path, kind: str
) -> list[Issue]:
    """Check that a Markdown file carries the required sections, in order, with content.

    Returns a list of ``CUR007`` or ``CUR008`` issues and never raises. Costs one file
    read and one regex scan of the text.
    """
    relative = relpath(path, repo_root)
    text = read_text(path)
    if text is None:
        return [Issue("CUR007", relative, f"{kind} cannot be read as UTF-8 text")]

    matches = list(SECTION_RE.finditer(text))
    names: list[str] = []
    bodies: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        name = match.group("text").strip()
        names.append(name)
        bodies[name] = text[match.end() : end].strip()

    issues: list[Issue] = []
    positions: list[int] = []
    for name in expected:
        if name not in names:
            issues.append(Issue("CUR008", relative, f"missing section '## {name}'"))
            continue
        positions.append(names.index(name))
        if not bodies[name]:
            issues.append(Issue("CUR008", relative, f"section '## {name}' has no content"))

    if len(positions) == len(expected) and positions != sorted(positions):
        issues.append(
            Issue(
                "CUR008",
                relative,
                f"sections are out of order, expected: {', '.join(expected)}",
            )
        )
    return issues
