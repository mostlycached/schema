import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv('/Users/hprasann/Documents/GitHub/schema/.env')

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
        "prompt_influence": 0.75
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
    config_path = os.path.join(script_dir, "reading_audiobook_config.json")
    output_dir = script_dir
    
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    for chapter in config['chapters']:
        chapter_id = chapter['id']
        prompt = chapter['music_prompt']
        
        # 2:30 minutes to cover the full text comfortably (approx 600-800 words is ~4-5 mins usually, but these are condensed or partial)
        # Wait, 700 words at 150wpm is 4.6 mins.
        # But our condensed scripts are usually shorter.
        # Earlier chapters were ~600 words.
        # ElevenLabs max duration is often limited.
        # Previous successful generations used 120s (2 mins).
        # We'll stick to 120s for now, and loop/stretch if needed, or assume the intro/outro format where music is just intro.
        # Actually, the user wants "Reading-Modulated Lo-Fi", which implies background music?
        # The prompt says "Music Intro" in previous tasks.
        # But here the concept is "container modulated by reading".
        # If it's pure background, we need longer tracks or looping.
        # For this prototype, I'll generate 2-minute "Textures" that can be used as Intros or partial beds.
        duration = 120
        
        output_filename = f"{chapter_id}_music.mp3"
        output_path = os.path.join(output_dir, output_filename)
        
        if os.path.exists(output_path):
             # Check if valid size
            file_size = os.path.getsize(output_path)
            if file_size > 1000000:
                print(f"Skipping {chapter_id} (Music already exists)")
                continue
        
        success = generate_music(prompt, duration, output_path)
        
        if success:
            time.sleep(2)
