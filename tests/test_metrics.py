import pandas as pd
from verbaterra.core.metrics import crm, nlis


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ritual": [40, 50, 60],
            "trade": [30, 45, 55],
            "symbolism": [20, 35, 45],
            "hierarchy": [25, 45, 65],
            "lexical_diversity": [10, 20, 30],
            "syntax_complexity": [15, 25, 35],
        }
    )


def test_nlis_computes_without_error():
    df = _sample_df()
    scores = nlis(df)
    assert not scores.isna().any()
    assert len(scores) == len(df)


def test_crm_is_bounded_between_zero_and_one():
    df = _sample_df()
    scores = crm(df)
    assert ((0 <= scores) & (scores <= 1)).all()
