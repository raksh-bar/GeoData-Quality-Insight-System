"""Run the full Map Data Quality & Anomaly Detection System."""

from pathlib import Path
import argparse
import sys

import pandas as pd

from analysis import create_summary, defects_by_city
from anomaly_detection import defective_records, duplicate_records, eta_anomalies
from data_cleaning import clean_data
from report_generator import create_city_chart, create_excel_report
from validation import add_quality_flags, check_required_columns


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check map data for quality issues.")
    parser.add_argument(
        "--input", type=Path, default=PROJECT_ROOT / "data" / "map_data.csv",
        help="CSV file to analyse (default: data/map_data.csv)",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=PROJECT_ROOT,
        help="Folder in which reports/ and charts/ are created (default: project folder)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    input_file = args.input.resolve()
    if not input_file.is_file():
        print(f"Error: CSV file not found: {input_file}")
        return 1

    try:
        raw_data = pd.read_csv(input_file)
        check_required_columns(raw_data)
        analysed_data = add_quality_flags(clean_data(raw_data))
    except (OSError, ValueError, pd.errors.ParserError) as error:
        print(f"Error: {error}")
        return 1

    summary = create_summary(analysed_data)
    city_summary = defects_by_city(analysed_data)
    output_dir = args.output_dir.resolve()
    report_file = output_dir / "reports" / "map_quality_report.xlsx"
    chart_file = output_dir / "charts" / "anomaly_by_city.png"

    create_excel_report(
        analysed_data, summary, city_summary, duplicate_records(analysed_data),
        eta_anomalies(analysed_data), report_file,
    )
    if not city_summary.empty:
        create_city_chart(city_summary, chart_file)

    print("Analysis completed successfully.\n")
    for metric, value in summary.items():
        print(f"{metric}: {value}")
    print(f"\nExcel report: {report_file}")
    if not city_summary.empty:
        print(f"Chart: {chart_file}")
    print(f"Defective-record view contains {len(defective_records(analysed_data))} record(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
