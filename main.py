from app.application.services.indicator_service import (
    IndicatorService,
)
from app.application.services.prediction_service import (
    PredictionService,
)

from app.application.workflow.research_graph import (
    create_research_graph,
)

from app.infrastructure.llm.ollama_provider import (
    OllamaProvider,
)
from app.infrastructure.market_data.yahoo_repository import (
    YahooRepository,
)
from app.infrastructure.ml.forecast_model_factory import (
    ForecastModelFactory,
)

from app.infrastructure.rag.ollama_embedding_model import (
    OllamaEmbeddingModel,
)
from app.infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)
from app.infrastructure.rag.vector_evidence_retriever import (
    VectorEvidenceRetriever,
)


# =============================================================
# Research configuration
# =============================================================

TICKER = "AAPL"

# Change only this value to switch forecasting models.
MODEL_NAME = "transformer"

# Natural-language research objective.

RESEARCH_QUESTION = (
    "What are Apple's recent business risks?"
)

def main() -> None:

    # ---------------------------------------------------------
    # 1. Market data dependency
    # ---------------------------------------------------------

    price_repository = YahooRepository()

    # ---------------------------------------------------------
    # 2. Technical analysis dependency
    # ---------------------------------------------------------

    indicator_service = IndicatorService()

    # ---------------------------------------------------------
    # 3. Forecasting dependency
    # ---------------------------------------------------------

    forecast_model = ForecastModelFactory.create(
        MODEL_NAME
    )

    prediction_service = PredictionService(
        model=forecast_model
    )

    # ---------------------------------------------------------
    # 4. Fundamental retrieval dependencies
    #
    # SEC filings are prepared separately by the knowledge
    # ingestion workflow and stored persistently in Chroma.
    #
    # The online research workflow only retrieves evidence
    # when the Research Supervisor selects fundamental
    # analysis.
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
    # 5. LLM dependency
    #
    # qwen3:8b supports a much larger context window, but
    # Ollama otherwise defaults to a smaller runtime context.
    #
    # 16,384 tokens provides sufficient room for integrated
    # multi-agent synthesis while avoiding unnecessary use
    # of the model's full context capacity.
    # ---------------------------------------------------------

    llm = OllamaProvider(
        model="qwen3:8b",
        num_ctx=16384,
    )

    # ---------------------------------------------------------
    # 6. Build multi-agent LangGraph research workflow
    # ---------------------------------------------------------

    research_graph = create_research_graph(
        price_repository=price_repository,
        indicator_service=indicator_service,
        prediction_service=prediction_service,
        evidence_retriever=evidence_retriever,
        llm=llm,
    )

    # ---------------------------------------------------------
    # 7. Initial LangGraph research state
    # ---------------------------------------------------------

    initial_state = {
        "ticker": TICKER,
        "research_question": RESEARCH_QUESTION,
    }

    # ---------------------------------------------------------
    # 8. Display research request
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
    # 9. Run multi-agent LangGraph research workflow
    # ---------------------------------------------------------

    result = research_graph.invoke(
        initial_state
    )

    # ---------------------------------------------------------
    # 10. Display Research Supervisor decision
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
    # 11. Extract final report
    # ---------------------------------------------------------

    report = result[
        "report"
    ]

    # ---------------------------------------------------------
    # 12. Display final report
    # ---------------------------------------------------------

    print(report)


if __name__ == "__main__":
    main()