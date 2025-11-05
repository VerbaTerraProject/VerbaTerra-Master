from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence

import pandas as pd
from sklearn.linear_model import LinearRegression

from ..dataio.schema import DATASET_SCHEMA, validate_frame


@dataclass
class ICLHFModel:
    """Inter-Cultural Linguistic Harmony Forecasting model."""

    feature_cols: Sequence[str] = field(
        default_factory=lambda: ("ritual", "trade", "symbolism", "hierarchy")
    )
    _reg_lex: Optional[LinearRegression] = field(default=None, init=False, repr=False)
    _reg_syn: Optional[LinearRegression] = field(default=None, init=False, repr=False)

    def fit(self, df: pd.DataFrame) -> "ICLHFModel":
        validate_frame(df, DATASET_SCHEMA)
        X = df[list(self.feature_cols)].to_numpy()
        y_lex = df["lexical_diversity"].to_numpy()
        y_syn = df["syntax_complexity"].to_numpy()
        self._reg_lex = LinearRegression().fit(X, y_lex)
        self._reg_syn = LinearRegression().fit(X, y_syn)
        return self

    def _check_fitted(self) -> None:
        if self._reg_lex is None or self._reg_syn is None:
            raise RuntimeError("ICLHFModel must be fit before calling predict or summary")

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        self._check_fitted()
        assert self._reg_lex is not None and self._reg_syn is not None
        missing = [c for c in self.feature_cols if c not in df]
        if missing:
            raise KeyError(f"Missing columns for prediction: {missing}")
        X = df[list(self.feature_cols)].to_numpy()
        return pd.DataFrame(
            {
                "lexical_diversity_hat": self._reg_lex.predict(X),
                "syntax_complexity_hat": self._reg_syn.predict(X),
            },
            index=df.index,
        )

    def summary(self) -> str:
        self._check_fitted()
        assert self._reg_lex is not None and self._reg_syn is not None

        def fmt(name: str, reg: LinearRegression) -> str:
            weights = ", ".join(
                f"{col}:{coef:.3f}" for col, coef in zip(self.feature_cols, reg.coef_, strict=False)
            )
            return f"{name} ~ {weights} | intercept={reg.intercept_:.3f}"

        return "ICLHFModel\n" + "\n".join(
            (
                fmt("lexical_diversity", self._reg_lex),
                fmt("syntax_complexity", self._reg_syn),
            )
        )


__all__ = ["ICLHFModel"]
