# VerbaTerra User Manual

This manual walks through the VerbaTerra workflow from installation to
publication-ready experiment reports. The system integrates the Integrated
Cultural-Linguistic Harmonics Framework (ICLHF) with the Cultural Adaptation &
Linguistic Resilience (CALR) metrics suite.

## Installation

```bash
python -m pip install -e .[all]
```

The `[all]` extra installs optional dependencies used by pytest, MkDocs, and
the command line utilities.

## CLI overview

| Command           | Purpose                                       |
| ----------------- | --------------------------------------------- |
| `vt-sim`          | Run simulations with vSION, CCH, or NΦRA      |
| `vt-metrics`      | Compute NLIS/CRM metrics for a simulation run |
| `vt-model-train`  | Train the ICLHF predictive model              |
| `vt-model-eval`   | Evaluate a trained model on a dataset         |

All CLIs provide `--help` for a full argument list.

## Workflow summary

1. **Simulate.** Generate cultural-linguistic data with one of the engines.
2. **Compute metrics.** Run CALR to attach NLIS and CRM signals.
3. **Train.** Fit the ICLHF model to the simulation outputs.
4. **Evaluate.** Transfer the model to new runs or engines to measure
   generalisation.
5. **Report.** Use the labs utilities or MkDocs pages to communicate findings.

## Example pipeline

```bash
vt-sim --engine vsion --seed 42 --out runs/run_001
vt-metrics --in runs/run_001 --metrics NLIS CRM
vt-model-train --model iclhf --in runs/run_001 --out models/iclhf_run001
vt-sim --engine nphra --seed 7 --out runs/run_002
vt-model-eval --model-path models/iclhf_run001/iclhf.json --in runs/run_002 --out evals/iclhf_on_run002
```

Artifacts are written alongside each run:

- `dataset.parquet` – Primary simulation output.
- `config_used.yaml` – Engine configuration used for the run.
- `metadata.json` – Engine, seed, row count, and version metadata.
- `metrics.json` – Aggregated NLIS/CRM scores from `vt-metrics`.
- `iclhf.json` – Serialized model parameters.
- `eval.json` – Evaluation metrics (MSE per target).

## Troubleshooting

- **Missing Parquet support:** Ensure `pyarrow` is installed (included via the
  `[all]` extra).
- **Schema errors:** Verify generated datasets include ritual, trade,
  symbolism, hierarchy, lexical_diversity, and syntax_complexity columns before
  running metrics or model evaluation.
- **CLI discovery:** Reinstall with `pip install -e .[all]` if the console
  entry points are not visible.
