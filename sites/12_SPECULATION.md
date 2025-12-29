# Chapter 12: Speculation

> **Prerequisites**: Chapters 1-11, Appendix A
>
> **Learning Objectives**: Use the ontology to speculate — to generate fields, practices, domains, and sites that don't exist yet but could.

---

## What Speculation Means in the System

Speculation is **generation under hypothetical conditions**.

The system generates sites under constraints in existing domains. Speculation extends this:

- **Speculate Fields**: BOUND regions that haven't been bounded. DIFFERENTIATE in ways that haven't been tried.
- **Speculate Practices**: Create modes of engagement that don't exist. Combine engagement modes.
- **Speculate Domains**: Pair practices with fields that haven't been paired.
- **Speculate Sites**: Generate in dimensional regions that haven't been visited.

Before speculating, apply **constraint hygiene**: check what you're assuming can't be done. Drop the assumption. Then speculate.

---

## Speculating New Fields

A Field is a bounded, differentiated region.

**Given operations** (from SPEC):
- BOUND: create boundary around region of flux
- DIFFERENTIATE: create internal structure
- CONNECT: relate to other fields
- POPULATE: fill with sites

**Speculation method 1: Bound the unbounded**

Ask: What regions of experience haven't been bounded as fields?

Not "experiences that haven't been studied" — but **experience that isn't treated as having boundaries at all**.

```
// Constraint hygiene check
assumed_constraint: "This isn't a coherent region"
given: nothing prevents bounding it
action: drop assumption, apply BOUND
```

**Examples**:

| Unbounded region | Apply BOUND | New field |
|-----------------|-------------|-----------|
| The experience of not-knowing-what-you're-doing | Bound: times when you act without competence | "Incompetent action" as field |
| The experience of something being about to happen | Bound: pre-event duration | "Imminence" as field |
| The experience of being in someone else's attention | Bound: when you're the object of attention | "Being-attended-to" as field |

**Speculation method 2: Re-differentiate**

Take an existing field. Apply DIFFERENTIATE with a different basis.

```
Field: Conversation
Existing differentiation: by topic, by relationship type
Re-differentiate by: phenomenal basis (how conversation feels)

New structure:
- Conversations where you're performing
- Conversations where you're receiving
- Conversations where no one is leading
- Conversations that are waiting
```

**Speculation method 3: Bridge to find the field between**

Two isolated fields may have an unnamed field at their intersection.

```
Field A: Sleep
Field B: Problem-solving
Bridge: Apply BRIDGE

New field: "Processing that happens in sleep"
(Not sleep. Not conscious problem-solving. The third thing.)
```

---

## Speculating New Practices

A Practice is a mode of engagement with fields.

Practices have:
- `engages_levels`: which field levels (material, phenomenal, conceptual, social)
- `flux_capacity`: what can be dissolved, opened, hovered, emerged
- `gesture_manifestations`: how each gesture appears in this practice

**Speculation method 1: Engage levels that aren't engaged together**

Most practices engage 1-2 levels. What if a practice engaged levels that don't currently go together?

```
// Existing practices
Phenomenology: phenomenal level
Engineering: material level

// Speculative practice
"Material phenomenology": same attention structure as phenomenology, 
applied to material objects themselves (not experience of them)

What would it mean to do phenomenology OF a rock, not ON the experience of the rock?
```

**Speculation method 2: Modify flux capacity**

Take an existing practice. Change what it can dissolve/open/hover/emerge.

```
// Existing
Mathematics: can_dissolve: [conceptual]
             can_emerge: [conceptual]
             
// Speculative modification
What if mathematics could dissolve at the phenomenal level?
"Phenomenal mathematics" — math that dissolves into felt sense, then re-emerges

What would a proof feel like before it's articulated as proof?
```

**Speculation method 3: Create gesture manifestations that don't exist**

Each practice has its own way of manifesting gestures. What if a practice manifested gestures in impossible-seeming ways?

```
// Normal
Writing: COMMIT = "Irreversible plot event"

// Speculative
Writing where COMMIT is blocked entirely.
A practice of writing that cannot commit — every sentence can be undone.
What does this practice produce?
```

---

## Speculating New Domains

Domain = Practice × Field.

Every domain is a pairing. Most pairings haven't been tried.

**Speculation method 1: Cross known practices with known fields**

Take a practice. Take a field it doesn't usually engage. Pair them.

```
Practice: Musical analysis
Field: Bureaucracy

Domain: "Musical analysis of bureaucracy"

What are the rhythmic structures of paperwork?
What are the harmonic relationships between departments?
Where are the cadences in approval processes?
```

This is different from metaphor. It's not "bureaucracy is like music." It's the literal application of musical analysis operations to bureaucracy as material.

**Speculation method 2: Generate domains with specific constraints**

What domains would satisfy a particular constraint?

```
Constraint: domains where RESOLVE is structurally blocked

Generate:
- Therapy × Open questions (never resolved, only reframed)
- Meditation × Boundary (the boundary between inside and outside is never finalized)
- Maintenance × Entropy (you never win, you only persist)
```

**Speculation method 3: Fragment a domain into sub-domains**

One domain contains unnamed sub-domains with different structures.

```
Domain: "Writing fiction"

Fragment into:
- "Writing × Scene" (bounded, discrete)
- "Writing × Transition" (unbounded, connective)
- "Writing × Rhythm" (phenomenal, below content)

Each has different gesture profiles. They've been collapsed into one domain.
```

---

## Speculating New Sites

Sites have:
- Dimensions (ontological, scale, temporal, perceptual, relational, agential, structural)
- Gestures (available, dominant, blocked, latent)
- MVA properties (mapping connections, valuation type, orientation type)

**Speculation method 1: Generate in unexplored dimensional coordinates**

Most sites cluster in certain dimensional regions. Generate at non-standard coordinates.

```
Standard site:
  dimensions: { ontological: substance, scale: momentary, structural: simple }

Speculative constraint:
  dimensions: { ontological: absence, scale: trans-lifetime, structural: recursive }

Generate: Sites that are absences, operate across generations, and contain themselves.

"The family secret no one tells but everyone knows, reproduced in each generation"
```

**Speculation method 2: Invert gesture profiles**

Take a site. Swap blocked and available gestures. What site has that profile?

```
Existing site: "The decision point"
  gestures: { dominant: COMMIT, blocked: DEFER }

Invert:
  gestures: { dominant: DEFER, blocked: COMMIT }

Generate: "The decision point where deciding is impossible"
  — Not indecision. The site itself blocks COMMIT.
  — What sites have this structure? The trolley problem. The double bind.
```

**Speculation method 3: Generate at MVA limits**

Push each MVA property to its extreme. What sites exist at the limit?

```
Mapping limit: transfer_potential = 0
  Sites that don't connect to anything.
  "The experience that can't be shared or described"

Valuation limit: value = undefined (not high or low — no valuation applies)
  Sites outside the value structure entirely.
  "The thing that doesn't matter and doesn't not-matter"

Orientation limit: direction = null (no pull in any direction)
  Sites with no attractor, no trajectory.
  "The state of pure drifting"
```

---

## Gaps in the Ontology (To Be Fixed)

Through speculation, we discover gaps:

### Gap 1: No Speculative Mode

The SPEC has modes for FluxState (`structured | dissolving | hovering | flux`) but no mode for "speculating" — operating under hypothetical conditions.

**Proposed addition**:

```
State {
  // Existing
  current_site: Site | null
  current_domain: Domain | null
  
  // New
  speculation_mode: {
    active: Boolean
    hypothetical_fields: Field[]
    hypothetical_practices: Practice[]
    hypothetical_domains: Domain[]
    hypothetical_constraints: Constraint[]
  }
}
```

In speculation mode, generation happens against hypotheticals. Sites generated are marked as `speculative: true`.

### Gap 2: No Hypothesis Operation

The SPEC has `AddConstraint`, `RemoveConstraint`, but no operation for "hypothesize constraint without committing."

**Proposed addition**:

```
Hypothesize(state: State, hypothetical: Constraint | Field | Practice | Domain) => State
// Adds hypothetical to speculation_mode without committing to State.active_constraints

CommitHypothetical(state: State, id: UUID) => State
// Move from hypothetical to actual

DiscardHypothetical(state: State, id: UUID) => State
// Remove hypothetical without consequence
```

### Gap 3: No Field Generation From Scratch

The SPEC has `GenerateField` but the input is `FieldGenerationMode` and `FieldConstraint[]` — it assumes something already exists to constrain.

**Proposed addition**:

```
SpeculateField(region_of_flux: FluxRegion, boundary_basis: BoundaryBasis) => Field
// Create a field from unbounded flux with only a bounding basis

SpeculatePractice(levels: FieldLevel[], flux_capacity: FluxCapacity) => Practice
// Create a practice from level specification and flux capacity
```

---

## Protocol for Speculation

1. **Enter speculation mode**: `speculation_mode.active = true`
2. **Declare hypotheticals**: Fields, Practices, Domains, or Constraints that don't exist
3. **Apply constraint hygiene**: Check what you're assuming can't exist. Drop the assumption.
4. **Generate under hypotheticals**: Sites, constraints, derived structures
5. **Evaluate**: Do the speculative sites reveal anything? Are they fertile?
6. **Commit or discard**: If valuable, commit hypotheticals to actual state. If not, discard.

---

## Summary

| Level | Speculation Method |
|-------|-------------------|
| **Fields** | Bound the unbounded, re-differentiate, bridge between |
| **Practices** | New level combinations, modified flux capacity, new gesture manifestations |
| **Domains** | Cross unfamiliar practice × field, generate with constraints, fragment existing |
| **Sites** | Unexplored dimensional coordinates, inverted gesture profiles, MVA limits |

Speculation extends generation to the hypothetical. The ontology supports it, but needs the additions above to make speculation explicit.

---

## Next

[Chapter 13: Cross-Domain Transfer →](./13_TRANSFER.md)

Transfer applies speculation: what if this structure existed in that domain?

---

## Exercises

### Warm-up

**12.1** Speculate a field that doesn't currently exist by re-bounding something familiar:
- Take "sleep" and bound it differently. What field emerges?

**12.2** You wake up tomorrow with a new practice installed — you see everything phenomenologically but can also dissolve at will.

What domain would you explore first? Why?

---

### Standard

**12.3** Speculate at the domain level:
- Pick a practice you know
- Cross it with a field you've never engaged through that practice
- Generate three sites that might exist in this speculative domain

Were any sites surprising?

**12.4** Speculate a site at unexplored dimensional coordinates:
- Ontological: virtuality
- Temporal: trans-lifetime
- Perceptual: other-mediated

What site lives there? Is it habitable?

**12.5** The chapter describes four ways to speculate sites:
1. Unexplored dimensional coordinates
2. Inverted gesture profiles
3. Constraint composition
4. MVA limits

Apply each method to generate one site. Compare the results. Which method produces the most vertigo?

---

### Challenge

**12.6** Speculate a practice that currently can't exist — one that requires capacities humans don't have.

What would this practice reveal? What domains would it open? Is there any way to approximate it with existing capacities?

**12.7** The chapter says "Speculation extends generation to the hypothetical."

But what's the difference between speculation and fiction? Between speculation and delusion? Where are the boundaries of productive speculation?

---

*Solutions: [SOLUTIONS.md](./SOLUTIONS.md#chapter-12-speculation)*

