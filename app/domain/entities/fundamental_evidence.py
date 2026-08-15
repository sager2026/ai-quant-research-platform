from dataclasses import dataclass


@dataclass
class FundamentalEvidence:
    text: str
    ticker: str
    filing_type: str
    filing_date: str
    section: str
    source: str
    relevance_score: float