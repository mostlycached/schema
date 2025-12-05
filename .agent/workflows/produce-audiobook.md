---
description: Produce a "Concept Album" audiobook with music intros and speech narration.
---

This workflow describes how to generate an audiobook where each chapter has a unique musical intro followed by the narration.

## Prerequisites
1.  **ElevenLabs API Key**: Ensure `ELEVENLABS_API_KEY` is set in your `.env` file.
2.  **ffmpeg**: Must be installed and available in your PATH.
3.  **Python Libraries**: `requests`, `python-dotenv`.

## 1. Configuration
Create or update `book/audiobook_config.json`. This file defines the chapters and their music prompts.

Format:
```json
{
    "project_name": "My Audiobook",
    "elevenlabs_model_id": "eleven_v3",
    "default_voice_id": "JBFqnCBsd6RMkjVDRZzb",
    "chapters": [
        {
            "id": "chapter_01",
            "title": "The Chapter Title",
            "file_path": "book/chapter_01.md",
            "music_prompt": "Description of the music style, instruments, and mood. Length: 2:15."
        }
    ]
}
```

## 2. Script Preparation
Convert your markdown chapters into speech-optimized scripts.
*   **Location**: Save as `.txt` files in `book/scripts/` (e.g., `book/scripts/chapter_01_script.txt`).
*   **Format**:
    *   Use **CAPS** for emphasis.
    *   Use `...` for pauses.
    *   Use allowed tags: `[whispers]`, `[sighs]`, `[exhales]`, `[laughs]`, `[sarcastic]`, `[curious]`, `[excited]`, `[crying]`, `[snorts]`, `[mischievously]`.

## 3. Generate Music
Run the batch music generation script. This uses the `v1/music` endpoint to generate full-length tracks (~2:15m).

```bash
python3 book/generate_music_batch.py
```

## 4. Generate Speech
Run the batch speech generation script. This uses the `eleven_v3` model.

```bash
python3 book/generate_audio_batch.py
```

## 5. Merge Audio
Merge the music intro and speech narration into the final audiobook file.
The output files will be named `Chapter XX - Title.mp3` in the `book/` directory.

```bash
python3 book/merge_audio.py
```
