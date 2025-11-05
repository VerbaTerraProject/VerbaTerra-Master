# ICLHF — Integrated Cultural–Linguistic Heuristic Framework

**Purpose.** Model directional influence of cultural drivers on linguistic outcomes.

**Cultural drivers (X):**
- `ritual` — stability, repetitive structure
- `trade` — openness, intergroup exchange
- `symbolism` — figurative density, mythopoesis
- `hierarchy` — power distance, role stratification

**Linguistic outcomes (Y):**
- `lexical_diversity` — vocabulary breadth adjusted for sample size
- `syntax_complexity` — structural depth/branching

**Baseline specification.**
- Separate linear estimators for Y₁ and Y₂:
  - `lexical_diversity ~ ritual + trade + symbolism - hierarchy + ε`
  - `syntax_complexity ~ ritual + hierarchy + trade + symbolism + ε`
- Extensions: interactions (e.g., `trade×symbolism`), nonlinearity (splines), mixed effects (region/time).

**Interpretation.** Trade & symbolism tend to expand vocabularies; hierarchy can suppress lexical spread but increase syntactic convention; ritual stabilizes both via repetition and patterning.
