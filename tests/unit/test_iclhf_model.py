from __future__ import annotations

import pandas as pd
import pytest

from verbaterra.engines.vsion.simulator import VSIONSimulator
from verbaterra.models import ICLHFModel


@pytest.fixture()
def sample_frame() -> pd.DataFrame:
    sim = VSIONSimulator(seed=0)
    return sim.run().head(50)


def test_fit_predict_roundtrip(sample_frame: pd.DataFrame) -> None:
    model = ICLHFModel().fit(sample_frame)
    preds = model.predict(sample_frame)
    assert {"lexical_diversity_hat", "syntax_complexity_hat"} <= set(preds.columns)
    assert len(preds) == len(sample_frame)


def test_predict_requires_fit(sample_frame: pd.DataFrame) -> None:
    model = ICLHFModel()
    with pytest.raises(RuntimeError):
        model.predict(sample_frame)


def test_predict_missing_columns(sample_frame: pd.DataFrame) -> None:
    model = ICLHFModel().fit(sample_frame)
    with pytest.raises(KeyError):
        model.predict(sample_frame.drop(columns=["ritual"]))
