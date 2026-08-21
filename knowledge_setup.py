from app.application.services.filing_ingestion_service import (
    FilingIngestionService,
)

from app.infrastructure.rag.sec_filing_repository import (
    SECFilingRepository,
)
from app.infrastructure.rag.sec_document_extractor import (
    SECDocumentExtractor,
)
from app.infrastructure.rag.text_chunker import (
    TextChunker,
)
from app.infrastructure.rag.ollama_embedding_model import (
    OllamaEmbeddingModel,
)
from app.infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)
from app.infrastructure.rag.vector_knowledge_store import (
    VectorKnowledgeStore,
)


SEC_USER_AGENT = "QuantMind sagerlht@gmail.com"


def prepare_knowledge(
    ticker: str,
    filing_type: str = "10-K",
) -> None:
    """
    Prepare QuantMind's fundamental knowledge base
    using the latest SEC filing.
    """

    # ---------------------------------------------------------
    # 1. SEC filing repository
    # ---------------------------------------------------------

    filing_repository = SECFilingRepository(
        user_agent=SEC_USER_AGENT
    )

    # ---------------------------------------------------------
    # 2. Document processing
    # ---------------------------------------------------------

    extractor = SECDocumentExtractor()

    chunker = TextChunker(
        chunk_size=2000,
        overlap=300,
    )

    # ---------------------------------------------------------
    # 3. Embedding model
    # ---------------------------------------------------------

    embedding_model = OllamaEmbeddingModel(
        model="embeddinggemma"
    )

    # ---------------------------------------------------------
    # 4. Vector store
    # ---------------------------------------------------------

    vector_store = ChromaVectorStore(
        path="data/chroma",
        collection_name="quantmind_filings",
    )

    # ---------------------------------------------------------
    # 5. Knowledge store
    # ---------------------------------------------------------

    knowledge_store = VectorKnowledgeStore(
        extractor=extractor,
        chunker=chunker,
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    # ---------------------------------------------------------
    # 6. Filing ingestion service
    # ---------------------------------------------------------

    ingestion_service = FilingIngestionService(
        filing_repository=filing_repository,
        knowledge_store=knowledge_store,
    )

    # ---------------------------------------------------------
    # 7. Prepare knowledge
    # ---------------------------------------------------------

    print(
        f"Preparing fundamental knowledge: "
        f"{ticker.upper()} {filing_type}"
    )

    ingestion_service.ingest(
        ticker=ticker,
        filing_type=filing_type,
    )

    print(
        f"Fundamental knowledge ready: "
        f"{ticker.upper()} {filing_type}"
    )