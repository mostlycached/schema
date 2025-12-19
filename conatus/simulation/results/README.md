# Experiment Results

> Published findings from Conatus Agent Simulation experiments

---

## Overview

This directory contains two types of results:

1. **Standard Experiments** - Quick simulations showing stance transitions (22 experiments)
2. **Deep Analyses** - Rich phenomenological studies with detailed failure/novelty/experience analysis (5 experiments)

---

## 🔬 Deep Analysis Experiments (Recommended)

These experiments include detailed phenomenological reasoning:

| Context | Experiment | Key Finding |
|---------|------------|-------------|
| **Dance** | [The Fall and Recovery](./dance/deep_analysis_01.md) | Novelty 0.8: "Vertical Dancer" → "Ground Bloom" |
| **Woodworking** | [The Grain Rebels](./woodworking/deep_analysis_01.md) | Tool-material relationship transformation |
| **Child Rearing** | [When Logic Breaks](./child_rearing/deep_analysis_01.md) | Novelty 0.7: "Authoritative" → "Embodied Resonance" |
| **Forge** | [Beyond Capacity](./forge/deep_analysis_01.md) | Controlled effort to surrender |
| **Arena** | [Public Failure](./arena/deep_analysis_01.md) | Prepared performance to authentic emergence |

Each deep analysis includes:
- **Part I: The Failure** - Why prior functional components failed  
- **Part II: The Emergence** - Novelty spectrum analysis (similarity vs. alien)
- **Part III: Phenomenology** - Bodily sensation, temporal experience, world-relation shifts

---

## Standard Experiments

### THESIS.md Examples

| Context | Experiment | Description |
|---------|------------|-------------|
| **Dance** | [Balance Crisis](./dance/experiment_01_balance_crisis.md) | Stance transition when vertical balance is lost |
| | [Tempo Pressure](./dance/experiment_02_tempo_pressure.md) | Adaptation under increasing speed demands |
| **Woodworking** | [Wild Grain](./woodworking/experiment_01_wild_grain.md) | Technique adaptation when material resists |
| | [Knot Encounter](./woodworking/experiment_02_knot_encounter.md) | Stance shifts from unexpected defects |
| **Child Rearing** | [Tantrum Escalation](./child_rearing/experiment_01_tantrum.md) | Transition to co-regulating stance |
| | [Bedtime Resistance](./child_rearing/experiment_02_bedtime.md) | Adaptation during persistent resistance |

---

### Castle Rooms Contexts

| Context | Room | Experiment | Description |
|---------|------|------------|-------------|
| **Forge** | 026 | [Max Effort](./forge/experiment_01_max_effort.md) | Near-maximal physical load |
| | | [Form Breakdown](./forge/experiment_02_form_breakdown.md) | Recovery from technique failure |
| **Dojo** | 034 | [Plateau](./dojo/experiment_01_plateau.md) | Adaptation when progress stalls |
| | | [Speed Pressure](./dojo/experiment_02_speed_pressure.md) | Skill under tempo demands |
| **Arena** | 029 | [Hostile Audience](./arena/experiment_01_hostile_audience.md) | Performance under criticism |
| | | [Public Mistake](./arena/experiment_02_public_mistake.md) | Recovery from major error |
| **Campfire** | 051 | [Deep Vulnerability](./campfire/experiment_01_deep_vulnerability.md) | Response to intimate sharing |
| | | [Conflict Emergence](./campfire/experiment_02_conflict.md) | Stance when disagreement surfaces |
| **War Room** | 035 | [Cascade Failure](./war_room/experiment_01_cascade.md) | Compounding system failures |
| | | [Resource Depletion](./war_room/experiment_02_resource_depletion.md) | Adaptation when resources run out |
| **Wilderness** | 041 | [Lost](./wilderness/experiment_01_lost.md) | Complete loss of orientation |
| | | [Storm Approach](./wilderness/experiment_02_storm.md) | Weather threat adaptation |
| **Improv Stage** | 042 | [Block Recovery](./improv_stage/experiment_01_block.md) | Partner blocks offers |
| | | [Creative Freeze](./improv_stage/experiment_02_freeze.md) | Inspiration drought |
| **Void** | 063+ | [Anxiety Rise](./void/experiment_01_anxiety.md) | Existential anxiety emergence |
| | | [Ego Dissolution](./void/experiment_02_dissolution.md) | Edge of self-dissolution |

---

## Key Patterns Observed

### 1. Viability Decline Curve
Most experiments show a characteristic viability decline as encounters escalate, triggering Novelty Search when threshold is crossed.

### 2. LLM-Generated Affect Registers
The Gemini model generates contextually appropriate affect names:
- Dance: "grounded fluidity", "subterranean flow"
- Woodworking: "slicing awareness", "material listening"
- Void: "groundless ground", "dissolved presence"

### 3. Component Reconfiguration
Novelty Search consistently:
1. Inhibits core stance components
2. Activates previously dormant components
3. Synthesizes new coordination pattern

---

## Running Your Own Experiments

```bash
# Run pre-built experiment
python3 -m conatus.simulation.experiments --experiment dance

# Interactive mode
python3 -m conatus.simulation.experiments --experiment void --intervention stance_guide

# Output to file
python3 -m conatus.simulation.experiments --experiment forge --output ./my_results/
```
