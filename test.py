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
from app.infrastructure.rag.vector_evidence_retriever import (
    VectorEvidenceRetriever,
)
from app.application.services.filing_ingestion_service import (
    FilingIngestionService,
)


# ---------------------------------------------------------
# 1. Create infrastructure components
# ---------------------------------------------------------

filing_repository = SECFilingRepository(
    user_agent="QuantMind your-email@example.com"
)

extractor = SECDocumentExtractor()

chunker = TextChunker(
    chunk_size=2000,
    overlap=300,
)

embedding_model = OllamaEmbeddingModel(
    model="embeddinggemma"
)

vector_store = ChromaVectorStore(
    path="data/chroma",
    collection_name="quantmind_filings",
)


# ---------------------------------------------------------
# 2. Create KnowledgeStore implementation
# ---------------------------------------------------------

knowledge_store = VectorKnowledgeStore(
    extractor=extractor,
    chunker=chunker,
    embedding_model=embedding_model,
    vector_store=vector_store,
)


# ---------------------------------------------------------
# 3. Create ingestion service
# ---------------------------------------------------------

ingestion_service = FilingIngestionService(
    filing_repository=filing_repository,
    knowledge_store=knowledge_store,
)


# ---------------------------------------------------------
# 4. Ingest Apple's 10-K
# ---------------------------------------------------------

print("Downloading and ingesting AAPL 10-K...")

ingestion_service.ingest(
    ticker="AAPL",
    filing_type="10-K",
)

print("AAPL 10-K ingestion complete.")


# ---------------------------------------------------------
# 5. Create retriever
# ---------------------------------------------------------

retriever = VectorEvidenceRetriever(
    embedding_model=embedding_model,
    vector_store=vector_store,
    top_k=5,
)


# ---------------------------------------------------------
# 6. Retrieve evidence
# ---------------------------------------------------------

query = "What are Apple's major business risks?"

print()
print("Research question:")
print(query)
print()

result = retriever.retrieve(
    ticker="AAPL",
    query=query,
)


# ---------------------------------------------------------
# 7. Print RetrievalResult
# ---------------------------------------------------------

print("Retrieved evidence:")
print("=" * 80)

for index, evidence in enumerate(
    result.evidence,
    start=1,
):

    print()
    print(f"Evidence #{index}")
    print("-" * 80)

    print(
        f"Ticker: {evidence.ticker}"
    )

    print(
        f"Filing type: {evidence.filing_type}"
    )

    print(
        f"Filing date: {evidence.filing_date}"
    )

    print(
        f"Section: {evidence.section}"
    )

    print(
        f"Relevance score: "
        f"{evidence.relevance_score:.4f}"
    )

    print(
        f"Source: {evidence.source}"
    )

    print()
    print(evidence.text)

    print()
    print("=" * 80)