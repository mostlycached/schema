import os
import json
import subprocess

def merge_audio(music_path, speech_path, output_path):
    """Merge music intro with speech using ffmpeg."""
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
        print(f"Error merging: {result.stderr}")
        return False

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "rich_audiobook_config.json")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    for chapter in config['chapters']:
        chapter_id = chapter['id']
        title = chapter['title']
        
        # Construct file names
        music_path = os.path.join(script_dir, f"{chapter_id}_music.mp3")
        speech_path = os.path.join(script_dir, f"{chapter_id}.mp3")
        
        # Format: "Rich Chapter 01 - The Women Notice You.mp3"
        chapter_num = chapter_id.replace("rich_chapter_", "")
        output_filename = f"Rich Chapter {chapter_num} - {title}.mp3"
        output_path = os.path.join(script_dir, output_filename)
        
        if not os.path.exists(music_path):
            print(f"Skipping {chapter_id} (No music file)")
            continue
            
        if not os.path.exists(speech_path):
            print(f"Skipping {chapter_id} (No speech file)")
            continue
        
        print(f"Merging {chapter_id}...")
        merge_audio(music_path, speech_path, output_path)
