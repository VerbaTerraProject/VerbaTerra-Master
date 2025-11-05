# VerbaTerra — Simulation Lab

**AI-driven cultural–linguistic research ecosystem** exploring how ritual,
trade, symbolism, and hierarchy shape language, cognition, and cultural
resilience. VerbaTerra combines simulation engines, analytical metrics, and
predictive models so researchers can prototype and evaluate new hypotheses in a
single toolkit.

[![CI](https://github.com/VerbaTerraProject/VerbaTerra-Master/actions/workflows/ci.yml/badge.svg)](https://github.com/VerbaTerraProject/VerbaTerra-Master/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-blueviolet)](https://verbaterraproject.github.io/VerbaTerra-Master/)

## Features
- **vSION simulation engine** for generating synthetic cultural-linguistic
  communities.
- **ICLHF model** to learn lexical and syntactic harmonics from enriched data.
- **CALR metrics (NLIS & CRM)** capturing narrative integration and cultural
  resilience.
- Reproducible workflows with pytest regression tests and MkDocs technical
  documentation.

## Installation
VerbaTerra currently ships as a source distribution. Clone the repository and
install it in editable mode:

```bash
git clone https://github.com/VerbaTerraProject/VerbaTerra-Master.git
cd VerbaTerra-Master
python -m pip install -e .[test]
```

This installs the core package plus the optional pytest dependency for running
checks locally.

## Quickstart
```python
from verbaterra.iclhf.model import ICLHFModel
from verbaterra.engines.vsion import simulate_block
from verbaterra.core.metrics import nlis, crm

df = simulate_block(n=120, seed=7)
df["NLIS"] = nlis(df)
df["CRM"] = crm(df)
print(ICLHFModel().fit(df).summary())
```

Run the bundled demonstration script:

```bash
python run_quickstart.py
```

## Project layout
- `src/verbaterra/` — Python package with engines, metrics, and models.
- `tests/` — pytest suite covering simulation, metrics, and modelling.
- `docs/` — MkDocs documentation (see `mkdocs.yml` for the navigation map).
- `01_quickstart.ipynb` — interactive notebook showcasing the workflow end to
  end.

## Development workflow
1. Install the project with testing extras: `python -m pip install -e .[test]`
2. Run the unit tests: `pytest`
3. Optionally execute the quickstart script to smoke test: `python run_quickstart.py`
4. Build the documentation site locally:
   ```bash
   pip install mkdocs-material
   mkdocs serve
   ```

Refer to `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` for collaboration
guidelines.

## License
This project is licensed under the terms of the [MIT License](LICENSE).
