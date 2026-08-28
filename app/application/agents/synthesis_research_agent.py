from app.application.llm.llm_interface import (
    LLMInterface,
)
from app.application.prompts.equity_prompt import (
    EquityPrompt,
)
from app.domain.entities.research_context import (
    ResearchContext,
)


class SynthesisResearchAgent:
    """
    Specialized research agent responsible for integrating
    raw evidence and specialist-agent interpretations into
    the final equity research report.
    """

    def __init__(
        self,
        llm: LLMInterface,
    ):
        self.llm = llm

    def synthesize(
        self,
        context: ResearchContext,
    ) -> str:
        """
        Produce the final grounded research report from the
        curated multi-agent research context.
        """

        prompt = EquityPrompt.build(
            context
        )

        report = self.llm.generate(
            prompt
        )

        return report