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

QUESTION = (
    "What are Apple's recent business risks "
    "and operational challenges?"
)


# ---------------------------------------------------------
# 1. Infrastructure
# ---------------------------------------------------------

embedding_model = OllamaEmbeddingModel(
    model="embeddinggemma"
)

vector_store = ChromaVectorStore(
    path="data/chroma",
    collection_name="quantmind_filings",
)


# ---------------------------------------------------------
# 2. Evidence retriever
# ---------------------------------------------------------

retriever = VectorEvidenceRetriever(
    embedding_model=embedding_model,
    vector_store=vector_store,
    top_k=5,
)


# ---------------------------------------------------------
# 3. Retrieve ONLY 10-Q evidence
# ---------------------------------------------------------

result = retriever.retrieve(
    ticker=TICKER,
    query=QUESTION,
    filing_types=["10-Q"],
)


# ---------------------------------------------------------
# 4. Inspect results
# ---------------------------------------------------------

print(f"Question: {QUESTION}")
print("=" * 70)

for index, evidence in enumerate(
    result.evidence,
    start=1,
):

    print()
    print(f"Evidence #{index}")
    print(f"Ticker: {evidence.ticker}")
    print(f"Filing type: {evidence.filing_type}")
    print(f"Filing date: {evidence.filing_date}")
    print(
        f"Relevance score: "
        f"{evidence.relevance_score:.4f}"
    )
    print(f"Source: {evidence.source}")

    print()
    print(evidence.text[:500])

    print("-" * 70)