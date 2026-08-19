"""Convenient filtered views of detected quality issues."""

import pandas as pd


def defective_records(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["defect_type"] != "Valid"].copy()


def duplicate_records(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["defect_type"].str.contains("Potential duplicate", na=False)].copy()


def eta_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    return df[
        df["defect_type"].str.contains("Invalid normal ETA|Excessive ETA delay", na=False)
    ].copy()
