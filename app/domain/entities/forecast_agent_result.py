from dataclasses import dataclass, field


@dataclass
class ForecastAgentResult:
    """
    Structured interpretation produced by the
    Forecast Research Agent.
    """

    summary: str
    observations: list[str] = field(
        default_factory=list
    )
    risks: list[str] = field(
        default_factory=list
    )