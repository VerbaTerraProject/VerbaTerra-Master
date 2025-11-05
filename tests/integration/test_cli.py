from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from verbaterra.cli import metrics_main, sim_main


def test_sim_cli_generates_expected_artifacts(tmp_path: Path) -> None:
    out_dir = tmp_path / "run"
    artifacts = sim_main(["--out", str(out_dir), "--seed", "123"])

    expected_files = {
        "dataset",
        "dataset_csv",
        "metrics",
        "config",
        "config_hash",
        "metadata",
        "readme",
    }
    assert expected_files.issubset(artifacts.keys())
    for path in artifacts.values():
        assert path.exists()

    df = pd.read_csv(artifacts["dataset_csv"])
    assert {"ritual", "trade", "symbolism", "hierarchy"}.issubset(df.columns)


def test_metrics_cli_reads_bundle_and_writes_metrics(tmp_path: Path) -> None:
    out_dir = tmp_path / "bundle"
    sim_main(["--out", str(out_dir), "--seed", "7"])

    metrics_path = metrics_main(["--in", str(out_dir), "--metrics", "NLIS", "CRM"])
    assert metrics_path.exists()

    payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert "nlis" in payload and "crm" in payload
    assert isinstance(payload["nlis"], float)
    assert isinstance(payload["crm"], float)
