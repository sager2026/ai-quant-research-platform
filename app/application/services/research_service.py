from app.application.llm.llm_interface import LLMInterface
from app.application.prompts.equity_prompt import build_equity_prompt
from app.domain.repositories.price_repository import PriceRepository


class ResearchService:

    def __init__(
        self,
        repository: PriceRepository,
        llm: LLMInterface,
    ):
        self.repository = repository
        self.llm = llm

    def research(self, ticker: str):

        history = self.repository.get_history(ticker)

        prompt = build_equity_prompt(
            ticker,
            history,
        )

        report = self.llm.generate(prompt)

        return report