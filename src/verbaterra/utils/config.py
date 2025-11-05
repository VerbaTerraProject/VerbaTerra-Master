from __future__ import annotations

import ast
import importlib.util
import json
from os import PathLike
from pathlib import Path
from typing import Any, Dict

yaml_spec = importlib.util.find_spec("yaml")
if yaml_spec is not None:  # pragma: no branch - deterministic probe
    import yaml  # type: ignore[import-untyped]
else:  # pragma: no cover - exercised via fallback tests
    yaml = None  # type: ignore[assignment]


def _parse_simple_yaml(text: str) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"Unsupported YAML line: {raw_line!r}")
        key, value_text = line.split(":", 1)
        key = key.strip()
        value_text = value_text.strip()
        if not value_text:
            result[key] = None
            continue
        try:
            result[key] = ast.literal_eval(value_text)
        except (ValueError, SyntaxError):
            lowered = value_text.lower()
            if lowered in {"true", "false"}:
                result[key] = lowered == "true"
            else:
                result[key] = value_text
    return result


Pathish = str | Path | PathLike[str]


def load_yaml(path: Pathish) -> Dict[str, Any]:
    path_obj = Path(path)
    text = path_obj.read_text(encoding="utf-8")
    if yaml is not None:
        loaded = yaml.safe_load(text) or {}
        return dict(loaded)
    return _parse_simple_yaml(text)


def dump_yaml(data: Dict[str, Any], path: Pathish) -> None:
    path_obj = Path(path)
    if yaml is not None:
        with path_obj.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(data, handle, sort_keys=False)
        return

    lines = [f"{key}: {json.dumps(value)}" for key, value in data.items()]
    path_obj.write_text("\n".join(lines) + "\n", encoding="utf-8")
