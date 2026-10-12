from __future__ import annotations

import pandas as pd

from src.data.cpi_loader import compute_yoy_from_index, standardize_cpi_dataframe


def test_standardize_cpi_dataframe_handles_date_and_numeric_values():
    df = pd.DataFrame({
        "date": ["2023-01-31", "2023-02-28", "2023-03-31"],
        "cpiaucns": [300.0, 301.5, 303.0],
    })
    result = standardize_cpi_dataframe(df)
    assert list(result.columns) == ["date", "cpiaucns"]
    assert result["date"].dtype.kind == "M"
    assert result["cpiaucns"].dtype.kind in {"f", "i"}


def test_compute_yoy_from_index_uses_twelve_month_comparison():
    df = pd.DataFrame({
        "date": pd.date_range("2022-01-31", periods=15, freq="M"),
        "cpiaucns": [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 110.0, 111.0, 112.0, 113.0, 114.0, 115.0, 116.0, 117.0],
    })
    result = compute_yoy_from_index(df, target_month="2023-01-31")
    assert abs(result - 17.0) < 1e-9


def test_compute_yoy_target_month_must_exist():
    df = pd.DataFrame({
        "date": pd.date_range("2022-01-31", periods=3, freq="M"),
        "cpiaucns": [100.0, 101.0, 102.0],
    })
    try:
        compute_yoy_from_index(df, target_month="2024-01-31")
        assert False, "Expected a ValueError for missing target month"
    except ValueError:
        pass
