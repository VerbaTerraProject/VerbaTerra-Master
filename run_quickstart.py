"""Run a minimal VerbaTerra workflow."""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_src_on_path() -> None:
    root = Path(__file__).resolve().parent
    src_dir = root / "src"
    if src_dir.exists() and str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))


def main() -> None:
    _ensure_src_on_path()
    from verbaterra import (
        ICLHFModel,
        SimulationConfig,
        VSIONSimulator,
        compute_crm,
        compute_nlis,
    )

    simulator = VSIONSimulator(SimulationConfig(population=120), seed=7)
    df = simulator.run()
    df["NLIS"] = compute_nlis(df)
    df["CRM"] = compute_crm(df)
    model = ICLHFModel().fit(df)
    print(model.summary())


if __name__ == "__main__":  # pragma: no cover
    main()
