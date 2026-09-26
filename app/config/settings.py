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

    llm_provider: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_LLM_PROVIDER",
            "ollama",
        )
    )

    bedrock_model_id: str = field(
    default_factory=lambda: os.getenv(
        "QUANTMIND_BEDROCK_MODEL_ID",
        "us.amazon.nova-lite-v1:0",
        )
    )


    bedrock_region: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_BEDROCK_REGION",
            os.getenv(
                "AWS_REGION",
                "us-east-2",
            ),
        )
    )

    embedding_provider: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_EMBEDDING_PROVIDER",
            "ollama",
        )
    )

    bedrock_embedding_model_id: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_BEDROCK_EMBEDDING_MODEL_ID",
            "amazon.titan-embed-text-v2:0",
        )
    )

    bedrock_embedding_region: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_BEDROCK_EMBEDDING_REGION",
            os.getenv(
                "AWS_REGION",
                "us-east-2",
            ),
        )
    )

    bedrock_embedding_dimensions: int = field(
        default_factory=lambda: int(
            os.getenv(
                "QUANTMIND_BEDROCK_EMBEDDING_DIMENSIONS",
                "1024",
            )
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

    ollama_host: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_OLLAMA_HOST",
            "http://localhost:11434",
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

    vector_store_provider: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_VECTOR_STORE_PROVIDER",
            "chroma",
        )
    )

    s3_vector_bucket_name: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_S3_VECTOR_BUCKET",
            "quantmind-sec-vectors",
        )
    )

    s3_vector_index_name: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_S3_VECTOR_INDEX",
            "sec-filings-titan-v2-1024",
        )
    )

    s3_vector_region: str = field(
        default_factory=lambda: os.getenv(
            "QUANTMIND_S3_VECTOR_REGION",
            os.getenv(
                "AWS_REGION",
                "us-east-2",
            ),
        )
    )

@lru_cache
def get_settings() -> Settings:
    """
    Return one cached Settings instance per Python process.
    """

    return Settings()
