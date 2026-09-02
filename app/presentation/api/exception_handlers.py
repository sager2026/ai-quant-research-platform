import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.application.exceptions.research_execution_error import (
    ResearchExecutionError,
)


logger = logging.getLogger(__name__)


async def research_execution_error_handler(
    request: Request,
    exc: ResearchExecutionError,
) -> JSONResponse:
    """
    Handle known QuantMind research execution failures.
    """

    logger.error(
        "Research execution failed while processing %s %s",
        request.method,
        request.url.path,
        exc_info=(
            type(exc),
            exc,
            exc.__traceback__,
        ),
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Research execution failed.",
        },
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Handle completely unexpected server-side failures.
    """

    logger.error(
        "Unhandled exception while processing %s %s",
        request.method,
        request.url.path,
        exc_info=(
            type(exc),
            exc,
            exc.__traceback__,
        ),
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error.",
        },
    )