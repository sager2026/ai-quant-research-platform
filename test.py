from app.application.services.prediction_service import PredictionService
from app.infrastructure.market_data.yahoo_repository import YahooRepository
from app.infrastructure.ml.lstm_model import LSTMModel


repository = YahooRepository()

history = repository.get_history("AAPL")

prices = history["Close"]

model = LSTMModel(
    sequence_length=30,
    hidden_size=32,
    epochs=100,
)

prediction_service = PredictionService(model)

result = prediction_service.predict(
    prices=prices,
    forecast_horizon=1,
)

print(result)
print()

print(f"Direction: {result.direction}")
print(f"Current price: {result.current_price:.2f}")
print(f"Predicted price: {result.predicted_price:.2f}")
print(f"Predicted return: {result.predicted_return:.2%}")
print(f"Validation loss: {result.validation_loss:.6f}")
print(f"Validation RMSE: {result.validation_rmse:.2f}")
print(f"Validation MAE: {result.validation_mae:.2f}")
print(f"Baseline RMSE: {result.baseline_rmse:.2f}")
print(f"Beats baseline: {result.beats_baseline}")

print(
    "Improvement over baseline: "
    f"{result.improvement_over_baseline:.2%}"
) 