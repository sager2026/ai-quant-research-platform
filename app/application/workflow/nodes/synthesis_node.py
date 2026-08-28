from collections.abc import Callable

from app.application.agents.synthesis_research_agent import (
    SynthesisResearchAgent,
)
from app.application.workflow.research_state import (
    ResearchState,
)
from app.domain.entities.research_context import (
    ResearchContext,
)


def create_synthesis_node(
    synthesis_agent: SynthesisResearchAgent,
) -> Callable[[ResearchState], dict]:
    """
    Create a LangGraph adapter for the
    Synthesis Research Agent.
    """

    def synthesis_node(
        state: ResearchState,
    ) -> dict:

        # ---------------------------------------------------------
        # 1. Build curated synthesis context
        # ---------------------------------------------------------

        context = ResearchContext(
            ticker=state["ticker"],
            research_question=state[
                "research_question"
            ],
            current_price=state.get(
                "current_price"
            ),
            indicators=state.get(
                "indicators"
            ),
            prediction=state.get(
                "prediction"
            ),
            retrieval=state.get(
                "retrieval"
            ),
            technical_agent_result=state.get(
                "technical_agent_result"
            ),
            forecast_agent_result=state.get(
                "forecast_agent_result"
            ),
            fundamental_agent_result=state.get(
                "fundamental_agent_result"
            ),
        )

        # ---------------------------------------------------------
        # 2. Delegate final reasoning to synthesis agent
        # ---------------------------------------------------------

        report = synthesis_agent.synthesize(
            context
        )

        # ---------------------------------------------------------
        # 3. Return final workflow output
        # ---------------------------------------------------------

        return {
            "report": report,
        }

    return synthesis_node