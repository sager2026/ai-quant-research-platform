from dataclasses import dataclass


@dataclass
class MACDResult:
    macd: float
    signal: float
    histogram: float