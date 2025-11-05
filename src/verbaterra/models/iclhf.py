from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

FEATURE_COLUMNS: Tuple[str, ...] = ("ritual", "trade", "symbolism", "hierarchy")
TARGET_COLUMNS: Tuple[str, ...] = ("lexical_diversity", "syntax_complexity")


@dataclass
class ICLHFModel:
    """Simplified ICLHF model using linear regression backbones."""

    reg_lex: LinearRegression | None = field(default=None, init=False)
    reg_syn: LinearRegression | None = field(default=None, init=False)
    feature_cols: Tuple[str, ...] = FEATURE_COLUMNS

    def fit(self, df: pd.DataFrame) -> "ICLHFModel":
        self._validate(df, required=self.feature_cols + TARGET_COLUMNS)
        X = df[list(self.feature_cols)].to_numpy()
        y_lex = df[TARGET_COLUMNS[0]].to_numpy()
        y_syn = df[TARGET_COLUMNS[1]].to_numpy()
        self.reg_lex = LinearRegression().fit(X, y_lex)
        self.reg_syn = LinearRegression().fit(X, y_syn)
        return self

    def _validate(self, df: pd.DataFrame, required: Iterable[str]) -> None:
        missing = [c for c in required if c not in df]
        if missing:
            raise KeyError(f"Dataset missing columns: {', '.join(missing)}")

    def _check_fitted(self) -> None:
        if self.reg_lex is None or self.reg_syn is None:
            raise RuntimeError("ICLHFModel must be fit before use")

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        self._check_fitted()
        self._validate(df, required=self.feature_cols)
        X = df[list(self.feature_cols)].to_numpy()
        predictions = {
            "lexical_diversity_hat": self.reg_lex.predict(X),
            "syntax_complexity_hat": self.reg_syn.predict(X),
        }
        return pd.DataFrame(predictions, index=df.index)

    def summary(self) -> str:
        self._check_fitted()

        def _line(name: str, reg: LinearRegression) -> str:
            coefs = ", ".join(f"{col}:{coef:.3f}" for col, coef in zip(self.feature_cols, reg.coef_))
            return f"{name} ~ {coefs} | intercept={reg.intercept_:.3f}"

        return "ICLHFModel (demo)\n" + _line(TARGET_COLUMNS[0], self.reg_lex) + "\n" + _line(
            TARGET_COLUMNS[1], self.reg_syn
        )

    def to_dict(self) -> Dict[str, Dict[str, float]]:
        self._check_fitted()
        assert self.reg_lex and self.reg_syn
        return {
            "feature_columns": list(self.feature_cols),
            "lexical": {
                "coef": self.reg_lex.coef_.tolist(),
                "intercept": float(self.reg_lex.intercept_),
            },
            "syntax": {
                "coef": self.reg_syn.coef_.tolist(),
                "intercept": float(self.reg_syn.intercept_),
            },
        }

    def save(self, directory: Path | str, name: str = "iclhf.json") -> Path:
        payload = self.to_dict()
        directory_path = Path(directory)
        directory_path.mkdir(parents=True, exist_ok=True)
        target = directory_path / name
        target.write_text(json.dumps(payload, indent=2))
        return target

    @classmethod
    def load(cls, path: Path | str) -> "ICLHFModel":
        payload = json.loads(Path(path).read_text())
        return cls.from_dict(payload)

    @classmethod
    def from_dict(cls, payload: Dict[str, Dict[str, float]]) -> "ICLHFModel":
        model = cls(feature_cols=tuple(payload.get("feature_columns", FEATURE_COLUMNS)))
        lexical = payload.get("lexical")
        syntax = payload.get("syntax")
        if lexical is None or syntax is None:
            raise ValueError("Serialized payload missing components")
        model.reg_lex = LinearRegression()
        model.reg_lex.coef_ = np.array(lexical["coef"])
        model.reg_lex.intercept_ = float(lexical["intercept"])
        model.reg_lex.n_features_in_ = len(model.feature_cols)
        model.reg_syn = LinearRegression()
        model.reg_syn.coef_ = np.array(syntax["coef"])
        model.reg_syn.intercept_ = float(syntax["intercept"])
        model.reg_syn.n_features_in_ = len(model.feature_cols)
        return model
