from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _ensure_project_on_path() -> None:
    project_root = Path(__file__).resolve().parents[2]
    src_dir = project_root / "src"
    if importlib.util.find_spec("verbaterra") is None and src_dir.exists():
        sys.path.insert(0, str(src_dir))


def main() -> None:  # pragma: no cover - thin wrapper
    _ensure_project_on_path()
    from verbaterra.examples.run_vsion import main as run_main

    run_main()


if __name__ == "__main__":  # pragma: no cover
    main()
