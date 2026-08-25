import json

from app.application.llm.llm_interface import LLMInterface
from app.domain.entities.research_plan import ResearchPlan


class ResearchSupervisor:
    """
    Uses an LLM to convert a natural-language research
    question into a structured ResearchPlan.
    """

    def __init__(
        self,
        llm: LLMInterface,
    ) -> None:
        self.llm = llm

    def plan(
        self,
        ticker: str,
        research_question: str,
    ) -> ResearchPlan:

        prompt = self._build_prompt(
            ticker=ticker,
            research_question=research_question,
        )

        response = self.llm.generate(
            prompt
        )

        return self._parse_response(
            response
        )

    @staticmethod
    def _build_prompt(
        ticker: str,
        research_question: str,
    ) -> str:

        return f"""
You are the research supervisor for QuantMind,
an AI-assisted quantitative investment research platform.

Your task is to determine which research capabilities
are required to answer the user's research question.

Ticker:
{ticker}

Research question:
{research_question}

Available research capabilities:

1. Technical analysis
   Use for questions involving:
   - price trends
   - moving averages
   - RSI
   - MACD
   - overbought or oversold conditions
   - technical momentum

2. Forecast analysis
   Use for questions involving:
   - future price direction
   - next-day forecasts
   - predictive models
   - expected returns
   - Transformer or LSTM forecasts

3. Fundamental analysis
   Use for questions involving:
   - business risks
   - financial condition
   - operations
   - competition
   - regulation
   - supply chains
   - company fundamentals
   - SEC filings

Available SEC filing types:

10-K:
Use primarily for annual, structural,
long-term fundamental analysis.

10-Q:
Use primarily for recent quarterly
fundamental developments.

You may select both 10-K and 10-Q when
both long-term and recent fundamental
evidence are useful.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "use_technical": true,
    "use_forecast": true,
    "use_fundamental": true,
    "filing_types": ["10-K", "10-Q"]
}}

Rules:

- Set each analysis field to true only when that
  capability materially helps answer the question.

- If use_fundamental is false,
  filing_types must be an empty list.

- If use_fundamental is true,
  filing_types must contain at least one of:
  "10-K", "10-Q".

- Do not include explanations.

- Do not include Markdown code fences.

- Do not include any text before or after the JSON.
""".strip()

    @staticmethod
    def _parse_response(
        response: str,
    ) -> ResearchPlan:

        try:
            data = json.loads(
                response.strip()
            )

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Research Supervisor returned "
                "invalid JSON."
            ) from exc

        use_technical = bool(
            data.get(
                "use_technical",
                False,
            )
        )

        use_forecast = bool(
            data.get(
                "use_forecast",
                False,
            )
        )

        use_fundamental = bool(
            data.get(
                "use_fundamental",
                False,
            )
        )

        filing_types = data.get(
            "filing_types",
            [],
        )

        if not isinstance(
            filing_types,
            list,
        ):
            raise ValueError(
                "filing_types must be a list."
            )

        allowed_filing_types = {
            "10-K",
            "10-Q",
        }

        filing_types = [
            str(filing_type).upper()
            for filing_type in filing_types
        ]

        if any(
            filing_type not in allowed_filing_types
            for filing_type in filing_types
        ):
            raise ValueError(
                "Research Supervisor returned "
                "an unsupported filing type."
            )

        if not use_fundamental:
            filing_types = []

        if (
            use_fundamental
            and not filing_types
        ):
            raise ValueError(
                "Fundamental research requires "
                "at least one filing type."
            )

        return ResearchPlan(
            use_technical=use_technical,
            use_forecast=use_forecast,
            use_fundamental=use_fundamental,
            filing_types=filing_types,
        )