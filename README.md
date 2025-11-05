# VerbaTerra

VerbaTerra is a production-ready cultural–linguistic simulation lab. It ships with configurable engines, resilience metrics, and regression baselines so you can study how ritual, trade, symbolism, and hierarchy co-evolve with language.

[![CI](https://github.com/VerbaTerraProject/VerbaTerra-Master/actions/workflows/ci.yml/badge.svg)](https://github.com/VerbaTerraProject/VerbaTerra-Master/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-blueviolet)](https://verbaterraproject.github.io/VerbaTerra-Master/)

## Installation

```bash
git clone https://github.com/VerbaTerraProject/verbaterra.git
cd verbaterra
python -m pip install -e .[dev]
```

The `dev` extra installs pytest, ruff, black, and mypy for local validation.

## 60-second quickstart

```python
from verbaterra import VSIONSimulator, ICLHFModel, compute_nlis

sim = VSIONSimulator(seed=7)
df = sim.run()
df["NLIS"] = compute_nlis(df)
model = ICLHFModel().fit(df)
print(model.summary())
```

Or run the scripted example:

```bash
python run_quickstart.py
```

## Project layout

```
src/verbaterra/    # engines, metrics, models, dataio, hypotheses, utilities
examples/          # CLI scripts and notebooks
tests/             # unit and integration suites
docs/              # MkDocs Material documentation
.github/workflows/ # CI and documentation pipelines
data/              # dictionary and sample datasets
```

## Development workflow

1. Install dependencies: `python -m pip install -e .[dev,docs]`
2. Lint & format: `ruff check .` and `black --check .`
3. Type-check: `mypy .`
4. Run tests: `pytest`
5. Build docs: `mkdocs build`

See [CONTRIBUTING.md](CONTRIBUTING.md) for pull request guidelines and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community expectations.
