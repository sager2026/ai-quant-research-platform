from pydantic import BaseModel


class ResearchPlanToolResult(BaseModel):
    """
    MCP representation of the QuantMind research plan.
    """

    use_technical: bool
    use_forecast: bool
    use_fundamental: bool
    filing_types: list[str]


class ResearchToolResult(BaseModel):
    """
    Public structured result returned by the
    QuantMind research_equity MCP tool.
    """

    ticker: str
    research_question: str
    research_plan: ResearchPlanToolResult
    report: str