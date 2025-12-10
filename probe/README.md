# Memoir Probe

Interactive interrogation module for capturing personal life-world scenes using phenomenological, sociological, and structural frameworks.

## Quick Start

1. **Setup environment**:
```bash
# Create .env file in schema repo root
echo "MEMOIR_REPO=/path/to/your/memoir/directory" >> ../.env
echo "GEMINI_KEY=your_gemini_api_key" >> ../.env  # Optional, for LLM features
```

2. **Initialize memoir repository**:
```bash
python memoir_manager.py --init
```

3. **Capture your first scene**:
```bash
python interrogator.py
```

4. **View your scenes**:
```bash
python memoir_manager.py --list-scenes
python memoir_manager.py --stats
```

5. **Build a graph**:
```bash
python memoir_manager.py --build-graph
```

## Documentation

- **[THESIS.md](THESIS.md)** - High-level intent and goals
- **[SCHEMA.md](SCHEMA.md)** - Complete data schema definition
- **[PIPELINE.md](PIPELINE.md)** - Detailed usage and architecture

## Modules

- `interrogator.py` - Interactive interview for scene capture
- `memoir_manager.py` - Repository management and privacy
- `graph.py` - Graph representation and operations

## Privacy

The memoir probe maintains strict separation:
- **Public (this repo)**: Schema, code, documentation
- **Private (memoir repo)**: Your personal scenes and data

The memoir repository **must** be outside the schema repository.

## Integration

This implements the **Room Interrogator** from the [Adjacent Rooms architecture](../ADJACENT.md):

```
Room Interrogator → Room expander → Room affordance helper
     ^
     |
   YOU ARE HERE
```

Future modules will use captured scenes to suggest adjacent possible rooms and interventions.
