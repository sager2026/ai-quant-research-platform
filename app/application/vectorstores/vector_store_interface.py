from abc import ABC, abstractmethod


class VectorStoreInterface(ABC):

    @abstractmethod
    def add(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        pass

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        ticker: str,
        filing_types: list[str] | None = None,
        top_k: int = 5,
    ) -> list[dict]:
        pass