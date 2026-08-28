import json

from app.application.llm.llm_interface import LLMInterface
from app.domain.entities.prediction_result import PredictionResult
from app.domain.entities.forecast_agent_result import (
    ForecastAgentResult,
)


class ForecastResearchAgent:
    """
    Specialized research agent responsible for interpreting
    deterministic forecasting evidence.
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
        prediction: PredictionResult,
        research_question: str,
    ) -> ForecastAgentResult:

        prompt = self._build_prompt(
            ticker=ticker,
            current_price=current_price,
            prediction=prediction,
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
        prediction: PredictionResult,
        research_question: str,
    ) -> str:

        if prediction.beats_baseline:
            baseline_status = (
                "The model beats the naive zero-return baseline."
            )
        else:
            baseline_status = (
                "The model does not beat the naive "
                "zero-return baseline."
            )

        return f"""
You are the Forecast Research Agent in a multi-agent
equity research system.

Your responsibility is to interpret ONLY the forecasting
evidence supplied below.

Do not use external knowledge.
Do not invent market information.
Do not make investment recommendations.

Research question:
{research_question}

Ticker:
{ticker}

Current price:
{current_price:.2f}


FORECAST EVIDENCE

Model:
{prediction.model_name}

Forecast horizon:
{prediction.forecast_horizon} trading day

Forecast target:
Next-day simple return

Predicted return:
{prediction.predicted_return:.4%}

Implied next-day price:
{prediction.predicted_price:.2f}

Forecast direction:
{prediction.direction}

Validation RMSE:
{prediction.validation_rmse:.4f}

Validation MAE:
{prediction.validation_mae:.4f}

Naive baseline RMSE:
{prediction.baseline_rmse:.4f}

Improvement over baseline:
{prediction.improvement_over_baseline:.4%}

Baseline comparison:
{baseline_status}


ANALYSIS RULES

1. Interpret only the supplied forecast evidence.

2. The predicted return is a model forecast, not an
   observed future outcome.

3. Do not describe the forecast as certain or guaranteed.

4. Do not interpret the forecast direction as an
   investment recommendation.

5. RMSE and MAE are historical validation-error measures.
   They are not confidence intervals.

6. Do not claim statistical significance or insignificance.

7. Do not characterize RMSE or MAE as low, moderate,
   high, good, bad, large, or small unless an explicit
   benchmark supporting that classification is supplied.

8. Use the naive baseline only for the supplied model
   comparison.

9. If the improvement over the baseline is numerically
   small, it may be described as economically limited,
   but do not describe it as statistically insignificant.

10. Do not infer long-term expected returns from a
    one-trading-day forecast.

11. Clearly distinguish model observations from
    uncertainty, limitations, and risks.

12. Answer the research question when the supplied
    forecasting evidence supports an answer.


OUTPUT FORMAT

Return ONLY valid JSON.

Do not use Markdown.
Do not include ```json code fences.
Do not include any text before or after the JSON.

Use exactly this structure:

{{
    "summary": "concise interpretation of the forecast evidence",
    "observations": [
        "forecast observation 1",
        "forecast observation 2"
    ],
    "risks": [
        "forecast limitation or risk 1",
        "forecast limitation or risk 2"
    ]
}}
"""

    @staticmethod
    def _parse_response(
        response: str,
    ) -> ForecastAgentResult:

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
                "Forecast Research Agent returned "
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
                "Forecast agent summary must be a string."
            )

        if not isinstance(observations, list):
            raise ValueError(
                "Forecast agent observations must be a list."
            )

        if not isinstance(risks, list):
            raise ValueError(
                "Forecast agent risks must be a list."
            )

        return ForecastAgentResult(
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