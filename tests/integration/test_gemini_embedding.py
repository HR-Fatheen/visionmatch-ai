from dotenv import load_dotenv
from google import genai
import os
from app.services.gemini_embedding_provider import GeminiEmbeddingProvider


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

provider = GeminiEmbeddingProvider()

text = "A red fox standing in a forest."
token_count = client.models.count_tokens(
    model="gemini-embedding-2",
    contents=text,
)

print("Token count:", token_count.total_tokens)

result = provider.embed_text(text)

print("Model:", result.model_name)
print("Vector dimensions:", len(result.vector))
print("First 5 values:", result.vector[:5])
print("Input units:", result.input_units)

assert result.model_name == "gemini-embedding-2"
assert len(result.vector) > 0
assert all(isinstance(value, float) for value in result.vector)

print("Gemini embedding test: PASSED")