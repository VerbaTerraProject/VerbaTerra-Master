from __future__ import annotations

import pandas as pd

from verbaterra.metrics import crm, nlis
from verbaterra.engines import run_engine


def test_metrics_return_series():
    df, _ = run_engine("vsion", seed=5)
    nlis_scores = nlis(df)
    crm_scores = crm(df)
    assert isinstance(nlis_scores, pd.Series)
    assert isinstance(crm_scores, pd.Series)
    assert len(nlis_scores) == len(df)
    assert len(crm_scores) == len(df)
