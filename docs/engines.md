# Simulation Engines

VerbaTerra bundles three engines representing distinct cultural dynamics.
Each engine emits the canonical feature columns (`ritual`, `trade`,
`symbolism`, `hierarchy`, `lexical_diversity`, `syntax_complexity`) plus
engine-specific diagnostics.

## vSION — Adaptive Civilization Simulator

- **Focus:** Interplay between trade, symbolism, and ritual.
- **Configuration file:** `src/verbaterra/engines/vsion/configs/default.yaml`
- **CLI usage:** `vt-sim --engine vsion --out runs/run_vsion`
- **Extra columns:** `adaptive_pressure`

## CCH — Cultural–Cognitive Heuristic Engine

- **Focus:** Ritual diffusion and hierarchy balance.
- **Configuration file:** `src/verbaterra/engines/cch/configs/default.yaml`
- **CLI usage:** `vt-sim --engine cch --out runs/run_cch`
- **Extra columns:** `collective_memory`, `diffusion_rate`

## NΦRA — Neuromorphic Φ-Resonance Analyzer

- **Focus:** Oscillatory coherence, resonance, and neuroplastic adaptation.
- **Configuration file:** `src/verbaterra/engines/nphra/configs/default.yaml`
- **CLI usage:** `vt-sim --engine nphra --out runs/run_nphra`
- **Extra columns:** `resonance_wave`, `neuro_coherence`

## Configuration schema

All configuration files share the following structure:

```yaml
n: <int>                 # number of records to generate
<engine-specific keys>:  # parameters controlling variance and bias
```

Override any value via the `--config` flag when invoking `vt-sim`. The CLI
merges overrides with the default configuration bundled with each engine.

## Lab demos

Each engine exposes a quick lab script for exploratory analysis:

```bash
python -m verbaterra.engines.vsion.lab_demo
python -m verbaterra.engines.cch.lab_demo
python -m verbaterra.engines.nphra.lab_demo
```

The lab outputs summarise NLIS/CRM behaviour and key diagnostics for rapid
comparison.
