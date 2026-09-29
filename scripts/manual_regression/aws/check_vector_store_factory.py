import os

from app.bootstrap.vector_store_factory import (
    create_vector_store,
)
from app.config.settings import Settings


# =========================================================
# Local
# =========================================================

os.environ[
    "QUANTMIND_VECTOR_STORE_PROVIDER"
] = "chroma"

local_settings = Settings()

local_store = create_vector_store(
    local_settings
)

print(
    "Local vector store:",
    type(local_store).__name__,
)


# =========================================================
# AWS
# =========================================================

os.environ[
    "QUANTMIND_VECTOR_STORE_PROVIDER"
] = "s3vectors"

aws_settings = Settings()

aws_store = create_vector_store(
    aws_settings
)

print(
    "AWS vector store:",
    type(aws_store).__name__,
)

print(
    "Vector bucket:",
    aws_store.vector_bucket_name,
)

print(
    "Vector index:",
    aws_store.index_name,
)

print(
    "Vector region:",
    aws_store.region,
)