# Experiment Templates

VerbaTerra experiments follow a structured, reproducible pipeline. Use the
following templates to design new studies or replicate existing ones.

## Baseline template

```yaml
name: vsion_baseline
engine: vsion
seed: 42
config: src/verbaterra/engines/vsion/configs/default.yaml
metrics: [NLIS, CRM]
model: iclhf
train_run: runs/run_001
compare_against: null
```

Steps:

1. `vt-sim --engine vsion --seed 42 --out runs/run_001`
2. `vt-metrics --in runs/run_001`
3. `vt-model-train --model iclhf --in runs/run_001 --out models/iclhf_run001`

## Cross-engine transfer

```yaml
name: resonance_transfer
train_engine: vsion
train_seed: 11
train_out: runs/run_vsion_11
transfer_engine: nphra
transfer_seed: 7
transfer_out: runs/run_nphra_07
model_path: models/iclhf_vsion/iclhf.json
eval_out: evals/iclhf_vsion_on_nphra
```

Steps:

1. Simulate the training run and compute metrics.
2. Train the ICLHF model.
3. Simulate the transfer run.
4. Evaluate: `vt-model-eval --model-path <model_path> --in <transfer_out> --out <eval_out>`
5. Review `eval.json` for MSE comparisons.

## Comparative metric study

```yaml
name: ritual_diffusion_sweep
engines:
  - cch
  - vsion
seeds: [3, 7, 13]
out_dir: runs/diffusion_sweep
metrics: [NLIS, CRM]
```

Automate with a simple Python script:

```python
from pathlib import Path
from verbaterra.cli import vt_sim, vt_metrics

for engine in ["cch", "vsion"]:
    for seed in [3, 7, 13]:
        out = Path("runs/diffusion_sweep") / f"{engine}_{seed:02d}"
        vt_sim(["--engine", engine, "--seed", str(seed), "--out", str(out)])
        vt_metrics(["--in", str(out)])
```

## Reporting

Aggregate results using pandas or the lab demos. Publish findings by adding new
sections to `docs/labs.md` or exporting Markdown/HTML reports from the lab
modules.
