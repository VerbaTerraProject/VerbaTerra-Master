from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple

import pandas as pd

from .types import EngineSpec, SimulationConfig
from . import vsion, cch, nphra

__all__ = ["ENGINE_REGISTRY", "get_engine", "available_engines", "run_engine"]


ENGINE_REGISTRY: Dict[str, EngineSpec] = {
    "vsion": EngineSpec(
        name="vsion",
        description="Adaptive civilization simulator emphasising trade and symbolism interplay.",
        default_config=vsion.DEFAULT_CONFIG,
        simulate=vsion.simulate,
    ),
    "cch": EngineSpec(
        name="cch",
        description="Cultural–Cognitive Heuristic engine focused on ritual diffusion and hierarchy balance.",
        default_config=cch.DEFAULT_CONFIG,
        simulate=cch.simulate,
    ),
    "nphra": EngineSpec(
        name="nphra",
        description="Neuromorphic Φ-Resonance Analyzer capturing oscillatory coherence dynamics.",
        default_config=nphra.DEFAULT_CONFIG,
        simulate=nphra.simulate,
    ),
}


def get_engine(name: str) -> EngineSpec:
    try:
        return ENGINE_REGISTRY[name]
    except KeyError as exc:
        raise KeyError(f"Unknown engine '{name}'. Available: {', '.join(sorted(ENGINE_REGISTRY))}") from exc


def available_engines() -> Iterable[str]:
    return sorted(ENGINE_REGISTRY)


def run_engine(
    name: str, config: Dict[str, Any] | None = None, seed: int | None = None
) -> Tuple[pd.DataFrame, SimulationConfig]:
    spec = get_engine(name)
    df, engine_config = spec.simulate(config, seed=seed)
    used_config = dict(spec.default_config)
    if engine_config:
        used_config.update(engine_config)
    if config:
        used_config.update(config)
    used_config["n"] = int(used_config.get("n", spec.default_config.get("n", 200)))
    return df, used_config
