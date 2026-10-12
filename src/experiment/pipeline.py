from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class ForecastOrigin:
    origin: pd.Timestamp
    target_month: pd.Timestamp
    target_release_date: pd.Timestamp
    target_value: float | None = None
    historical_cutoff: pd.Timestamp | None = None

    @property
    def origin_iso(self) -> str:
        return self.origin.strftime("%Y-%m-%d")


def generate_origin_schedule(start: str | pd.Timestamp, end: str | pd.Timestamp) -> list[ForecastOrigin]:
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    origins: list[ForecastOrigin] = []
    current = start_ts

    while current <= end_ts:
        month_end = current
        month_start = month_end.to_period("M").to_timestamp()
        target_month = month_end
        target_release = bls_release_date_for_month(month_end)
        origins.append(
            ForecastOrigin(
                origin=month_end,
                target_month=target_month,
                target_release_date=target_release,
                target_value=None,
                historical_cutoff=(month_end - pd.DateOffset(days=1)),
            )
        )
        current = current + pd.DateOffset(months=1)

    return origins


def bls_release_date_for_month(reference_month: pd.Timestamp) -> pd.Timestamp:
    month = reference_month.month
    year = reference_month.year
    next_month = pd.Timestamp(year=year, month=month, day=1) + pd.DateOffset(months=1)
    first_day = next_month
    weekday = first_day.weekday()  # Monday=0 ... Sunday=6
    first_friday_offset = (4 - weekday) % 7
    first_friday = first_day + pd.Timedelta(days=first_friday_offset)
    second_friday = first_friday + pd.Timedelta(days=7)
    return second_friday
