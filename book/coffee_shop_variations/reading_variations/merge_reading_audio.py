import os
import json
import subprocess
import re

def merge_audio(music_path, speech_path, output_path):
    """Merge music intro with speech using ffmpeg.
    
    Structure per PRODUCTION_WORKFLOW.md:
    - Music intro plays
    - Speech follows
    - 3 seconds silence at end
    """
    cmd = [
        'ffmpeg', '-y',
        '-i', music_path,
        '-i', speech_path,
        '-f', 'lavfi', '-t', '3', '-i', 'anullsrc=r=44100:cl=stereo',
        '-filter_complex', '[0][1][2]concat=n=3:v=0:a=1[out]',
        '-map', '[out]',
        '-acodec', 'libmp3lame',
        '-q:a', '2',
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Created: {output_path}")
        return True
    else:
        print(f"Error merging {output_path}: {result.stderr}")
        return False

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "reading_audiobook_config.json")
    audio_dir = os.path.join(script_dir, "audio")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    for chapter in config['chapters']:
        chapter_id = chapter['id']
        title = chapter['title']
        
        # Construct file names in audio/ subdirectory
        music_path = os.path.join(audio_dir, f"{chapter_id}_music.mp3")
        speech_path = os.path.join(audio_dir, f"{chapter_id}.mp3")
        
        # Friendly output name
        # e.g., "Reading Chapter 01 - Serres Climbing.mp3"
        # Extract number if possible or just use title
        
        # Helper to get number from ID like "reading_chapter_01_serres_climbing" -> "01"
        match = re.search(r'chapter_(\d+)', chapter_id)
        num = match.group(1) if match else "XX"
        
        clean_title = title.replace(":", " -")
        output_filename = f"Reading Chapter {num} - {clean_title}.mp3"
        output_path = os.path.join(audio_dir, output_filename)
        
        if not os.path.exists(music_path):
            print(f"Skipping {chapter_id} (No music file)")
            continue
            
        if not os.path.exists(speech_path):
            print(f"Skipping {chapter_id} (No speech file)")
            continue
        
        print(f"Merging {chapter_id}...")
        merge_audio(music_path, speech_path, output_path)

import re
