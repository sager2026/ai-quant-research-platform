from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from app.application.services.research_application_service import (
    ResearchApplicationService,
)
from app.presentation.api.dependencies import (
    get_research_service,
)
from app.presentation.api.schemas.research_schema import (
    ResearchPlanResponse,
    ResearchRequest,
    ResearchResponse,
)


router = APIRouter()


@router.post(
    "/research",
    response_model=ResearchResponse,
    tags=["Research"],
)
def research(
    request: ResearchRequest,
    research_service: Annotated[
        ResearchApplicationService,
        Depends(get_research_service),
    ],
) -> ResearchResponse:
    """
    Execute a QuantMind financial research request.
    """

    # ---------------------------------------------------------
    # 1. Execute application use case
    # ---------------------------------------------------------

    result = research_service.research(
        ticker=request.ticker.upper(),
        research_question=request.research_question,
    )

    # ---------------------------------------------------------
    # 2. Map Domain/Application result to API response
    # ---------------------------------------------------------

    plan = result.research_plan

    return ResearchResponse(
        ticker=result.ticker,
        research_question=result.research_question,
        research_plan=ResearchPlanResponse(
            use_technical=plan.use_technical,
            use_forecast=plan.use_forecast,
            use_fundamental=plan.use_fundamental,
            filing_types=plan.filing_types,
        ),
        report=result.report,
    )