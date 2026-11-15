"""Run every validator over a repository and report the findings.

Usage::

    python tools/validators/run_all.py [--repo PATH] [--json]

Exit code 0 when every validator passes, 1 when any validator reports an issue.
The runner never raises on a broken repository: a validator that crashes is reported as
an issue against that validator, so one bad rule cannot hide the others.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.validators.common import Issue, Result  # noqa: E402

VALIDATOR_PREFIX = "validate_"


def discover() -> list[str]:
    """Return the validator module names in a stable order."""
    package_dir = Path(__file__).resolve().parent
    names = [
        path.stem
        for path in sorted(package_dir.glob(f"{VALIDATOR_PREFIX}*.py"))
    ]
    return names


def run_all(repo_root: Path) -> list[Result]:
    """Run every discovered validator against ``repo_root``."""
    results: list[Result] = []
    for name in discover():
        try:
            module = importlib.import_module(f"tools.validators.{name}")
            issues = list(module.validate(repo_root))
        except Exception:  # noqa: BLE001 - a crashing validator must not hide the others
            detail = traceback.format_exc(limit=3).strip().splitlines()[-1]
            issues = [
                Issue("VAL000", f"tools/validators/{name}.py", f"validator crashed: {detail}")
            ]
        results.append(Result(name=name, issues=issues))
    return results


def main(argv: list[str] | None = None) -> int:
    """Parse the arguments, run the validators and report. Returns the exit code."""
    parser = argparse.ArgumentParser(description="Run the polymath repository validators.")
    parser.add_argument("--repo", default=str(REPO_ROOT), help="repository root to validate")
    parser.add_argument(
        "--json", action="store_true", help="print a JSON report instead of a table"
    )
    args = parser.parse_args(argv)

    repo_root = Path(args.repo).resolve()
    results = run_all(repo_root)
    failed = [result for result in results if not result.ok]

    if args.json:
        payload = {
            "repo": str(repo_root),
            "ok": not failed,
            "validators": [result.to_dict() for result in results],
        }
        print(json.dumps(payload, indent=2))
        return 1 if failed else 0

    for result in results:
        status = "PASS" if result.ok else "FAIL"
        print(f"[{status}] {result.name} ({len(result.issues)} issue(s))")
        for issue in result.issues:
            print(f"    {issue.code} {issue.path}: {issue.message}")

    total = sum(len(result.issues) for result in results)
    print(f"\n{len(results)} validator(s), {total} issue(s).")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
