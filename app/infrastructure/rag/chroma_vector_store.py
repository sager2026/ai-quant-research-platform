import chromadb


class ChromaVectorStore:

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
        top_k: int = 5,
    ) -> list[dict]:

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k,
            where={
                "ticker": ticker.upper()
            },
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