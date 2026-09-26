from app.application.llm.llm_interface import (
    LLMInterface,
)
from app.config.settings import (
    Settings,
)
from app.infrastructure.llm.bedrock_provider import (
    BedrockProvider,
)
from app.infrastructure.llm.ollama_provider import (
    OllamaProvider,
)


def create_llm(
    settings: Settings,
) -> LLMInterface:
    """
    Create the configured QuantMind LLM provider.

    Provider selection belongs in the composition layer,
    keeping application services and agents independent
    of concrete LLM infrastructure.
    """

    provider = settings.llm_provider.strip().lower()

    if provider == "ollama":

        return OllamaProvider(
            model=settings.llm_model,
            num_ctx=settings.llm_num_ctx,
        )

    if provider == "bedrock":

        return BedrockProvider(
            model_id=settings.bedrock_model_id,
            region=settings.bedrock_region,
        )

    raise ValueError(
        "Unsupported LLM provider: "
        f"{settings.llm_provider!r}. "
        "Expected 'ollama' or 'bedrock'."
    )