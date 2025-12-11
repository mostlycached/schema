---
layout: post
title: "How We Make Rooms: A Behind-the-Scenes Look"
date: 2025-12-11
categories: technical process
---

A tea ceremony performed in ten different emotional temperatures. The same subway ride refracted through musique concrète and a cappella. These are Rooms — and here's how an AI agent builds them from the inside out.

The entire production pipeline runs through an AI coding agent. When triggered via `/produce-room` or a conversation, the agent follows six phases to transform a sociological "world" into a finished Room.

---

## The Big Picture

Every Room follows six phases:

1. **Explore a world** (where does the story live?)
2. **Generate variations** (10 different ways to experience it)
3. **Compose the narrative** (using literary structures)
4. **Refine the style** (make it speech-friendly)
5. **Generate audio** (music + narration)
6. **Create cover art**

---

## Phase 1: Explore a World

Every Room starts with a *world* — a distinct social, professional, or cultural space with its own rules, rhythms, and tensions.

For *Cello Book of Tea*, the world is **The Tea Ceremony**. The agent explores its properties:

- **Genealogy**: Zen Buddhism → Sen no Rikyū → modern practice
- **Tension**: Simplicity vs. elaborate ritual; presence vs. performance
- **Inhabitants**: Host, Guest, Utensils
- **Phenomenology**: Silence, slowness, precise gesture

The repository maintains a [catalog of 105+ worlds](https://github.com/mostlycached/schema/blob/main/world/WORLDS.md) — from *The Algorithmic Gig Economy* to *The Zen Monastery* — each analyzed through sociological and phenomenological lenses.

---

## Phase 2: Generate Variations

Once a world is selected, the agent applies **variational techniques** — systematic ways to shift *how* the world is experienced without changing *what* it is.

For *Cello Book of Tea*, the agent generated 10 variations:

| Chapter | Variation Technique |
|---------|---------------------|
| The Scalded Ceremony | Temperature: +5°C (aggressive heat) |
| The Delayed Ceremony | Temporal: stretched to maximum slowness |
| The Silent Ceremony | Sensory: sound reduced to near-zero |
| The First-Timer | Position: novice experiencing initiation |
| The Unseen Servant | Position: invisible labor, backstage |
| The Estranged | Relational: former intimacy, unspoken wound |
| The Final Meeting | Relational: impending death/separation |
| The Memory | Ontological: recalled past, nostalgic |
| The Rehearsal | Ontological: practice, performativity exposed |
| The Paranoid | Stance: suspicion, coded messages |

The [Variational Techniques catalog](https://github.com/mostlycached/schema/blob/main/world/VARIATIONAL_TECHNIQUES.md) contains dozens of these "dials" — temperature, density, stance, position, relational history, temporal frame, and more.

---

## Phase 3: Compose the Narrative

Each variation becomes a short prose piece using **literary structures** borrowed from Calvino, Borges, Cortázar, Perec, and Bachelard.

For example:
- **The Traveler** (second-person immersion): "You enter the tearoom. You watch the host's hands."
- **The Manual** (step-by-step instructions): "First, you must purify your hands. Then, you must cross the threshold."
- **The Miniature** (compression): The entire universe contained in a single tea bowl.

Here's how "The Scalded Ceremony" opens:

> *This room measures exactly four and a half mats. The water has been heated five degrees beyond the optimal point for matcha. This is not an accident.*
>
> *The host kneels with perfect posture. The ladle dips into the kettle. Steam rises too aggressively, hissing against the cold air like a warning...*

---

## Phase 4: Refine the Style

Before audio generation, the agent applies a strict style guide to make prose speech-friendly:

**The Three Commandments**:

1. **Room Frame**: Start by defining the enclosed space
   - ✓ "This room measures exactly four and a half mats."
   - ✗ "The tea ceremony is a traditional Japanese ritual."

2. **Direct Assertion**: No negation ("It is not X, but Y")
   - ✓ "The Tagelmust wraps ten times around the skull."
   - ✗ "The Tagelmust is not a scarf; it is a wall."

3. **No Meta-Commentary**: Never explain the logic
   - ✓ "Time here travels in a circle."
   - ✗ "Because this is about repetition, time is circular."

**Also avoid**: Onomatopoeia (sounds absurd when AI reads "whish, whish"), passive voice, and academic framing.

---

## Phase 5: Generate Audio

Now the agent creates the actual audio — music and narration.

### Music

For *Cello Book of Tea*, each chapter opens with solo cello. The agent generates a music prompt in plain English:

> *Solo Cello in D minor. Aggressive, sul ponticello bowing. Structure: Intro (0:00-0:20, tense harmonics establishing unease) → A Section (main melody, harsh metallic timbre) → Coda (sudden exhaustion, melody collapses into silence). Mood: Suppressed rage.*

The AI (ElevenLabs Music) generates a 2-minute piece.

### Narration

The agent feeds the written story to text-to-speech AI. Narration for one chapter takes about 3-5 minutes.

### Merging

The agent uses ffmpeg to stitch: `[Music Intro] → [Narration] → [3 seconds silence]`

---

## Phase 6: Cover Art

The agent generates cover art with:
- No text in the image
- Minimal, single striking element
- At least 1400×1400 pixels

---

## The Result

Start to finish, producing one album (10 chapters) takes about 3-4 hours of active work. The final output:

- 10 MP3 files, each 4-7 minutes long
- One cover image
- Ready for Bandcamp

[🎧 Listen to Cello Book of Tea on Bandcamp](https://72rooms.bandcamp.com/album/cello-book-of-tea)

---

## AI Apologia

_I believe that human agency must be intentionally designed for in AI heavy projects so that subjectivity is not lost. In this project, I have allowed three openings for agency._

_One lies in choosing the world to explore — selecting *The Tea Ceremony* rather than *The Oil Rig* or *The Emergency Room*, or bringing an entirely new world of your own. That choice cuts the path. After that, the agent routes itself like water finding its way downhill._

_The second lies in the guides in the framework(literary structures, variational techniques, style guide, etc.) — those are the terrain I designed, and you can reshape while you navigate. They shape where the water can go, but they don't dictate the exact route. And it's interesting to watch where that fails — where the agent encounters resistance, where the expected path doesn't work, and new shapes form come to be that I did not foresee._

_The third lies in the participatory and negative spaces opened up as a part of the blog announcements._

---

*The complete production workflow is available as `/produce-room` in the [GitHub repository](https://github.com/mostlycached/schema).*
