# Map Data Quality & Anomaly Detection System

A Python portfolio project that checks map/location CSV data for common quality problems and produces an Excel report plus a chart.

## What it checks

- Missing location fields
- Invalid latitude (must be between -90 and 90)
- Invalid longitude (must be between -180 and 180)
- Potential duplicate locations
- Zero, negative, or missing normal ETA values
- ETA delays over 30 minutes

Each record receives a `defect_type` and a severity: `Valid`, `Medium`, `High`, or `Critical`. Records with several problems keep every issue label.

## Project structure

```text
Map-Data-Quality-Project/
├── data/                 # Input CSV files
│   └── map_data.csv       # Included sample data
├── src/                  # Application code
├── tests/                # Basic validation tests
├── reports/              # Generated Excel reports
├── charts/               # Generated PNG charts
├── requirements.txt
└── README.md
```

## Installation and first run (Windows)

1. Install [Python](https://www.python.org/downloads/) and make sure **Add Python to PATH** is selected.
2. Open PowerShell or the VS Code terminal inside this project folder.
3. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked, run this command once in the current terminal, then repeat the activation command:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

4. Install the libraries:

```powershell
pip install -r requirements.txt
```

5. Run the analysis:

```powershell
python src/main.py
```

The program creates:

- `reports/map_quality_report.xlsx` — summary, all records, duplicates, and ETA anomalies
- `charts/anomaly_by_city.png` — number of defective records by city

## Use this with another CSV file

You can reuse this project for another map-data dataset without changing the source code.

### 1. Prepare the new file

Your CSV must contain these required columns:

```text
place_id, place_name, city, latitude, longitude, normal_eta_min, actual_eta_min
```

These optional columns are accepted and are included in the output when present:

```text
category, distance_km, traffic_level
```

Example:

```csv
place_id,place_name,city,latitude,longitude,normal_eta_min,actual_eta_min
101,Central Station,Pune,18.528,73.874,20,28
102,City Hospital,Pune,18.516,73.856,15,16
```

### 2. Run it against the new file

Place the file anywhere, then provide its path. Example when the file is in the `data` folder:

```powershell
python src/main.py --input data/my_new_data.csv
```

The new report replaces the default report. To keep its outputs separate, use `--output-dir`:

```powershell
python src/main.py --input data/my_new_data.csv --output-dir results/new_dataset
```

This creates:

```text
results/new_dataset/reports/map_quality_report.xlsx
results/new_dataset/charts/anomaly_by_city.png
```

### 3. Adapt it for a related project

For delivery, logistics, store-location, or travel datasets, keep the required columns and rename your source columns before saving the CSV. For example:

| Your column | Required name |
|---|---|
| `store_lat` | `latitude` |
| `store_lng` | `longitude` |
| `expected_minutes` | `normal_eta_min` |
| `observed_minutes` | `actual_eta_min` |

To add a new quality rule, edit `src/validation.py`, create a Boolean mask for the rule, then add it to `flags` and `severity_by_issue` in `add_quality_flags()`.

## What to ask a company for before analysing its data

When you receive a real company dataset, ask for a **CSV or Excel export**, a short **data dictionary** (meaning of every column), and the answers to these questions:

1. Which column uniquely identifies a place or record? (`place_id`)
2. Which columns give the place name, city, latitude, and longitude?
3. Are coordinates stored in standard decimal degrees (example: `22.5726`, `88.3639`)?
4. What do ETA columns mean, and are they always measured in minutes?
5. What period does the data cover, and how often is it updated?
6. Which errors matter most to the business: wrong location, duplicate place, delayed route, or missing data?
7. Are there privacy restrictions? Never upload customer names, phone numbers, emails, addresses, API keys, or confidential company data to a public GitHub repository.

The required input structure is in `data/company_data_template.csv`. Ask the company to provide these fields, or map/rename their equivalent fields to these names before running the project.

## Generate and analyse a large fictional company dataset

This repository includes a generator that makes realistic-looking but entirely fictional map-operations data. It is safe to use for practice and for a GitHub portfolio.

Generate 5,000 rows:

```powershell
python src/generate_demo_data.py --rows 5000
```

Analyse it and keep its outputs separate from the small sample report:

```powershell
python src/main.py --input data/company_map_operations_demo.csv --output-dir results/company_demo
```

The outputs will be saved under `results/company_demo/`. The data contains a small, intentional number of missing coordinates, invalid coordinates, duplicate locations, invalid ETAs, and excessive delays, just like quality problems that can appear in a real operational data feed.

## Run the tests

Install pytest once:

```powershell
pip install pytest
pytest
```

## Publish to GitHub

1. Create a new **public** GitHub repository named `Map-Data-Quality-Project`. Do not initialize it with a README.
2. In this project folder, run:

```powershell
git init
git add .
git commit -m "Build map data quality analysis system"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/Map-Data-Quality-Project.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub username.

For future changes:

```powershell
git add .
git commit -m "Describe your change"
git push
```

## Interview explanation

> I built a Python-based data quality system for map data. It reads a CSV file, identifies missing fields, invalid coordinates, duplicate locations, and ETA anomalies, then assigns a severity to each issue. The system produces an Excel report and a chart so non-technical users can quickly understand data quality problems.

## Technologies

Python, Pandas, Matplotlib, OpenPyXL
