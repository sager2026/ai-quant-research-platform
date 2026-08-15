from dataclasses import dataclass

import pandas as pd

from app.domain.entities.indicator_result import IndicatorResult
from app.domain.entities.prediction_result import PredictionResult
from app.domain.entities.retrieval_result import RetrievalResult


@dataclass
class ResearchContext:
    """
    Contains all structured information required
    to generate an equity research report.
    """

    ticker: str
    current_price: float
    history: pd.DataFrame
    indicators: IndicatorResult
    prediction: PredictionResult
    retrieval: RetrievalResult