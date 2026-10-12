from __future__ import annotations

import pandas as pd

from src.forecasting.baselines import random_walk_baseline_forecast
from src.forecasting.metrics import mae, rmse, forecast_revision, mean_revision


def test_random_walk_baseline_uses_previous_month_yoy():
    df = pd.DataFrame({
        "date": pd.date_range("2022-01-31", periods=13, freq="M"),
        "cpiaucns": [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0, 112.0],
    })
    result = random_walk_baseline_forecast(df, "2023-01-31")
    assert abs(result - 12.0) < 1e-9


def test_mae_and_rmse_are_calculated_in_percentage_points():
    forecast = [2.0, 3.0, 5.0]
    actual = [1.0, 4.0, 4.0]
    assert abs(mae(forecast, actual) - 1.0) < 1e-9
    assert abs(rmse(forecast, actual) - 1.0) < 1e-9


def test_forecast_revision_and_mean_revision():
    a = [2.0, 2.0, 2.0]
    b = [2.5, 2.0, 3.0]
    revisions = forecast_revision(b, a)
    assert revisions == [0.5, 0.0, 1.0]
    assert abs(mean_revision(revisions) - 0.5) < 1e-9
