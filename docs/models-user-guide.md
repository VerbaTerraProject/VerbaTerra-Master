# ICLHF Models — User Guide

The Integrated Cultural-Linguistic Harmonics Framework (ICLHF) models predict
how cultural signals (ritual, trade, symbolism, hierarchy) give rise to
linguistic outcomes (lexical diversity, syntax complexity).

## Model registry

The registry currently exposes a single model entry:

| Name   | Description                                                  |
| ------ | ------------------------------------------------------------ |
| iclhf  | Dual linear-regression backbones for lexical and syntax axes |

Register custom models by extending `verbaterra.models.MODEL_REGISTRY` with a
`ModelSpec` entry.

## Training

```bash
vt-model-train --model iclhf --in runs/run_001 --out models/iclhf_run001
```

Training expects a dataset with the six base columns (`ritual`, `trade`,
`symbolism`, `hierarchy`, `lexical_diversity`, `syntax_complexity`). The CLI
writes:

- `iclhf.json` – serialized coefficients and intercepts
- `training_summary.txt` – human-readable coefficient report

## Loading / saving manually

```python
from verbaterra.models import ICLHFModel

model = ICLHFModel().fit(df)
path = model.save("models/iclhf_demo")
restored = ICLHFModel.load(path)
```

The JSON payload contains feature column ordering plus regression parameters.

## Evaluation

```bash
vt-model-eval --model-path models/iclhf_run001/iclhf.json \
              --in runs/run_002 \
              --out evals/iclhf_on_run002
```

Evaluation artifacts include `predictions.parquet` (combined inputs and
predictions) and `eval.json` (MSE for lexical and syntax predictions).
