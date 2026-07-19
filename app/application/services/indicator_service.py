from app.domain.indicators.calculators.sma import SMA
from app.domain.indicators.calculators.ema import EMA
from app.domain.indicators.calculators.rsi import RSI
from app.domain.indicators.calculators.macd import MACD

from app.domain.entities.indicator_result import IndicatorResult


class IndicatorService:

    def __init__(self):

        self.sma = SMA()
        self.ema = EMA()
        self.rsi = RSI()
        self.macd = MACD()

    def calculate(self, prices):

        return IndicatorResult(
            sma=self.sma.calculate(prices),
            ema=self.ema.calculate(prices),
            rsi=self.rsi.calculate(prices),
            macd=self.macd.calculate(prices),
        )