# Carry: Objects That Reshape Ontology

A simulation framework exploring how carry objects (physical, symbolic, mathematical, ontological) reshape a human's intra and inter-external relations through persistent presence.

## Core Insight

> *"When a foreign object is introduced, it forces a gravitational response through its persistence, affecting the human's ontological internal and inter-external relations."*

Like a cane modifying a blind person's intra and inter relations — the carry object doesn't just help, it *restructures* the entire mode of being.

## Structure

```
carry/
├── THESIS.md           # Founding concept
├── CARRY_INDEX.md      # Catalog of carry objects
└── simulation/
    ├── carry.py        # CarryObject dataclass & canonical objects
    └── injection.py    # Injection simulation & reports
```

## Usage

```python
from carry.simulation import (
    get_canonical_object,
    inject_carry_object,
    generate_injection_report,
)

# Get a pre-defined carry object
cane = get_canonical_object("cane")

# Simulate injection into a subject's lifeworld
result = inject_carry_object(
    carry_object=cane,
    subject_name="Elena",
    subject_age=34,
    subject_context="Recently lost vision due to diabetic retinopathy"
)

# Generate report
report = generate_injection_report(result, "results/elena_cane.md")
```

## CLI

```bash
# Run example injection
python -m carry.simulation.injection --object cane --subject Elena --age 34

# With context  
python -m carry.simulation.injection \
    --object smartphone \
    --subject Marcus \
    --age 16 \
    --context "First smartphone, previously used flip phone" \
    --output-dir results/
```

## Canonical Objects

| Key | Name | Type | Animism |
|-----|------|------|---------|
| `cane` | White cane | Physical | Earth |
| `smartphone` | Smartphone | Physical | Jaw |
| `wedding_ring` | Wedding ring | Symbolic | Earth |
| `calculus` | Calculus | Mathematical | Knife |
| `spinoza` | Spinoza's immanence | Ontological | Fire |
| `diagnosis_adhd` | ADHD diagnosis | Ontological | Knife |

## The Three Phases

Every carry object injection follows this arc:

1. **Disruption**: Object's persistence creates friction with existing Stances
2. **Reconfiguration**: Novelty search finds new Stance-Component bindings
3. **Sedimentation**: New configuration becomes habitual, invisible

The deeper the carry (ontological > mathematical > symbolic > physical), the more complete the sedimentation — and the harder to remove.
