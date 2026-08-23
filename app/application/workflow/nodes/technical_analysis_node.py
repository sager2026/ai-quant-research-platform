from collections.abc import Callable

from app.application.services.indicator_service import IndicatorService
from app.application.workflow.research_state import ResearchState


def create_technical_analysis_node(
    indicator_service: IndicatorService,
) -> Callable[[ResearchState], dict]:

    def technical_analysis_node(
        state: ResearchState,
    ) -> dict:

        history = state["history"]

        prices = history["Close"]

        indicators = indicator_service.calculate(
            prices
        )

        return {
            "indicators": indicators,
        }

    return technical_analysis_node