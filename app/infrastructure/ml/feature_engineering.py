from dataclasses import dataclass

import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import StandardScaler


@dataclass
class SequenceDataset:
    """Prepared return sequences for LSTM training and validation."""

    x_train: torch.Tensor
    y_train: torch.Tensor

    x_validation: torch.Tensor
    y_validation: torch.Tensor

    scaler: StandardScaler
    last_sequence: torch.Tensor

    validation_previous_prices: np.ndarray
    validation_actual_prices: np.ndarray


class FeatureEngineering:
    """
    Convert closing prices into return sequences for LSTM forecasting.

    The model receives historical daily returns and predicts the next
    trading day's return.
    """

    def __init__(
        self,
        sequence_length: int = 30,
        train_ratio: float = 0.8,
    ) -> None:
        if sequence_length <= 0:
            raise ValueError(
                "sequence_length must be greater than zero."
            )

        if not 0 < train_ratio < 1:
            raise ValueError(
                "train_ratio must be between zero and one."
            )

        self.sequence_length = sequence_length
        self.train_ratio = train_ratio

    def prepare(
        self,
        prices: pd.Series,
    ) -> SequenceDataset:
        """
        Prepare scaled daily-return sequences.

        Each input contains `sequence_length` historical daily returns.
        The target is the following daily return.
        """
        if not isinstance(prices, pd.Series):
            raise TypeError(
                "prices must be a pandas Series."
            )

        clean_prices = (
            prices
            .dropna()
            .astype(float)
        )

        minimum_prices = self.sequence_length + 20

        if len(clean_prices) < minimum_prices:
            raise ValueError(
                f"At least {minimum_prices} prices are required."
            )

        price_values = clean_prices.to_numpy(
            dtype=np.float64
        )

        return_values = (
            price_values[1:] / price_values[:-1]
        ) - 1.0

        return_values = return_values.reshape(-1, 1)

        split_index = int(
            len(return_values) * self.train_ratio
        )

        if split_index <= self.sequence_length:
            raise ValueError(
                "Training data is too small for the sequence length."
            )

        # Fit only on training returns to avoid data leakage.
        scaler = StandardScaler()

        scaler.fit(
            return_values[:split_index]
        )

        scaled_returns = scaler.transform(
            return_values
        )

        x_values: list[np.ndarray] = []
        y_values: list[float] = []

        target_indices: list[int] = []
        previous_prices: list[float] = []
        actual_prices: list[float] = []

        for index in range(
            self.sequence_length,
            len(scaled_returns),
        ):
            sequence = scaled_returns[
                index - self.sequence_length:index,
                0,
            ]

            target = scaled_returns[index, 0]

            x_values.append(sequence)
            y_values.append(float(target))
            target_indices.append(index)

            # Return at index i maps:
            # previous price = price_values[i]
            # actual next price = price_values[i + 1]
            previous_prices.append(
                float(price_values[index])
            )

            actual_prices.append(
                float(price_values[index + 1])
            )

        x_array = np.asarray(
            x_values,
            dtype=np.float32,
        ).reshape(
            -1,
            self.sequence_length,
            1,
        )

        y_array = np.asarray(
            y_values,
            dtype=np.float32,
        ).reshape(-1, 1)

        target_indices_array = np.asarray(
            target_indices
        )

        previous_prices_array = np.asarray(
            previous_prices,
            dtype=np.float64,
        )

        actual_prices_array = np.asarray(
            actual_prices,
            dtype=np.float64,
        )

        train_mask = (
            target_indices_array < split_index
        )

        validation_mask = (
            target_indices_array >= split_index
        )

        if not validation_mask.any():
            raise ValueError(
                "Validation set is empty."
            )

        x_train = torch.tensor(
            x_array[train_mask],
            dtype=torch.float32,
        )

        y_train = torch.tensor(
            y_array[train_mask],
            dtype=torch.float32,
        )

        x_validation = torch.tensor(
            x_array[validation_mask],
            dtype=torch.float32,
        )

        y_validation = torch.tensor(
            y_array[validation_mask],
            dtype=torch.float32,
        )

        last_sequence_array = scaled_returns[
            -self.sequence_length:,
            0,
        ].reshape(
            1,
            self.sequence_length,
            1,
        )

        last_sequence = torch.tensor(
            last_sequence_array,
            dtype=torch.float32,
        )

        return SequenceDataset(
            x_train=x_train,
            y_train=y_train,
            x_validation=x_validation,
            y_validation=y_validation,
            scaler=scaler,
            last_sequence=last_sequence,
            validation_previous_prices=(
                previous_prices_array[validation_mask]
            ),
            validation_actual_prices=(
                actual_prices_array[validation_mask]
            ),
        )