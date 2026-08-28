import json

from app.application.llm.llm_interface import LLMInterface
from app.domain.entities.indicator_result import IndicatorResult
from app.domain.entities.technical_agent_result import (
    TechnicalAgentResult,
)


class TechnicalResearchAgent:
    """
    Specialized research agent responsible for interpreting
    deterministic technical-indicator evidence.
    """

    def __init__(
        self,
        llm: LLMInterface,
    ):
        self.llm = llm

    def analyze(
        self,
        ticker: str,
        current_price: float,
        indicators: IndicatorResult,
        research_question: str,
    ) -> TechnicalAgentResult:

        prompt = self._build_prompt(
            ticker=ticker,
            current_price=current_price,
            indicators=indicators,
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
        current_price: float,
        indicators: IndicatorResult,
        research_question: str,
    ) -> str:

        return f"""
You are the Technical Research Agent in a multi-agent
equity research system.

Your responsibility is to interpret ONLY the technical
evidence supplied below.

Do not use external knowledge.
Do not invent price history.
Do not make investment recommendations.

Research question:
{research_question}

Ticker:
{ticker}

Current price:
{current_price:.2f}

Technical evidence:

20-day SMA:
{indicators.sma:.2f}

20-day EMA:
{indicators.ema:.2f}

14-day RSI:
{indicators.rsi:.2f}

MACD line:
{indicators.macd.macd:.2f}

MACD signal:
{indicators.macd.signal:.2f}

MACD histogram:
{indicators.macd.histogram:.2f}


ANALYSIS RULES

1. Interpret only the supplied technical evidence.

2. A single SMA or EMA observation does not establish
   whether either moving average is rising or falling.

3. Do not infer a moving-average crossover unless
   historical observations proving the crossover are supplied.

4. RSI describes the current momentum condition only.
   Do not claim that an overbought or oversold RSI predicts
   a reversal.

5. The MACD histogram describes its current sign only.
   Do not claim momentum is strengthening, weakening,
   accelerating, or decelerating without historical MACD data.

6. Clearly distinguish observations from risks or limitations.

7. Answer the research question when the supplied technical
   evidence supports an answer.


OUTPUT FORMAT

Return ONLY valid JSON.

Do not use Markdown.
Do not include ```json code fences.
Do not include any text before or after the JSON.

Use exactly this structure:

{{
    "summary": "concise technical interpretation",
    "observations": [
        "observation 1",
        "observation 2"
    ],
    "risks": [
        "limitation or risk 1",
        "limitation or risk 2"
    ]
}}
"""

    @staticmethod
    def _parse_response(
        response: str,
    ) -> TechnicalAgentResult:

        cleaned = response.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.removeprefix(
                "```json"
            )
            cleaned = cleaned.removeprefix(
                "```"
            )

            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

        try:
            data = json.loads(
                cleaned
            )
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Technical Research Agent returned "
                "invalid JSON."
            ) from exc

        summary = data.get(
            "summary",
            "",
        )

        observations = data.get(
            "observations",
            [],
        )

        risks = data.get(
            "risks",
            [],
        )

        if not isinstance(summary, str):
            raise ValueError(
                "Technical agent summary must be a string."
            )

        if not isinstance(observations, list):
            raise ValueError(
                "Technical agent observations must be a list."
            )

        if not isinstance(risks, list):
            raise ValueError(
                "Technical agent risks must be a list."
            )

        return TechnicalAgentResult(
            summary=summary,
            observations=[
                str(item)
                for item in observations
            ],
            risks=[
                str(item)
                for item in risks
            ],
        )