from dataclasses import dataclass

import pandas as pd

from app.domain.entities.indicator_result import IndicatorResult
from app.domain.entities.prediction_result import PredictionResult
from app.domain.entities.retrieval_result import RetrievalResult


@dataclass
class ResearchContext:
    """
    Contains the structured evidence available
    for generating an equity research report.

    Analytical components may be absent when
    they are not selected by the research plan.
    """

    ticker: str
    research_question: str

    current_price: float | None = None
    history: pd.DataFrame | None = None
    indicators: IndicatorResult | None = None
    prediction: PredictionResult | None = None
    retrieval: RetrievalResult | None = None