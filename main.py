from app.application.services.indicator_service import (
    IndicatorService,
)
from app.application.services.prediction_service import (
    PredictionService,
)
from app.application.services.research_service import (
    ResearchService,
)
from app.infrastructure.llm.ollama_provider import (
    OllamaProvider,
)
from app.infrastructure.market_data.yahoo_repository import (
    YahooRepository,
)
from app.infrastructure.ml.lstm_model import (
    LSTMModel,
)


def main() -> None:
    ticker = "AAPL"

    price_repository = YahooRepository()

    indicator_service = IndicatorService()

    lstm_model = LSTMModel(
        sequence_length=30,
        hidden_size=32,
        num_layers=1,
        learning_rate=0.001,
        epochs=100,
        random_seed=42,
    )

    prediction_service = PredictionService(
        model=lstm_model
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

    report = research_service.research(
        ticker=ticker
    )

    print(report)


if __name__ == "__main__":
    main()