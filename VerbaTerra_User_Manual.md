
# VerbaTerra — User Manual (Experience Pipeline & Repository Usage)

_Last updated: 2025-11-05_

Welcome to **VerbaTerra** — a cultural–linguistic simulation and analysis toolkit. This manual explains the overall **experience pipeline** and provides step‑by‑step instructions to **install, run, extend, test, document, and deploy** the project.

---

## 1) What is VerbaTerra?
VerbaTerra models how cultures and languages co‑evolve. You can:
- **Simulate** societies with tunable “ICLHF” knobs (ritual, trade, symbolism, hierarchy).
- **Compute metrics** like **NLIS** (Neuro‑Linguistic Integration Score) and **CRM** (Cultural Resilience Metric).
- **Fit simple models** (e.g., `ICLHFModel`) to study signal relationships.
- **Version & reproduce** experiments using configs, seeds, and CI.

**Core components**
- **Engines:** vSION (always available), plus optional CCH and NΦRA (feature branch).
- **Metrics:** NLIS (hierarchy term repaired), CRM.
- **Model:** ICLHFModel (fitted‑state checks; deterministic given seed).

---

## 2) Repository Layout (at a glance)
```
verbaterra/
├─ src/verbaterra/          # installable package (src-layout)
│  ├─ engines/              # simulators (vSION; optionally CCH, NΦRA)
│  ├─ metrics/              # NLIS/CRM + schema validation
│  ├─ models/               # ICLHFModel
│  ├─ cli.py                # console entrypoints
│  └─ __init__.py           # clean top-level exports
├─ tests/                   # unit & (optional) integration tests
├─ docs/                    # MkDocs site
├─ .github/workflows/       # CI for tests & docs
├─ pyproject.toml           # packaging metadata & deps
├─ mkdocs.yml               # docs config
├─ README.md                # quickstart
└─ Makefile                 # common tasks
```

**Branch model**
- **`main` (master-min)**: vSION only (lean, stable).
- **`feat/all-simulators`**: adds CCH & NΦRA with tests/docs → merged to `main` via PR.

---

## 3) Installation & Environment
**Requirements:** Python **3.10+**, `pip`, optional `virtualenv`.

```bash
# Clone and set up a virtual environment
git clone <your_repo_url> verbaterra && cd verbaterra
python -m venv .venv && source .venv/bin/activate

# Install (dev + docs extras)
pip install -U pip
pip install -e .[all]  # or: pip install -e .[dev]  /  .[docs]

# Pre-commit hooks (recommended)
pre-commit install
```

**Makefile shortcuts** (optional):
```bash
make setup       # venv + install + pre-commit
make lint        # ruff + black --check
make type        # mypy
make test        # pytest
make docs        # mkdocs build
```

---

## 4) Experience Pipeline (End‑to‑End)

### Step A — Configure a Simulation
- Choose an engine and a config file (YAML).
- Set a **seed** to ensure reproducibility.
- Core knobs (ICLHF): `ritual`, `trade`, `symbolism`, `hierarchy`.

Example (vSION default config at `src/verbaterra/engines/vsion/configs/default.yaml`):
```yaml
steps: 50
population: 200
ritual: 0.5
trade: 0.5
symbolism: 0.5
hierarchy: 0.5
```

### Step B — Run Simulation (CLI)
```bash
vt-sim --config src/verbaterra/engines/vsion/configs/default.yaml \
       --seed 42 \
       --out runs/run_001
```
**Outputs in `runs/run_001/`:**
- `dataset.parquet` — simulated data
- `config.json` — resolved parameters
- (you can add `README_run.md`, plots, etc.)

### Step C — Compute Metrics (CLI)
```bash
vt-metrics --in runs/run_001 --metrics NLIS CRM
```
Creates `runs/run_001/metrics.json` with aggregated values.

### Step D — Model Fitting (Python API)
```python
from verbaterra import ICLHFModel, VSIONSimulator, SimulationConfig
import pandas as pd

cfg = SimulationConfig(seed=42)
df = VSIONSimulator(cfg).run()
model = ICLHFModel(seed=42).fit(df)
pred = model.predict(df)   # raises NotFittedError if fit() not called
```

### Step E — Document & Share
- Build docs locally: `mkdocs build` (serves HTML in `site/`).
- Publish via GitHub Pages (automatic on merge to `main` if workflow enabled).

### Step F — Continuous Validation
- CI runs lint/type/tests/coverage on PRs and `main`.
- A passing PR can be **squash‑merged** to keep history tidy.

---

## 5) Simulators (Engines)

### vSION (always available)
- Deterministic RNG with `seed`.
- Produces a DataFrame with required columns:
  - `ritual`, `trade`, `symbolism`, `hierarchy`, `signal`.

### CCH (feature branch)
- Tilt towards ritual structure & trade diffusion (slightly different weighting, lower noise).

### NΦRA (feature branch)
- Adds a small non‑linear **trade × symbolism** coupling controlled by `coherence`.

> All engines **must** return the same required columns. This keeps metrics & models plug‑and‑play.

---

## 6) Metrics

### NLIS — Neuro‑Linguistic Integration Score
- Uses means of ICLHF features with a repaired hierarchy term applying **diminishing returns**:
  - `sqrt(mean(hierarchy^2))` × weight × `hierarchy_weight` (configurable).
- Usage (Python):
```python
from verbaterra.metrics.nlis import compute_nlis, NLISConfig
v = compute_nlis(df, NLISConfig(hierarchy_weight=1.0))
```
- **Regression tests** ensure stability within expected ranges.

### CRM — Cultural Resilience Metric
- A simple variance‑based proxy combining ritual/trade variability:
```python
from verbaterra.metrics.crm import compute_crm, CRMConfig
v = compute_crm(df, CRMConfig(alpha=0.6, beta=0.4))
```

### Schema Validation
- All metrics call `metrics/schema.validate_columns(df)`.
- Raises `SchemaError` if required columns are missing — fail fast with actionable error.

---

## 7) Python API Cheatsheet
```python
from verbaterra import (
    VSIONSimulator, SimulationConfig,   # always available
    compute_nlis, NLISConfig,
    compute_crm,  CRMConfig,
    ICLHFModel,
    # On feature branch (after merge):
    # CCHSimulator, CCHConfig, NPHRASimulator, NPHRAConfig
)

# Simulation
cfg = SimulationConfig(seed=123, ritual=0.6)
df  = VSIONSimulator(cfg).run()

# Metrics
nlis = compute_nlis(df, NLISConfig(hierarchy_weight=1.2))
crm  = compute_crm(df)

# Model
m = ICLHFModel(seed=7).fit(df)
preds = m.predict(df)
```

---

## 8) Configuration & Reproducibility
- Keep configs in `src/verbaterra/engines/<engine>/configs/` or `configs/` at repo root.
- Always record: **seed**, **config hash**, **library versions** (consider a run manifest).
- Use one of:
  - CLI flags (`--config`, `--seed`, `--out`),
  - or hydrate `SimulationConfig` in Python with parameters.
- Prefer **deterministic** sources of randomness.

---

## 9) Running Tests & Coverage
```bash
pytest -q
pytest --cov=verbaterra --cov-report=term-missing
```
**What’s tested**
- ICLHFModel success/unfitted error paths.
- NLIS regression stability (bounded range).
- CRM non‑negativity sanity.
- Schema missing columns → `SchemaError`.

---

## 10) Documentation (MkDocs)
- Main entry: `docs/index.md`.
- Engines intro: `docs/engines.md` (branch‑specific contents).
- Build locally:
```bash
mkdocs serve     # live preview at http://127.0.0.1:8000
mkdocs build     # static site in site/
```
- GitHub Pages deploys automatically via `docs.yml` workflow (on merge to `main`).

---

## 11) CI/CD (GitHub Actions)
- `ci.yml`: lint (`ruff`), format check (`black --check`), type (`mypy`), tests (`pytest`) with coverage gate (≥85%).
- `docs.yml`: build & deploy docs to Pages.
- Optional: security/audit jobs (`pip-audit`) as non‑blocking checks.

---

## 12) Contributing & Governance
- Use **feature branches** + PRs. Protect `main` (require CI; prohibit direct pushes).
- Conventional commits (e.g., `feat:`, `fix:`, `docs:`).
- Update **CHANGELOG** on releases.
- Community docs: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.
- Add **CITATION.cff** and issue templates for better collaboration.

---

## 13) Troubleshooting

**Q: `NotFittedError` when calling `predict`?**  
A: Call `fit()` with a valid DataFrame first. The error is intentional to catch misuse.

**Q: `SchemaError: Missing columns ...`?**  
A: Ensure your DataFrame has exactly: `ritual, trade, symbolism, hierarchy, signal`.

**Q: My metrics fluctuate across runs.**  
A: Fix a `seed` and use identical configs; check for code that bypasses the RNG seed.

**Q: CI failing on lint/mypy.**  
A: Run `make lint` / `make type` locally; apply autofixes (`ruff --fix`, `black .`).

**Q: Docs not deploying.**  
A: Ensure Pages is enabled; verify `docs.yml` ran and published the `site/` artifact.

---

## 14) FAQs

**Can I add new engines?**  
Yes. Implement a simulator that returns the **same schema**, add a config loader, tests, and export it in `__init__.py`.

**Can I change NLIS weights?**  
Yes. Adjust `NLISConfig(hierarchy_weight=…)` or edit the implementation with tests + doc updates.

**Is the project pip‑installable?**  
Yes. `pip install -e .[all]` (or subset extras).

**How do I cite VerbaTerra?**  
Use the `CITATION.cff` and add DOIs in the docs/papers section.

---

## 15) Release & Versioning
- Tag stable releases (e.g., `v0.1.0`) after merging feature branches.
- Keep `main` releasable; rely on CI for automated checks.
- Consider Release Drafter or a CHANGELOG for transparency.

---

## 16) Roadmap Pointers
- Expand datasets & dictionary.
- Deeper validation of NLIS/CRM against new scenarios.
- Richer models; add integration tests and benchmarks.
- Versioned docs for major releases.

---

## 17) Quick Reference

**CLI**
```bash
vt-sim --config <path.yaml> --seed <int> --out <dir>
vt-metrics --in <run_dir> --metrics NLIS CRM
```

**Python**
```python
from verbaterra import VSIONSimulator, SimulationConfig, compute_nlis, ICLHFModel
df = VSIONSimulator(SimulationConfig(seed=7)).run()
nlis = compute_nlis(df)
model = ICLHFModel(seed=7).fit(df)
```

**Docs**
```bash
mkdocs serve   # preview
mkdocs build   # static site
```

---

### You’re ready.
If you need a **one‑click seed project** or a **GitHub Actions‑friendly release flow**, ask for the “Codex Orchestration Prompt” and branch protection policies.

