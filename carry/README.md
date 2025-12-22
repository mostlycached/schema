# Carry: Assemblage Interaction Framework

A Deleuzian simulation framework analyzing how encounters reshape assemblages through LLM-powered semantic reasoning.

## Structure

```
carry/
├── assemblages/
│   ├── INDEX.md              # Information architecture
│   ├── subjects/hari.yaml    # Subject assemblages
│   ├── encounters/           # 148 encounter assemblages
│   │   ├── person.yaml       # 42 (Farmer, Nurse, Trucker...)
│   │   ├── environment.yaml  # 15 
│   │   ├── object.yaml       # 14
│   │   ├── artwork.yaml      # 10
│   │   ├── event.yaml        # 15
│   │   ├── symbolic.yaml     # 10
│   │   ├── institution.yaml  # 9
│   │   ├── space.yaml        # 10
│   │   ├── temporal.yaml     # 9
│   │   └── relational.yaml   # 14
│   └── profiles/             # Life profiles (*.md)
│
├── engine/interaction.py     # LLM-based analysis
├── interactions/             # Generated interaction reports
├── reference/                # Reference docs (SKILL_TRANSFER.md)
└── THESIS.md
```

## Usage

```bash
python3 engine/interaction.py \
  --subject-name "Hari-Attention-Assemblage" \
  --encounter-name "The-Librarian-Assemblage" \
  --output interactions/attention_librarian.md
```

## Output

The engine produces rich semantic analysis:
- **Component Relationships**: TENSION, ALLIANCE, AMBIGUOUS
- **Effects**: AMPLIFY, ATROPHY, NARROW, TRANSFORM
- **Emergent Tensions**: Lines of flight
- **Virtual Capacities**: Potentials actualized
