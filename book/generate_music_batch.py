import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv('/Users/hprasann/Documents/GitHub/schema/.env')

API_KEY = os.getenv("ELEVENLABS_API_KEY")

def generate_music(prompt, duration, output_path):
    # Correct endpoint for long-form music
    url = "https://api.elevenlabs.io/v1/music"
    
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Use music_length_ms (duration in milliseconds)
    # 135 seconds = 135000 ms
    duration_ms = duration * 1000
    
    data = {
        "prompt": prompt,
        "music_length_ms": duration_ms,
        "prompt_influence": 0.5
    }
    
    print(f"Generating music for prompt: {prompt[:50]}... ({duration}s)", flush=True)
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=300) # 5 minute timeout
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
    # Use paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "audiobook_config.json")
    output_dir = script_dir
    
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    for chapter in config['chapters']:
        chapter_id = chapter['id']
        prompt = chapter['music_prompt']
        
        # We want full songs now. Let's aim for ~2:15 (135 seconds) as a good average.
        # The prompt text mentions specific lengths (e.g. 2:30), but for batch simplicity/quota safety,
        # let's stick to a safe high number like 135s.
        duration = 135 
        
        output_filename = f"{chapter_id}_music.mp3"
        output_path = os.path.join(output_dir, output_filename)
        
        # Force overwrite because previous files were too short (22s)
        # But maybe check size? 22s is ~350KB. 135s should be ~2MB.
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 1000000: # If > 1MB, assume it's already the long version
                print(f"Skipping {chapter_id} (Long music already exists)")
                continue
            else:
                print(f"Regenerating {chapter_id} (Existing file is too short: {file_size} bytes)")
        
        success = generate_music(prompt, duration, output_path)
        
        if success:
            time.sleep(1) # Avoid rate limits
