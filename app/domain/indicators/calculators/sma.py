import pandas as pd


class SMA:

    def __init__(self, window: int = 20):
        self.window = window

    def calculate(self, prices: pd.Series) -> float:

        if not isinstance(prices, pd.Series):
            raise TypeError("prices must be a pandas Series")

        if len(prices) < self.window:
            raise ValueError(
                f"SMA requires at least {self.window} prices."
            )

        return float(
            prices
            .rolling(self.window)
            .mean()
            .iloc[-1]
        )