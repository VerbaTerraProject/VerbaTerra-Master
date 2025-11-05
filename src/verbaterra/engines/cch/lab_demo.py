from __future__ import annotations

import json

from .simulator import simulate
from ...metrics import crm, nlis


def main() -> None:
    df, _ = simulate(seed=5)
    df["NLIS"] = nlis(df)
    df["CRM"] = crm(df)
    highlight = df[["diffusion_rate", "collective_memory", "NLIS", "CRM"]].describe().loc[
        ["mean", "std"]
    ]
    print("CCH Lab Demo Summary:")
    print(json.dumps(highlight.to_dict(), indent=2))


if __name__ == "__main__":
    main()
