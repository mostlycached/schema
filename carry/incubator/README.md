# Incubator

Assemblage proximity, clustering, and emergence engine.

Brings assemblages into proximity based on multi-dimensional similarity, analyzes collective dynamics (transversal lines, tensions, fertility), and generates new hybrid assemblages from "fertile" incubations.

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
```

## Options

| Flag | Description |
|------|-------------|
| `--subjects` | Path to subject assemblages YAML (required) |
| `--encounters` | Path to encounters directory |
| `--threshold` | Proximity threshold for clustering (0.0-1.0, default: 0.5) |
| `--min-cluster-size` | Minimum assemblages per cluster (default: 2) |
| `--mode` | `cluster`, `incubate`, or `full` (default: full) |
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

## Visualizations

When `--viz` is enabled, generates interactive HTML network graphs:

| File | Description |
|------|-------------|
| `proximity.html` | All assemblages with edges colored by alliance/tension |
| `clusters.html` | Cluster membership with diamond centroids |
| `incubation_N.html` | Per-cluster dynamics with emerged assemblage as gold star |

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
