"""Repo-root pytest configuration.

Putting the repository root on ``sys.path`` here makes ``from tools.validators import ...``
work in every test file without an install step, and keeps the test suite runnable in a
fresh clone with nothing but ``pip install -e ".[dev]"``.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
