from collections.abc import Callable

from app.application.llm.llm_interface import LLMInterface
from app.application.prompts.equity_prompt import EquityPrompt
from app.application.workflow.research_state import ResearchState
from app.domain.entities.research_context import ResearchContext


def create_synthesis_node(
    llm: LLMInterface,
) -> Callable[[ResearchState], dict]:

    def synthesis_node(
        state: ResearchState,
    ) -> dict:

        # ---------------------------------------------------------
        # Build research context from available evidence
        # ---------------------------------------------------------

        context = ResearchContext(
            ticker=state["ticker"],
            research_question=state[
                "research_question"
            ],
            current_price=state.get(
                "current_price"
            ),
            history=state.get(
                "history"
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
        )

        # ---------------------------------------------------------
        # Build evidence-grounded synthesis prompt
        # ---------------------------------------------------------

        prompt = EquityPrompt.build(
            context
        )

        # ---------------------------------------------------------
        # Generate final research report
        # ---------------------------------------------------------

        report = llm.generate(
            prompt
        )

        return {
            "report": report,
        }

    return synthesis_node