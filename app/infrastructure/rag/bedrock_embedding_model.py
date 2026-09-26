import json
from typing import Any

import boto3

from app.application.embeddings.embedding_interface import (
    EmbeddingInterface,
)


class BedrockEmbeddingModel(EmbeddingInterface):

    DEFAULT_MODEL_ID = "amazon.titan-embed-text-v2:0"
    DEFAULT_REGION = "us-east-2"
    DEFAULT_DIMENSIONS = 1024

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        region: str = DEFAULT_REGION,
        dimensions: int = DEFAULT_DIMENSIONS,
        client: Any | None = None,
    ):
        self.model_id = model_id
        self.region = region
        self.dimensions = dimensions

        self.client = client or boto3.client(
            "bedrock-runtime",
            region_name=region,
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:

        if not text or not text.strip():
            raise ValueError(
                "Text must not be empty."
            )

        body = {
            "inputText": text,
            "dimensions": self.dimensions,
            "normalize": True,
        }

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )

        payload = json.loads(
            response["body"].read()
        )

        return payload["embedding"]

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        return [
            self.embed(text)
            for text in texts
        ]