from dataclasses import dataclass

from app.domain.entities.indicator_result import (
    IndicatorResult,
)
from app.domain.entities.prediction_result import (
    PredictionResult,
)
from app.domain.entities.retrieval_result import (
    RetrievalResult,
)

from app.domain.entities.technical_agent_result import (
    TechnicalAgentResult,
)
from app.domain.entities.forecast_agent_result import (
    ForecastAgentResult,
)
from app.domain.entities.fundamental_agent_result import (
    FundamentalAgentResult,
)


@dataclass
class ResearchContext:
    """
    Contains the structured evidence and specialist
    interpretations available for final research synthesis.

    Analytical components may be absent when they are not
    selected by the Research Supervisor.
    """

    # ---------------------------------------------------------
    # Research input
    # ---------------------------------------------------------

    ticker: str
    research_question: str

    # ---------------------------------------------------------
    # Market context
    # ---------------------------------------------------------

    current_price: float | None = None

    # ---------------------------------------------------------
    # Analytical evidence
    # ---------------------------------------------------------

    indicators: IndicatorResult | None = None
    prediction: PredictionResult | None = None
    retrieval: RetrievalResult | None = None

    # ---------------------------------------------------------
    # Specialist agent reasoning
    # ---------------------------------------------------------

    technical_agent_result: TechnicalAgentResult | None = None
    forecast_agent_result: ForecastAgentResult | None = None
    fundamental_agent_result: FundamentalAgentResult | None = None