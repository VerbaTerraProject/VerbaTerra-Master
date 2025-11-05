# VerbaTerra

VerbaTerra is a cultural–linguistic simulation lab. It combines configurable engines, regression-ready models, and evaluative metrics so researchers can explore how ritual, trade, symbolism, and hierarchy shape language.

## Quickstart

```bash
python -m pip install verbaterra
python -m verbaterra.examples.run_vsion --out runs/example
```

Or from a cloned repository:

```bash
python run_quickstart.py
```

The [VSIONSimulator](engines.md) produces structured cultural observations that plug directly into [metrics](metrics.md) and [models](models.md).

## Architecture

- **Engines:** modular simulators (vSION, CCH, NΦRA) that synthesize cultural traits.
- **Metrics:** NLIS and CRM provide resilience scores with validated hierarchy handling.
- **Models:** ICLHFModel forecasts lexical and syntactic outcomes from cultural signals.
- **DataIO:** Schema validators and loaders guarantee reproducible experiments.

Refer to the dedicated pages for deep dives and configuration details. Methodology papers and lab notebooks are in the `docs/methodology` and `docs/labs` sections.
