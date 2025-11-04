# VerbaTerra — Simulation Lab (ICLHF • CALR • vSION • NΦRA • Analyst • Nexus)

**AI-driven cultural–linguistic research ecosystem** that models how ritual, trade, symbolism, and hierarchy shape language, cognition, and cultural resilience.
Powered by the **vSION**, **NΦRA**, **Analyst**, and **Nexus** engines, implementing the **ICLHF** and **CALR** frameworks.

## Quickstart (10 lines)
```python
from verbaterra.iclhf.model import ICLHFModel
from verbaterra.engines.vsion import simulate_block
from verbaterra.core.metrics import nlis, crm

df = simulate_block(n=120, seed=7)
df["NLIS"] = nlis(df); df["CRM"] = crm(df)
print(ICLHFModel().fit(df).summary())
```
