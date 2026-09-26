from app.application.embeddings.embedding_interface import (
    EmbeddingInterface,
)
from app.config.settings import (
    Settings,
)
from app.infrastructure.rag.bedrock_embedding_model import (
    BedrockEmbeddingModel,
)
from app.infrastructure.rag.ollama_embedding_model import (
    OllamaEmbeddingModel,
)


def create_embedding_model(
    settings: Settings,
) -> EmbeddingInterface:
    """
    Create the configured QuantMind embedding provider.

    Provider selection belongs in the composition layer,
    keeping retrieval logic independent of concrete
    embedding infrastructure.
    """

    provider = (
        settings.embedding_provider
        .strip()
        .lower()
    )

    if provider == "ollama":

        return OllamaEmbeddingModel(
            model=settings.embedding_model,
        )

    if provider == "bedrock":

        return BedrockEmbeddingModel(
            model_id=(
                settings.bedrock_embedding_model_id
            ),
            region=(
                settings.bedrock_embedding_region
            ),
            dimensions=(
                settings.bedrock_embedding_dimensions
            ),
        )

    raise ValueError(
        "Unsupported embedding provider: "
        f"{settings.embedding_provider!r}. "
        "Expected 'ollama' or 'bedrock'."
    )