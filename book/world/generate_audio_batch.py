import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb" # Using the default voice ID from config
MODEL_ID = "eleven_v3"

def generate_audio(text, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }
    
    data = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Audio saved to {output_path}")
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    # Use paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(script_dir, "scripts")
    output_dir = script_dir
    
    # Get all script files
    script_files = [f for f in os.listdir(scripts_dir) if f.endswith(".txt")]
    script_files.sort()
    
    for script_file in script_files:
        script_path = os.path.join(scripts_dir, script_file)
        
        # Determine output filename (e.g., chapter_01_script.txt -> chapter_01_tuareg.mp3)
        # We need to map script names to meaningful audio names or just use the script basename
        # For simplicity, let's use the script basename but change extension to .mp3
        base_name = os.path.splitext(script_file)[0]
        # Remove "_script" suffix if present
        if base_name.endswith("_script"):
            base_name = base_name[:-7]
            
        output_filename = f"{base_name}.mp3"
        output_path = os.path.join(output_dir, output_filename)
        
        # Check if audio already exists
        if os.path.exists(output_path):
            print(f"Skipping {script_file} (Audio already exists at {output_filename})")
            continue
            
        print(f"Processing {script_file}...")
        
        try:
            with open(script_path, 'r') as f:
                text = f.read()
            
            success = generate_audio(text, output_path)
            
            if success:
                # Sleep to avoid rate limits if necessary
                time.sleep(1)
                
        except Exception as e:
            print(f"Failed to process {script_file}: {e}")
