import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))


scenes = [
    {
        "name": "scene_1_setup",
        "prompt": "Cinematic wide shot, black and white, high contrast. A desolate grey road with a single bus stop bench. A woman in a large grey coat sits huddled on the far right. A man in a rumpled suit walks briskly from the left, humming. Beckett style, surreal, minimalist, 35mm film grain."
    },
    {
        "name": "scene_2_invasion",
        "prompt": "Medium shot. The man sits uncomfortably close to the woman on the bench. He has a wide, manic, predatory smile. She looks terrified and slides away. The background is a flat, featureless grey fog. Intense, psychological tension, cinematic lighting."
    },
    {
        "name": "scene_3_chase",
        "prompt": "Wide shot. The man is running in a tight circle around the woman, waving his arms wildly. She is curled into a ball on the ground, covering her ears. The lighting is harsh and flickering. Surreal, avant-garde film style, experimental cinema."
    },
    {
        "name": "scene_4_silence",
        "prompt": "Close up on the man. He looks defeated, sad, head in hands. In the background, out of focus, the woman lifts her head and looks at him with a mix of fear and curiosity. Soft, melancholic lighting. 35mm film grain, emotional."
    }
]

def generate_scenes():
    print("Generating videos for 'The Distance' with Veo 3.1...")
    
    for scene in scenes:
        print(f"\n--- Generating {scene['name']} ---")
        print(f"Prompt: {scene['prompt']}")
        
        max_retries = 5
        retry_delay = 60
        
        for attempt in range(max_retries):
            try:
                operation = client.models.generate_videos(
                    model='veo-3.1-generate-preview',
                    prompt=scene['prompt'],
                    config=types.GenerateVideosConfig(
                        number_of_videos=1,
                        generate_audio=True,
                    )
                )
                
                print(f"Operation Name: {operation.name}")
                
                # Poll for completion
                while True:
                    print("Polling operation status...")
                    try:
                        op_status = client.operations.get(operation)
                    except Exception as e:
                        if "429" in str(e):
                            print("Rate limit hit during polling. Sleeping 60s...")
                            time.sleep(60)
                            continue
                        raise e
                    
                    if op_status.done:
                        print("Operation completed.")
                        if op_status.error:
                            print(f"Operation failed with error: {op_status.error}")
                        else:
                            response = op_status.result
                            
                            if response and response.generated_videos:
                                video = response.generated_videos[0]
                                if video.video.video_bytes:
                                    filename = f"{scene['name']}.mp4"
                                    print(f"Video bytes received. Saving to {filename}...")
                                    with open(filename, "wb") as f:
                                        f.write(video.video.video_bytes)
                                    print(f"Video saved: {filename}")
                                elif video.video.uri:
                                    print(f"Video URI received: {video.video.uri}")
                                else:
                                    print("No video bytes or URI found in result.")
                                    print(f"Video object: {video}")
                            else:
                                print("No generated videos in result.")
                                print(response)
                        break
                    
                    print("Operation still running. Sleeping 10s...")
                    time.sleep(10)
                
                # If we get here, success (or failed operation but not exception). Break retry loop.
                break
                
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print(f"Rate limit hit (Attempt {attempt+1}/{max_retries}). Sleeping {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2 # Exponential backoff
                else:
                    print(f"Error generating {scene['name']}: {e}")
                    break # Don't retry other errors
            
        # Sleep between scenes to avoid rate limits
        print("Sleeping for 60 seconds before next scene...")
        time.sleep(60)

if __name__ == "__main__":
    generate_scenes()
