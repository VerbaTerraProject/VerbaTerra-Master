from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd

from ..dataio.schema import DATASET_SCHEMA, validate_frame


@dataclass(frozen=True)
class NLISConfig:
    """Weights used to compute the Neuro-Linguistic Integration Score."""

    lexical_weight: float = 0.7
    cultural_weight: float = 0.3
    lexical_diversity_weight: float = 0.6
    syntax_complexity_weight: float = 0.4
    ritual_weight: float = 0.25
    trade_weight: float = 0.25
    symbolism_weight: float = 0.25
    hierarchy_weight: float = 0.25

    def cultural_weights(self) -> tuple[float, float, float, float]:
        return (
            self.ritual_weight,
            self.trade_weight,
            self.symbolism_weight,
            self.hierarchy_weight,
        )


def _safe_norm(series: pd.Series) -> pd.Series:
    series = series.astype(float)
    rng = series.max() - series.min()
    if np.isclose(rng, 0):
        return pd.Series(np.zeros(len(series)), index=series.index, dtype=float)
    return (series - series.min()) / rng


def _combine(series_list: Iterable[pd.Series], weights: Iterable[float]) -> pd.Series:
    total = None
    for weight, series in zip(weights, series_list):
        contribution = weight * series
        total = contribution if total is None else total + contribution
    assert total is not None
    return total


def compute_nlis(df: pd.DataFrame, config: NLISConfig | None = None) -> pd.Series:
    """Compute the Neuro-Linguistic Integration Score for each observation."""

    config = config or NLISConfig()
    validate_frame(df, DATASET_SCHEMA)

    lexical = _combine(
        (
            _safe_norm(df["lexical_diversity"]),
            _safe_norm(df["syntax_complexity"]),
        ),
        (config.lexical_diversity_weight, config.syntax_complexity_weight),
    )
    cultural = _combine(
        (
            _safe_norm(df["ritual"]),
            _safe_norm(df["trade"]),
            _safe_norm(df["symbolism"]),
            _safe_norm(df["hierarchy"]),
        ),
        config.cultural_weights(),
    )
    return config.lexical_weight * lexical + config.cultural_weight * cultural


__all__ = ["NLISConfig", "compute_nlis"]
