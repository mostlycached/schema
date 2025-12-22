"""
Visualization Module: Network Graphs for Assemblage Clusters

Uses pyvis to generate interactive HTML network visualizations.
"""

from pathlib import Path
from typing import List, Optional, Dict

from pyvis.network import Network

from carry.incubator.proximity import ProximityMatrix, ProximityScore, SpaceCompatibility
from carry.incubator.cluster import IncubationCluster, ClusteringResult
from carry.incubator.incubation import IncubationResult, TransversalLine
from carry.engine.interaction import Assemblage


# =============================================================================
# COLOR SCHEMES
# =============================================================================

SPACE_TYPE_COLORS = {
    "smooth": "#4CAF50",      # Green - nomadic, open
    "striated": "#2196F3",    # Blue - organized, controlled
    "mixed": "#9C27B0",       # Purple - hybrid
}

RELATION_COLORS = {
    "alliance": "#4CAF50",    # Green
    "resonance": "#8BC34A",   # Light green
    "opposition": "#F44336",  # Red
    "tension": "#FF9800",     # Orange
    "neutral": "#9E9E9E",     # Gray
}

CLUSTER_COLORS = [
    "#E91E63",  # Pink
    "#00BCD4",  # Cyan
    "#FFEB3B",  # Yellow
    "#795548",  # Brown
    "#607D8B",  # Blue Gray
    "#FF5722",  # Deep Orange
    "#3F51B5",  # Indigo
    "#009688",  # Teal
]


# =============================================================================
# NETWORK BUILDERS
# =============================================================================

def get_dominant_space_type(asm: Assemblage) -> str:
    """Determine dominant space type for an assemblage."""
    if not asm.territories:
        return "mixed"
    smooth = sum(1 for t in asm.territories if t.space_type == "smooth")
    striated = len(asm.territories) - smooth
    if smooth > striated:
        return "smooth"
    elif striated > smooth:
        return "striated"
    return "mixed"


def build_proximity_network(
    matrix: ProximityMatrix,
    assemblages: List[Assemblage],
    threshold: float = 0.3,
    height: str = "800px",
    width: str = "100%"
) -> Network:
    """
    Build a network graph from proximity matrix.

    Nodes = assemblages
    Edges = proximity scores above threshold
    """
    net = Network(
        height=height,
        width=width,
        bgcolor="#1a1a2e",
        font_color="white",
        directed=False
    )

    # Physics settings for better layout
    net.barnes_hut(
        gravity=-3000,
        central_gravity=0.3,
        spring_length=200,
        spring_strength=0.05,
        damping=0.09
    )

    name_to_asm = {a.name: a for a in assemblages}

    # Add nodes
    for name in matrix.assemblage_names:
        asm = name_to_asm.get(name)
        if not asm:
            continue

        space_type = get_dominant_space_type(asm)
        color = SPACE_TYPE_COLORS.get(space_type, "#9E9E9E")

        # Size based on number of components
        size = 20 + len(asm.components) * 5

        # Build tooltip
        tooltip = f"""<b>{name}</b><br>
<i>{asm.abstract_machine}</i><br><br>
<b>Territories:</b> {', '.join(t.name for t in asm.territories)}<br>
<b>Space Type:</b> {space_type}<br>
<b>Becomings:</b> {', '.join(asm.becoming_vectors)}<br>
<b>Stratification:</b> {asm.stratification_depth:.2f}
"""

        net.add_node(
            name,
            label=name.replace("-Assemblage", "").replace("Hari-", ""),
            title=tooltip,
            color=color,
            size=size,
            shape="dot",
            borderWidth=2,
            borderWidthSelected=4
        )

    # Add edges
    for (name_a, name_b), score in matrix.scores.items():
        if score.composite_score < threshold:
            continue

        # Edge color based on space compatibility
        if score.space_compatibility == SpaceCompatibility.OPPOSING:
            edge_color = RELATION_COLORS["tension"]
        elif score.space_compatibility in (SpaceCompatibility.BOTH_SMOOTH, SpaceCompatibility.BOTH_STRIATED):
            edge_color = RELATION_COLORS["alliance"]
        else:
            edge_color = RELATION_COLORS["neutral"]

        # Edge width based on proximity
        width = 1 + score.composite_score * 5

        # Build edge tooltip
        edge_tooltip = f"""<b>{name_a}</b> ↔ <b>{name_b}</b><br><br>
<b>Composite:</b> {score.composite_score:.3f}<br>
<b>Intensity:</b> {score.intensity_proximity:.3f}<br>
<b>Space:</b> {score.space_type_proximity:.3f}<br>
<b>Semantic:</b> {score.semantic_proximity:.3f}<br>
<b>Becoming:</b> {score.becoming_overlap:.3f}<br>
<b>Shared:</b> {', '.join(score.shared_becomings) or 'none'}
"""

        net.add_edge(
            name_a,
            name_b,
            value=score.composite_score,
            width=width,
            color=edge_color,
            title=edge_tooltip
        )

    return net


def build_cluster_network(
    clustering: ClusteringResult,
    height: str = "800px",
    width: str = "100%"
) -> Network:
    """
    Build a network graph showing cluster membership.

    Nodes colored by cluster, with cluster centroids.
    """
    net = Network(
        height=height,
        width=width,
        bgcolor="#1a1a2e",
        font_color="white",
        directed=False
    )

    net.barnes_hut(
        gravity=-2000,
        central_gravity=0.5,
        spring_length=150,
        spring_strength=0.08,
        damping=0.09
    )

    # Add cluster nodes and member nodes
    for cluster in clustering.clusters:
        cluster_color = CLUSTER_COLORS[cluster.cluster_id % len(CLUSTER_COLORS)]

        # Add cluster centroid node
        centroid_id = f"cluster_{cluster.cluster_id}"
        centroid_tooltip = f"""<b>Cluster {cluster.cluster_id}</b><br><br>
<b>Members:</b> {len(cluster.assemblages)}<br>
<b>Cohesion:</b> {cluster.internal_cohesion:.3f}<br>
<b>Diversity:</b> {cluster.diversity_score:.3f}<br>
<b>Tension:</b> {cluster.tension_potential:.3f}<br>
<b>Space:</b> {cluster.dominant_space_type}<br>
<b>Shared Becomings:</b> {', '.join(cluster.shared_becomings) or 'none'}
"""

        net.add_node(
            centroid_id,
            label=f"C{cluster.cluster_id}",
            title=centroid_tooltip,
            color=cluster_color,
            size=40,
            shape="diamond",
            borderWidth=3
        )

        # Add member nodes
        for asm in cluster.assemblages:
            space_type = get_dominant_space_type(asm)

            tooltip = f"""<b>{asm.name}</b><br>
<i>{asm.abstract_machine}</i><br><br>
<b>Cluster:</b> {cluster.cluster_id}<br>
<b>Space:</b> {space_type}
"""

            net.add_node(
                asm.name,
                label=asm.name.replace("-Assemblage", "").replace("Hari-", ""),
                title=tooltip,
                color=cluster_color,
                size=25,
                shape="dot",
                borderWidth=2
            )

            # Connect to centroid
            net.add_edge(
                centroid_id,
                asm.name,
                color=cluster_color,
                width=2,
                dashes=True
            )

        # Add intra-cluster edges
        matrix = clustering.proximity_matrix
        for i, asm_a in enumerate(cluster.assemblages):
            for asm_b in cluster.assemblages[i+1:]:
                score = matrix.get_score(asm_a.name, asm_b.name)
                if score and score.composite_score > 0.4:
                    net.add_edge(
                        asm_a.name,
                        asm_b.name,
                        value=score.composite_score,
                        width=1 + score.composite_score * 3,
                        color={"color": cluster_color, "opacity": 0.6},
                        title=f"Proximity: {score.composite_score:.3f}"
                    )

    # Add noise nodes
    for asm in clustering.noise:
        space_type = get_dominant_space_type(asm)
        color = SPACE_TYPE_COLORS.get(space_type, "#9E9E9E")

        net.add_node(
            asm.name,
            label=asm.name.replace("-Assemblage", "").replace("Hari-", ""),
            title=f"<b>{asm.name}</b><br><i>Unclustered</i>",
            color=color,
            size=20,
            shape="dot",
            borderWidth=1,
            opacity=0.6
        )

    return net


def build_incubation_network(
    result: IncubationResult,
    height: str = "900px",
    width: str = "100%"
) -> Network:
    """
    Build a network graph showing incubation dynamics.

    Shows assemblages, transversal lines, and emerged assemblage.
    """
    net = Network(
        height=height,
        width=width,
        bgcolor="#1a1a2e",
        font_color="white",
        directed=False
    )

    net.barnes_hut(
        gravity=-4000,
        central_gravity=0.2,
        spring_length=250,
        spring_strength=0.04,
        damping=0.09
    )

    cluster = result.cluster
    fertility = result.fertility_assessment

    # Add parent assemblage nodes
    for asm in cluster.assemblages:
        space_type = get_dominant_space_type(asm)
        color = SPACE_TYPE_COLORS.get(space_type, "#9E9E9E")

        tooltip = f"""<b>{asm.name}</b><br>
<i>{asm.abstract_machine}</i><br><br>
<b>Territories:</b> {', '.join(t.name for t in asm.territories)}<br>
<b>Codes:</b> {', '.join(c.name for c in asm.codes)}<br>
<b>Components:</b> {', '.join(c.name for c in asm.components)}<br>
<b>Becomings:</b> {', '.join(asm.becoming_vectors)}
"""

        net.add_node(
            asm.name,
            label=asm.name.replace("-Assemblage", "").replace("Hari-", ""),
            title=tooltip,
            color=color,
            size=35,
            shape="dot",
            borderWidth=3
        )

    # Add transversal line edges
    line_edges = {}  # Track edges to combine parallel lines

    for line in result.transversal_lines:
        participants = line.participating_assemblages

        # Create edges between all participants
        for i, p1 in enumerate(participants):
            for p2 in participants[i+1:]:
                edge_key = tuple(sorted([p1, p2]))

                if edge_key not in line_edges:
                    line_edges[edge_key] = {
                        "alliances": [],
                        "oppositions": [],
                        "resonances": []
                    }

                if line.line_type == "alliance":
                    line_edges[edge_key]["alliances"].append(line)
                elif line.line_type == "opposition":
                    line_edges[edge_key]["oppositions"].append(line)
                else:
                    line_edges[edge_key]["resonances"].append(line)

    # Add combined edges
    for (p1, p2), lines_data in line_edges.items():
        all_lines = lines_data["alliances"] + lines_data["oppositions"] + lines_data["resonances"]

        # Determine overall edge color
        if lines_data["oppositions"] and not lines_data["alliances"]:
            color = RELATION_COLORS["opposition"]
            edge_type = "opposition"
        elif lines_data["alliances"] and not lines_data["oppositions"]:
            color = RELATION_COLORS["alliance"]
            edge_type = "alliance"
        elif lines_data["oppositions"] and lines_data["alliances"]:
            color = "#FF9800"  # Orange for mixed
            edge_type = "mixed"
        else:
            color = RELATION_COLORS["resonance"]
            edge_type = "resonance"

        # Build tooltip
        tooltip_lines = [f"<b>{p1}</b> ↔ <b>{p2}</b><br><br>"]
        for line in all_lines:
            emoji = "🤝" if line.line_type == "alliance" else ("⚡" if line.line_type == "opposition" else "🔄")
            tooltip_lines.append(f"{emoji} {line.dimension}: {line.description}<br>")

        width = 2 + len(all_lines) * 1.5

        net.add_edge(
            p1, p2,
            width=width,
            color=color,
            title="".join(tooltip_lines),
            smooth={"type": "curvedCW", "roundness": 0.2} if edge_type == "mixed" else False
        )

    # Add emerged assemblage if present
    if result.emerged_assemblage:
        emerged = result.emerged_assemblage

        tooltip = f"""<b>{emerged.name}</b> (EMERGED)<br>
<i>{emerged.abstract_machine}</i><br><br>
<b>Type:</b> {fertility.emergence_type if fertility else 'unknown'}<br>
<b>Fertility Score:</b> {fertility.fertility_score:.3f if fertility else 'N/A'}<br><br>
<b>Territories:</b> {', '.join(t.name for t in emerged.territories)}<br>
<b>Codes:</b> {', '.join(c.name for c in emerged.codes)}<br>
<b>Components:</b> {', '.join(c.name for c in emerged.components)}<br>
<b>Becomings:</b> {', '.join(emerged.becoming_vectors)}
"""

        # Add emerged node (star shape, gold color)
        net.add_node(
            emerged.name,
            label=emerged.name.replace("-Assemblage", ""),
            title=tooltip,
            color="#FFD700",  # Gold
            size=50,
            shape="star",
            borderWidth=4,
            borderWidthSelected=6
        )

        # Connect emerged to all parents
        for asm in cluster.assemblages:
            net.add_edge(
                asm.name,
                emerged.name,
                color="#FFD700",
                width=3,
                dashes=[5, 5],
                arrows={"to": {"enabled": True, "scaleFactor": 0.5}},
                title=f"Contributed to emergence"
            )

    # Add legend as hidden nodes (positioned manually)
    legend_y = -300
    legend_items = [
        ("🟢 Smooth Space", SPACE_TYPE_COLORS["smooth"]),
        ("🔵 Striated Space", SPACE_TYPE_COLORS["striated"]),
        ("🟣 Mixed Space", SPACE_TYPE_COLORS["mixed"]),
        ("—— Alliance", RELATION_COLORS["alliance"]),
        ("—— Opposition", RELATION_COLORS["opposition"]),
    ]

    return net


# =============================================================================
# EXPORT FUNCTIONS
# =============================================================================

def visualize_proximity(
    matrix: ProximityMatrix,
    assemblages: List[Assemblage],
    output_path: Path,
    threshold: float = 0.3
) -> Path:
    """Generate and save proximity network visualization."""
    net = build_proximity_network(matrix, assemblages, threshold)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    net.save_graph(str(output_path))
    return output_path


def visualize_clusters(
    clustering: ClusteringResult,
    output_path: Path
) -> Path:
    """Generate and save cluster visualization."""
    net = build_cluster_network(clustering)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    net.save_graph(str(output_path))
    return output_path


def visualize_incubation(
    result: IncubationResult,
    output_path: Path
) -> Path:
    """Generate and save incubation visualization."""
    net = build_incubation_network(result)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    net.save_graph(str(output_path))
    return output_path


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    from pathlib import Path
    from carry.engine.interaction import load_assemblages
    from carry.incubator.proximity import build_proximity_matrix
    from carry.incubator.cluster import cluster_by_proximity
    from carry.incubator.incubation import incubate

    carry_root = Path(__file__).parent.parent
    subjects_path = carry_root / "assemblages" / "subjects" / "hari.yaml"
    output_dir = carry_root / "incubator" / "viz"

    print("Loading assemblages...")
    subjects = load_assemblages(subjects_path)

    print("Building proximity matrix...")
    matrix = build_proximity_matrix(subjects, use_llm_semantics=False)

    print("Generating proximity network...")
    viz_path = visualize_proximity(matrix, subjects, output_dir / "proximity.html")
    print(f"  Saved to {viz_path}")

    print("Clustering...")
    clustering = cluster_by_proximity(subjects, matrix, threshold=0.5)

    print("Generating cluster network...")
    viz_path = visualize_clusters(clustering, output_dir / "clusters.html")
    print(f"  Saved to {viz_path}")

    if clustering.clusters:
        print("Incubating first cluster...")
        result = incubate(clustering.clusters[0], matrix, generate_emergence=False)

        print("Generating incubation network...")
        viz_path = visualize_incubation(result, output_dir / "incubation.html")
        print(f"  Saved to {viz_path}")

    print("\nDone! Open the HTML files in a browser.")
