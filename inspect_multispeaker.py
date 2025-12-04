import inspect
from google.genai import types

print("Inspect MultiSpeakerVoiceConfig:")
for name, obj in inspect.getmembers(types.MultiSpeakerVoiceConfig):
    if not name.startswith("_"):
        print(f"{name}: {obj}")

print("\nInspect SpeakerVoiceConfig:")
for name, obj in inspect.getmembers(types.SpeakerVoiceConfig):
    if not name.startswith("_"):
        print(f"{name}: {obj}")
