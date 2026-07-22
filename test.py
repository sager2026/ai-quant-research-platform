from app.application.services.prediction_service import PredictionService
from app.infrastructure.market_data.yahoo_repository import YahooRepository
from app.infrastructure.ml.lstm_model import LSTMModel
from app.infrastructure.ml.transformer_model import TransformerModel


repository = YahooRepository()
history = repository.get_history("AAPL")
prices = history["Close"]

models = {
    "LSTM": LSTMModel(
        sequence_length=30,
        hidden_size=32,
        epochs=100,
        random_seed=42,
    ),
    "Transformer": TransformerModel(
        sequence_length=30,
        d_model=32,
        nhead=4,
        num_layers=2,
        dim_feedforward=64,
        dropout=0.1,
        epochs=100,
        random_seed=42,
    ),
}

for model_name, model in models.items():
    service = PredictionService(model=model)
    result = service.predict(prices, forecast_horizon=1)

    improvement = (
        result.baseline_rmse - result.validation_rmse
    ) / result.baseline_rmse

    print("=" * 50)
    print(f"Model: {model_name}")
    print(f"Predicted return: {result.predicted_return:.2%}")
    print(f"Direction: {result.direction}")
    print(f"Validation RMSE: {result.validation_rmse:.4f}")
    print(f"Validation MAE: {result.validation_mae:.4f}")
    print(f"Baseline RMSE: {result.baseline_rmse:.4f}")
    print(f"Improvement: {improvement:.2%}")
    print(f"Beats baseline: {result.beats_baseline}")