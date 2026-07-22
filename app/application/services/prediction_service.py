from dataclasses import replace

import pandas as pd

from app.domain.entities.prediction_result import PredictionResult
from app.domain.forecast.interfaces.forecast_model import ForecastModel


class PredictionService:
    """Application service coordinating return forecasting."""

    def __init__(
        self,
        model: ForecastModel,
    ) -> None:
        self.model = model

    def predict(
        self,
        prices: pd.Series,
        forecast_horizon: int = 1,
    ) -> PredictionResult:
        result = self.model.fit_predict(
            prices=prices,
            forecast_horizon=forecast_horizon,
        )

        return replace(
            result,
            model_name=self._get_model_name(),
        )

    def _get_model_name(self) -> str:
        class_name = type(self.model).__name__

        if class_name.endswith("Model"):
            class_name = class_name[:-5]

        return class_name