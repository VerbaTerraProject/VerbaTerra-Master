from __future__ import annotations

from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd

DEFAULT_CONFIG: Dict[str, Any] = {
    "n": 240,
    "ritual_mean": 52.0,
    "ritual_std": 9.0,
    "trade_mean": 48.0,
    "trade_std": 14.0,
    "symbolism_mean": 55.0,
    "symbolism_std": 11.0,
    "hierarchy_mean": 47.0,
    "hierarchy_std": 16.0,
    "lexical_bias": 18.0,
    "syntax_bias": 14.0,
}


def _resolve_config(config: Dict[str, Any] | None) -> Dict[str, Any]:
    merged = dict(DEFAULT_CONFIG)
    if config:
        merged.update(config)
    merged["n"] = int(merged.get("n", DEFAULT_CONFIG["n"]))
    return merged


def simulate(config: Dict[str, Any] | None = None, seed: int | None = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    cfg = _resolve_config(config)
    rng = np.random.default_rng(seed)
    n = cfg["n"]

    ritual = rng.normal(cfg["ritual_mean"], cfg["ritual_std"], n)
    trade = rng.normal(cfg["trade_mean"], cfg["trade_std"], n)
    symbolism = rng.normal(cfg["symbolism_mean"], cfg["symbolism_std"], n)
    hierarchy = rng.normal(cfg["hierarchy_mean"], cfg["hierarchy_std"], n)

    adaptive_pressure = 0.4 * ritual + 0.3 * trade + 0.2 * symbolism - 0.2 * hierarchy
    integrative_noise = rng.normal(0.0, 4.0, n)

    lexical_diversity = (
        0.35 * trade
        + 0.25 * symbolism
        - 0.12 * hierarchy
        + 0.22 * ritual
        + cfg["lexical_bias"]
        + integrative_noise
    )
    syntax_complexity = (
        0.24 * ritual
        + 0.18 * hierarchy
        + 0.18 * trade
        + 0.16 * symbolism
        + cfg["syntax_bias"]
        + integrative_noise
    )

    df = pd.DataFrame(
        {
            "ritual": ritual,
            "trade": trade,
            "symbolism": symbolism,
            "hierarchy": hierarchy,
            "lexical_diversity": lexical_diversity,
            "syntax_complexity": syntax_complexity,
            "adaptive_pressure": adaptive_pressure,
        }
    )
    return df, cfg
