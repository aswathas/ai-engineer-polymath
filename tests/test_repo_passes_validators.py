"""The repository must pass its own validators.

This is the self-hosting test: it runs every validator against the real tree, so a change
that breaks a contract fails the test-suite rather than waiting for a human to notice.
"""

from __future__ import annotations

from pathlib import Path

from tools.validators.run_all import run_all

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_repository_passes_every_validator() -> None:
    """Every validator reports zero issues against the repository itself."""
    results = run_all(REPO_ROOT)
    failures = [f"{result.name}: {issue}" for result in results for issue in result.issues]
    assert not failures, "\n".join(failures)
