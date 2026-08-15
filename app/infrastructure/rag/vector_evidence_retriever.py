from app.application.retrieval.evidence_retriever import (
    EvidenceRetriever,
)

from app.domain.entities.fundamental_evidence import (
    FundamentalEvidence,
)

from app.domain.entities.retrieval_result import (
    RetrievalResult,
)

from app.infrastructure.rag.ollama_embedding_model import (
    OllamaEmbeddingModel,
)

from app.infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)


class VectorEvidenceRetriever(EvidenceRetriever):

    def __init__(
        self,
        embedding_model: OllamaEmbeddingModel,
        vector_store: ChromaVectorStore,
        top_k: int = 5,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(
        self,
        ticker: str,
        query: str,
    ) -> RetrievalResult:

        # Convert the research question into an embedding
        query_embedding = self.embedding_model.embed(
            query
        )

        # Search the vector database for relevant filing chunks
        matches = self.vector_store.search(
            query_embedding=query_embedding,
            ticker=ticker,
            top_k=self.top_k,
        )

        evidence = []

        # Convert Chroma search results into Domain objects
        for match in matches:

            metadata = match["metadata"]

            relevance_score = self._distance_to_relevance(
                match["distance"]
            )

            item = FundamentalEvidence(
                text=match["document"],
                ticker=metadata.get(
                    "ticker",
                    ticker.upper(),
                ),
                filing_type=metadata.get(
                    "filing_type",
                    "",
                ),
                filing_date=metadata.get(
                    "filing_date",
                    "",
                ),
                section=metadata.get(
                    "section",
                    "Unknown",
                ),
                source=metadata.get(
                    "source",
                    "",
                ),
                relevance_score=relevance_score,
            )

            evidence.append(item)

        # Package all evidence into one Domain result object
        return RetrievalResult(
            query=query,
            evidence=evidence,
        )

    @staticmethod
    def _distance_to_relevance(
        distance: float,
    ) -> float:

        if distance is None:
            return 0.0

        return 1.0 / (
            1.0 + max(float(distance), 0.0)
        )