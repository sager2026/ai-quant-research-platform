from app.application.prompts.equity_prompt import EquityPrompt

from app.domain.entities.research_context import ResearchContext


class ResearchService:

    def __init__(
        self,
        price_repository,
        indicator_service,
        llm,
    ):
        self.price_repository = price_repository
        self.indicator_service = indicator_service
        self.llm = llm

    def research(
        self,
        ticker: str
    ) -> str:

        # 1. Get market data
        history = self.price_repository.get_history(ticker)

        # 2. Extract close prices
        prices = history["Close"]

        # 3. Calculate indicators
        indicators = self.indicator_service.calculate(prices)

        # 4. Build context
        context = ResearchContext(

            ticker=ticker,

            current_price=float(prices.iloc[-1]),

            history=history,

            indicators=indicators,
        )

        # 5. Build prompt
        prompt = EquityPrompt.build(context)

        # 6. Ask LLM
        report = self.llm.generate(prompt)

        return report