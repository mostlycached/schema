import os
import base64
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

def run_podcast_simulation():
    print("Initializing Experiment D: The Podcast Simulation")
    print("-----------------------------------------------")

    # Step 1: Generate the Script
    print("Generating Podcast Script...")
    
    prompt_script = """
    Write a short, engaging podcast script (approx 2 minutes spoken) between two hosts:
    
    HOST (Alex): Enthusiastic, high energy, loves technology and simple explanations.
    GUEST (Dr. V): Deep, philosophical, slightly skeptical, obsessed with complexity and emergence.
    
    Topic: Valentino Braitenberg's Vehicles and the idea that "complexity is an illusion".
    
    The script should be a dialogue. 
    Format:
    Alex: [Text]
    Dr. V: [Text]
    """
    
    response_script = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt_script
    )
    
    script_text = response_script.text
    print("\n--- SCRIPT START ---")
    print(script_text)
    print("--- SCRIPT END ---\n")

    # Step 2: Generate Audio
    print("Generating Audio (this may take a moment)...")
    
    # We need to guide the model to use two voices.
    # The prompt for TTS should include the script and instructions on voices.
    
    tts_prompt = f"""
    Generate a podcast audio file for the following script.
    Use two distinct voices:
    - Voice 1 (Alex): Energetic, American male.
    - Voice 2 (Dr. V): Calm, Deep, British male (or distinct from Voice 1).
    
    Script:
    {script_text}
    """
    
    try:
        response_audio = client.models.generate_content(
            model='gemini-2.5-flash-preview-tts',
            contents=tts_prompt,
            config=types.GenerateContentConfig(
                response_mime_type='audio/wav'
            )
        )
        
        # Check if we got audio bytes
        if response_audio.bytes:
            print("Audio bytes received. Saving to podcast_simulation.wav...")
            with open("podcast_simulation.wav", "wb") as f:
                f.write(response_audio.bytes)
            print("Audio saved successfully!")
        elif response_audio.candidates and response_audio.candidates[0].content.parts:
             # Sometimes it's in parts
             for part in response_audio.candidates[0].content.parts:
                 if part.inline_data:
                     print("Audio inline data received. Saving...")
                     with open("podcast_simulation.wav", "wb") as f:
                         f.write(base64.b64decode(part.inline_data.data)) # It might be already bytes or b64
                     print("Audio saved.")
                     break
        else:
            print("No audio data found in response.")
            print(response_audio)

    except Exception as e:
        print(f"Error generating audio: {e}")

if __name__ == "__main__":
    run_podcast_simulation()
