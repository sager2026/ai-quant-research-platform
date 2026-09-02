from dataclasses import dataclass

from app.domain.entities.research_plan import ResearchPlan


@dataclass
class ResearchResult:
    """
    Stable application-level result returned by a
    QuantMind research execution.

    ResearchResult intentionally exposes only the
    information required by application callers.

    It is separate from ResearchState, which contains
    internal LangGraph workflow state.
    """

    ticker: str
    research_question: str
    research_plan: ResearchPlan
    report: str