from app.infrastructure.llm.bedrock_provider import BedrockProvider


provider = BedrockProvider()

print("Provider:", type(provider).__name__)
print("Model:", provider.model_id)
print("Region:", provider.region)
print("Client:", provider.client.meta.service_model.service_name)