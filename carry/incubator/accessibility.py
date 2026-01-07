"""
Accessibility Paths: How Assemblages Perceive and Leverage Each Other

The Problem:
- Proximity tells us HOW CLOSE assemblages are
- Accessibility tells us HOW ONE SEES ANOTHER from its own position

Key Insight: Accessibility is ASYMMETRIC.
- How Knife-Assemblage sees Cello-Assemblage differs from how Cello sees Knife
- Each assemblage has a "lens" (defined by its capacities) that determines what it can perceive

This moves beyond meta-assemblages (Philosophy, Writing) being the only positions
from which other assemblages can be envisioned. Now a Knife can "see" a Sea,
a Cello can "see" a Volcano - through their own specific capacities.

Accessibility Dimensions:
1. Capacity Lenses - What aspects of others can I perceive through my capacities?
2. Becoming Channels - Shared becoming vectors create mutual access
3. Intensity Resonance - Similar intensity values create visibility
4. Territory Analogies - Similar territory functions create mapping paths
5. Code Translation - How my codes can interpret/leverage other codes
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum
from pathlib import Path
import sys

# Import from existing engine
_carry_root = Path(__file__).parent.parent.parent
if str(_carry_root) not in sys.path:
    sys.path.insert(0, str(_carry_root))

from carry.engine.interaction import Assemblage, load_assemblages

# Optional LLM support
try:
    import google.generativeai as genai
    import os
    from dotenv import load_dotenv
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_KEY"))
    HAS_GENAI = True
except ImportError:
    genai = None
    HAS_GENAI = False


# =============================================================================
# DATA STRUCTURES
# =============================================================================

class AccessMode(Enum):
    """How one assemblage accesses another."""
    CAPACITY_LENS = "capacity_lens"       # Through its own capacities
    BECOMING_CHANNEL = "becoming_channel"  # Via shared becoming vectors
    INTENSITY_RESONANCE = "intensity_resonance"  # Similar intensity values
    TERRITORY_ANALOGY = "territory_analogy"  # Similar territory functions
    CODE_TRANSLATION = "code_translation"  # Codes that can interpret other codes


@dataclass
class AccessibilityPath:
    """A specific path from one assemblage to another."""
    source: str  # The perceiving assemblage
    target: str  # The perceived assemblage
    mode: AccessMode

    # What creates the path
    source_element: str  # The capacity/becoming/intensity/territory/code in source
    target_element: str  # What it accesses in target

    # Quality of access
    clarity: float  # 0.0 = opaque, 1.0 = crystal clear
    description: str  # Human-readable description of the path

    # What can be leveraged
    leverageable_capacities: List[str] = field(default_factory=list)
    potential_becomings: List[str] = field(default_factory=list)


@dataclass
class AssemblageLens:
    """The perceptual apparatus of an assemblage - what it can see in others."""
    assemblage_name: str

    # Capacity-based lenses (what aspects of others I can perceive)
    capacity_lenses: Dict[str, List[str]] = field(default_factory=dict)
    # Maps capacity name -> [perceivable aspects]
    # e.g., "Precision-Cutter" -> ["precision", "control", "exactness", "edge"]

    # Becoming channels (what becomings I share and can access through)
    becoming_channels: Set[str] = field(default_factory=set)

    # Intensity sensitivities (what intensity dimensions I'm attuned to)
    intensity_sensitivities: Dict[str, float] = field(default_factory=dict)
    # Maps dimension -> sensitivity (my own value defines what I can "see")

    # Territory analogies (what territory functions I can recognize)
    territory_analogies: List[str] = field(default_factory=list)


@dataclass
class AccessibilityMatrix:
    """Full accessibility mapping between all assemblages."""
    assemblage_names: List[str]
    lenses: Dict[str, AssemblageLens] = field(default_factory=dict)
    paths: Dict[Tuple[str, str], List[AccessibilityPath]] = field(default_factory=dict)

    def get_paths_from(self, source: str) -> List[AccessibilityPath]:
        """Get all accessibility paths from a source assemblage."""
        result = []
        for (src, tgt), paths in self.paths.items():
            if src == source:
                result.extend(paths)
        return result

    def get_paths_to(self, target: str) -> List[AccessibilityPath]:
        """Get all accessibility paths to a target assemblage."""
        result = []
        for (src, tgt), paths in self.paths.items():
            if tgt == target:
                result.extend(paths)
        return result

    def get_paths_between(self, source: str, target: str) -> List[AccessibilityPath]:
        """Get all paths from source to target."""
        return self.paths.get((source, target), [])

    def get_most_accessible_from(self, source: str, k: int = 5) -> List[Tuple[str, float]]:
        """Get k most accessible assemblages from source's perspective."""
        accessibility_scores = {}
        for path in self.get_paths_from(source):
            if path.target not in accessibility_scores:
                accessibility_scores[path.target] = 0.0
            accessibility_scores[path.target] += path.clarity

        sorted_scores = sorted(accessibility_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:k]


# =============================================================================
# CAPACITY LENS EXTRACTION
# =============================================================================

# Semantic mapping of capacities to perceivable aspects
CAPACITY_PERCEPTION_MAP = {
    # Precision/Attention capacities
    "precision": ["precision", "control", "exactness", "edge", "sharpness"],
    "attention": ["focus", "presence", "awareness", "clarity", "sustained"],
    "control": ["precision", "modulation", "restraint", "balance"],

    # Embodiment capacities
    "resonance": ["vibration", "depth", "body", "echo", "sound"],
    "gesture": ["movement", "flow", "stroke", "arc", "embodiment"],
    "breath": ["rhythm", "pace", "life", "flow", "cycle"],

    # Perception capacities
    "witness": ["observation", "seeing", "presence", "testimony", "clarity"],
    "gaze": ["horizon", "distance", "depth", "edge", "limit"],

    # Transformation capacities
    "transform": ["change", "becoming", "cutting", "destruction", "creation"],
    "cut": ["separation", "precision", "transformation", "edge"],

    # Rhythm/Cycle capacities
    "rhythm": ["cycle", "return", "pattern", "repetition", "tide"],
    "cycle": ["return", "rhythm", "repetition", "pattern"],
    "return": ["rhythm", "cycle", "practice", "ritual"],
}


def extract_capacity_lens(capacity_name: str, capacity_text: str) -> List[str]:
    """Extract what aspects of the world this capacity can perceive."""
    perceivable = set()

    # Check against semantic map
    text_lower = (capacity_name + " " + capacity_text).lower()

    for key, aspects in CAPACITY_PERCEPTION_MAP.items():
        if key in text_lower:
            perceivable.update(aspects)

    # Add direct terms from capacity
    words = text_lower.replace(",", " ").replace(".", " ").split()
    for word in words:
        if len(word) > 4:  # Skip short words
            perceivable.add(word)

    return list(perceivable)


def build_assemblage_lens(asm: Assemblage) -> AssemblageLens:
    """Build the perceptual lens for an assemblage."""
    lens = AssemblageLens(assemblage_name=asm.name)

    # Extract capacity lenses
    for comp in asm.components:
        perceivable = extract_capacity_lens(comp.name, comp.capacity)
        if perceivable:
            lens.capacity_lenses[comp.name] = perceivable

    # Becoming channels
    lens.becoming_channels = set(asm.becoming_vectors)

    # Intensity sensitivities (high values = strong sensitivity)
    for dim, value in asm.intensity_field.items():
        if value >= 0.6:  # Only sensitive to dimensions where we're strong
            lens.intensity_sensitivities[dim] = value

    # Territory analogies (extract territory functions)
    for terr in asm.territories:
        lens.territory_analogies.append(terr.function)

    return lens


# =============================================================================
# PATH COMPUTATION
# =============================================================================

def compute_capacity_paths(
    source: Assemblage,
    target: Assemblage,
    source_lens: AssemblageLens
) -> List[AccessibilityPath]:
    """Find paths from source to target through capacity lenses."""
    paths = []

    for comp_name, perceivable_aspects in source_lens.capacity_lenses.items():
        # Check each target component for matches
        for target_comp in target.components:
            target_text = (target_comp.name + " " + target_comp.capacity).lower()

            matching_aspects = []
            for aspect in perceivable_aspects:
                if aspect in target_text:
                    matching_aspects.append(aspect)

            if matching_aspects:
                clarity = min(1.0, len(matching_aspects) * 0.25)
                paths.append(AccessibilityPath(
                    source=source.name,
                    target=target.name,
                    mode=AccessMode.CAPACITY_LENS,
                    source_element=comp_name,
                    target_element=target_comp.name,
                    clarity=clarity,
                    description=f"{comp_name} perceives {', '.join(matching_aspects)} in {target_comp.name}",
                    leverageable_capacities=[target_comp.capacity],
                    potential_becomings=[]
                ))

    return paths


def compute_becoming_paths(
    source: Assemblage,
    target: Assemblage,
    source_lens: AssemblageLens
) -> List[AccessibilityPath]:
    """Find paths through shared becoming vectors."""
    paths = []

    shared_becomings = source_lens.becoming_channels & set(target.becoming_vectors)

    for becoming in shared_becomings:
        # Higher clarity for shared becomings
        paths.append(AccessibilityPath(
            source=source.name,
            target=target.name,
            mode=AccessMode.BECOMING_CHANNEL,
            source_element=becoming,
            target_element=becoming,
            clarity=0.8,  # Shared becomings are clear channels
            description=f"Both share {becoming}, creating direct access",
            leverageable_capacities=[c.capacity for c in target.components],
            potential_becomings=list(set(target.becoming_vectors) - {becoming})
        ))

    return paths


def compute_intensity_paths(
    source: Assemblage,
    target: Assemblage,
    source_lens: AssemblageLens
) -> List[AccessibilityPath]:
    """Find paths through intensity field resonance."""
    paths = []

    for dim, source_value in source_lens.intensity_sensitivities.items():
        target_value = target.intensity_field.get(dim, 0.5)

        # Resonance when both have high values
        if target_value >= 0.6:
            resonance = min(source_value, target_value)

            paths.append(AccessibilityPath(
                source=source.name,
                target=target.name,
                mode=AccessMode.INTENSITY_RESONANCE,
                source_element=f"{dim}:{source_value:.2f}",
                target_element=f"{dim}:{target_value:.2f}",
                clarity=resonance,
                description=f"High {dim} in both creates resonant visibility",
                leverageable_capacities=[],
                potential_becomings=[]
            ))

    return paths


def compute_territory_paths(
    source: Assemblage,
    target: Assemblage,
    source_lens: AssemblageLens
) -> List[AccessibilityPath]:
    """Find paths through territory function analogies."""
    paths = []

    # Keywords that indicate similar functions
    FUNCTION_ANALOGIES = {
        "daily": ["ritual", "practice", "return", "repetition"],
        "return": ["daily", "cycle", "rhythm", "repetition"],
        "edge": ["boundary", "liminal", "threshold", "between"],
        "contemplative": ["meditative", "slow", "attention", "presence"],
        "transformation": ["change", "becoming", "cutting", "destruction"],
    }

    for source_func in source_lens.territory_analogies:
        source_keywords = set(source_func.lower().split())

        for target_terr in target.territories:
            target_keywords = set(target_terr.function.lower().split())

            # Check for direct overlap
            direct_overlap = source_keywords & target_keywords

            # Check for analogical overlap
            analogical_overlap = set()
            for kw in source_keywords:
                for key, analogies in FUNCTION_ANALOGIES.items():
                    if kw == key or kw in analogies:
                        for analog in analogies:
                            if analog in target_keywords:
                                analogical_overlap.add(f"{kw}≈{analog}")

            if direct_overlap or analogical_overlap:
                clarity = 0.4 + (len(direct_overlap) * 0.2) + (len(analogical_overlap) * 0.15)
                paths.append(AccessibilityPath(
                    source=source.name,
                    target=target.name,
                    mode=AccessMode.TERRITORY_ANALOGY,
                    source_element=source_func,
                    target_element=target_terr.name,
                    clarity=min(1.0, clarity),
                    description=f"Territory analogy: '{source_func}' maps to '{target_terr.function}'",
                    leverageable_capacities=[],
                    potential_becomings=[]
                ))

    return paths


def compute_all_paths(
    source: Assemblage,
    target: Assemblage,
    source_lens: AssemblageLens
) -> List[AccessibilityPath]:
    """Compute all accessibility paths from source to target."""
    if source.name == target.name:
        return []

    paths = []
    paths.extend(compute_capacity_paths(source, target, source_lens))
    paths.extend(compute_becoming_paths(source, target, source_lens))
    paths.extend(compute_intensity_paths(source, target, source_lens))
    paths.extend(compute_territory_paths(source, target, source_lens))

    return paths


# =============================================================================
# MATRIX BUILDER
# =============================================================================

def build_accessibility_matrix(assemblages: List[Assemblage]) -> AccessibilityMatrix:
    """Build full accessibility matrix for all assemblage pairs."""
    names = [a.name for a in assemblages]
    name_to_asm = {a.name: a for a in assemblages}

    # Build lenses for all assemblages
    lenses = {}
    for asm in assemblages:
        lenses[asm.name] = build_assemblage_lens(asm)

    # Compute all paths (asymmetric - A->B different from B->A)
    paths = {}
    for source in assemblages:
        for target in assemblages:
            if source.name != target.name:
                key = (source.name, target.name)
                paths[key] = compute_all_paths(source, target, lenses[source.name])

    return AccessibilityMatrix(
        assemblage_names=names,
        lenses=lenses,
        paths=paths
    )


# =============================================================================
# REPORTS
# =============================================================================

def generate_accessibility_report(
    matrix: AccessibilityMatrix,
    assemblages: List[Assemblage]
) -> str:
    """Generate markdown report of accessibility paths."""
    lines = [
        "# Assemblage Accessibility Paths",
        "",
        "> How each assemblage perceives and can leverage others from its own position.",
        "",
        "---",
        ""
    ]

    for asm_name in matrix.assemblage_names:
        lens = matrix.lenses.get(asm_name)
        if not lens:
            continue

        lines.append(f"## {asm_name}")
        lines.append("")

        # Describe the lens
        lines.append("### Perceptual Lens")
        lines.append("")

        if lens.capacity_lenses:
            lines.append("**Capacity-based perception:**")
            for cap, aspects in lens.capacity_lenses.items():
                lines.append(f"- {cap} → can perceive: {', '.join(aspects[:5])}")
            lines.append("")

        if lens.becoming_channels:
            lines.append(f"**Becoming channels:** {', '.join(lens.becoming_channels)}")
            lines.append("")

        if lens.intensity_sensitivities:
            sens = [f"{dim}:{val:.1f}" for dim, val in lens.intensity_sensitivities.items()]
            lines.append(f"**Intensity sensitivities:** {', '.join(sens)}")
            lines.append("")

        # Accessibility to others
        lines.append("### Accessible Assemblages")
        lines.append("")

        most_accessible = matrix.get_most_accessible_from(asm_name, k=5)
        if most_accessible:
            lines.append("| Target | Total Clarity | Primary Path |")
            lines.append("|--------|---------------|--------------|")

            for target_name, clarity in most_accessible:
                paths = matrix.get_paths_between(asm_name, target_name)
                if paths:
                    best_path = max(paths, key=lambda p: p.clarity)
                    lines.append(f"| {target_name} | {clarity:.2f} | {best_path.mode.value}: {best_path.description[:50]}... |")
            lines.append("")

        # Detailed paths
        lines.append("### Detailed Paths")
        lines.append("")

        all_paths = matrix.get_paths_from(asm_name)

        # Group by mode
        by_mode = {}
        for path in all_paths:
            if path.mode not in by_mode:
                by_mode[path.mode] = []
            by_mode[path.mode].append(path)

        for mode, mode_paths in by_mode.items():
            lines.append(f"**{mode.value}:**")
            for path in sorted(mode_paths, key=lambda p: p.clarity, reverse=True)[:3]:
                lines.append(f"- → {path.target} (clarity: {path.clarity:.2f})")
                lines.append(f"  - {path.description}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def generate_path_narrative(
    source: Assemblage,
    target: Assemblage,
    paths: List[AccessibilityPath],
    model_name: str = "gemini-2.0-flash"
) -> str:
    """Use LLM to generate a narrative of how source perceives target."""
    if not HAS_GENAI:
        return "LLM not available for narrative generation."

    if not paths:
        return f"{source.name} has no clear paths to perceive {target.name}."

    paths_desc = "\n".join([
        f"- {p.mode.value}: {p.description} (clarity: {p.clarity:.2f})"
        for p in sorted(paths, key=lambda p: p.clarity, reverse=True)
    ])

    prompt = f"""You are describing how one assemblage perceives and could leverage another.

SOURCE ASSEMBLAGE: {source.name}
Abstract Machine: "{source.abstract_machine}"
Components: {[c.name for c in source.components]}
Becomings: {source.becoming_vectors}

TARGET ASSEMBLAGE: {target.name}
Abstract Machine: "{target.abstract_machine}"
Components: {[c.name for c in target.components]}
Becomings: {target.becoming_vectors}

ACCESSIBILITY PATHS FROM SOURCE TO TARGET:
{paths_desc}

Write 2-3 sentences describing HOW {source.name} perceives {target.name} from its own position.
What aspects does it see? What remains invisible? What could it leverage?
Focus on the specific paths - this is NOT a meta-philosophical view, but the view FROM the source assemblage.
"""

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Narrative generation failed: {e}"


# =============================================================================
# VISUALIZATION
# =============================================================================

def visualize_accessibility(
    matrix: AccessibilityMatrix,
    assemblages: List[Assemblage],
    output_path: str,
    min_clarity: float = 0.3
) -> None:
    """Generate interactive HTML network visualization of accessibility paths."""
    try:
        from pyvis.network import Network
    except ImportError:
        print("Warning: pyvis not installed. Skipping visualization.")
        return

    net = Network(
        height="800px",
        width="100%",
        directed=True,  # Accessibility is asymmetric
        bgcolor="#1a1a2e",
        font_color="#eee"
    )

    # Physics for directed graph
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "forceAtlas2Based": {
          "gravitationalConstant": -100,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.05
        },
        "solver": "forceAtlas2Based"
      },
      "edges": {
        "arrows": {"to": {"enabled": true, "scaleFactor": 0.5}},
        "smooth": {"type": "curvedCW", "roundness": 0.2}
      }
    }
    """)

    name_to_asm = {a.name: a for a in assemblages}

    # Color by assemblage type
    TYPE_COLORS = {
        "elemental": "#4ecdc4",    # Sea, Volcano, Calligraphy, Cello, Knife
        "practice": "#ffe66d",     # Attention, Witnessing
        "movement": "#ff6b6b",     # Nomad
        "cultural": "#95d5b2",     # Tamil
        "bodily": "#dda0dd",       # Body
    }

    def get_type_color(name: str) -> str:
        name_lower = name.lower()
        if any(x in name_lower for x in ["sea", "volcano", "calligraphy", "cello", "knife"]):
            return TYPE_COLORS["elemental"]
        if any(x in name_lower for x in ["attention", "witness"]):
            return TYPE_COLORS["practice"]
        if "nomad" in name_lower:
            return TYPE_COLORS["movement"]
        if "tamil" in name_lower:
            return TYPE_COLORS["cultural"]
        if "body" in name_lower:
            return TYPE_COLORS["bodily"]
        return "#888888"

    # Add nodes
    for name in matrix.assemblage_names:
        asm = name_to_asm.get(name)
        if not asm:
            continue

        lens = matrix.lenses.get(name)
        capacity_count = len(lens.capacity_lenses) if lens else 0
        becoming_count = len(lens.becoming_channels) if lens else 0

        tooltip = f"""<b>{name}</b><br>
<i>{asm.abstract_machine}</i><br><br>
<b>Capacity Lenses:</b> {capacity_count}<br>
<b>Becoming Channels:</b> {becoming_count}<br>
<b>Becomings:</b> {', '.join(asm.becoming_vectors)}
"""
        net.add_node(
            name,
            label=name.replace("Hari-", "").replace("-Assemblage", ""),
            title=tooltip,
            color=get_type_color(name),
            size=15 + capacity_count * 3
        )

    # Add edges (directed, with different colors by mode)
    MODE_COLORS = {
        AccessMode.CAPACITY_LENS: "#4ecdc4",
        AccessMode.BECOMING_CHANNEL: "#ffe66d",
        AccessMode.INTENSITY_RESONANCE: "#ff6b6b",
        AccessMode.TERRITORY_ANALOGY: "#95d5b2",
        AccessMode.CODE_TRANSLATION: "#dda0dd",
    }

    # Aggregate paths between pairs for cleaner visualization
    edge_data = {}  # (source, target) -> {total_clarity, best_path, modes}

    for (source, target), paths in matrix.paths.items():
        if not paths:
            continue

        # Filter by minimum clarity
        strong_paths = [p for p in paths if p.clarity >= min_clarity]
        if not strong_paths:
            continue

        total_clarity = sum(p.clarity for p in strong_paths)
        best_path = max(strong_paths, key=lambda p: p.clarity)
        modes = set(p.mode for p in strong_paths)

        edge_data[(source, target)] = {
            "total_clarity": total_clarity,
            "best_path": best_path,
            "modes": modes,
            "path_count": len(strong_paths)
        }

    for (source, target), data in edge_data.items():
        best = data["best_path"]

        # Color by primary mode
        color = MODE_COLORS.get(best.mode, "#888888")

        tooltip = f"""<b>{source} → {target}</b><br>
Total Clarity: {data['total_clarity']:.2f}<br>
Paths: {data['path_count']}<br>
Primary Mode: {best.mode.value}<br><br>
<i>{best.description}</i>
"""
        net.add_edge(
            source, target,
            title=tooltip,
            color=color,
            width=1 + data["total_clarity"],
            arrows="to"
        )

    net.save_graph(str(output_path))


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    from pathlib import Path

    carry_root = Path(__file__).parent.parent
    subjects_path = carry_root / "assemblages" / "subjects" / "hari.yaml"

    print("Loading assemblages...")
    assemblages = load_assemblages(subjects_path)
    print(f"Loaded {len(assemblages)} assemblages")

    print("\nBuilding accessibility matrix...")
    matrix = build_accessibility_matrix(assemblages)

    print(f"\nTotal paths computed: {sum(len(p) for p in matrix.paths.values())}")

    # Example: How does Knife see Cello?
    knife = next((a for a in assemblages if "Knife" in a.name), None)
    cello = next((a for a in assemblages if "Cello" in a.name), None)

    if knife and cello:
        print(f"\n{'='*60}")
        print(f"How {knife.name} perceives {cello.name}:")
        print(f"{'='*60}")

        paths = matrix.get_paths_between(knife.name, cello.name)
        for path in paths:
            print(f"\n  [{path.mode.value}] clarity={path.clarity:.2f}")
            print(f"    {path.source_element} → {path.target_element}")
            print(f"    {path.description}")

    # Generate full report
    print("\n\nGenerating full report...")
    report = generate_accessibility_report(matrix, assemblages)

    output_path = carry_root / "incubator" / "results" / "accessibility.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    print(f"Report saved to {output_path}")
