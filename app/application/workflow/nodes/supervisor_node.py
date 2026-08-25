from app.application.services.research_supervisor import (
    ResearchSupervisor,
)

from app.application.workflow.research_state import (
    ResearchState,
)


class SupervisorNode:
    """
    Uses the Research Supervisor to determine which
    research capabilities should be executed.
    """

    def __init__(
        self,
        research_supervisor: ResearchSupervisor,
    ) -> None:
        self.research_supervisor = research_supervisor

    def __call__(
        self,
        state: ResearchState,
    ) -> dict:

        plan = self.research_supervisor.plan(
            ticker=state["ticker"],
            research_question=state[
                "research_question"
            ],
        )

        return {
            "research_plan": plan
        }