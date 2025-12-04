from google.genai import types

print("MultiSpeakerVoiceConfig fields:")
try:
    print(types.MultiSpeakerVoiceConfig.model_fields.keys())
except:
    pass

print("\nSpeakerVoiceConfig fields:")
try:
    print(types.SpeakerVoiceConfig.model_fields.keys())
except:
    pass
