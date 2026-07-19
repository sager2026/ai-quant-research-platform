from app.domain.entities.research_context import ResearchContext


class EquityPrompt:
    """
    Build a structured prompt for equity research.
    """

    @staticmethod
    def build(context: ResearchContext) -> str:

        indicators = context.indicators

        return f"""
You are a senior quantitative equity research analyst.

Your task is to analyze the following stock objectively using quantitative indicators.
Do not fabricate numbers.
Base your conclusions only on the supplied information.

========================================
Stock Information
========================================

Ticker: {context.ticker}

Current Price: {context.current_price:.2f}

========================================
Technical Indicators
========================================

20-day SMA : {indicators.sma:.2f}

20-day EMA : {indicators.ema:.2f}

14-day RSI : {indicators.rsi:.2f}

MACD       : {indicators.macd.macd:.2f}

Signal     : {indicators.macd.signal:.2f}

Histogram  : {indicators.macd.histogram:.2f}

========================================
Tasks
========================================

Please write a professional investment research report with the following sections:

1. Executive Summary

2. Trend Analysis
   - Discuss SMA and EMA
   - Identify trend direction

3. Momentum Analysis
   - Interpret RSI
   - Explain whether the stock is overbought, oversold, or neutral

4. MACD Analysis
   - Interpret MACD
   - Discuss momentum changes

5. Risk Assessment
   - Mention potential risks
   - Mention possible uncertainties

6. Overall Investment Outlook

Requirements:

- Use professional financial language.
- Be objective.
- Do not give guaranteed predictions.
- Explain your reasoning.
- Use Markdown formatting.
"""