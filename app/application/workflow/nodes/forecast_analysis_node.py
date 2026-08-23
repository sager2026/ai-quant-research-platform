from collections.abc import Callable

from app.application.services.prediction_service import (
    PredictionService,
)
from app.application.workflow.research_state import (
    ResearchState,
)


def create_forecast_analysis_node(
    prediction_service: PredictionService,
) -> Callable[[ResearchState], dict]:

    def forecast_analysis_node(
        state: ResearchState,
    ) -> dict:

        history = state["history"]

        prices = history["Close"]

        prediction = prediction_service.predict(
            prices
        )

        return {
            "prediction": prediction,
        }

    return forecast_analysis_node