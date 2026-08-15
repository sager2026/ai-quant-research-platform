from abc import ABC, abstractmethod

from app.domain.entities.filing import Filing


class FilingRepository(ABC):

    @abstractmethod
    def get_filing(
        self,
        ticker: str,
        filing_type: str,
    ) -> Filing:
        pass