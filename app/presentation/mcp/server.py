from mcp.server import MCPServer

from app.presentation.mcp.research_service_provider import (
    get_research_service,
)
from app.presentation.mcp.research_tool_schema import (
    ResearchPlanToolResult,
    ResearchToolResult,
)


mcp = MCPServer(
    "QuantMind",
)


@mcp.tool()
def research_equity(
    ticker: str,
    research_question: str,
) -> ResearchToolResult:
    """
    Run QuantMind financial research for an equity.

    Args:
        ticker:
            Equity ticker symbol, for example AAPL.

        research_question:
            Natural-language financial research question.

    Returns:
        Structured QuantMind research result including
        the research plan and final report.
    """

    # ---------------------------------------------------------
    # 1. Obtain the reusable QuantMind application service
    # ---------------------------------------------------------

    research_service = get_research_service()

    # ---------------------------------------------------------
    # 2. Execute the QuantMind application use case
    # ---------------------------------------------------------

    result = research_service.research(
        ticker=ticker.upper(),
        research_question=research_question,
    )

    # ---------------------------------------------------------
    # 3. Map application result to MCP public result
    # ---------------------------------------------------------

    plan = result.research_plan

    return ResearchToolResult(
        ticker=result.ticker,
        research_question=result.research_question,
        research_plan=ResearchPlanToolResult(
            use_technical=plan.use_technical,
            use_forecast=plan.use_forecast,
            use_fundamental=plan.use_fundamental,
            filing_types=plan.filing_types,
        ),
        report=result.report,
    )


def main() -> None:
    """
    Run the QuantMind MCP server.
    """

    mcp.run()


if __name__ == "__main__":
    main()