import copy
import math

import numpy as np
import pandas as pd
import torch
from torch import nn

from app.domain.entities.prediction_result import PredictionResult
from app.domain.forecast.interfaces.forecast_model import ForecastModel
from app.infrastructure.ml.feature_engineering import FeatureEngineering


class PositionalEncoding(nn.Module):
    """
    Add sinusoidal positional information to sequence embeddings.

    Self-attention does not inherently know the order of observations,
    so positional encoding tells the Transformer where each return
    appears in the sequence.
    """

    def __init__(
        self,
        d_model: int,
        max_length: int = 500,
    ) -> None:
        super().__init__()

        positions = torch.arange(
            max_length,
            dtype=torch.float32,
        ).unsqueeze(1)

        frequency_terms = torch.exp(
            torch.arange(
                0,
                d_model,
                2,
                dtype=torch.float32,
            )
            * (-math.log(10000.0) / d_model)
        )

        encoding = torch.zeros(
            max_length,
            d_model,
            dtype=torch.float32,
        )

        encoding[:, 0::2] = torch.sin(
            positions * frequency_terms
        )

        encoding[:, 1::2] = torch.cos(
            positions * frequency_terms
        )

        # Shape:
        # (1, sequence_length, d_model)
        encoding = encoding.unsqueeze(0)

        self.register_buffer(
            "encoding",
            encoding,
        )

    def forward(
        self,
        inputs: torch.Tensor,
    ) -> torch.Tensor:
        sequence_length = inputs.size(1)

        return (
            inputs
            + self.encoding[:, :sequence_length, :]
        )


class ReturnTransformerNetwork(nn.Module):
    """
    Transformer encoder network for next-day return forecasting.
    """

    def __init__(
        self,
        input_size: int = 1,
        d_model: int = 32,
        nhead: int = 4,
        num_layers: int = 2,
        dim_feedforward: int = 64,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()

        if d_model % nhead != 0:
            raise ValueError(
                "d_model must be divisible by nhead."
            )

        self.input_projection = nn.Linear(
            input_size,
            d_model,
        )

        self.positional_encoding = PositionalEncoding(
            d_model=d_model,
        )

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )

        self.transformer_encoder = nn.TransformerEncoder(
    encoder_layer=encoder_layer,
    num_layers=num_layers,
    enable_nested_tensor=False,
)

        self.output_norm = nn.LayerNorm(
            d_model
        )

        self.output_layer = nn.Linear(
            d_model,
            1,
        )

    def forward(
        self,
        inputs: torch.Tensor,
    ) -> torch.Tensor:
        """
        Args:
            inputs:
                Shape:
                (batch_size, sequence_length, input_size)

        Returns:
            Predicted standardized next-day return.
        """
        embedded = self.input_projection(
            inputs
        )

        embedded = self.positional_encoding(
            embedded
        )

        encoded = self.transformer_encoder(
            embedded
        )

        # Use the representation of the final time step.
        final_time_step = encoded[:, -1, :]

        final_time_step = self.output_norm(
            final_time_step
        )

        return self.output_layer(
            final_time_step
        )


class TransformerModel(ForecastModel):
    """
    Train a Transformer encoder to forecast next-day return.
    """

    def __init__(
        self,
        sequence_length: int = 30,
        d_model: int = 32,
        nhead: int = 4,
        num_layers: int = 2,
        dim_feedforward: int = 64,
        dropout: float = 0.1,
        learning_rate: float = 0.0005,
        epochs: int = 100,
        random_seed: int = 42,
    ) -> None:
        self.sequence_length = sequence_length
        self.d_model = d_model
        self.nhead = nhead
        self.num_layers = num_layers
        self.dim_feedforward = dim_feedforward
        self.dropout = dropout
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.random_seed = random_seed

    def fit_predict(
        self,
        prices: pd.Series,
        forecast_horizon: int = 1,
    ) -> PredictionResult:
        """
        Train the Transformer and forecast next-day return.
        """
        if not isinstance(prices, pd.Series):
            raise TypeError(
                "prices must be a pandas Series."
            )

        if forecast_horizon != 1:
            raise ValueError(
                "The current Transformer implementation "
                "supports forecast_horizon=1 only."
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

        model = ReturnTransformerNetwork(
            input_size=1,
            d_model=self.d_model,
            nhead=self.nhead,
            num_layers=self.num_layers,
            dim_feedforward=self.dim_feedforward,
            dropout=self.dropout,
        )

        loss_function = nn.MSELoss()

        optimizer = torch.optim.AdamW(
            model.parameters(),
            lr=self.learning_rate,
            weight_decay=0.0001,
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

            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                max_norm=1.0,
            )

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

            if validation_loss < best_validation_loss:
                best_validation_loss = validation_loss

                best_state = copy.deepcopy(
                    model.state_dict()
                )

        model.load_state_dict(
            best_state
        )

        model.eval()

        # Validation forecasts in standardized-return units.
        with torch.no_grad():
            predicted_scaled_returns = model(
                dataset.x_validation
            ).cpu().numpy()

        actual_scaled_returns = (
            dataset.y_validation
            .cpu()
            .numpy()
        )

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

        # Zero-return baseline:
        # next price equals current price.
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

        # Forecast next-day return from latest sequence.
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
        torch.manual_seed(
            self.random_seed
        )

        np.random.seed(
            self.random_seed
        )
