import os

# from dotenv import load_dotenv

from app.application.services.research_service import ResearchService
# from app.infrastructure.llm.openai_provider import OpenAIProvider
from app.infrastructure.llm.ollama_provider import OllamaProvider
from app.infrastructure.market_data.yahoo_repository import YahooRepository


# load_dotenv()


def main():

    repository = YahooRepository()

    # llm = OpenAIProvider(
    #     os.getenv("OPENAI_API_KEY")
    # )

    #llm = OllamaProvider()
    llm = OllamaProvider("qwen3:8b")
    service = ResearchService(
        repository,
        llm,
    )

    report = service.research("AAPL")

    print(report)


if __name__ == "__main__":
    main()