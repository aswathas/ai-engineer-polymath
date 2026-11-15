"""Validate the capstone project briefs and the capstone rubric.

Codes:

``PRJ001``  a brief is missing a required section
``PRJ002``  the sections are not in the required order
``PRJ003``  "Acceptance criteria" has fewer than five checklist items
``PRJ004``  "Modules exercised" names a module id that does not exist in the series
``PRJ005``  the rubric table has fewer than three body rows
``PRJ006``  the rubric weights do not sum to 100
``PRJ007``  the rubric table is missing a required column

The validator reads only files inside ``repo_root``. It touches neither the network nor the clock,
and it never raises on a malformed file: it returns an issue instead.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from tools.validators.common import Issue, read_text, relpath

REQUIRED_SECTIONS: tuple[str, ...] = (
    "Goal",
    "Modules exercised",
    "Acceptance criteria",
    "Evidence required",
    "Rubric",
)
RUBRIC_COLUMNS: tuple[str, ...] = ("Criterion", "Weight", "What the evidence must show")
BUILTIN_SERIES: frozenset[str] = frozenset({f"P{index}" for index in range(10)} | {"CAPSTONE"})

BRIEF_TITLE_RE = re.compile(r"^#\s+(?P<code>PJ\d+)\b", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(?P<text>.+?)\s*$", re.MULTILINE)
CHECKLIST_RE = re.compile(r"^\s*[-*+]\s*\[[ xX]\]", re.MULTILINE)
MODULE_ID_RE = re.compile(r"\b(?:P\d+|CAPSTONE)\b")
TABLE_LINE_RE = re.compile(r"^\s*\|")
SEPARATOR_CELL_RE = re.compile(r"^:?-{2,}:?$")
WEIGHT_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
WEIGHT_SUM_TOLERANCE = 0.01


def validate(repo_root: Path) -> list[Issue]:
    """Validate every project brief and the capstone rubric.

    Returns one issue per finding; an empty list means the briefs follow the contract.
    Costs one directory scan of ``projects/`` plus one read of the capstone rubric.
    """
    issues: list[Issue] = []
    issues.extend(_validate_briefs(repo_root))
    issues.extend(_validate_capstone_rubric(repo_root))
    return issues


def _validate_briefs(repo_root: Path) -> list[Issue]:
    """Validate every brief under ``projects/``.

    Returns the issues found across all briefs. Costs one read per Markdown file in the folder.
    """
    issues: list[Issue] = []
    projects_dir = repo_root / "projects"
    if not projects_dir.is_dir():
        return issues
    series = _series_ids(repo_root)
    for path in sorted(projects_dir.rglob("*.md")):
        if not path.is_file():
            continue
        relative = relpath(path, repo_root)
        text = read_text(path)
        if text is None:
            issues.append(Issue("PRJ001", relative, "brief cannot be read as UTF-8 text"))
            continue
        if not BRIEF_TITLE_RE.search(text):
            continue
        try:
            issues.extend(_validate_brief(text, relative, series))
        except Exception as exc:  # noqa: BLE001 - a malformed brief is a finding, not a crash
            issues.append(Issue("PRJ001", relative, f"brief cannot be validated: {exc}"))
    return issues


def _validate_brief(text: str, relative: str, series: frozenset[str]) -> list[Issue]:
    """Validate one brief against the section contract.

    Returns the issues found in the brief. Costs one parse of the document text.
    """
    issues: list[Issue] = []
    order, bodies = _parse_sections(text)
    required = [name.lower() for name in REQUIRED_SECTIONS]

    present = [name for name in order if name in required]
    for section in REQUIRED_SECTIONS:
        if section.lower() not in present:
            issues.append(Issue("PRJ001", relative, f"missing required section '## {section}'"))

    expected = [name for name in required if name in present]
    if present != expected:
        found = ", ".join(present)
        wanted = ", ".join(expected)
        issues.append(
            Issue("PRJ002", relative, f"sections out of order: found {found}, expected {wanted}")
        )

    criteria = bodies.get("acceptance criteria")
    if criteria is not None:
        count = len(CHECKLIST_RE.findall(criteria))
        if count < 5:
            issues.append(
                Issue(
                    "PRJ003",
                    relative,
                    f"'Acceptance criteria' has {count} checklist items, expected at least 5",
                )
            )

    modules = bodies.get("modules exercised")
    if modules is not None:
        for module_id in sorted(set(MODULE_ID_RE.findall(modules))):
            if module_id not in series:
                issues.append(
                    Issue(
                        "PRJ004",
                        relative,
                        f"module id '{module_id}' does not exist in the series",
                    )
                )

    rubric = bodies.get("rubric")
    if rubric is not None:
        issues.extend(_validate_rubric(rubric, relative))
    return issues


def _validate_capstone_rubric(repo_root: Path) -> list[Issue]:
    """Validate the rubric table of the capstone gate.

    Returns the issues found; an absent rubric file is not an issue here. Costs one file read.
    """
    path = repo_root / "curriculum" / "capstone" / "rubric.md"
    if not path.is_file():
        return []
    relative = relpath(path, repo_root)
    text = read_text(path)
    if text is None:
        return [Issue("PRJ001", relative, "capstone rubric cannot be read as UTF-8 text")]
    _, bodies = _parse_sections(text)
    rubric_text = bodies.get("rubric", text)
    return _validate_rubric(rubric_text, relative)


def _validate_rubric(rubric_text: str, relative: str) -> list[Issue]:
    """Validate a rubric section: columns, row count and weights.

    Returns the issues found in the rubric table. Costs one table parse.
    """
    issues: list[Issue] = []
    header, body_rows = _first_table(rubric_text)
    if header is None:
        issues.append(Issue("PRJ007", relative, "the rubric has no markdown table"))
        issues.append(
            Issue("PRJ005", relative, "the rubric table has 0 body rows, expected at least 3")
        )
        return issues

    normalized = [_normalize_cell(cell) for cell in header]
    missing = [column for column in RUBRIC_COLUMNS if _normalize_cell(column) not in normalized]
    if missing:
        issues.append(
            Issue("PRJ007", relative, f"rubric table is missing column(s): {', '.join(missing)}")
        )

    if len(body_rows) < 3:
        issues.append(
            Issue(
                "PRJ005",
                relative,
                f"rubric table has {len(body_rows)} body rows, expected at least 3",
            )
        )
        return issues

    weight_column = _normalize_cell("Weight")
    if weight_column not in normalized:
        return issues

    weight_index = normalized.index(weight_column)
    weights: list[float] = []
    for row in body_rows:
        cell = row[weight_index] if weight_index < len(row) else ""
        value = _parse_weight(cell)
        if value is None:
            issues.append(
                Issue("PRJ006", relative, f"rubric weight {cell!r} is not a number")
            )
            continue
        weights.append(value)

    if len(weights) == len(body_rows):
        total = sum(weights)
        if abs(total - 100) > WEIGHT_SUM_TOLERANCE:
            issues.append(
                Issue("PRJ006", relative, f"rubric weights sum to {total:g}, expected 100")
            )
    return issues


def _parse_sections(text: str) -> tuple[list[str], dict[str, str]]:
    """Return the level-2 headings of a document and their bodies.

    The first element is the heading order, lower-cased; the second maps a heading to the text
    that follows it. Costs one regex scan.
    """
    matches = list(H2_RE.finditer(text))
    order: list[str] = []
    bodies: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        name = match.group("text").strip().strip("#").strip().lower()
        order.append(name)
        bodies.setdefault(name, text[match.end() : end])
    return order, bodies


def _first_table(text: str) -> tuple[list[str] | None, list[list[str]]]:
    """Return the header cells and body rows of the first markdown table in ``text``.

    Returns ``(None, [])`` when the text holds no table. Costs one line scan.
    """
    tables = _tables(text)
    if not tables:
        return None, []
    return tables[0]


def _tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    """Return every markdown table in ``text`` as a header row plus body rows.

    Costs one line scan and one split per table row.
    """
    groups: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if TABLE_LINE_RE.match(line):
            current.append(line)
        elif current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)

    tables: list[tuple[list[str], list[list[str]]]] = []
    for group in groups:
        rows = [_split_row(line) for line in group]
        if len(rows) >= 2 and all(SEPARATOR_CELL_RE.match(cell or "-") for cell in rows[1]):
            tables.append((rows[0], rows[2:]))
        else:
            tables.append((rows[0], rows[1:]))
    return tables


def _split_row(line: str) -> list[str]:
    """Split a markdown table row into trimmed cells.

    Costs one string split per row.
    """
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _normalize_cell(cell: str) -> str:
    """Normalise a table cell for comparison: lower case, single spaces.

    Costs one regex substitution.
    """
    return re.sub(r"\s+", " ", cell.strip().lower())


def _parse_weight(cell: str) -> float | None:
    """Parse a rubric weight cell into a number, or ``None`` when it is not one.

    Accepts ``20``, ``20%`` and ``20 %``. Costs one regex match.
    """
    candidate = cell.strip().replace("%", "").replace(" ", "")
    if not WEIGHT_RE.match(candidate):
        return None
    return float(candidate)


def _series_ids(repo_root: Path) -> frozenset[str]:
    """Return the module ids of the series.

    Reads ``curriculum/curriculum.yaml`` when it is present and parseable, and falls back to the
    built-in list ``P0``-``P9`` plus ``CAPSTONE`` otherwise. Costs one file read.
    """
    path = repo_root / "curriculum" / "curriculum.yaml"
    if not path.is_file():
        return BUILTIN_SERIES
    text = read_text(path)
    if text is None:
        return BUILTIN_SERIES
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        return BUILTIN_SERIES
    ids = _ids_from_yaml(data)
    known = any(identifier.startswith("P") and identifier[1:].isdigit() for identifier in ids)
    if not ids or not known:
        return BUILTIN_SERIES
    return frozenset(ids)


def _ids_from_yaml(data: object) -> set[str]:
    """Collect module ids from a parsed ``curriculum.yaml`` document.

    Accepts a mapping with a ``modules`` key or a top-level sequence of module mappings.
    Returns the ids found, which may be empty. Costs one traversal of the document.
    """
    ids: set[str] = set()
    if isinstance(data, dict):
        for key in ("modules", "curriculum", "series"):
            ids |= _ids_from_container(data.get(key))
        for key in ("capstone", "CAPSTONE"):
            value = data.get(key)
            if isinstance(value, str):
                ids.add(value)
            elif isinstance(value, dict):
                identifier = value.get("id")
                if isinstance(identifier, str):
                    ids.add(identifier)
    elif isinstance(data, list):
        ids |= _ids_from_container(data)
    return ids


def _ids_from_container(value: object) -> set[str]:
    """Collect module ids from a container of modules.

    Handles a list of ids, a list of mappings with an ``id``, and a mapping keyed by id.
    Returns the ids found. Costs one traversal of the container.
    """
    ids: set[str] = set()
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                ids.add(item)
            elif isinstance(item, dict):
                identifier = item.get("id")
                if isinstance(identifier, str):
                    ids.add(identifier)
    elif isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str):
                ids.add(key)
            if isinstance(item, dict):
                identifier = item.get("id")
                if isinstance(identifier, str):
                    ids.add(identifier)
    return ids
