from app.domain.repositories.filing_repository import FilingRepository
from app.application.knowledge.knowledge_store import KnowledgeStore


class FilingIngestionService:

    def __init__(
        self,
        filing_repository: FilingRepository,
        knowledge_store: KnowledgeStore,
    ):
        self.filing_repository = filing_repository
        self.knowledge_store = knowledge_store

    def ingest(
        self,
        ticker: str,
        filing_type: str = "10-K",
    ) -> None:

        filing = self.filing_repository.get_filing(
            ticker=ticker,
            filing_type=filing_type,
        )

        self.knowledge_store.store(
            filing
        )