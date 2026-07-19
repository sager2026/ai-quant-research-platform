from app.infrastructure.market_data.yahoo_repository import YahooRepository

from app.application.services.indicator_service import IndicatorService
from app.application.services.research_service import ResearchService


repo = YahooRepository()

indicator_service = IndicatorService()

research = ResearchService(
    repo,
    indicator_service,
)

context = research.build_context("AAPL")

print(context)