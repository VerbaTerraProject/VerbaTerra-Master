from __future__ import annotations

import numpy as np

from verbaterra.models import create_model
from verbaterra.engines import run_engine


def test_iclhf_train_predict_cycle():
    df, _ = run_engine("vsion", seed=10)
    model = create_model("iclhf").fit(df)
    preds = model.predict(df)
    assert set(preds.columns) == {"lexical_diversity_hat", "syntax_complexity_hat"}
    assert np.isfinite(preds.values).all()
    serialized = model.to_dict()
    restored = model.from_dict(serialized)
    regenerated = restored.predict(df)
    assert np.allclose(preds.values, regenerated.values)
