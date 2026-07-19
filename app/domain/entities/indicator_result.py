from dataclasses import dataclass

from app.domain.entities.macd_result import MACDResult


@dataclass
class IndicatorResult:

    sma: float

    ema: float

    rsi: float

    macd: MACDResult