from knowledge_setup import prepare_knowledge

from app.application.services.indicator_service import IndicatorService
from app.application.services.prediction_service import PredictionService
from app.application.services.research_service import ResearchService

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


TICKER = "AAPL"

# Change only this value to switch forecasting models.
MODEL_NAME = "transformer"

# Research question used by the RAG subsystem.
RESEARCH_QUESTION = "What are Apple's major business risks?"

# SEC filing used to prepare fundamental knowledge.
FILING_TYPE = "10-K"


def main() -> None:

    # ---------------------------------------------------------
    # 1. Fundamental knowledge preparation
    # ---------------------------------------------------------

    prepare_knowledge(
        ticker=TICKER,
        filing_type=FILING_TYPE,
    )

    # ---------------------------------------------------------
    # 2. Market data
    # ---------------------------------------------------------

    price_repository = YahooRepository()

    # ---------------------------------------------------------
    # 3. Technical indicators
    # ---------------------------------------------------------

    indicator_service = IndicatorService()

    # ---------------------------------------------------------
    # 4. Forecasting
    # ---------------------------------------------------------

    forecast_model = ForecastModelFactory.create(
        MODEL_NAME
    )

    prediction_service = PredictionService(
        model=forecast_model
    )

    # ---------------------------------------------------------
    # 5. RAG retrieval
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
    # 6. LLM
    # ---------------------------------------------------------

    llm = OllamaProvider(
        model="qwen3:8b"
    )

    # ---------------------------------------------------------
    # 7. Research service
    # ---------------------------------------------------------

    research_service = ResearchService(
        price_repository=price_repository,
        indicator_service=indicator_service,
        prediction_service=prediction_service,
        evidence_retriever=evidence_retriever,
        llm=llm,
    )

    # ---------------------------------------------------------
    # 8. Display configuration
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
    # 9. Run complete QuantMind research workflow
    # ---------------------------------------------------------

    report = research_service.research(
        ticker=TICKER,
        research_question=RESEARCH_QUESTION,
    )

    # ---------------------------------------------------------
    # 10. Display report
    # ---------------------------------------------------------

    print(report)


if __name__ == "__main__":
    main()