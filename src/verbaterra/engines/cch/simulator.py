from __future__ import annotations

from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd

DEFAULT_CONFIG: Dict[str, Any] = {
    "n": 180,
    "ritual_core": 60.0,
    "ritual_variance": 8.5,
    "hierarchy_center": 52.0,
    "hierarchy_variance": 10.5,
    "diffusion_rate": 0.18,
    "trade_base": 42.0,
    "symbolism_base": 57.0,
}


def _merge_config(config: Dict[str, Any] | None) -> Dict[str, Any]:
    merged = dict(DEFAULT_CONFIG)
    if config:
        merged.update(config)
    merged["n"] = int(merged.get("n", DEFAULT_CONFIG["n"]))
    return merged


def simulate(config: Dict[str, Any] | None = None, seed: int | None = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    cfg = _merge_config(config)
    rng = np.random.default_rng(seed)
    n = cfg["n"]

    ritual = rng.normal(cfg["ritual_core"], cfg["ritual_variance"], n)
    hierarchy = rng.normal(cfg["hierarchy_center"], cfg["hierarchy_variance"], n)
    diffusion = rng.beta(2.5, 3.0, n) * cfg["diffusion_rate"]
    trade = cfg["trade_base"] + diffusion * 120 + rng.normal(0.0, 6.0, n)
    symbolism = cfg["symbolism_base"] + diffusion * 80 + rng.normal(0.0, 5.5, n)

    ritual_coherence = 1 - np.abs(ritual - ritual.mean()) / (ritual.std() + 1e-6)
    hierarchy_balance = 1 - np.abs(hierarchy - hierarchy.mean()) / (hierarchy.std() + 1e-6)
    collective_memory = 0.6 * ritual_coherence + 0.4 * hierarchy_balance

    noise = rng.normal(0.0, 3.5, n)
    lexical_diversity = 0.25 * trade + 0.35 * symbolism + 0.15 * diffusion * 100 + noise + 16
    syntax_complexity = 0.3 * ritual + 0.2 * hierarchy + 0.1 * diffusion * 80 + noise + 13

    df = pd.DataFrame(
        {
            "ritual": ritual,
            "trade": trade,
            "symbolism": symbolism,
            "hierarchy": hierarchy,
            "lexical_diversity": lexical_diversity,
            "syntax_complexity": syntax_complexity,
            "collective_memory": collective_memory,
            "diffusion_rate": diffusion,
        }
    )
    return df, cfg
