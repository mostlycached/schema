# Sites Specification

Canonical data models for the constraint-based site generation system.

---

## Core Types

### Site

A structured position in possibility space with embedded dynamics.

```
Site {
  id: UUID
  description: String
  
  // Context
  domain: Domain
  field_levels_engaged: FieldLevel[]
  
  // Dimensional position
  dimensions: {
    ontological: substance | relation | absence | process | limit | tension | interference | virtuality
    scale: sub-momentary | momentary | extended | lifetime | trans-lifetime | cosmic
    temporal: instant | transition | oscillation | accumulation | memory | anticipation
    perceptual: direct | peripheral | retrospective | failure-mediated | other-mediated | somatic
    relational: solitary | dyadic | small-group | collective | non-human | hybrid
    agential: beginner | expert | anyone | specific-capacity | non-human
    structural: simple | composite | recursive | paradoxical | incomplete | boundary-only
  }
  
  // Embedded movement operations
  gestures: {
    available: Gesture[]
    dominant: Gesture | null
    blocked: Gesture[]
    latent: Gesture[]
  }
  
  // MVA properties
  mapping_properties: {
    connected_to: Site[]
    transfer_potential: Float
    boundary: Boolean
  }
  valuation_properties: {
    value: Float
    value_type: peak | valley | slope | plateau | boundary
    contested: Boolean
  }
  orientation_properties: {
    direction: Vector
    type: source | sink | saddle | path | eddy
    stability: stable | unstable
  }
  
  // Derivation
  derived_from: Site | null
  derived_via: Constraint | null
  
  // Metadata
  fertility: Float
  stability: Float
  existence_type: engagement_dependent | persistent | periodic | conditional
}
```

---

### Gesture

A possibility operation that can be executed from a site.

```
GestureType = BRANCH | NARROW | COMMIT | DEFER | SUSPEND | WIDEN | RESOLVE

Gesture {
  type: GestureType
  strength: Float
  direction: opening | closing | holding
  target: DimensionType | null
  conditions: Condition[]
}

GestureConsequences = {
  BRANCH:  { opens: true,  commits: false, reversible: true,  creates_branches: true,  time_sensitive: false }
  NARROW:  { opens: false, commits: false, reversible: true,  creates_branches: false, time_sensitive: false }
  COMMIT:  { opens: false, commits: true,  reversible: false, creates_branches: false, time_sensitive: false }
  DEFER:   { opens: false, commits: false, reversible: true,  creates_branches: false, time_sensitive: true  }
  SUSPEND: { opens: true,  commits: false, reversible: true,  creates_branches: false, time_sensitive: true, creates_obligation: true }
  WIDEN:   { opens: true,  commits: false, reversible: true,  creates_branches: false, time_sensitive: false }
  RESOLVE: { opens: false, commits: true,  reversible: false, creates_branches: false, discharges_obligation: true }
}

// Effects on the three operations (MVA)
GestureEffects = {
  BRANCH:  { mapping: UNFOLD,   valuation: SPREAD,      orientation: MULTIPLY }
  NARROW:  { mapping: PROJECT,  valuation: CONCENTRATE, orientation: FOCUS }
  COMMIT:  { mapping: COLLAPSE, valuation: CONCENTRATE, orientation: FIX }
  DEFER:   { mapping: SUSPEND,  valuation: PRESERVE,    orientation: PAUSE }
  SUSPEND: { mapping: SUSPEND,  valuation: PRESERVE,    orientation: PAUSE }
  WIDEN:   { mapping: EXPAND,   valuation: EXTEND,      orientation: OPEN }
  RESOLVE: { mapping: COMPLETE, valuation: DISCHARGE,   orientation: ARRIVE }
}
```

---

### Field

A bounded, differentiated region of reality that can be attended to.

```
FieldLevel = material | phenomenal | conceptual | social

Field {
  id: UUID
  name: String
  description: String
  
  // Structure
  levels: {
    material: MaterialDescription | null
    phenomenal: PhenomenalDescription | null
    conceptual: ConceptualDescription | null
    social: SocialDescription | null
  }
  
  // Boundary
  boundary: {
    type: crisp | fuzzy | contested
    basis: spatial | temporal | conceptual | phenomenal | social
    stability: stable | shifting | oscillating
    permeability: Float
  }
  
  // Internal structure
  differentiation: {
    type: categorical | continuous | hierarchical | networked | mixed
    depth: Integer
    density: Float
  }
  
  // External relations
  connections: {
    parent: Field | null
    children: Field[]
    siblings: Field[]
    analogues: Field[]
    opposites: Field[]
  }
  
  // Field gestures
  gestures: EXPAND | CONTRACT | DEEPEN | FLATTEN | BRIDGE | ISOLATE | NEST | EMBED
  
  // Lifecycle
  lifecycle: latent | emerging | established | contested | fragmenting | merging | dissolving | residual
  
  // Generativity
  site_potential: Float
  practice_affordance: Practice[]
  constraint_fertility: Float
}
```

---

### Practice

A mode of engagement with fields.

```
Practice {
  id: UUID
  name: String
  description: String
  
  // What this practice engages
  engages_levels: FieldLevel[]
  core_operations: Operation[]
  
  // How constraints appear
  constraint_form: {
    name: String              // "premise", "axiom", "motif", etc.
    establishment_verb: String
    development_verb: String
    resolution_verb: String
  }
  
  // How gestures manifest
  gesture_manifestations: Map<GestureType, GestureManifestation>
  
  // Flux capacity
  flux_capacity: {
    can_dissolve: StructureLevel[]
    can_open: StructureLevel[]
    can_hover: Boolean
    can_emerge: StructureLevel[]
    dissolution_style: controlled | uncontrolled | gradual | sudden
    emergence_style: passive | guided | structured
  }
  
  // Lineage
  parent: Practice | null
  children: Practice[]
  related: Practice[]
}

GestureManifestation {
  gesture: GestureType
  verb: String
  noun: String
  example: String
}
```

---

### Domain

A stabilized practice-field pairing where sites emerge.

```
Domain {
  id: UUID
  name: String
  
  // Constitution
  practice: Practice
  field: Field
  
  // Accumulation
  sites: Site[]
  constraints: Constraint[]
  
  // State
  barrenness: {
    level: Float
    type: familiarity | completion | categorical | exhaustion | status | null
    filters_active: Filter[]
  }
  
  // Hierarchy
  parent: Domain | null
  children: Domain[]
  
  // Cross-domain relations
  bridges_to: Domain[]
  translates_to: Domain[]
}

Filter {
  type: BarrennessType
  strength: Float
  defamiliarization_applied: DefamiliarizationPractice[]
}

DefamiliarizationPractice =
  | LITERAL_ESTRANGEMENT | TEMPORAL_ESTRANGEMENT | MATERIAL_ESTRANGEMENT
  | FAILURE_ESTRANGEMENT | SCALE_ESTRANGEMENT
  | COUNTER_HISTORY | INCOMPLETENESS_HUNTING | FUTURE_PROJECTION
  | CONTRADICTION_FINDING
  | CATEGORY_REFUSAL | CATEGORY_MULTIPLICATION | CATEGORY_THEFT | META_CATEGORIZATION
  | SENSE_SWITCHING | PACE_SWITCHING | STANCE_SWITCHING | PURPOSE_SWITCHING
  | ELEVATION | EXPERTISE_SEEKING | DEPENDENCY_TRACING | INVERSION
```

---

### Constraint

A generative restriction that shapes site visibility.

```
Constraint {
  id: UUID
  description: String
  
  // Core
  predicate: (Site) => Boolean | Float
  dimensions_targeted: DimensionType[]
  
  // Properties
  strength: Float
  fertility: Float
  internalization: Float
  
  // Type
  constraint_type: ontological | scale | temporal | perceptual | relational | agential | structural | gestural | compound | meta
  
  // As MVA structure
  as_mapping: {
    from: AllPossibleSites
    to: SatisfyingSites
    transfer: what_constraint_preserves
  }
  as_valuation: {
    function: degree_of_satisfaction
    peaks: fully_satisfying
    ground: Ground
  }
  as_orientation: {
    field: toward_satisfaction
    attractor: full_satisfaction
  }
  
  // Derivation
  derived_from_site: Site | null
  parent_constraints: Constraint[]
  
  // Lifecycle
  lifecycle: potential | active | internalized | exhausted | resolved
  
  // Metadata
  times_applied: Integer
  sites_generated: Integer
  success_rate: Float
}

Ground = GIVEN | DERIVED | FUNCTIONAL | RELATIONAL | CONSTITUTIVE
```

---

### The Three Operations (MVA)

The infrastructure underlying all meaning-making.

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
  
  instance_type: formal_analogy | metaphor | embedding | projection | translation | homology
  semantic_content: SemanticContent | null
}

Valuation {
  id: UUID
  domain: Structure
  
  function: (Element) => Value
  
  properties: {
    value_type: cardinal | ordinal | partial_order | boolean
    range: [min, max] | unbounded
    differentiability: smooth | discontinuous
  }
  
  ground: Ground
  instance_type: preference | importance | salience | stakes | care | narrative_significance
}

Orientation {
  id: UUID
  space: Structure
  
  field: (Point) => Direction
  
  properties: {
    type: point_attractor | gradient | flow | basin_structure
    strength: Float
    stability: stable | dynamic | chaotic
  }
  
  source: TELOS | ORIGIN | GRADIENT | ATTRACTOR | FIELD | INTERNAL
  instance_type: telos | origin | gradient | attractor | causal | narrative_trajectory
}
```

---

### Flux

The ever-present ground from which structures emerge and to which they can return.

```
FluxState {
  mode: structured | dissolving | hovering | flux
  
  // If structured
  structure_solidity: Float
  
  // If dissolving
  dissolving_structures: Structure[]
  dissolution_progress: Float
  flux_pockets: FluxPocket[]
  
  // If hovering
  boundary: Boundary
  hovering_duration: Duration
  stability: Float
  
  // If flux
  flux_region: FluxRegion
  loose_constraints: Constraint[]
  pre_structures: PreStructure[]
}

FluxPocket {
  id: UUID
  location: Structure
  dissolved_from: Structure | null
  attention: Attention
  emerging: PreStructure[]
  duration: Duration
}

PreStructure {
  id: UUID
  coherence: Float
  provisional_description: String
  fragility: Float
  related_to: Structure[]
}

FluxOperation = DISSOLVE | OPEN | EMERGE | HOVER
```

---

## State

The system maintains complete state:

```
State {
  // Current position
  current_site: Site | null
  current_domain: Domain | null
  active_constraints: Constraint[]
  
  // Workspace
  constraint_queue: Constraint[]
  derived_constraints: Constraint[]
  
  // History
  history: HistoryTree
  current_node: HistoryNode
  
  // Accumulation
  all_sites: Site[]
  all_constraints: Constraint[]
  all_domains: Domain[]
  all_fields: Field[]
  all_practices: Practice[]
  
  // MVA state
  mva: {
    active_mappings: Mapping[]
    active_valuations: Valuation[]
    active_orientations: Orientation[]
    convergences: MVAConvergence[]
    conflicts: MVAConflict[]
  }
  
  // Flux state
  flux: FluxState
  flux_history: FluxEvent[]
  flux_capacity: {
    dissolution_tolerance: Float
    reconstitution_speed: Float
    hovering_stability: Float
    flux_duration_tolerance: Float
  }
  
  // Analysis
  detected_attractors: Attractor[]
  current_basin: Basin | null
  
  // Speculation mode
  speculation_mode: {
    active: Boolean
    hypothetical_fields: Field[]
    hypothetical_practices: Practice[]
    hypothetical_domains: Domain[]
    hypothetical_constraints: Constraint[]
    hypothetical_sites: Site[]
  }
  
  // Constraint hygiene
  constraint_audit: {
    given: Constraint[]
    assumed: Constraint[]
    assumption_warranted: Map<Constraint, Boolean>
  }
  
  // Session
  session_id: UUID
  created_at: Timestamp
  last_modified: Timestamp
}

HistoryNode {
  id: UUID
  site: Site | null
  constraints_active: Constraint[]
  domain: Domain | null
  
  parent: HistoryNode | null
  children: HistoryNode[]
  
  operation_that_led_here: Operation
  branch_taken: Boolean
  timestamp: Timestamp
}

Attractor {
  id: UUID
  type: site_attractor | constraint_attractor | joint_attractor
  sites_involved: Site[]
  constraints_involved: Constraint[]
  basin_size_estimate: Float
  stability: Float
}
```

---

## Operations

### Site Operations

```
Generate(state: State) => Site[]
GenerateWithGestureEmphasis(state: State, gesture: GestureType) => Site[]
DeriveConstraints(state: State) => Constraint[]
DeriveSitesFromGesture(state: State, gesture: GestureType) => Site[]
```

### Constraint Operations

```
AddConstraint(state: State, constraint: Constraint) => State
RemoveConstraint(state: State, constraint_id: UUID) => State
ModifyConstraint(state: State, constraint_id: UUID, modification: Modification) => State
ConjoinConstraints(state: State, c1: UUID, c2: UUID) => Constraint
DisjoinConstraints(state: State, c1: UUID, c2: UUID) => Constraint
SequenceConstraints(state: State, c1: Constraint, c2: Constraint) => Constraint
NestConstraints(state: State, outer: Constraint, inner: Constraint) => Constraint
RecurseConstraint(state: State, constraint: Constraint) => Constraint
```

### Navigation Operations

```
MoveTo(state: State, site_id: UUID) => State
FollowGesture(state: State, gesture: GestureType) => State
Backtrack(state: State, steps: Integer) => State
TakeBranch(state: State, node_id: UUID) => State
```

### Domain Operations

```
CreateDomain(practice: Practice, field: Field) => Domain
EnterDomain(state: State, domain: Domain) => State
SwitchPractice(state: State, practice: Practice) => State
SwitchField(state: State, field: Field) => State
DiagnoseBarrenness(state: State) => BarrennessDiagnosis
ApplyDefamiliarization(state: State, practice: DefamiliarizationPractice) => State
```

### Field Operations

```
GenerateField(mode: FieldGenerationMode, constraints: FieldConstraint[]) => Field[]
SplitField(field: Field, fault_line: FaultLine) => Field[]
MergeFields(fields: Field[], similarity: Similarity) => Field
GenerateByAnalogy(source: Field, target_region: Region) => Field
```

### Flux Operations

```
DissolveField(state: State, field: Field, mode: DissolutionMode) => State
OpenFluxInField(state: State, field: Field) => FluxPocket
EmergeFromFlux(state: State, pocket: FluxPocket, constraints: Constraint[]) => Field[]
HoverAtBoundary(state: State, field: Field) => Boundary
```

### Translation Operations

```
TranslateSite(site: Site, source: Domain, target: Domain) => Site | null
TransferConstraint(constraint: Constraint, source: Domain, target: Domain) => Constraint | null
IdentifyBridgingSites(domain_a: Domain, domain_b: Domain) => Site[]
```

### Speculation Operations

```
// Enter/exit speculation mode
EnterSpeculation(state: State) => State
ExitSpeculation(state: State) => State

// Hypothesize without committing
Hypothesize(state: State, hypothetical: Constraint | Field | Practice | Domain) => State
CommitHypothetical(state: State, id: UUID) => State
DiscardHypothetical(state: State, id: UUID) => State

// Generate speculative structures
SpeculateField(flux_region: FluxRegion, boundary_basis: BoundaryBasis) => Field
SpeculatePractice(levels: FieldLevel[], flux_capacity: FluxCapacity) => Practice
SpeculateDomain(practice: Practice, field: Field) => Domain
SpeculateSite(domain: Domain, dimensional_coordinates: DimensionalCoordinates) => Site

// Generate under hypotheticals
GenerateUnderHypotheticals(state: State) => Site[]
```

### Constraint Hygiene Operations

```
// Audit constraints for given vs assumed
AuditConstraints(state: State) => ConstraintAuditResult

ConstraintAuditResult {
  given: Constraint[]
  assumed: Constraint[]
  blocked_by_assumption: Gesture[]
  recommendation: "drop" | "keep" | "investigate"
}

// Remove unwarranted assumptions
DropAssumedConstraints(state: State, to_drop: Constraint[]) => State

// Check if a gesture is genuinely blocked
CheckGestureBlock(state: State, gesture: GestureType) => {
  blocked: Boolean
  blocked_by: Constraint | null
  block_type: "given" | "assumed" | "structural"
}
```

### TransitionValue (Evaluating Movement)

All movement — whether local (gesture) or global (generation/speculation) — can be evaluated. TransitionValue is the framework for this evaluation.

```
// What accompanies any transition
TransitionValue {
  // Intensity delta: did the frame grow or shrink?
  mode: collapse | expansion | null
  
  // How the transition feels
  affect: Affect
  
  // Generative values (pick which to optimize)
  values: {
    vertigo: Float      // Frame displacement
    fertility: Float    // Derivation potential
    coherence: Float    // Fit with existing structures
    novelty: Float      // Difference from existing
    depth: Float        // Levels affected
    stability: Float    // Persistence expected
  }
  
  // What emerged
  precipitated: Structure[]
  
  // Productivity
  outcome: productive | decorative | noise
}

// Affect: the phenomenology of transition
Affect = comedic | tragic | uncanny | sublime | quotidian | vertiginous | disorienting | liberating

// Mode: intensity delta
TransitionMode = {
  collapse: {
    description: "The frame shrinks or breaks"
    intensity_delta: negative
    examples: [
      "Memory-as-counterfeiting dissolves archive model",
      "Bounding 'incompetent action' cracks competence-as-prerequisite"
    ]
  }
  expansion: {
    description: "The frame opens wider than expected"
    intensity_delta: positive
    examples: [
      "Recursion→Architecture reveals scale-collapse",
      "Bridging sleep and problem-solving reveals new field"
    ]
  }
}

// Affect can accompany either mode
// collapse + comedic = bathetic deflation
// collapse + tragic = loss of ground
// expansion + sublime = overwhelming opening
// expansion + uncanny = familiar becoming vast
```

---

### Gestures (Local and Global)

Gestures are possibility operations. **Local gestures** move between sites. **Global gestures** move between structures at any level.

```
// Local gestures (site → site)
GestureType = BRANCH | NARROW | COMMIT | DEFER | SUSPEND | WIDEN | RESOLVE

Gesture {
  type: GestureType
  strength: Float
  direction: opening | closing | holding
  target: DimensionType | null
  conditions: Condition[]
}

// Gesture execution carries transition value
GestureExecution {
  gesture: Gesture
  from: Site
  to: Site
  transition_value: TransitionValue
}

// Global gestures (structure → structure at any level)
GlobalGestureType = GENERATE | SPECULATE | TRANSFER | DISSOLVE | EMERGE

GlobalGesture {
  type: GlobalGestureType
  level: field | practice | domain | site | constraint | gesture
  source: Structure | null  // null for emergence from flux
  target: Structure | null  // null for dissolution into flux
}

GlobalGestureExecution {
  gesture: GlobalGesture
  before_state: State
  after_state: State
  transition_value: TransitionValue
}

// Global gestures defined
GlobalGestureSemantics = {
  GENERATE: {
    description: "Produce new structure under constraints"
    direction: opening
    typical_mode: expansion
  }
  SPECULATE: {
    description: "Produce structure under hypothetical conditions"
    direction: opening
    typical_mode: expansion
  }
  TRANSFER: {
    description: "Apply structure from one domain to another"
    direction: opening | closing  // depends on transfer
    typical_mode: collapse | expansion  // vertigo-prone
  }
  DISSOLVE: {
    description: "Return structure to flux"
    direction: opening  // releases constraint
    typical_mode: collapse
  }
  EMERGE: {
    description: "Precipitate structure from flux"
    direction: closing  // creates constraint
    typical_mode: expansion
  }
}
```

---

### Evaluating Transitions

```
// Evaluate any transition (local or global)
EvaluateTransition(execution: GestureExecution | GlobalGestureExecution) => TransitionValue

// Choose which values to optimize
TransitionValueProfile {
  weights: Map<ValueType, Float>  // which values matter for this operation
}

// Example profiles
BreakingOpen: { vertigo: 0.8, novelty: 0.2 }
BuildingOut: { coherence: 0.6, fertility: 0.3, stability: 0.1 }
Seeding: { fertility: 0.7, novelty: 0.3 }
Grounding: { stability: 0.5, coherence: 0.4, depth: 0.1 }

// The vertigo test (now one value among many)
HasVertigo(execution: GestureExecution | GlobalGestureExecution) => Boolean
  // Can you still use the naive model innocently?
  // High vertigo + low noise = productive displacement

// Strangeness as heuristic (applies to any pairing)
StrangenessScore(a: Structure, b: Structure) => Float
  // Categorical distance
  // Higher = more likely to produce vertigo
  // Strangeness is heuristic, not guarantee
```

---

### Frame

The default model that a transition can displace.

```
Frame {
  id: UUID
  description: String
  
  // What level the frame operates at
  level: field | practice | domain | site | constraint | gesture
  
  // What the frame assumed
  ontological_commitments: Assumption[]
  
  // What the frame made visible/invisible
  visibility_structure: {
    visible: Structure[]
    invisible: Structure[]
  }
  
  // Stability
  load_bearing: Boolean
  contingency_visible: Boolean
}

// Transition displaces frame when:
// 1. The frame was operative (you were using it)
// 2. The transition produced structures incompatible with it
// 3. You can't return to using it innocently
```

---

## Constraint Templates

Pre-built constraints for common generation tasks:

```
// Ontological
is_absence: (s) => s.dimensions.ontological == 'absence'
is_relation: (s) => s.dimensions.ontological == 'relation'
is_process: (s) => s.dimensions.ontological == 'process'
is_limit: (s) => s.dimensions.ontological == 'limit'
is_tension: (s) => s.dimensions.ontological == 'tension'
is_interference: (s) => s.dimensions.ontological == 'interference'
is_virtuality: (s) => s.dimensions.ontological == 'virtuality'

// Temporal
exists_only_in_transition: (s) => s.dimensions.temporal == 'transition'
exists_only_in_memory: (s) => s.dimensions.temporal == 'memory'
exists_only_in_anticipation: (s) => s.dimensions.temporal == 'anticipation'

// Perceptual
perceived_only_through_failure: (s) => s.dimensions.perceptual == 'failure-mediated'
perceived_only_through_other: (s) => s.dimensions.perceptual == 'other-mediated'
perceived_only_retrospectively: (s) => s.dimensions.perceptual == 'retrospective'

// Relational
requires_solitude: (s) => s.dimensions.relational == 'solitary'
requires_two_people: (s) => s.dimensions.relational == 'dyadic'
involves_non_human: (s) => s.dimensions.relational in ['non-human', 'hybrid']

// Structural
is_recursive: (s) => s.dimensions.structural == 'recursive'
is_paradoxical: (s) => s.dimensions.structural == 'paradoxical'
is_incomplete: (s) => s.dimensions.structural == 'incomplete'

// Gestural
dominant_gesture_is(g): (s) => s.gestures.dominant == g
affords_gesture(g): (s) => g in s.gestures.available
blocks_gesture(g): (s) => g in s.gestures.blocked
has_latent_gesture(g): (s) => g in s.gestures.latent
primarily_opening: (s) => count(opening_gestures(s)) > count(closing_gestures(s))
primarily_closing: (s) => count(closing_gestures(s)) > count(opening_gestures(s))
gesture_rich: (s) => s.gestures.available.length >= 4
gesture_poor: (s) => s.gestures.available.length <= 2
```

---

## Gesture Manifestations by Practice

```
Writing: {
  BRANCH: "Open narrative possibilities without committing"
  NARROW: "Specify detail, close off alternatives"
  COMMIT: "Irreversible plot event, revelation"
  DEFER: "Withhold information, delay resolution"
  SUSPEND: "Pose question, create tension without answering"
  WIDEN: "Expand scope, introduce new elements"
  RESOLVE: "Answer question, complete arc, end"
}

Mathematics: {
  BRANCH: "Consider cases, disjunctive proof"
  NARROW: "Add hypothesis, specialize theorem"
  COMMIT: "Assert lemma, take as proven"
  DEFER: "Leave as exercise, postpone proof"
  SUSPEND: "Conjecture, open problem"
  WIDEN: "Generalize, remove hypotheses"
  RESOLVE: "Complete proof, QED"
}

Music: {
  BRANCH: "Variation, alternative voicing"
  NARROW: "Develop theme, reduce to motif"
  COMMIT: "Cadence, arrival"
  DEFER: "Deceptive cadence, extension"
  SUSPEND: "Suspension, pedal point, dominant prolongation"
  WIDEN: "Modulation, new theme, expansion"
  RESOLVE: "Authentic cadence, return to tonic"
}

Philosophy: {
  BRANCH: "Distinguish cases, consider objections"
  NARROW: "Define terms, specify conditions"
  COMMIT: "Assert thesis, take position"
  DEFER: "Bracket question, set aside"
  SUSPEND: "Aporia, unresolved tension"
  WIDEN: "Extend argument, connect to new problems"
  RESOLVE: "Conclude argument, dissolve problem"
}
```

---

## Summary

The system has four levels:

1. **Flux** — undifferentiated ground, always accessible
2. **Field** — bounded, differentiated region (generated via BOUND, DIFFERENTIATE, CONNECT, POPULATE)
3. **Domain** — practice × field pairing (where sites become visible)
4. **Site** — position with embedded gestures (generated under constraints)

Three primitive operations underlie all structure:

- **Mapping**: relates structures (A → B)
- **Valuation**: assigns significance (X → value)
- **Orientation**: establishes direction (point → vector)

Seven gestures move through possibility space:

- Opening: BRANCH, WIDEN, SUSPEND
- Closing: NARROW, COMMIT, RESOLVE
- Holding: DEFER
