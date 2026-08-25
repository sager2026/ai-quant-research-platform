from app.domain.entities.research_context import ResearchContext


class EquityPrompt:
    """
    Build a grounded equity research prompt from
    the evidence selected by the research workflow.
    """

    @staticmethod
    def build(
        context: ResearchContext,
    ) -> str:

        evidence_blocks = []

        # ---------------------------------------------------------
        # Technical evidence
        # ---------------------------------------------------------

        if context.indicators is not None:

            indicators = context.indicators

            technical_block = f"""
====================
TECHNICAL EVIDENCE
====================

Ticker: {context.ticker}
Current price: {context.current_price:.2f}

20-day SMA: {indicators.sma:.2f}
20-day EMA: {indicators.ema:.2f}
14-day RSI: {indicators.rsi:.2f}
MACD line: {indicators.macd.macd:.2f}
MACD signal line: {indicators.macd.signal:.2f}
MACD histogram: {indicators.macd.histogram:.2f}
""".strip()

            evidence_blocks.append(
                technical_block
            )

        # ---------------------------------------------------------
        # Forecast evidence
        # ---------------------------------------------------------

        if context.prediction is not None:

            prediction = context.prediction

            if prediction.beats_baseline:
                model_status = (
                    f"The {prediction.model_name} model beats "
                    "the naive zero-return baseline."
                )
            else:
                model_status = (
                    f"The {prediction.model_name} model does not "
                    "beat the naive zero-return baseline."
                )

            forecast_block = f"""
====================
FORECAST EVIDENCE
====================

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
""".strip()

            evidence_blocks.append(
                forecast_block
            )

        # ---------------------------------------------------------
        # Fundamental evidence
        # ---------------------------------------------------------

        if context.retrieval is not None:

            retrieval = context.retrieval

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
                    "No relevant fundamental evidence "
                    "was retrieved."
                )

            fundamental_block = f"""
====================
FUNDAMENTAL EVIDENCE
====================

Retrieved SEC filing evidence:

{fundamental_evidence}
""".strip()

            evidence_blocks.append(
                fundamental_block
            )

        # ---------------------------------------------------------
        # Combine selected evidence
        # ---------------------------------------------------------

        if evidence_blocks:

            evidence_text = "\n\n".join(
                evidence_blocks
            )

        else:

            evidence_text = (
                "No analytical evidence was produced "
                "for this research request."
            )

        # ---------------------------------------------------------
        # Build final prompt
        # ---------------------------------------------------------

        return f"""
You are a senior quantitative equity research analyst.

Research objective:

{context.research_question}

Ticker:

{context.ticker}

Write a professional Markdown equity research report
that directly answers the research objective using ONLY
the evidence supplied below.

Do not assume that technical, forecast, and fundamental
evidence are all available.

The QuantMind research workflow intentionally selected
only the evidence considered relevant to this research
objective.

Do not describe an omitted evidence type as missing,
unavailable, or a system failure.

====================
AVAILABLE EVIDENCE
====================

{evidence_text}


====================
ANALYSIS RULES
====================

1. Use only the evidence supplied above.

2. Directly answer the stated research objective.

3. Analyze only evidence streams that are actually supplied.

4. Technical evidence describes the current indicator state.

5. Forecast evidence describes the supplied model forecast
   over its stated forecast horizon.

6. SEC filing evidence describes company fundamentals,
   risks, financial conditions, operations, or other
   filing-based information.

7. Do not claim statistical significance or insignificance.
   RMSE and MAE are historical validation-error measures,
   not confidence intervals.

8. An overbought or oversold RSI describes the current
   condition only. Do not infer that it predicts a reversal.

9. Do not claim that SEC fundamental evidence causes,
   confirms, supports, or contradicts technical signals
   or model forecasts unless the supplied evidence
   explicitly establishes that relationship.

10. Do not fabricate facts, news, macroeconomic information,
    support/resistance levels, company strategies,
    management actions, or recommendations.

11. A single SMA and EMA observation supports only their
    current relative ordering. Do not infer their slope,
    movement, or a crossover from one observation.

12. A positive or negative MACD histogram describes its
    current sign only. Do not infer strengthening,
    weakening, acceleration, or deceleration without
    historical MACD observations.

13. Do not classify RMSE or MAE as low, moderate, high,
    large, or small unless a benchmark for that
    classification is supplied.

14. When multiple evidence streams are supplied, keep their
    different analytical horizons conceptually separate.

15. When citing fundamental evidence, refer to the relevant
    Evidence # numbers.


====================
REPORT STRUCTURE
====================

Adapt the report structure to the research objective and
the evidence actually supplied.

Always include:

## 1. Executive Summary

Directly answer the research objective and summarize the
most important available evidence.

Then include ONLY the relevant analytical sections:

- Technical Analysis
- Forecast Analysis
- Fundamental Evidence Analysis
- Cross-Evidence Assessment

Include Cross-Evidence Assessment only when two or more
different evidence streams are supplied.

Then include:

## Risk Assessment

Discuss only risks or limitations supported by the
available evidence.

## Overall Research Conclusion

Provide a concise conclusion that directly addresses
the original research objective.

Do not force a Bullish/Bearish classification when the
research objective does not call for an overall market
outlook.

End with exactly:

"This report is for research and educational purposes only and does not
constitute investment advice."
""".strip()