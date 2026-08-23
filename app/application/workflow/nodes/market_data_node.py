from collections.abc import Callable

from app.application.workflow.research_state import ResearchState
from app.domain.repositories.price_repository import PriceRepository


def create_market_data_node(
    price_repository: PriceRepository,
) -> Callable[[ResearchState], dict]:

    def market_data_node(
        state: ResearchState,
    ) -> dict:

        ticker = state["ticker"]

        history = price_repository.get_history(
            ticker
        )

        if history.empty:
            raise ValueError(
                f"No market data found for {ticker}"
            )

        current_price = float(
            history["Close"].iloc[-1]
        )

        return {
            "history": history,
            "current_price": current_price,
        }

    return market_data_node