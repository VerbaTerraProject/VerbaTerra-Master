"""Command-line entry points for VerbaTerra."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Dict, Iterable, Mapping

import pandas as pd

from .examples import run_vsion as run_vsion_module
from .metrics import compute_crm, compute_nlis

MetricFunc = Callable[[pd.DataFrame], float]


def _json_dump(path: Path, payload: Mapping[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _resolve_metrics(metric_names: Iterable[str]) -> Dict[str, MetricFunc]:
    registry: Dict[str, MetricFunc] = {
        "NLIS": lambda df: float(compute_nlis(df).mean()),
        "CRM": lambda df: float(compute_crm(df).mean()),
    }
    resolved: Dict[str, MetricFunc] = {}
    for name in metric_names:
        key = name.upper()
        if key not in registry:
            available = ", ".join(sorted(registry))
            raise SystemExit(f"Unknown metric '{name}'. Available metrics: {available}")
        resolved[key] = registry[key]
    return resolved


def _load_dataset(run_dir: Path) -> pd.DataFrame:
    dataset_parquet = run_dir / "dataset.parquet"
    if dataset_parquet.exists():
        try:
            return pd.read_parquet(dataset_parquet)
        except (ImportError, ValueError, OSError):
            # The workflow stores CSV data inside dataset.parquet when parquet engines are absent.
            return pd.read_csv(dataset_parquet)
    dataset_csv = run_dir / "dataset.csv"
    if dataset_csv.exists():
        return pd.read_csv(dataset_csv)
    raise SystemExit(
        f"Could not locate a dataset in '{run_dir}'. Expected 'dataset.parquet' or 'dataset.csv'."
    )


def _build_sim_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a vSION simulation and export artifacts.")
    parser.add_argument("--config", type=Path, default=None, help="Optional YAML config path")
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed")
    parser.add_argument("--out", type=Path, required=True, help="Output directory for artifacts")
    return parser


def _build_metrics_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compute VerbaTerra metrics for a run directory.")
    parser.add_argument("--in", dest="run_dir", type=Path, required=True, help="Run directory")
    parser.add_argument(
        "--metrics",
        nargs="+",
        default=["NLIS", "CRM"],
        help="Metrics to compute (choices: NLIS, CRM)",
    )
    parser.add_argument(
        "--out",
        dest="output",
        type=Path,
        default=None,
        help="Optional output path. Defaults to <run_dir>/metrics.json",
    )
    return parser


def sim_main(argv: list[str] | None = None) -> Dict[str, Path]:
    """Entry point for the vt-sim console script."""

    args = _build_sim_parser().parse_args(argv)
    return run_vsion_module.run_vsion(out_dir=args.out, config_path=args.config, seed=args.seed)


def metrics_main(argv: list[str] | None = None) -> Path:
    """Entry point for the vt-metrics console script."""

    args = _build_metrics_parser().parse_args(argv)
    run_dir: Path = args.run_dir
    metrics = _resolve_metrics(args.metrics)
    df = _load_dataset(run_dir)

    results = {name.lower(): func(df) for name, func in metrics.items()}
    output = args.output or (run_dir / "metrics.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    _json_dump(output, results)
    return output


__all__ = ["metrics_main", "sim_main"]
