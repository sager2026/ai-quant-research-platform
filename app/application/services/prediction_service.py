import pandas as pd

from app.domain.entities.prediction_result import PredictionResult
from app.domain.ml.interfaces.ml_model import MLModel


class PredictionService:
    """Application service coordinating price prediction."""

    def __init__(self, model: MLModel) -> None:
        self.model = model

    def predict(
        self,
        prices: pd.Series,
        forecast_horizon: int = 1,
    ) -> PredictionResult:
        return self.model.fit_predict(
            prices=prices,
            forecast_horizon=forecast_horizon,
        )