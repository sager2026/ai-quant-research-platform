from collections.abc import Callable

from app.application.retrieval.evidence_retriever import (
    EvidenceRetriever,
)
from app.application.workflow.research_state import (
    ResearchState,
)


def create_fundamental_analysis_node(
    evidence_retriever: EvidenceRetriever,
) -> Callable[[ResearchState], dict]:

    def fundamental_analysis_node(
        state: ResearchState,
    ) -> dict:

        ticker = state["ticker"]

        research_question = state[
            "research_question"
        ]

        research_plan = state[
            "research_plan"
        ]

        retrieval = evidence_retriever.retrieve(
            ticker=ticker,
            query=research_question,
            filing_types=research_plan.filing_types,
        )

        return {
            "retrieval": retrieval,
        }

    return fundamental_analysis_node