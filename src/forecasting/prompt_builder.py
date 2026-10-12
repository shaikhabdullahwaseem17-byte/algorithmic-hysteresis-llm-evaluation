from __future__ import annotations

from abc import ABC, abstractmethod


class ForecastingModel(ABC):
    @abstractmethod
    def forecast(self, prompt: str) -> str:
        raise NotImplementedError


class MockModel(ForecastingModel):
    """A deterministic mock model used only for pipeline validation."""

    def __init__(self, default_value: float = 2.5):
        self.default_value = float(default_value)

    def forecast(self, prompt: str) -> str:
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt must be a non-empty string")
        return str(self.default_value)


class DummyModel(ForecastingModel):
    def forecast(self, prompt: str) -> str:
        return "2.5"


__all__ = ["ForecastingModel", "MockModel", "DummyModel"]
