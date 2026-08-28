from dataclasses import dataclass, field


@dataclass
class FundamentalAgentResult:
    """
    Structured interpretation produced by the
    Fundamental Research Agent.
    """

    summary: str
    observations: list[str] = field(
        default_factory=list
    )
    risks: list[str] = field(
        default_factory=list
    )
    evidence_references: list[int] = field(
        default_factory=list
    )