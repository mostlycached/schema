# Memoir Probe Pipeline

## Overview

The memoir probe system captures personal life-world scenes through an interactive interview process, structures them using sociological/phenomenological frameworks, and represents them as a searchable graph.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Experience                         │
│                                                             │
│  1. Run interrogator.py                                    │
│  2. Answer guided questions                                │
│  3. Review and save scene                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  InterviewSession                           │
│                  (interrogator.py)                          │
│                                                             │
│  • Phenomenological prompts                                │
│  • Structural prompts                                      │
│  • Systemic prompts                                        │
│  • Optional LLM-assisted follow-ups                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 Structured Scene Data                       │
│                    (YAML/JSON)                             │
│                                                             │
│  • Metadata (title, date, location)                        │
│  • Phenomenology (time, space, body)                       │
│  • Structure (capital, habitus, hierarchy)                 │
│  • System (function, boundaries, code)                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    MemoirRepo                               │
│                 (memoir_manager.py)                         │
│                                                             │
│  • Privacy validation                                      │
│  • Save to private repository                              │
│  • Index management                                        │
│  • Load/query scenes                                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    MemoirGraph                              │
│                     (graph.py)                             │
│                                                             │
│  • Build graph from scenes                                 │
│  • Create temporal edges                                   │
│  • Detect world intersections                              │
│  • Export to JSON/GraphML/DOT                              │
└─────────────────────────────────────────────────────────────┘
```

## Usage

### 1. Setup Environment

Create a `.env` file in the schema repository root:

```bash
GEMINI_KEY=your_gemini_api_key_here
MEMOIR_REPO=/path/to/your/private/memoir/repo
```

**Important**: The memoir repository must be **outside** the schema repository to maintain privacy.

### 2. Initialize Memoir Repository

```bash
cd /Users/hprasann/Documents/GitHub/schema
python probe/memoir_manager.py --init
```

This creates the following structure in your memoir repo:

```
memoir/
├── scenes/          # Individual scene YAML files
├── graphs/          # Exported graph files
└── index.yaml       # Scene index and metadata
```

### 3. Capture a Scene

Run the interactive interrogator:

```bash
python probe/interrogator.py
```

The interview will guide you through:

1. **Initial Narrative**: Describe the scene in your own words
2. **Metadata**: Title, date, location, duration, tags
3. **Phenomenology**: How you experienced time, space, emotions, body
4. **Structure**: Social dynamics, capital, power, habits
5. **System**: Function, boundaries, binary codes
6. **Inhabitants**: Who was present and their relationships
7. **Reflection**: Significance, patterns, questions

**Optional**: Use `--llm` or answer "y" to enable AI-assisted follow-up questions for deeper exploration.

### 4. View and Manage Scenes

List all captured scenes:

```bash
python probe/memoir_manager.py --list-scenes
```

View repository statistics:

```bash
python probe/memoir_manager.py --stats
```

Example output:
```
Repository Statistics:
  Location: /Users/hprasann/Documents/memoir
  Total scenes: 15
  Total tags: 28
  Popular tags:
    commute: 8
    work: 5
    family: 4
```

### 5. Build and Visualize Graph

Build a graph from all scenes:

```bash
python probe/memoir_manager.py --build-graph
```

This creates:
- Temporal edges between scenes (chronological)
- Scene nodes with full data
- Graph exported to `memoir/graphs/main_graph.json`

Generate visualizations:

```python
from probe.graph import MemoirGraph

graph = MemoirGraph.from_json('path/to/memoir/graphs/main_graph.json')

# Export to Graphviz DOT format
graph.to_dot('memoir_graph.dot')

# Then render with: dot -Tpng memoir_graph.dot -o memoir_graph.png
```

### 6. Programmatic Access

Use the modules in your own scripts:

```python
from probe.memoir_manager import MemoirRepo
from probe.graph import MemoirGraph

# Load memoir repository
repo = MemoirRepo()

# Get all scenes
scenes = repo.load_all_scenes()

# Build graph
graph = repo.build_graph()

# Query the graph
recent_scenes = graph.get_temporal_sequence()[-10:]  # Last 10 scenes
work_scenes = graph.find_scenes_by_tag("work")

# Get statistics
stats = graph.get_statistics()
print(f"Total scenes: {stats['scenes']}")
print(f"Total edges: {stats['total_edges']}")
```

## Data Flow

### Input

Raw user responses to interview prompts:

```
Q: How did you experience time in this scene?
A: Stretched infinitely, every minute felt like hours
```

### Processing

Structured into schema-compliant format:

```yaml
phenomenology:
  cognitive_style:
    time_experience: "Stretched infinitely, every minute felt like hours"
```

### Storage

Saved as individual YAML file in private memoir repo:

```
memoir/scenes/2024-12-10_morning_meeting.yaml
```

### Indexing

Added to central index:

```yaml
scenes:
  a3f2b8c1-9d4e-4a1b-8c2f-7e3d5f6a9b0c:
    filename: "2024-12-10_morning_meeting.yaml"
    title: "Morning Meeting"
    date: "2024-12-10"
    tags: ["work", "meeting", "anxiety"]
```

### Graph Representation

Converted to graph nodes/edges:

```json
{
  "nodes": [
    {
      "node_id": "a3f2b8c1-9d4e-4a1b-8c2f-7e3d5f6a9b0c",
      "node_type": "scene",
      "title": "Morning Meeting",
      "date": "2024-12-10"
    }
  ],
  "edges": [
    {
      "edge_id": "temporal_0",
      "edge_type": "temporal",
      "source": "<previous_scene_id>",
      "target": "a3f2b8c1-9d4e-4a1b-8c2f-7e3d5f6a9b0c"
    }
  ]
}
```

## Integration with Adjacent Rooms Architecture

This memoir probe implements the first component of the Adjacent Rooms architecture from `ADJACENT.md`:

```
Room Interrogator → Room expander / neighboring Room generator → Room affordance helper
     ^
     |
  THIS MODULE
```

The interrogator captures the current "room" (life-world scene) with rich detail. Future modules will:

- **Room Expander**: Suggest adjacent possible rooms based on current scenes
- **Room Affordance Helper**: Identify actions/interventions to move between rooms

See [ADJACENT.md](file:///Users/hprasann/Documents/GitHub/schema/ADJACENT.md) for the full architecture.

## Privacy Considerations

### What Stays Private (memoir repo)

- Individual scene YAML files
- Personal narratives and reflections
- Specific names, dates, locations
- Graph files (may contain personal data)
- Index file

### What's Public (schema repo)

- Schema definition (SCHEMA.md)
- Python modules (interrogator.py, graph.py, memoir_manager.py)
- Documentation (this file, THESIS.md)
- Example/template files (no personal data)

**Never commit files from your memoir repository to the schema repository.**

The `memoir_manager.py` module includes validation to prevent accidental writes to the schema repo.

## Next Steps

After capturing scenes, you can:

1. **Analyze patterns**: Identify recurring worlds, emotions, power dynamics
2. **Detect intersections**: Map scenes to worlds from WORLDS.md
3. **Generate interventions**: Use INTERVENTION_TECHNIQUES.md to explore shifts
4. **Build narratives**: Export sequences for storytelling
5. **Visualize trajectories**: See how you move between life-worlds over time

## Troubleshooting

### "MEMOIR_REPO not found in .env"

Create a `.env` file in the schema repo root with:
```
MEMOIR_REPO=/absolute/path/to/memoir/directory
```

### "Memoir repo is inside schema repo"

Move your memoir repository to a completely separate directory, outside the schema repo.

### "GEMINI_KEY not found"

If you want LLM-assisted prompts, add your Gemini API key to `.env`:
```
GEMINI_KEY=your_key_here
```

Otherwise, the interrogator will use manual prompts only.

### Import errors

Ensure you're running from the schema repository root:
```bash
cd /Users/hprasann/Documents/GitHub/schema
python probe/interrogator.py
```

Or add the repo to your PYTHONPATH:
```bash
export PYTHONPATH="/Users/hprasann/Documents/GitHub/schema:$PYTHONPATH"
```

## File Reference

- [SCHEMA.md](file:///Users/hprasann/Documents/GitHub/schema/probe/SCHEMA.md) - Complete schema definition
- [interrogator.py](file:///Users/hprasann/Documents/GitHub/schema/probe/interrogator.py) - Interactive interview module
- [memoir_manager.py](file:///Users/hprasann/Documents/GitHub/schema/probe/memoir_manager.py) - Repository manager
- [graph.py](file:///Users/hprasann/Documents/GitHub/schema/probe/graph.py) - Graph data structures
- [THESIS.md](file:///Users/hprasann/Documents/GitHub/schema/probe/THESIS.md) - High-level intent
