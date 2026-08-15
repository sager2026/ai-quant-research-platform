from dataclasses import dataclass

from app.domain.entities.fundamental_evidence import FundamentalEvidence


@dataclass
class RetrievalResult:
    query: str
    evidence: list[FundamentalEvidence]