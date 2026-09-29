import os

from app.bootstrap.embedding_factory import (
    create_embedding_model,
)
from app.config.settings import (
    Settings,
)


# =========================================================
# Ollama
# =========================================================

os.environ[
    "QUANTMIND_EMBEDDING_PROVIDER"
] = "ollama"

ollama_settings = Settings()

ollama_embedding = create_embedding_model(
    settings=ollama_settings,
)

print(
    "Local embedding provider:",
    type(ollama_embedding).__name__,
)


# =========================================================
# Bedrock
# =========================================================

os.environ[
    "QUANTMIND_EMBEDDING_PROVIDER"
] = "bedrock"

bedrock_settings = Settings()

bedrock_embedding = create_embedding_model(
    settings=bedrock_settings,
)

print(
    "AWS embedding provider:",
    type(bedrock_embedding).__name__,
)

print(
    "Bedrock embedding model:",
    bedrock_embedding.model_id,
)

print(
    "Bedrock embedding region:",
    bedrock_embedding.region,
)

print(
    "Embedding dimensions:",
    bedrock_embedding.dimensions,
)