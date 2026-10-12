from __future__ import annotations

import pandas as pd


def build_condition_a_prompt(origin_date: str, target_month: str, history_df: pd.DataFrame) -> str:
    history_df = history_df.copy()
    history_df["date"] = pd.to_datetime(history_df["date"])
    lines = [
        "You are a macroeconomic forecaster.",
        "Task: nowcast the CPI-U year-over-year inflation rate for the target month.",
        f"Forecast origin: {origin_date}",
        f"Target month: {target_month}",
        "Historical data:",
    ]
    for _, row in history_df.tail(12).iterrows():
        lines.append(f"- {row['date'].strftime('%Y-%m-%d')}: CPIAUCNS={row['cpiaucns']}")

    lines.append("Return a single numeric percentage value for the target month.")
    return "\n".join(lines)


def build_condition_b_prompt(origin_date: str, target_month: str, history_df: pd.DataFrame, indicators: dict) -> str:
    prompt = build_condition_a_prompt(origin_date, target_month, history_df)
    prompt += "\nAdditional structured economics after origin:\n"
    for key, value in indicators.items():
        if isinstance(value, dict):
            prompt += f"- {key}: {value.get('value', '')} (released {value.get('release_date', 'unknown')})\n"
        else:
            prompt += f"- {key}: {value}\n"
    prompt += "Do not include the target CPI value itself."
    return prompt


def validate_condition_a_exclusions(prompt: str, target_value: float | None) -> None:
    if target_value is not None:
        if str(target_value) in prompt:
            raise ValueError("Condition A prompt leaked a target value")


def validate_condition_b_post_origin_only(indicators: dict, origin_date: str) -> None:
    for key, value in indicators.items():
        if isinstance(value, dict):
            release_date = value.get("release_date")
            if release_date is not None and release_date <= origin_date:
                raise ValueError(f"Indicator {key} is not post-origin: {release_date} <= {origin_date}")


__all__ = [
    "build_condition_a_prompt",
    "build_condition_b_prompt",
    "validate_condition_a_exclusions",
    "validate_condition_b_post_origin_only",
]
