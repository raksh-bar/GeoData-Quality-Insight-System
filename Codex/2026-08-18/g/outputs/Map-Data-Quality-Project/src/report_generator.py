"""Excel and chart output for the project."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def create_excel_report(
    all_records: pd.DataFrame,
    summary: dict[str, object],
    city_summary: pd.DataFrame,
    duplicates: pd.DataFrame,
    eta_issues: pd.DataFrame,
    output_file: Path,
) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    summary_df = pd.DataFrame(summary.items(), columns=["Metric", "Value"])
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        all_records.to_excel(writer, sheet_name="All Records", index=False)
        city_summary.to_excel(writer, sheet_name="Defects by City", index=False)
        duplicates.to_excel(writer, sheet_name="Duplicates", index=False)
        eta_issues.to_excel(writer, sheet_name="ETA Anomalies", index=False)


def create_city_chart(city_summary: pd.DataFrame, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.bar(city_summary["city"].fillna("Unknown"), city_summary["defect_count"], color="#e76f51")
    plt.title("Map Data Defects by City")
    plt.xlabel("City")
    plt.ylabel("Number of defective records")
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()
