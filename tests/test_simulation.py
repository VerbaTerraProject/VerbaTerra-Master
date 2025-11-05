import pandas as pd

from verbaterra.engines.vsion import simulate_block


def test_simulate_block_shape_and_columns():
    df = simulate_block(n=25, seed=42)
    expected_columns = {
        "ritual",
        "trade",
        "symbolism",
        "hierarchy",
        "lexical_diversity",
        "syntax_complexity",
    }
    assert set(df.columns) == expected_columns
    assert len(df) == 25
    assert isinstance(df, pd.DataFrame)
