from typing import TypedDict

import pandas as pd

from app.domain.entities.indicator_result import IndicatorResult
from app.domain.entities.prediction_result import PredictionResult
from app.domain.entities.retrieval_result import RetrievalResult
from app.domain.entities.research_plan import ResearchPlan

from app.domain.entities.technical_agent_result import (
    TechnicalAgentResult,
)
from app.domain.entities.forecast_agent_result import (
    ForecastAgentResult,
)
from app.domain.entities.fundamental_agent_result import (
    FundamentalAgentResult,
)


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
    # Deterministic analytical evidence
    # ---------------------------------------------------------

    indicators: IndicatorResult
    prediction: PredictionResult
    retrieval: RetrievalResult

    # ---------------------------------------------------------
    # Specialist agent reasoning
    # ---------------------------------------------------------

    technical_agent_result: TechnicalAgentResult
    forecast_agent_result: ForecastAgentResult
    fundamental_agent_result: FundamentalAgentResult

    # ---------------------------------------------------------
    # Final output
    # ---------------------------------------------------------

    report: str