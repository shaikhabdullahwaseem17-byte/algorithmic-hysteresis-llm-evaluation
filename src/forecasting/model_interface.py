from __future__ import annotations

import math
from typing import Iterable


def mae(forecast_values: Iterable[float], actual_values: Iterable[float]) -> float:
    forecast = list(forecast_values)
    actual = list(actual_values)
    if len(forecast) != len(actual):
        raise ValueError("Forecast and actual arrays must have the same length")
    if len(forecast) == 0:
        raise ValueError("Empty forecast series")
    return sum(abs(float(f) - float(a)) for f, a in zip(forecast, actual)) / len(forecast)


def rmse(forecast_values: Iterable[float], actual_values: Iterable[float]) -> float:
    forecast = list(forecast_values)
    actual = list(actual_values)
    if len(forecast) != len(actual):
        raise ValueError("Forecast and actual arrays must have the same length")
    if len(forecast) == 0:
        raise ValueError("Empty forecast series")
    sq = sum((float(f) - float(a)) ** 2 for f, a in zip(forecast, actual))
    return math.sqrt(sq / len(forecast))


def forecast_revision(condition_b_forecasts: Iterable[float], condition_a_forecasts: Iterable[float]) -> list[float]:
    b = list(condition_b_forecasts)
    a = list(condition_a_forecasts)
    if len(b) != len(a):
        raise ValueError("Condition B and A forecast arrays must have the same length")
    return [float(y) - float(x) for x, y in zip(a, b)]


def mean_revision(revisions: Iterable[float]) -> float:
    revs = list(revisions)
    if not revs:
        raise ValueError("Revision series is empty")
    return sum(float(x) for x in revs) / len(revs)


__all__ = ["mae", "rmse", "forecast_revision", "mean_revision"]
