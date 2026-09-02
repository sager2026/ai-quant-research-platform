from app.bootstrap.research_factory import (
    create_research_service,
)


# =============================================================
# CLI configuration
# =============================================================

TICKER = "AAPL"

MODEL_NAME = "transformer"

RESEARCH_QUESTION = (
    "What are Apple's recent business risks?"
)


def main() -> None:

    # ---------------------------------------------------------
    # 1. Build the QuantMind application service
    # ---------------------------------------------------------

    research_service = create_research_service()

    # ---------------------------------------------------------
    # 2. Display research request
    # ---------------------------------------------------------

    print()

    print(
        f"Ticker: {TICKER}"
    )

    print(
        f"Forecast model: {MODEL_NAME}"
    )

    print(
        f"Research question: {RESEARCH_QUESTION}"
    )

    print(
        "=" * 60
    )

    # ---------------------------------------------------------
    # 3. Execute QuantMind research
    # ---------------------------------------------------------

    result = research_service.research(
        ticker=TICKER,
        research_question=RESEARCH_QUESTION,
    )

    # ---------------------------------------------------------
    # 4. Display Supervisor plan
    # ---------------------------------------------------------

    plan = result.research_plan

    print()
    print("Research Supervisor Plan")
    print("-" * 60)

    print(
        f"Technical analysis:   "
        f"{plan.use_technical}"
    )

    print(
        f"Forecast analysis:    "
        f"{plan.use_forecast}"
    )

    print(
        f"Fundamental analysis: "
        f"{plan.use_fundamental}"
    )

    print(
        f"SEC filing types:     "
        f"{plan.filing_types}"
    )

    print(
        "=" * 60
    )

    # ---------------------------------------------------------
    # 5. Display final report
    # ---------------------------------------------------------

    print(
        result.report
    )


if __name__ == "__main__":
    main()