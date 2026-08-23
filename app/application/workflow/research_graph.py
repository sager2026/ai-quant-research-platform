from langgraph.graph import END, START, StateGraph

from app.application.workflow.research_state import ResearchState
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
    # 2. Create configured nodes
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
    # 3. Register nodes
    # ---------------------------------------------------------

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
    # 4. Define graph edges
    # ---------------------------------------------------------

    graph.add_edge(
        START,
        "market_data",
    )

    graph.add_edge(
        START,
        "fundamental_analysis",
    )

    graph.add_edge(
        "market_data",
        "technical_analysis",
    )

    graph.add_edge(
        "market_data",
        "forecast_analysis",
    )

    graph.add_edge(
        [
            "technical_analysis",
            "forecast_analysis",
            "fundamental_analysis",
        ],
        "synthesis",
    )

    graph.add_edge(
        "synthesis",
        END,
    )

    # ---------------------------------------------------------
    # 5. Compile executable graph
    # ---------------------------------------------------------

    return graph.compile()