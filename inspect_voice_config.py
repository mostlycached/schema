from google.genai import types

print("VoiceConfig fields:")
try:
    print(types.VoiceConfig.model_fields.keys())
except:
    pass

print("\nSpeechConfig fields:")
try:
    print(types.SpeechConfig.model_fields.keys())
except:
    pass
