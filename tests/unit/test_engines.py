from __future__ import annotations

import pandas as pd

from verbaterra.engines import available_engines, run_engine


def test_run_engine_returns_dataframe():
    for name in available_engines():
        df, config = run_engine(name, seed=3)
        assert isinstance(df, pd.DataFrame)
        assert {"ritual", "trade", "symbolism", "hierarchy"}.issubset(df.columns)
        assert config["n"] == len(df)
