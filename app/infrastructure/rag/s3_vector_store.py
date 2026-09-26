from typing import Any

import boto3

from app.application.vectorstores.vector_store_interface import (
    VectorStoreInterface,
)


class S3VectorStore(VectorStoreInterface):

    MAX_BATCH_SIZE = 500

    def __init__(
        self,
        vector_bucket_name: str,
        index_name: str,
        region: str = "us-east-2",
        client: Any | None = None,
    ):
        self.vector_bucket_name = vector_bucket_name
        self.index_name = index_name
        self.region = region

        self.client = client or boto3.client(
            "s3vectors",
            region_name=region,
        )

    def add(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:

        if not documents:
            return

        if not (
            len(ids)
            == len(documents)
            == len(embeddings)
            == len(metadatas)
        ):
            raise ValueError(
                "ids, documents, embeddings, and "
                "metadatas must have the same length."
            )

        vectors = []

        for (
            vector_id,
            document,
            embedding,
            metadata,
        ) in zip(
            ids,
            documents,
            embeddings,
            metadatas,
        ):

            stored_metadata = dict(metadata)

            # Keep source chunk with the vector.
            stored_metadata["document"] = document

            vectors.append(
                {
                    "key": vector_id,
                    "data": {
                        "float32": [
                            float(value)
                            for value in embedding
                        ]
                    },
                    "metadata": stored_metadata,
                }
            )

        for start in range(
            0,
            len(vectors),
            self.MAX_BATCH_SIZE,
        ):

            batch = vectors[
                start:
                start + self.MAX_BATCH_SIZE
            ]

            self.client.put_vectors(
                vectorBucketName=(
                    self.vector_bucket_name
                ),
                indexName=self.index_name,
                vectors=batch,
            )

    def search(
        self,
        query_embedding: list[float],
        ticker: str,
        filing_types: list[str] | None = None,
        top_k: int = 5,
    ) -> list[dict]:

        metadata_filter = {
            "ticker": ticker.upper()
        }

        if filing_types:

            normalized_filing_types = [
                filing_type.upper()
                for filing_type in filing_types
            ]

            metadata_filter = {
                "$and": [
                    {
                        "ticker": ticker.upper()
                    },
                    {
                        "filing_type": {
                            "$in": normalized_filing_types
                        }
                    },
                ]
            }

        response = self.client.query_vectors(
            vectorBucketName=(
                self.vector_bucket_name
            ),
            indexName=self.index_name,
            queryVector={
                "float32": [
                    float(value)
                    for value in query_embedding
                ]
            },
            topK=top_k,
            filter=metadata_filter,
            returnDistance=True,
            returnMetadata=True,
        )

        matches = []

        for vector in response.get(
            "vectors",
            [],
        ):

            metadata = dict(
                vector.get(
                    "metadata",
                    {},
                )
            )

            document = metadata.pop(
                "document",
                "",
            )

            matches.append(
                {
                    "document": document,
                    "metadata": metadata,
                    "distance": vector.get(
                        "distance"
                    ),
                }
            )

        return matches