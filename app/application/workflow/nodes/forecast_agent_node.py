from collections.abc import Callable

from app.application.agents.forecast_research_agent import (
    ForecastResearchAgent,
)
from app.application.workflow.research_state import (
    ResearchState,
)


def create_forecast_agent_node(
    forecast_agent: ForecastResearchAgent,
) -> Callable[[ResearchState], dict]:

    def forecast_agent_node(
        state: ResearchState,
    ) -> dict:

        result = forecast_agent.analyze(
            ticker=state["ticker"],
            current_price=state["current_price"],
            prediction=state["prediction"],
            research_question=state[
                "research_question"
            ],
        )

        return {
            "forecast_agent_result": result,
        }

    return forecast_agent_node