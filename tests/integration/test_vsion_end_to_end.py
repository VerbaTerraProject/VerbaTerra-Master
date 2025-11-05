from __future__ import annotations

from pathlib import Path

import pandas as pd

from verbaterra.engines.vsion import SimulationConfig, VSIONSimulator
from verbaterra.metrics import compute_crm, compute_nlis


def test_vsion_simulation_produces_metrics(tmp_path: Path) -> None:
    config = SimulationConfig(population=50)
    sim = VSIONSimulator(config=config, seed=123)
    df = sim.run()
    nlis = compute_nlis(df)
    crm = compute_crm(df)
    assert len(nlis) == len(crm) == config.population

    out_dir = tmp_path / "run"
    out_dir.mkdir()
    df.to_csv(out_dir / "dataset.csv", index=False)
    summary = pd.DataFrame({"nlis": nlis, "crm": crm})
    summary.to_json(out_dir / "metrics.json", orient="records")

    assert (out_dir / "dataset.csv").exists()
    assert (out_dir / "metrics.json").exists()
