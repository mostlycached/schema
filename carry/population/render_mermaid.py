#!/usr/bin/env python3
"""
Render mermaid diagrams from a markdown file to PNG images.

Usage:
    python render_mermaid.py <markdown_file> [output_dir]

Requirements:
    npm install -g @mermaid-js/mermaid-cli
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path


def extract_mermaid_blocks(markdown_path: Path) -> list[tuple[str, str]]:
    """Extract mermaid code blocks from markdown with descriptive names."""
    content = markdown_path.read_text()
    
    # Find all mermaid blocks with their preceding headers
    blocks = []
    lines = content.split('\n')
    
    current_header = "diagram"
    in_mermaid = False
    mermaid_content = []
    block_count = 0
    
    for i, line in enumerate(lines):
        # Track headers for naming
        if line.startswith('## '):
            current_header = line[3:].strip().lower()
            current_header = re.sub(r'[^a-z0-9]+', '_', current_header)
        elif line.startswith('### '):
            current_header = line[4:].strip().lower()
            current_header = re.sub(r'[^a-z0-9]+', '_', current_header)
        
        # Detect mermaid block boundaries
        if line.strip() == '```mermaid':
            in_mermaid = True
            mermaid_content = []
        elif in_mermaid and line.strip() == '```':
            in_mermaid = False
            block_count += 1
            name = f"{block_count:02d}_{current_header}"
            blocks.append((name, '\n'.join(mermaid_content)))
        elif in_mermaid:
            mermaid_content.append(line)
    
    return blocks


def render_mermaid(code: str, output_path: Path) -> bool:
    """Render mermaid code to PNG using mmdc."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
        f.write(code)
        temp_path = Path(f.name)
    
    try:
        result = subprocess.run(
            ['mmdc', '-i', str(temp_path), '-o', str(output_path), '-b', 'transparent'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"  Error: {result.stderr}")
            return False
        return True
    finally:
        temp_path.unlink()


def main():
    if len(sys.argv) < 2:
        print("Usage: python render_mermaid.py <markdown_file> [output_dir]")
        sys.exit(1)
    
    markdown_path = Path(sys.argv[1])
    if not markdown_path.exists():
        print(f"Error: File not found: {markdown_path}")
        sys.exit(1)
    
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else markdown_path.parent / "diagrams"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Extracting mermaid blocks from: {markdown_path}")
    blocks = extract_mermaid_blocks(markdown_path)
    
    if not blocks:
        print("No mermaid blocks found.")
        sys.exit(0)
    
    print(f"Found {len(blocks)} mermaid blocks")
    print(f"Output directory: {output_dir}\n")
    
    for name, code in blocks:
        output_path = output_dir / f"{name}.png"
        print(f"Rendering: {name}.png ... ", end='', flush=True)
        if render_mermaid(code, output_path):
            print("✓")
        else:
            print("✗")
    
    print(f"\nDone! Images saved to: {output_dir}")


if __name__ == "__main__":
    main()
