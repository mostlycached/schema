import os
import subprocess
import json

def merge_audio():
    # Use paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "audiobook_config.json")
    output_dir = script_dir
    
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    chapters = config['chapters']
    
    for chapter in chapters:
        chapter_id = chapter['id']
        music_file = os.path.join(output_dir, f"{chapter_id}_music.mp3")
        speech_file = os.path.join(output_dir, f"{chapter_id}.mp3")
        # Construct descriptive filename: "Chapter XX - Title.mp3"
        # Handle "preface" case
        if chapter_id == "preface":
            output_filename = f"Preface - {chapter['title']}.mp3"
        else:
            # chapter_id is "chapter_XX"
            # We want "Chapter XX" (capitalized)
            chapter_prefix = chapter_id.replace("chapter_", "Chapter ")
            output_filename = f"{chapter_prefix} - {chapter['title']}.mp3"
            
        output_file = os.path.join(output_dir, output_filename)
        
        if not os.path.exists(music_file):
            print(f"Skipping {chapter_id}: Music file missing")
            continue
            
        if not os.path.exists(speech_file):
            print(f"Skipping {chapter_id}: Speech file missing")
            continue
            
        # if os.path.exists(output_file):
        #     print(f"Skipping {chapter_id}: Full audio already exists")
        #     continue
            
        print(f"Merging {chapter_id}...")
        
        # ffmpeg command to concatenate
        # ffmpeg -i music.mp3 -i speech.mp3 -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1[out]" -map "[out]" output.mp3
        cmd = [
            "ffmpeg",
            "-y", # Overwrite
            "-i", music_file,
            "-i", speech_file,
            "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]",
            "-map", "[out]",
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Successfully merged to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error merging {chapter_id}: {e}")

if __name__ == "__main__":
    merge_audio()
