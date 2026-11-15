#!/usr/bin/env python3
"""Print the curriculum prerequisite graph.

Reads ``curriculum/curriculum.yaml`` from a repository root and reports the modules in
prerequisite order, the direct prerequisites of one module, or a summary of the graph.
PyYAML is the only dependency.

    python skills/curriculum-graph/scripts/graph.py --repo . --order
    python skills/curriculum-graph/scripts/graph.py --repo . --module P3

The module file is read leniently: the module list may live under a ``modules`` key or
be the top-level value, each entry may be a mapping or a bare id, and the common key
spellings for id, title, prerequisites and hours are all accepted.

Exit codes: 0 on success, 1 when the curriculum file is missing or unparseable, when
the requested module is unknown, or when the graph contains a cycle.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

CURRICULUM_RELPATH = ("curriculum", "curriculum.yaml")

ID_KEYS: tuple[str, ...] = ("id", "module_id", "code", "key")
TITLE_KEYS: tuple[str, ...] = ("title", "name", "label")
PREREQ_KEYS: tuple[str, ...] = (
    "prerequisites",
    "prereqs",
    "prereq",
    "requires",
    "depends_on",
    "needs",
)
HOURS_KEYS: tuple[str, ...] = ("hours", "estimated_hours", "duration_hours")


@dataclass
class Module:
    """One module of the curriculum.

    ``id`` is the short handle such as ``P3``, ``title`` the human name, ``prereqs``
    the ids of the modules that come first, and ``hours`` the estimated effort.
    """

    id: str
    title: str = ""
    prereqs: list[str] = field(default_factory=list)
    hours: int | float | None = None


def load_modules(path: Path) -> list[Module]:
    """Read the module list from a curriculum file.

    Returns the modules in the order they appear in the file. Raises ``OSError`` when
    the file cannot be read and ``ValueError`` when it cannot be parsed. The cost is
    one read of the file and one pass over the module list.
    """
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    entries = extract_entries(data)
    modules: list[Module] = []
    for index, entry in enumerate(entries):
        modules.append(build_module(index, entry))
    return modules


def extract_entries(data: object) -> list[object]:
    """Return the raw module entries from a parsed curriculum file.

    Accepts a mapping with a ``modules`` key, a mapping of module id to mapping, or a
    bare list. Returns an empty list when nothing recognisable is present. The cost is
    constant.
    """
    if isinstance(data, dict):
        raw = data.get("modules")
        if raw is None:
            raw = data.get("curriculum")
        if raw is None:
            raw = data
        if isinstance(raw, list):
            return list(raw)
        if isinstance(raw, dict):
            entries: list[object] = []
            for key, value in raw.items():
                if isinstance(value, dict):
                    merged = dict(value)
                    merged.setdefault("id", key)
                    entries.append(merged)
                else:
                    entries.append({"id": key, "title": str(value)})
            return entries
        return []
    if isinstance(data, list):
        return list(data)
    return []


def build_module(index: int, entry: object) -> Module:
    """Turn one raw entry into a :class:`Module`.

    A bare string becomes a module with that id. A mapping is read leniently: the
    first key that is present wins. The cost is constant.
    """
    if isinstance(entry, str):
        return Module(id=entry, title=entry)
    if not isinstance(entry, dict):
        return Module(id=f"M{index}", title=str(entry))

    module_id = ""
    for key in ID_KEYS:
        value = entry.get(key)
        if isinstance(value, str) and value:
            module_id = value
            break
    if not module_id:
        module_id = f"M{index}"

    title = module_id
    for key in TITLE_KEYS:
        value = entry.get(key)
        if isinstance(value, str) and value:
            title = value
            break

    prereqs: list[str] = []
    for key in PREREQ_KEYS:
        if key in entry:
            raw = entry.get(key)
            if isinstance(raw, str):
                prereqs = [part.strip() for part in raw.split(",") if part.strip()]
            elif isinstance(raw, list):
                prereqs = [str(part).strip() for part in raw if str(part).strip()]
            break

    hours: int | float | None = None
    for key in HOURS_KEYS:
        value = entry.get(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, int) or isinstance(value, float):
            hours = value
            break

    return Module(id=module_id, title=title, prereqs=prereqs, hours=hours)


def prereq_map(modules: list[Module]) -> dict[str, list[str]]:
    """Return the prerequisite edges of the graph, keyed by module id.

    Only prerequisites that name a known module are kept, so a typo cannot break the
    ordering. The cost is one pass over the modules.
    """
    known = {module.id for module in modules}
    graph: dict[str, list[str]] = {}
    for module in modules:
        graph[module.id] = [prereq for prereq in module.prereqs if prereq in known]
    return graph


def unknown_prereqs(modules: list[Module]) -> dict[str, list[str]]:
    """Return the prerequisites that name no known module, keyed by module id.

    Returns an empty mapping when every prerequisite resolves. The cost is one pass
    over the modules.
    """
    known = {module.id for module in modules}
    missing: dict[str, list[str]] = {}
    for module in modules:
        unknown = [prereq for prereq in module.prereqs if prereq not in known]
        if unknown:
            missing[module.id] = unknown
    return missing


def topological_order(modules: list[Module], graph: dict[str, list[str]]) -> list[str]:
    """Return the modules in prerequisite order.

    Uses Kahn's algorithm with a stable tie-break, so modules that share a
    prerequisite keep the order they have in the file. A module caught in a cycle is
    left out. The cost is O(V + E).
    """
    remaining = {module.id: set(graph.get(module.id, [])) for module in modules}
    order: list[str] = []
    placed: set[str] = set()

    while True:
        ready = [
            module.id
            for module in modules
            if module.id not in placed and not (remaining[module.id] - placed)
        ]
        if not ready:
            break
        for module_id in ready:
            placed.add(module_id)
            order.append(module_id)

    return order


def find_cycle(modules: list[Module], graph: dict[str, list[str]]) -> list[str]:
    """Return one cycle in the graph as a list of module ids.

    The last id repeats the first, so the cycle reads as a path. Returns an empty list
    when the graph is acyclic. The cost is O(V + E).
    """
    color: dict[str, int] = {module.id: 0 for module in modules}
    stack: list[str] = []

    def visit(module_id: str) -> list[str]:
        color[module_id] = 1
        stack.append(module_id)
        for prereq in graph.get(module_id, []):
            if color.get(prereq, 0) == 1:
                start = stack.index(prereq)
                return stack[start:] + [prereq]
            if color.get(prereq, 0) == 0:
                found = visit(prereq)
                if found:
                    return found
        stack.pop()
        color[module_id] = 2
        return []

    for module in modules:
        if color.get(module.id, 0) == 0:
            found = visit(module.id)
            if found:
                return found
    return []


def module_titles(modules: list[Module]) -> dict[str, str]:
    """Return a mapping from module id to title. The cost is one pass."""
    return {module.id: module.title for module in modules}


def render_order(modules: list[Module], order: list[str]) -> str:
    """Render the module order as one line per module. The cost is O(V)."""
    titles = module_titles(modules)
    return "\n".join(f"{module_id}  {titles.get(module_id, module_id)}" for module_id in order)


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the graph tool. The cost is constant."""
    parser = argparse.ArgumentParser(
        prog="graph.py",
        description="Print the curriculum prerequisite graph and check it for cycles.",
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="repository root (default: the current directory)",
    )
    parser.add_argument(
        "--order",
        action="store_true",
        help="print the modules in prerequisite order",
    )
    parser.add_argument("--module", help="print the direct prerequisites of one module")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the graph tool against a repository.

    Returns 0 on success and 1 when the curriculum file is missing or unparseable,
    when the requested module is unknown, or when the graph contains a cycle. The cost
    is one read of the curriculum file plus a few linear passes over the modules.
    """
    args = build_parser().parse_args(argv)
    repo_root = Path(args.repo).expanduser().resolve()
    curriculum_path = repo_root.joinpath(*CURRICULUM_RELPATH)

    if not curriculum_path.is_file():
        print(
            f"No curriculum file at {curriculum_path}. "
            "The curriculum has not been created yet, so there is no graph to print.",
            file=sys.stderr,
        )
        return 1

    try:
        modules = load_modules(curriculum_path)
    except (OSError, yaml.YAMLError) as exc:
        print(f"Cannot read {curriculum_path}: {exc}", file=sys.stderr)
        return 1

    if not modules:
        print(f"{curriculum_path} lists no modules.", file=sys.stderr)
        return 1

    graph = prereq_map(modules)
    order = topological_order(modules, graph)
    cycle = find_cycle(modules, graph)

    if cycle:
        print("CYCLE detected: " + " -> ".join(cycle), file=sys.stderr)
        return 1

    titles = module_titles(modules)

    if args.module:
        wanted = args.module.strip()
        match = next(
            (module for module in modules if module.id.lower() == wanted.lower()),
            None,
        )
        if match is None:
            print(
                f"Unknown module '{wanted}'. Known modules: "
                + ", ".join(module.id for module in modules),
                file=sys.stderr,
            )
            return 1
        direct = graph.get(match.id, [])
        if args.json:
            print(
                json.dumps(
                    {
                        "module": match.id,
                        "title": match.title,
                        "prerequisites": direct,
                    },
                    indent=2,
                )
            )
        else:
            print(f"{match.id}  {match.title}")
            print("Direct prerequisites:")
            if direct:
                for prereq in direct:
                    print(f"  {prereq}  {titles.get(prereq, prereq)}")
            else:
                print("  (none)")
        return 0

    if args.order:
        if args.json:
            print(json.dumps({"order": order, "titles": titles}, indent=2))
        else:
            print(render_order(modules, order))
            print(f"OK: {len(order)} module(s) in prerequisite order, no cycle.")
        return 0

    for module_id, missing in unknown_prereqs(modules).items():
        print(
            f"Warning: {module_id} names an unknown prerequisite: " + ", ".join(missing),
            file=sys.stderr,
        )

    if args.json:
        print(
            json.dumps(
                {
                    "modules": [
                        {
                            "id": module.id,
                            "title": module.title,
                            "prerequisites": graph.get(module.id, []),
                            "hours": module.hours,
                        }
                        for module in modules
                    ],
                    "order": order,
                },
                indent=2,
            )
        )
    else:
        edges = sum(len(value) for value in graph.values())
        print(f"{len(modules)} module(s), {edges} prerequisite edge(s)")
        for module in modules:
            direct = graph.get(module.id, [])
            joined = ", ".join(direct) if direct else "(none)"
            print(f"{module.id}  {module.title}  <- {joined}")
        print("Order: " + " -> ".join(order))
    return 0


if __name__ == "__main__":
    sys.exit(main())
