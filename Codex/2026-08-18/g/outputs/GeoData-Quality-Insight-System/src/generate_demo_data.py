"""Create a realistic, fictional company-scale map operations CSV.

This generator uses no external data and intentionally introduces a small
number of quality issues so the main project has meaningful findings.
"""

from pathlib import Path
import argparse
import random

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOCATIONS = {
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Delhi": (28.6139, 77.2090),
    "Hyderabad": (17.3850, 78.4867),
    "Kolkata": (22.5726, 88.3639),
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
}
PLACE_TYPES = ["Airport", "Hospital", "Mall", "Metro Station", "Office", "School", "Warehouse"]
TRAFFIC_LEVELS = ["Low", "Medium", "High"]


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate fictional map operations data.")
    parser.add_argument("--rows", type=int, default=5000, help="Number of records (default: 5000)")
    parser.add_argument(
        "--output", type=Path,
        default=PROJECT_ROOT / "data" / "company_map_operations_demo.csv",
        help="CSV output path",
    )
    return parser.parse_args()


def create_records(row_count: int) -> pd.DataFrame:
    random.seed(42)  # Makes the demo repeatable for interview demonstrations.
    records = []
    for place_id in range(1, row_count + 1):
        city = random.choice(list(LOCATIONS))
        center_lat, center_lon = LOCATIONS[city]
        category = random.choice(PLACE_TYPES)
        traffic = random.choice(TRAFFIC_LEVELS)
        distance = round(random.uniform(1, 35), 2)
        normal_eta = max(5, round(distance * random.uniform(1.5, 2.5)))
        traffic_delay = {"Low": 0, "Medium": random.randint(2, 8), "High": random.randint(8, 22)}[traffic]
        records.append({
            "place_id": place_id,
            "place_name": f"{category} {place_id}",
            "city": city,
            "latitude": round(center_lat + random.uniform(-0.18, 0.18), 6),
            "longitude": round(center_lon + random.uniform(-0.18, 0.18), 6),
            "category": category,
            "distance_km": distance,
            "normal_eta_min": normal_eta,
            "actual_eta_min": normal_eta + traffic_delay,
            "traffic_level": traffic,
        })

    # Intentional imperfections simulate issues discovered in a vendor/company feed.
    for index in range(0, row_count, 211):
        records[index]["latitude"] = None
    for index in range(29, row_count, 257):
        records[index]["longitude"] = 230.0
    for index in range(47, row_count, 307):
        records[index]["normal_eta_min"] = 0
    for index in range(71, row_count, 389):
        records[index]["actual_eta_min"] = records[index]["normal_eta_min"] + 55
    for index in range(101, row_count, 503):
        records[index]["place_name"] = records[index - 1]["place_name"]
        records[index]["city"] = records[index - 1]["city"]
        records[index]["latitude"] = records[index - 1]["latitude"]
        records[index]["longitude"] = records[index - 1]["longitude"]

    return pd.DataFrame(records)


def main() -> None:
    args = parse_arguments()
    if args.rows < 1:
        raise ValueError("--rows must be at least 1")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    data = create_records(args.rows)
    data.to_csv(args.output, index=False)
    print(f"Created {len(data):,} fictional company records: {args.output}")


if __name__ == "__main__":
    main()
