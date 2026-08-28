from app.application.agents.forecast_research_agent import (
    ForecastResearchAgent,
)
from app.application.services.prediction_service import (
    PredictionService,
)
from app.infrastructure.llm.ollama_provider import (
    OllamaProvider,
)
from app.infrastructure.market_data.yahoo_repository import (
    YahooRepository,
)
from app.infrastructure.ml.forecast_model_factory import (
    ForecastModelFactory,
)


TICKER = "AAPL"

MODEL_NAME = "transformer"

RESEARCH_QUESTION = (
    "What does the next-day forecast suggest for Apple?"
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

    prices = history["Close"]

    current_price = float(
        prices.iloc[-1]
    )

    # ---------------------------------------------------------
    # 2. Generate deterministic forecast evidence
    # ---------------------------------------------------------

    forecast_model = ForecastModelFactory.create(
        MODEL_NAME
    )

    prediction_service = PredictionService(
        model=forecast_model
    )

    prediction = prediction_service.predict(
        prices
    )

    # ---------------------------------------------------------
    # 3. Create Forecast Research Agent
    # ---------------------------------------------------------

    llm = OllamaProvider(
        model="qwen3:8b"
    )

    forecast_agent = ForecastResearchAgent(
        llm=llm
    )

    # ---------------------------------------------------------
    # 4. Ask agent to interpret forecast evidence
    # ---------------------------------------------------------

    result = forecast_agent.analyze(
        ticker=TICKER,
        current_price=current_price,
        prediction=prediction,
        research_question=RESEARCH_QUESTION,
    )

    # ---------------------------------------------------------
    # 5. Display structured result
    # ---------------------------------------------------------

    print()
    print("FORECAST RESEARCH AGENT")
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

    print("Deterministic Forecast Evidence")
    print("-" * 70)

    print(
        f"Model:                  {prediction.model_name}"
    )

    print(
        f"Forecast horizon:       "
        f"{prediction.forecast_horizon} trading day"
    )

    print(
        f"Predicted return:       "
        f"{prediction.predicted_return:.4%}"
    )

    print(
        f"Predicted price:        "
        f"{prediction.predicted_price:.2f}"
    )

    print(
        f"Direction:              "
        f"{prediction.direction}"
    )

    print(
        f"Validation RMSE:        "
        f"{prediction.validation_rmse:.4f}"
    )

    print(
        f"Validation MAE:         "
        f"{prediction.validation_mae:.4f}"
    )

    print(
        f"Baseline RMSE:          "
        f"{prediction.baseline_rmse:.4f}"
    )

    print(
        f"Baseline improvement:   "
        f"{prediction.improvement_over_baseline:.4%}"
    )

    print(
        f"Beats baseline:         "
        f"{prediction.beats_baseline}"
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