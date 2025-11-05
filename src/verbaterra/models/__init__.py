from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable

from .iclhf import ICLHFModel

__all__ = [
    "MODEL_REGISTRY",
    "ICLHFModel",
    "available_models",
    "create_model",
]


@dataclass(frozen=True)
class ModelSpec:
    name: str
    factory: Callable[[], ICLHFModel]
    description: str


MODEL_REGISTRY: Dict[str, ModelSpec] = {
    "iclhf": ModelSpec(
        name="iclhf",
        factory=ICLHFModel,
        description="Integrated Cultural-Linguistic Harmonics Framework linear model",
    )
}


def available_models() -> Iterable[str]:
    return sorted(MODEL_REGISTRY)


def create_model(name: str) -> ICLHFModel:
    key = name.lower()
    if key not in MODEL_REGISTRY:
        raise KeyError(f"Unknown model '{name}'. Available: {', '.join(sorted(MODEL_REGISTRY))}")
    return MODEL_REGISTRY[key].factory()
