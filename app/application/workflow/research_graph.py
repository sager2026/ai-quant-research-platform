from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from app.application.agents.forecast_research_agent import (
    ForecastResearchAgent,
)
from app.application.agents.fundamental_research_agent import (
    FundamentalResearchAgent,
)
from app.application.agents.synthesis_research_agent import (
    SynthesisResearchAgent,
)
from app.application.agents.technical_research_agent import (
    TechnicalResearchAgent,
)
from app.application.llm.llm_interface import (
    LLMInterface,
)
from app.application.services.research_supervisor import (
    ResearchSupervisor,
)
from app.application.workflow.nodes.forecast_agent_node import (
    create_forecast_agent_node,
)
from app.application.workflow.nodes.forecast_analysis_node import (
    create_forecast_analysis_node,
)
from app.application.workflow.nodes.fundamental_agent_node import (
    create_fundamental_agent_node,
)
from app.application.workflow.nodes.fundamental_analysis_node import (
    create_fundamental_analysis_node,
)
from app.application.workflow.nodes.market_data_node import (
    create_market_data_node,
)
from app.application.workflow.nodes.supervisor_node import (
    create_supervisor_node,
)
from app.application.workflow.nodes.synthesis_node import (
    create_synthesis_node,
)
from app.application.workflow.nodes.technical_agent_node import (
    create_technical_agent_node,
)
from app.application.workflow.nodes.technical_analysis_node import (
    create_technical_analysis_node,
)
from app.application.workflow.research_state import (
    ResearchState,
)


def create_research_graph(
    price_repository,
    indicator_service,
    prediction_service,
    evidence_retriever,
    llm: LLMInterface,
):
    """
    Build the QuantMind v0.8 multi-agent research workflow.

    The Research Supervisor decides which research branches
    are required.

    Evidence-production nodes create structured analytical
    evidence.

    Specialist research agents interpret that evidence.

    The Synthesis Research Agent integrates the selected
    research streams into the final report.

    v0.8 intentionally uses conditional but sequential
    execution.
    """

    # ============================================================
    # 1. Create application-level reasoning components
    # ============================================================

    research_supervisor = ResearchSupervisor(
        llm=llm,
    )

    technical_agent = TechnicalResearchAgent(
        llm=llm,
    )

    forecast_agent = ForecastResearchAgent(
        llm=llm,
    )

    fundamental_agent = FundamentalResearchAgent(
        llm=llm,
    )

    synthesis_agent = SynthesisResearchAgent(
        llm=llm,
    )

    # ============================================================
    # 2. Create LangGraph node adapters
    # ============================================================

    supervisor_node = create_supervisor_node(
        research_supervisor,
    )

    market_data_node = create_market_data_node(
        price_repository,
    )

    technical_analysis_node = (
        create_technical_analysis_node(
            indicator_service,
        )
    )

    technical_agent_node = (
        create_technical_agent_node(
            technical_agent,
        )
    )

    forecast_analysis_node = (
        create_forecast_analysis_node(
            prediction_service,
        )
    )

    forecast_agent_node = (
        create_forecast_agent_node(
            forecast_agent,
        )
    )

    fundamental_analysis_node = (
        create_fundamental_analysis_node(
            evidence_retriever,
        )
    )

    fundamental_agent_node = (
        create_fundamental_agent_node(
            fundamental_agent,
        )
    )

    synthesis_node = create_synthesis_node(
        synthesis_agent,
    )

    # ============================================================
    # 3. Define routing functions
    # ============================================================

    def route_after_supervisor(
        state: ResearchState,
    ) -> str:
        """
        Determine the first research branch required by the
        Research Supervisor's plan.
        """

        plan = state["research_plan"]

        # Technical and forecast analysis both require
        # market data first.
        if (
            plan.use_technical
            or plan.use_forecast
        ):
            return "market_data"

        # Fundamental-only research does not require
        # market data.
        if plan.use_fundamental:
            return "fundamental_analysis"

        # No analytical branch selected.
        return "synthesis"

    def route_after_market_data(
        state: ResearchState,
    ) -> str:
        """
        Choose which market-data-dependent branch executes
        first.

        Technical analysis has priority when both technical
        and forecast research were selected.
        """

        plan = state["research_plan"]

        if plan.use_technical:
            return "technical_analysis"

        if plan.use_forecast:
            return "forecast_analysis"

        raise ValueError(
            "Market data was executed without a technical "
            "or forecast research branch."
        )

    def route_after_technical_agent(
        state: ResearchState,
    ) -> str:
        """
        After technical specialist reasoning, continue to
        forecast research, fundamental research, or
        synthesis.
        """

        plan = state["research_plan"]

        if plan.use_forecast:
            return "forecast_analysis"

        if plan.use_fundamental:
            return "fundamental_analysis"

        return "synthesis"

    def route_after_forecast_agent(
        state: ResearchState,
    ) -> str:
        """
        After forecast specialist reasoning, continue to
        fundamental research when required; otherwise move
        directly to synthesis.
        """

        plan = state["research_plan"]

        if plan.use_fundamental:
            return "fundamental_analysis"

        return "synthesis"

    # ============================================================
    # 4. Create graph
    # ============================================================

    graph = StateGraph(
        ResearchState,
    )

    # ============================================================
    # 5. Register nodes
    # ============================================================

    graph.add_node(
        "supervisor",
        supervisor_node,
    )

    graph.add_node(
        "market_data",
        market_data_node,
    )

    graph.add_node(
        "technical_analysis",
        technical_analysis_node,
    )

    graph.add_node(
        "technical_agent",
        technical_agent_node,
    )

    graph.add_node(
        "forecast_analysis",
        forecast_analysis_node,
    )

    graph.add_node(
        "forecast_agent",
        forecast_agent_node,
    )

    graph.add_node(
        "fundamental_analysis",
        fundamental_analysis_node,
    )

    graph.add_node(
        "fundamental_agent",
        fundamental_agent_node,
    )

    graph.add_node(
        "synthesis",
        synthesis_node,
    )

    # ============================================================
    # 6. Entry point
    # ============================================================

    graph.add_edge(
        START,
        "supervisor",
    )

    # ============================================================
    # 7. Supervisor conditional routing
    # ============================================================

    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "market_data": "market_data",
            "fundamental_analysis": (
                "fundamental_analysis"
            ),
            "synthesis": "synthesis",
        },
    )

    # ============================================================
    # 8. Market-data routing
    # ============================================================

    graph.add_conditional_edges(
        "market_data",
        route_after_market_data,
        {
            "technical_analysis": (
                "technical_analysis"
            ),
            "forecast_analysis": (
                "forecast_analysis"
            ),
        },
    )

    # ============================================================
    # 9. Technical branch
    # ============================================================

    graph.add_edge(
        "technical_analysis",
        "technical_agent",
    )

    graph.add_conditional_edges(
        "technical_agent",
        route_after_technical_agent,
        {
            "forecast_analysis": (
                "forecast_analysis"
            ),
            "fundamental_analysis": (
                "fundamental_analysis"
            ),
            "synthesis": "synthesis",
        },
    )

    # ============================================================
    # 10. Forecast branch
    # ============================================================

    graph.add_edge(
        "forecast_analysis",
        "forecast_agent",
    )

    graph.add_conditional_edges(
        "forecast_agent",
        route_after_forecast_agent,
        {
            "fundamental_analysis": (
                "fundamental_analysis"
            ),
            "synthesis": "synthesis",
        },
    )

    # ============================================================
    # 11. Fundamental branch
    # ============================================================

    graph.add_edge(
        "fundamental_analysis",
        "fundamental_agent",
    )

    graph.add_edge(
        "fundamental_agent",
        "synthesis",
    )

    # ============================================================
    # 12. Final synthesis
    # ============================================================

    graph.add_edge(
        "synthesis",
        END,
    )

    # ============================================================
    # 13. Compile workflow
    # ============================================================

    return graph.compile()