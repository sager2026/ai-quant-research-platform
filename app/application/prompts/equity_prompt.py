from app.domain.entities.research_context import ResearchContext


class EquityPrompt:
    """Build a grounded multi-evidence equity research prompt."""

    @staticmethod
    def build(
        context: ResearchContext,
    ) -> str:

        indicators = context.indicators
        prediction = context.prediction
        retrieval = context.retrieval

        # ---------------------------------------------------------
        # Model evaluation
        # ---------------------------------------------------------

        if prediction.beats_baseline:
            model_status = (
                f"The {prediction.model_name} model beats "
                "the naive zero-return baseline."
            )
        else:
            model_status = (
                f"The {prediction.model_name} model does not beat "
                "the naive zero-return baseline."
            )

        # ---------------------------------------------------------
        # Format retrieved fundamental evidence
        # ---------------------------------------------------------

        if retrieval.evidence:
            fundamental_evidence = "\n\n".join(
                (
                    f"Evidence #{index}\n"
                    f"Filing: {evidence.filing_type}\n"
                    f"Date: {evidence.filing_date}\n"
                    f"Text: {evidence.text}"
                )
                for index, evidence in enumerate(
                    retrieval.evidence,
                    start=1,
                )
            )
        else:
            fundamental_evidence = (
                "No fundamental evidence was retrieved."
            )

        # ---------------------------------------------------------
        # Build prompt
        # ---------------------------------------------------------

        return f"""
You are a senior quantitative equity research analyst.

Write a professional Markdown equity research report using ONLY
the three evidence blocks supplied below.

IMPORTANT:
All three evidence blocks contain valid input data.
Do not say that technical or forecast data is unavailable.


====================
EVIDENCE 1: TECHNICAL
====================

Ticker: {context.ticker}
Current price: {context.current_price:.2f}

20-day SMA: {indicators.sma:.2f}
20-day EMA: {indicators.ema:.2f}
14-day RSI: {indicators.rsi:.2f}
MACD line: {indicators.macd.macd:.2f}
MACD signal line: {indicators.macd.signal:.2f}
MACD histogram: {indicators.macd.histogram:.2f}


===================
EVIDENCE 2: FORECAST
===================

Model: {prediction.model_name}
Forecast horizon: {prediction.forecast_horizon} trading day
Forecast target: next-day simple return

Predicted return: {prediction.predicted_return:.2%}
Implied next-day price: {prediction.predicted_price:.2f}
Forecast direction: {prediction.direction}

Validation RMSE: {prediction.validation_rmse:.2f}
Validation MAE: {prediction.validation_mae:.2f}
Naive baseline RMSE: {prediction.baseline_rmse:.2f}
Improvement over baseline: {prediction.improvement_over_baseline:.2%}

Model evaluation:
{model_status}


======================
EVIDENCE 3: FUNDAMENTAL
======================

Research question:
{retrieval.query}

Retrieved SEC filing evidence:

{fundamental_evidence}


====================
ANALYSIS RULES
====================

1. Use only the evidence supplied above.

2. Treat the three evidence streams separately:
   - Technical evidence describes the current indicator state.
   - Forecast evidence describes the next-day model forecast.
   - SEC filing evidence describes fundamental business risks
     that may operate over a longer horizon.

3. Do not claim statistical significance or insignificance.
   RMSE and MAE are historical validation-error measures,
   not confidence intervals.

4. An overbought or oversold RSI describes the current condition only.
   Do not infer that it predicts a reversal.

5. Do not claim that SEC fundamental risks cause, confirm, support,
   or contradict current technical signals or the next-day forecast
   unless the supplied evidence explicitly establishes that relationship.

6. Do not fabricate facts, news, macroeconomic information,
   support/resistance levels, company strategies, or recommendations.
   
7. A single SMA and EMA observation supports only their current
   relative ordering. Do not infer the slope, direction, or movement
   of either moving average from one observation.

8. A positive or negative MACD histogram describes its current sign
   only. Do not say momentum is declining, increasing, strengthening,
   weakening, accelerating, or decelerating without historical
   MACD observations.

9. Do not classify RMSE or MAE as low, moderate, high, large, or small
   unless a benchmark for that classification is supplied.

10. When describing technical evidence based only on the supplied
    current observations, prefer terms such as "current technical
    configuration" or "current technical condition" rather than
    claiming that a trend is developing or changing.

====================
REQUIRED REPORT
====================

Produce EXACTLY these eight sections:


## 1. Executive Summary

Summarize the current technical condition, the forecast,
model performance relative to the baseline, and the main
fundamental risks found in the SEC evidence.


## 2. Trend Analysis

Analyze:

- Current price relative to SMA
- Current price relative to EMA
- SMA relative to EMA

Use only the current observations.
Do not infer a crossover or changes over time.


## 3. Momentum Analysis

Analyze:

- RSI
- MACD line relative to signal line
- Sign of MACD histogram

Do not infer an impending reversal from an overbought
or oversold RSI.


## 4. {prediction.model_name} Forecast Analysis

Analyze:

- Predicted next-day return
- Implied next-day price
- Forecast direction
- Validation RMSE and MAE
- Performance relative to the naive baseline

A small baseline improvement should be described as economically
limited, not statistically insignificant.


## 5. Fundamental Evidence Analysis

Answer the research question using only the retrieved SEC evidence.

Identify the most important business risks and cite the relevant
Evidence # numbers in the discussion.

Do not invent management actions or mitigation strategies.


## 6. Cross-Evidence Assessment

Compare the technical condition with the next-day forecast.

Then discuss the SEC fundamental evidence separately because it
generally operates over a different horizon.

Do not force the fundamental evidence to agree or disagree with
the short-horizon quantitative evidence.


## 7. Risk Assessment

Discuss:

- Forecast uncertainty
- Validation errors
- Baseline improvement
- Current RSI condition
- Short forecast horizon
- Fundamental risks identified in the SEC evidence

Keep quantitative and fundamental risks conceptually separate.


## 8. Overall Research Outlook

Classify the overall outlook as exactly one of:

- Bullish
- Moderately Bullish
- Neutral
- Moderately Bearish
- Bearish

Explain the classification using the three evidence streams while
acknowledging their different analytical horizons.

End with exactly:

"This report is for research and educational purposes only and does not
constitute investment advice."
"""