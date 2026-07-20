from dataclasses import dataclass


@dataclass
class PredictionResult:
    current_price: float
    predicted_price: float
    predicted_return: float
    forecast_horizon: int

    validation_loss: float
    validation_rmse: float
    validation_mae: float
    baseline_rmse: float

    @property
    def direction(self) -> str:
        threshold = 0.002  # 0.20%

        if self.predicted_return > threshold:
            return "Bullish"

        if self.predicted_return < -threshold:
            return "Bearish"

        return "Neutral"

    @property
    def beats_baseline(self) -> bool:
        return self.validation_rmse < self.baseline_rmse

    @property
    def improvement_over_baseline(self) -> float:
        if self.baseline_rmse == 0:
            return 0.0

        return (
            self.baseline_rmse - self.validation_rmse
        ) / self.baseline_rmse