from app.domain.entities.research_context import (
    ResearchContext,
)


class EquityPrompt:
    """
    Build the final multi-agent synthesis prompt from
    deterministic evidence and specialist-agent reasoning.
    """

    @staticmethod
    def build(
        context: ResearchContext,
    ) -> str:

        research_blocks = []

        # ---------------------------------------------------------
        # Technical research
        # ---------------------------------------------------------

        if context.indicators is not None:

            indicators = context.indicators

            technical_evidence = f"""
TECHNICAL EVIDENCE

Ticker: {context.ticker}
Current price: {context.current_price:.2f}

20-day SMA: {indicators.sma:.2f}
20-day EMA: {indicators.ema:.2f}
14-day RSI: {indicators.rsi:.2f}
MACD line: {indicators.macd.macd:.2f}
MACD signal line: {indicators.macd.signal:.2f}
MACD histogram: {indicators.macd.histogram:.2f}
""".strip()

            if context.technical_agent_result is not None:

                result = context.technical_agent_result

                observations = (
                    "\n".join(
                        f"- {item}"
                        for item in result.observations
                    )
                    if result.observations
                    else "- None"
                )

                risks = (
                    "\n".join(
                        f"- {item}"
                        for item in result.risks
                    )
                    if result.risks
                    else "- None"
                )

                technical_reasoning = f"""
TECHNICAL SPECIALIST INTERPRETATION

Summary:
{result.summary}

Observations:
{observations}

Risks / limitations:
{risks}
""".strip()

            else:

                technical_reasoning = """
TECHNICAL SPECIALIST INTERPRETATION

No specialist interpretation was produced.
""".strip()

            research_blocks.append(
                f"""
====================
TECHNICAL RESEARCH
====================

{technical_evidence}

{technical_reasoning}
""".strip()
            )

        # ---------------------------------------------------------
        # Forecast research
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

            forecast_evidence = f"""
FORECAST EVIDENCE

Model: {prediction.model_name}
Forecast horizon: {prediction.forecast_horizon} trading day
Forecast target: next-day simple return

Predicted return: {prediction.predicted_return:.4%}
Implied next-day price: {prediction.predicted_price:.2f}
Forecast direction: {prediction.direction}

Validation RMSE: {prediction.validation_rmse:.4f}
Validation MAE: {prediction.validation_mae:.4f}
Naive baseline RMSE: {prediction.baseline_rmse:.4f}
Improvement over baseline: {prediction.improvement_over_baseline:.4%}

Model evaluation:
{model_status}
""".strip()

            if context.forecast_agent_result is not None:

                result = context.forecast_agent_result

                observations = (
                    "\n".join(
                        f"- {item}"
                        for item in result.observations
                    )
                    if result.observations
                    else "- None"
                )

                risks = (
                    "\n".join(
                        f"- {item}"
                        for item in result.risks
                    )
                    if result.risks
                    else "- None"
                )

                forecast_reasoning = f"""
FORECAST SPECIALIST INTERPRETATION

Summary:
{result.summary}

Observations:
{observations}

Risks / limitations:
{risks}
""".strip()

            else:

                forecast_reasoning = """
FORECAST SPECIALIST INTERPRETATION

No specialist interpretation was produced.
""".strip()

            research_blocks.append(
                f"""
====================
FORECAST RESEARCH
====================

{forecast_evidence}

{forecast_reasoning}
""".strip()
            )

        # ---------------------------------------------------------
        # Fundamental research
        # ---------------------------------------------------------

        if context.retrieval is not None:

            retrieval = context.retrieval

            if retrieval.evidence:

                fundamental_evidence = "\n\n".join(
                    (
                        f"Evidence #{index}\n"
                        f"Filing: {evidence.filing_type}\n"
                        f"Date: {evidence.filing_date}\n"
                        f"Section: {evidence.section}\n"
                        f"Relevance: "
                        f"{evidence.relevance_score:.4f}\n"
                        f"Text: {evidence.text}"
                    )
                    for index, evidence in enumerate(
                        retrieval.evidence,
                        start=1,
                    )
                )

            else:

                fundamental_evidence = (
                    "No relevant SEC filing evidence "
                    "was retrieved."
                )

            if context.fundamental_agent_result is not None:

                result = context.fundamental_agent_result

                observations = (
                    "\n".join(
                        f"- {item}"
                        for item in result.observations
                    )
                    if result.observations
                    else "- None"
                )

                risks = (
                    "\n".join(
                        f"- {item}"
                        for item in result.risks
                    )
                    if result.risks
                    else "- None"
                )

                references = (
                    ", ".join(
                        f"Evidence #{reference}"
                        for reference in (
                            result.evidence_references
                        )
                    )
                    if result.evidence_references
                    else "None"
                )

                fundamental_reasoning = f"""
FUNDAMENTAL SPECIALIST INTERPRETATION

Summary:
{result.summary}

Observations:
{observations}

Risks / limitations:
{risks}

Evidence references:
{references}
""".strip()

            else:

                fundamental_reasoning = """
FUNDAMENTAL SPECIALIST INTERPRETATION

No specialist interpretation was produced.
""".strip()

            research_blocks.append(
                f"""
====================
FUNDAMENTAL RESEARCH
====================

SEC FILING EVIDENCE

{fundamental_evidence}

{fundamental_reasoning}
""".strip()
            )

        # ---------------------------------------------------------
        # Combine selected research streams
        # ---------------------------------------------------------

        if research_blocks:

            research_text = "\n\n".join(
                research_blocks
            )

        else:

            research_text = (
                "No analytical research stream was produced "
                "for this request."
            )

        # ---------------------------------------------------------
        # Build final synthesis prompt
        # ---------------------------------------------------------

        return f"""
You are the Synthesis Research Agent in a multi-agent
equity research system.

Your responsibility is to produce the final research report
by integrating the evidence and specialist interpretations
produced by the QuantMind research workflow.

Research objective:

{context.research_question}

Ticker:

{context.ticker}


====================
RESEARCH INPUT
====================

{research_text}


====================
SYNTHESIS ROLE
====================

The specialist agents have already performed domain-specific
interpretation.

Your role is NOT to independently redo their analysis from
scratch.

Your role is to:

1. Directly answer the original research objective.

2. Synthesize the relevant specialist interpretations into
   one coherent research conclusion.

3. Use the underlying evidence to verify and ground factual
   and quantitative statements.

4. Preserve important uncertainty, limitations, and
   qualifications identified by the specialist agents.

5. Compare different research streams when more than one
   stream is available.

6. Keep different analytical horizons conceptually separate.

7. Resolve apparent differences between specialist
   interpretations only when the supplied evidence supports
   doing so.

8. Do not blindly repeat a specialist conclusion if it is
   inconsistent with the underlying evidence. In that case,
   describe the inconsistency conservatively and rely on the
   supplied evidence.

9. When a specialist interpretation goes beyond what the
   underlying evidence supports, do not propagate that
   interpretation into the final report. Use the underlying
   evidence as the authoritative grounding source.

10. Do not invent evidence that was not supplied.


====================
GROUNDING RULES
====================

1. Use only the evidence and specialist interpretations
   supplied above.

2. Treat deterministic and retrieved evidence as the factual
   grounding layer.

3. Treat specialist-agent outputs as interpretations of that
   evidence, not as new factual evidence.

4. Do not introduce external company facts, news,
   macroeconomic information, price levels, strategies,
   management actions, or investment recommendations.

5. Analyze only research streams that were actually supplied.

6. Do not describe an omitted research stream as missing,
   unavailable, failed, or a system limitation.

7. If a specialist interpretation contains a statement that
   is not supported by the underlying evidence, do not repeat
   that statement. Prefer the underlying evidence and state
   only what the evidence supports.

8. Do not claim statistical significance or insignificance.
   RMSE and MAE are historical validation-error measures,
   not confidence intervals or statistical tests.

9. Do not describe forecast accuracy, predictive precision,
   predictive reliability, or forecasting ability as high,
   low, strong, weak, good, bad, limited, or poor unless an
   explicit supplied benchmark supports that classification.

10. Do not describe a forecast or model result as random,
    noise, statistically distinguishable from random,
    statistically indistinguishable from random, significant,
    or insignificant unless an appropriate statistical test
    is explicitly supplied.

11. Do not assign a probability, confidence level,
    likelihood, or probability-based description to a
    forecast unless that measure is explicitly supplied.

12. A small improvement over the naive baseline may be
    described as economically limited. Do not convert the
    baseline comparison into a statistical claim.

13. Forecast direction is the classification supplied by the
    forecasting system. Do not reinterpret a Neutral forecast
    as bullish or bearish merely because the raw predicted
    return is slightly positive or negative.

14. Do not infer causal relationships from forecast output.

15. Do not infer long-term expected returns from a forecast
    whose supplied horizon is one trading day.

16. An overbought or oversold RSI describes the current
    condition only. Do not infer that it predicts a reversal.

17. A single SMA and EMA observation supports only their
    current relative ordering. Do not infer slope, movement,
    trend development, or a crossover from one observation.

18. A positive or negative MACD histogram describes its
    current sign only. Do not infer strengthening, weakening,
    acceleration, or deceleration without historical MACD
    observations.

19. Do not characterize technical-indicator magnitude as
    weak, strong, small, large, extreme, or near zero unless
    an explicit supplied threshold supports that
    characterization.

20. Do not claim that fundamental evidence causes, confirms,
    supports, or contradicts technical or forecast evidence
    unless the supplied evidence explicitly establishes that
    relationship.

21. When discussing SEC filing evidence, cite the relevant
    Evidence # numbers.

22. Do not convert SEC risk disclosures into predictions
    that those risks will occur.

23. Do not fabricate causal relationships between different
    evidence streams.

24. Do not mention transaction costs, trading costs,
    liquidity, slippage, market volatility, or other
    implementation costs unless those quantities or facts
    are explicitly supplied.

25. Do not infer economic significance or practical
    significance from RMSE or MAE.

26. Statistical significance and economic significance are
    different concepts. Do not use the terms statistically
    significant or statistically insignificant unless an
    explicit statistical significance test is supplied.

27. The magnitude of the predicted return may be described
    numerically or as close to zero when the supplied value
    directly supports that description. Do not infer whether
    it is profitable, tradeable, economically significant,
    or sufficient to overcome costs unless appropriate
    supporting evidence is supplied.

28. When no benchmark exists for interpreting a validation
    metric, report the metric without qualitatively
    classifying its magnitude.

29. Evidence # references always refer to raw retrieved SEC
    evidence. Never describe an Evidence # as a specialist
    interpretation. Specialist-agent output is interpretation
    supported by one or more Evidence # references.

30. Do not introduce the names of laws, regulations,
    jurisdictions, court cases, technologies, business
    arrangements, fee structures, counterparties, or
    regulatory proceedings unless they are explicitly stated
    in the supplied SEC evidence.

31. Do not infer specific financial mechanisms such as
    revenue loss, licensing disruption, fee changes,
    operating-cost increases, or stock-price effects unless
    the supplied evidence explicitly supports them.

32. Preserve the conditional language used in SEC
    disclosures. A filing statement that an event "could",
    "may", or "might" have an adverse effect must not be
    rewritten as an expected or certain outcome.

33. When citing fundamental conclusions, clearly distinguish
    between:
    - what the SEC filing states,
    - what the specialist agent interprets,
    - and what the synthesis concludes.

====================
REPORT STRUCTURE
====================

Adapt the report structure to the research objective and
the research streams actually supplied.

Always include:

## 1. Executive Summary

Directly answer the research objective and summarize the
most important conclusions supported by the available
research.

Then include ONLY the relevant analytical sections:

## Technical Analysis

Use when technical research was supplied.

## Forecast Analysis

Use when forecast research was supplied.

## Fundamental Evidence Analysis

Use when fundamental research was supplied.

## Cross-Evidence Assessment

Include this section ONLY when two or more different
research streams were supplied.

In this section, compare the specialist interpretations
without forcing agreement across different analytical
horizons.

Then always include:

## Risk Assessment

Summarize material risks, uncertainty, analytical
limitations, and model limitations supported by the
available research.

## Overall Research Conclusion

Provide a concise final conclusion that directly answers
the original research objective.

Do not force a Bullish/Bearish classification unless the
research objective calls for an overall market outlook.

End with exactly:

"This report is for research and educational purposes only and does not
constitute investment advice."
"""