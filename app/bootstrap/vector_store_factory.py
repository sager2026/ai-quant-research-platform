from app.application.vectorstores.vector_store_interface import (
    VectorStoreInterface,
)
from app.config.settings import Settings
from app.infrastructure.rag.chroma_vector_store import (
    ChromaVectorStore,
)
from app.infrastructure.rag.s3_vector_store import (
    S3VectorStore,
)


def create_vector_store(
    settings: Settings,
) -> VectorStoreInterface:
    """
    Create the configured QuantMind vector-store provider.
    """

    provider = (
        settings.vector_store_provider
        .strip()
        .lower()
    )

    if provider == "chroma":

        return ChromaVectorStore(
            path=settings.chroma_path,
            collection_name=(
                settings.chroma_collection_name
            ),
        )

    if provider == "s3vectors":

        return S3VectorStore(
            vector_bucket_name=(
                settings.s3_vector_bucket_name
            ),
            index_name=(
                settings.s3_vector_index_name
            ),
            region=(
                settings.s3_vector_region
            ),
        )

    raise ValueError(
        "Unsupported vector-store provider: "
        f"{settings.vector_store_provider!r}. "
        "Expected 'chroma' or 's3vectors'."
    )