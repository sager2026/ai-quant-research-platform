from app.application.prompts.equity_prompt import EquityPrompt
from app.domain.entities.research_context import ResearchContext


class ResearchService:
    """
    Coordinates market data retrieval, quantitative analysis,
    forecasting, fundamental evidence retrieval,
    prompt generation, and LLM reporting.
    """

    def __init__(
        self,
        price_repository,
        indicator_service,
        prediction_service,
        evidence_retriever,
        llm,
    ) -> None:
        self.price_repository = price_repository
        self.indicator_service = indicator_service
        self.prediction_service = prediction_service
        self.evidence_retriever = evidence_retriever
        self.llm = llm

    def research(
        self,
        ticker: str,
        research_question: str,
    ) -> str:
        # ---------------------------------------------------------
        # 1. Download historical market data
        # ---------------------------------------------------------

        history = self.price_repository.get_history(
            ticker
        )

        if history.empty:
            raise ValueError(
                f"No historical data was returned for {ticker}."
            )

        # ---------------------------------------------------------
        # 2. Extract closing prices
        # ---------------------------------------------------------

        prices = history["Close"]

        # ---------------------------------------------------------
        # 3. Calculate deterministic technical indicators
        # ---------------------------------------------------------

        indicators = self.indicator_service.calculate(
            prices
        )

        # ---------------------------------------------------------
        # 4. Run forecasting model
        # ---------------------------------------------------------

        prediction = self.prediction_service.predict(
            prices=prices,
            forecast_horizon=1,
        )

        # ---------------------------------------------------------
        # 5. Retrieve relevant fundamental evidence
        # ---------------------------------------------------------

        retrieval = self.evidence_retriever.retrieve(
            ticker=ticker,
            query=research_question,
        )

        # ---------------------------------------------------------
        # 6. Assemble structured research context
        # ---------------------------------------------------------

        context = ResearchContext(
            ticker=ticker,
            current_price=float(
                prices.iloc[-1]
            ),
            history=history,
            indicators=indicators,
            prediction=prediction,
            retrieval=retrieval,
        )

        # ---------------------------------------------------------
        # 7. Build evidence-constrained LLM prompt
        # ---------------------------------------------------------

        prompt = EquityPrompt.build(
            context
        )

        # ---------------------------------------------------------
        # 8. Generate integrated equity research report
        # ---------------------------------------------------------

        report = self.llm.generate(
            prompt
        )

        return report