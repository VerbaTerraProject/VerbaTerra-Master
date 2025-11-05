from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from verbaterra.metrics import compute_crm, compute_nlis


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute VerbaTerra metrics for a dataset.")
    parser.add_argument("dataset", type=Path, help="CSV file containing simulation output")
    parser.add_argument("--out", type=Path, required=True, help="Output JSON file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.dataset)
    nlis = compute_nlis(df)
    crm = compute_crm(df)
    payload = {
        "nlis_mean": nlis.mean(),
        "crm_mean": crm.mean(),
        "nlis_std": nlis.std(ddof=0),
        "crm_std": crm.std(ddof=0),
    }
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")


if __name__ == "__main__":  # pragma: no cover
    main()
