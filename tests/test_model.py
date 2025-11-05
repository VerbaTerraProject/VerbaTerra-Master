import pytest

from verbaterra.engines.vsion import simulate_block
from verbaterra.iclhf.model import ICLHFModel


def test_predict_requires_fit():
    df = simulate_block(n=10, seed=123)
    model = ICLHFModel()
    with pytest.raises(RuntimeError):
        model.predict(df)


def test_fit_predict_roundtrip():
    df = simulate_block(n=30, seed=77)
    model = ICLHFModel().fit(df)
    preds = model.predict(df)
    assert set(preds.columns) == {"lexical_diversity_hat", "syntax_complexity_hat"}
    assert len(preds) == len(df)
    summary = model.summary()
    assert "ICLHFModel" in summary
    assert "lexical_diversity" in summary
