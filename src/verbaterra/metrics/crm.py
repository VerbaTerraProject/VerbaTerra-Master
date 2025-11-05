from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..dataio.schema import DATASET_SCHEMA, validate_frame


@dataclass(frozen=True)
class CRMConfig:
    trade_weight: float = 0.5
    symbolism_weight: float = 0.5
    hierarchy_penalty_weight: float = 0.2
    ritual_stability_weight: float = 0.2


def _safe_norm(series: pd.Series) -> pd.Series:
    series = series.astype(float)
    rng = series.max() - series.min()
    if np.isclose(rng, 0):
        return pd.Series(np.zeros(len(series)), index=series.index, dtype=float)
    return (series - series.min()) / rng


def compute_crm(df: pd.DataFrame, config: CRMConfig | None = None) -> pd.Series:
    config = config or CRMConfig()
    validate_frame(df, DATASET_SCHEMA)

    trade_component = config.trade_weight * _safe_norm(df["trade"])
    symbolism_component = config.symbolism_weight * _safe_norm(df["symbolism"])
    trade_sym = trade_component + symbolism_component
    hierarchy_penalty = 1 - _safe_norm((df["hierarchy"] - df["hierarchy"].mean()).abs())
    ritual_rolling = df["ritual"].rolling(3, min_periods=1).mean()
    ritual_stability = 1 - _safe_norm((df["ritual"] - ritual_rolling).abs())
    base = (
        0.6 * trade_sym
        + config.hierarchy_penalty_weight * hierarchy_penalty
        + config.ritual_stability_weight * ritual_stability
    )
    return base.clip(0, 1)


__all__ = ["CRMConfig", "compute_crm"]
