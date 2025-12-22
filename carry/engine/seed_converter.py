"""
Seed to Assemblage Converter

Parses seed instances from schema/seeds/ and generates rich assemblages
using LLM, then outputs to carry/assemblages/encounters/
"""

import os
import re
import yaml
from pathlib import Path
from typing import List, Dict, Tuple

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


def parse_seed_file(filepath: Path) -> List[Tuple[str, str, str]]:
    """
    Parse a seed markdown file and extract instances.
    Returns list of (category, name, description) tuples.
    """
    instances = []
    content = filepath.read_text()
    
    current_category = ""
    current_subcategory = ""
    
    for line in content.split('\n'):
        # Match ## Category
        if line.startswith('## '):
            current_category = line[3:].strip()
        # Match ### Subcategory  
        elif line.startswith('### '):
            current_subcategory = line[4:].strip()
        # Match - **Name** — Description
        elif line.startswith('- **'):
            match = re.match(r'- \*\*(.+?)\*\* — (.+)', line)
            if match:
                name = match.group(1).strip()
                desc = match.group(2).strip()
                full_context = f"{current_category} > {current_subcategory}: {name} — {desc}"
                instances.append((current_category, name, full_context))
    
    return instances


def generate_assemblage(name: str, context: str, model_name: str = "gemini-2.0-flash") -> Dict:
    """
    Use LLM to generate a rich assemblage from a seed instance.
    """
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""Generate a Deleuzian assemblage for this seed:

SEED: {context}

Output ONLY valid YAML (no markdown fences) for a single assemblage with this exact structure:

name: {name.replace(' ', '-')}-Assemblage
abstract_machine: "One-line poetic essence of what this does"
entity_type: object
territories:
  - name: Territory-Name
    function: "What this territory does"
    quality: "single-word quality"
    space_type: smooth or striated
codes:
  - name: Code-Name
    content: "The habit or rule"
    type: habit
    level: molar or molecular
components:
  - name: Component-Name
    type: organic or technical or sign
    capacity: "What capacity this enables"
intensity_field:
  focus: 0.0-1.0
  speed: 0.0-1.0
  abstraction: 0.0-1.0
  tactility: 0.0-1.0
  patience: 0.0-1.0
  social: 0.0-1.0
becoming_vectors:
  - becoming-something
  - becoming-something-else

Include 2-3 territories, 2-3 codes, 2-3 components, and 2-4 becoming_vectors.
Be specific and evocative, not generic. Output ONLY the YAML, nothing else."""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Remove markdown fences if present
        if text.startswith('```'):
            text = re.sub(r'^```\w*\n?', '', text)
            text = re.sub(r'\n?```$', '', text)
        return yaml.safe_load(text)
    except Exception as e:
        print(f"Error generating {name}: {e}")
        return None


def convert_seed_file(seed_path: Path, output_dir: Path, limit: int = None):
    """
    Convert a seed file to assemblages.
    Preserves category structure: seeds/spatial/by_function.md → encounters/spatial/by_function.yaml
    """
    instances = parse_seed_file(seed_path)
    print(f"Found {len(instances)} instances in {seed_path.name}")
    
    if limit:
        instances = instances[:limit]
    
    assemblages = []
    for i, (category, name, context) in enumerate(instances):
        print(f"  [{i+1}/{len(instances)}] Generating: {name}")
        asm = generate_assemblage(name, context)
        if asm:
            assemblages.append(asm)
    
    if assemblages:
        # Preserve folder structure from seeds/
        # e.g., seeds/spatial/by_function.md → encounters/spatial/by_function.yaml
        category_folder = seed_path.parent.name  # e.g., "spatial"
        output_subdir = output_dir / category_folder
        output_subdir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_subdir / f"{seed_path.stem}.yaml"
        with open(output_file, 'w') as f:
            yaml.dump({'assemblages': assemblages}, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"  → Saved {len(assemblages)} assemblages to {category_folder}/{output_file.name}")
    
    return assemblages


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert seeds to assemblages")
    parser.add_argument("--seeds-dir", type=Path, default=Path(__file__).parent.parent.parent / "seeds",
                        help="Path to seeds directory")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent.parent / "assemblages" / "encounters",
                        help="Output directory for assemblages")
    parser.add_argument("--category", type=str, help="Only process this category (e.g., 'material')")
    parser.add_argument("--limit", type=int, help="Limit instances per file")
    parser.add_argument("--file", type=str, help="Only process this specific file")
    
    args = parser.parse_args()
    
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find seed files
    if args.file:
        seed_files = list(args.seeds_dir.rglob(args.file))
    elif args.category:
        seed_files = list((args.seeds_dir / args.category).glob("*.md"))
    else:
        seed_files = list(args.seeds_dir.rglob("*.md"))
        # Exclude ENUMERATION.md and other top-level files
        seed_files = [f for f in seed_files if f.parent != args.seeds_dir]
    
    print(f"Processing {len(seed_files)} seed files")
    
    total = 0
    for seed_file in seed_files:
        assemblages = convert_seed_file(seed_file, args.output_dir, args.limit)
        total += len(assemblages)
    
    print(f"\nTotal: {total} assemblages generated")


if __name__ == "__main__":
    main()
