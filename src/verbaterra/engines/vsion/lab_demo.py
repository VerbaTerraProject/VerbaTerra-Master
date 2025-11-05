from __future__ import annotations

import json

from .simulator import simulate
from ...metrics import crm, nlis


def main() -> None:
    df, _ = simulate(seed=7)
    df["NLIS"] = nlis(df)
    df["CRM"] = crm(df)
    summary = {
        "rows": len(df),
        "nlis_mean": float(df["NLIS"].mean()),
        "crm_mean": float(df["CRM"].mean()),
    }
    print("vSION Lab Demo Summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
