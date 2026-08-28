
from collections.abc import Callable

from app.application.agents.fundamental_research_agent import (
    FundamentalResearchAgent,
)
from app.application.workflow.research_state import (
    ResearchState,
)


def create_fundamental_agent_node(
    fundamental_agent: FundamentalResearchAgent,
) -> Callable[[ResearchState], dict]:

    def fundamental_agent_node(
        state: ResearchState,
    ) -> dict:

        result = fundamental_agent.analyze(
            ticker=state["ticker"],
            research_question=state[
                "research_question"
            ],
            retrieval=state["retrieval"],
        )

        return {
            "fundamental_agent_result": result,
        }

    return fundamental_agent_node