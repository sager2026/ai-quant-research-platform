from collections.abc import Callable

from app.application.prompts.equity_prompt import EquityPrompt
from app.application.workflow.research_state import ResearchState
from app.domain.entities.research_context import ResearchContext
from app.application.llm.llm_interface import LLMInterface


def create_synthesis_node(
    llm: LLMInterface,
) -> Callable[[ResearchState], dict]:

    def synthesis_node(
        state: ResearchState,
    ) -> dict:

        context = ResearchContext(
            ticker=state["ticker"],
            current_price=state["current_price"],
            history=state["history"],
            indicators=state["indicators"],
            prediction=state["prediction"],
            retrieval=state["retrieval"],
        )

        prompt = EquityPrompt.build(
            context
        )

        report = llm.generate(
            prompt
        )

        return {
            "report": report,
        }

    return synthesis_node