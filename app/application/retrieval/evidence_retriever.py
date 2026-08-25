from abc import ABC, abstractmethod

from app.domain.entities.retrieval_result import RetrievalResult


class EvidenceRetriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        ticker: str,
        query: str,
        filing_types: list[str] | None = None,
    ) -> RetrievalResult:
        pass