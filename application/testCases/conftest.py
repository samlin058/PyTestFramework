from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

pytest_plugins = [
    "service.execution.fixtures.api_fixtures",
    "service.execution.fixtures.ui_fixtures",
    "service.execution.fixtures.common_fixtures",
    "service.execution.hooks.pytest_hooks",
]
