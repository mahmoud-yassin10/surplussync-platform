from surplussync_ml.data.synthetic import generate


def test_generator_is_reproducible_and_contains_canonical_row() -> None:
    first = generate()
    second = generate()
    assert first.equals(second)
    row = first.loc[first["date"].astype(str) == "2026-03-12"].iloc[0]
    assert row["actual_attendance"] == 528
    assert row["trip_students"] == 112
    assert row["early_dismissal"] == 1
