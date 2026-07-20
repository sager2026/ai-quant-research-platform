import copy

import numpy as np
import pandas as pd
import torch
from torch import nn

from app.domain.entities.prediction_result import (
    PredictionResult,
)
from app.domain.ml.interfaces.ml_model import MLModel
from app.infrastructure.ml.feature_engineering import (
    FeatureEngineering,
)


class ReturnLSTMNetwork(nn.Module):
    """PyTorch LSTM network for daily-return forecasting."""

    def __init__(
        self,
        input_size: int = 1,
        hidden_size: int = 32,
        num_layers: int = 1,
    ) -> None:
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )

        self.output_layer = nn.Linear(
            hidden_size,
            1,
        )

    def forward(
        self,
        inputs: torch.Tensor,
    ) -> torch.Tensor:
        lstm_output, _ = self.lstm(inputs)

        final_time_step = lstm_output[:, -1, :]

        return self.output_layer(
            final_time_step
        )


class LSTMModel(MLModel):
    """
    Train an LSTM to forecast the next trading day's return.
    """

    def __init__(
        self,
        sequence_length: int = 30,
        hidden_size: int = 32,
        num_layers: int = 1,
        learning_rate: float = 0.001,
        epochs: int = 100,
        random_seed: int = 42,
    ) -> None:
        self.sequence_length = sequence_length
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.random_seed = random_seed

    def fit_predict(
        self,
        prices: pd.Series,
        forecast_horizon: int = 1,
    ) -> PredictionResult:
        """
        Train the LSTM and forecast the next daily return.
        """
        if not isinstance(prices, pd.Series):
            raise TypeError(
                "prices must be a pandas Series."
            )

        if forecast_horizon != 1:
            raise ValueError(
                "The current implementation supports "
                "forecast_horizon=1 only."
            )

        clean_prices = (
            prices
            .dropna()
            .astype(float)
        )

        if clean_prices.empty:
            raise ValueError(
                "prices cannot be empty."
            )

        self._set_random_seed()

        feature_engineering = FeatureEngineering(
            sequence_length=self.sequence_length,
        )

        dataset = feature_engineering.prepare(
            clean_prices
        )

        model = ReturnLSTMNetwork(
            input_size=1,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
        )

        loss_function = nn.MSELoss()

        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=self.learning_rate,
        )

        best_validation_loss = float("inf")

        best_state = copy.deepcopy(
            model.state_dict()
        )

        for _ in range(self.epochs):
            model.train()

            optimizer.zero_grad()

            train_prediction = model(
                dataset.x_train
            )

            train_loss = loss_function(
                train_prediction,
                dataset.y_train,
            )

            train_loss.backward()

            optimizer.step()

            model.eval()

            with torch.no_grad():
                validation_prediction = model(
                    dataset.x_validation
                )

                validation_loss = loss_function(
                    validation_prediction,
                    dataset.y_validation,
                ).item()

            if (
                validation_loss
                < best_validation_loss
            ):
                best_validation_loss = (
                    validation_loss
                )

                best_state = copy.deepcopy(
                    model.state_dict()
                )

        model.load_state_dict(
            best_state
        )

        model.eval()

        # Validation predictions in scaled-return units.
        with torch.no_grad():
            predicted_scaled_returns = model(
                dataset.x_validation
            ).cpu().numpy()

        actual_scaled_returns = (
            dataset.y_validation
            .cpu()
            .numpy()
        )

        # Convert scaled values back to actual daily returns.
        predicted_returns = (
            dataset.scaler.inverse_transform(
                predicted_scaled_returns
            )
            .reshape(-1)
        )

        actual_returns = (
            dataset.scaler.inverse_transform(
                actual_scaled_returns
            )
            .reshape(-1)
        )

        # Convert return forecasts into price forecasts.
        validation_predicted_prices = (
            dataset.validation_previous_prices
            * (1.0 + predicted_returns)
        )

        validation_actual_prices = (
            dataset.validation_actual_prices
        )

        validation_errors = (
            validation_predicted_prices
            - validation_actual_prices
        )

        validation_rmse = float(
            np.sqrt(
                np.mean(
                    validation_errors ** 2
                )
            )
        )

        validation_mae = float(
            np.mean(
                np.abs(
                    validation_errors
                )
            )
        )

        # Naive baseline:
        # next price equals the previous observed price,
        # equivalent to predicting a zero daily return.
        baseline_predicted_prices = (
            dataset.validation_previous_prices
        )

        baseline_errors = (
            baseline_predicted_prices
            - validation_actual_prices
        )

        baseline_rmse = float(
            np.sqrt(
                np.mean(
                    baseline_errors ** 2
                )
            )
        )

        # Forecast the next trading day's return.
        with torch.no_grad():
            scaled_return_prediction = model(
                dataset.last_sequence
            ).cpu().numpy()

        predicted_return = float(
            dataset.scaler.inverse_transform(
                scaled_return_prediction
            )[0, 0]
        )

        current_price = float(
            clean_prices.iloc[-1]
        )

        predicted_price = (
            current_price
            * (1.0 + predicted_return)
        )

        return PredictionResult(
            current_price=current_price,
            predicted_price=float(
                predicted_price
            ),
            predicted_return=predicted_return,
            forecast_horizon=forecast_horizon,
            validation_loss=float(
                best_validation_loss
            ),
            validation_rmse=validation_rmse,
            validation_mae=validation_mae,
            baseline_rmse=baseline_rmse,
        )

    def _set_random_seed(self) -> None:
        """Set random seeds for reproducibility."""
        torch.manual_seed(
            self.random_seed
        )

        np.random.seed(
            self.random_seed
        )