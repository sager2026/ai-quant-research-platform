from app.application.prompts.equity_prompt import EquityPrompt
from app.domain.entities.research_context import ResearchContext


class ResearchService:
    """
    Coordinates market data retrieval, quantitative analysis,
    LSTM forecasting, prompt generation, and LLM reporting.
    """

    def __init__(
        self,
        price_repository,
        indicator_service,
        prediction_service,
        llm,
    ) -> None:
        self.price_repository = price_repository
        self.indicator_service = indicator_service
        self.prediction_service = prediction_service
        self.llm = llm

    def research(
        self,
        ticker: str,
    ) -> str:
        # 1. Download historical market data.
        history = self.price_repository.get_history(ticker)

        if history.empty:
            raise ValueError(
                f"No historical data was returned for {ticker}."
            )

        # 2. Extract closing prices.
        prices = history["Close"]

        # 3. Calculate deterministic technical indicators.
        indicators = self.indicator_service.calculate(
            prices
        )

        # 4. Train the LSTM and forecast next-day return.
        prediction = self.prediction_service.predict(
            prices=prices,
            forecast_horizon=1,
        )

        # 5. Assemble structured research context.
        context = ResearchContext(
            ticker=ticker,
            current_price=float(prices.iloc[-1]),
            history=history,
            indicators=indicators,
            prediction=prediction,
        )

        # 6. Convert structured results into an LLM prompt.
        prompt = EquityPrompt.build(context)

        # 7. Ask Ollama to synthesize the research report.
        report = self.llm.generate(prompt)

        return report