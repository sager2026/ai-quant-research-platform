from dataclasses import dataclass

import pandas as pd

from app.domain.entities.indicator_result import IndicatorResult


@dataclass
class ResearchContext:

    ticker: str

    current_price: float

    history: pd.DataFrame

    indicators: IndicatorResult