# VerbaTerra — Cultural–Linguistic Simulation & Research

*A unified, open-source repository for the VerbaTerra project: ICLHF • CALR • vSION • NΦRA • Analyst • Nexus*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license) [![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue)]() [![Status](https://img.shields.io/badge/status-active-brightgreen)]()

---

## Overview

VerbaTerra is a research and engineering initiative exploring how **culture shapes language** and how linguistic adaptation feeds back into **cultural resilience**. The code and docs in this repository operationalize the **Integrated Cultural–Linguistic Heuristic Framework (ICLHF)** and its applied extension **CALR**, and provide runnable prototypes of the **vSION** engines (civilization simulation) and the **Analyst/Nexus** modules (analysis + practical tooling).

**Core ideas**

* Culture → (ritual, trade, symbolism, hierarchy) drives linguistic structure (syntax, semantics, lexicon) and cognitive load.
* Linguistic adaptability ↔ cultural resilience (CALR).
* Blended empirical–simulative method: literature‑synthesized proxies + theory‑guided simulation.

> This repository is the single source of truth (code, data stubs, docs, notebooks) for the VerbaTerra ecosystem.

---

## Repository Structure

```
verbaterra/
├─ src/
│  └─ verbaterra/
│     ├─ __init__.py
│     ├─ core/                 # shared datatypes, metrics (NLIS, CRM), utilities
│     ├─ iclhf/                # ICLHF models (variables, causal graph, estimators)
│     ├─ calr/                 # CALR metrics and policy diagnostics
│     ├─ engines/
│     │  ├─ vsion/             # vSION simulation stubs + runners
│     │  └─ nphra/             # NΦRA (ASCII: nphra) experimental modules
│     ├─ dataio/               # loaders, validators, schema
│     └─ viz/                  # plots (heatmaps, clusters, paths)
├─ notebooks/
│  ├─ 01_quickstart.ipynb
│  ├─ 02_results_replication.ipynb
│  └─ 03_vSION_demo.ipynb
├─ data/
│  ├─ README.md                # data usage & provenance notes
│  ├─ simulated/               # generated samples (small, license‑friendly)
│  └─ empirical_proxies/       # literature‑coded proxies (placeholders)
├─ docs/
│  ├─ overview.md
│  ├─ methods.md
│  └─ roadmap.md
├─ papers/
│  └─ language_as_cultural_algorithm_publication.pdf   # distribution copy
├─ tests/
│  └─ test_nlis_crm.py
├─ .github/
│  ├─ ISSUE_TEMPLATE.md
│  ├─ PULL_REQUEST_TEMPLATE.md
│  └─ workflows/ci.yml
├─ .gitignore
├─ LICENSE
├─ CITATION.cff
├─ CONTRIBUTING.md
├─ CODE_OF_CONDUCT.md
├─ pyproject.toml
└─ README.md
```

> **Note**: Many folders start as stubs so you can push immediately and grow iteratively.

---

## Installation

```bash
# clone your repo (replace with your remote)
 git clone https://github.com/<your-org>/verbaterra.git
 cd verbaterra

# (optional) create a venv
 python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# editable install
 pip install -e .
```

Minimal runtime deps (suggested): `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `networkx`.

---

## Quickstart (10 lines)

```python
from verbaterra.iclhf import ICLHFModel
from verbaterra.engines.vsion import simulate_block
from verbaterra.core.metrics import nlis, crm

# 1) Simulate a tiny cultural block (n=50) with theory-guided priors
sim_df = simulate_block(n=50, seed=13)

# 2) Estimate NLIS/CRM
sim_df["NLIS"] = nlis(sim_df)
sim_df["CRM"]  = crm(sim_df)

# 3) Fit ICLHF regressions (culture -> language)
model = ICLHFModel().fit(sim_df)
print(model.summary())
```

> The above APIs are provided as thin stubs in `src/verbaterra/…` so the snippet runs once you wire the repo.

---

## Reproducibility

* **Python**: 3.10–3.11
* **Determinism**: all simulators accept `seed=`; CI seeds are pinned.
* **Environments**: provide `pyproject.toml` + `requirements.txt` (optional) + `notebooks/` with cell‑deterministic demos.

---

## Data Policy

* `data/simulated/` contains tiny, redistributable CSVs for demos.
* `data/empirical_proxies/` uses literature‑coded, license‑safe aggregates (no raw copyrighted corpora). See `data/README.md`.

---

## Documentation

* **docs/overview.md** – project narrative, glossary, system diagram.
* **docs/methods.md** – variables, scoring, regression specs, cluster logic.
* **docs/roadmap.md** – milestones (vSION V19+, Analyst V0→V1, Nexus Beta), including *Robustness & Directionality Validation*.

---

## Contributing

We welcome issues, PRs, and discussion. Please read **CONTRIBUTING.md** and the **CODE_OF_CONDUCT.md** (Contributor Covenant). Typical flow:

1. Fork → feature branch → small, focused PRs.
2. Add/extend tests in `tests/`.
3. Document public APIs in `docs/` and README.

---

## Cite This Work

If you use VerbaTerra, please cite the project and the publication:

```bibtex
@software{verbaterra_repo,
  title   = {VerbaTerra: Cultural–Linguistic Simulation & Research},
  author  = {Gupta, Harshit},
  year    = {2025},
  url     = {https://github.com/<your-org>/verbaterra}
}
```

> Also include the thesis/publication DOI in `CITATION.cff` once your ORCID/DOI details are finalized.

---

## License

This project is released under the **MIT License**. See `LICENSE` for details.

---

## Maintainer

**Harshit Gupta**
VerbaTerra Project — *The Master Compendium*
Contact: *add preferred email/website*

---

### Appendix — Ready‑to‑paste boilerplates (short versions)

**.gitignore (Python + notebooks)**

```
__pycache__/
*.py[cod]
*.ipynb_checkpoints
.venv/
.env
.DS_Store
.build/
dist/
*.egg-info/
```

**pyproject.toml (minimal)**

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "verbaterra"
version = "0.1.0"
description = "Cultural–linguistic simulation & analysis toolkit"
authors = [{name="Harshit Gupta"}]
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
  "numpy>=1.26",
  "pandas>=2.1",
  "scikit-learn>=1.4",
  "matplotlib>=3.8",
  "networkx>=3.2"
]

[tool.setuptools.packages.find]
where = ["src"]
```

**CONTRIBUTING.md (excerpt)**

```
- Use feature branches and small PRs.
- Add tests for new behavior; keep coverage stable.
- Follow semantic commit messages (feat:, fix:, docs:, refactor:, test:, chore:).
```

**CODE_OF_CONDUCT.md** → use Contributor Covenant v2.1 template.

**CITATION.cff (stub)**

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
title: "VerbaTerra: Cultural–Linguistic Simulation & Research"
authors:
  - family-names: Gupta
    given-names: Harshit
version: 0.1.0
license: MIT
identifiers:
  - type: doi
    value: 10.38124/ijisrt/25oct973
```

**LICENSE (MIT)**

```
MIT License

Copyright (c) 2025 Harshit Gupta

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
