---
layout: page
title: Repository Guide
permalink: /guide/
---

This guide explains how to navigate and use the Hyperframes repository, including its structure, workflows, and generative tools.

---

## Structure

The repository is organized into several major directories:

### 📁 `world/`
Contains schemas and frameworks for analyzing sociological and phenomenological worlds:
- **[WORLDS.md](https://github.com/mostlycached/schema/blob/main/world/WORLDS.md)** — Comprehensive schema of 105+ worlds analyzed through Schutz, Bourdieu, and Luhmann frameworks
- **[VARIATIONAL_TECHNIQUES.md](https://github.com/mostlycached/schema/blob/main/world/VARIATIONAL_TECHNIQUES.md)** — Catalog of intervention techniques for generating world variations

### 📁 `intervention/`
Tools and frameworks for analyzing and optimizing worlds:
- **[VALUES.md](https://github.com/mostlycached/schema/blob/main/intervention/VALUES.md)** — Value systems (phenomenological, economic, artistic criteria) for world optimization
- **[INTERVENTION_TECHNIQUES.md](https://github.com/mostlycached/schema/blob/main/intervention/INTERVENTION_TECHNIQUES.md)** — Detailed techniques for world interventions
- Example optimizations (e.g., `tradwife_variations.md`)

### 📁 `book/`
Audiobook projects and narrative variations:
- **[LITERARY_STRUCTURES.md](https://github.com/mostlycached/schema/blob/main/book/LITERARY_STRUCTURES.md)** — Classical forms adapted for narrative variations
- **[PRODUCTION_WORKFLOW.md](https://github.com/mostlycached/schema/blob/main/book/PRODUCTION_WORKFLOW.md)** — Complete audiobook production pipeline
- **[STYLE_GUIDE.md](https://github.com/mostlycached/schema/blob/main/book/STYLE_GUIDE.md)** — Writing guidelines for speech-friendly narratives
- Subdirectories for each audiobook project (`coffee_shop_variations/`, `nyc_subway_variations/`, etc.)

### 📁 `attention/`
Attention architecture research:
- **[THESIS.md](https://github.com/mostlycached/schema/blob/main/attention/THESIS.md)** — Architectural framework for attention systems
- Diagrams and supporting materials

### 📁 `braitenberg_vehicles/`
Synthetic psychology simulations and narratives:
- **[BRAITENBERG_VS_LAUTMAN_PAPER.md](https://github.com/mostlycached/schema/blob/main/braitenberg_vehicles/BRAITENBERG_VS_LAUTMAN_PAPER.md)** — Theoretical comparison
- Simulation scripts and screenplay adaptations

### 📁 `.agent/workflows/`
Reusable agent workflows for common tasks (see [Workflows](#workflows) section below)

---

## Workflows

The repository includes automated workflows in `.agent/workflows/` that can be invoked by AI agents to perform complex tasks. These workflows encode best practices for common operations.

### `/optimize-world`
**Purpose**: Optimize a given world using specified value systems.

**Usage**: Provide a world from `WORLDS.md` and value criteria from `VALUES.md`. The workflow:
1. Identifies the world's characteristics
2. Applies relevant value systems
3. Generates optimized variations using intervention techniques
4. Outputs results in formal and poetic registers

**Example**: Optimizing "The TradWife / Cottagecore Sphere" using phenomenological and aesthetic criteria.

### `/produce-audiobook`
**Purpose**: Generate a complete audiobook with music and narration.

**Usage**: Provide source text and musical concept. The workflow:
1. Refactors narrative into speech-friendly form
2. Generates musical introductions
3. Synthesizes speech narration
4. Merges audio components
5. Exports final audiobook files

**Prerequisites**: ElevenLabs API key (set in `.env`)

### `/refactor-narrative-flow`
**Purpose**: Transform structured, formulaic text into fluid, essayistic narrative suitable for audiobook narration.

**Usage**: Provide a chapter or text file. The workflow applies narrative techniques to create natural, flowing prose optimized for speech synthesis.

---

## How to Generate Your Own Variations

Want to create your own world optimizations or audiobook variations? Here's how:

### 1. World Optimization

**Step 1**: Choose a world from [WORLDS.md](https://github.com/mostlycached/schema/blob/main/world/WORLDS.md)  
**Step 2**: Select value criteria from [VALUES.md](https://github.com/mostlycached/schema/blob/main/intervention/VALUES.md)  
**Step 3**: Apply techniques from [VARIATIONAL_TECHNIQUES.md](https://github.com/mostlycached/schema/blob/main/world/VARIATIONAL_TECHNIQUES.md) or [INTERVENTION_TECHNIQUES.md](https://github.com/mostlycached/schema/blob/main/intervention/INTERVENTION_TECHNIQUES.md)  
**Step 4**: Generate variations by:
- Changing micro-mechanisms (e.g., "What if the algorithm screamed?")
- Shifting stance or temporal frame
- Applying defamiliarization or metaphorical reframing

**Example**: See [tradwife_variations.md](https://github.com/mostlycached/schema/blob/main/intervention/tradwife_variations.md)

### 2. Audiobook Production

**Step 1**: Write or adapt source text  
**Step 2**: Refactor into speech-friendly narrative (see [STYLE_GUIDE.md](https://github.com/mostlycached/schema/blob/main/book/STYLE_GUIDE.md))  
**Step 3**: Choose a literary structure from [LITERARY_STRUCTURES.md](https://github.com/mostlycached/schema/blob/main/book/LITERARY_STRUCTURES.md)  
**Step 4**: Generate audio using the production workflow:
- Create music intros (ElevenLabs Music API)
- Synthesize speech narration (ElevenLabs Speech API)
- Merge audio components
**Step 5**: Export and publish

**See**: [PRODUCTION_WORKFLOW.md](https://github.com/mostlycached/schema/blob/main/book/PRODUCTION_WORKFLOW.md) for complete details

---

## Prerequisites

To use the audiobook production workflows, you'll need:

### Required
- **ElevenLabs API Key**: For music generation and speech synthesis
  - Sign up at [elevenlabs.io](https://elevenlabs.io)
  - Add your API key to `.env` file: `ELEVENLABS_API_KEY=your_key_here`

### Optional
- **Python 3.x**: For any custom scripts
- **ffmpeg**: For audio processing and format conversion
  - Install on macOS: `brew install ffmpeg`
- **Jekyll** (for local site preview): `gem install bundler jekyll`

---

## Contributing & Collaboration

This is an open research project. You're welcome to:
- Fork the repository and create your own variations
- Suggest new worlds for the schema
- Propose new intervention techniques
- Share your generated audiobooks or world optimizations

For questions or collaboration inquiries, open an issue on [GitHub](https://github.com/mostlycached/schema/issues).

---

## Repository Links

- **GitHub Repository**: [github.com/mostlycached/schema](https://github.com/mostlycached/schema)
- **Research Overview**: [Hyperframes Research](/research)
- **Audiobook Projects**: [Hyperframes Audiobooks](/audiobooks)
