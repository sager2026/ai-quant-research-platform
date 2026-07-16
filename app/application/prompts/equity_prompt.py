def build_equity_prompt(ticker: str, history) -> str:

    latest = history.tail(20).to_markdown()

    return f"""
You are a professional equity research analyst.

Analyze the following market data.

Ticker:

{ticker}

Recent Price History:

{latest}

Write a concise report including

1. Trend

2. Volatility

3. Possible risks

4. Possible opportunities
"""