"""Validators for the AI Engineer Polymath curriculum repository.

Every validator module exposes the same entry point::

    validate(repo_root: Path) -> list[Issue]

The runner in ``run_all.py`` discovers those modules and aggregates their findings.
"""

from __future__ import annotations

from tools.validators.common import Issue, Result

__all__ = ["Issue", "Result"]
