from app.application.exceptions.research_execution_error import (
    ResearchExecutionError,
)
from app.domain.entities.research_result import ResearchResult


class ResearchApplicationService:

    def __init__(self, research_graph):
        self.research_graph = research_graph

    def research(
        self,
        ticker: str,
        research_question: str,
    ) -> ResearchResult:

        initial_state = {
            "ticker": ticker,
            "research_question": research_question,
        }

        try:
            final_state = self.research_graph.invoke(
                initial_state
            )

        except Exception as exc:
            raise ResearchExecutionError(
                "Research workflow execution failed."
            ) from exc

        return ResearchResult(
            ticker=ticker,
            research_question=research_question,
            research_plan=final_state["research_plan"],
            report=final_state["report"],
        )