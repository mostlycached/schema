import os
import re

def process_text(text):
    # Remove emotional tags [text]
    text = re.sub(r'\[.*?\]', '', text)
    
    # Remove markdown headers but keep the text
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    
    # Remove bold/italic markers
    text = re.sub(r'\*', '', text)
    
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            processed_lines.append("")
            continue
            
        # Punctuation to ellipses for natural pauses
        line = re.sub(r'[,;:\u2014]', '...', line)
        
        processed_lines.append(line)
        
    # Reassemble
    text = '\n'.join(processed_lines)
    
    # Clean up multiple ellipses
    text = re.sub(r'\.{4,}', '...', text)
    
    # Remove multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, 'scripts')
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    # Find all chapter markdown files in this directory
    files = [f for f in os.listdir(script_dir) if f.endswith('.md') and f.startswith('chapter_')]
    
    print(f"Found {len(files)} files to process.")
    
    for filename in files:
        source_path = os.path.join(script_dir, filename)
        
        # Extract chapter number: chapter_XX_*.md -> chapter_XX_script.txt
        match = re.search(r'(chapter_\d+)', filename)
        if match:
            dest_filename = f"{match.group(1)}_script.txt"
        else:
            dest_filename = filename.replace('.md', '_script.txt')
        
        dest_path = os.path.join(dest_dir, dest_filename)
        
        print(f"Processing {filename} -> {dest_filename}")
        
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        processed_content = process_text(content)
        
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
            
    print("Done.")

if __name__ == '__main__':
    main()
