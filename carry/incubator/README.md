# Incubator

Assemblage proximity, clustering, emergence, and **accessibility** engine.

Brings assemblages into proximity based on multi-dimensional similarity, analyzes collective dynamics (transversal lines, tensions, fertility), generates new hybrid assemblages from "fertile" incubations, and computes **accessibility paths** - how assemblages perceive and leverage each other from their own positions.

## Usage

```bash
# Cluster assemblages
python -m carry.incubator \
  --subjects carry/assemblages/subjects/hari.yaml \
  --threshold 0.5 \
  --mode cluster

# Analyze without emergence
python -m carry.incubator \
  --subjects carry/assemblages/subjects/hari.yaml \
  --mode incubate

# Full with emergence generation
python -m carry.incubator \
  --subjects carry/assemblages/subjects/hari.yaml \
  --mode full

# With encounters
python -m carry.incubator \
  --subjects carry/assemblages/subjects/hari.yaml \
  --encounters carry/assemblages/encounters \
  --mode full

# Save output with visualizations
python -m carry.incubator \
  --subjects carry/assemblages/subjects/hari.yaml \
  --mode full \
  --output carry/incubator/results \
  --viz

# Compute accessibility paths (how assemblages perceive each other)
python -m carry.incubator \
  --subjects carry/assemblages/subjects/hari.yaml \
  --mode accessibility \
  --output carry/incubator/results \
  --viz
```

## Options

| Flag | Description |
|------|-------------|
| `--subjects` | Path to subject assemblages YAML (required) |
| `--encounters` | Path to encounters directory |
| `--threshold` | Proximity threshold for clustering (0.0-1.0, default: 0.5) |
| `--min-cluster-size` | Minimum assemblages per cluster (default: 2) |
| `--mode` | `cluster`, `incubate`, `full`, or `accessibility` (default: full) |
| `--cluster-id` | Only incubate a specific cluster |
| `--output` | Output directory for reports |
| `--format` | `markdown` or `json` (default: markdown) |
| `--viz` | Generate interactive HTML network visualizations |
| `--no-llm` | Disable LLM for semantic proximity |

## Module Structure

```
carry/incubator/
├── __init__.py       # Exports + CLI
├── __main__.py       # Module runner
├── proximity.py      # Multi-dimensional proximity
├── cluster.py        # Hierarchical clustering
├── incubation.py     # Transversal lines, tensions, fertility
├── emergence.py      # New assemblage generation
├── accessibility.py  # Perception paths between assemblages
├── report.py         # Markdown/JSON reports
└── viz.py            # pyvis network visualizations
```

## Proximity Computation

Multi-dimensional proximity between assemblages:

| Dimension | Weight | Method |
|-----------|--------|--------|
| Intensity field | 0.35 | Euclidean distance in 6D (focus, patience, abstraction, speed, tactility, social) |
| Space type | 0.20 | Smooth/striated compatibility |
| Semantic | 0.25 | LLM-computed component capacity similarity |
| Becoming overlap | 0.20 | Jaccard similarity + semantic boost |

## Clustering

Hierarchical agglomerative clustering with average linkage:
1. Convert proximity to distance (1 - proximity)
2. Build linkage matrix
3. Cut at threshold
4. Filter by minimum cluster size
5. Compute cluster characteristics (cohesion, diversity, tension potential)

## Incubation Analysis

For each cluster:

**Transversal Lines** - Alliances/oppositions spanning multiple assemblages:
- Intensity alliances (3+ assemblages with similar values)
- Becoming resonances (shared becoming vectors)
- Space type alliances (smooth vs striated blocs)

**Collective Tensions** - LLM-enhanced analysis of:
- Intensity clashes (>0.5 spread on a dimension)
- Space incompatibility (mixed smooth/striated)
- Code conflicts (molar vs molecular)

**Actualization Potentials** - Virtual capacities that could be triggered by other assemblages in the cluster

## Fertility Assessment

Goldilocks zone for emergence:

| Factor | Threshold | Meaning |
|--------|-----------|---------|
| Creative tension | 0.25-0.75 | Too low = stasis, too high = destruction |
| Resonance foundation | > 0.35 | Enough alliance to build on |
| Virtual triggers | >= 1 | Something unactualized can become actual |

**Emergence Types:**
- `synthesis` - Cohesive cluster merges into coherent new form
- `mutation` - One assemblage radically transforms under pressure
- `transcendence` - Diverse cluster produces genuinely novel abstract machine
- `hybrid` - Component mixing without deep synthesis

## Accessibility Paths

**The Problem:** Proximity tells us HOW CLOSE assemblages are. But how does one assemblage **perceive** another from its own position? Previously, only "meta-assemblages" (Philosophy, Writing, Witnessing) could reflect on other assemblages. A Knife couldn't "see" what a Cello offers.

**The Solution:** Accessibility paths are asymmetric perception channels. How Knife sees Cello differs from how Cello sees Knife. Each assemblage has a "lens" defined by its capacities.

### Access Modes

| Mode | Description | Example |
|------|-------------|---------|
| `capacity_lens` | My capacities define what I can perceive in others | Knife's Precision-Cutter sees Cello's Bow-Arm's "weight" |
| `becoming_channel` | Shared becoming vectors create direct access | Both share "becoming-patient" → mutual channel |
| `intensity_resonance` | High values on same dimension create visibility | Both high on "tactility" → can see each other's tactile capacities |
| `territory_analogy` | Similar territory functions create mapping paths | "Daily return to board" ≈ "Daily return to instrument" |
| `code_translation` | How my codes can interpret other codes | Knife's "Edge-Maintenance" can interpret Cello's "Slow-Passage-Work" |

### Key Insight

Accessibility is NOT symmetric like proximity:
- Knife → Cello: Sees weight, control, precision in bow work
- Cello → Knife: Sees rhythm, gesture, sustained attention in cutting

Each assemblage has a **lens** (extracted from its components) that determines what aspects of other assemblages it can perceive and leverage.

### Programmatic Usage

```python
from carry.incubator import (
    build_accessibility_matrix,
    generate_accessibility_report,
    generate_path_narrative,
    visualize_accessibility,
)
from carry.engine.interaction import load_assemblages

# Load
subjects = load_assemblages("carry/assemblages/subjects/hari.yaml")

# Build accessibility matrix
matrix = build_accessibility_matrix(subjects)

# Get how Knife sees Cello
knife = next(a for a in subjects if "Knife" in a.name)
cello = next(a for a in subjects if "Cello" in a.name)
paths = matrix.get_paths_between(knife.name, cello.name)

for path in paths:
    print(f"[{path.mode.value}] clarity={path.clarity:.2f}")
    print(f"  {path.description}")

# Get most accessible assemblages from Knife's perspective
most_accessible = matrix.get_most_accessible_from(knife.name, k=5)
for target, clarity in most_accessible:
    print(f"  {target}: {clarity:.2f}")

# Generate narrative (uses LLM)
narrative = generate_path_narrative(knife, cello, paths)
print(narrative)

# Visualize
visualize_accessibility(matrix, subjects, "accessibility.html")
```

## Visualizations

When `--viz` is enabled, generates interactive HTML network graphs:

| File | Description |
|------|-------------|
| `proximity.html` | All assemblages with edges colored by alliance/tension |
| `clusters.html` | Cluster membership with diamond centroids |
| `incubation_N.html` | Per-cluster dynamics with emerged assemblage as gold star |
| `accessibility.html` | Directed perception paths (arrows show how A sees B) |

**Visual encoding:**
- Node color: space type (green=smooth, blue=striated, purple=mixed)
- Node size: number of components
- Edge color: relation (green=alliance, red=opposition, orange=mixed)
- Edge width: proximity score
- Emerged assemblages: gold star shape

**Interaction:**
- Drag nodes to rearrange
- Scroll to zoom
- Hover for detailed tooltips
- Click to select/highlight

## Programmatic Usage

```python
from carry.incubator import (
    build_proximity_matrix,
    cluster_by_proximity,
    incubate,
    generate_incubation_report,
    visualize_proximity,
    visualize_incubation,
)
from carry.engine.interaction import load_assemblages

# Load
subjects = load_assemblages("carry/assemblages/subjects/hari.yaml")

# Proximity
matrix = build_proximity_matrix(subjects)

# Cluster
clustering = cluster_by_proximity(subjects, matrix, threshold=0.5)

# Incubate
for cluster in clustering.clusters:
    result = incubate(cluster, matrix, generate_emergence=True)

    # Report
    report = generate_incubation_report(result)
    print(report)

    # Visualize
    visualize_incubation(result, "incubation.html")

    # Access emerged assemblage
    if result.emerged_assemblage:
        print(result.emerged_assemblage.abstract_machine)
```

## Output Example

```
Cluster 0: Hari-Witnessing + Hari-Calligraphy

Transversal Lines:
  🤝 intensity:focus (0.80) - High focus alliance
  🤝 intensity:patience (0.85) - High patience alliance
  ⚡ intensity:tactility (0.80) - Opposition

Collective Tensions:
  - tactility clash (0.78): Calligraphy (high) vs Witnessing (low)
  - code conflict (0.70): Fragment-Over-Book vs Mistake-Integration

Fertility: ✅ FERTILE (0.64)
  Type: MUTATION

Emerged: Scribal-Divination-Assemblage
  "Marking the unknown, revealing through gesture"
```
