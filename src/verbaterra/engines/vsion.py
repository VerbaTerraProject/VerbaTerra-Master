from __future__ import annotations
import numpy as np
import pandas as pd

def simulate_block(n: int = 200, seed: int | None = None) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    ritual = rng.normal(50, 10, n)
    trade = rng.normal(50, 15, n)
    symbolism = rng.normal(50, 12, n)
    hierarchy = rng.normal(50, 18, n)
    noise = rng.normal(0, 5, n)
    lexical_diversity = 0.3*trade + 0.25*symbolism - 0.1*hierarchy + 0.2*ritual + noise + 20
    syntax_complexity = 0.2*ritual + 0.2*hierarchy + 0.15*trade + 0.15*symbolism + noise + 15

    return pd.DataFrame({
        "ritual": ritual,
        "trade": trade,
        "symbolism": symbolism,
        "hierarchy": hierarchy,
        "lexical_diversity": lexical_diversity,
        "syntax_complexity": syntax_complexity,
    })
