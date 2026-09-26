import os
from typing import Any

import boto3

from app.application.llm.llm_interface import LLMInterface


class BedrockProvider(LLMInterface):
    """
    Amazon Bedrock implementation of the QuantMind LLM interface.

    Authentication is intentionally not handled here.

    Local development:
        boto3 uses the normal AWS credential chain.

    ECS/Fargate:
        boto3 automatically obtains temporary credentials
        from the ECS Task Role.
    """

    DEFAULT_MODEL_ID = "amazon.nova-lite-v1:0"
    DEFAULT_REGION = "us-east-2"

    def __init__(
        self,
        model_id: str | None = None,
        region: str | None = None,
        client: Any | None = None,
    ):
        self.model_id = (
            model_id
            or os.getenv("QUANTMIND_BEDROCK_MODEL_ID")
            or self.DEFAULT_MODEL_ID
        )

        self.region = (
            region
            or os.getenv("AWS_REGION")
            or os.getenv("AWS_DEFAULT_REGION")
            or self.DEFAULT_REGION
        )

        self.client = client or boto3.client(
            "bedrock-runtime",
            region_name=self.region,
        )

    def generate(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("Prompt must not be empty.")

        response = self.client.converse(
            modelId=self.model_id,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt,
                        }
                    ],
                }
            ],
            inferenceConfig={
                "maxTokens": 1024,
                "temperature": 0.2,
            },
        )

        content = response["output"]["message"]["content"]

        for block in content:
            if "text" in block:
                text = block["text"].strip()
                return self._normalize_text(text)

        raise RuntimeError(
            "Bedrock returned no text content."
        )

    @staticmethod
    def _normalize_text(text: str) -> str:
        if not text:
            return text

        replacements = {
            "\u00e2\u0080\u0099": "\u2019",
            "\u00e2\u0080\u0098": "\u2018",
            "\u00e2\u0080\u009c": "\u201c",
            "\u00e2\u0080\u009d": "\u201d",
            "\u00e2\u0080\u0093": "\u2013",
            "\u00e2\u0080\u0094": "\u2014",
        }

        for corrupted, correct in replacements.items():
            text = text.replace(
                corrupted,
                correct,
            )

        return text