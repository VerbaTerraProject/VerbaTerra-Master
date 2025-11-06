# Metrics Reference

## NLIS – Narrative Linguistic Integration Score

NLIS is a weighted combination of the four cultural parameters. Values are normalised between 0 and 1.

```
NLIS = w1 * ritual + w2 * trade + w3 * symbolism + w4 * hierarchy
```

Default weights: `w1=0.3`, `w2=0.25`, `w3=0.25`, `w4=0.2`.

## CRM – Cultural Resonance Metric

CRM highlights diversity, multilinguality, and hybridity influences. Values are also normalised between 0 and 1.

```
CRM = α * diversity + β * multilinguality + γ * hybridity
```

Default coefficients: `α=0.4`, `β=0.35`, `γ=0.25`.

## Usage

The Analyst engine computes both metrics per record. Charts reveal correlations and distributions, while the vSION and NΦRA engines surface similar parameters for qualitative exploration.
