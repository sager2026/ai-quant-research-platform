from functools import lru_cache

from app.application.services.research_application_service import (
    ResearchApplicationService,
)
from app.bootstrap.research_factory import (
    create_research_service,
)


@lru_cache
def get_research_service() -> ResearchApplicationService:
    """
    Create and cache the QuantMind application service
    for MCP tool execution.

    The service and its infrastructure dependencies are
    initialized once per Python process and reused across
    MCP tool calls.
    """

    return create_research_service()