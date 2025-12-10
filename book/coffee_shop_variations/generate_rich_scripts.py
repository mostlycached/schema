import os
import json

def extract_text_from_md(md_path):
    """Extract readable text from markdown file, removing headers and formatting."""
    with open(md_path, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    text_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Skip headers
        if line.startswith('#'):
            continue
        
        # Skip horizontal rules
        if line.startswith('---'):
            continue
        
        # Skip empty lines
        if not line:
            continue
        
        # Skip bold section markers like **THE VARIATION**
        if line.startswith('**') and line.endswith('**') and len(line.split()) < 5:
            text_lines.append('')
            continue
        
        # Clean markdown formatting
        line = line.replace('**', '')
        line = line.replace('*', '')
        line = line.replace('_', '')
        
        text_lines.append(line)
    
    text = '\n\n'.join(text_lines)
    return text

def condense_if_needed(text, max_chars=4800):
    """Condense text if over character limit."""
    if len(text) <= max_chars:
        return text
    
    # Simple approach: remove some paragraphs from middle
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    while len('\n\n'.join(paragraphs)) > max_chars and len(paragraphs) > 5:
        # Remove from middle-ish
        mid = len(paragraphs) // 2
        paragraphs.pop(mid)
    
    return '\n\n'.join(paragraphs)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "rich_audiobook_config.json")
    scripts_dir = os.path.join(script_dir, "rich_scripts")
    
    os.makedirs(scripts_dir, exist_ok=True)
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    for chapter in config['chapters']:
        chapter_id = chapter['id']
        md_path = os.path.join('/Users/hprasann/Documents/GitHub/schema', chapter['file_path'])
        
        if not os.path.exists(md_path):
            print(f"Warning: {md_path} not found")
            continue
        
        print(f"Processing {chapter_id}...")
        
        text = extract_text_from_md(md_path)
        text = condense_if_needed(text)
        
        script_filename = f"{chapter_id}_script.txt"
        script_path = os.path.join(scripts_dir, script_filename)
        
        with open(script_path, 'w') as f:
            f.write(text)
        
        char_count = len(text)
        word_count = len(text.split())
        print(f"  Generated: {script_filename} ({word_count} words, {char_count} chars)")

    print(f"\nAll scripts generated in {scripts_dir}")
