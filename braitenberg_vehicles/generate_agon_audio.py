import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

def run_agon_audio():
    print("Generating Agon Audio Simulation (Multi-Speaker with Tags)")
    print("--------------------------------------------------------")

    # Step 1: Generate the Dialogue
    print("Generating Dialogue...")
    
    prompt_dialogue = """
    Write a short, intense, realistic dialogue (approx 1 minute spoken) set in a DARK INTERROGATION ROOM.
    
    1. Person A (Aggressor): A corrupt Detective. Loud, aggressive, slamming the table (implied). Wants a confession NOW.
    2. Person B (Coward): The Suspect. Terrified, trembling, barely able to speak. Wants to disappear.
    
    The Detective is trying to break the Suspect. The Suspect is shutting down.
    
    CRITICAL INSTRUCTIONS FOR AUDIO GENERATION:
    1. Use the following tags to control pacing and volume:
       - [short pause], [medium pause], [long pause]
       - [shouting] (for Detective's screaming)
       - [whispering] (for Suspect's terrified answers)
       - [sigh], [breath] (for reactions)
    2. PAUSES ARE CRITICAL. Insert [long pause] between EVERY speaker turn. We need uncomfortable silence.
    3. Make it sound GRITTY and REAL.
    
    Format:
    Aggressor: [shouting] [Text] [long pause]
    Coward: [whispering] [Text] [long pause]
    """
    
    response_script = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt_dialogue
    )
    
    script_text = response_script.text
    print("\n--- DIALOGUE START ---")
    print(script_text)
    print("--- DIALOGUE END ---\n")

    # Step 2: Generate Audio
    print("Generating Audio...")
    
    try:
        response_audio = client.models.generate_content(
            model='gemini-2.5-flash-preview-tts',
            contents=script_text,
            config=types.GenerateContentConfig(
                response_modalities=['AUDIO'],
                speech_config=types.SpeechConfig(
                    multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                        speaker_voice_configs=[
                            types.SpeakerVoiceConfig(
                                speaker="Aggressor",
                                voice_config=types.VoiceConfig(
                                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                        voice_name="Charon" # Deep Male
                                    )
                                )
                            ),
                            types.SpeakerVoiceConfig(
                                speaker="Coward",
                                voice_config=types.VoiceConfig(
                                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                        voice_name="Kore" # Female
                                    )
                                )
                            )
                        ]
                    )
                )
            )
        )
        
        print(f"Response Candidates: {len(response_audio.candidates)}")
        if response_audio.candidates:
            for i, candidate in enumerate(response_audio.candidates):
                for j, part in enumerate(candidate.content.parts):
                    if part.inline_data:
                        raw_data = part.inline_data.data
                        print(f"  Part {j} Audio Data Length: {len(raw_data)} bytes")
                        with open("agon_simulation.wav", "wb") as f:
                            f.write(raw_data)
                        print("  Audio saved to agon_simulation.wav")
                    else:
                        print(f"  Part {j} Text: {part.text}")
        else:
            print("No candidates found.")
            print(response_audio)

    except Exception as e:
        print(f"Error generating audio: {e}")

if __name__ == "__main__":
    run_agon_audio()
