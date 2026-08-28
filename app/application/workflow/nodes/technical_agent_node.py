from collections.abc import Callable

from app.application.agents.technical_research_agent import (
    TechnicalResearchAgent,
)
from app.application.workflow.research_state import (
    ResearchState,
)


def create_technical_agent_node(
    technical_agent: TechnicalResearchAgent,
) -> Callable[[ResearchState], dict]:

    def technical_agent_node(
        state: ResearchState,
    ) -> dict:

        result = technical_agent.analyze(
            ticker=state["ticker"],
            current_price=state["current_price"],
            indicators=state["indicators"],
            research_question=state[
                "research_question"
            ],
        )

        return {
            "technical_agent_result": result,
        }

    return technical_agent_node