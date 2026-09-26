from fastapi import FastAPI

from app.application.exceptions.research_execution_error import (
    ResearchExecutionError,
)
from app.presentation.api.exception_handlers import (
    research_execution_error_handler,
    unhandled_exception_handler,
)
from app.presentation.api.routes.health import (
    router as health_router,
)
from app.presentation.api.routes.research import (
    router as research_router,
)


app = FastAPI(
    title="QuantMind API",
    description=(
        "Financial AI research API powered by "
        "QuantMind's multi-agent research system."
    ),
    version="0.11.0",
)


app.add_exception_handler(
    ResearchExecutionError,
    research_execution_error_handler,
)

app.add_exception_handler(
    Exception,
    unhandled_exception_handler,
)


app.include_router(health_router)
app.include_router(research_router)