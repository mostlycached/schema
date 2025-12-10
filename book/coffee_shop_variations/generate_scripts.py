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
            # Add pause before section
            text_lines.append('')
            continue
        
        # Clean markdown formatting
        line = line.replace('**', '')  # Remove bold
        line = line.replace('*', '')   # Remove italics
        line = line.replace('_', '')   # Remove underscores
        
        text_lines.append(line)
    
    # Join with appropriate pauses
    text = '\n\n'.join(text_lines)
    
    return text

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "audiobook_config.json")
    scripts_dir = os.path.join(script_dir, "scripts")
    
    # Create scripts directory if it doesn't exist
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
        
        # Extract text
        text = extract_text_from_md(md_path)
        
        # Save to scripts directory
        script_filename = f"{chapter_id}_script.txt"
        script_path = os.path.join(scripts_dir, script_filename)
        
        with open(script_path, 'w') as f:
            f.write(text)
        
        word_count = len(text.split())
        print(f"  Generated: {script_filename} ({word_count} words)")
    
    print(f"\nAll scripts generated in {scripts_dir}")
