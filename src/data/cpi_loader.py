from __future__ import annotations

import pandas as pd

from src.data.cpi_loader import compute_yoy_from_index, standardize_cpi_dataframe, bls_release_date_for_month
from src.data.validation import validate_cpi_dataset, validate_no_future_leakage, validate_release_date_vs_origin
from src.forecasting.baselines import random_walk_baseline_forecast
from src.forecasting.metrics import mae, rmse, forecast_revision


def build_synthetic_cpi_series(start: str = "2017-01-31", end: str = "2024-06-30") -> pd.DataFrame:
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    months = pd.date_range(start=start_ts, end=end_ts, freq="M")
    index_values = []
    value = 250.0
    for i, month in enumerate(months):
        if i > 0:
            value = value * (1 + (0.0025 + 0.003 * (i % 5) / 10))
        index_values.append(float(value))

    df = pd.DataFrame({"date": months, "cpiaucns": index_values})
    df = standardize_cpi_dataframe(df)
    return df


def build_mock_condition_records(cpi_df: pd.DataFrame, origins: list[pd.Timestamp]) -> list[dict]:
    records: list[dict] = []
    for origin in origins:
        target_month = origin
        target_release = bls_release_date_for_month(target_month)
        history_df = cpi_df[cpi_df["date"] <= origin].copy()
        validate_no_future_leakage(history_df, origin, target_month)

        # Use previous month as random-walk baseline
        base = random_walk_baseline_forecast(history_df, target_month)
        actual = None
        # If actual target exists in synthetic series, keep it for the same month if present.
        actual_match = cpi_df[cpi_df["date"] == target_month]
        if not actual_match.empty:
            actual = float(actual_match["cpiaucns"].iloc[0])
            actual_yoy = compute_yoy_from_index(cpi_df, target_month)
        else:
            actual = None
            actual_yoy = None

        records.append({
            "origin": origin.strftime("%Y-%m-%d"),
            "target_month": target_month.strftime("%Y-%m-%d"),
            "target_release_date": target_release.strftime("%Y-%m-%d"),
            "baseline_yoy": base,
            "actual_yoy": actual_yoy,
            "actual_index": actual,
            "cutoff_valid": True,
        })
    return records


def validate_sample(origins: list[pd.Timestamp], cpi_df: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    for origin in origins:
        target_month = origin
        history_df = cpi_df[cpi_df["date"] <= origin].copy()
        try:
            validate_no_future_leakage(history_df, origin, target_month)
        except ValueError as exc:
            issues.append(f"{origin.strftime('%Y-%m-%d')}: {exc}")

        if origin not in cpi_df["date"].to_list():
            # This is not a synthetic-data validation failure; we do not require origin row to exist.
            pass

    return issues


def mock_pipeline_report() -> dict:
    cpi_df = build_synthetic_cpi_series()
    origins = pd.date_range(start="2018-01-31", end="2024-06-30", freq="M")
    records = build_mock_condition_records(cpi_df, origins)
    valid = [r for r in records if r["actual_yoy"] is not None]

    actual_values = [r["actual_yoy"] for r in valid]
    baseline_values = [r["baseline_yoy"] for r in valid]
    report = {
        "records_total": len(records),
        "records_valid": len(valid),
        "baseline_mae": mae(baseline_values, actual_values),
        "baseline_rmse": rmse(baseline_values, actual_values),
        "origin_count": len(origins),
        "sample_issues": validate_sample(origins, cpi_df),
    }
    return report


__all__ = [
    "build_synthetic_cpi_series",
    "build_mock_condition_records",
    "validate_sample",
    "mock_pipeline_report",
    "ForecastOrigin",
    "generate_origin_schedule",
    "bls_release_date_for_month",
]
