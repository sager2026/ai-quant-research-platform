from collections.abc import Callable

from app.application.services.research_supervisor import (
    ResearchSupervisor,
)
from app.application.workflow.research_state import (
    ResearchState,
)


def create_supervisor_node(
    research_supervisor: ResearchSupervisor,
) -> Callable[[ResearchState], dict]:
    """
    Create a LangGraph node that uses the Research
    Supervisor to determine which research capabilities
    should be executed.
    """

    def supervisor_node(
        state: ResearchState,
    ) -> dict:

        plan = research_supervisor.plan(
            ticker=state["ticker"],
            research_question=state[
                "research_question"
            ],
        )

        return {
            "research_plan": plan,
        }

    return supervisor_node