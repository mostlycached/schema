# Conatus Agent Simulation

> Simulated environment for exploring the Dynamic Stance-Component Architecture from [THESIS.md](../THESIS.md)

---

## Overview

This package instantiates the agent architecture described in `THESIS.md`:

- **Two modes**: Adoption (refine) vs Novelty Search (generate)
- **Critic evaluation** through 11 theoretical lenses
- **Per-encounter component retrieval** from vector store
- **Configurable force_novelty** for maximum stance diversity

## Package Structure

```
conatus/simulation/
├── agent.py           # ConatusAgent, Stance, FunctionalComponent
├── environment.py     # Environment, encounter generation
├── simulation.py      # Unified loop orchestrator
├── critic.py          # Critic with theoretical modes
├── diversity.py       # MAP-Elites + semantic distance
├── component_store.py # Qdrant vector store
├── experiments.py     # CLI interface
├── visualization.py   # Console, Mermaid, matplotlib
└── results/           # Experiment outputs
```

## Quick Start

```python
from conatus.simulation import (
    ConatusAgent, Simulation, EnvironmentConfig, 
    CriticConfig, generate_report
)
from conatus.simulation.agent import FunctionalComponent, Stance

# Create agent
components = [
    FunctionalComponent("focus", "Concentrated attention", "cognitive"),
    FunctionalComponent("breath", "Breathing regulation", "motor"),
]

agent = ConatusAgent(
    name="Practitioner",
    context="Training",
    functional_components=components,
    initial_stance=Stance(
        name="Ready",
        description="Alert and prepared",
        core_components=["focus"],
        active_weights={"focus": 1.0},
        affect_register="sharp presence"
    ),
)

# Run simulation
sim = Simulation(
    agent=agent,
    env_config=EnvironmentConfig.for_context("forge"),
    critic_config=CriticConfig(mode="nietzschean"),
    force_novelty=True,  # Always generate new stances
    use_vector_store=True,  # Per-encounter component retrieval
)

records = sim.run([
    "Heavy deadlift. Grip failing.",
    "Coach criticizes your form.",
])

# Generate report
generate_report(sim, "Test Run", "Description", "results/test.md")
```

## Critic Modes

| Mode | Evaluation Question |
|------|---------------------|
| `materialist` | Does this solve the physical problem? |
| `nietzschean` | Is this GROWTH or decline? |
| `pragmatist` | What can this ACCOMPLISH? |
| `psychoanalytic` | What is AVOIDED or REPRESSED? |
| `marxist` | Who BENEFITS? |
| `barthes` | PLEASURE or BLISS? Where is jouissance? |
| `ranciere` | Distribution of sensible or DISSENSUS? |
| `deleuze` | BECOMING or fixed identity? Lines of flight? |
| `sloterdijk` | What ANTHROPOTECHNIQUE? Practice-of-self? |
| `blumenberg` | What absolute METAPHOR structures the stance? |
| `heidegger` | AUTHENTIC or fallen into das Man? |

## THESIS Modes

From [THESIS.md](../THESIS.md):

1. **Adoption Mode** (viability ≥ threshold): Refine current stance
2. **Novelty Search Mode** (viability < threshold): Generate new stance

Control via `force_novelty` parameter:
- `False`: Use viability-based mode switching (THESIS behavior)
- `True`: Always generate new stances (maximum diversity)

## Component Vector Store

Initialize with 230+ cross-domain components:

```bash
python3 conatus/simulation/component_store.py --expand
```

Enable per-encounter retrieval:

```python
sim = Simulation(
    agent=agent,
    use_vector_store=True,
    component_count=30,
)
```

> **TODO**: Replace centroid sampling with DPP for stochastic diversity.

## Related Files

- [../THESIS.md](../THESIS.md) - The theoretical foundation
- [../../qualia/CASTLE_ROOMS_IIT_ANALYSIS.md](../../qualia/CASTLE_ROOMS_IIT_ANALYSIS.md) - IIT analysis contexts
