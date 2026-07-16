from ollama import chat

from app.application.llm.llm_interface import LLMInterface


class OllamaProvider(LLMInterface):

    def __init__(self, model: str = "qwen3:8b"):
        self.model = model

    def generate(self, prompt: str) -> str:

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]