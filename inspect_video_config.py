
import google.genai.types as types

print("Fields in GenerateVideosConfig:")
for field in types.GenerateVideosConfig.model_fields.keys():
    print(f"- {field}")
