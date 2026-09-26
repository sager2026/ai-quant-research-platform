import chromadb

from app.application.vectorstores.vector_store_interface import (
    VectorStoreInterface,
)


class ChromaVectorStore(VectorStoreInterface):

    def __init__(
        self,
        path: str = "data/chroma",
        collection_name: str = "quantmind_filings",
    ):
        self.client = chromadb.PersistentClient(
            path=path
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
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

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        ticker: str,
        filing_types: list[str] | None = None,
        top_k: int = 5,
    ) -> list[dict]:

        where = {
            "ticker": ticker.upper()
        }

        if filing_types:

            normalized_filing_types = [
                filing_type.upper()
                for filing_type in filing_types
            ]

            where = {
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

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k,
            where=where,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

        matches = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            matches.append(
                {
                    "document": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        return matches