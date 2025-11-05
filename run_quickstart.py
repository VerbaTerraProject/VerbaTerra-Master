"""Run a minimal VerbaTerra workflow."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
if _SRC.exists():
    sys.path.insert(0, str(_SRC))

from verbaterra import ICLHFModel, SimulationConfig, VSIONSimulator, compute_crm, compute_nlis


def main() -> None:
    simulator = VSIONSimulator(SimulationConfig(population=120), seed=7)
    df = simulator.run()
    df["NLIS"] = compute_nlis(df)
    df["CRM"] = compute_crm(df)
    model = ICLHFModel().fit(df)
    print(model.summary())


if __name__ == "__main__":  # pragma: no cover
    main()
