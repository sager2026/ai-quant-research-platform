from app.application.services.indicator_service import IndicatorService
from app.application.services.prediction_service import PredictionService

from app.application.workflow.research_graph import (
    create_research_graph,
)

from app.infrastructure.llm.ollama_provider import OllamaProvider
from app.infrastructure.market_data.yahoo_repository import YahooRepository
from app.infrastructure.ml.forecast_model_factory import ForecastModelFactory

from app.infrastructure.rag.ollama_embedding_model import (
    OllamaEmbeddingModel,
)
from app.infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)
from app.infrastructure.rag.vector_evidence_retriever import (
    VectorEvidenceRetriever,
)

from knowledge_setup import prepare_knowledge


TICKER = "AAPL"

# Change only this value to switch forecasting models.
MODEL_NAME = "transformer"

# Natural-language research objective.
RESEARCH_QUESTION = (
    "Give me an integrated outlook for Apple using "
    "technical, forecast, and fundamental evidence."
)

# SEC filing types available to the Research Supervisor.
FILING_TYPES = [
    "10-K",
    "10-Q",
]


def main() -> None:

    # ---------------------------------------------------------
    # 1. Prepare available fundamental knowledge
    # ---------------------------------------------------------

    for filing_type in FILING_TYPES:

        prepare_knowledge(
            ticker=TICKER,
            filing_type=filing_type,
        )

    # ---------------------------------------------------------
    # 2. Market data dependency
    # ---------------------------------------------------------

    price_repository = YahooRepository()

    # ---------------------------------------------------------
    # 3. Technical analysis dependency
    # ---------------------------------------------------------

    indicator_service = IndicatorService()

    # ---------------------------------------------------------
    # 4. Forecasting dependency
    # ---------------------------------------------------------

    forecast_model = ForecastModelFactory.create(
        MODEL_NAME
    )

    prediction_service = PredictionService(
        model=forecast_model
    )

    # ---------------------------------------------------------
    # 5. Fundamental retrieval dependencies
    # ---------------------------------------------------------

    embedding_model = OllamaEmbeddingModel(
        model="embeddinggemma"
    )

    vector_store = ChromaVectorStore(
        path="data/chroma",
        collection_name="quantmind_filings",
    )

    evidence_retriever = VectorEvidenceRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
        top_k=5,
    )

    # ---------------------------------------------------------
    # 6. LLM dependency
    # ---------------------------------------------------------

    llm = OllamaProvider(
        model="qwen3:8b"
    )

    # ---------------------------------------------------------
    # 7. Build agentic LangGraph research workflow
    # ---------------------------------------------------------

    research_graph = create_research_graph(
        price_repository=price_repository,
        indicator_service=indicator_service,
        prediction_service=prediction_service,
        evidence_retriever=evidence_retriever,
        llm=llm,
    )

    # ---------------------------------------------------------
    # 8. Initial LangGraph research state
    # ---------------------------------------------------------

    initial_state = {
        "ticker": TICKER,
        "research_question": RESEARCH_QUESTION,
    }

    # ---------------------------------------------------------
    # 9. Display research request
    # ---------------------------------------------------------

    print()

    print(
        f"Ticker: {TICKER}"
    )

    print(
        f"Forecast model: {MODEL_NAME}"
    )

    print(
        f"Research question: {RESEARCH_QUESTION}"
    )

    print(
        "=" * 60
    )

    # ---------------------------------------------------------
    # 10. Run agentic LangGraph research workflow
    # ---------------------------------------------------------

    result = research_graph.invoke(
        initial_state
    )

    # ---------------------------------------------------------
    # 11. Display Supervisor decision
    # ---------------------------------------------------------

    plan = result[
        "research_plan"
    ]

    print()
    print("Research Supervisor Plan")
    print("-" * 60)

    print(
        f"Technical analysis:   "
        f"{plan.use_technical}"
    )

    print(
        f"Forecast analysis:    "
        f"{plan.use_forecast}"
    )

    print(
        f"Fundamental analysis: "
        f"{plan.use_fundamental}"
    )

    print(
        f"SEC filing types:     "
        f"{plan.filing_types}"
    )

    print(
        "=" * 60
    )

    # ---------------------------------------------------------
    # 12. Extract final report
    # ---------------------------------------------------------

    report = result[
        "report"
    ]

    # ---------------------------------------------------------
    # 13. Display final report
    # ---------------------------------------------------------

    print(report)


if __name__ == "__main__":
    main()