from app.application.services.indicator_service import IndicatorService
from app.application.services.prediction_service import PredictionService
from app.application.services.research_service import ResearchService

from app.infrastructure.llm.ollama_provider import OllamaProvider
from app.infrastructure.market_data.yahoo_repository import YahooRepository
from app.infrastructure.ml.forecast_model_factory import ForecastModelFactory


TICKER = "AAPL"

# Change only this value to switch forecasting models.
MODEL_NAME = "transformer"


def main() -> None:
    price_repository = YahooRepository()

    indicator_service = IndicatorService()

    forecast_model = ForecastModelFactory.create(
        MODEL_NAME
    )

    prediction_service = PredictionService(
        model=forecast_model
    )

    llm = OllamaProvider(
        model="qwen3:8b"
    )

    research_service = ResearchService(
        price_repository=price_repository,
        indicator_service=indicator_service,
        prediction_service=prediction_service,
        llm=llm,
    )

    print(
        f"Ticker: {TICKER}"
    )

    print(
        f"Forecast model: {MODEL_NAME}"
    )

    print(
        "=" * 60
    )

    report = research_service.research(
        ticker=TICKER
    )

    print(report)


if __name__ == "__main__":
    main()