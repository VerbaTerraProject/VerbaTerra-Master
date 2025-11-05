from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
if _SRC.exists():
    sys.path.insert(0, str(_SRC))

from verbaterra.iclhf.model import ICLHFModel
from verbaterra.engines.vsion import simulate_block
from verbaterra.core.metrics import nlis, crm

def main():
    df = simulate_block(n=120, seed=7)
    df["NLIS"] = nlis(df); df["CRM"] = crm(df)
    print(ICLHFModel().fit(df).summary())

if __name__ == "__main__":
    main()
