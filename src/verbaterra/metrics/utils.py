from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

MANDATORY_COLUMNS = [
    "ritual",
    "trade",
    "symbolism",
    "hierarchy",
    "lexical_diversity",
    "syntax_complexity",
]


def require_columns(df: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = [c for c in columns if c not in df]
    if missing:
        raise KeyError(f"Dataset missing required columns: {', '.join(missing)}")


def safe_norm(series: pd.Series) -> pd.Series:
    arr = series.astype(float)
    rng = arr.max() - arr.min()
    if np.isclose(rng, 0.0):
        return pd.Series(np.zeros(len(arr)), index=arr.index)
    return (arr - arr.min()) / rng
