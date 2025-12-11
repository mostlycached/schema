---
description: Produce a complete audiobook album from a world or user-specified concept
---

# Produce Room Workflow

This workflow produces a complete audiobook album (10 variations + cover art) from either a world in `WORLDS.md` or a user-specified concept.

## Prerequisites

- ElevenLabs API key set in `.env` as `ELEVENLABS_API_KEY`
- `ffmpeg` installed (`brew install ffmpeg` on macOS)
- Python 3.x with `requests` and `python-dotenv`

---

## Phase 1: World Selection & Exploration

### Step 1: Identify the Base World

If the user provides a world from `WORLDS.md`:
1. Read `world/WORLDS.md` and locate the specified world
2. Extract its key properties: Genealogy, Tension, Iteration, Inhabitants, Phenomenology, Structure, System

If the user provides a custom concept:
1. Create a world entry following the WORLDS.md schema structure
2. Identify what the core "room" or situation will be

---

## Phase 2: Variation Generation

### Step 2: Select Variational Techniques

Read `world/VARIATIONAL_TECHNIQUES.md` and choose 8-10 techniques to generate distinct chapter variations:

- **Micro-Physical**: Temperature, Temporal, Density, Sensory, Scale
- **Stance**: Clinical, Melancholic, Paranoid, Devotional, Erotic, Nostalgic
- **Narrative Position**: First-Timer, Expert, Unseen Servant, Exile, Saboteur
- **Relational History**: Estranged, Final Meeting, Betrayal, Mentorship
- **Temporal Frame**: Preparation, Interruption, Aftermath, Repetition
- **Intentionality**: Apology, Farewell, Test, Offering
- **Ontological Status**: Dream, Memory, Rehearsal, Prophecy

### Step 3: Define 10 Chapter Titles

Create titles based on selected variations. Example for Tea Ceremony:
1. The Scalded Ceremony (Temperature + Estranged)
2. The Delayed Ceremony (Temporal)
3. The Silent Ceremony (Sensory muted)
4. The First-Timer (Narrative position)
... etc.

---

## Phase 3: Literary Composition

### Step 4: Select Literary Structure

Read `book/LITERARY_STRUCTURES.md` and choose structures:

- **Calvino Canon**: City (Panorama), Object (Totem), Traveler (Immersion), Manual (Algorithm)
- **Dreamy Canon**: Encyclopedia (Borges), Instructions (Cortázar), Inventory (Perec), Parable (Kafka)
- **Bachelard Canon**: Shell (Enclosure), Miniature (Compression), Cellar (Descent)

### Step 5: Write Chapter Narratives

Write each chapter as a markdown file. Save as `chapter_01_name.md`, `chapter_02_name.md`, etc.

---

## Phase 4: Style Refinement

### Step 6: Apply Style Guide

Read `book/STYLE_GUIDE.md` and apply the Three Commandments:

1. **Room Frame**: Start by defining the enclosed space ("This room measures exactly four and a half mats.")
2. **Direct Assertion**: No "It is not X, but Y" structures. State what things ARE.
3. **No Meta-Commentary**: Never explain the logic of the world.

**Avoid**: Passive voice, onomatopoeia (sounds absurd in TTS), "The genealogy is...", "The tension is..."

---

## Phase 5: Audio Generation

### Step 7: Create audiobook_config.json

```json
{
  "project_name": "Project Name",
  "elevenlabs_model_id": "eleven_turbo_v2_5",
  "default_voice_id": "JBFqnCBsd6RMkjVDRZzb",
  "musical_concept": "Description of musical approach",
  "chapters": [
    {
      "id": "chapter_01",
      "title": "Chapter Title",
      "file_path": "path/to/chapter.md",
      "music_prompt": "Instrument, mood, structure (Intro→A→B→Coda), duration 2:00. No vocals."
    }
  ]
}
```

### Step 8: Generate Music

// turbo
```bash
python3 generate_music.py
```

### Step 9: Generate Speech

// turbo
```bash
python3 generate_audio.py
```

### Step 10: Merge Audio

// turbo
```bash
python3 merge_audio.py
```

---

## Phase 6: Cover Art

### Step 11: Generate Cover Art

- No text in image
- Minimal, single striking element
- Resolution: 1400×1400px minimum
- Save as `cover.png`

---

## Output

- 10 MP3 files (4-7 minutes each)
- 10 WAV files (optional)
- cover.png
- audiobook_config.json
- 10 chapter markdown files
