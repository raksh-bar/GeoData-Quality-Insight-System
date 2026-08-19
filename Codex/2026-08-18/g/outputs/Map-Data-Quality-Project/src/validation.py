"""Rules for identifying map-data quality issues."""

import pandas as pd


REQUIRED_COLUMNS = {
    "place_id", "place_name", "city", "latitude", "longitude",
    "normal_eta_min", "actual_eta_min",
}


def check_required_columns(df: pd.DataFrame) -> None:
    """Raise a clear error when an input file lacks required columns."""
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            "Input CSV is missing required column(s): " + ", ".join(sorted(missing))
        )


def add_quality_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Add issue labels, severity, and ETA difference to every record.

    A record may have more than one issue. `defect_type` keeps all labels so
    the report does not hide data-quality problems.
    """
    result = df.copy()
    result["eta_difference_min"] = result["actual_eta_min"] - result["normal_eta_min"]

    duplicate_mask = result.duplicated(
        subset=["place_name", "city", "latitude", "longitude"], keep=False
    )
    missing_mask = result[["place_name", "city", "latitude", "longitude"]].isna().any(axis=1)
    invalid_coordinate_mask = (
        result["latitude"].notna()
        & ((result["latitude"] < -90) | (result["latitude"] > 90))
    ) | (
        result["longitude"].notna()
        & ((result["longitude"] < -180) | (result["longitude"] > 180))
    )
    invalid_eta_mask = result["normal_eta_min"].isna() | (result["normal_eta_min"] <= 0)
    excessive_delay_mask = result["eta_difference_min"] > 30

    flags = {
        "Missing data": missing_mask,
        "Invalid coordinates": invalid_coordinate_mask,
        "Potential duplicate": duplicate_mask,
        "Invalid normal ETA": invalid_eta_mask,
        "Excessive ETA delay": excessive_delay_mask,
    }
    severity_by_issue = {
        "Missing data": "High",
        "Invalid coordinates": "Critical",
        "Potential duplicate": "Medium",
        "Invalid normal ETA": "High",
        "Excessive ETA delay": "Medium",
    }
    severity_rank = {"Valid": 0, "Medium": 1, "High": 2, "Critical": 3}

    defect_types, severities = [], []
    for row_number in result.index:
        row_issues = [name for name, mask in flags.items() if bool(mask.loc[row_number])]
        if not row_issues:
            defect_types.append("Valid")
            severities.append("Valid")
            continue
        defect_types.append("; ".join(row_issues))
        severities.append(max((severity_by_issue[issue] for issue in row_issues), key=severity_rank.get))

    result["defect_type"] = defect_types
    result["severity"] = severities
    return result
