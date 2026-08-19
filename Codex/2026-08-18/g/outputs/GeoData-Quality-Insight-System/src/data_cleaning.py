"""Small, safe cleaning steps used before validation."""

import pandas as pd


TEXT_COLUMNS = ["place_name", "city", "category", "traffic_level"]
NUMERIC_COLUMNS = [
    "latitude", "longitude", "distance_km", "normal_eta_min", "actual_eta_min"
]


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with tidy text and correctly typed number columns."""
    cleaned = df.copy()

    for column in TEXT_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].astype("string").str.strip()

    for column in NUMERIC_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    return cleaned
