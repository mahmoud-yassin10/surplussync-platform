# Model card — baseline attendance forecast

## Intended use

Estimate school-day meal participation so cafeteria staff can review a safer preparation plan and
identify likely preventable surplus.

## Model

Three CatBoost regressors: point estimate, 10th percentile, and 90th percentile. Categorical
features are passed natively. Evaluation is time ordered to avoid future leakage.

## Not intended for

- autonomous ordering or disposal decisions;
- food-safety or donation eligibility decisions;
- punitive attendance decisions;
- claims about real Chicago Public Schools performance;
- replacing cafeteria managers or school administrators.

## Data

The current baseline uses reproducible synthetic data plus one explicit canonical demonstration
fixture. It is not trained on private student-level data.

## Metrics

The training script records MAE, RMSE, R², interval coverage, and mean interval width. The model
must be compared with a weekday rolling-mean baseline before any accuracy claim is made.

## Known limitations

Synthetic relationships can make performance look stronger than real deployment. Event feeds may
be missing or stale. Severe weather, closures, menu substitutions, and last-minute attendance
corrections can produce distribution shift. Human review is mandatory.
