from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..engines.vsion import SimulationConfig, VSIONSimulator
from ..metrics import compute_crm, compute_nlis
from ..utils.logging import setup_logging


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a vSION simulation and export results.")
    parser.add_argument("--config", type=Path, help="YAML config file", default=None)
    parser.add_argument("--seed", type=int, default=None, help="Optional random seed")
    parser.add_argument("--out", type=Path, required=True, help="Output directory")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    logger = setup_logging(name="verbaterra.examples.run_vsion")
    config = SimulationConfig.from_yaml(args.config) if args.config else SimulationConfig()
    simulator = VSIONSimulator(config=config, seed=args.seed)
    df = simulator.run()

    args.out.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out / "dataset.csv", index=False)
    metrics = {
        "nlis": compute_nlis(df).mean(),
        "crm": compute_crm(df).mean(),
        "seed": args.seed,
    }
    (args.out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (args.out / "metadata.json").write_text(json.dumps(simulator.generate_metadata(), indent=2), encoding="utf-8")
    (args.out / "README_run.md").write_text(
        "# VerbaTerra Run\n\n" + json.dumps(metrics, indent=2),
        encoding="utf-8",
    )
    logger.info("Run completed", extra={"output": str(args.out)})


if __name__ == "__main__":  # pragma: no cover
    main()
