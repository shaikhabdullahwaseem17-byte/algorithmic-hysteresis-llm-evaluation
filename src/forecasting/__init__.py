from __future__ import annotations

import pandas as pd


def validate_cpi_dataset(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        raise ValueError("CPI dataset is empty")

    normalized = df.copy()
    if "date" not in normalized.columns:
        raise ValueError("CPI data must include a 'date' column")
    if "cpiaucns" not in normalized.columns:
        raise ValueError("CPI data must include a 'cpiaucns' column")

    normalized["date"] = pd.to_datetime(normalized["date"])
    if normalized["date"].duplicated().any():
        raise ValueError("CPI dataset contains duplicate dates")
    if normalized["date"].isna().any():
        raise ValueError("CPI dataset contains null dates")
    if normalized["cpiaucns"].isna().any():
        raise ValueError("CPI dataset contains missing CPI values")

    return normalized.sort_values("date").reset_index(drop=True)


def validate_no_future_leakage(history_df: pd.DataFrame, origin_date: pd.Timestamp | str, target_month: pd.Timestamp | str) -> None:
    origin = pd.Timestamp(origin_date)
    target = pd.Timestamp(target_month)
    if history_df.empty:
        return

    normalized = validate_cpi_dataset(history_df)
    future_dates = normalized[normalized["date"] > origin]
    if not future_dates.empty:
        raise ValueError(f"Future data leaked past origin date: earliest future date {future_dates['date'].min().date()}")

    if target in normalized["date"].values:
        raise ValueError(f"Target month {target.date()} appears in historical input data; this is not allowed")


def validate_release_date_vs_origin(origin_date: pd.Timestamp | str, release_date: pd.Timestamp | str) -> None:
    origin = pd.Timestamp(origin_date)
    release = pd.Timestamp(release_date)
    if release <= origin:
        raise ValueError(f"Release date {release.date()} must be after the forecast origin {origin.date()}")


def validate_target_value_separation(history_df: pd.DataFrame, target_value: float | None) -> None:
    if target_value is None:
        return
    if target_value in history_df["cpiaucns"].astype(float).values:
        raise ValueError("Target value appears in historical input data; this is not permitted")


def validate_post_origin_indicator(indicator_date: pd.Timestamp | str, origin_date: pd.Timestamp | str) -> None:
    indicator = pd.Timestamp(indicator_date)
    origin = pd.Timestamp(origin_date)
    if indicator <= origin:
        raise ValueError(
            f"Indicator availability {indicator.date()} must be after the nowcast origin {origin.date()} "
            "to qualify as post-origin information."
        )


def validate_vintage_data(vintage_df: pd.DataFrame, origin_date: pd.Timestamp | str) -> pd.DataFrame:
    origin = pd.Timestamp(origin_date)
    normalized = validate_cpi_dataset(vintage_df)
    max_date = normalized["date"].max()
    if max_date > origin:
        raise ValueError(f"Vintage data includes values after origin ({origin.date()}); max observed date {max_date.date()}")
    return normalized


__all__ = [
    "validate_cpi_dataset",
    "validate_no_future_leakage",
    "validate_release_date_vs_origin",
    "validate_target_value_separation",
    "validate_post_origin_indicator",
    "validate_vintage_data",
]
