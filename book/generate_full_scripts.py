import os
import re

def process_text(text):
    # Remove emotional tags [text]
    text = re.sub(r'\[.*?\]', '', text)
    
    # Remove markdown headers but keep the text if it's not just a number
    # Actually, for the title "Chapter X: The Title", we might want to keep it clean.
    # The current files have "# The Ama Divers", etc.
    # Let's strip the '#' characters.
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    
    # Remove bold/italic markers
    text = re.sub(r'\*', '', text)
    
    # Normalize whitespace
    # text = re.sub(r'\s+', ' ', text).strip() # careful, we want to keep paragraphs?
    # The user wants "audiobook friendly". The previous scripts had line breaks.
    # Let's keep paragraphs separated by double newlines.
    
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            processed_lines.append("") # keep empty lines for paragraph separation
            continue
            
        # Punctuation to ellipses conversation
        # Replace , ; : — with ...
        line = re.sub(r'[,;:\u2014]', '...', line)
        
        # Ensure periods have a pause too, maybe just keep them as is?
        # The user said "audiobook friendly like the old script".
        # Old script: "The Iso-bue... "Sea Whistle"... is not a mechanical instrument... "
        # It seems periods are also roughly treated as pauses or kept.
        # Let's basically replace most pauses with ellipses for that flow.
        
        processed_lines.append(line)
        
    # Reassemble
    text = '\n'.join(processed_lines)
    
    # Clean up multiple ellipses
    text = re.sub(r'\.{4,}', '...', text)
    
    # Remove multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def main():
    source_dir = '/Users/hprasann/Documents/GitHub/schema/book'
    dest_dir = os.path.join(source_dir, 'scripts')
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    # Find all markdown files
    files = [f for f in os.listdir(source_dir) if f.endswith('.md') and (f.startswith('chapter_') or f == 'preface.md')]
    
    print(f"Found {len(files)} files to process.")
    
    for filename in files:
        source_path = os.path.join(source_dir, filename)
        
        # Determine output filename
        if filename == 'preface.md':
            dest_filename = 'preface_script.txt'
        else:
            # extract chapter number to maintain consistency if filename is complex
            # current files: chapter_06_ama_divers.md -> chapter_06_script.txt
            # We need to map 'chapter_XX_*.md' to 'chapter_XX_script.txt'
            match = re.search(r'(chapter_\d+)', filename)
            if match:
                dest_filename = f"{match.group(1)}_script.txt"
            else:
                # Fallback
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
