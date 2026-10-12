from __future__ import annotations

import pandas as pd

from src.data.cpi_loader import compute_yoy_from_index


def random_walk_baseline_forecast(history_df: pd.DataFrame, target_month: pd.Timestamp | str) -> float:
    df = history_df.copy()
    if df.empty:
        raise ValueError("History is empty; cannot compute a random-walk baseline")

    df["date"] = pd.to_datetime(df["date"])
    target_ts = pd.Timestamp(target_month)
    prior_month = target_ts - pd.DateOffset(months=1)
    if prior_month not in df["date"].values:
        raise ValueError(f"History does not include the prior month {prior_month.date()} needed for random-walk baseline")

    previous_month = df[df["date"] == prior_month].iloc[0]
    current_m12 = df[df["date"] == (prior_month - pd.DateOffset(months=12))]
    if current_m12.empty:
        raise ValueError(f"12-month history is unavailable for {prior_month.date()}")

    value_prev = float(previous_month["cpiaucns"])
    value_prev_12 = float(current_m12["cpiaucns"].iloc[0])
    if value_prev_12 == 0:
        raise ValueError("Historical value for prior-year comparison is zero; cannot compute YoY")

    yoy = ((value_prev / value_prev_12) - 1.0) * 100.0
    return yoy


__all__ = ["random_walk_baseline_forecast"]
