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

# Research question used by the RAG subsystem.
RESEARCH_QUESTION = "What are Apple's major business risks?"

# SEC filing used to prepare fundamental knowledge.
FILING_TYPE = "10-K"


def main() -> None:

    # ---------------------------------------------------------
    # 1. Prepare fundamental knowledge
    # ---------------------------------------------------------

    prepare_knowledge(
        ticker=TICKER,
        filing_type=FILING_TYPE,
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
    # 7. Build LangGraph research workflow
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
    # 9. Display configuration
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
    # 10. Run complete LangGraph research workflow
    # ---------------------------------------------------------

    result = research_graph.invoke(
        initial_state
    )

    # ---------------------------------------------------------
    # 11. Extract final report from ResearchState
    # ---------------------------------------------------------

    report = result["report"]

    # ---------------------------------------------------------
    # 12. Display report
    # ---------------------------------------------------------

    print(report)


if __name__ == "__main__":
    main()