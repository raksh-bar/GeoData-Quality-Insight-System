import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from validation import add_quality_flags, check_required_columns


def test_quality_flags_detect_multiple_issues():
    df = pd.DataFrame({
        "place_id": [1, 2], "place_name": ["A", "A"], "city": ["X", "X"],
        "latitude": [100, 100], "longitude": [20, 20],
        "normal_eta_min": [10, 10], "actual_eta_min": [50, 10],
    })
    result = add_quality_flags(df)
    assert "Invalid coordinates" in result.loc[0, "defect_type"]
    assert "Excessive ETA delay" in result.loc[0, "defect_type"]
    assert result.loc[0, "severity"] == "Critical"


def test_required_column_check_reports_missing_column():
    df = pd.DataFrame({"place_id": [1]})
    try:
        check_required_columns(df)
    except ValueError as error:
        assert "place_name" in str(error)
    else:
        raise AssertionError("Expected a ValueError")
