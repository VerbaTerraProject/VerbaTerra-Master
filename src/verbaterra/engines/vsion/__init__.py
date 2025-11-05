from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .simulator import DEFAULT_CONFIG, simulate

__all__ = ["DEFAULT_CONFIG", "simulate", "load_default_config", "default_config_path"]


def load_default_config() -> Dict[str, Any]:
    """Return a copy of the packaged default configuration."""
    return dict(DEFAULT_CONFIG)


def default_config_path() -> Path:
    return Path(__file__).resolve().parent / "configs" / "default.yaml"
