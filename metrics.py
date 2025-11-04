from __future__ import annotations
import pandas as pd
import numpy as np

def _safe_norm(s: pd.Series) -> pd.Series:
    s = s.astype(float)
    rng = s.max() - s.min()
    if rng == 0:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - s.min()) / rng

def nlis(df: pd.DataFrame) -> pd.Series:
    """Neuro‑Linguistic Integration Score (demo).
    Expects: lexical_diversity, syntax_complexity, ritual, trade, symbolism, hierarchy.
    """
    required = ["lexical_diversity", "syntax_complexity", "ritual", "trade", "symbolism", "hierarchy"]
    for c in required:
        if c not in df:
            raise KeyError(f"Missing column: {c}")
    ling = 0.6 * _safe_norm(df["lexical_diversity"]) + 0.4 * _safe_norm(df["syntax_complexity"])
    cult = 0.25 * _safe_norm(df["ritual"]) + 0.25 * _safe_norm(df["trade"]) + 0.25 * _safe_norm(df["symbolism"]) + 0.25 * _safe_norm(df["hierarchy"])
    return 0.7 * ling + 0.3 * cult

def crm(df: pd.DataFrame) -> pd.Series:
    """Cultural Resilience Metric (demo).
    Expects: ritual, trade, symbolism, hierarchy.
    """
    for c in ["ritual", "trade", "symbolism", "hierarchy"]:
        if c not in df:
            raise KeyError(f"Missing column: {c}")
    trade_sym = 0.5 * _safe_norm(df["trade"]) + 0.5 * _safe_norm(df["symbolism"])
    hierarchy_penalty = 1 - _safe_norm((df["hierarchy"] - df["hierarchy"].mean()).abs())
    ritual_stab = 1 - _safe_norm((df["ritual"] - df["ritual"].rolling(3, min_periods=1).mean()).abs())
    base = 0.6 * trade_sym + 0.2 * hierarchy_penalty + 0.2 * ritual_stab
    return base.clip(0, 1)
