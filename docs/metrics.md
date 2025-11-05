# Metrics

## NLIS — Neuro-Linguistic Integration Score

`compute_nlis(df, config)` normalizes lexical and cultural signals before combining them. The hierarchy contribution is now calculated with the same `_safe_norm` routine as other cultural features, fixing the prior line-break bug that dropped the term entirely.

Default weighting comes from `NLISConfig`:

- `lexical_weight=0.7`, `cultural_weight=0.3`
- `lexical_diversity_weight=0.6`, `syntax_complexity_weight=0.4`
- Cultural weights default to 0.25 across ritual, trade, symbolism, hierarchy.

## CRM — Cultural Resilience Metric

`compute_crm(df, config)` measures trade-symbolism synergy, hierarchy penalties, and ritual stability. Adjust `CRMConfig` to emphasize specific pressures. Output is clipped to `[0, 1]` for interpretability.

Both metrics validate input via `verbaterra.dataio.validate_frame`, ensuring the schema expectation is enforced prior to computation.
