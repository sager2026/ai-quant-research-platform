from app.infrastructure.llm.bedrock_provider import BedrockProvider


class FakeBedrockClient:
    def __init__(self):
        self.last_request = None

    def converse(self, **kwargs):
        self.last_request = kwargs

        return {
            "output": {
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "text": "QuantMind mock Bedrock response"
                        }
                    ],
                }
            },
            "stopReason": "end_turn",
            "usage": {
                "inputTokens": 10,
                "outputTokens": 5,
                "totalTokens": 15,
            },
        }


fake_client = FakeBedrockClient()

provider = BedrockProvider(
    model_id="amazon.nova-lite-v1:0",
    region="us-east-2",
    client=fake_client,
)

result = provider.generate(
    "Analyze AAPL."
)

print("Result:", result)

print(
    "Model:",
    fake_client.last_request["modelId"]
)

print(
    "Prompt:",
    fake_client.last_request["messages"][0]["content"][0]["text"]
)

print(
    "MaxTokens:",
    fake_client.last_request["inferenceConfig"]["maxTokens"]
)

print(
    "Temperature:",
    fake_client.last_request["inferenceConfig"]["temperature"]
)