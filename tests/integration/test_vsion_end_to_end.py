from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from verbaterra.examples.run_vsion import compute_config_hash, run_vsion


def test_vsion_simulation_produces_artifacts(tmp_path: Path) -> None:
    out_dir = tmp_path / "run"
    outputs = run_vsion(out_dir=out_dir, seed=123)

    dataset = outputs["dataset"]
    csv_copy = outputs["dataset_csv"]
    metrics_path = outputs["metrics"]
    config_path = outputs["config"]
    hash_path = outputs["config_hash"]
    readme_path = outputs["readme"]
    metadata_path = outputs["metadata"]

    assert dataset.exists() and dataset.suffix == ".parquet"
    assert csv_copy.exists() and csv_copy.suffix == ".csv"

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    dataset_format = metadata.get("dataset_format")
    assert dataset_format in {"parquet", "csv"}

    if dataset_format == "parquet":
        df = pd.read_parquet(dataset)
    else:
        df = pd.read_csv(dataset)
    assert not df.empty

    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    assert {"nlis", "crm"} <= metrics.keys()

    config = json.loads(config_path.read_text(encoding="utf-8"))
    hash_value = hash_path.read_text(encoding="utf-8").strip()
    assert hash_value == compute_config_hash(config, seed=123)

    readme_text = readme_path.read_text(encoding="utf-8")
    assert "VerbaTerra Run" in readme_text
    assert f"**Dataset format:** {dataset_format}" in readme_text
