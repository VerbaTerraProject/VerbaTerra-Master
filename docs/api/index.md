# API Reference Overview

The VerbaTerra package exposes a concise surface API that wraps the core
simulation engines and analysis utilities. Import from the top-level package
for the most common workflows:

```python
from verbaterra import ICLHFModel, simulate_block, nlis, crm
```

## Simulation engine (`verbaterra.engines.vsion`)
- `simulate_block(n: int, *, seed: int | None = None) -> pandas.DataFrame`
  generates a synthetic cultural-linguistic community with lexical, symbolic,
  trade, and hierarchy attributes. The output is suitable for direct scoring
  with the metrics module or as input to the ICLHF model.

## Metrics module (`verbaterra.core.metrics`)
- `nlis(df: pandas.DataFrame) -> pandas.Series` computes the Narrative
  Linguistic Integration Score combining lexical density, ritual salience,
  trade centrality, and hierarchical balance.
- `crm(df: pandas.DataFrame) -> pandas.Series` measures Cultural Resilience via
  weighted symbolism and resource flow parameters.

All metric helpers automatically handle missing columns by coercing absent
inputs to zero prior to normalization.

## ICLHF model (`verbaterra.iclhf.model.ICLHFModel`)
The main entry point for predictive modelling. `ICLHFModel` exposes
`fit()`, `predict()`, and `summary()` for calibrating lexical and syntactic
regressors against NLIS/CRM enriched datasets. Calling `predict()` before
`fit()` raises a clear runtime error to guard against misuse.

Refer to the unit tests under `tests/` for end-to-end usage examples that
exercise the simulator, metric computations, and the model pipeline.
