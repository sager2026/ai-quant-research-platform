from dataclasses import dataclass, field


@dataclass
class ResearchPlan:
    """
    Structured research decisions produced by
    the Research Supervisor.
    """

    use_technical: bool
    use_forecast: bool
    use_fundamental: bool
    filing_types: list[str] = field(
        default_factory=list
    )