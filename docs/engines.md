# Engines

## vSION (Vectorial Societal Integration Oscillation Network)

- `SimulationConfig` controls population size, distribution means/standard deviations, and lexical/syntax weightings.
- `VSIONSimulator` produces ritual, trade, symbolism, hierarchy, lexical_diversity, and syntax_complexity columns.
- Configurations can be loaded from YAML under `verbaterra/engines/vsion/configs` or constructed programmatically.

### Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `population` | Number of agents simulated | `200` |
| `noise_std` | Gaussian noise added to linguistic outputs | `5.0` |
| `lexical_weights` | Tuple for ritual, trade, symbolism, hierarchy, intercept | `(0.2, 0.3, 0.25, -0.1, 20.0)` |

## CCH (Core Cultural Heuristics)

Skeleton engine summarizing heuristic drift dynamics. Defaults exposed through `CCHConfig` with diffusion and cohesion controls.

## NΦRA (Civilization Lab V19)

NΦRA scaffolds long-horizon adaptation experiments. The `NPHRAConfig` dataclass communicates mutation and adaptation steps; see the [lab notebook](labs/civilization_lab_v19.md) for planned behaviors.
