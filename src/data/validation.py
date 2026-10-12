from __future__ import annotations

import pandas as pd
from dateutil.relativedelta import relativedelta


CPI_SERIES_ID = "CPIAUCNS"


def standardize_cpi_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        raise ValueError("CPI dataframe must not be empty")

    required = {"date", "cpiaucns"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"CPI data missing required columns: {sorted(missing)}")

    normalized = df.copy()
    normalized["date"] = pd.to_datetime(normalized["date"])
    normalized = normalized.sort_values("date").drop_duplicates(subset="date", keep="last")
    normalized["cpiaucns"] = pd.to_numeric(normalized["cpiaucns"], errors="raise")
    normalized = normalized.reset_index(drop=True)
    return normalized


def infer_release_date_for_observation(obs_month: pd.Timestamp) -> pd.Timestamp:
    month_start = pd.Timestamp(year=obs_month.year, month=obs_month.month, day=1)
    next_month = month_start + relativedelta(months=1)
    weekday = next_month.weekday()
    first_friday_offset = (4 - weekday) % 7
    first_friday = next_month + pd.Timedelta(days=first_friday_offset)
    return first_friday + pd.Timedelta(days=7)


def compute_yoy_from_index(df: pd.DataFrame, target_month: pd.Timestamp | str | None = None, date_col: str = "date", value_col: str = "cpiaucns") -> float | pd.Series:
    normalized = standardize_cpi_dataframe(df)
    if target_month is not None:
        target_ts = pd.Timestamp(target_month)
        target_row = normalized[normalized[date_col] == target_ts]
        if target_row.empty:
            raise ValueError(f"Target month {target_ts} is not present in the CPI series")
        prior = normalized[normalized[date_col] == (target_ts - pd.DateOffset(months=12))]
        if prior.empty:
            raise ValueError(f"No 12-month comparison value present for target month {target_ts}")
        current = float(target_row[value_col].iloc[0])
        previous = float(prior[value_col].iloc[0])
        if previous == 0:
            raise ValueError("Cannot compute YoY inflation when previous value is zero")
        return ((current / previous) - 1.0) * 100.0

    result = pd.Series(index=normalized.index, dtype=float)
    for idx, row in normalized.iterrows():
        date_val = row[date_col]
        prior_match = normalized[normalized[date_col] == (date_val - pd.DateOffset(months=12))]
        if prior_match.empty:
            result.iloc[idx] = float("nan")
        else:
            current = float(row[value_col])
            previous = float(prior_match[value_col].iloc[0])
            if previous == 0:
                raise ValueError(f"Cannot compute YoY inflation because previous value at {date_val} is zero")
            result.iloc[idx] = ((current / previous) - 1.0) * 100.0
    return result


def build_historical_vintage_dataframe(df: pd.DataFrame, origin_date: pd.Timestamp) -> pd.DataFrame:
    normalized = standardize_cpi_dataframe(df)
    cutoff = pd.Timestamp(origin_date)
    eligible = normalized[normalized["date"] <= cutoff].copy()
    eligible["origin_date"] = cutoff
    eligible["historical_cutoff_ok"] = True
    return eligible


def ensure_post_origin_indicator_is_after_origin(indicator_date: pd.Timestamp | str, origin_date: pd.Timestamp | str) -> bool:
    actual_indicator = pd.Timestamp(indicator_date)
    actual_origin = pd.Timestamp(origin_date)
    return actual_indicator > actual_origin


__all__ = [
    "CPI_SERIES_ID",
    "standardize_cpi_dataframe",
    "infer_release_date_for_observation",
    "compute_yoy_from_index",
    "build_historical_vintage_dataframe",
    "ensure_post_origin_indicator_is_after_origin",
]
