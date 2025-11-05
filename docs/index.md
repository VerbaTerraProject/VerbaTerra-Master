# VerbaTerra

VerbaTerra is a cultural–linguistic simulation lab. It combines configurable engines, regression-ready models, and evaluative metrics so researchers can explore how ritual, trade, symbolism, and hierarchy shape language.

## Quickstart

```bash
python -m pip install verbaterra
vt-sim --out runs/example --seed 42
vt-metrics --in runs/example --metrics NLIS CRM
```

Or from a cloned repository:

```bash
python run_quickstart.py
```

The [VSIONSimulator](engines.md) produces structured cultural observations that plug directly into [metrics](metrics.md) and [models](models.md).

### Public API

Installers can rely on stable, top-level imports:

```python
from verbaterra import VSIONSimulator, compute_nlis, compute_crm, ICLHFModel
```

These symbols are exported via `verbaterra.__all__` and covered by regression tests to guarantee availability across releases.

## Architecture

- **Engines:** modular simulators (vSION, CCH, NΦRA) that synthesize cultural traits.
- **Metrics:** NLIS and CRM provide resilience scores with validated hierarchy handling.
- **Models:** ICLHFModel forecasts lexical and syntactic outcomes from cultural signals.
- **DataIO:** Schema validators and loaders guarantee reproducible experiments.

Refer to the dedicated pages for deep dives and configuration details. Methodology papers and lab notebooks are in the `docs/methodology` and `docs/labs` sections.
