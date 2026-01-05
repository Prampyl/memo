
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Skipping probe, no key.")
    exit(0)

client = genai.Client(api_key=api_key)

print("Client.models attributes:")
print(dir(client.models))

try:
    print("\nAttempting basic embedding:")
    # Trying the most logical method name
    resp = client.models.embed_content(
        model="models/text-embedding-004",
        contents="Hello world"
    )
    print("Success! Embedding length:", len(resp.embeddings[0].values))
except Exception as e:
    print("Embedding failed:", e)

