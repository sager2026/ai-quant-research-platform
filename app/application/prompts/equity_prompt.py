from app.domain.entities.research_context import ResearchContext


class EquityPrompt:
    """Build an evidence-constrained quantitative equity research prompt."""

    @staticmethod
    def build(
        context: ResearchContext,
    ) -> str:
        indicators = context.indicators
        prediction = context.prediction

        if prediction.beats_baseline:
            model_status = (
                f"The {prediction.model_name} model outperformed "
                "the naive zero-return baseline on validation RMSE."
            )
        else:
            model_status = (
                f"The {prediction.model_name} model did not outperform "
                "the naive zero-return baseline on validation RMSE."
            )

        return f"""
You are a senior quantitative equity research analyst.

Use only the supplied evidence and produce a professional Markdown report.

# Evidence Rules

- Do not fabricate company information, news, fundamentals, macroeconomic data,
  market events, support levels, resistance levels, trendlines, or chart patterns.
- Refer to the security only by ticker unless a company name is explicitly supplied.
- Do not infer changes over time from a single observation.
- Do not claim that price, SMA, EMA, RSI, MACD, or MACD histogram is rising,
  falling, widening, narrowing, accelerating, decelerating, strengthening,
  weakening, expanding, or contracting unless historical values are supplied.
- Do not use the terms crossover, cross above, or cross below unless historical
  moving-average values or an explicit crossover event are supplied.
- Do not claim that any value, spread, gap, or distance remains unchanged unless
  at least two observations are supplied.
- Do not classify the magnitude of MACD or MACD histogram as large, small,
  strong, weak, moderate, or extreme unless a benchmark or historical
  distribution is explicitly supplied.
- A single indicator observation supports only a current-state interpretation.
- Do not claim statistical significance or insignificance unless a formal test,
  p-value, confidence interval, or standard error is supplied.
- The {prediction.model_name} model predicts next-day return, not price directly.
- The implied price is mechanically derived from the predicted return.
- Validation RMSE and MAE are aggregate historical validation-error metrics
  measured in price units.
- Do not interpret RMSE or MAE as a confidence interval, prediction interval,
  probability bound, or symmetric plus-or-minus error range.
- Evaluate the model relative to the naive zero-return baseline.
- A small improvement over the baseline does not imply strong predictive power.
- Separate deterministic indicator evidence from model-based forecast evidence.
- Do not provide guaranteed investment outcomes.

# Stock Information

Ticker: {context.ticker}
Current price: {context.current_price:.2f}

# Technical Indicators

20-day SMA: {indicators.sma:.2f}
20-day EMA: {indicators.ema:.2f}
14-day RSI: {indicators.rsi:.2f}
MACD line: {indicators.macd.macd:.2f}
MACD signal line: {indicators.macd.signal:.2f}
MACD histogram: {indicators.macd.histogram:.2f}

# Forecast Model

Model name: {prediction.model_name}
Forecast horizon: {prediction.forecast_horizon} trading day
Forecast target: next-day simple return
Predicted return: {prediction.predicted_return:.2%}
Implied next-day price: {prediction.predicted_price:.2f}
Forecast direction: {prediction.direction}
Validation RMSE: {prediction.validation_rmse:.2f}
Validation MAE: {prediction.validation_mae:.2f}
Naive baseline RMSE: {prediction.baseline_rmse:.2f}
Improvement over baseline: {prediction.improvement_over_baseline:.2%}
Model evaluation: {model_status}

# Required Report Structure

## 1. Executive Summary

Summarize:

- Current technical condition
- {prediction.model_name} forecast
- Model reliability relative to the baseline
- Main risks

Do not add a company name unless one is supplied.

## 2. Trend Analysis

Interpret only:

- Current price relative to SMA
- Current price relative to EMA
- Current relationship between SMA and EMA
- Current-state trend implication

State only which moving average is currently higher.
Do not describe the SMA and EMA relationship as a crossover.
Do not infer whether SMA, EMA, price-to-average distance,
or trend strength is changing over time.
Do not compare the current price-to-average distance with a previous
observation unless previous distances are supplied.
Do not mention support or resistance.

## 3. Momentum Analysis

Interpret only:

- Current RSI level
- Whether RSI is currently overbought, oversold, or neutral
- Current relationship between MACD line and signal line
- Current sign of the MACD histogram

Do not infer whether momentum is strengthening or weakening.
Do not classify MACD or histogram magnitude without a supplied benchmark.

## 4. {prediction.model_name} Forecast Analysis

Explain:

- Predicted next-day return
- Mechanically implied next-day price
- Forecast direction
- Whether the model beats the naive baseline
- Whether the improvement appears economically meaningful
  relative to validation error

Do not describe the result as statistically significant
or statistically insignificant.

Do not treat a very small positive or negative return
as a strong directional signal.

## 5. Signal Alignment

Discuss whether:

- Technical indicators and the {prediction.model_name} forecast confirm each other
- They conflict
- They provide only weak or neutral evidence

Clearly distinguish:

- Deterministic indicator evidence
- Model-based forecast evidence

## 6. Risk Assessment

Discuss:

- Forecast uncertainty
- Validation RMSE and MAE as historical error measures in price units
- Limited baseline improvement
- Overbought or oversold risk
- Short forecast horizon
- Structural breaks
- Market regime changes

Do not convert RMSE or MAE into a formal error interval.
Do not introduce external facts or examples.

## 7. Overall Research Outlook

Classify the outlook as one of:

- Bullish
- Moderately Bullish
- Neutral
- Moderately Bearish
- Bearish

Explain the classification using only the supplied evidence.

End with this exact statement:

"This report is for research and educational purposes only and does not
constitute investment advice."
"""