from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd

from ...dataio.schema import DATASET_SCHEMA, validate_frame
from ...utils.config import load_yaml


@dataclass(frozen=True)
class SimulationConfig:
    """Configuration for a vSION simulation run."""

    population: int = 200
    ritual_mean: float = 50.0
    ritual_std: float = 10.0
    trade_mean: float = 50.0
    trade_std: float = 15.0
    symbolism_mean: float = 50.0
    symbolism_std: float = 12.0
    hierarchy_mean: float = 50.0
    hierarchy_std: float = 18.0
    noise_std: float = 5.0
    lexical_weights: tuple[float, float, float, float, float] = (0.2, 0.3, 0.25, -0.1, 20.0)
    syntax_weights: tuple[float, float, float, float, float] = (0.2, 0.15, 0.15, 0.2, 15.0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SimulationConfig":
        payload: Dict[str, Any] = dict(data)
        if "lexical_weights" in payload:
            payload["lexical_weights"] = tuple(payload["lexical_weights"])
        if "syntax_weights" in payload:
            payload["syntax_weights"] = tuple(payload["syntax_weights"])
        return cls(**payload)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "SimulationConfig":
        return cls.from_dict(load_yaml(path))

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["lexical_weights"] = list(self.lexical_weights)
        data["syntax_weights"] = list(self.syntax_weights)
        return data


class VSIONSimulator:
    """Vectorial Societal Integration Oscillation Network simulator."""

    def __init__(self, config: SimulationConfig | None = None, seed: Optional[int] = None) -> None:
        self.config = config or SimulationConfig()
        self.seed = seed

    def run(self, *, seed: Optional[int] = None) -> pd.DataFrame:
        cfg = self.config
        population = cfg.population
        rng = np.random.default_rng(seed if seed is not None else self.seed)

        ritual = rng.normal(cfg.ritual_mean, cfg.ritual_std, population)
        trade = rng.normal(cfg.trade_mean, cfg.trade_std, population)
        symbolism = rng.normal(cfg.symbolism_mean, cfg.symbolism_std, population)
        hierarchy = rng.normal(cfg.hierarchy_mean, cfg.hierarchy_std, population)
        noise = rng.normal(0.0, cfg.noise_std, population)

        lex_weights = cfg.lexical_weights
        syn_weights = cfg.syntax_weights

        lexical_diversity = (
            lex_weights[0] * ritual
            + lex_weights[1] * trade
            + lex_weights[2] * symbolism
            + lex_weights[3] * hierarchy
            + noise
            + lex_weights[4]
        )
        syntax_complexity = (
            syn_weights[0] * ritual
            + syn_weights[1] * trade
            + syn_weights[2] * symbolism
            + syn_weights[3] * hierarchy
            + noise
            + syn_weights[4]
        )

        df = pd.DataFrame(
            {
                "ritual": ritual,
                "trade": trade,
                "symbolism": symbolism,
                "hierarchy": hierarchy,
                "lexical_diversity": lexical_diversity,
                "syntax_complexity": syntax_complexity,
            }
        )
        validate_frame(df, DATASET_SCHEMA)
        return df

    def generate_metadata(self) -> Dict[str, Any]:
        return {
            "config": self.config.to_dict(),
            "seed": self.seed,
        }


__all__ = ["SimulationConfig", "VSIONSimulator"]
