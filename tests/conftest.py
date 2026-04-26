"""Pytest config — makes .github/scripts importable for tests."""

import sys
from pathlib import Path

# Add .github/scripts to sys.path so tests can `import build_namespace_landings`.
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / ".github" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
