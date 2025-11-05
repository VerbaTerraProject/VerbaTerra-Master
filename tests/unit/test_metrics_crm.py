from __future__ import annotations

import pandas as pd

from verbaterra.metrics import CRMConfig, compute_crm


def test_crm_score_bounds() -> None:
    df = pd.read_csv("data/samples/vsion_sample.csv")
    scores = compute_crm(df)
    assert scores.between(0, 1).all()


def test_crm_adjustable_weights() -> None:
    df = pd.read_csv("data/samples/vsion_sample.csv")
    alt = compute_crm(df, CRMConfig(trade_weight=0.2, symbolism_weight=0.8))
    default = compute_crm(df)
    assert not alt.equals(default)
