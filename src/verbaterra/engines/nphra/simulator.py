from __future__ import annotations

from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd

DEFAULT_CONFIG: Dict[str, Any] = {
    "n": 160,
    "oscillation_scale": 0.35,
    "resonance_bias": 0.5,
    "trade_level": 46.0,
    "symbolism_level": 60.0,
    "hierarchy_level": 44.0,
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

    time = np.linspace(0, 4 * np.pi, n)
    oscillation = np.sin(time) * cfg["oscillation_scale"] + rng.normal(0.0, 0.05, n)
    coherence = np.cos(time / 2) * 0.4 + cfg["resonance_bias"]

    ritual = 55 + 12 * coherence + rng.normal(0.0, 4.5, n)
    trade = cfg["trade_level"] + 8 * oscillation + rng.normal(0.0, 3.5, n)
    symbolism = cfg["symbolism_level"] + 15 * coherence + rng.normal(0.0, 4.0, n)
    hierarchy = cfg["hierarchy_level"] + 9 * np.cos(time / 3) + rng.normal(0.0, 5.0, n)

    neuro_coherence = coherence + oscillation * 0.3
    lexical_diversity = 0.28 * trade + 0.32 * symbolism - 0.1 * hierarchy + 19 + neuro_coherence * 8
    syntax_complexity = 0.22 * ritual + 0.2 * hierarchy + neuro_coherence * 6 + 12

    df = pd.DataFrame(
        {
            "ritual": ritual,
            "trade": trade,
            "symbolism": symbolism,
            "hierarchy": hierarchy,
            "lexical_diversity": lexical_diversity,
            "syntax_complexity": syntax_complexity,
            "resonance_wave": oscillation,
            "neuro_coherence": neuro_coherence,
        }
    )
    return df, cfg
