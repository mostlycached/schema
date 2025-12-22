"""
Assemblage Interaction Engine (LLM-Enhanced)

Uses an LLM to compute rich semantic relationships between assemblages,
similar to SKILL_TRANSFER.md's analysis of how "center-control" from chess
relates to typography skills (TENSION, ALLIANCE, etc.)

The LLM interprets:
1. WHY there is tension or alliance (not just numeric difference)
2. How each component might atrophy, amplify, narrow, or transform
3. What new lines of flight emerge from the interaction
4. What virtualities might be actualized
"""

import os
import json
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


# =============================================================================
# DATA STRUCTURES
# =============================================================================

class RelationType(Enum):
    TENSION = "tension"
    ALLIANCE = "alliance"
    NEUTRAL = "neutral"


class EffectType(Enum):
    AMPLIFICATION = "amplification"
    ATROPHY = "atrophy"
    NARROWING = "narrowing"
    TRANSFORMATION = "transformation"
    UNCHANGED = "unchanged"


@dataclass
class Territory:
    name: str
    function: str
    quality: str
    space_type: str  # "smooth" or "striated"


@dataclass
class Code:
    name: str
    content: str
    type: str
    level: str  # "molar" or "molecular"


@dataclass
class Component:
    name: str
    type: str
    capacity: str


@dataclass
class VirtualCapacity:
    name: str
    access_point: str
    reason_unactualized: str


@dataclass
class Assemblage:
    name: str
    abstract_machine: str
    entity_type: str = "subject"  # "subject", "person", "environment", etc.
    
    territories: List[Territory] = field(default_factory=list)
    codes: List[Code] = field(default_factory=list)
    components: List[Component] = field(default_factory=list)
    
    intensity_field: Dict[str, float] = field(default_factory=dict)
    becoming_vectors: List[str] = field(default_factory=list)
    stratification_depth: float = 0.5
    
    virtual_capacities: List[VirtualCapacity] = field(default_factory=list)


@dataclass
class IntensityRelation:
    """Relationship between two assemblages on a specific intensity dimension."""
    dimension: str
    value_a: float
    value_b: float
    relation: RelationType
    difference: float


@dataclass
class TerritoryRelation:
    """Compatibility between territories."""
    territory_a: str
    territory_b: str
    space_type_a: str
    space_type_b: str
    relation: RelationType
    note: str


@dataclass
class CodeConflict:
    """Potential conflict between codes."""
    code_a: str
    code_b: str
    conflict_type: str  # "molar-molar", "molar-molecular", "molecular-molecular"
    description: str


@dataclass
class AssemblageEffect:
    """Effect on a component of the subject assemblage."""
    component_name: str
    effect_type: EffectType
    cause: str
    description: str


@dataclass
class LineOfFlightEmergence:
    """Emergent line of flight from the interaction."""
    direction: str
    source_type: str  # "tension", "alliance", "irreconcilable"
    source_description: str


@dataclass
class InteractionResult:
    """Full result of an assemblage interaction."""
    subject: Assemblage
    encounter: Assemblage
    
    intensity_relations: List[IntensityRelation] = field(default_factory=list)
    territory_relations: List[TerritoryRelation] = field(default_factory=list)
    code_conflicts: List[CodeConflict] = field(default_factory=list)
    
    effects: List[AssemblageEffect] = field(default_factory=list)
    lines_of_flight: List[LineOfFlightEmergence] = field(default_factory=list)
    
    becoming_vectors_activated: List[str] = field(default_factory=list)
    virtual_capacities_actualized: List[str] = field(default_factory=list)


# =============================================================================
# LOADERS
# =============================================================================

def load_assemblages(yaml_path: Path) -> List[Assemblage]:
    """Load assemblages from YAML file."""
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    assemblages = []
    for asm_data in data.get('assemblages', []):
        territories = [Territory(**t) for t in asm_data.get('territories', [])]
        codes = [Code(**c) for c in asm_data.get('codes', [])]
        components = [Component(**c) for c in asm_data.get('components', [])]
        
        virtual_caps = []
        for vc in asm_data.get('virtual_capacities', []):
            if isinstance(vc, dict):
                virtual_caps.append(VirtualCapacity(**vc))
            else:
                virtual_caps.append(VirtualCapacity(name=str(vc), access_point="", reason_unactualized=""))
        
        assemblages.append(Assemblage(
            name=asm_data['name'],
            abstract_machine=asm_data['abstract_machine'],
            entity_type=asm_data.get('entity_type', 'subject'),
            territories=territories,
            codes=codes,
            components=components,
            intensity_field=asm_data.get('intensity_field', {}),
            becoming_vectors=asm_data.get('becoming_vectors', []),
            stratification_depth=asm_data.get('stratification_depth', 0.5),
            virtual_capacities=virtual_caps,
        ))
    
    return assemblages


# =============================================================================
# INTERACTION MECHANICS
# =============================================================================

def compute_intensity_relations(a: Assemblage, b: Assemblage) -> List[IntensityRelation]:
    """Compare intensity fields to find tension/alliance/neutral."""
    relations = []
    all_dims = set(a.intensity_field.keys()) | set(b.intensity_field.keys())
    
    for dim in all_dims:
        v_a = a.intensity_field.get(dim, 0.5)
        v_b = b.intensity_field.get(dim, 0.5)
        diff = abs(v_a - v_b)
        
        if diff > 0.5:
            rel = RelationType.TENSION
        elif diff < 0.2:
            rel = RelationType.ALLIANCE
        else:
            rel = RelationType.NEUTRAL
        
        relations.append(IntensityRelation(
            dimension=dim,
            value_a=v_a,
            value_b=v_b,
            relation=rel,
            difference=diff
        ))
    
    return relations


def compute_territory_relations(a: Assemblage, b: Assemblage) -> List[TerritoryRelation]:
    """Analyze territory compatibility."""
    relations = []
    
    for t_a in a.territories:
        for t_b in b.territories:
            if t_a.space_type != t_b.space_type:
                rel = RelationType.TENSION
                note = f"Space type conflict: {t_a.space_type} vs {t_b.space_type}"
            else:
                rel = RelationType.ALLIANCE
                note = f"Compatible space type: {t_a.space_type}"
            
            relations.append(TerritoryRelation(
                territory_a=t_a.name,
                territory_b=t_b.name,
                space_type_a=t_a.space_type,
                space_type_b=t_b.space_type,
                relation=rel,
                note=note
            ))
    
    return relations


def detect_code_conflicts(a: Assemblage, b: Assemblage) -> List[CodeConflict]:
    """Detect potential conflicts between codes."""
    conflicts = []
    
    for c_a in a.codes:
        for c_b in b.codes:
            conflict_type = f"{c_a.level}-{c_b.level}"
            
            # Molar-molar conflicts are most visible
            if c_a.level == "molar" and c_b.level == "molar":
                conflicts.append(CodeConflict(
                    code_a=c_a.name,
                    code_b=c_b.name,
                    conflict_type=conflict_type,
                    description=f"'{c_a.content}' vs '{c_b.content}'"
                ))
            # Molecular codes from encounter may infiltrate
            elif c_a.level == "molar" and c_b.level == "molecular":
                conflicts.append(CodeConflict(
                    code_a=c_a.name,
                    code_b=c_b.name,
                    conflict_type=conflict_type,
                    description=f"Molecular '{c_b.content}' may destabilize molar '{c_a.content}'"
                ))
    
    return conflicts


def compute_effects(
    subject: Assemblage,
    encounter: Assemblage,
    intensity_relations: List[IntensityRelation],
    code_conflicts: List[CodeConflict]
) -> List[AssemblageEffect]:
    """Compute effects on subject's components."""
    effects = []
    
    # Count tensions and alliances
    tensions = [r for r in intensity_relations if r.relation == RelationType.TENSION]
    alliances = [r for r in intensity_relations if r.relation == RelationType.ALLIANCE]
    
    for comp in subject.components:
        # Find related intensity dimensions
        effect_type = EffectType.UNCHANGED
        cause = ""
        description = ""
        
        # High tension count -> atrophy or transformation
        if len(tensions) > len(alliances):
            # Check for irreconcilable tension (opposite extremes)
            extreme_tensions = [t for t in tensions if t.difference > 0.7]
            if extreme_tensions:
                effect_type = EffectType.TRANSFORMATION
                cause = f"Extreme tension on {extreme_tensions[0].dimension}"
                description = f"{comp.name} may mutate under pressure from encounter's opposite logic"
            else:
                effect_type = EffectType.ATROPHY
                cause = f"Multiple tensions: {', '.join(t.dimension for t in tensions[:2])}"
                description = f"{comp.name} may weaken as encounter's logic dominates"
        
        # High alliance count -> amplification or narrowing
        elif len(alliances) > len(tensions):
            effect_type = EffectType.AMPLIFICATION
            cause = f"Alliance on {', '.join(a.dimension for a in alliances[:2])}"
            description = f"{comp.name} may strengthen through resonance with encounter"
        
        if effect_type != EffectType.UNCHANGED:
            effects.append(AssemblageEffect(
                component_name=comp.name,
                effect_type=effect_type,
                cause=cause,
                description=description
            ))
    
    return effects


def compute_lines_of_flight(
    subject: Assemblage,
    encounter: Assemblage,
    intensity_relations: List[IntensityRelation],
    territory_relations: List[TerritoryRelation]
) -> List[LineOfFlightEmergence]:
    """Generate emergent lines of flight."""
    lines = []
    
    # Extreme tensions open lines of flight
    extreme_tensions = [r for r in intensity_relations if r.difference > 0.6]
    for t in extreme_tensions:
        lines.append(LineOfFlightEmergence(
            direction=f"Escape from {t.dimension} tension",
            source_type="tension",
            source_description=f"{subject.name} ({t.value_a:.1f}) vs {encounter.name} ({t.value_b:.1f}) on {t.dimension}"
        ))
    
    # Strong alliances open lines of flight through intensification
    strong_alliances = [r for r in intensity_relations if r.relation == RelationType.ALLIANCE and r.value_a > 0.7]
    for a in strong_alliances:
        lines.append(LineOfFlightEmergence(
            direction=f"Intensification of {a.dimension}",
            source_type="alliance",
            source_description=f"Both assemblages high on {a.dimension} ({a.value_a:.1f})"
        ))
    
    # Territory conflicts open lines of flight
    territory_tensions = [r for r in territory_relations if r.relation == RelationType.TENSION]
    if territory_tensions:
        lines.append(LineOfFlightEmergence(
            direction=f"Deterritorialization from {territory_tensions[0].territory_a}",
            source_type="territory_conflict",
            source_description=f"Striated {territory_tensions[0].territory_a} meets smooth {territory_tensions[0].territory_b}"
        ))
    
    # Becoming vectors from encounter may activate
    for bv in encounter.becoming_vectors:
        if bv not in subject.becoming_vectors:
            lines.append(LineOfFlightEmergence(
                direction=f"New becoming: {bv}",
                source_type="becoming_transfer",
                source_description=f"Encounter's {bv} activates in subject"
            ))
    
    return lines


def interact(subject: Assemblage, encounter: Assemblage) -> InteractionResult:
    """Full interaction computation."""
    intensity_relations = compute_intensity_relations(subject, encounter)
    territory_relations = compute_territory_relations(subject, encounter)
    code_conflicts = detect_code_conflicts(subject, encounter)
    effects = compute_effects(subject, encounter, intensity_relations, code_conflicts)
    lines_of_flight = compute_lines_of_flight(subject, encounter, intensity_relations, territory_relations)
    
    # Check for becoming vector activation
    activated_becomings = [bv for bv in encounter.becoming_vectors if bv not in subject.becoming_vectors]
    
    # Check for virtual capacity actualization
    actualized = []
    for vc in subject.virtual_capacities:
        # If encounter's intensities align with virtual capacity, it may actualize
        for ir in intensity_relations:
            if ir.relation == RelationType.ALLIANCE and ir.value_b > 0.7:
                actualized.append(vc.name)
                break
    
    return InteractionResult(
        subject=subject,
        encounter=encounter,
        intensity_relations=intensity_relations,
        territory_relations=territory_relations,
        code_conflicts=code_conflicts,
        effects=effects,
        lines_of_flight=lines_of_flight,
        becoming_vectors_activated=activated_becomings,
        virtual_capacities_actualized=actualized
    )


# =============================================================================
# LLM-ENHANCED INTERACTION (SKILL_TRANSFER.md style)
# =============================================================================

def describe_assemblage(a: Assemblage) -> str:
    """Generate a rich text description of an assemblage for LLM prompting."""
    lines = [
        f"**{a.name}**",
        f"Abstract Machine: \"{a.abstract_machine}\"",
        "",
        "Territories:",
    ]
    for t in a.territories:
        lines.append(f"  - {t.name}: {t.function} ({t.space_type})")
    
    lines.append("")
    lines.append("Codes:")
    for c in a.codes:
        lines.append(f"  - {c.name} [{c.level}]: \"{c.content}\"")
    
    lines.append("")
    lines.append("Components:")
    for c in a.components:
        lines.append(f"  - {c.name}: {c.capacity}")
    
    lines.append("")
    lines.append(f"Intensity Field: {a.intensity_field}")
    lines.append(f"Becoming Vectors: {a.becoming_vectors}")
    
    if a.virtual_capacities:
        lines.append("")
        lines.append("Virtual Capacities (unactualized):")
        for vc in a.virtual_capacities:
            lines.append(f"  - {vc.name}: {vc.reason_unactualized}")
    
    return "\n".join(lines)


def interact_llm(
    subject: Assemblage,
    encounter: Assemblage,
    model_name: str = "gemini-2.0-flash"
) -> str:
    """
    Use an LLM to generate rich semantic analysis of how the encounter
    affects the subject's assemblage, similar to SKILL_TRANSFER.md.
    
    Returns a markdown report.
    """
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""You are a Deleuzian analyst performing a SKILL_TRANSFER.md-style analysis.

SUBJECT ASSEMBLAGE:
{describe_assemblage(subject)}

ENCOUNTER ASSEMBLAGE:
{describe_assemblage(encounter)}

---

Analyze how the ENCOUNTER ASSEMBLAGE would affect the SUBJECT ASSEMBLAGE.
For EACH component of the subject, determine its relationship to the encounter:

RELATIONSHIP TYPES:
- **TENSION**: The component and encounter work on opposite logics (explain WHY)
- **STRONG ALLIANCE**: They reinforce each other (explain WHY)
- **AMBIGUOUS TENSION**: Partial conflict, partial resonance (explain the nuance)
- **MODERATE ALLIANCE**: Some resonance but not strong (explain)
- **NEUTRAL**: No significant interaction

For each relationship, explain:
1. WHY this relationship exists (the logic, not just the numbers)
2. EFFECT on the component: Does it AMPLIFY, ATROPHY, NARROW, or TRANSFORM?
3. What is LOST and what is GAINED through this interaction?

Then identify:
- EMERGENT TENSIONS that create potential lines of flight
- TRANSVERSAL LINES (when multiple components ally against or with the encounter)
- VIRTUAL CAPACITIES that might be actualized by this encounter

Write in the style of SKILL_TRANSFER.md - concrete, specific, insightful.

Format your analysis as markdown with clear sections:

# {subject.name} × {encounter.name}

## Component Relationships

### [Component Name]
- **Relation**: [TENSION/ALLIANCE/etc]
- **Why**: [Explanation of the logic]
- **Effect**: [AMPLIFY/ATROPHY/NARROW/TRANSFORM]
- **What's Lost**: [...]
- **What's Gained**: [...]

[Repeat for each component]

## Emergent Tensions

[List tensions that might force a line of flight]

## Transversal Lines

[Alliances or oppositions that span multiple components]

## Virtual Capacities Potentially Actualized

[Which unactualized potentials might this encounter trigger?]

## New Dispositions After Encounter

[A table or list showing how each component has changed]
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating LLM analysis: {e}"

def generate_report(result: InteractionResult) -> str:
    """Generate a markdown report of the interaction."""
    lines = [
        f"# Assemblage Interaction: {result.subject.name} × {result.encounter.name}",
        "",
        f"**Subject**: {result.subject.name}",
        f"**Subject Machine**: *{result.subject.abstract_machine}*",
        "",
        f"**Encounter**: {result.encounter.name}",
        f"**Encounter Machine**: *{result.encounter.abstract_machine}*",
        "",
        "---",
        "",
        "## Intensity Field Relations",
        "",
        "| Dimension | Subject | Encounter | Relation |",
        "|-----------|---------|-----------|----------|",
    ]
    
    for ir in result.intensity_relations:
        emoji = "⚡" if ir.relation == RelationType.TENSION else ("🤝" if ir.relation == RelationType.ALLIANCE else "➖")
        lines.append(f"| {ir.dimension} | {ir.value_a:.2f} | {ir.value_b:.2f} | {emoji} **{ir.relation.value.upper()}** |")
    
    lines.extend(["", "---", "", "## Territory Relations", ""])
    
    tension_terrs = [t for t in result.territory_relations if t.relation == RelationType.TENSION]
    alliance_terrs = [t for t in result.territory_relations if t.relation == RelationType.ALLIANCE]
    
    if tension_terrs:
        lines.append("### Tensions (Striated vs Smooth)")
        for tr in tension_terrs[:3]:
            lines.append(f"- **{tr.territory_a}** ({tr.space_type_a}) ⚡ **{tr.territory_b}** ({tr.space_type_b})")
    
    if alliance_terrs:
        lines.append("")
        lines.append("### Alliances (Compatible Space)")
        for tr in alliance_terrs[:3]:
            lines.append(f"- **{tr.territory_a}** 🤝 **{tr.territory_b}** ({tr.space_type_a})")
    
    lines.extend(["", "---", "", "## Code Conflicts", ""])
    
    if result.code_conflicts:
        for cc in result.code_conflicts[:5]:
            lines.append(f"- **{cc.code_a}** vs **{cc.code_b}** [{cc.conflict_type}]")
            lines.append(f"  - {cc.description}")
    else:
        lines.append("*No significant code conflicts detected*")
    
    lines.extend(["", "---", "", "## Effects on Subject", ""])
    
    if result.effects:
        for ef in result.effects:
            emoji = {"amplification": "📈", "atrophy": "📉", "narrowing": "🔍", "transformation": "🔄", "unchanged": "➖"}
            lines.append(f"### {emoji.get(ef.effect_type.value, '')} {ef.component_name}: **{ef.effect_type.value.upper()}**")
            lines.append(f"- **Cause**: {ef.cause}")
            lines.append(f"- **Effect**: {ef.description}")
            lines.append("")
    else:
        lines.append("*No significant effects computed*")
    
    lines.extend(["---", "", "## Lines of Flight Opened", ""])
    
    if result.lines_of_flight:
        for lof in result.lines_of_flight:
            lines.append(f"### → {lof.direction}")
            lines.append(f"- **Source**: {lof.source_type}")
            lines.append(f"- **Description**: {lof.source_description}")
            lines.append("")
    else:
        lines.append("*No lines of flight detected*")
    
    if result.becoming_vectors_activated:
        lines.extend(["---", "", "## Becomings Activated", ""])
        for bv in result.becoming_vectors_activated:
            lines.append(f"- **{bv}**")
    
    if result.virtual_capacities_actualized:
        lines.extend(["---", "", "## Virtual Capacities Potentially Actualized", ""])
        for vc in result.virtual_capacities_actualized:
            lines.append(f"- **{vc}**")
    
    return "\n".join(lines)


# =============================================================================
# MULTI-FILE LOADER
# =============================================================================

def load_all_encounters(encounters_dir: Path) -> List[Assemblage]:
    """Load all encounter assemblages from a directory tree of YAML files."""
    all_assemblages = []
    if encounters_dir.is_dir():
        # Recursively find all YAML files in subdirectories
        for yaml_file in encounters_dir.rglob("*.yaml"):
            try:
                all_assemblages.extend(load_assemblages(yaml_file))
            except Exception as e:
                print(f"Warning: Could not load {yaml_file}: {e}")
    elif encounters_dir.is_file():
        all_assemblages = load_assemblages(encounters_dir)
    return all_assemblages


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    # Default paths relative to carry/ root
    carry_root = Path(__file__).parent.parent
    default_subject = carry_root / "assemblages" / "subjects" / "hari.yaml"
    default_encounters = carry_root / "assemblages" / "encounters"
    
    parser = argparse.ArgumentParser(description="Compute assemblage interactions using LLM.")
    parser.add_argument("--subject", type=Path, default=default_subject,
                        help="Path to subject assemblages YAML")
    parser.add_argument("--encounters", type=Path, default=default_encounters,
                        help="Path to encounter assemblages (YAML file or directory)")
    parser.add_argument("--subject-name", type=str, help="Name of specific subject assemblage")
    parser.add_argument("--encounter-name", type=str, help="Name of specific encounter assemblage")
    parser.add_argument("--output", type=Path, help="Output markdown file")
    
    args = parser.parse_args()
    
    # Load assemblages
    subject_assemblages = load_assemblages(args.subject)
    encounter_assemblages = load_all_encounters(args.encounters)
    
    print(f"Loaded {len(subject_assemblages)} subject assemblages from {args.subject}")
    print(f"Loaded {len(encounter_assemblages)} encounter assemblages from {args.encounters}")
    
    # Select assemblages
    if args.subject_name:
        subject = next((a for a in subject_assemblages if a.name == args.subject_name), subject_assemblages[0])
    else:
        subject = subject_assemblages[0]
    
    if args.encounter_name:
        encounter = next((a for a in encounter_assemblages if a.name == args.encounter_name), encounter_assemblages[0])
    else:
        encounter = encounter_assemblages[0]
    
    print(f"\nAnalyzing: {subject.name} × {encounter.name}")
    
    report = interact_llm(subject, encounter)
    
    if args.output:
        args.output.write_text(report)
        print(f"Report saved to: {args.output}")
    else:
        print("\n" + report)
