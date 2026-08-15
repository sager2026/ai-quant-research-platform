from dataclasses import dataclass


@dataclass
class Filing:
    ticker: str
    filing_type: str
    filing_date: str
    content: str
    source: str