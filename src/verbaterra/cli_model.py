from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from .metrics.utils import MANDATORY_COLUMNS, require_columns
from .models import ICLHFModel, available_models, create_model


_DEF_MODEL = "iclhf"


def _load_dataset(path: Path) -> pd.DataFrame:
    if path.is_dir():
        candidate = path / "dataset.parquet"
        if not candidate.exists():
            raise FileNotFoundError(f"Expected dataset.parquet in {path}")
        return pd.read_parquet(candidate)
    return pd.read_parquet(path)


def vt_model_train(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Train a VerbaTerra predictive model")
    parser.add_argument("--model", default=_DEF_MODEL, choices=list(available_models()))
    parser.add_argument("--in", dest="input_path", type=Path, required=True)
    parser.add_argument("--out", dest="out_path", type=Path, required=True)
    parser.add_argument("--seed", type=int, help="Seed placeholder for reproducibility", default=None)
    args = parser.parse_args(argv)

    df = _load_dataset(args.input_path)
    model = create_model(args.model)
    model.fit(df)
    model_path = model.save(args.out_path, name=f"{args.model}.json")
    summary_path = args.out_path / "training_summary.txt"
    summary_path.write_text(model.summary())
    print(f"Model saved to {model_path}")


def vt_model_eval(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained VerbaTerra model")
    parser.add_argument("--model-path", type=Path, required=True)
    parser.add_argument("--in", dest="input_path", type=Path, required=True)
    parser.add_argument("--out", dest="out_path", type=Path, required=True)
    args = parser.parse_args(argv)

    df = _load_dataset(args.input_path)
    require_columns(df, MANDATORY_COLUMNS)

    model = ICLHFModel.load(args.model_path)
    preds = model.predict(df)
    out_dir = args.out_path
    out_dir.mkdir(parents=True, exist_ok=True)

    predictions = pd.concat([df, preds], axis=1)
    predictions.to_parquet(out_dir / "predictions.parquet", index=False)

    metrics = {
        "mse_lexical": float(np.mean((preds["lexical_diversity_hat"] - df["lexical_diversity"]) ** 2)),
        "mse_syntax": float(np.mean((preds["syntax_complexity_hat"] - df["syntax_complexity"]) ** 2)),
    }
    (out_dir / "eval.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))
    print(f"Evaluation artifacts written to {out_dir}")


if __name__ == "__main__":
    vt_model_train()
