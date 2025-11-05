from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a markdown report from simulation outputs."
    )
    parser.add_argument("dataset", type=Path, help="CSV dataset")
    parser.add_argument("metrics", type=Path, help="Metrics JSON file")
    parser.add_argument("--out", type=Path, required=True, help="Markdown report path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.dataset)
    metrics = pd.read_json(args.metrics)

    report = [
        "# VerbaTerra Simulation Report",
        "",
        f"Observations: {len(df)}",
        "",
        "## Metrics Summary",
        metrics.to_markdown(index=False),
    ]
    args.out.write_text("\n".join(report), encoding="utf-8")


if __name__ == "__main__":  # pragma: no cover
    main()
