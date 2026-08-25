from typing import TypedDict

import pandas as pd

from app.domain.entities.indicator_result import IndicatorResult
from app.domain.entities.prediction_result import PredictionResult
from app.domain.entities.retrieval_result import RetrievalResult
from app.domain.entities.research_plan import ResearchPlan


class ResearchState(TypedDict, total=False):

    # ---------------------------------------------------------
    # Research input
    # ---------------------------------------------------------

    ticker: str
    research_question: str

    # ---------------------------------------------------------
    # Agentic research planning
    # ---------------------------------------------------------

    research_plan: ResearchPlan

    # ---------------------------------------------------------
    # Market data
    # ---------------------------------------------------------

    history: pd.DataFrame
    current_price: float

    # ---------------------------------------------------------
    # Analytical evidence
    # ---------------------------------------------------------

    indicators: IndicatorResult
    prediction: PredictionResult
    retrieval: RetrievalResult

    # ---------------------------------------------------------
    # Final output
    # ---------------------------------------------------------

    report: str