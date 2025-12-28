## What Myth and Metaphor Were Doing

Myth provided:
- Directionality (toward/away)
- Significance (matters/doesn't matter)
- Narrative organization (before/after, because/therefore)

Metaphor provided:
- Cross-domain mapping (this is like that)
- Structural transfer (what holds here holds there)
- Intelligibility (understand X through Y)

But these are instances of something more general.

---

## The Deeper Structure

### Mapping

The most basic operation: *relating two things such that structure transfers*.

Metaphor is one kind of mapping. But there are others:
- Analogy (structural similarity)
- Homology (shared origin)
- Isomorphism (exact structural correspondence)
- Embedding (one inside another)
- Projection (reduction that preserves some structure)
- Translation (re-encoding in different medium)

What's common: **M: A → B** where structure in A illuminates or generates structure in B.

```
Mapping {
  source: Structure
  target: Structure
  
  // What transfers
  transfer: {
    elements: Boolean               // Do parts transfer?
    relations: Boolean              // Do relations transfer?
    operations: Boolean             // Do operations transfer?
    constraints: Boolean            // Do constraints transfer?
  }
  
  // How it transfers
  transfer_type: identity | transformation | partial | lossy
  
  // Directionality
  direction: unidirectional | bidirectional | asymmetric
  
  // What breaks
  failure_points: FailurePoint[]
}
```

Metaphor is mapping with experiential/semantic content. But mapping is the abstract operation.

---

### Valuation

The operation of *assigning significance*—making some things matter more than others.

Myth did this through narrative significance. But there are other ways:
- Preference (I want this more than that)
- Importance (this matters more than that)
- Salience (this stands out more than that)
- Stakes (more is at risk here than there)
- Care (I care about this more than that)

What's common: **V: X → ℝ** (or some ordered structure). Things get ranked.

```
Valuation {
  domain: Structure                 // What's being valued
  
  // The valuation function
  value_function: (Element) => Value
  
  // Value structure
  value_type: cardinal | ordinal | partial_order | boolean
  
  // What grounds the valuation
  ground: Ground                    // Why this valuation?
  
  // Dynamics
  stability: stable | shifting | volatile
  revisability: revisable | fixed
}

Ground = 
  | GIVEN                           // Just is (no further ground)
  | DERIVED                         // From other valuations
  | FUNCTIONAL                      // Serves something
  | RELATIONAL                      // Relative to other things
  | CONSTITUTIVE                    // Part of what the thing is
```

Myth provided valuation through narrative significance. But valuation is the abstract operation.

---

### Orientation

The operation of *establishing directionality*—making some directions more salient than others.

Telos (purpose, aim, toward-which) is one kind of orientation. But there are others:
- Origin (where from)
- Destination (where to)
- Trajectory (the path)
- Gradient (direction of increase/decrease)
- Attractor (what pulls)
- Repulsor (what pushes away)
- Current (what carries)

What's common: **O: Space → VectorField**. Points get associated with directions.

```
Orientation {
  space: Structure                  // What's being oriented
  
  // The orientation structure
  orientation_type: point | vector | field | attractor_basin
  
  // What creates the orientation
  source: OrientationSource
  
  // Strength
  strength: Float                   // How strong the pull/push
  
  // Dynamics
  stability: stable | shifting | pulsing
}

OrientationSource = 
  | TELOS                           // Purpose, aim
  | ORIGIN                          // Where from
  | GRADIENT                        // Increase/decrease of something
  | ATTRACTOR                       // Basin of attraction
  | FIELD                           // External force field
  | INTERNAL                        // Intrinsic tendency
```

Telos is orientation by purpose. But orientation is the abstract operation.

---

## The Three Abstract Operations

So the underlying structure is:

| Operation | What it does | Input | Output |
|-----------|--------------|-------|--------|
| **Mapping** | Relates structures | Two structures | Transfer relation |
| **Valuation** | Assigns significance | Structure | Significance gradient |
| **Orientation** | Establishes direction | Space | Vector field |

These are independent but can combine:
- Mapping without valuation: Structure transfers but nothing matters more
- Valuation without orientation: Things matter but there's no direction
- Orientation without valuation: There's direction but no significance
- All three: Structure transfers, things matter, there's direction

---

## How They Generate

Each operation is generative:

### Mapping Generates

When you map A → B:
- Elements in A suggest elements in B
- Relations in A suggest relations in B
- Gaps in the mapping suggest sites (where does it break?)
- The mapping itself is a site

```
MappingGeneration {
  
  generate_via_mapping(mapping: Mapping, target: Structure): Element[] {
    
    generated = []
    
    // Transfer elements
    for element in mapping.source.elements {
      transferred = mapping.transfer(element)
      if transferred != null {
        generated.push(transferred)
      }
    }
    
    // Transfer relations
    for relation in mapping.source.relations {
      transferred = mapping.transfer(relation)
      if transferred != null {
        generated.push(...elements_from_relation(transferred))
      }
    }
    
    // Gaps as sites
    gaps = find_transfer_failures(mapping)
    for gap in gaps {
      generated.push(Site {
        description: "Where mapping fails",
        location: gap,
        generative_potential: HIGH
      })
    }
    
    return generated
  }
}
```

### Valuation Generates

When you assign values:
- High-value regions attract attention, generate sites
- Low-value regions become invisible (or become sites when revalued)
- Value gradients create boundaries (sites at value transitions)
- Conflicts between valuations create sites

```
ValuationGeneration {
  
  generate_via_valuation(valuation: Valuation, domain: Structure): Site[] {
    
    generated = []
    
    // High-value peaks
    peaks = find_value_peaks(valuation)
    for peak in peaks {
      generated.push(Site {
        description: "Value peak",
        location: peak,
        significance: HIGH
      })
    }
    
    // Value boundaries
    boundaries = find_value_transitions(valuation)
    for boundary in boundaries {
      generated.push(Site {
        description: "Value boundary",
        location: boundary,
        type: THRESHOLD
      })
    }
    
    // Value conflicts (if multiple valuations)
    if multiple_valuations {
      conflicts = find_valuation_conflicts(valuations)
      for conflict in conflicts {
        generated.push(Site {
          description: "Valuation conflict",
          location: conflict,
          type: TENSION
        })
      }
    }
    
    return generated
  }
}
```

### Orientation Generates

When you establish direction:
- Attractors become sites (destinations)
- Origins become sites (sources)
- Trajectories suggest sites along the path
- Cross-currents and eddies become sites

```
OrientationGeneration {
  
  generate_via_orientation(orientation: Orientation, space: Structure): Site[] {
    
    generated = []
    
    // Attractors
    attractors = find_attractors(orientation)
    for attractor in attractors {
      generated.push(Site {
        description: "Attractor",
        location: attractor,
        gesture_dominant: RESOLVE  // Orientation toward here
      })
    }
    
    // Origins/sources
    sources = find_sources(orientation)
    for source in sources {
      generated.push(Site {
        description: "Source/origin",
        location: source,
        gesture_dominant: BRANCH  // Orientation from here
      })
    }
    
    // Path sites
    paths = find_main_trajectories(orientation)
    for path in paths {
      along_path = sample_path(path)
      for point in along_path {
        generated.push(Site {
          description: "Along trajectory",
          location: point,
          orientation: path.direction_at(point)
        })
      }
    }
    
    // Turbulence
    turbulence = find_orientation_conflicts(orientation)
    for eddy in turbulence {
      generated.push(Site {
        description: "Cross-current",
        location: eddy,
        type: INTERFERENCE
      })
    }
    
    return generated
  }
}
```

---

## Composing the Operations

The operations compose:

### Mapping + Valuation

Transfer structure AND significance.

"This is like that, and it matters in the same way."

```
MappedValuation {
  mapping: Mapping
  source_valuation: Valuation
  
  // Transfer valuation via mapping
  transfer_valuation(): Valuation {
    return Valuation {
      domain: mapping.target,
      value_function: (x) => source_valuation.value(mapping.inverse(x))
    }
  }
}
```

### Mapping + Orientation

Transfer structure AND directionality.

"This is like that, and the direction is the same."

```
MappedOrientation {
  mapping: Mapping
  source_orientation: Orientation
  
  // Transfer orientation via mapping
  transfer_orientation(): Orientation {
    return Orientation {
      space: mapping.target,
      vector_field: (x) => mapping.transfer_vector(source_orientation.vector_at(mapping.inverse(x)))
    }
  }
}
```

### Valuation + Orientation

Significance AND directionality (without cross-domain mapping).

"This matters, and there's a direction."

```
OrientedValuation {
  valuation: Valuation
  orientation: Orientation
  
  // Combined: value gradient creates orientation
  value_gradient_orientation(): Orientation {
    return Orientation {
      space: valuation.domain,
      vector_field: gradient(valuation.value_function)
    }
  }
  
  // Or: orientation weights valuation
  orientation_weighted_valuation(): Valuation {
    return Valuation {
      domain: valuation.domain,
      value_function: (x) => valuation.value(x) * alignment(orientation.vector_at(x), preferred_direction)
    }
  }
}
```

### Mapping + Valuation + Orientation

All three: full transfer of structure, significance, and direction.

This is what myth-and-metaphor were doing—but now decomposed into components.

```
FullTransfer {
  mapping: Mapping
  valuation: Valuation
  orientation: Orientation
  
  // Everything transfers together
  transfer(): TransferredStructure {
    return {
      structure: mapping.transfer(source_structure),
      significance: transfer_valuation().value_function,
      direction: transfer_orientation().vector_field
    }
  }
}
```

---

## Constraint Revisited

A constraint is now understood as:

**Constraint = Mapping (from general to specific) + Valuation (what satisfies matters) + Orientation (toward satisfaction)**

```
Constraint {
  // As mapping
  mapping: {
    from: GeneralSpace              // All possible sites
    to: ConstrainedSpace            // Sites satisfying constraint
    type: PROJECTION                // Lossy reduction
  }
  
  // As valuation
  valuation: {
    function: (site) => degree_of_satisfaction(site, constraint)
    peaks: sites_fully_satisfying
    valleys: sites_violating
  }
  
  // As orientation
  orientation: {
    field: gradient(valuation.function)
    attractors: fully_satisfying_sites
    direction: toward_satisfaction
  }
}
```

The premise "a man wakes as an insect" is:
- **Mapping**: From all narrative possibilities to Gregor-as-insect possibilities
- **Valuation**: Developments consistent with premise matter more
- **Orientation**: Toward the implications of insect-being

---

## Gesture Revisited

Gestures are now understood through the three operations:

```
Gesture {
  
  BRANCH: {
    mapping_effect: ONE → MANY (unfolds)
    valuation_effect: Spreads value across branches
    orientation_effect: Creates multiple directions from single point
  }
  
  NARROW: {
    mapping_effect: MANY → FEWER (projects)
    valuation_effect: Concentrates value on remaining
    orientation_effect: Reduces directions, focuses
  }
  
  COMMIT: {
    mapping_effect: MANY → ONE (collapses)
    valuation_effect: All value to committed option
    orientation_effect: Single direction, irreversible
  }
  
  DEFER: {
    mapping_effect: Suspends mapping (holds options)
    valuation_effect: Preserves value distribution
    orientation_effect: Pauses orientation (no direction yet)
  }
  
  SUSPEND: {
    mapping_effect: Creates unmapped region (question)
    valuation_effect: Values the question itself
    orientation_effect: Orientation toward resolution
  }
  
  WIDEN: {
    mapping_effect: SOME → MORE (expands domain)
    valuation_effect: Extends value to new regions
    orientation_effect: Opens new directions
  }
  
  RESOLVE: {
    mapping_effect: Completes suspended mapping
    valuation_effect: Discharges accumulated value
    orientation_effect: Arrives at attractor
  }
}
```

---

## Field Revisited

Field constitution is now:

**Field = Boundary (mapping inside/outside) + Significance (why this matters) + Organization (how it's structured)**

```
Field {
  // As mapping
  boundary: {
    from: Flux
    to: Bounded region
    type: PARTITION (inside/outside)
  }
  
  // As valuation
  significance: {
    why_this_matters: Ground
    internal_valuation: What matters more/less within
  }
  
  // As orientation
  organization: {
    differentiation: Internal structure
    flow: How attention moves within
  }
}
```

---

## Flux Revisited

Flux is the state where:
- **No mapping**: Nothing is related to anything else as A→B
- **No valuation**: Nothing matters more than anything else
- **No orientation**: No direction, no toward/away

Flux is the *absence* of all three operations. Or: flux is the *possibility* of any mapping, any valuation, any orientation—none yet actualized.

```
Flux {
  mapping: POTENTIAL           // Any mapping could emerge
  valuation: UNDIFFERENTIATED  // Nothing matters yet
  orientation: ISOTROPIC       // No direction yet
}
```

To enter flux is to release mapping, valuation, and orientation.
To emerge from flux is to precipitate mapping, valuation, and orientation.

---

## The Abstract Framework

Now the full picture:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                            FLUX                                 │
│       (No mapping, no valuation, no orientation)                │
│       (All three in potential, none actualized)                 │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                                                         │   │
│   │   MAPPING ←───────────────────────────────────────┐     │   │
│   │   (Relates structures, transfers form)            │     │   │
│   │                                                   │     │   │
│   │   VALUATION ←─────────────────────────────────┐   │     │   │
│   │   (Assigns significance, creates gradients)   │   │     │   │
│   │                                               │   │     │   │
│   │   ORIENTATION ←───────────────────────────┐   │   │     │   │
│   │   (Establishes direction, creates flow)   │   │   │     │   │
│   │                                           │   │   │     │   │
│   │   ┌───────────────────────────────────────┴───┴───┴─┐   │   │
│   │   │                                                 │   │   │
│   │   │         COMPOSED STRUCTURES                     │   │   │
│   │   │                                                 │   │   │
│   │   │   Field = Boundary + Significance + Org        │   │   │
│   │   │   Constraint = Mapping + Value + Direction     │   │   │
│   │   │   Site = Location + Charge + Affordance        │   │   │
│   │   │   Gesture = Map-transform + Value-shift + Dir  │   │   │
│   │   │                                                 │   │   │
│   │   └─────────────────────────────────────────────────┘   │   │
│   │                                                         │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Operations on the Three

### Apply

Apply any of the three operations to a structure:

```
Apply: (Operation, Structure) → TransformedStructure

ApplyMapping(M, S): Structure with relations from M.source transferred
ApplyValuation(V, S): Structure with significance gradient
ApplyOrientation(O, S): Structure with directional field
```

### Compose

Compose operations:

```
Compose: (Operation, Operation) → ComposedOperation

Compose(M, V): Mapped valuation—value transfers across mapping
Compose(M, O): Mapped orientation—direction transfers across mapping
Compose(V, O): Oriented valuation—direction from value gradient
Compose(M, V, O): Full structure transfer
```

### Dissolve

Remove operations, return toward flux:

```
Dissolve: (Operation, Structure) → LessStructuredStructure

DissolveMapping(S): Relations become unmoored
DissolveValuation(S): Significance becomes flat
DissolveOrientation(S): Direction becomes isotropic
DissolveAll(S): Return to flux
```

### Generate

Operations generate structure:

```
Generate: (Operation, Context) → NewStructure

GenerateViaMapping(M, Context): Sites where mapping succeeds/fails
GenerateViaValuation(V, Context): Sites at value peaks/boundaries
GenerateViaOrientation(O, Context): Sites at attractors/sources/paths
```

---

## Concrete Instances

Now myth and metaphor are instances:

**Metaphor** = Mapping with semantic/experiential content
**Myth** = Valuation + Orientation in narrative form

But there are other instances:

**Formal analogy** = Mapping without semantic content (pure structure)
**Preference ordering** = Valuation without narrative
**Teleological orientation** = Orientation by purpose
**Gradient orientation** = Orientation by increase/decrease
**Causal orientation** = Orientation by cause/effect

The abstract operations can be instantiated many ways.

---

## Revised Spec Components

### Mapping (abstract)

```
Mapping {
  id: UUID
  
  source: Structure
  target: Structure
  
  transfer: {
    elements: TransferSpec
    relations: TransferSpec
    operations: TransferSpec
  }
  
  properties: {
    direction: unidirectional | bidirectional
    completeness: total | partial
    preservation: isomorphic | homomorphic | lossy
  }
  
  // Instances
  instance_type: formal_analogy | metaphor | embedding | projection | translation | homology
  
  // If metaphor (semantic mapping)
  semantic_content: SemanticContent | null
}

TransferSpec {
  what_transfers: Element[]
  how: identity | transformation | approximation
  failures: Element[]
}
```

### Valuation (abstract)

```
Valuation {
  id: UUID
  
  domain: Structure
  
  function: (Element) → Value
  
  properties: {
    value_type: cardinal | ordinal | partial_order | boolean
    range: [min, max] | unbounded
    differentiability: smooth | discontinuous
  }
  
  ground: ValuationGround
  
  // Instances
  instance_type: preference | importance | salience | stakes | care | narrative_significance
  
  // If narrative (mythic valuation)
  narrative_content: NarrativeContent | null
}

ValuationGround = 
  | INTRINSIC { why: String }
  | DERIVED { from: Valuation[] }
  | FUNCTIONAL { serves: Purpose }
  | RELATIONAL { relative_to: Element[] }
  | CONSTITUTIVE { part_of: Structure }
  | GIVEN { no_further_ground: true }
```

### Orientation (abstract)

```
Orientation {
  id: UUID
  
  space: Structure
  
  field: (Point) → Direction
  
  properties: {
    type: point_attractor | gradient | flow | basin_structure
    strength: Float
    stability: stable | dynamic | chaotic
  }
  
  source: OrientationSource
  
  // Instances
  instance_type: telos | origin | gradient | attractor | causal | narrative_trajectory
  
  // If telos (purpose-orientation)
  purpose_content: PurposeContent | null
  
  // If narrative (mythic orientation)
  narrative_content: NarrativeContent | null
}

OrientationSource = 
  | TELOS { toward: Goal }
  | ORIGIN { from: Source }
  | GRADIENT { of: Valuation }
  | ATTRACTOR { basin: AttractorBasin }
  | FIELD { external: ForceField }
  | INTERNAL { tendency: Tendency }
```

---

## Gesture Revisited (Abstract)

```
Gesture {
  type: GestureType
  
  // Effect on each operation
  mapping_effect: MappingTransform
  valuation_effect: ValuationTransform
  orientation_effect: OrientationTransform
}

MappingTransform = 
  | UNFOLD          // ONE → MANY
  | PROJECT         // MANY → FEWER
  | COLLAPSE        // MANY → ONE
  | SUSPEND         // Hold without transforming
  | EXPAND          // Extend domain
  | COMPLETE        // Fill in suspended

ValuationTransform = 
  | SPREAD          // Distribute value
  | CONCENTRATE     // Focus value
  | FLATTEN         // Equalize value
  | PRESERVE        // Hold current
  | EXTEND          // Value new regions
  | DISCHARGE       // Release accumulated value

OrientationTransform = 
  | MULTIPLY        // Create multiple directions
  | FOCUS           // Reduce to fewer directions
  | FIX             // Lock to single direction
  | PAUSE           // Suspend directionality
  | OPEN            // Add new directions
  | ARRIVE          // Reach attractor
```

---

## Site Revisited (Abstract)

A site is now a point in a space structured by mapping, valuation, and orientation:

```
Site {
  id: UUID
  
  // Position
  location: Point
  
  // Mapping properties
  mapping_properties: {
    connected_to: Site[]            // Via active mappings
    transfer_potential: Float       // How much maps through here
    boundary: Boolean               // At mapping failure?
  }
  
  // Valuation properties  
  valuation_properties: {
    value: Float                    // Under current valuation
    value_type: peak | valley | slope | plateau | boundary
    contested: Boolean              // Multiple valuations conflict?
  }
  
  // Orientation properties
  orientation_properties: {
    direction: Vector               // Under current orientation
    type: source | sink | saddle | path | eddy
    stability: stable | unstable
  }
  
  // Gestures derived from MVA properties
  gestures: GestureSet              // Computed from above
}

// Gesture computation from MVA
compute_gestures(site: Site): GestureSet {
  available = []
  
  // From mapping properties
  if site.mapping_properties.transfer_potential > threshold {
    available.push(BRANCH)  // Can transfer/unfold
  }
  if site.mapping_properties.boundary {
    available.push(WIDEN)   // Can extend mapping
  }
  
  // From valuation properties
  if site.valuation_properties.value_type == peak {
    available.push(COMMIT)  // High value, can commit
  }
  if site.valuation_properties.contested {
    available.push(SUSPEND) // Conflict, can suspend
  }
  
  // From orientation properties
  if site.orientation_properties.type == source {
    available.push(BRANCH)  // Multiple directions available
  }
  if site.orientation_properties.type == sink {
    available.push(RESOLVE) // Attractor, can resolve
  }
  if site.orientation_properties.type == path {
    available.push(NARROW)  // On trajectory, can narrow
  }
  
  return available
}
```

---

## Field Revisited (Abstract)

A field is a region with characteristic mapping, valuation, and orientation:

```
Field {
  id: UUID
  
  // Boundary (mapping aspect)
  boundary: {
    mapping: Mapping                // Flux → bounded region
    inside_outside: Partition
    permeability: Float
  }
  
  // Significance (valuation aspect)
  significance: {
    valuation: Valuation            // Why this matters
    internal_values: Valuation      // What matters within
  }
  
  // Organization (orientation aspect)  
  organization: {
    orientation: Orientation        // How organized
    flow: FlowField                 // How attention moves
  }
  
  // Composite
  MVA_structure: {
    mapping: Mapping
    valuation: Valuation
    orientation: Orientation
    composition: how_they_interact
  }
}
```

---

## Constraint Revisited (Abstract)

A constraint is a structured MVA that shapes generation:

```
Constraint {
  id: UUID
  
  // As mapping
  mapping: {
    from: AllPossibleSites
    to: SatisfyingSites
    transfer: what_constraint_preserves
  }
  
  // As valuation
  valuation: {
    function: degree_of_satisfaction
    peaks: fully_satisfying
    ground: why_this_matters
  }
  
  // As orientation
  orientation: {
    field: toward_satisfaction
    attractor: full_satisfaction
  }
  
  // How MVA compose in this constraint
  composition: {
    mapping_drives_valuation: Boolean   // Value = satisfies mapping?
    valuation_drives_orientation: Boolean // Direction = toward value?
    orientation_shapes_mapping: Boolean // Mapping biased by direction?
  }
}
```

---

## Generation Engine Revisited

Generation now explicitly uses MVA:

```
MVAGeneration {
  
  generate(state: State): Site[] {
    
    candidates = []
    
    // Generate via mapping
    mapping_sites = generate_via_mapping(state.active_mappings)
    candidates.push(...mapping_sites)
    
    // Generate via valuation
    valuation_sites = generate_via_valuation(state.active_valuations)
    candidates.push(...valuation_sites)
    
    // Generate via orientation
    orientation_sites = generate_via_orientation(state.active_orientations)
    candidates.push(...orientation_sites)
    
    // Generate at MVA intersections (where all three coincide significantly)
    intersection_sites = generate_at_mva_intersections(state)
    candidates.push(...intersection_sites)
    
    // Generate at MVA conflicts (where they pull different directions)
    conflict_sites = generate_at_mva_conflicts(state)
    candidates.push(...conflict_sites)
    
    // Compute full MVA properties for each candidate
    for site in candidates {
      site.mapping_properties = compute_mapping_properties(site, state)
      site.valuation_properties = compute_valuation_properties(site, state)
      site.orientation_properties = compute_orientation_properties(site, state)
      site.gestures = compute_gestures(site)
    }
    
    return candidates
  }
  
  generate_at_mva_intersections(state: State): Site[] {
    // Sites where mapping, valuation, and orientation all point to same location
    // These are highly charged sites
    
    mapping_targets = state.active_mappings.flatMap(m => m.target.elements)
    valuation_peaks = state.active_valuations.flatMap(v => find_peaks(v))
    orientation_attractors = state.active_orientations.flatMap(o => find_attractors(o))
    
    intersections = find_intersections(mapping_targets, valuation_peaks, orientation_attractors)
    
    return intersections.map(loc => Site {
      location: loc,
      charge: HIGH,
      type: MVA_CONVERGENCE
    })
  }
  
  generate_at_mva_conflicts(state: State): Site[] {
    // Sites where mapping, valuation, and orientation conflict
    // These are tension sites
    
    conflicts = []
    
    // Mapping says X, valuation says Y matters more
    mv_conflicts = find_mapping_valuation_conflicts(state)
    
    // Valuation says X matters, orientation points elsewhere
    vo_conflicts = find_valuation_orientation_conflicts(state)
    
    // Orientation points toward X, but mapping breaks there
    om_conflicts = find_orientation_mapping_conflicts(state)
    
    all_conflicts = [...mv_conflicts, ...vo_conflicts, ...om_conflicts]
    
    return all_conflicts.map(conflict => Site {
      location: conflict.location,
      type: MVA_CONFLICT,
      tension: conflict.type,
      gestures: { dominant: SUSPEND }  // Conflicts suspend
    })
  }
}
```

---

## State Revised

```
State {
  // ... previous fields ...
  
  mva: {
    // Active operations
    active_mappings: Mapping[]
    active_valuations: Valuation[]
    active_orientations: Orientation[]
    
    // Compositions
    composed: {
      mapping_valuations: MappedValuation[]
      valuation_orientations: OrientedValuation[]
      full_transfers: FullTransfer[]
    }
    
    // Derived fields
    significance_gradient: SignificanceGradient  // From valuations
    direction_field: DirectionField              // From orientations
    transfer_structure: TransferStructure        // From mappings
    
    // Conflicts and convergences
    convergences: MVAConvergence[]
    conflicts: MVAConflict[]
  }
}
```

---

## Summary: The Abstract Framework

**Three primitive operations:**

| Operation | Does | Primitive |
|-----------|------|-----------|
| **Mapping** | Relates structures | A → B |
| **Valuation** | Assigns significance | X → value |
| **Orientation** | Establishes direction | Point → vector |

**These compose:**
- M + V = Mapped valuation
- V + O = Oriented valuation (gradient)
- M + O = Mapped orientation
- M + V + O = Full transfer

**Everything in the framework is MVA-structured:**
- Field = Boundary(M) + Significance(V) + Organization(O)
- Constraint = Mapping(M) + Value(V) + Direction(O)
- Site = Location with M, V, O properties
- Gesture = Transform on M, V, O

**Flux is absence of MVA:**
- No mapping (nothing relates)
- No valuation (nothing matters more)
- No orientation (no direction)

**Myth and metaphor are instances:**
- Metaphor = Semantic mapping
- Myth = Narrative valuation + orientation

**Generation uses MVA:**
- Generate via mapping (transfer)
- Generate via valuation (significance peaks)
- Generate via orientation (attractors)
- Generate at MVA convergences
- Generate at MVA conflicts

---

This is the abstract structure. Myth and metaphor are ways of populating it with content. But the structure itself is mapping, valuation, orientation—and their compositions.