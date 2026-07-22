from app.domain.forecast.interfaces.forecast_model import ForecastModel
from app.infrastructure.ml.lstm_model import LSTMModel
from app.infrastructure.ml.transformer_model import TransformerModel


class ForecastModelFactory:
    """Create forecasting-model implementations by name."""

    @staticmethod
    def create(model_name: str) -> ForecastModel:
        if not isinstance(model_name, str):
            raise TypeError("model_name must be a string.")

        normalized_name = model_name.strip().lower()

        if normalized_name == "lstm":
            return LSTMModel(
                sequence_length=30,
                hidden_size=32,
                num_layers=1,
                learning_rate=0.001,
                epochs=100,
                random_seed=42,
            )

        if normalized_name == "transformer":
            return TransformerModel(
                sequence_length=30,
                d_model=32,
                nhead=4,
                num_layers=2,
                dim_feedforward=64,
                dropout=0.1,
                learning_rate=0.0005,
                epochs=100,
                random_seed=42,
            )

        supported_models = "lstm, transformer"

        raise ValueError(
            f"Unsupported forecasting model: {model_name}. "
            f"Supported models: {supported_models}."
        )