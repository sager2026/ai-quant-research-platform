from openai import OpenAI

from app.application.llm.llm_interface import LLMInterface


class OpenAIProvider(LLMInterface):

    def __init__(self, api_key: str):

        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str) -> str:

        response = self.client.responses.create(
            model="gpt-5",
            input=prompt
        )

        return response.output_text