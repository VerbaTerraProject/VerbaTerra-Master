from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Tuple

import pandas as pd


@dataclass(frozen=True)
class EngineSpec:
    """Metadata and callables for a simulation engine."""

    name: str
    description: str
    default_config: Dict[str, Any]
    simulate: Callable[[Dict[str, Any] | None, int | None], Tuple[pd.DataFrame, Dict[str, Any]]]


SimulationConfig = Dict[str, Any]
