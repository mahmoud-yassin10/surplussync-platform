from pathlib import Path

from surplussync_ml.data.synthetic import generate
from surplussync_ml.modeling.train import train


def test_training_writes_artifacts(tmp_path: Path) -> None:
    data_path = tmp_path / "data.csv"
    generate().to_csv(data_path, index=False)
    output = tmp_path / "models"
    metadata = train(data_path, output)
    assert (output / "attendance_point.cbm").exists()
    assert (output / "attendance_q10.cbm").exists()
    assert (output / "attendance_q90.cbm").exists()
    assert metadata["metrics"]["mae"] >= 0
