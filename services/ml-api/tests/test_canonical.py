from datetime import date

from surplussync_ml.canonical import canonical_forecast


def test_canonical_contract_is_locked() -> None:
    result = canonical_forecast()
    assert result.date == date(2026, 3, 12)
    assert result.expectedAttendance == 528
    assert result.intervalLow == 497
    assert result.intervalHigh == 557
    assert result.recommendedPrep == 562
    assert result.preventableSurplus == 168
    assert result.shortageProb == 0.041
    assert result.approvalRequired is True
    assert result.decisionStatus == "PROPOSED"
