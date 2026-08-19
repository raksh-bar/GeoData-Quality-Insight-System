"""Business-friendly summaries of validation results."""

import pandas as pd


def create_summary(df: pd.DataFrame) -> dict[str, object]:
    total = len(df)
    defective = int((df["defect_type"] != "Valid").sum())
    valid = total - defective
    quality = round((valid / total * 100), 2) if total else 0.0
    return {
        "Total records": total,
        "Valid records": valid,
        "Defective records": defective,
        "Data quality percentage": quality,
    }


def defects_by_city(df: pd.DataFrame) -> pd.DataFrame:
    defective = df[df["defect_type"] != "Valid"]
    return (
        defective.groupby("city", dropna=False)
        .size()
        .reset_index(name="defect_count")
        .sort_values("defect_count", ascending=False)
    )


def defects_by_type(df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for issue_list in df.loc[df["defect_type"] != "Valid", "defect_type"]:
        for issue in issue_list.split("; "):
            records.append(issue)
    return pd.Series(records, name="defect_type").value_counts().rename_axis("defect_type").reset_index(name="count")


def create_findings(summary: dict[str, object], city_summary: pd.DataFrame) -> list[dict[str, str]]:
    """Plain-English observations for the executive report."""
    findings = [{
        "Topic": "Overall data quality",
        "Finding": f"{summary['Data quality percentage']}% of records passed all configured quality checks.",
        "Why it matters": "Reliable map data improves routing, customer experience, and operational decisions.",
    }]
    if not city_summary.empty:
        top_city = city_summary.iloc[0]
        findings.append({
            "Topic": "Priority location",
            "Finding": f"{top_city['city']} has the highest number of defective records ({top_city['defect_count']}).",
            "Why it matters": "Review this city first to reduce the largest concentration of known issues.",
        })
    findings.append({
        "Topic": "Recommended next step",
        "Finding": "Correct critical coordinate errors before publishing or using the locations in routing.",
        "Why it matters": "Invalid coordinates can place a location in the wrong area or make it unusable.",
    })
    return findings
