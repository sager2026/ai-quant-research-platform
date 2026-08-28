from ollama import chat

from app.application.llm.llm_interface import (
    LLMInterface,
)


class OllamaProvider(LLMInterface):
    """
    Ollama-backed implementation of the LLM interface.

    num_ctx controls the runtime context window allocated
    by Ollama for each generation request.
    """

    def __init__(
        self,
        model: str = "qwen3:8b",
        num_ctx: int = 16384,
    ):
        self.model = model
        self.num_ctx = num_ctx

    def generate(
        self,
        prompt: str,
    ) -> str:

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            options={
                "num_ctx": self.num_ctx,
            },
        )

        return response[
            "message"
        ][
            "content"
        ]