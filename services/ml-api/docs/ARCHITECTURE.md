# Architecture

```text
Synthetic generator -> CSV -> feature builder -> CatBoost training
                                             -> model artifacts + metadata
Frontend -> FastAPI request validation -> canonical fixture or model inference
                                      -> Forecast-compatible response
```

## Boundaries

The service owns forecasting, uncertainty intervals, evidence factors, similar-day retrieval,
and preparation recommendations. It does not own authentication, partner messaging, recovery
eligibility, route execution, audit approvals, or impact-ledger writes.

## Forecast contract

The response mirrors the frontend `Forecast` type and adds machine-readable governance fields:
`approvalRequired`, `decisionStatus`, `safetyFloorApplied`, and `generatedAt`.

## Artifact strategy

- `attendance_point.cbm`: CatBoost RMSE model.
- `attendance_q10.cbm`: lower quantile model.
- `attendance_q90.cbm`: upper quantile model.
- `metadata.json`: metrics, feature list, categorical features, versions, and data window.

The canonical demo fixture is code-reviewed and immutable. It prevents model drift from changing
recorded demo narration while still allowing the judges to inspect a real trained pipeline.
