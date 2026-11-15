"""Create the curriculum issues from the acceptance criteria in the module notes.

One issue per acceptance criterion. The chain is sequential: issue *n* is blocked by issue
*n-1* within a module, and the first issue of a module is blocked by the last issue of the
module before it.

Usage::

    python tools/create_issues.py --dry-run
    python tools/create_issues.py --repo aswathas/ai-engineer-polymath

The script is idempotent by title: an issue that already exists is reused, never duplicated.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import yaml  # noqa: E402

from tools.validators.common import read_text  # noqa: E402

CRITERION_RE = re.compile(r"^\s*[-*]\s*(?:\[[ xX]?\]\s*)?(?P<text>.+?)\s*$")


def module_tasks(curriculum_yaml: Path) -> list[dict[str, object]]:
    """Return one task list per module, in series order.

    Each task carries the module id, the module title, the gate id, the criterion text and
    the position of the criterion inside the module.
    """
    data = yaml.safe_load(curriculum_yaml.read_text(encoding="utf-8")) or {}
    modules = data.get("modules", [])
    tasks: list[dict[str, object]] = []
    for module in modules:
        note = curriculum_yaml.parent / str(module["dir"]) / "module-note.md"
        text = read_text(note)
        if text is None:
            continue
        criteria = _acceptance_criteria(text)
        for index, criterion in enumerate(criteria, start=1):
            tasks.append(
                {
                    "id": module["id"],
                    "title": module["title"],
                    "gate": module["gate"],
                    "dir": module["dir"],
                    "index": index,
                    "total": len(criteria),
                    "criterion": criterion,
                    "title_line": f"{module['id']}.{index} - {criterion}",
                }
            )
    return tasks


def _acceptance_criteria(text: str) -> list[str]:
    """Return the checklist items under the '## Acceptance criteria' section."""
    match = re.search(r"^##\s+Acceptance criteria\s*$", text, re.MULTILINE)
    if not match:
        return []
    rest = text[match.end() :]
    next_heading = re.search(r"^##\s+", rest, re.MULTILINE)
    section = rest[: next_heading.start()] if next_heading else rest
    criteria: list[str] = []
    for line in section.splitlines():
        item = CRITERION_RE.match(line)
        if item:
            criteria.append(item.group("text"))
    return criteria


def issue_body(task: dict[str, object]) -> str:
    """Return the body of the issue for one acceptance criterion."""
    return (
        f"## Module\n{task['id']} - {task['title']} (gate {task['gate']})\n\n"
        f"## Task\nCriterion {task['index']} of {task['total']} in {task['dir']}/module-note.md\n\n"
        f"## Done when\n- [ ] {task['criterion']}\n\n"
        "## Notes\n- The learner writes the code. The agent never does.\n"
    )


def gh(args: list[str]) -> str:
    """Run a gh command and return its stdout."""
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def main(argv: list[str] | None = None) -> int:
    """Parse the arguments and create the issues. Returns the exit code."""
    parser = argparse.ArgumentParser(
        description="Create the curriculum issues from the module notes."
    )
    parser.add_argument("--repo", default="aswathas/ai-engineer-polymath", help="target repository")
    parser.add_argument("--dry-run", action="store_true", help="print the plan instead of creating")
    args = parser.parse_args(argv)

    curriculum_yaml = REPO_ROOT / "curriculum" / "curriculum.yaml"
    if not curriculum_yaml.is_file():
        print(f"curriculum.yaml not found at {curriculum_yaml}", file=sys.stderr)
        return 1

    tasks = module_tasks(curriculum_yaml)
    if not tasks:
        print("no acceptance criteria found in the module notes", file=sys.stderr)
        return 1

    if args.dry_run:
        print(
            json.dumps(
                [{"title": t["title_line"], "body": issue_body(t)} for t in tasks], indent=2
            )
        )
        print(f"{len(tasks)} issue(s) planned", file=sys.stderr)
        return 0

    existing = json.loads(
        gh(
            [
                "issue",
                "list",
                "--repo",
                args.repo,
                "--state",
                "all",
                "--limit",
                "200",
                "--json",
                "number,title",
            ]
        )
    )
    by_title = {issue["title"]: issue["number"] for issue in existing}

    previous: int | None = None
    for task in tasks:
        title = str(task["title_line"])
        if title in by_title:
            previous = by_title[title]
            print(f"#{previous} {title} (exists)")
            continue
        args_list = [
            "issue",
            "create",
            "--repo",
            args.repo,
            "--title",
            title,
            "--body",
            issue_body(task),
        ]
        if previous is not None:
            args_list += ["--blocked-by", str(previous)]
        url = gh(args_list)
        previous = int(url.rsplit("/", 1)[1])
        print(f"#{previous} {title}")

    print(f"total: {len(tasks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
