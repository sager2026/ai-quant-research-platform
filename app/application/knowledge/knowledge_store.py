from abc import ABC, abstractmethod

from app.domain.entities.filing import Filing


class KnowledgeStore(ABC):

    @abstractmethod
    def store(
        self,
        filing: Filing,
    ) -> None:
        pass