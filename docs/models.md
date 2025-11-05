# Models

## ICLHFModel — Inter-Cultural Linguistic Harmony Forecasting

- Fits paired linear regressors for lexical_diversity and syntax_complexity.
- Requires the dataset schema validated by `verbaterra.dataio.validate_frame`.
- Guards against usage prior to `.fit()` and raises clear errors for missing columns.

### Usage

```python
from verbaterra import ICLHFModel, VSIONSimulator

sim = VSIONSimulator(seed=7)
df = sim.run()
model = ICLHFModel().fit(df)
print(model.summary())
```
