import os
import re

def condense_script(text, target_chars=4800):
    """Intelligently condense script to under target character count."""
    current_chars = len(text)
    
    if current_chars <= target_chars:
        return text
    
    # Calculate reduction needed
    reduction_ratio = target_chars / current_chars
    
    # Split into paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    condensed_paragraphs = []
    
    for para in paragraphs:
        # Keep short paragraphs as-is
        if len(para) < 100:
            condensed_paragraphs.append(para)
            continue
        
        # For longer paragraphs, remove some sentences
        sentences = re.split(r'(?<=[.!?])\s+', para)
        
        # Keep ~ratio of sentences
        keep_count = max(1, int(len(sentences) * reduction_ratio))
        
        # Prioritize keeping first and last sentences
        if len(sentences) <= 2:
            condensed_paragraphs.append(para)
        else:
            kept_sentences = [sentences[0]]  # Always keep first
            if keep_count > 2:
                # Keep some middle sentences
                middle_keep = keep_count - 2
                step = max(1, len(sentences[1:-1]) // middle_keep)
                kept_sentences.extend(sentences[1:-1][::step][:middle_keep])
            kept_sentences.append(sentences[-1])  # Always keep last
            
            condensed_paragraphs.append(' '.join(kept_sentences))
    
    result = '\n\n'.join(condensed_paragraphs)
    
    # If still too long, do more aggressive trimming
    if len(result) > target_chars:
        # Remove some paragraphs from the middle
        total_paras = len(condensed_paragraphs)
        keep_paras = int(total_paras * 0.85)
        
        # Keep first 40%, last 45%, skip middle 15%
        first_part = condensed_paragraphs[:int(total_paras * 0.4)]
        last_part = condensed_paragraphs[-int(total_paras * 0.45):]
        
        result = '\n\n'.join(first_part + last_part)
    
    return result

if __name__ == "__main__":
    scripts_dir = "/Users/hprasann/Documents/GitHub/schema/book/coffee_shop_variations/scripts"
    
    # Chapters that need condensing (over 5000 chars)
    chapters_to_condense = ['chapter_01', 'chapter_04', 'chapter_05', 'chapter_08', 'chapter_10']
    
    for chapter_id in chapters_to_condense:
        script_path = os.path.join(scripts_dir, f"{chapter_id}_script.txt")
        
        if not os.path.exists(script_path):
            print(f"Skipping {chapter_id} (not found)")
            continue
        
        with open(script_path, 'r') as f:
            original_text = f.read()
        
        original_chars = len(original_text)
        
        if original_chars <= 5000:
            print(f"{chapter_id}: Already under limit ({original_chars} chars)")
            continue
        
        print(f"{chapter_id}: Condensing from {original_chars} chars...")
        
        condensed_text = condense_script(original_text, target_chars=4800)
        condensed_chars = len(condensed_text)
        
        # Save condensed version
        with open(script_path, 'w') as f:
            f.write(condensed_text)
        
        print(f"  → Reduced to {condensed_chars} chars ({condensed_chars/original_chars*100:.1f}% of original)")

    print("\nCondensing complete!")
