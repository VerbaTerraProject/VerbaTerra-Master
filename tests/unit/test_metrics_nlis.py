from __future__ import annotations

import pandas as pd
import pytest

from verbaterra.dataio import DATASET_SCHEMA, SchemaError, validate_frame
from verbaterra.metrics import NLISConfig, compute_nlis


def test_nlis_computation_matches_shape() -> None:
    df = pd.read_csv("data/samples/vsion_sample.csv")
    validate_frame(df, DATASET_SCHEMA)
    scores = compute_nlis(df)
    assert scores.shape[0] == df.shape[0]
    assert scores.between(0, 1).all()


def test_nlis_schema_error() -> None:
    df = pd.DataFrame({"ritual": [1, 2], "trade": [3, 4]})
    with pytest.raises(SchemaError):
        compute_nlis(df)


def test_nlis_configurable_weights() -> None:
    df = pd.read_csv("data/samples/vsion_sample.csv")
    high_cultural = compute_nlis(df, NLISConfig(lexical_weight=0.3, cultural_weight=0.7))
    default = compute_nlis(df)
    assert not high_cultural.equals(default)
