import ollama


class OllamaEmbeddingModel:

    def __init__(
        self,
        model: str = "embeddinggemma",
    ):
        self.model = model

    def embed(
        self,
        text: str,
    ) -> list[float]:

        response = ollama.embed(
            model=self.model,
            input=text,
        )

        return response["embeddings"][0]

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        response = ollama.embed(
            model=self.model,
            input=texts,
        )

        return response["embeddings"]