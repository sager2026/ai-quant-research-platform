from abc import ABC, abstractmethod


class EmbeddingInterface(ABC):

    @abstractmethod
    def embed(
        self,
        text: str,
    ) -> list[float]:
        pass

    @abstractmethod
    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        pass