# Memoir Scene Schema

## Overview

This document defines the schema for capturing personal life-world scenes. Each scene represents a moment of lived experience analyzed through three simultaneous lenses (following Schutz, Bourdieu, and Luhmann).

The schema enables:
- **Rich qualitative capture** of phenomenological experience
- **Structural analysis** of power, capital, and social positioning
- **Systemic mapping** of functional roles and boundaries
- **Graph representation** for exploring relationships between scenes

## Scene Definition

A **Scene** is a discrete unit of lived experience with clear boundaries (temporal, spatial, or thematic).

### Core Metadata

```yaml
scene_id: string              # Unique identifier (UUID)
title: string                 # Short descriptive name
date: ISO-8601 date           # When the scene occurred
location: string              # Where (can be physical or virtual)
duration: string              # How long (e.g., "2 hours", "ongoing", "moment")
tags: [string]                # Freeform tags for categorization
```

### Phenomenological Lens (Schutz)

Captures the subjective experience and cognitive style.

```yaml
phenomenology:
  cognitive_style:            # How time, space, and causality are experienced
    time_experience: string   # e.g., "stretched", "compressed", "cyclical", "fragmented"
    space_experience: string  # e.g., "confined", "open", "virtual", "liminal"
    attention_mode: string    # e.g., "hypervigilant", "flow", "dissociated", "scanning"
  
  intersubjectivity:          # Shared meanings and emotional resonance
    shared_meanings: [string] # What is collectively understood without words
    emotional_tone: string    # Dominant affect (e.g., "anxiety", "joy", "boredom")
    intimacy_level: string    # e.g., "parasocial", "anonymous", "familial", "romantic"
  
  body_experience:            # Somatic/embodied aspects
    sensations: [string]      # Physical sensations (e.g., "cold", "pressure", "pain")
    posture: string           # Body position/orientation
    mobility: string          # Degree of movement freedom
```

### Structural Lens (Bourdieu)

Captures power dynamics, capital, and social positioning.

```yaml
structure:
  capital:                    # What is valued and exchanged
    economic: string          # Money, resources
    cultural: string          # Knowledge, taste, credentials
    social: string            # Networks, connections
    symbolic: string          # Prestige, reputation, status
  
  doxa:                       # Unspoken rules and beliefs
    beliefs: [string]         # What goes without saying
    taboos: [string]          # What cannot be said or done
  
  habitus:                    # Internalized dispositions and behaviors
    behaviors: [string]       # Automatic actions, habits
    gestures: [string]        # Bodily hexis, mannerisms
    language_style: string    # How one speaks (register, code-switching)
  
  hierarchy:                  # Power relations
    position: string          # Where you stand (e.g., "subordinate", "peer", "authority")
    mobility: string          # Ability to change position
```

### Systemic Lens (Luhmann)

Captures the functional role and communicative boundaries.

```yaml
system:
  function:                   # What purpose does this scene serve?
    primary: string           # Main function (e.g., "education", "labor", "intimacy")
    secondary: [string]       # Additional functions
  
  binary_code:                # The core operational distinction
    code: string              # e.g., "legal/illegal", "profit/loss", "sacred/profane"
    position: string          # Which side you're on
  
  boundaries:                 # What defines inclusion/exclusion
    entry_criteria: [string]  # How to get in
    exit_criteria: [string]   # How to leave or be expelled
  
  communication:              # How meaning circulates
    medium: string            # e.g., "money", "power", "truth", "love"
    code_switching: [string]  # When/how codes shift
```

### Inhabitants and Actors

```yaml
inhabitants:
  - role: string              # e.g., "boss", "stranger", "friend", "algorithm"
    name: string              # Optional identifier
    relationship: string      # To the observer
    power: string             # Relative power position
```

### Genealogy and Tension

```yaml
genealogy:
  origin: string              # Historical/social root of this scene type
  influences: [string]        # What shaped this world
  
tension:
  internal: string            # Conflicts within the scene
  external: string            # Pressures from outside
  trajectory: string          # "growth", "decay", "mutation", "stagnation"
```

### Narrative and Reflection

```yaml
narrative:
  description: string         # Free-form narrative description
  key_moments: [string]       # Significant events within the scene
  turning_points: [string]    # Moments of change or realization

reflection:
  significance: string        # Why this scene matters
  patterns: [string]          # Recurring themes or structures
  questions: [string]         # Open questions or tensions
```

---

## Graph Schema

The memoir is represented as a directed graph where:
- **Nodes** = Scenes (+ optionally: Worlds, Actors)
- **Edges** = Relationships between scenes

### Node Types

#### Scene Node
```yaml
node_type: "scene"
scene_id: string
data: Scene                   # Full scene object as defined above
```

#### World Node (Optional)
```yaml
node_type: "world"
world_id: string
world_name: string            # Reference to WORLDS.md
world_type: string            # "novel" or "long-lasting"
```

#### Actor Node (Optional)
```yaml
node_type: "actor"
actor_id: string
name: string
roles: [string]               # Roles played across scenes
```

### Edge Types

#### Temporal Edge
Connects scenes in chronological sequence.
```yaml
edge_type: "temporal"
source: scene_id
target: scene_id
direction: "before" | "after" | "concurrent"
```

#### Causal Edge
One scene leads to or causes another.
```yaml
edge_type: "causal"
source: scene_id
target: scene_id
causality: string             # Description of causal relationship
```

#### Similarity Edge
Scenes share structural or phenomenological similarities.
```yaml
edge_type: "similar"
source: scene_id
target: scene_id
similarity_type: string       # "phenomenological", "structural", "systemic"
similarity_score: float       # 0.0 to 1.0
```

#### Intersection Edge
Scene belongs to multiple overlapping worlds.
```yaml
edge_type: "intersection"
source: scene_id
target: world_id
intersection_type: string     # How the world manifests in the scene
```

#### Opposition Edge
Scenes represent dialectical opposites.
```yaml
edge_type: "opposition"
source: scene_id
target: scene_id
opposition_type: string       # e.g., "thesis/antithesis", "before/after transformation"
```

---

## File Format

Scenes are stored as individual YAML files in the memoir repository:

```
memoir/
├── scenes/
│   ├── 2024-01-15_morning_commute.yaml
│   ├── 2024-01-20_team_meeting.yaml
│   └── ...
├── graphs/
│   └── main_graph.json
└── index.yaml                 # Metadata about all scenes
```

### Example Scene File

```yaml
scene_id: "a3f2b8c1-9d4e-4a1b-8c2f-7e3d5f6a9b0c"
title: "Morning Subway Commute"
date: "2024-01-15"
location: "NYC Subway, 4/5 train"
duration: "45 minutes"
tags: ["commute", "transit", "daily", "solitude"]

phenomenology:
  cognitive_style:
    time_experience: "suspended animation between destinations"
    space_experience: "compressed metal tube; bodies pressed together yet isolated"
    attention_mode: "scanning for threats, zoning out, phone-scrolling"
  intersubjectivity:
    shared_meanings: ["don't make eye contact", "move to the center of the car"]
    emotional_tone: "low-grade anxiety mixed with resignation"
    intimacy_level: "anonymous proximity"
  body_experience:
    sensations: ["swaying with the train", "pressure of other bodies", "stale air"]
    posture: "standing, one hand on pole, other holding phone"
    mobility: "constrained by crowd density"

structure:
  capital:
    economic: "MetroCard balance, time as currency"
    cultural: "knowing which car doors align with exits"
    social: "none, radical atomization"
    symbolic: "those with seats vs. those standing"
  doxa:
    beliefs: ["this is what adults do", "the train will come eventually"]
    taboos: ["talking loudly", "taking up too much space", "aggressive eye contact"]
  habitus:
    behaviors: ["automatic swiping", "podcast listening", "vacant stare"]
    gestures: ["defensive posture", "phone as shield"]
    language_style: "silence, headphones as barrier"
  hierarchy:
    position: "anonymous unit in the mass"
    mobility: "trapped until the next stop"

system:
  function:
    primary: "logistics/mobility"
    secondary: ["time compression", "enforced waiting"]
  binary_code:
    code: "on-time/delayed"
    position: "subject to the system's timing"
  boundaries:
    entry_criteria: ["MetroCard", "willingness to endure"]
    exit_criteria: ["reaching your stop", "giving up and leaving"]
  communication:
    medium: "announcements, digital signs, body language"
    code_switching: ["switching from work-mode to commute-mode to prep for arrival"]

inhabitants:
  - role: "fellow commuters"
    relationship: "anonymous strangers"
    power: "equal in powerlessness"
  - role: "train conductor"
    relationship: "distant authority"
    power: "controls movement"
  - role: "the train itself"
    relationship: "non-human agent"
    power: "determines experience"

genealogy:
  origin: "NYC subway system (1904), evolved into current overcrowded reality"
  influences: ["car-centric city planning failure", "real estate pushing workers to outer boroughs"]

tension:
  internal: "desire for solitude vs. forced proximity"
  external: "rising fares, aging infrastructure, increasing delays"
  trajectory: "decay"

narrative:
  description: |
    Another morning, another swipe. The platform is packed. When the train arrives,
    there's a collective surge. I wedge myself in, phone out, podcast on. 45 minutes
    of swaying, scanning faces, trying not to meet anyone's eyes. The train lurches.
    Someone's coffee spills. Nobody says anything. At my stop, I flow out with the
    crowd, up the stairs, into the daylight.
  key_moments:
    - "The moment of deciding whether to push onto this train or wait for the next"
    - "The doors closing on someone still trying to get in"
    - "Emerging from underground into the street"
  turning_points: []

reflection:
  significance: "Exemplifies the NYC commuter world—atomization, resignation, urban precarity"
  patterns: ["repeated daily", "mirrors other transit systems globally"]
  questions: ["How long can I sustain this?", "What would it take to escape this pattern?"]
```

---

## Integration with WORLDS.md

Scenes can be **mapped** to one or more worlds defined in `WORLDS.md`. This creates intersection edges:

- Scene: "Morning Subway Commute" → World: "The Algorithmic Gig Economy" (if you're an Uber driver)
- Scene: "Morning Subway Commute" → World: "The NYC Subway Commuter" (hypothetical world)

The interrogator module can suggest relevant worlds based on scene characteristics.

---

## Privacy and Storage

- **Public repo (schema/)**: Contains this schema definition, interrogator code, graph utilities
- **Private repo (memoir/)**: Contains actual scene YAML files, personal data, graphs
- **Never commit personal scenes to the public repo**
