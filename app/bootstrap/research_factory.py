from app.application.services.indicator_service import (
    IndicatorService,
)
from app.application.services.prediction_service import (
    PredictionService,
)
from app.application.services.research_application_service import (
    ResearchApplicationService,
)
from app.application.workflow.research_graph import (
    create_research_graph,
)

from app.config.settings import (
    Settings,
    get_settings,
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
from app.infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)
from app.infrastructure.rag.ollama_embedding_model import (
    OllamaEmbeddingModel,
)
from app.infrastructure.rag.vector_evidence_retriever import (
    VectorEvidenceRetriever,
)


def create_research_service(
    settings: Settings | None = None,
) -> ResearchApplicationService:
    """
    Build and return the QuantMind research application service.

    This function is the composition root for the QuantMind
    research engine.

    It creates the concrete infrastructure dependencies,
    builds the LangGraph research workflow, and wraps the
    compiled graph inside ResearchApplicationService.

    Runtime configuration is supplied through Settings rather
    than being hard-coded in the presentation layer.
    """

    # =========================================================
    # 1. Load runtime configuration
    # =========================================================

    settings = settings or get_settings()

    # =========================================================
    # 2. Market data dependency
    # =========================================================

    price_repository = YahooRepository()

    # =========================================================
    # 3. Technical analysis dependency
    # =========================================================

    indicator_service = IndicatorService()

    # =========================================================
    # 4. Forecasting dependency
    # =========================================================

    forecast_model = ForecastModelFactory.create(
        settings.forecast_model_name
    )

    prediction_service = PredictionService(
        model=forecast_model
    )

    # =========================================================
    # 5. Fundamental retrieval dependencies
    #
    # SEC filings are ingested separately and stored
    # persistently in Chroma.
    #
    # The online research engine only retrieves evidence
    # from the existing vector store.
    # =========================================================

    embedding_model = OllamaEmbeddingModel(
        model=settings.embedding_model
    )

    vector_store = ChromaVectorStore(
        path=settings.chroma_path,
        collection_name=settings.chroma_collection_name,
    )

    evidence_retriever = VectorEvidenceRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
        top_k=settings.retrieval_top_k,
    )

    # =========================================================
    # 6. LLM dependency
    # =========================================================

    llm = OllamaProvider(
        model=settings.llm_model,
        num_ctx=settings.llm_num_ctx,
    )

    # =========================================================
    # 7. Build QuantMind LangGraph workflow
    # =========================================================

    research_graph = create_research_graph(
        price_repository=price_repository,
        indicator_service=indicator_service,
        prediction_service=prediction_service,
        evidence_retriever=evidence_retriever,
        llm=llm,
    )

    # =========================================================
    # 8. Create stable application boundary
    # =========================================================

    research_service = ResearchApplicationService(
        research_graph=research_graph
    )

    return research_service