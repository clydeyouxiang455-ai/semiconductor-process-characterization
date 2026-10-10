from pathlib import Path
from src.data_loader import load_secom, validate_secom


def test_loads_source_shaped_files(tmp_path: Path):
    (tmp_path / "secom.data").write_text("1 NaN 3\n4 5 6\n")
    (tmp_path / "secom_labels.data").write_text('-1 "19/07/2008 11:55:00"\n1 "20/07/2008 12:00:00"\n')
    features, labels = load_secom(tmp_path)
    checks = validate_secom(features, labels)
    assert features.shape == (2, 3)
    assert checks["row_alignment"] is True
    assert checks["observed_labels"] == [-1, 1]
