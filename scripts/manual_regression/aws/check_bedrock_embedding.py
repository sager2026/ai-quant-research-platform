import io
import json

from app.infrastructure.rag.bedrock_embedding_model import (
    BedrockEmbeddingModel,
)


class FakeBedrockClient:

    def __init__(self):
        self.last_request = None

    def invoke_model(self, **kwargs):
        self.last_request = kwargs

        fake_response = {
            "embedding": [
                0.10,
                0.20,
                0.30,
                0.40,
            ],
            "inputTextTokenCount": 4,
        }

        return {
            "body": io.BytesIO(
                json.dumps(
                    fake_response
                ).encode("utf-8")
            )
        }


fake_client = FakeBedrockClient()

model = BedrockEmbeddingModel(
    model_id="amazon.titan-embed-text-v2:0",
    region="us-east-2",
    dimensions=1024,
    client=fake_client,
)


# =========================================================
# Single embedding
# =========================================================

embedding = model.embed(
    "Apple reported higher revenue."
)

print(
    "Embedding:",
    embedding,
)


request_body = json.loads(
    fake_client.last_request["body"]
)

print(
    "Model:",
    fake_client.last_request["modelId"],
)

print(
    "Input:",
    request_body["inputText"],
)

print(
    "Dimensions:",
    request_body["dimensions"],
)

print(
    "Normalize:",
    request_body["normalize"],
)


# =========================================================
# Multiple embeddings
# =========================================================

embeddings = model.embed_many(
    [
        "Apple revenue increased.",
        "Apple faces supply-chain risks.",
    ]
)

print(
    "Embedding count:",
    len(embeddings),
)