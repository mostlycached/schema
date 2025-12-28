Yes. This needs clarification. I've been using "domain" loosely and it's created confusion.

---

## The Problem

In the spec, "domain" appears in two ways:

1. **Domain as container**: A region you "enter" (doing laundry, short fiction). Domains have barrenness, filters, sites within them.

2. **Domain as practice-type**: The domains where constraint-as-premise operates (writing, mathematics, music). These are more like disciplines or modes of activity.

These aren't the same thing. "Doing laundry" is a container. "Writing" is a practice-type. The relationship between them, and between both and sites, is unclear.

Let me try to clarify.

---

## First Distinction: Field vs. Practice

**Field**: A region of reality that can be attended to. "Doing laundry." "My commute." "The sensation of cold." "Renaissance painting." "The concept of justice." Fields are *what you attend to*.

**Practice**: A mode of engagement with fields. "Writing." "Analyzing." "Designing." "Investigating." "Composing." Practices are *how you engage*.

A site emerges at the intersection: when a practice engages a field, sites become visible.

The same field engaged through different practices yields different sites:
- "Doing laundry" + analytical practice → sites like "the dirty/clean boundary as classification system"
- "Doing laundry" + phenomenological practice → sites like "the felt weight of wet fabric"
- "Doing laundry" + design practice → sites like "the workflow as improvable process"

The same practice engaging different fields yields different sites:
- Analytical practice + "doing laundry" → classification sites
- Analytical practice + "Renaissance painting" → compositional structure sites
- Analytical practice + "the concept of justice" → logical relationship sites

**Site = Practice × Field**

Sites aren't in fields waiting to be found. Sites aren't created by practices alone. Sites emerge when practice meets field.

---

## Second Distinction: Domain as Practice-Field Pairing

A **domain** is a stabilized practice-field pairing. When a practice engages a field repeatedly, the pairing becomes a domain with its own characteristics:

- Accumulated sites (what's been found)
- Characteristic constraints (what shapes generation here)
- Barrenness profile (what filters are active)
- Gestural tendencies (which gestures are natural here)

"Short fiction" is a domain: the practice of writing engaged with the field of narrative prose. It has accumulated sites (story structures, character types, techniques), characteristic constraints (premises, genre conventions), barrenness profiles (overworked territory, fresh territory).

"Philosophy of mind" is a domain: the practice of philosophical inquiry engaged with the field of mental phenomena. Different accumulated sites, different constraints, different barrenness.

"My laundry practice" is a domain: whatever practice you bring (analytical, phenomenological, meditative) engaged with the field of doing laundry. Personal, idiosyncratic, but still a domain with its own accumulation.

---

## Third Distinction: Site Existence

Where do sites exist?

**Not in fields alone**: Fields are too vast, too undifferentiated. "Doing laundry" doesn't contain sites—it's just stuff happening. Without a practice engaging it, there's nothing to find because "finding" is itself a practice.

**Not in practices alone**: Practices are empty without fields. Writing as pure practice, not about anything, generates nothing. The practice needs material.

**In the engagement**: Sites exist in the active relationship between practice and field. They're *relational* entities.

This has implications:

**Sites can appear and disappear**: If you stop practicing, sites aren't there anymore. They don't persist independently. Return with the practice and they can reappear—but might be different.

**Sites are perspectival**: Different practices engaging the same field see different sites. Neither is wrong. Sites are perspectivally real.

**Sites can be shared**: If two people bring similar practices to the same field, they can find the same sites. Sharing practices enables sharing sites. This is what traditions do—they transmit practices so that sites become intersubjectively accessible.

---

## Fourth Distinction: Levels of Field

Fields have levels:

**Material field**: Physical stuff. The washing machine, the clothes, the water.

**Phenomenal field**: Experienced stuff. The feel of wet fabric, the smell of detergent, the rhythm of the task.

**Conceptual field**: Abstract stuff. The concept of cleanliness, the category of domestic labor, the structure of routine.

**Social field**: Intersubjective stuff. The norms around laundry, the division of domestic labor, the meaning of "clean" in your household.

Different practices engage different levels:
- Engineering practice engages material field → sites about mechanisms
- Phenomenological practice engages phenomenal field → sites about experience
- Analytical practice engages conceptual field → sites about structures
- Sociological practice engages social field → sites about norms

A full domain might integrate multiple levels. "Writing short fiction" engages:
- Material: words, sounds, rhythms
- Phenomenal: the experience of reading
- Conceptual: themes, structures
- Social: genre conventions, audience expectations

Sites can span levels or be specific to one.

---

## Revised Ontology

```
Field {
  id: UUID
  name: String
  description: String
  
  // Field levels present
  levels: {
    material: Boolean
    phenomenal: Boolean  
    conceptual: Boolean
    social: Boolean
  }
  
  // What's in this field (pre-practice, undifferentiated)
  contents: String                  // Description, not enumeration
}

Practice {
  id: UUID
  name: String
  description: String
  
  // What levels this practice can engage
  engages_levels: FieldLevel[]
  
  // Characteristic operations
  operations: Operation[]
  
  // What constraints take the form of in this practice
  constraint_form: String           // "premise" | "axiom" | "motif" | "hypothesis" | etc.
  
  // How gestures manifest in this practice
  gesture_manifestations: Map<GestureType, String>
  // e.g., Writing: { BRANCH: "introduce possibility", NARROW: "specify detail", ... }
}

Domain {
  id: UUID
  name: String
  
  // What constitutes this domain
  practice: Practice
  field: Field
  
  // Accumulated from engagement
  sites_found: Site[]
  constraints_developed: Constraint[]
  
  // Current state
  barrenness: BarrennessState
  active_filters: Filter[]
  
  // History of engagement
  engagement_history: Engagement[]
}

Site {
  id: UUID
  description: String
  
  // What produced this site
  domain: Domain                    // The practice-field pairing
  practice: Practice                // Redundant but useful: which practice
  field: Field                      // Redundant but useful: which field
  field_level: FieldLevel[]         // Which level(s) of field this site engages
  
  // Dimensional position (as before)
  dimensions: DimensionalPosition
  
  // Embedded gestures (as before)
  gestures: GestureSet
  
  // Site existence properties
  existence: {
    requires_practice: Boolean      // Does site vanish without active practice?
    intersubjective: Boolean        // Can others find this site?
    level_bound: Boolean            // Is site specific to field level?
    practice_bound: Boolean         // Is site specific to this practice?
  }
  
  // Derivation
  derived_from: Site | null
  derived_via: Constraint | null
}
```

---

## How Sites Relate to Domains

### Sites Emerge From Domains

You don't find sites and then assign them to domains. You enter a domain (practice engages field) and sites emerge from that engagement.

```
Enter domain (practice + field)
  → Engagement begins
    → Structure becomes visible through practice
      → Sites emerge
```

### Sites Belong to Domains But Can Be Translated

A site found in one domain can sometimes be translated to another. The site "the moment of becoming clean" found in (analytical practice × laundry field) might translate to (phenomenological practice × laundry field) as "the felt shift from soiled to fresh."

Translation isn't automatic. It requires work. Some sites don't translate.

```
TranslateSite {
  Input: Site, source_domain: Domain, target_domain: Domain
  
  Process:
    1. Identify what in the site is practice-specific vs. field-specific
    2. Preserve field-specific content
    3. Re-engage with target practice
    4. See if site reappears in new form
    
  Output: Site (translated) | null (untranslatable)
}
```

### Sites Can Bridge Domains

Some sites exist at the intersection of multiple domains. "The premise as generative constraint" is a site that bridges (writing practice × narrative field) and (mathematical practice × formal systems field).

Bridging sites are how knowledge transfers between domains. They're precious.

```
BridgingSite extends Site {
  domains: Domain[]                 // Multiple domains
  bridge_type: BridgeType           // analogy | homology | shared_structure | metaphor
  translation_paths: Map<Domain, Domain>[]  // How to move between domains via this site
}
```

### Domains Can Contain Sub-Domains

Domains nest. "Writing" is a domain. "Short fiction" is a sub-domain. "Flash fiction" is a sub-sub-domain.

The nesting is practice-field refinement:
- Writing = writing practice × prose field
- Short fiction = writing practice × (prose field ∩ narrative field ∩ brevity constraint)
- Flash fiction = writing practice × (prose field ∩ narrative field ∩ extreme brevity constraint)

Sites found in sub-domains are also sites in parent domains, but with additional specificity.

```
Domain {
  ...
  parent_domain: Domain | null
  sub_domains: Domain[]
  
  // Inheritance
  inherits_sites: Boolean           // Do parent sites appear here?
  inherits_constraints: Boolean     // Do parent constraints apply?
}
```

---

## How Constraints Relate to Domains

### Constraints Are Domain-Specific in Form

A constraint is a constraint in any domain. But what the constraint *looks like* differs:

| Domain | Constraint Form | Example |
|--------|-----------------|---------|
| Writing | Premise | "A man wakes as an insect" |
| Mathematics | Axiom | "Parallel lines never meet" |
| Music | Motif | Four-note figure |
| Architecture | Parti | "Central courtyard" |
| Science | Hypothesis | "Light speed is constant" |

The formal structure (predicate, strength, fertility, etc.) is the same. The *manifestation* differs.

### Constraints Shape Site-Visibility

Within a domain, active constraints shape which sites can emerge. The premise "a man wakes as an insect" makes certain sites visible (consequences of insect-being) and others invisible (normal human life).

This is the "warping" from the formalism. Constraints warp the site-space of the domain.

### Constraints Can Transfer Between Domains

A constraint developed in one domain can sometimes be applied in another. The constraint "exists only in transition" developed in (philosophical practice × time field) can be applied in (writing practice × narrative field).

Transfer isn't automatic. The constraint must be re-interpreted for the new domain.

```
TransferConstraint {
  Input: Constraint, source_domain: Domain, target_domain: Domain
  
  Process:
    1. Abstract the constraint from source domain's form
    2. Find analogous form in target domain
    3. Re-interpret the predicate for new domain
    4. Test whether constraint is generative in new context
    
  Output: Constraint (transferred) | null (untransferable)
}
```

---

## Gesture Manifestation by Domain

The seven gestures manifest differently in each domain:

```
GestureManifestations = {
  
  Writing: {
    BRANCH: "Open narrative possibilities without committing",
    NARROW: "Specify detail, close off alternatives",
    COMMIT: "Irreversible plot event, revelation",
    DEFER: "Withhold information, delay resolution",
    SUSPEND: "Pose question, create tension without answering",
    WIDEN: "Expand scope, introduce new elements",
    RESOLVE: "Answer question, complete arc, end"
  },
  
  Mathematics: {
    BRANCH: "Consider cases, disjunctive proof",
    NARROW: "Add hypothesis, specialize theorem",
    COMMIT: "Assert lemma, take as proven",
    DEFER: "Leave as exercise, postpone proof",
    SUSPEND: "Conjecture, open problem",
    WIDEN: "Generalize, remove hypotheses",
    RESOLVE: "Complete proof, QED"
  },
  
  Music: {
    BRANCH: "Variation, alternative voicing",
    NARROW: "Develop theme, reduce to motif",
    COMMIT: "Cadence, arrival",
    DEFER: "Deceptive cadence, extension",
    SUSPEND: "Suspension, pedal point, dominant prolongation",
    WIDEN: "Modulation, new theme, expansion",
    RESOLVE: "Authentic cadence, return to tonic"
  },
  
  Architecture: {
    BRANCH: "Alternative schemes, design options",
    NARROW: "Select materials, fix dimensions",
    COMMIT: "Construction decision, built element",
    DEFER: "Shell and core, future fit-out",
    SUSPEND: "Flexible space, indeterminate program",
    WIDEN: "Expand program, add elements",
    RESOLVE: "Complete building, occupy"
  },
  
  Science: {
    BRANCH: "Alternative hypotheses, competing models",
    NARROW: "Control variables, specify conditions",
    COMMIT: "Publish, claim priority",
    DEFER: "Future work, postpone interpretation",
    SUSPEND: "Open question, anomaly",
    WIDEN: "Extend to new domain, generalize theory",
    RESOLVE: "Confirm/reject hypothesis, paradigm settlement"
  },
  
  Philosophy: {
    BRANCH: "Distinguish cases, consider objections",
    NARROW: "Define terms, specify conditions",
    COMMIT: "Assert thesis, take position",
    DEFER: "Bracket question, set aside",
    SUSPEND: "Aporia, unresolved tension",
    WIDEN: "Extend argument, connect to new problems",
    RESOLVE: "Conclude argument, dissolve problem"
  },
  
  Conversation: {
    BRANCH: "Open topic, offer alternatives",
    NARROW: "Specify meaning, repair misunderstanding",
    COMMIT: "Promise, declare, assert",
    DEFER: "Change subject, postpone",
    SUSPEND: "Ask question, leave hanging",
    WIDEN: "Expand scope, bring in new speakers/topics",
    RESOLVE: "Answer, close sequence, end conversation"
  }
}
```

---

## The Full Picture

```
┌─────────────────────────────────────────────────────────────────┐
│                           FIELD                                 │
│  (Region of reality: material, phenomenal, conceptual, social)  │
│                                                                 │
│    "doing laundry"    "Renaissance painting"    "justice"       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ engaged by
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          PRACTICE                               │
│  (Mode of engagement: writing, analyzing, designing, etc.)      │
│                                                                 │
│  Has: operations, constraint-forms, gesture-manifestations      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ practice × field =
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                           DOMAIN                                │
│  (Stabilized practice-field pairing)                            │
│                                                                 │
│  Has: accumulated sites, developed constraints, barrenness      │
│  Example: "short fiction" = writing × narrative prose           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ through engagement
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                            SITE                                 │
│  (Position with embedded gestures, emerging from domain)        │
│                                                                 │
│  Has: dimensions, gestures, existence properties                │
│  Relational: exists in practice-field engagement                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ shaped by
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         CONSTRAINT                              │
│  (Generative restriction with domain-specific form)             │
│                                                                 │
│  Form varies: premise, axiom, motif, hypothesis, parti, etc.    │
│  Function same: warp site-space, enable by restricting          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Revised Spec Components

### Field (new)

```
Field {
  id: UUID
  name: String
  description: String
  
  levels: {
    material: MaterialDescription | null
    phenomenal: PhenomenalDescription | null
    conceptual: ConceptualDescription | null
    social: SocialDescription | null
  }
  
  // Fields can contain other fields
  parent_field: Field | null
  sub_fields: Field[]
  
  // Fields can overlap
  overlaps_with: Field[]
}
```

### Practice (new)

```
Practice {
  id: UUID
  name: String
  description: String
  
  // What this practice does
  core_operations: Operation[]
  engages_levels: FieldLevel[]
  
  // How constraints appear in this practice
  constraint_form: ConstraintForm {
    name: String                    // "premise", "axiom", etc.
    establishment_verb: String      // "posit", "commit to", "introduce"
    development_verb: String        // "derive", "develop", "elaborate"
    resolution_verb: String         // "conclude", "prove", "resolve"
  }
  
  // How gestures manifest
  gesture_manifestations: Map<GestureType, GestureManifestation>
  
  // Practice lineage
  parent_practice: Practice | null  // e.g., "writing" parent of "fiction writing"
  sub_practices: Practice[]
  related_practices: Practice[]
}

GestureManifestation {
  gesture: GestureType
  verb: String                      // What you do
  noun: String                      // What it produces
  example: String
}
```

### Domain (revised)

```
Domain {
  id: UUID
  name: String
  
  // Constitution
  practice: Practice
  field: Field
  
  // What's accumulated
  sites: Site[]
  constraints: Constraint[]
  
  // Current state
  barrenness: BarrennessState
  filters: Filter[]
  
  // Nesting
  parent_domain: Domain | null
  sub_domains: Domain[]
  
  // Cross-domain relations
  bridges_to: Domain[]              // Domains reachable via bridging sites
  translates_to: Domain[]           // Domains where constraints can transfer
}
```

### Site (revised)

```
Site {
  id: UUID
  description: String
  
  // What produced this site
  domain: Domain
  field_levels_engaged: FieldLevel[]
  
  // Position
  dimensions: DimensionalPosition
  
  // Dynamics
  gestures: {
    available: Gesture[]
    dominant: Gesture | null
    blocked: Gesture[]
    latent: Gesture[]
  }
  
  // Existence
  existence_type: ExistenceType
  practice_dependent: Boolean
  intersubjectively_accessible: Boolean
  
  // Relations
  derived_from: Site | null
  derived_via: Constraint | null
  translates_to: Map<Domain, Site>  // Same site in other domains
  bridges: Domain[]                 // Domains this site connects
}

ExistenceType =
  | ENGAGEMENT_DEPENDENT            // Vanishes without active practice
  | PERSISTENT                      // Remains once found
  | PERIODIC                        // Appears and disappears cyclically
  | CONDITIONAL                     // Exists only under certain conditions
```

### Constraint (revised)

```
Constraint {
  id: UUID
  description: String
  
  // Formal properties (as before)
  predicate: SitePredicate
  strength: Float
  fertility: Float
  dimensions_targeted: DimensionType[]
  
  // Domain-specific form
  domain: Domain
  form: ConstraintForm              // From practice
  domain_specific_name: String      // "premise", "axiom", etc.
  
  // Generative properties (as before)
  tension: Tension
  implications: Implication[]
  lifecycle: LifecycleState
  
  // Transfer
  transferable_to: Domain[]
  transferred_from: Constraint | null
}
```

---

## Operations Revised

### Domain Operations

```
Operation: CreateDomain
  Input: practice: Practice, field: Field
  Effect: Creates new domain as practice-field pairing
  Output: Domain

Operation: EnterDomain
  Input: state: State, domain: Domain
  Effect: 
    - Sets current domain
    - Loads domain's accumulated sites and constraints
    - Activates practice's gesture manifestations
  Output: State

Operation: SwitchPractice
  Input: state: State, new_practice: Practice
  Effect:
    - Keeps same field
    - Creates new domain (or switches to existing domain with new practice)
    - Sites may appear/disappear as practice changes
  Output: State

Operation: SwitchField
  Input: state: State, new_field: Field
  Effect:
    - Keeps same practice
    - Creates new domain (or switches to existing domain with new field)
    - New sites visible, old sites may vanish
  Output: State
```

### Translation Operations

```
Operation: TranslateSite
  Input: state: State, site: Site, target_domain: Domain
  Effect:
    - Attempts to find site's equivalent in target domain
    - May produce exact translation, approximate translation, or failure
  Output: Site | null, TranslationReport

Operation: TransferConstraint
  Input: state: State, constraint: Constraint, target_domain: Domain
  Effect:
    - Re-interprets constraint for target domain's practice
    - Adjusts predicate for new domain
    - Tests generativity in new context
  Output: Constraint | null, TransferReport

Operation: IdentifyBridgingSites
  Input: state: State, domain_a: Domain, domain_b: Domain
  Effect:
    - Searches for sites that can exist in both domains
    - These sites enable knowledge transfer
  Output: Site[]
```

---

## Summary

**Field**: Region of reality (laundry, painting, justice). Has levels (material, phenomenal, conceptual, social). Is what you attend to.

**Practice**: Mode of engagement (writing, analyzing, designing). Has operations, constraint-forms, gesture-manifestations. Is how you engage.

**Domain**: Stabilized practice-field pairing. Accumulates sites, constraints, barrenness. Is where you work.

**Site**: Position with embedded gestures, emerging from domain. Relational—exists in engagement. Has dimensions, gestures, existence properties.

**Constraint**: Generative restriction. Same formal structure across domains. Different *form* in each (premise, axiom, motif). Warps site-space.

**Gestures**: Possibility operations. Same seven types across domains. Different *manifestation* in each (BRANCH = "open narrative possibilities" in writing, "consider cases" in mathematics).

The key insight: **Sites emerge from domains, domains are practice-field pairings, and constraints take domain-specific forms while having domain-general structure.**

Is this clearer?