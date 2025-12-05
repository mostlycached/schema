import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import time

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_KEY")

if not api_key:
    print("Error: GEMINI_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

# Artifacts directory
output_dir = "/Users/hprasann/.gemini/antigravity/brain/9e202ce4-e305-48c1-ac01-6e3fb480a175"
os.makedirs(output_dir, exist_ok=True)

# Image prompts
images_to_generate = [
    {
        "name": "imperial_eunuch_realistic",
        "prompt": "A hyper-realistic photograph of a man in a traditional silk robe standing in a courtyard with red walls. He holds a small wooden box. Atmospheric lighting."
    },
    {
        "name": "imperial_eunuch_sketch",
        "prompt": "A simple pencil sketch of a bamboo flute. Wind is blowing through it. Minimalist style."
    }
]

# Generation loop
model_name = "models/gemini-2.0-flash-exp-image-generation"
print(f"Using model: {model_name}")
model = genai.GenerativeModel(model_name)

for img_data in images_to_generate:
    print(f"Generating {img_data['name']}...")
    try:
        response = model.generate_content("Generate an image of: " + img_data['prompt'])
        
        # Check if response has parts and if they are images
        if not response.parts:
            print(f"No parts in response for {img_data['name']}")
            print(response)
            continue

        # Assuming the first part is the image data if successful
        # This part is speculative on the response structure for Imagen via this SDK
        # We will try to save it if it looks like image data, or print it to debug
        
        timestamp = int(time.time() * 1000)
        filename = f"{img_data['name']}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)

        # For Gemini API, images might be returned as inline_data
        # We need to handle the response object correctly. 
        # Since I am not 100% sure of the object structure for Imagen on this specific SDK version,
        # I will try to inspect it if standard access fails.
        
        # Try to access the image bytes directly if possible
        # In some versions, response.text gives text, but for images?
        
        # Let's try to iterate parts and save if it's a blob
        saved = False
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                img_data_bytes = part.inline_data.data
                # It might be base64 encoded or raw bytes? 
                # usually it's raw bytes in the proto, but let's check mime_type
                import base64
                # If it's already bytes, good. If it's a proto object, we access .data
                
                # Actually, let's use the PIL to save from bytes
                from io import BytesIO
                # part.inline_data.data is likely bytes
                img = Image.open(BytesIO(img_data_bytes))
                img.save(filepath)
                print(f"Saved to {filepath}")
                saved = True
                break
        
        if not saved:
             print(f"Could not find image data in response for {img_data['name']}")
             print(f"Response candidates: {response.candidates}")

    except Exception as e:
        print(f"Failed to generate {img_data['name']}: {e}")
        import traceback
        traceback.print_exc()
