from app.application.retrieval.evidence_retriever import EvidenceRetriever
from app.domain.entities.fundamental_evidence import FundamentalEvidence
from app.domain.entities.retrieval_result import RetrievalResult
from app.application.embeddings.embedding_interface import EmbeddingInterface
from app.application.vectorstores.vector_store_interface import VectorStoreInterface


class VectorEvidenceRetriever(EvidenceRetriever):

    def __init__(
        self,
        embedding_model: EmbeddingInterface,
        vector_store: VectorStoreInterface,
        top_k: int = 5,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(
        self,
        ticker: str,
        query: str,
        filing_types: list[str] | None = None,
    ) -> RetrievalResult:

        query_embedding = self.embedding_model.embed(
            query
        )

        matches = self.vector_store.search(
            query_embedding=query_embedding,
            ticker=ticker,
            filing_types=filing_types,
            top_k=self.top_k,
        )

        evidence = []

        for match in matches:

            metadata = match["metadata"]

            relevance_score = self._distance_to_relevance(
                match["distance"]
            )

            document = self._normalize_text(
                match["document"]
            )

            item = FundamentalEvidence(
                text=document,
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

        return RetrievalResult(
            query=query,
            evidence=evidence,
        )

    @staticmethod
    def _normalize_text(
        text: str,
    ) -> str:

        if not text:
            return text

        replacements = {
            "\u00e2\u0080\u0099": "\u2019",
            "\u00e2\u0080\u0098": "\u2018",
            "\u00e2\u0080\u009c": "\u201c",
            "\u00e2\u0080\u009d": "\u201d",
            "\u00e2\u0080\u0093": "\u2013",
            "\u00e2\u0080\u0094": "\u2014",
        }

        for corrupted, correct in replacements.items():
            text = text.replace(
                corrupted,
                correct,
            )

        return text

    @staticmethod
    def _distance_to_relevance(
        distance: float,
    ) -> float:

        if distance is None:
            return 0.0

        return 1.0 / (
            1.0 + max(float(distance), 0.0)
        )