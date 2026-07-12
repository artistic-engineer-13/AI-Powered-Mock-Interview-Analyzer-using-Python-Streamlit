from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("Testing models/gemini-3.5-flash...")

response = client.models.generate_content(
    model=os.getenv("GEMINI_MODEL", "models/gemini-3.5-flash"),
    contents="Say hello in one sentence."
)

print(response.text)