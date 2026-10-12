from __future__ import annotations

import pandas as pd

from src.data.cpi_loader import build_historical_vintage_dataframe, ensure_post_origin_indicator_is_after_origin
from src.data.validation import validate_no_future_leakage, validate_post_origin_indicator, validate_release_date_vs_origin


def test_validate_no_future_leakage_rejects_data_after_origin():
    df = pd.DataFrame({
        "date": ["2023-12-31", "2024-01-31"],
        "cpiaucns": [300.0, 301.0],
    })
    try:
        validate_no_future_leakage(df, "2024-01-31", "2024-02-29")
        assert False, "Expected future leakage detection"
    except ValueError:
        pass


def test_historical_vintage_data_is_capped_at_origin():
    df = pd.DataFrame({
        "date": ["2023-11-30", "2023-12-31", "2024-01-31"],
        "cpiaucns": [299.0, 300.0, 301.0],
    })
    result = build_historical_vintage_dataframe(df, "2024-01-31")
    assert set(result["date"]) == {pd.Timestamp("2023-11-30"), pd.Timestamp("2023-12-31"), pd.Timestamp("2024-01-31")}


def test_validate_release_date_vs_origin_requires_post_release_timing():
    try:
        validate_release_date_vs_origin("2024-01-31", "2024-01-31")
        assert False, "Expected release date to be after origin"
    except ValueError:
        pass


def test_validate_post_origin_indicator_requires_after_origin():
    try:
        validate_post_origin_indicator("2024-01-31", "2024-01-31")
        assert False, "Expected indicator to be after origin"
    except ValueError:
        pass

    assert ensure_post_origin_indicator_is_after_origin("2024-02-01", "2024-01-31") is True
