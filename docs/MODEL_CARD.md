# Model Card

## Intended Use

Estimate school meal participation for operational preparation planning in the SurplusSync Plus prototype.

## Prohibited Use

Do not use this model for autonomous meal denial, student-level decisions, production staffing, audited financial reporting, or unsupervised partner commitments.

## Model Family

Three CatBoost regressors:

- point attendance estimate
- q10 attendance estimate
- q90 attendance estimate

## Training Data

The current dataset is synthetic and covers business days from August 2023 to June 2026. The canonical demo date is explicitly inserted for reproducibility. No private student-level data is used.

## Features

Weekday, month, week of year, enrolled students, eligible students, normal preparation, expected attendance input, exams, field trips, early dismissal, assemblies, sports absences, rain probability, rain amount, temperature, menu name, menu popularity, recent 7-day attendance, and recent 14-day attendance.

## Target

Actual attendance / meal participation.

## Evaluation

Synthetic holdout metrics:

- training rows: 551
- test rows: 138
- MAE: about 13.84 students
- RMSE: about 19.71
- R2: about 0.619
- approximate 80% interval coverage: 78.99%
- mean interval width: about 42.23
- weekday-only baseline MAE: about 24.50

These are synthetic-data metrics, not real Chicago school performance.

## Recommendation Policy

The general policy uses the maximum of point prediction plus 20 meals and upper uncertainty bound plus a 5-meal safety buffer, subject to safety floor and eligibility cap.

## Canonical Fixture

The official demo values are deterministic and contract-locked: baseline attendance 528, interval 497-557, prep 562; corrected attendance 540, interval 512-568, prep 575.

## Limitations

Training data is synthetic, shortage probability is heuristic for general predictions, and the preparation policy is safety-oriented rather than a full newsvendor optimizer. Deployment would require real historical data, monitoring, drift detection, human review, and district-specific validation.
