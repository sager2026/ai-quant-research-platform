import os

from dataclasses import dataclass, field
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    """
    Runtime configuration for QuantMind.

    Values may be supplied through environment variables.
    Safe development defaults are provided for local use.
    """

    forecast_model_name: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_FORECAST_MODEL",
            "transformer",
        )
    )

    llm_model: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_LLM_MODEL",
            "qwen3:8b",
        )
    )

    llm_num_ctx: int = field(
        default_factory=lambda: int(
            os.getenv(
                "QUANTMIND_LLM_NUM_CTX",
                "16384",
            )
        )
    )

    embedding_model: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_EMBEDDING_MODEL",
            "embeddinggemma",
        )
    )

    chroma_path: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_CHROMA_PATH",
            "data/chroma",
        )
    )

    chroma_collection_name: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_CHROMA_COLLECTION",
            "quantmind_filings",
        )
    )

    retrieval_top_k: int = field(
        default_factory=lambda: int(
            os.getenv(
                "QUANTMIND_RETRIEVAL_TOP_K",
                "5",
            )
        )
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return one cached Settings instance per Python process.
    """

    return Settings()