from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Tuple

from ..engines.vsion import SimulationConfig, VSIONSimulator
from ..metrics import compute_crm, compute_nlis
from ..utils.logging import setup_logging


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a vSION simulation and export results.")
    parser.add_argument("--config", type=Path, help="YAML config file", default=None)
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed")
    parser.add_argument("--out", type=Path, required=True, help="Output directory")
    return parser.parse_args(argv)


def _json_default(value: Any) -> Any:
    if isinstance(value, tuple):
        return list(value)
    raise TypeError(f"Unsupported type for JSON serialization: {type(value)!r}")


def compute_config_hash(config: Dict[str, Any], seed: int | None) -> str:
    payload = {"config": config, "seed": seed}
    normalised = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=_json_default)
    return hashlib.sha256(normalised.encode("utf-8")).hexdigest()


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, default=_json_default),
        encoding="utf-8",
    )


def _build_readme(
    config_hash: str, metrics: Dict[str, float], seed: int | None, dataset_format: str
) -> str:
    timestamp = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc).isoformat()
    metric_lines = "\n".join(
        f"- **{name.upper()}**: {value:.4f}" for name, value in metrics.items()
    )
    return (
        "# VerbaTerra Run\n\n"
        f"- **Timestamp (UTC):** {timestamp}\n"
        f"- **Seed:** {seed if seed is not None else 'default'}\n"
        f"- **Dataset format:** {dataset_format}\n"
        f"- **Config hash:** {config_hash}\n\n"
        "## Metrics\n"
        f"{metric_lines}\n\n"
        "## Artifacts\n"
        "- `config.json`\n"
        "- `config_hash`\n"
        "- `dataset.parquet`\n"
        "- `metrics.json`\n"
        "- `dataset.csv` (fallback copy)\n\n"
        "If parquet engines are unavailable, `dataset.parquet` contains CSV text "
        "and a duplicate CSV is stored."
    )


def _write_dataset(df, dataset_path: Path, logger) -> Tuple[Path, str]:
    try:
        df.to_parquet(dataset_path, index=False)
        return dataset_path, "parquet"
    except (ImportError, ValueError) as exc:
        # Fallback when optional parquet engines are unavailable.
        logger.warning(
            "Parquet engine unavailable; storing dataset as CSV text",
            extra={"path": str(dataset_path), "reason": str(exc)},
        )
        df.to_csv(dataset_path, index=False)
        return dataset_path, "csv"


def run_vsion(
    *, out_dir: Path, config_path: Path | None = None, seed: int | None = None
) -> Dict[str, Path]:
    logger = setup_logging(name="verbaterra.examples.run_vsion")
    config = SimulationConfig.from_yaml(config_path) if config_path else SimulationConfig()
    simulator = VSIONSimulator(config=config, seed=seed)
    df = simulator.run()

    out_dir.mkdir(parents=True, exist_ok=True)

    dataset_path = out_dir / "dataset.parquet"
    dataset_path, dataset_format = _write_dataset(df, dataset_path, logger)
    csv_shadow = out_dir / "dataset.csv"
    df.to_csv(csv_shadow, index=False)

    metrics = {
        "nlis": float(compute_nlis(df).mean()),
        "crm": float(compute_crm(df).mean()),
    }
    metrics_path = out_dir / "metrics.json"
    _write_json(metrics_path, metrics)

    config_payload = config.to_dict()
    config_path_out = out_dir / "config.json"
    _write_json(config_path_out, config_payload)

    config_hash = compute_config_hash(config_payload, seed)
    hash_path = out_dir / "config_hash"
    hash_path.write_text(config_hash + "\n", encoding="utf-8")

    metadata: Dict[str, Any] = {
        "config": config_payload,
        "seed": seed,
        "config_hash": config_hash,
        "artifacts": {
            "dataset": dataset_path.name,
            "metrics": metrics_path.name,
            "config": config_path_out.name,
            "config_hash": hash_path.name,
            "dataset_csv": csv_shadow.name,
        },
        "dataset_format": dataset_format,
    }
    metadata_path = out_dir / "metadata.json"
    _write_json(metadata_path, metadata)

    readme_path = out_dir / "README_run.md"
    readme_path.write_text(
        _build_readme(config_hash, metrics, seed, dataset_format),
        encoding="utf-8",
    )

    logger.info(
        "Run completed",
        extra={
            "output": str(out_dir),
            "config_hash": config_hash,
        },
    )

    return {
        "dataset": dataset_path,
        "dataset_csv": csv_shadow,
        "metrics": metrics_path,
        "config": config_path_out,
        "config_hash": hash_path,
        "metadata": metadata_path,
        "readme": readme_path,
    }


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    run_vsion(out_dir=args.out, config_path=args.config, seed=args.seed)


__all__ = [
    "compute_config_hash",
    "parse_args",
    "run_vsion",
    "main",
]


if __name__ == "__main__":  # pragma: no cover
    main()
