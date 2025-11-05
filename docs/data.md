# Data

The canonical simulation schema includes the following numeric columns:

- `ritual`
- `trade`
- `symbolism`
- `hierarchy`
- `lexical_diversity`
- `syntax_complexity`

Use `verbaterra.dataio.validate_frame` to enforce the schema. Sample datasets live under `data/samples/` (also packaged under `verbaterra.data.samples`). Metadata definitions are documented in `data/dictionary/fields.md`.

### Reproducible run outputs

`python -m verbaterra.examples.run_vsion --out runs/example` emits a bundle with:

- `dataset.parquet` — preferred storage; falls back to CSV text when parquet engines (pyarrow/fastparquet) are unavailable and duplicates the contents as `dataset.csv`. Install the `verbaterra[io]` extra to enable native parquet output.
- `metrics.json` — aggregate NLIS and CRM means.
- `config.json` / `config_hash` — frozen configuration and deterministic hash, used by regression tests to guard configuration drift.
- `README_run.md` — timestamp, dataset format, and artifact manifest for fast auditing.
