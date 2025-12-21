#!/usr/bin/env python3
"""
Encounter Navigator for Hari's Assemblage Genealogies.

Generates Deleuzian narratives showing how Hari's assemblages transform
through encounters with persons, environments, objects, artworks, and events.

Usage:
    python map_navigator.py --output output.md
    python map_navigator.py --path random --output output.md
"""

import argparse
import random
from pathlib import Path
from typing import NamedTuple


# --- Data Structures ---

class Encounter(NamedTuple):
    id: str
    entity_type: str  # person, environment, object, artwork, event
    name: str
    context: str
    affects: list[str]
    becomings: list[str]
    lines_of_flight: list[str]


# --- Hari's Base Assemblages ---

HARI_BASE = [
    ("Python-Developer", "writing code, debugging, system design"),
    ("Continental-Philosophy-Reader", "reading Deleuze, Spinoza, Nietzsche"),
    ("Audiobook-Producer", "creating audio narratives, mixing"),
    ("Knowledge-Worker", "screen-based, cognitive labor"),
    ("Body-in-Chair", "sedentary, ergonomic tension"),
    ("Coffee-Ritualist", "daily caffeine rhythm"),
    ("Night-Worker", "working late, inverted schedule"),
    ("Solo-Creator", "working alone, self-directed"),
    ("Tamil-Background", "cultural inheritance, language"),
    ("Meta-Reflector", "thinking about thinking"),
]

# --- Relational Modes ---

RELATIONAL_MODES = [
    ("love", "Love / Desire", "Hari falls in love with", "the intensity of attraction reshapes his world"),
    ("loss", "Loss / Grief", "Hari loses", "the absence becomes a presence that restructures everything"),
    ("joy", "Joy / Play", "Hari plays with", "lightness enters, the serious dissolves"),
    ("boredom", "Boredom / Stagnation", "Hari is bored by", "the weight of sameness reveals hidden depths"),
    ("conflict", "Conflict / Violence", "Hari is hurt by", "the wound becomes a teacher"),
    ("care", "Care / Obligation", "Hari cares for", "responsibility transforms the self"),
    ("discovery", "Discovery / Revelation", "Hari discovers", "the new cracks open the old"),
    ("fear", "Fear / Aversion", "Hari fears", "avoidance shapes the territory of the possible"),
]

# --- Encounter Pool Loader ---

def load_encounters(csv_path: Path) -> list[Encounter]:
    """Load encounters from CSV file."""
    import csv
    encounters = []
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip comment lines
            if row['id'].startswith('#'):
                continue
            
            encounters.append(Encounter(
                id=row['id'],
                entity_type=row['type'],
                name=row['name'],
                context=row['context'],
                affects=row['affects'].split('|'),
                becomings=row['becomings'].split('|'),
                lines_of_flight=row['lines_of_flight'].split('|'),
            ))
    
    return encounters


# Default CSV path
DEFAULT_POOL_PATH = Path(__file__).parent / "encounter_pool.csv"


# --- Narrative Generation ---

def generate_encounter_narrative(enc: Encounter, relation: tuple, intensity: str) -> list[str]:
    """Generate a Deleuzian narrative for a single encounter."""
    rel_id, rel_name, rel_verb, rel_effect = relation
    
    lines = [
        f"## ENCOUNTER: {enc.name.upper()}",
        "",
        f"*{rel_verb} {enc.name.lower()}*",
        f"*Intensity: {intensity.title()}*",
        "",
        f"### The Event",
        "",
    ]
    
    # Generate a narrative paragraph
    if enc.entity_type == "person":
        lines.append(f"Hari meets {enc.name.lower()} in the context of {enc.context.lower()}. "
                     f"{rel_effect.capitalize()}. "
                     f"There is {enc.affects[0]} and {enc.affects[1]}. "
                     f"Something shifts.")
    elif enc.entity_type == "environment":
        lines.append(f"Hari finds himself in {enc.name.lower()}: {enc.context.lower()}. "
                     f"The {enc.affects[0]} and {enc.affects[1]} work on him slowly. "
                     f"{rel_effect.capitalize()}.")
    elif enc.entity_type == "object":
        lines.append(f"Hari holds {enc.name.lower()}. {enc.context}. "
                     f"The {enc.affects[0]} passes into his hand. "
                     f"{rel_effect.capitalize()}.")
    elif enc.entity_type == "artwork":
        lines.append(f"Hari encounters {enc.name}. {enc.context}. "
                     f"The {enc.affects[0]} and {enc.affects[1]} open something in him. "
                     f"{rel_effect.capitalize()}.")
    elif enc.entity_type == "event":
        lines.append(f"{enc.name}: {enc.context.lower()}. "
                     f"The {enc.affects[0]} restructures Hari's world. "
                     f"{rel_effect.capitalize()}.")
    
    lines.extend([
        "",
        "### Affects Passed",
        "",
    ])
    for affect in enc.affects[:3]:
        lines.append(f"- **{affect.replace('-', ' ').title()}**: enters Hari's body/thought")
    
    lines.extend([
        "",
        "### Becomings Activated",
        "",
    ])
    for becoming in enc.becomings[:3]:
        lines.append(f"- **{becoming.replace('-', ' ').title()}**: Hari's assemblage shifts toward this")
    
    lines.extend([
        "",
        "### Lines of Flight",
        "",
    ])
    for lof in enc.lines_of_flight[:2]:
        lines.append(f"- **{lof.replace('-', ' ').title()}**: a new trajectory opens")
    
    lines.extend(["", "---", ""])
    return lines


def generate_genealogy(num_encounters: int = 4) -> str:
    """Generate a full Deleuzian genealogy for Hari."""
    
    # Select diverse encounters (one from each type if possible)
    types = ["person", "environment", "object", "artwork", "event"]
    selected = []
    for t in types[:num_encounters]:
        pool = [e for e in ENCOUNTERS if e.entity_type == t]
        if pool:
            selected.append(random.choice(pool))
    
    # Fill remaining with random
    while len(selected) < num_encounters:
        selected.append(random.choice(ENCOUNTERS))
    
    lines = [
        "# Hari: Assemblage Genealogy",
        "",
        "*How encounters reshape the self*",
        "",
        "---",
        "",
        "## HARI'S BASE SET (T=0)",
        "",
        "*Before these encounters*",
        "",
        "| # | Assemblage | Description |",
        "|---|------------|-------------|",
    ]
    
    for i, (name, desc) in enumerate(HARI_BASE, 1):
        lines.append(f"| {i} | **{name}** | {desc} |")
    
    lines.extend(["", "---", ""])
    
    # Generate each encounter
    intensities = ["fleeting", "sustained", "defining"]
    for i, enc in enumerate(selected):
        relation = random.choice(RELATIONAL_MODES)
        intensity = random.choice(intensities)
        lines.append(f"## T={i+1}")
        lines.append("")
        lines.extend(generate_encounter_narrative(enc, relation, intensity))
    
    # Recursive self
    lines.extend([
        "## T=5: HARI REFLECTS",
        "",
        "After these encounters, Hari is no longer the same:",
        "",
        "- The **becomings** have redistributed his capacities",
        "- The **affects** have left traces in his body",
        "- The **lines of flight** have opened new territories",
        "",
        "The assemblage continues to move.",
        "",
    ])
    
    return "\n".join(lines)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Generate Deleuzian encounter genealogies for Hari.")
    parser.add_argument("--output", type=Path, required=True, help="Output markdown file")
    parser.add_argument("--num", type=int, default=4, help="Number of encounters")
    
    args = parser.parse_args()
    
    content = generate_genealogy(args.num)
    args.output.write_text(content)
    print(f"Wrote genealogy to: {args.output}")


if __name__ == "__main__":
    main()
