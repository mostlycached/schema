import os
import json
import subprocess

def merge_audio(music_path, speech_path, output_path):
    """Merge music intro with speech narration using ffmpeg."""
    
    # Create a 3-second silence to append at the end
    # Concatenate: [Music] -> [Speech] -> [Silence]
    
    cmd = [
        'ffmpeg', '-y',
        '-i', music_path,
        '-i', speech_path,
        '-f', 'lavfi', '-t', '3', '-i', 'anullsrc=r=44100:cl=stereo',
        '-filter_complex', '[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]',
        '-map', '[out]',
        '-c:a', 'libmp3lame',
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
    config_path = os.path.join(script_dir, "audiobook_config.json")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    for chapter in config['chapters']:
        chapter_id = chapter['id']
        title = chapter['title']
        
        # Extract chapter number for filename
        chapter_num = chapter_id.replace('chapter_', '')
        
        music_path = os.path.join(script_dir, f"{chapter_id}_music.mp3")
        speech_path = os.path.join(script_dir, f"{chapter_id}.mp3")
        output_filename = f"Chapter {chapter_num} - {title}.mp3"
        output_path = os.path.join(script_dir, output_filename)
        
        # Check if source files exist
        if not os.path.exists(music_path):
            print(f"Skipping {chapter_id}: Music file not found")
            continue
        if not os.path.exists(speech_path):
            print(f"Skipping {chapter_id}: Speech file not found")
            continue
            
        # Skip if output already exists
        if os.path.exists(output_path):
            print(f"Skipping {chapter_id}: Output already exists")
            continue
            
        print(f"Merging {chapter_id}...")
        merge_audio(music_path, speech_path, output_path)
