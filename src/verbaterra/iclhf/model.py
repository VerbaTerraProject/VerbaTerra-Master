from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple
import pandas as pd
from sklearn.linear_model import LinearRegression

@dataclass
class ICLHFModel:
    reg_lex: Optional[LinearRegression] = None
    reg_syn: Optional[LinearRegression] = None
    feature_cols: Tuple[str, ...] = ("ritual", "trade", "symbolism", "hierarchy")

    def fit(self, df: pd.DataFrame) -> 'ICLHFModel':
        for c in self.feature_cols + ("lexical_diversity", "syntax_complexity"):
            if c not in df:
                raise KeyError(f"Missing column: {c}")
        X = df[list(self.feature_cols)].to_numpy()
        y_lex = df["lexical_diversity"].to_numpy()
        y_syn = df["syntax_complexity"].to_numpy()
        self.reg_lex = LinearRegression().fit(X, y_lex)
        self.reg_syn = LinearRegression().fit(X, y_syn)
        return self

    def _check_fitted(self) -> None:
        if self.reg_lex is None or self.reg_syn is None:
            raise RuntimeError("ICLHFModel must be fit before calling predict or summary")

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        self._check_fitted()
        for c in self.feature_cols:
            if c not in df:
                raise KeyError(f"Missing column: {c}")
        X = df[list(self.feature_cols)].to_numpy()
        return pd.DataFrame({
            "lexical_diversity_hat": self.reg_lex.predict(X),
            "syntax_complexity_hat": self.reg_syn.predict(X),
        }, index=df.index)

    def summary(self) -> str:
        self._check_fitted()
        def coef_line(name, reg):
            coefs = ', '.join(f"{c}:{w:.3f}" for c, w in zip(self.feature_cols, reg.coef_))
            return f"{name} ~ {coefs} | intercept={reg.intercept_:.3f}"
        return (
            "ICLHFModel (demo)\n" +
            coef_line("lexical_diversity", self.reg_lex) + "\n" +
            coef_line("syntax_complexity", self.reg_syn)
        )
