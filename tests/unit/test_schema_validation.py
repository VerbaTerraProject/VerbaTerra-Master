from __future__ import annotations

import pandas as pd
import pytest

from verbaterra.dataio import DATASET_SCHEMA, SchemaError, validate_frame


def test_validate_frame_passes_for_sample() -> None:
    df = pd.read_csv("data/samples/vsion_sample.csv")
    validate_frame(df, DATASET_SCHEMA)


def test_validate_frame_missing_columns() -> None:
    df = pd.DataFrame({"ritual": [1, 2], "trade": [3, 4]})
    with pytest.raises(SchemaError):
        validate_frame(df, DATASET_SCHEMA)


def test_validate_frame_non_numeric() -> None:
    df = pd.DataFrame({
        "ritual": [1, 2],
        "trade": [3, 4],
        "symbolism": ["a", "b"],
        "hierarchy": [5, 6],
        "lexical_diversity": [7, 8],
        "syntax_complexity": [9, 10],
    })
    with pytest.raises(SchemaError):
        validate_frame(df, DATASET_SCHEMA)
