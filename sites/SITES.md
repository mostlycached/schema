Full specification that integrates the constraint formalism with the possibility gesture grammar, so sites aren't just static positions but have operational dynamics embedded in them.
Addl. Context: https://docs.google.com/document/d/12pF3UwwmwTwwdSJq73oy7NUu9AuQYz38OQLgQKNa-vM/edit?tab=t.ic1w1hyx3lz8 

---

## Specification: Constraint-Based Site Generation Engine

### Overview

A system for navigating and generating sites within a multi-dimensional space, where:
- **Sites** are positions with embedded movement operations (possibility gestures)
- **Constraints** shape generation by warping the space
- **Domains** provide context and barrenness diagnostics
- **History** accumulates as navigable branching structure

The system tracks state, executes operations, and presents navigable views of the territory being explored.

---

## Core Ontology

### Site

A site is not just a location but a **structured position with embedded dynamics**.

```
Site {
  id: UUID
  
  // Content
  description: String           // What the site is
  domain: Domain | null         // What domain it belongs to
  
  // Dimensional position
  dimensions: {
    ontological: OntologicalType    // substance | relation | absence | process | limit | tension | interference | virtuality
    scale: ScaleType                // sub-momentary | momentary | extended | lifetime | trans-lifetime | cosmic
    temporal: TemporalType          // instant | transition | oscillation | accumulation | memory | anticipation
    perceptual: PerceptualType      // direct | peripheral | retrospective | failure-mediated | other-mediated | somatic
    relational: RelationalType      // solitary | dyadic | small-group | collective | non-human | hybrid
    agential: AgentialType          // beginner | expert | anyone | specific-capacity | non-human
    structural: StructuralType      // simple | composite | recursive | paradoxical | incomplete | boundary-only
  }
  
  // Embedded movement operations (possibility gestures)
  gestures: {
    available: Gesture[]            // What movements this site affords
    dominant: Gesture | null        // The site's characteristic gesture
    blocked: Gesture[]              // What movements this site forecloses
    latent: Gesture[]               // Movements available but not obvious
  }
  
  // Relational
  derived_from: Site | null         // Parent site if derived
  derived_via: Constraint | null    // Constraint that produced this site
  
  // Metadata
  created_at: Timestamp
  generation_number: Integer        // How many steps from origin
  fertility: Float                  // How many constraints/sites derived from this
  stability: Float                  // How often generation returns here (attractor measure)
}
```

### Gesture (Possibility Operations)

The seven core operations from the earlier grammar, embedded in sites:

```
Gesture {
  type: GestureType
  strength: Float                   // 0-1, how strongly the gesture operates
  direction: GestureDirection       // opening | closing | ambiguous
  target: DimensionType | null      // Which dimension it primarily affects
  conditions: Condition[]           // When the gesture activates
}

GestureType = 
  | BRANCH    // Create divergent paths without committing
  | NARROW    // Reduce possibilities by adding constraints  
  | COMMIT    // Foreclose alternatives irrevocably
  | DEFER     // Preserve option value by postponing commitment
  | SUSPEND   // Hold open possibility for later resolution
  | WIDEN     // Expand possibility space beyond current boundaries
  | RESOLVE   // Collapse suspended possibilities into determinate state

GestureDirection = opening | closing | ambiguous

// Examples of embedded gestures:
// 
// Site: "The pause in speech"
//   dominant: SUSPEND (holds open what comes next)
//   available: [BRANCH (pause can go multiple directions), RESOLVE (pause ends)]
//   blocked: [COMMIT (pause is inherently uncommitted)]
//
// Site: "The unlived life"  
//   dominant: DEFER (perpetually postponed)
//   available: [WIDEN (more unlived possibilities), NARROW (grieving specific paths)]
//   blocked: [RESOLVE (can never be fully resolved), COMMIT (can't commit to unlived)]
//   latent: [BRANCH (unlived life as generative source)]
```

### Constraint

```
Constraint {
  id: UUID
  
  // Content
  description: String               // Human-readable description
  predicate: SitePredicate          // Formal condition sites must satisfy
  
  // Dimensional targeting
  dimensions_targeted: DimensionType[]
  
  // Constraint properties
  strength: Float                   // 0-1, how restrictive
  fertility: Float                  // Estimated generative potential
  internalization: Float            // 0-1, how automatic it's become
  
  // Type
  constraint_type: ConstraintType
  
  // Relational
  derived_from_site: Site | null
  parent_constraints: Constraint[]  // If combined from others
  
  // Metadata  
  times_applied: Integer
  sites_generated: Integer
  success_rate: Float               // Proportion of generation attempts that succeeded
}

ConstraintType =
  | ONTOLOGICAL     // What kind of being
  | SCALE           // What size
  | TEMPORAL        // What time-structure
  | PERCEPTUAL      // How perceived
  | RELATIONAL      // What social structure
  | AGENTIAL        // Who can access
  | STRUCTURAL      // What internal structure
  | GESTURAL        // What movements embedded (constraint on gestures)
  | COMPOUND        // Combination of above
  | META            // Constraint on constraints

SitePredicate = (Site) => Boolean | Float  // Boolean for hard constraints, Float for soft
```

### Gestural Constraints

A special class of constraints that target the embedded gestures:

```
GesturalConstraint extends Constraint {
  gesture_requirement: {
    must_have: GestureType[]        // Site must afford these gestures
    must_lack: GestureType[]        // Site must block these gestures
    dominant_must_be: GestureType | null
    direction_must_be: GestureDirection | null
    min_gesture_count: Integer | null
  }
}

// Examples:
//
// "Generate a site whose dominant gesture is SUSPEND"
// "Generate a site that blocks COMMIT"  
// "Generate a site that affords BRANCH and NARROW simultaneously"
// "Generate a site with only closing gestures"
// "Generate a site with at least 4 available gestures"
```

### Domain

```
Domain {
  id: UUID
  name: String
  description: String
  
  // Barrenness state
  barrenness: {
    level: Float                    // 0-1, perceived barrenness
    type: BarrennessType | null     // Diagnosed type
    filters_active: Filter[]
  }
  
  // Domain properties
  familiarity: Float                // How exposed you've been
  status: Float                     // Cultural status level
  completion_narrative: String | null
  categorization: String[]
  effort_expended: Float            // Work already done here
  
  // Sites in domain
  sites_discovered: Site[]
  sites_density_estimate: Float     // Estimated actual density
}

BarrennessType = 
  | FAMILIARITY       // Too familiar to see
  | COMPLETION        // Narrative says it's finished
  | CATEGORICAL       // Category forecloses seeing
  | EXHAUSTION        // You've worked it too hard
  | STATUS            // Low status occludes
  
Filter {
  type: BarrennessType
  strength: Float
  defamiliarization_applied: DefamiliarizationPractice[]
}

DefamiliarizationPractice =
  | LITERAL_ESTRANGEMENT
  | TEMPORAL_ESTRANGEMENT  
  | MATERIAL_ESTRANGEMENT
  | FAILURE_ESTRANGEMENT
  | SCALE_ESTRANGEMENT
  | COUNTER_HISTORY
  | INCOMPLETENESS_HUNTING
  | FUTURE_PROJECTION
  | CONTRADICTION_FINDING
  | CATEGORY_REFUSAL
  | CATEGORY_MULTIPLICATION
  | CATEGORY_THEFT
  | META_CATEGORIZATION
  | SENSE_SWITCHING
  | PACE_SWITCHING
  | STANCE_SWITCHING
  | PURPOSE_SWITCHING
  | ELEVATION
  | EXPERTISE_SEEKING
  | DEPENDENCY_TRACING
  | INVERSION
```

---

## State

The system maintains a complete state:

```
State {
  // Current position
  current_site: Site | null
  current_domain: Domain | null
  active_constraints: Constraint[]
  
  // Constraint workspace
  constraint_queue: Constraint[]    // Queued for sequential application
  derived_constraints: Constraint[] // Extracted but not yet applied
  
  // History (branching)
  history: HistoryTree
  current_node: HistoryNode
  
  // Accumulations
  all_sites: Site[]
  all_constraints: Constraint[]
  all_domains: Domain[]
  
  // Analysis
  detected_attractors: Attractor[]
  current_basin: Basin | null
  
  // Session
  session_id: UUID
  created_at: Timestamp
  last_modified: Timestamp
}

HistoryTree {
  root: HistoryNode
  nodes: HistoryNode[]
}

HistoryNode {
  id: UUID
  site: Site | null
  constraints_active: Constraint[]
  domain: Domain | null
  
  parent: HistoryNode | null
  children: HistoryNode[]           // Branches taken and not taken
  
  operation_that_led_here: Operation
  branch_taken: Boolean             // True if this path was followed
  
  timestamp: Timestamp
}

Attractor {
  id: UUID
  type: AttractorType               // site_attractor | constraint_attractor | joint_attractor
  sites_involved: Site[]
  constraints_involved: Constraint[]
  basin_size_estimate: Float
  stability: Float
}

Basin {
  attractor: Attractor
  boundary_sites: Site[]            // Sites at the edge of this basin
  escape_constraints: Constraint[]  // Constraints that might exit basin
}
```

---

## Operations

### Generation Operations

```
Operation: Generate
  Input: State
  Effect: 
    - Uses active_constraints to shape generation
    - Produces candidate Site(s)
    - Computes gesture profile for each candidate
    - Updates history tree
  Output: Site[]

Operation: GenerateWithGestureEmphasis
  Input: State, GestureType
  Effect:
    - Generate but bias toward sites where specified gesture is dominant/available
  Output: Site[]

Operation: DeriveConstraints  
  Input: State
  Effect:
    - Analyzes current_site
    - Extracts potential constraints from site properties and gestures
    - Adds to derived_constraints
  Output: Constraint[]

Operation: DeriveSitesFromGesture
  Input: State, GestureType
  Effect:
    - Takes a gesture available at current site
    - "Runs" the gesture to generate what it opens/closes
    - Produces sites reachable by that gesture
  Output: Site[]
```

### Constraint Operations

```
Operation: AddConstraint
  Input: State, Constraint
  Effect: Adds constraint to active_constraints
  Output: State

Operation: RemoveConstraint
  Input: State, Constraint.id
  Effect: Removes constraint from active_constraints
  Output: State

Operation: ModifyConstraint
  Input: State, Constraint.id, Modification
  Effect: Adjusts constraint strength/scope
  Output: State
  
  Modification = 
    | Strengthen(factor: Float)
    | Weaken(factor: Float)
    | Negate
    | ExpandScope(dimensions: DimensionType[])
    | ContractScope(dimensions: DimensionType[])

Operation: ConjoinConstraints
  Input: State, Constraint.id, Constraint.id
  Effect: Creates new compound constraint (AND)
  Output: Constraint

Operation: DisjoinConstraints
  Input: State, Constraint.id, Constraint.id
  Effect: Creates new compound constraint (OR)
  Output: Constraint

Operation: SequenceConstraints
  Input: State, Constraint, Constraint
  Effect: Creates sequential constraint (first, then second)
  Output: Constraint

Operation: NestConstraints
  Input: State, Constraint (outer), Constraint (inner)
  Effect: Creates nested constraint (outer applied to output of inner)
  Output: Constraint

Operation: RecurseConstraint
  Input: State, Constraint
  Effect: Creates self-referential constraint
  Output: Constraint
```

### Domain Operations

```
Operation: EnterDomain
  Input: State, Domain | String (name)
  Effect: Sets current_domain, initializes domain if new
  Output: State

Operation: DiagnoseBarrenness
  Input: State
  Precondition: current_domain is set
  Effect: Analyzes domain for barrenness type
  Output: BarrennessDiagnosis

Operation: ApplyDefamiliarization
  Input: State, DefamiliarizationPractice
  Effect: 
    - Applies practice to current domain
    - Reduces filter strength
    - May reveal previously invisible sites
  Output: State, Site[] (newly visible)
```

### Navigation Operations

```
Operation: MoveTo
  Input: State, Site.id
  Effect: Changes current_site, updates history
  Output: State

Operation: FollowGesture
  Input: State, GestureType
  Precondition: Gesture is available at current_site
  Effect:
    - Executes the gesture from current site
    - Generates destination site(s)
    - Moves to selected destination
  Output: State

Operation: Backtrack
  Input: State, steps: Integer
  Effect: Reverts to ancestor node in history tree
  Output: State

Operation: TakeBranch
  Input: State, HistoryNode.id
  Effect: Jumps to unexplored branch
  Output: State

Operation: MarkBranch
  Input: State, annotation: String
  Effect: Annotates current node for later return
  Output: State
```

### Analysis Operations

```
Operation: AnalyzePosition
  Input: State
  Output: PositionAnalysis
  
  PositionAnalysis {
    local_density: Float            // How many sites nearby
    constraint_satisfaction: Map<Constraint, Float>
    gesture_profile: GestureProfile
    attractor_proximity: Attractor | null
    basin_info: Basin | null
    suggested_moves: SuggestedMove[]
  }
  
  GestureProfile {
    dominant_gesture: GestureType
    opening_potential: Float        // Sum of opening gesture strengths
    closing_potential: Float        // Sum of closing gesture strengths
    gesture_diversity: Float        // How many gestures available
    blocked_gestures: GestureType[]
  }
  
  SuggestedMove {
    operation: Operation
    rationale: String
    expected_outcome: String
    risk: Float
  }

Operation: AnalyzeHistory
  Input: State
  Output: HistoryAnalysis
  
  HistoryAnalysis {
    total_sites_visited: Integer
    total_constraints_used: Integer
    gesture_usage: Map<GestureType, Integer>
    dimension_coverage: Map<DimensionType, Float>
    attractor_visits: Attractor[]
    loops_detected: Loop[]
    fertile_branches: HistoryNode[]
    unexplored_branches: HistoryNode[]
  }
  
  Loop {
    nodes: HistoryNode[]
    constraint_pattern: Constraint[]
    gesture_pattern: GestureType[]
  }

Operation: DetectAttractors
  Input: State
  Effect: Analyzes history for attractor patterns
  Output: Attractor[]

Operation: MapBasin
  Input: State, Attractor
  Effect: Explores boundaries of attractor's basin
  Output: Basin
```

---

## Gesture Dynamics

The gestures aren't just labels—they're *operations* that can be executed from a site:

```
GestureDynamics {
  
  // Executing a gesture from a site
  execute(site: Site, gesture: GestureType): Site[] {
    switch(gesture) {
      
      BRANCH: 
        // Generate multiple divergent sites, none committed
        // Increases possibility space
        // Creates multiple history branches
        return generate_divergent_sites(site, branch_count: 2-5)
        
      NARROW:
        // Add constraint, reduce possibility space
        // Move toward more specific sites
        // History continues linearly but constrained
        return generate_constrained_sites(site, narrowing_constraint)
        
      COMMIT:
        // Foreclose alternatives
        // Move to a site with blocked gestures (especially BRANCH, DEFER)
        // Mark abandoned branches as closed
        return generate_committed_site(site, close_branches: true)
        
      DEFER:
        // Preserve current position without advancing
        // Increase "option value" on current site
        // Time-sensitive: the longer deferred, the more pressure to resolve
        return [site.with(deferral_count: site.deferral_count + 1)]
        
      SUSPEND:
        // Hold a question/tension open
        // Generate a site that embodies irresolution
        // Creates obligation for future RESOLVE
        return generate_suspended_site(site, suspension_content)
        
      WIDEN:
        // Expand beyond current constraints
        // Remove or weaken active constraints
        // Move to site with more available gestures
        return generate_widened_sites(site, constraints_to_loosen)
        
      RESOLVE:
        // Collapse suspended state
        // Move to determinate site
        // Discharge obligation from prior SUSPEND
        return generate_resolved_site(site, suspension_to_resolve)
    }
  }
  
  // Gesture compatibility at a site
  compatible(site: Site, gesture: GestureType): Boolean {
    return gesture in site.gestures.available 
           && gesture not in site.gestures.blocked
  }
  
  // Gesture consequences
  consequences(gesture: GestureType): GestureConsequences {
    return {
      BRANCH: { 
        opens: true, 
        commits: false, 
        reversible: true,
        creates_branches: true,
        time_sensitive: false
      },
      NARROW: {
        opens: false,
        commits: false,  // narrowing isn't committing—can still widen
        reversible: true,
        creates_branches: false,
        time_sensitive: false
      },
      COMMIT: {
        opens: false,
        commits: true,
        reversible: false,
        creates_branches: false,  // closes branches
        time_sensitive: false
      },
      DEFER: {
        opens: false,  // doesn't open or close—holds
        commits: false,
        reversible: true,
        creates_branches: false,
        time_sensitive: true  // option value decays
      },
      SUSPEND: {
        opens: true,  // opens a question
        commits: false,
        reversible: true,  // can resolve
        creates_branches: false,
        time_sensitive: true,  // creates obligation
        creates_obligation: true
      },
      WIDEN: {
        opens: true,
        commits: false,
        reversible: true,
        creates_branches: false,  // expands current branch
        time_sensitive: false
      },
      RESOLVE: {
        opens: false,
        commits: true,  // resolving is a form of committing
        reversible: false,
        creates_branches: false,
        discharges_obligation: true
      }
    }[gesture]
  }
}
```

---

## Constraint Templates

Pre-built constraints for common generation tasks:

```
ConstraintTemplates {
  
  // Ontological
  is_absence: Constraint {
    predicate: (s) => s.dimensions.ontological == 'absence'
    dimensions_targeted: ['ontological']
  }
  
  is_relation: Constraint {
    predicate: (s) => s.dimensions.ontological == 'relation'
    dimensions_targeted: ['ontological']
  }
  
  is_process: Constraint {
    predicate: (s) => s.dimensions.ontological == 'process'
    dimensions_targeted: ['ontological']
  }
  
  is_limit: Constraint {
    predicate: (s) => s.dimensions.ontological == 'limit'
    dimensions_targeted: ['ontological']
  }
  
  is_tension: Constraint {
    predicate: (s) => s.dimensions.ontological == 'tension'
    dimensions_targeted: ['ontological']
  }
  
  is_interference: Constraint {
    predicate: (s) => s.dimensions.ontological == 'interference'
    dimensions_targeted: ['ontological']
  }
  
  is_virtuality: Constraint {
    predicate: (s) => s.dimensions.ontological == 'virtuality'
    dimensions_targeted: ['ontological']
  }
  
  // Scale
  smaller_than_moment: Constraint {
    predicate: (s) => s.dimensions.scale == 'sub-momentary'
    dimensions_targeted: ['scale']
  }
  
  larger_than_lifetime: Constraint {
    predicate: (s) => s.dimensions.scale in ['trans-lifetime', 'cosmic']
    dimensions_targeted: ['scale']
  }
  
  // Temporal
  exists_only_in_transition: Constraint {
    predicate: (s) => s.dimensions.temporal == 'transition'
    dimensions_targeted: ['temporal']
  }
  
  exists_only_in_memory: Constraint {
    predicate: (s) => s.dimensions.temporal == 'memory'
    dimensions_targeted: ['temporal']
  }
  
  exists_only_in_anticipation: Constraint {
    predicate: (s) => s.dimensions.temporal == 'anticipation'
    dimensions_targeted: ['temporal']
  }
  
  // Perceptual
  perceived_only_through_failure: Constraint {
    predicate: (s) => s.dimensions.perceptual == 'failure-mediated'
    dimensions_targeted: ['perceptual']
  }
  
  perceived_only_through_other: Constraint {
    predicate: (s) => s.dimensions.perceptual == 'other-mediated'
    dimensions_targeted: ['perceptual']
  }
  
  perceived_only_retrospectively: Constraint {
    predicate: (s) => s.dimensions.perceptual == 'retrospective'
    dimensions_targeted: ['perceptual']
  }
  
  // Relational
  requires_two_people: Constraint {
    predicate: (s) => s.dimensions.relational == 'dyadic'
    dimensions_targeted: ['relational']
  }
  
  requires_solitude: Constraint {
    predicate: (s) => s.dimensions.relational == 'solitary'
    dimensions_targeted: ['relational']
  }
  
  involves_non_human: Constraint {
    predicate: (s) => s.dimensions.relational in ['non-human', 'hybrid']
    dimensions_targeted: ['relational']
  }
  
  // Structural
  is_recursive: Constraint {
    predicate: (s) => s.dimensions.structural == 'recursive'
    dimensions_targeted: ['structural']
  }
  
  is_paradoxical: Constraint {
    predicate: (s) => s.dimensions.structural == 'paradoxical'
    dimensions_targeted: ['structural']
  }
  
  is_incomplete: Constraint {
    predicate: (s) => s.dimensions.structural == 'incomplete'
    dimensions_targeted: ['structural']
  }
  
  // Gestural constraints
  dominant_gesture_is(g: GestureType): Constraint {
    predicate: (s) => s.gestures.dominant == g
    dimensions_targeted: ['gestural']
  }
  
  affords_gesture(g: GestureType): Constraint {
    predicate: (s) => g in s.gestures.available
    dimensions_targeted: ['gestural']
  }
  
  blocks_gesture(g: GestureType): Constraint {
    predicate: (s) => g in s.gestures.blocked
    dimensions_targeted: ['gestural']
  }
  
  has_latent_gesture(g: GestureType): Constraint {
    predicate: (s) => g in s.gestures.latent
    dimensions_targeted: ['gestural']
  }
  
  primarily_opening: Constraint {
    predicate: (s) => {
      opening = s.gestures.available.filter(g => g.direction == 'opening')
      closing = s.gestures.available.filter(g => g.direction == 'closing')
      return opening.length > closing.length
    }
    dimensions_targeted: ['gestural']
  }
  
  primarily_closing: Constraint {
    predicate: (s) => {
      opening = s.gestures.available.filter(g => g.direction == 'opening')
      closing = s.gestures.available.filter(g => g.direction == 'closing')
      return closing.length > opening.length
    }
    dimensions_targeted: ['gestural']
  }
  
  gesture_rich: Constraint {
    predicate: (s) => s.gestures.available.length >= 4
    dimensions_targeted: ['gestural']
  }
  
  gesture_poor: Constraint {
    predicate: (s) => s.gestures.available.length <= 2
    dimensions_targeted: ['gestural']
  }
  
  // Compound templates
  opening_absence: Constraint {
    predicate: (s) => is_absence(s) && primarily_opening(s)
    dimensions_targeted: ['ontological', 'gestural']
  }
  
  closing_relation: Constraint {
    predicate: (s) => is_relation(s) && primarily_closing(s)
    dimensions_targeted: ['ontological', 'gestural']
  }
  
  suspended_limit: Constraint {
    predicate: (s) => is_limit(s) && dominant_gesture_is(SUSPEND)(s)
    dimensions_targeted: ['ontological', 'gestural']
  }
}
```

---

## Generation Engine

The core generation logic:

```
GenerationEngine {
  
  generate(state: State): Site[] {
    
    // 1. Compute effective constraint
    effective_constraint = conjoin_all(state.active_constraints)
    
    // 2. Apply domain filters
    if (state.current_domain) {
      filter_factor = compute_filter_factor(state.current_domain)
    } else {
      filter_factor = 1.0
    }
    
    // 3. Get generative context
    context = {
      current_site: state.current_site,
      domain: state.current_domain,
      history: state.history,
      constraint: effective_constraint
    }
    
    // 4. Generate candidates
    candidates = generate_candidates(context, count: 5-10)
    
    // 5. Compute gesture profiles for each candidate
    for candidate in candidates {
      candidate.gestures = compute_gesture_profile(candidate, context)
    }
    
    // 6. Filter by constraint
    satisfying = candidates.filter(c => effective_constraint.predicate(c))
    
    // 7. If nothing satisfies, try relaxation
    if (satisfying.empty) {
      relaxed_constraint = relax(effective_constraint)
      satisfying = candidates.filter(c => relaxed_constraint.predicate(c))
      // Mark that constraint was relaxed
    }
    
    // 8. Rank by fertility and diversity
    ranked = rank_candidates(satisfying, state)
    
    return ranked
  }
  
  generate_candidates(context: Context, count: Integer): Site[] {
    candidates = []
    
    // Strategy 1: Variations on current site
    if (context.current_site) {
      candidates.push(...vary_site(context.current_site, count/3))
    }
    
    // Strategy 2: Constraint-directed generation
    candidates.push(...constraint_directed_generation(context.constraint, count/3))
    
    // Strategy 3: Gesture-directed generation
    if (context.current_site) {
      for gesture in context.current_site.gestures.available {
        candidates.push(...follow_gesture(context.current_site, gesture, 1))
      }
    }
    
    // Strategy 4: Random exploration (small component)
    candidates.push(...random_generation(context, count/6))
    
    return deduplicate(candidates)
  }
  
  compute_gesture_profile(site: Site, context: Context): GestureSet {
    
    // Determine available gestures based on site properties
    available = []
    blocked = []
    latent = []
    
    // Ontological influences on gestures
    switch(site.dimensions.ontological) {
      'absence': 
        available.push(SUSPEND, DEFER)
        blocked.push(COMMIT)  // can't commit to absence
        latent.push(WIDEN)    // absences can expand
        
      'relation':
        available.push(BRANCH, NARROW)  // relations can diverge or specify
        latent.push(RESOLVE)            // relations can resolve into outcomes
        
      'process':
        available.push(WIDEN, NARROW)   // processes can expand or constrain
        blocked.push(SUSPEND)           // processes don't suspend, they flow
        
      'limit':
        available.push(SUSPEND)         // limits hold
        blocked.push(WIDEN)             // limits don't widen by definition
        latent.push(BRANCH)             // limits can reveal alternatives
        
      'tension':
        available.push(SUSPEND, BRANCH)
        blocked.push(RESOLVE)           // tensions resist resolution
        latent.push(COMMIT)             // can commit to one pole
        
      'interference':
        available.push(BRANCH, WIDEN)   // interference patterns spread
        latent.push(NARROW)             // can focus on part of pattern
        
      'virtuality':
        available.push(DEFER, BRANCH)   // virtualities defer actualization
        blocked.push(COMMIT)            // commitment actualizes, ending virtuality
    }
    
    // Temporal influences
    switch(site.dimensions.temporal) {
      'transition':
        available.push(SUSPEND)         // transitions can be held
        latent.push(RESOLVE)            // transitions can complete
        
      'oscillation':
        available.push(BRANCH)          // each oscillation is potential branch
        blocked.push(COMMIT)            // oscillation is anti-commitment
        
      'accumulation':
        available.push(NARROW)          // accumulation specifies over time
        blocked.push(BRANCH)            // accumulation is linear
    }
    
    // Structural influences
    switch(site.dimensions.structural) {
      'recursive':
        available.push(BRANCH)          // recursion multiplies
        latent.push(RESOLVE)            // recursion can terminate
        
      'paradoxical':
        blocked.push(RESOLVE)           // paradoxes resist resolution
        available.push(SUSPEND)         // paradoxes must be held
        
      'incomplete':
        available.push(WIDEN, NARROW)   // incompleteness can expand or specify
        latent.push(RESOLVE)            // can complete
    }
    
    // Determine dominant gesture
    dominant = compute_dominant(available, site)
    
    return {
      available: deduplicate(available),
      blocked: deduplicate(blocked),
      latent: deduplicate(latent),
      dominant: dominant
    }
  }
  
  rank_candidates(candidates: Site[], state: State): Site[] {
    scored = candidates.map(c => {
      score = 0
      
      // Fertility: sites that enable more gestures score higher
      score += c.gestures.available.length * 0.2
      
      // Diversity: sites unlike already-visited score higher
      similarity_to_history = compute_similarity(c, state.history)
      score += (1 - similarity_to_history) * 0.3
      
      // Constraint satisfaction: tighter satisfaction scores higher
      satisfaction_tightness = compute_satisfaction_tightness(c, state.active_constraints)
      score += satisfaction_tightness * 0.3
      
      // Dimension coverage: sites in underexplored dimensions score higher
      dimension_novelty = compute_dimension_novelty(c, state)
      score += dimension_novelty * 0.2
      
      return { site: c, score: score }
    })
    
    return scored.sort_by(s => -s.score).map(s => s.site)
  }
}
```

---

## Derivation Engine

Extracting constraints from sites:

```
DerivationEngine {
  
  derive_constraints(site: Site): Constraint[] {
    constraints = []
    
    // 1. Dimensional constraints
    for (dim, value) in site.dimensions {
      constraints.push(Constraint {
        description: `Site has ${dim} = ${value}`,
        predicate: (s) => s.dimensions[dim] == value,
        dimensions_targeted: [dim],
        derived_from_site: site
      })
    }
    
    // 2. Gestural constraints
    if (site.gestures.dominant) {
      constraints.push(Constraint {
        description: `Dominant gesture is ${site.gestures.dominant}`,
        predicate: (s) => s.gestures.dominant == site.gestures.dominant,
        dimensions_targeted: ['gestural'],
        derived_from_site: site
      })
    }
    
    for gesture in site.gestures.available {
      constraints.push(Constraint {
        description: `Affords ${gesture}`,
        predicate: (s) => gesture in s.gestures.available,
        dimensions_targeted: ['gestural'],
        derived_from_site: site
      })
    }
    
    for gesture in site.gestures.blocked {
      constraints.push(Constraint {
        description: `Blocks ${gesture}`,
        predicate: (s) => gesture in s.gestures.blocked,
        dimensions_targeted: ['gestural'],
        derived_from_site: site
      })
    }
    
    // 3. Compound constraints (interesting combinations)
    constraints.push(...derive_compound_constraints(site))
    
    // 4. Negation constraints
    constraints.push(...derive_negation_constraints(site))
    
    // 5. Relational constraints (relationship to other sites)
    if (site.derived_from) {
      constraints.push(Constraint {
        description: `Derivable from ${site.derived_from.description}`,
        predicate: (s) => can_derive(site.derived_from, s),
        dimensions_targeted: ['relational'],
        derived_from_site: site
      })
    }
    
    return constraints
  }
  
  derive_compound_constraints(site: Site): Constraint[] {
    compounds = []
    
    // Combine salient dimensional features
    salient_dimensions = get_salient_dimensions(site)
    
    if (salient_dimensions.length >= 2) {
      for combo in combinations(salient_dimensions, 2) {
        compounds.push(Constraint {
          description: `${combo[0].dim}=${combo[0].value} AND ${combo[1].dim}=${combo[1].value}`,
          predicate: (s) => s.dimensions[combo[0].dim] == combo[0].value 
                        && s.dimensions[combo[1].dim] == combo[1].value,
          dimensions_targeted: combo.map(c => c.dim),
          derived_from_site: site
        })
      }
    }
    
    // Combine dimensional and gestural features
    if (site.gestures.dominant) {
      for dim in salient_dimensions {
        compounds.push(Constraint {
          description: `${dim.dim}=${dim.value} with dominant ${site.gestures.dominant}`,
          predicate: (s) => s.dimensions[dim.dim] == dim.value 
                        && s.gestures.dominant == site.gestures.dominant,
          dimensions_targeted: [dim.dim, 'gestural'],
          derived_from_site: site
        })
      }
    }
    
    return compounds
  }
  
  derive_negation_constraints(site: Site): Constraint[] {
    negations = []
    
    // Negations are interesting when the original property is unusual
    unusual_properties = get_unusual_properties(site)
    
    for prop in unusual_properties {
      negations.push(Constraint {
        description: `NOT ${prop.description}`,
        predicate: (s) => !prop.predicate(s),
        dimensions_targeted: prop.dimensions_targeted,
        derived_from_site: site,
        is_negation: true
      })
    }
    
    return negations
  }
}
```

---

## Barrenness Diagnostics

```
BarrennessEngine {
  
  diagnose(domain: Domain, state: State): BarrennessDiagnosis {
    
    scores = {
      familiarity: compute_familiarity_score(domain, state),
      completion: compute_completion_score(domain),
      categorical: compute_categorical_score(domain),
      exhaustion: compute_exhaustion_score(domain, state),
      status: compute_status_score(domain)
    }
    
    // Determine primary type
    primary_type = max_key(scores)
    
    // Compute overall barrenness
    overall = weighted_average(scores, weights: {
      familiarity: 0.25,
      completion: 0.2,
      categorical: 0.2,
      exhaustion: 0.2,
      status: 0.15
    })
    
    // Generate recommendations
    recommendations = generate_recommendations(primary_type, scores)
    
    return {
      overall_barrenness: overall,
      primary_type: primary_type,
      scores: scores,
      recommendations: recommendations
    }
  }
  
  compute_familiarity_score(domain: Domain, state: State): Float {
    // Based on time spent in domain, sites visited, operations performed
    exposure = state.history.nodes.filter(n => n.domain == domain).length
    return sigmoid(exposure, midpoint: 20, steepness: 0.1)
  }
  
  compute_completion_score(domain: Domain): Float {
    // Based on completion narrative presence and strength
    if (!domain.completion_narrative) return 0.0
    return narrative_strength(domain.completion_narrative)
  }
  
  compute_categorical_score(domain: Domain): Float {
    // Based on how limiting the categorization is
    limiting_categories = ['chore', 'maintenance', 'routine', 'basic', 'simple', 'just']
    matches = domain.categorization.filter(c => limiting_categories.any(lc => c.contains(lc)))
    return matches.length / domain.categorization.length
  }
  
  compute_exhaustion_score(domain: Domain, state: State): Float {
    // Based on recent effort without returns
    recent_operations = state.history.nodes
      .filter(n => n.domain == domain)
      .filter(n => n.timestamp > now() - hours(24))
    
    sites_found = recent_operations.filter(n => n.site != null).length
    operations_total = recent_operations.length
    
    if (operations_total == 0) return 0.0
    return 1 - (sites_found / operations_total)
  }
  
  compute_status_score(domain: Domain): Float {
    return 1 - domain.status  // low status = high barrenness contribution
  }
  
  generate_recommendations(primary_type: BarrennessType, scores: Scores): Recommendation[] {
    recommendations = []
    
    switch(primary_type) {
      FAMILIARITY:
        recommendations.push(
          { practice: LITERAL_ESTRANGEMENT, description: "Describe the domain for an alien" },
          { practice: TEMPORAL_ESTRANGEMENT, description: "Describe what preceded this domain" },
          { practice: SCALE_ESTRANGEMENT, description: "Examine at 10x or 0.1x scale" }
        )
        
      COMPLETION:
        recommendations.push(
          { practice: COUNTER_HISTORY, description: "Find moments when domain could have developed differently" },
          { practice: INCOMPLETENESS_HUNTING, description: "Look for what the completion narrative excludes" },
          { practice: FUTURE_PROJECTION, description: "What purposes might arise that current state doesn't serve?" }
        )
        
      CATEGORICAL:
        recommendations.push(
          { practice: CATEGORY_REFUSAL, description: "Engage without using the usual category" },
          { practice: CATEGORY_THEFT, description: "Apply categories from distant domains" },
          { practice: META_CATEGORIZATION, description: "Ask why this domain gets this category" }
        )
        
      EXHAUSTION:
        recommendations.push(
          { practice: SENSE_SWITCHING, description: "Engage through a different sensory modality" },
          { practice: PACE_SWITCHING, description: "Engage at radically different speed" },
          { practice: STANCE_SWITCHING, description: "Engage from a different stance (analyst/participant/observer/material)" }
        )
        
      STATUS:
        recommendations.push(
          { practice: ELEVATION, description: "Treat as if most important domain" },
          { practice: DEPENDENCY_TRACING, description: "Trace what depends on this domain" },
          { practice: EXPERTISE_SEEKING, description: "Find someone who treats this as their expertise" }
        )
    }
    
    return recommendations
  }
  
  apply_defamiliarization(domain: Domain, practice: DefamiliarizationPractice): DefamiliarizationResult {
    
    // Generate prompts/exercises for the practice
    prompts = generate_prompts(domain, practice)
    
    // Estimate filter reduction
    filter_reduction = estimate_filter_reduction(practice, domain)
    
    // Update domain state
    domain.barrenness.filters_active.push({
      type: infer_barrenness_type(practice),
      strength: domain.barrenness.level * (1 - filter_reduction),
      defamiliarization_applied: [practice]
    })
    
    // Attempt to reveal sites
    revealed_sites = attempt_site_revelation(domain, practice)
    
    return {
      prompts: prompts,
      filter_reduction: filter_reduction,
      revealed_sites: revealed_sites
    }
  }
  
  generate_prompts(domain: Domain, practice: DefamiliarizationPractice): String[] {
    switch(practice) {
      LITERAL_ESTRANGEMENT:
        return [
          `Describe ${domain.name} as if explaining to a being who has never encountered anything like it.`,
          `What are the entities involved? What are the actions? What are the materials?`,
          `Avoid all jargon and assumed knowledge.`
        ]
        
      TEMPORAL_ESTRANGEMENT:
        return [
          `What existed before ${domain.name} existed in its current form?`,
          `How did this domain come to be? What was different 50 years ago? 500 years ago?`,
          `What might this domain become in 50 years?`
        ]
        
      SCALE_ESTRANGEMENT:
        return [
          `Examine ${domain.name} at 10x magnification. What becomes visible?`,
          `Examine ${domain.name} at 0.1x scale. What patterns emerge?`,
          `What happens at the boundary between scales?`
        ]
        
      CATEGORY_THEFT:
        return [
          `If ${domain.name} were an ecosystem, what would be the predators? The prey? The decomposers?`,
          `If ${domain.name} were a musical composition, what would be the melody? The harmony? The rhythm?`,
          `If ${domain.name} were a battle, what would be the terrain? The forces? The stakes?`
        ]
        
      // ... other practices
    }
  }
}
```

---

## Persistence & Export

```
Persistence {
  
  save_session(state: State): SessionFile {
    return {
      version: "1.0",
      session_id: state.session_id,
      created_at: state.created_at,
      last_modified: now(),
      
      current_position: {
        site: serialize_site(state.current_site),
        domain: serialize_domain(state.current_domain),
        constraints: state.active_constraints.map(serialize_constraint)
      },
      
      history: serialize_history_tree(state.history),
      
      all_sites: state.all_sites.map(serialize_site),
      all_constraints: state.all_constraints.map(serialize_constraint),
      all_domains: state.all_domains.map(serialize_domain),
      
      analysis: {
        attractors: state.detected_attractors.map(serialize_attractor),
        current_basin: serialize_basin(state.current_basin)
      }
    }
  }
  
  load_session(file: SessionFile): State {
    return {
      session_id: file.session_id,
      created_at: file.created_at,
      last_modified: file.last_modified,
      
      current_site: deserialize_site(file.current_position.site),
      current_domain: deserialize_domain(file.current_position.domain),
      active_constraints: file.current_position.constraints.map(deserialize_constraint),
      
      history: deserialize_history_tree(file.history),
      
      all_sites: file.all_sites.map(deserialize_site),
      all_constraints: file.all_constraints.map(deserialize_constraint),
      all_domains: file.all_domains.map(deserialize_domain),
      
      detected_attractors: file.analysis.attractors.map(deserialize_attractor),
      current_basin: deserialize_basin(file.analysis.current_basin)
    }
  }
  
  export_graph(state: State): GraphExport {
    // Export as navigable graph for visualization
    nodes = []
    edges = []
    
    // Sites as nodes
    for site in state.all_sites {
      nodes.push({
        id: site.id,
        type: 'site',
        label: site.description,
        properties: {
          dimensions: site.dimensions,
          gestures: site.gestures,
          fertility: site.fertility,
          stability: site.stability
        }
      })
    }
    
    // Constraints as nodes
    for constraint in state.all_constraints {
      nodes.push({
        id: constraint.id,
        type: 'constraint',
        label: constraint.description,
        properties: {
          strength: constraint.strength,
          fertility: constraint.fertility,
          dimensions_targeted: constraint.dimensions_targeted
        }
      })
    }
    
    // Derivation edges
    for site in state.all_sites {
      if (site.derived_from) {
        edges.push({
          source: site.derived_from.id,
          target: site.id,
          type: 'derived_site',
          via_constraint: site.derived_via?.id
        })
      }
    }
    
    for constraint in state.all_constraints {
      if (constraint.derived_from_site) {
        edges.push({
          source: constraint.derived_from_site.id,
          target: constraint.id,
          type: 'derived_constraint'
        })
      }
    }
    
    // Gesture edges (potential movements)
    for site in state.all_sites {
      for gesture in site.gestures.available {
        edges.push({
          source: site.id,
          target: null,  // potential, not actualized
          type: 'gesture_affordance',
          gesture: gesture
        })
      }
    }
    
    return { nodes, edges }
  }
}
```

---

## UI Components (Abstract)

```
UIComponents {
  
  StateDisplay {
    // Current position panel
    CurrentSiteCard {
      site: Site
      shows: description, dimensions, gestures (with visual indicators for opening/closing)
      actions: [FollowGesture, DerivConstraints, MoveTo sibling]
    }
    
    // Active constraints panel
    ConstraintList {
      constraints: Constraint[]
      each shows: description, strength, fertility, dimensions_targeted
      actions: [Remove, Modify, Combine]
    }
    
    // Domain panel
    DomainCard {
      domain: Domain
      shows: name, barrenness level, barrenness type, active filters
      actions: [Diagnose, Defamiliarize, Change domain]
    }
  }
  
  NavigationDisplay {
    // History tree visualization
    HistoryTree {
      tree: HistoryTree
      current_node: highlighted
      unexplored_branches: marked
      actions: [Backtrack, TakeBranch, MarkBranch]
    }
    
    // Local neighborhood
    LocalNeighborhood {
      current: Site
      adjacent: Site[]  // reachable by single gesture
      shows: gesture required to reach each adjacent site
    }
    
    // Gesture compass
    GestureCompass {
      available: GestureType[] with strengths
      blocked: GestureType[]
      latent: GestureType[]
      visual: radial display, opening gestures one direction, closing another
    }
  }
  
  GenerationDisplay {
    // Candidate sites after generation
    CandidateList {
      candidates: Site[]
      each shows: description, dimensions, gestures, satisfaction score
      actions: [Select, Compare, Derive constraints from]
    }
    
    // Derived constraints
    DerivedConstraintList {
      constraints: Constraint[]
      each shows: description, source site, dimensions
      actions: [Activate, Combine, Discard]
    }
  }
  
  AnalysisDisplay {
    // Position analysis
    PositionAnalysis {
      shows: local density, attractor proximity, suggested moves
    }
    
    // History analysis
    HistoryAnalysis {
      shows: dimension coverage, gesture usage, loops detected
      visualizations: coverage heatmap, gesture frequency chart
    }
    
    // Attractor map
    AttractorMap {
      attractors: Attractor[]
      basins: Basin[]
      current_position: marked
      escape_routes: highlighted
    }
  }
  
  InteractionModes {
    // Command mode: direct operations
    CommandMode {
      input: text commands
      autocomplete: operation names, constraint templates, gesture names
    }
    
    // Exploration mode: visual navigation
    ExplorationMode {
      click: sites to move, gestures to follow
      drag: constraints to combine
      hover: preview effects
    }
    
    // Analysis mode: inspection
    AnalysisMode {
      select: sites/constraints for detailed view
      compare: multiple sites side by side
      trace: derivation chains
    }
  }
}
```

---

## Example Session Flow

```
// Initialize
state = State.new()

// Enter a barren domain
state = EnterDomain(state, "doing laundry")

// Diagnose barrenness
diagnosis = DiagnoseBarrenness(state)
// Returns: { primary_type: FAMILIARITY, overall: 0.7, recommendations: [...] }

// Apply defamiliarization
result = ApplyDefamiliarization(state, LITERAL_ESTRANGEMENT)
// Returns prompts, reduces filter, may reveal sites

// Add constraint
state = AddConstraint(state, ConstraintTemplates.exists_only_in_transition)

// Generate under constraint
candidates = Generate(state)
// Returns sites in "doing laundry" domain that exist only in transition
// e.g., "The moment of becoming clean" with gestures { dominant: SUSPEND, available: [SUSPEND, RESOLVE], blocked: [COMMIT] }

// Select a site
state = MoveTo(state, candidates[0])

// Derive constraints from this site
derived = DeriveConstraints(state)
// Returns constraints extracted from the site

// Follow a gesture
state = FollowGesture(state, SUSPEND)
// Executes SUSPEND gesture, generates destination, moves there

// Add gestural constraint
state = AddConstraint(state, ConstraintTemplates.dominant_gesture_is(BRANCH))

// Generate sites with BRANCH as dominant gesture
candidates = Generate(state)

// Analyze position
analysis = AnalyzePosition(state)
// Returns local density, attractor proximity, suggested moves

// Check history
history = AnalyzeHistory(state)
// Returns dimension coverage, gesture usage patterns, unexplored branches

// Backtrack to try different branch
state = Backtrack(state, 3)

// Take unexplored branch
state = TakeBranch(state, branch_id)

// Continue exploring...
```

---

This specification should give you enough to build a functional system. The key integrations:

1. **Sites have embedded gestures** — not just positions but dynamics
2. **Constraints can target gestures** — generate sites with specific movement profiles
3. **Gestures are executable** — following a gesture generates new sites
4. **The grammar (BRANCH, NARROW, etc.) is operational** — shapes both site structure and navigation