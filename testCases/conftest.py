from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

pytest_plugins = [
    "execution.fixtures.api_fixtures",
    "execution.fixtures.ui_fixtures",
    "execution.fixtures.common_fixtures",
    "execution.hooks.pytest_hooks",
]
