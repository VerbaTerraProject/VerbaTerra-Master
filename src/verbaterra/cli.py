from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable

import pandas as pd
import yaml

from . import __version__
from .engines import available_engines, run_engine
from .metrics import METRIC_REGISTRY, compute_metrics


def _load_yaml_config(path: Path | None) -> Dict[str, object]:
    if path is None:
        return {}
    data = yaml.safe_load(Path(path).read_text())
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError("Configuration file must decode to a mapping")
    return data


def _resolve_dataset(path: Path) -> pd.DataFrame:
    if path.is_dir():
        parquet_path = path / "dataset.parquet"
        if not parquet_path.exists():
            raise FileNotFoundError(f"Expected dataset at {parquet_path}")
        return pd.read_parquet(parquet_path)
    return pd.read_parquet(path)


def vt_sim(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run a VerbaTerra simulation")
    parser.add_argument("--engine", choices=list(available_engines()), default="vsion")
    parser.add_argument("--config", type=Path, help="Optional YAML config overriding engine defaults")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", type=Path, required=True, help="Output directory for artifacts")
    args = parser.parse_args(argv)

    config_overrides = _load_yaml_config(getattr(args, "config", None))
    df, used_config = run_engine(args.engine, config=config_overrides, seed=args.seed)

    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    dataset_path = out_dir / "dataset.parquet"
    df.to_parquet(dataset_path, index=False)

    config_path = out_dir / "config_used.yaml"
    config_path.write_text(yaml.safe_dump(used_config))

    metadata = {
        "engine": args.engine,
        "seed": args.seed,
        "rows": int(len(df)),
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "version": __version__,
    }
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
    print(f"Simulation complete. Artifacts written to {out_dir}")


def vt_metrics(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Compute VerbaTerra metrics for a simulation run")
    parser.add_argument("--in", dest="input_path", type=Path, required=True, help="Run directory or dataset")
    parser.add_argument(
        "--metrics",
        nargs="+",
        default=list(METRIC_REGISTRY.keys()),
        help="Metrics to compute (default: all)",
    )
    parser.add_argument("--out", dest="out_path", type=Path, help="Optional directory to store metrics.json")
    args = parser.parse_args(argv)

    df = _resolve_dataset(args.input_path)
    results = compute_metrics(df, args.metrics)

    out_dir = args.out_path or (args.input_path if args.input_path.is_dir() else args.input_path.parent)
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = out_dir / "metrics.json"
    metrics_path.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
    print(f"Metrics written to {metrics_path}")


if __name__ == "__main__":
    vt_sim()
