from __future__ import annotations

import pandas as pd

from .utils import require_columns, safe_norm


CRM_COLUMNS = ["ritual", "trade", "symbolism", "hierarchy"]


def crm(df: pd.DataFrame) -> pd.Series:
    """Compute the Cultural Resilience Metric (CRM)."""

    require_columns(df, CRM_COLUMNS)
    trade_sym = 0.5 * safe_norm(df["trade"]) + 0.5 * safe_norm(df["symbolism"])
    hierarchy_penalty = 1 - safe_norm((df["hierarchy"] - df["hierarchy"].mean()).abs())
    ritual_stability = 1 - safe_norm((df["ritual"] - df["ritual"].rolling(3, min_periods=1).mean()).abs())
    base = 0.6 * trade_sym + 0.2 * hierarchy_penalty + 0.2 * ritual_stability
    return base.clip(0, 1)
