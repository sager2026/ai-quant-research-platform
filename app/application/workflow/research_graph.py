from langgraph.graph import END, START, StateGraph

from app.application.services.research_supervisor import (
    ResearchSupervisor,
)

from app.application.workflow.research_state import (
    ResearchState,
)

from app.application.workflow.nodes.supervisor_node import (
    SupervisorNode,
)

from app.application.workflow.nodes.market_data_node import (
    create_market_data_node,
)

from app.application.workflow.nodes.technical_analysis_node import (
    create_technical_analysis_node,
)

from app.application.workflow.nodes.forecast_analysis_node import (
    create_forecast_analysis_node,
)

from app.application.workflow.nodes.fundamental_analysis_node import (
    create_fundamental_analysis_node,
)

from app.application.workflow.nodes.synthesis_node import (
    create_synthesis_node,
)


# ---------------------------------------------------------
# Routing functions
# ---------------------------------------------------------


def route_after_supervisor(
    state: ResearchState,
) -> str:

    plan = state["research_plan"]

    if (
        plan.use_technical
        or plan.use_forecast
    ):
        return "market_data"

    if plan.use_fundamental:
        return "fundamental_analysis"

    return "synthesis"


def route_after_market_data(
    state: ResearchState,
) -> str:

    plan = state["research_plan"]

    if plan.use_technical:
        return "technical_analysis"

    if plan.use_forecast:
        return "forecast_analysis"

    if plan.use_fundamental:
        return "fundamental_analysis"

    return "synthesis"


def route_after_technical(
    state: ResearchState,
) -> str:

    plan = state["research_plan"]

    if plan.use_forecast:
        return "forecast_analysis"

    if plan.use_fundamental:
        return "fundamental_analysis"

    return "synthesis"


def route_after_forecast(
    state: ResearchState,
) -> str:

    plan = state["research_plan"]

    if plan.use_fundamental:
        return "fundamental_analysis"

    return "synthesis"


# ---------------------------------------------------------
# Research graph
# ---------------------------------------------------------


def create_research_graph(
    price_repository,
    indicator_service,
    prediction_service,
    evidence_retriever,
    llm,
):

    # ---------------------------------------------------------
    # 1. Create LangGraph workflow
    # ---------------------------------------------------------

    graph = StateGraph(
        ResearchState
    )

    # ---------------------------------------------------------
    # 2. Create Research Supervisor
    # ---------------------------------------------------------

    research_supervisor = ResearchSupervisor(
        llm=llm
    )

    supervisor_node = SupervisorNode(
        research_supervisor=research_supervisor
    )

    # ---------------------------------------------------------
    # 3. Create analytical nodes
    # ---------------------------------------------------------

    market_data_node = create_market_data_node(
        price_repository
    )

    technical_analysis_node = (
        create_technical_analysis_node(
            indicator_service
        )
    )

    forecast_analysis_node = (
        create_forecast_analysis_node(
            prediction_service
        )
    )

    fundamental_analysis_node = (
        create_fundamental_analysis_node(
            evidence_retriever
        )
    )

    synthesis_node = create_synthesis_node(
        llm
    )

    # ---------------------------------------------------------
    # 4. Register nodes
    # ---------------------------------------------------------

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
        "forecast_analysis",
        forecast_analysis_node,
    )

    graph.add_node(
        "fundamental_analysis",
        fundamental_analysis_node,
    )

    graph.add_node(
        "synthesis",
        synthesis_node,
    )

    # ---------------------------------------------------------
    # 5. Start with the Research Supervisor
    # ---------------------------------------------------------

    graph.add_edge(
        START,
        "supervisor",
    )

    # ---------------------------------------------------------
    # 6. Supervisor routing
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # 7. Routing after market data
    # ---------------------------------------------------------

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
            "fundamental_analysis": (
                "fundamental_analysis"
            ),
            "synthesis": "synthesis",
        },
    )

    # ---------------------------------------------------------
    # 8. Routing after technical analysis
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "technical_analysis",
        route_after_technical,
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

    # ---------------------------------------------------------
    # 9. Routing after forecast analysis
    # ---------------------------------------------------------

    graph.add_conditional_edges(
        "forecast_analysis",
        route_after_forecast,
        {
            "fundamental_analysis": (
                "fundamental_analysis"
            ),
            "synthesis": "synthesis",
        },
    )

    # ---------------------------------------------------------
    # 10. Fundamental analysis always flows to synthesis
    # ---------------------------------------------------------

    graph.add_edge(
        "fundamental_analysis",
        "synthesis",
    )

    # ---------------------------------------------------------
    # 11. Finish
    # ---------------------------------------------------------

    graph.add_edge(
        "synthesis",
        END,
    )

    # ---------------------------------------------------------
    # 12. Compile executable graph
    # ---------------------------------------------------------

    return graph.compile()