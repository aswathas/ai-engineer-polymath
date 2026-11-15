"""Tests for the validator runner (``tools/validators/run_all.py``)."""

from __future__ import annotations

import json
from pathlib import Path

from tools.validators.run_all import discover, main, run_all


def test_discovery_finds_the_validators() -> None:
    names = discover()
    assert "validate_skeleton" in names
    assert "validate_links" in names
    assert "validate_records" in names
    assert all(name.startswith("validate_") for name in names)


def test_run_all_returns_one_result_per_validator(tmp_path: Path) -> None:
    results = run_all(tmp_path)
    assert len(results) == len(discover())


def test_json_output_is_machine_readable(tmp_path: Path, capsys) -> None:
    exit_code = main(["--repo", str(tmp_path), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert exit_code in (0, 1)
    assert payload["ok"] is (exit_code == 0)
    assert len(payload["validators"]) == len(discover())


def test_empty_repository_reports_issues(tmp_path: Path, capsys) -> None:
    exit_code = main(["--repo", str(tmp_path)])
    out = capsys.readouterr().out
    assert exit_code == 1
    assert "issue(s)" in out
