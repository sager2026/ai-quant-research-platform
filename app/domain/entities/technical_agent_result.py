from dataclasses import dataclass, field


@dataclass
class TechnicalAgentResult:
    """
    Structured interpretation produced by the
    Technical Research Agent.
    """

    summary: str
    observations: list[str] = field(
        default_factory=list
    )
    risks: list[str] = field(
        default_factory=list
    )