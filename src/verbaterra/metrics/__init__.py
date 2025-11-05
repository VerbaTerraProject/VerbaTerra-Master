from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable

import pandas as pd
from pandas import Series

from .crm import crm
from .nlis import nlis

__all__ = ["nlis", "crm", "METRIC_REGISTRY", "available_metrics", "compute_metrics"]


@dataclass(frozen=True)
class MetricSpec:
    name: str
    compute: Callable[[pd.DataFrame], Series]
    description: str


METRIC_REGISTRY: Dict[str, MetricSpec] = {
    "NLIS": MetricSpec(name="NLIS", compute=nlis, description="Neuro-Linguistic Integration Score"),
    "CRM": MetricSpec(name="CRM", compute=crm, description="Cultural Resilience Metric"),
}


def available_metrics() -> Iterable[str]:
    return sorted(METRIC_REGISTRY)


def compute_metrics(df: pd.DataFrame, metrics: Iterable[str]) -> Dict[str, float]:
    results: Dict[str, float] = {}
    for metric in metrics:
        key = metric.upper()
        if key not in METRIC_REGISTRY:
            raise KeyError(f"Unknown metric '{metric}'. Available: {', '.join(sorted(METRIC_REGISTRY))}")
        series = METRIC_REGISTRY[key].compute(df)
        results[key] = float(series.mean())
    return results
