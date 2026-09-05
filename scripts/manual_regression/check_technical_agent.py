from app.application.agents.technical_research_agent import (
    TechnicalResearchAgent,
)
from app.application.services.indicator_service import (
    IndicatorService,
)
from app.infrastructure.llm.ollama_provider import (
    OllamaProvider,
)
from app.infrastructure.market_data.yahoo_repository import (
    YahooRepository,
)


TICKER = "AAPL"

RESEARCH_QUESTION = (
    "Is Apple technically oversold?"
)


def main() -> None:

    # ---------------------------------------------------------
    # 1. Load market data
    # ---------------------------------------------------------

    price_repository = YahooRepository()

    history = price_repository.get_history(
        TICKER
    )

    if history.empty:
        raise ValueError(
            f"No market data found for {TICKER}"
        )

    current_price = float(
        history["Close"].iloc[-1]
    )

    # ---------------------------------------------------------
    # 2. Calculate deterministic technical evidence
    # ---------------------------------------------------------

    indicator_service = IndicatorService()

    indicators = indicator_service.calculate(
        history["Close"]
    )

    # ---------------------------------------------------------
    # 3. Create Technical Research Agent
    # ---------------------------------------------------------

    llm = OllamaProvider(
        model="qwen3:8b"
    )

    technical_agent = TechnicalResearchAgent(
        llm=llm
    )

    # ---------------------------------------------------------
    # 4. Ask agent to interpret the evidence
    # ---------------------------------------------------------

    result = technical_agent.analyze(
        ticker=TICKER,
        current_price=current_price,
        indicators=indicators,
        research_question=RESEARCH_QUESTION,
    )

    # ---------------------------------------------------------
    # 5. Display structured result
    # ---------------------------------------------------------

    print()
    print("TECHNICAL RESEARCH AGENT")
    print("=" * 70)

    print(
        f"Ticker: {TICKER}"
    )

    print(
        f"Research question: {RESEARCH_QUESTION}"
    )

    print(
        f"Current price: {current_price:.2f}"
    )

    print()

    print("Deterministic Evidence")
    print("-" * 70)

    print(
        f"SMA:            {indicators.sma:.2f}"
    )

    print(
        f"EMA:            {indicators.ema:.2f}"
    )

    print(
        f"RSI:            {indicators.rsi:.2f}"
    )

    print(
        f"MACD:           {indicators.macd.macd:.2f}"
    )

    print(
        f"MACD signal:    {indicators.macd.signal:.2f}"
    )

    print(
        f"MACD histogram: {indicators.macd.histogram:.2f}"
    )

    print()
    print("Agent Interpretation")
    print("-" * 70)

    print(
        f"Summary: {result.summary}"
    )

    print()
    print("Observations:")

    for observation in result.observations:
        print(
            f"- {observation}"
        )

    print()
    print("Risks / Limitations:")

    for risk in result.risks:
        print(
            f"- {risk}"
        )


if __name__ == "__main__":
    main()