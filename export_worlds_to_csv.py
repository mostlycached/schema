import re
import csv

def parse_worlds_md(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Regex to parse the markdown
    # Updated to include Genealogy, Tension, and Iteration
    pattern = re.compile(
        r"#### \d+\. (.*?)\n"  # World Name
        r"\*   \*\*Type\*\*: (.*?)\n"  # Type
        r"\*   \*\*Genealogy\*\*: (.*?)\n"  # Genealogy
        r"\*   \*\*Tension\*\*: (.*?)\n"  # Tension
        r"\*   \*\*Iteration\*\*: (.*?)\n"  # Iteration
        r"\*   \*\*Inhabitants\*\*: (.*?)\n"  # Inhabitants
        r"\*   \*\*Phenomenology \(Schutz\)\*\*: (.*?)\n"  # Phenomenology
        r"\*   \*\*Structure \(Bourdieu\)\*\*: (.*?)\n"  # Structure
        r"\*   \*\*System \(Luhmann\)\*\*: (.*?)(?=\n#+ |\Z)",  # System
        re.DOTALL
    )

    matches = pattern.findall(content)
    
    worlds = []
    for match in matches:
        worlds.append({
            'World Name': match[0].strip(),
            'Type': match[1].strip(),
            'Genealogy': match[2].strip(),
            'Tension': match[3].strip(),
            'Iteration': match[4].strip(),
            'Inhabitants': match[5].strip(),
            'Phenomenology (Schutz)': match[6].strip(),
            'Structure (Bourdieu)': match[7].strip(),
            'System (Luhmann)': match[8].strip()
        })
    
    return worlds

def write_csv(worlds, output_path):
    fieldnames = ['World Name', 'Type', 'Genealogy', 'Tension', 'Iteration', 'Inhabitants', 'Phenomenology (Schutz)', 'Structure (Bourdieu)', 'System (Luhmann)']
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for world in worlds:
            writer.writerow(world)

if __name__ == "__main__":
    md_path = '/Users/hprasann/Workspace/schema/WORLDS.md'
    csv_path = '/Users/hprasann/Workspace/schema/WORLDS.csv'
    
    print(f"Parsing {md_path}...")
    worlds = parse_worlds_md(md_path)
    print(f"Found {len(worlds)} worlds.")
    
    print(f"Writing to {csv_path}...")
    write_csv(worlds, csv_path)
    print("Done.")
