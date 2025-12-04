import os
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

print("Testing simple audio generation...")
try:
    response = client.models.generate_content(
        model='gemini-2.5-flash-preview-tts',
        contents="Hello, this is a test of the audio generation system.",
        config=types.GenerateContentConfig(
            response_modalities=['AUDIO']
        )
    )
    
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                raw_data = part.inline_data.data
                print(f"Data type: {type(raw_data)}")
                print(f"Raw Data Length: {len(raw_data)}")
                print(f"First 20 bytes: {raw_data[:20]}")
                
                # If it's bytes, it might be the raw audio OR base64 encoded bytes.
                # Let's try to write it directly first if it looks like audio (starts with RIFF for WAV).
                # Or try to decode if it looks like b64.
                
                try:
                    decoded_data = base64.b64decode(raw_data)
                    print(f"Decoded successfully. Length: {len(decoded_data)}")
                    with open("test_audio.wav", "wb") as f:
                        f.write(decoded_data)
                except Exception as e:
                    print(f"Decode failed: {e}")
                    print("Writing raw data...")
                    with open("test_audio.wav", "wb") as f:
                        f.write(raw_data)
            else:
                print(f"Text part: {part.text}")
    else:
        print("No candidates.")
        print(response)

except Exception as e:
    print(f"Error: {e}")
