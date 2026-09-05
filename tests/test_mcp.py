import pytest

from mcp import Client

import app.presentation.mcp.server as server_module
from app.domain.entities.research_plan import ResearchPlan
from app.domain.entities.research_result import ResearchResult


class FakeResearchService:
    def research(
        self,
        ticker: str,
        research_question: str,
    ) -> ResearchResult:
        return ResearchResult(
            ticker=ticker,
            research_question=research_question,
            research_plan=ResearchPlan(
                use_technical=False,
                use_forecast=False,
                use_fundamental=True,
                filing_types=["10-Q"],
            ),
            report="Fake QuantMind MCP research report.",
        )


@pytest.fixture(autouse=True)
def override_research_service(monkeypatch):
    def get_fake_research_service():
        return FakeResearchService()

    monkeypatch.setattr(
        server_module,
        "get_research_service",
        get_fake_research_service,
    )


@pytest.mark.anyio
async def test_research_equity_tool_is_registered():
    async with Client(server_module.mcp) as client:
        tools = await client.list_tools()

        tool_names = [
            tool.name
            for tool in tools.tools
        ]

        assert "research_equity" in tool_names


@pytest.mark.anyio
async def test_research_equity_tool():
    async with Client(server_module.mcp) as client:
        result = await client.call_tool(
            "research_equity",
            {
                "ticker": "AAPL",
                "research_question":
                    "What are Apple's recent business risks?",
            },
        )

        assert result.is_error is False

        assert result.structured_content == {
            "ticker": "AAPL",
            "research_question":
                "What are Apple's recent business risks?",
            "research_plan": {
                "use_technical": False,
                "use_forecast": False,
                "use_fundamental": True,
                "filing_types": ["10-Q"],
            },
            "report":
                "Fake QuantMind MCP research report.",
        }


@pytest.mark.anyio
async def test_research_equity_normalizes_ticker():
    async with Client(server_module.mcp) as client:
        result = await client.call_tool(
            "research_equity",
            {
                "ticker": "aapl",
                "research_question":
                    "What are Apple's recent business risks?",
            },
        )

        assert result.is_error is False
        assert result.structured_content["ticker"] == "AAPL"


@pytest.mark.anyio
async def test_research_equity_failure_returns_mcp_error(
    monkeypatch,
):
    class FailingResearchService:
        def research(
            self,
            ticker: str,
            research_question: str,
        ):
            raise RuntimeError("Simulated research failure.")

    def get_failing_research_service():
        return FailingResearchService()

    monkeypatch.setattr(
        server_module,
        "get_research_service",
        get_failing_research_service,
    )

    async with Client(server_module.mcp) as client:
        result = await client.call_tool(
            "research_equity",
            {
                "ticker": "AAPL",
                "research_question":
                    "What are Apple's recent business risks?",
            },
        )

        assert result.is_error is True