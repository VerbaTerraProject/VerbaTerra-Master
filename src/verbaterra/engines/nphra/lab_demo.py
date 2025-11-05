from __future__ import annotations

import json

from .simulator import simulate
from ...metrics import crm, nlis


def main() -> None:
    df, _ = simulate(seed=11)
    df["NLIS"] = nlis(df)
    df["CRM"] = crm(df)
    summary = {
        "resonance_mean": float(df["resonance_wave"].mean()),
        "neuro_coherence_peak": float(df["neuro_coherence"].max()),
        "nlis_p95": float(df["NLIS"].quantile(0.95)),
    }
    print("NΦRA Lab Demo Summary:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
