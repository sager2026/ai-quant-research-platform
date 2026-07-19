import pandas as pd


class RSI:

    def __init__(self, window: int = 14):
        self.window = window

    def calculate(self, prices: pd.Series) -> float:

        if not isinstance(prices, pd.Series):
            raise TypeError("prices must be a pandas Series")

        delta = prices.diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(self.window).mean()

        avg_loss = loss.rolling(self.window).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return float(rsi.iloc[-1])