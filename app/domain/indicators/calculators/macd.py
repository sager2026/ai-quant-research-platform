import pandas as pd

from app.domain.entities.macd_result import MACDResult


class MACD:

    def __init__(
        self,
        short_window: int = 12,
        long_window: int = 26,
        signal_window: int = 9,
    ):
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window

    def calculate(self, prices: pd.Series) -> MACDResult:

        short_ema = prices.ewm(
            span=self.short_window,
            adjust=False
        ).mean()

        long_ema = prices.ewm(
            span=self.long_window,
            adjust=False
        ).mean()

        macd_line = short_ema - long_ema

        signal_line = macd_line.ewm(
            span=self.signal_window,
            adjust=False
        ).mean()

        histogram = macd_line - signal_line

        return MACDResult(
            macd=float(macd_line.iloc[-1]),
            signal=float(signal_line.iloc[-1]),
            histogram=float(histogram.iloc[-1]),
        )