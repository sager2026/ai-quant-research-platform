import os

from app.bootstrap.llm_factory import (
    create_llm,
)
from app.config.settings import (
    Settings,
)


# =========================================================
# Ollama
# =========================================================

os.environ["QUANTMIND_LLM_PROVIDER"] = "ollama"

ollama_settings = Settings()

ollama_llm = create_llm(
    settings=ollama_settings,
)

print(
    "Local provider:",
    type(ollama_llm).__name__,
)


# =========================================================
# Bedrock
# =========================================================

os.environ["QUANTMIND_LLM_PROVIDER"] = "bedrock"

bedrock_settings = Settings()

bedrock_llm = create_llm(
    settings=bedrock_settings,
)

print(
    "AWS provider:",
    type(bedrock_llm).__name__,
)

print(
    "Bedrock model:",
    bedrock_llm.model_id,
)

print(
    "Bedrock region:",
    bedrock_llm.region,
)