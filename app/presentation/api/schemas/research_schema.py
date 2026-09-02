from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """
    Public HTTP request schema for a QuantMind
    research request.
    """

    ticker: str = Field(
        min_length=1,
        max_length=20,
        examples=["AAPL"],
    )

    research_question: str = Field(
        min_length=3,
        examples=[
            "What are Apple's recent business risks?"
        ],
    )


class ResearchPlanResponse(BaseModel):
    """
    Public API representation of the internal
    ResearchPlan domain entity.
    """

    use_technical: bool
    use_forecast: bool
    use_fundamental: bool
    filing_types: list[str]


class ResearchResponse(BaseModel):
    """
    Public HTTP response returned after QuantMind
    completes a research request.
    """

    ticker: str
    research_question: str
    research_plan: ResearchPlanResponse
    report: str