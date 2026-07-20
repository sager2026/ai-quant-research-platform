from abc import ABC, abstractmethod

import pandas as pd

from app.domain.entities.prediction_result import PredictionResult


class MLModel(ABC):
    """Interface implemented by all QuantMind forecasting models."""

    @abstractmethod
    def fit_predict(
        self,
        prices: pd.Series,
        forecast_horizon: int = 1,
    ) -> PredictionResult:
        """
        Train the model and produce a price forecast.

        Args:
            prices:
                Historical closing prices.

            forecast_horizon:
                Number of trading days represented by the forecast.

        Returns:
            Structured forecasting result.
        """
        raise NotImplementedError