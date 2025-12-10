import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

API_KEY = os.getenv("ELEVENLABS_API_KEY")

def generate_music(prompt, duration, output_path):
    url = "https://api.elevenlabs.io/v1/music"
    
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    duration_ms = duration * 1000
    
    data = {
        "prompt": prompt,
        "music_length_ms": duration_ms,
        "prompt_influence": 0.5
    }
    
    print(f"Generating music: {prompt[:60]}... ({duration}s)", flush=True)
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=300)
    except requests.exceptions.Timeout:
        print("Error: Request timed out", flush=True)
        return False
    except Exception as e:
        print(f"Error: {e}", flush=True)
        return False
    
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Saved to {output_path}", flush=True)
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}", flush=True)
        return False

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "audiobook_config.json")
    output_dir = script_dir
    
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    for chapter in config['chapters']:
        chapter_id = chapter['id']
        prompt = chapter['music_prompt']
        
        # Target ~2:00-2:15 (120 seconds)
        duration = 120
        
        output_filename = f"{chapter_id}_music.mp3"
        output_path = os.path.join(output_dir, output_filename)
        
        # Skip if already generated (>1MB = long version)
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 1000000:
                print(f"Skipping {chapter_id} (Music already exists)")
                continue
            else:
                print(f"Regenerating {chapter_id} (Existing file too short)")
        
        success = generate_music(prompt, duration, output_path)
        
        if success:
            time.sleep(2)  # Avoid rate limits
