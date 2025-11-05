from __future__ import annotations

from importlib import resources

import pandas as pd


def load_vsion_config(name: str = "default") -> SimulationConfig:
    import yaml
    from ..engines.vsion.simulator import SimulationConfig

    package = "verbaterra.engines.vsion.configs"
    with resources.files(package).joinpath(f"{name}.yaml").open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return SimulationConfig.from_dict(data)


def load_sample_dataset() -> pd.DataFrame:
    package = "verbaterra.data.samples"
    with resources.files(package).joinpath("vsion_sample.csv").open("r", encoding="utf-8") as handle:
        return pd.read_csv(handle)


__all__ = ["load_sample_dataset", "load_vsion_config"]
