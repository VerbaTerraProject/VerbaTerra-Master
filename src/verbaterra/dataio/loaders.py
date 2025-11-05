from __future__ import annotations

from importlib import resources

import pandas as pd

from ..engines.vsion.simulator import SimulationConfig
from ..utils.config import load_yaml


def load_vsion_config(name: str = "default") -> SimulationConfig:
    package = "verbaterra.engines.vsion.configs"
    resource = resources.files(package).joinpath(f"{name}.yaml")
    with resources.as_file(resource) as config_path:
        data = load_yaml(config_path)
    return SimulationConfig.from_dict(data)


def load_sample_dataset() -> pd.DataFrame:
    package = "verbaterra.data.samples"
    sample_path = resources.files(package).joinpath("vsion_sample.csv")
    with sample_path.open("r", encoding="utf-8") as handle:
        return pd.read_csv(handle)


__all__ = ["load_sample_dataset", "load_vsion_config"]
