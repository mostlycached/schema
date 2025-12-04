import os
import inspect
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

print("Checking client.models methods:")
for name, _ in inspect.getmembers(client.models):
    if "audio" in name or "speech" in name or "generate" in name:
        print(name)

print("\nChecking types for Audio/Speech configs:")
for name, _ in inspect.getmembers(genai.types):
    if "Audio" in name or "Speech" in name or "Voice" in name:
        print(name)
