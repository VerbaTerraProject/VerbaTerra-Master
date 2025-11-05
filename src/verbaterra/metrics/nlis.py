from __future__ import annotations

import pandas as pd

from .utils import MANDATORY_COLUMNS, require_columns, safe_norm


def nlis(df: pd.DataFrame) -> pd.Series:
    """Compute the Neuro-Linguistic Integration Score (NLIS)."""

    require_columns(df, MANDATORY_COLUMNS)
    ling = 0.6 * safe_norm(df["lexical_diversity"]) + 0.4 * safe_norm(df["syntax_complexity"])
    cult = (
        0.25 * safe_norm(df["ritual"])
        + 0.25 * safe_norm(df["trade"])
        + 0.25 * safe_norm(df["symbolism"])
        + 0.25 * safe_norm(df["hierarchy"])
    )
    return 0.7 * ling + 0.3 * cult
