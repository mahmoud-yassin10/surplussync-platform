# Synthetic Data

The prototype does not use private student-level data. It uses a synthetic business-day dataset covering August 2023 through June 2026.

The generator models weekday patterns, exams, field trips, early dismissal, assemblies, sports absences, weather, menu popularity, recent attendance trends, and random attendance noise. The canonical 2026-03-12 fixture is explicitly inserted so demos, tests, screenshots, and narration remain reproducible.

Synthetic data was used to build a public hackathon prototype without exposing student records or requiring district data access.

Limitations:

- Synthetic patterns may not match a real district.
- Calibration is not proven in real deployment.
- Severe weather, closures, menu substitutions, and stale event feeds can cause distribution shift.

Path to deployment: replace synthetic rows with approved historical cafeteria participation records, validate against local baselines, monitor drift, and keep human review mandatory.
