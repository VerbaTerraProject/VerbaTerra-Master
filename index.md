# API Reference (Stubs)

## `verbaterra.engines.vsion.simulate_block(n:int=200, seed:Optional[int]=None) -> pd.DataFrame`
Returns DataFrame with cultural drivers and linguistic outcomes.

## `verbaterra.iclhf.ICLHFModel`
- `fit(df)` → trains OLS models for lexical and syntax.
- `predict(df)` → returns `*_hat` predictions.
- `summary()` → human-readable coefficients.
