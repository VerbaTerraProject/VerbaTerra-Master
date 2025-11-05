# VerbaTerra — Cultural–Linguistic Research Stack

VerbaTerra is a unified ecosystem for simulating, modelling, and analysing
cultural–linguistic evolution. It integrates the Integrated Cultural-Linguistic
Harmonics Framework (ICLHF), the Cultural Adaptation & Linguistic Resilience
(CALR) metrics suite, and three simulation engines (vSION, CCH, NΦRA).

## Installation

```bash
python -m pip install -e .[all]
```

This installs the package in editable mode together with optional dependencies
(pytest, MkDocs, CLI extras).

## CLI overview

| Command          | Description                                        |
| ---------------- | -------------------------------------------------- |
| `vt-sim`         | Run simulations with vSION, CCH, or NΦRA engines   |
| `vt-metrics`     | Compute NLIS & CRM metrics for a simulation run    |
| `vt-model-train` | Train the ICLHF predictive model                   |
| `vt-model-eval`  | Evaluate a trained model on a new dataset          |

## Quickstart

```bash
vt-sim --engine vsion --seed 42 --out runs/run_001
vt-metrics --in runs/run_001
vt-model-train --model iclhf --in runs/run_001 --out models/iclhf_run001
vt-sim --engine nphra --seed 7 --out runs/run_002
vt-model-eval --model-path models/iclhf_run001/iclhf.json --in runs/run_002 --out evals/iclhf_on_run002
```

Outputs are written to the specified directories:

- `dataset.parquet` — generated dataset
- `config_used.yaml` — merged engine configuration
- `metadata.json` — engine, seed, row count, and version
- `metrics.json` — aggregated NLIS/CRM scores
- `iclhf.json` — serialized model parameters
- `eval.json` — evaluation metrics (MSE per target)

## Repository layout

```
src/verbaterra/
├── engines/          # vSION, CCH, NΦRA simulation engines
├── metrics/          # NLIS & CRM implementations + registry
├── models/           # ICLHF model definition and registry
├── cli.py            # vt-sim / vt-metrics entry points
├── cli_model.py      # vt-model-train / vt-model-eval entry points
└── __init__.py
```

Docs live under `docs/` and are rendered with MkDocs. Unit tests reside in
`tests/unit/` and can be executed via `pytest`.

## Development

1. Install with `[all]` extras: `python -m pip install -e .[all]`
2. Run tests: `pytest`
3. Build docs locally: `mkdocs serve`
4. Generate sample run: `python run_quickstart.py`

Refer to `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` for collaboration guidance.
