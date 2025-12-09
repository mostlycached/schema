import os
import subprocess
import time

def run_script(script_name):
    print(f"\n=== Running {script_name} ===")
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
    try:
        subprocess.run(["python3", script_path], check=True)
        print(f"=== {script_name} Completed ===")
    except subprocess.CalledProcessError as e:
        print(f"=== Error running {script_name}: {e} ===")
        exit(1)

def main():
    print("Starting Audiobook Production Pipeline...")
    
    # 1. Clean up old Speech files? 
    # The generate_audio_batch.py skips existing files.
    # Since text changed, we MUST remove old speech files (but keep music if valid).
    # Speech files are named `chapter_XX.mp3` or `preface.mp3`.
    # Music files are `chapter_XX_music.mp3`.
    # Merged files are `Chapter XX - Title.mp3`.
    
    # Let's delete the plain speech files to force regeneration.
    # Files: chapter_01.mp3, preface.mp3, etc.
    # CAREFUL: generate_audio_batch.py logic: output_filename = f"{base_name}.mp3"
    # base_name comes from chapter_XX_script.txt -> chapter_XX.
    
    audio_dir = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(audio_dir)
    for f in files:
        # Pattern match for speech files: 
        # Starts with 'chapter_' or 'preface', ends with '.mp3', 
        # DOES NOT contain 'music', DOES NOT contain ' - ' (final Title).
        if f.endswith(".mp3") and "music" not in f and " - " not in f:
             # Basic safety check
             if f.startswith("chapter_") or f.startswith("preface"):
                 print(f"Cleaning stale speech file: {f}")
                 os.remove(os.path.join(audio_dir, f))
    
    # 2. Generate Speech
    run_script("generate_audio_batch.py")
    
    # 3. Generate Music
    run_script("generate_music_batch.py")
    
    # 4. Merge
    run_script("merge_audio.py")
    
    print("\n=== Audiobook Production Complete! ===")

if __name__ == "__main__":
    main()
