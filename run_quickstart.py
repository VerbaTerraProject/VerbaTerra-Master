from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
if _SRC.exists():
    sys.path.insert(0, str(_SRC))

from verbaterra.engines import run_engine
from verbaterra.metrics import crm, nlis
from verbaterra.models import create_model


def main() -> None:
    df, _ = run_engine("vsion", seed=7)
    df["NLIS"] = nlis(df)
    df["CRM"] = crm(df)
    model = create_model("iclhf").fit(df)
    print(model.summary())


if __name__ == "__main__":
    main()
