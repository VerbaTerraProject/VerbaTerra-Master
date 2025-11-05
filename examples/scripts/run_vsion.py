from __future__ import annotations

import argparse
import json
from pathlib import Path

from verbaterra.engines.vsion import SimulationConfig, VSIONSimulator
from verbaterra.metrics import compute_crm, compute_nlis
from verbaterra.utils.logging import setup_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a vSION simulation and export results.")
    parser.add_argument("--config", type=Path, help="Path to a YAML config file", default=None)
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed")
    parser.add_argument("--out", type=Path, required=True, help="Output directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger = setup_logging(name="verbaterra.run_vsion")
    logger.info("Starting vSION simulation")

    config = SimulationConfig.from_yaml(args.config) if args.config else SimulationConfig()
    simulator = VSIONSimulator(config=config, seed=args.seed)
    df = simulator.run()
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    dataset_path = out_dir / "dataset.csv"
    metrics_path = out_dir / "metrics.json"
    metadata_path = out_dir / "metadata.json"

    df.to_csv(dataset_path, index=False)
    nlis = compute_nlis(df)
    crm = compute_crm(df)
    metrics = {"nlis": nlis.mean(), "crm": crm.mean()}
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    metadata_path.write_text(json.dumps(simulator.generate_metadata(), indent=2), encoding="utf-8")

    logger.info("Run complete", extra={"dataset": str(dataset_path), "metrics": str(metrics_path)})


if __name__ == "__main__":  # pragma: no cover
    main()
