import google.generativeai as genai
import inspect

print("Attributes of genai:")
for name, obj in inspect.getmembers(genai):
    if not name.startswith("_"):
        print(name)

print("\nChecking for 'veo' or 'video' in model names (listing all):")
try:
    for m in genai.list_models():
        print(f"{m.name} - Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")
