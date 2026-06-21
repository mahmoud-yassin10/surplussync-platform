# Synthetic data schema

Each row is one school day.

| Field | Type | Meaning |
|---|---:|---|
| `date` | date | ISO school day |
| `school_id` | string | School identifier |
| `enrolled` | int | Total enrollment |
| `eligible` | int | Meal-eligible students |
| `normal_prep` | int | Existing default preparation plan |
| `weekday` | string | Monday-Friday |
| `month` | int | Calendar month |
| `week_of_year` | int | ISO week |
| `is_exam` | int | Exam schedule flag |
| `trip_students` | int | Students expected off-campus |
| `early_dismissal` | int | Early dismissal flag |
| `assembly_students` | int | Students affected by assembly |
| `sports_students` | int | Students affected by sports travel |
| `rain_probability` | float | 0-1 precipitation probability |
| `rain_inches` | float | Expected rainfall |
| `temperature_f` | float | Temperature |
| `menu_name` | string | Entrée/menu family |
| `menu_popularity` | float | Historical relative participation |
| `recent_attendance_7d` | float | Trailing attendance feature |
| `recent_attendance_14d` | float | Trailing attendance feature |
| `expected_attendance` | int | Pre-day operational expectation |
| `actual_attendance` | int | Model target |
| `prepared_meals` | int | Meals prepared |
| `served_meals` | int | Meals served |
| `recoverable_surplus` | int | Safe recoverable surplus |
| `nonrecoverable_surplus` | int | Nonrecoverable surplus |

Synthetic rows are clearly labeled and must not be presented as observed district records.
The generator fixes its random seed and injects the canonical demo row exactly once.
