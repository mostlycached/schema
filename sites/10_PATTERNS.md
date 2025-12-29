# Chapter 10: Patterns

> **Prerequisites**: Chapters 1-9
>
> **Learning Objectives**: Recurring patterns in the ontology as applied to literature. Each pattern is a structure you can recognize and generate.

---

## What This Chapter Does

Chapter 9 showed one full analysis. This chapter identifies **recurring patterns** — structural configurations that appear across different works and can be used as templates.

Each pattern is described in SPEC terms.

---

## Pattern 1: The SUSPEND That Blocks RESOLVE

**Structure**:
- A site with `gestures.dominant = SUSPEND`
- `gestures.blocked.includes('RESOLVE')`
- `dimensions.temporal = 'oscillation' | 'accumulation'`

**What it does**: Creates sustained tension that never discharges. The work remains unresolved — not as failure, but as form.

**Literary instances**:

| Work | The unresolvable site |
|------|----------------------|
| Lispector, "Love" | The crack in Ana's world (no return possible) |
| Kafka, *The Trial* | Josef K.'s guilt (never specified, never acquitted) |
| Beckett, *Waiting for Godot* | The waiting itself (Godot never comes) |

**Constraint derived**:
```
Constraint {
  predicate: (s) => s.gestures.dominant == 'SUSPEND' 
                 && s.gestures.blocked.includes('RESOLVE')
  dimensions_targeted: [gestural, temporal]
  
  fertility: high
  // Generates: unfinished grief, endless trial, question without answer
}
```

**Use**: Apply when you want generative irresolution — a site that produces meaning by refusing closure.

---

## Pattern 2: Failure-Mediated Perception

**Structure**:
- `dimensions.perceptual = 'failure-mediated'`
- The site becomes visible only when something breaks down

**What it does**: Reveals what's normally invisible because functioning systems hide their structure.

**Literary instances**:

| Work | What becomes visible through breakdown |
|------|----------------------------------------|
| Lispector, "Love" | The "raw world" beneath domestic order |
| Tolstoy, *Death of Ivan Ilyich* | The unlived life, visible only when dying |
| Proust, madeleine moment | The past, accessible only through involuntary memory (will fails) |

**MVA structure**:
- **Mapping**: The failure creates a map between hidden structure and visible effect
- **Valuation**: What was low-value (the breakdown) reveals high-value (the hidden)
- **Orientation**: The failure becomes a source (radiates insight)

**Constraint derived**:
```
Constraint {
  predicate: (s) => s.dimensions.perceptual == 'failure-mediated'
  
  as_valuation: {
    inversion: true  // Low becomes high through breakdown
  }
}
```

**Use**: Generate sites about what only appears when systems fail: illness revealing health assumptions, breakdown revealing reliance, loss revealing value.

---

## Pattern 3: The WIDEN Cascade

**Structure**:
- Initial site is bounded
- WIDEN executes repeatedly
- Each expansion reveals a larger containing pattern
- Termination: cosmic scale or dissolution

**What it does**: A local observation becomes a meditation on totality. The particular opens to the universal without losing particularity.

**Literary instances**:

| Work | Widening cascade |
|------|-----------------|
| Sebald, *Rings of Saturn* | Walking in Suffolk → silk trade → colonialism → all human destruction |
| Proust, madeleine | Cookie → childhood → time itself → the structure of memory |
| Borges, "The Aleph" | Point under staircase → every point in the universe simultaneously |

**Gesture sequence**: WIDEN → WIDEN → WIDEN → (SUSPEND at cosmic scale)

**Dimensional shift**:
```
dimensions.scale: momentary → extended → lifetime → trans-lifetime → cosmic
```

**Use**: When you have a local site and want to discover what containing patterns it belongs to. Keep executing WIDEN until you reach a site that can't be widened further (or that loops back).

---

## Pattern 4: The Disappearing Agent

**Structure**:
- Site begins with `dimensions.agential = [some agent]`
- Through gesture sequence, agential dimension shifts
- Final site: `dimensions.agential = 'non-human' | null`

**What it does**: The self dissolves. Actions happen without a doer. The subject becomes object.

**Literary instances**:

| Work | Agent dissolution |
|------|------------------|
| Walser, *The Walk* | Writer goes for walk → observations accumulate → no one observing |
| Beckett, *The Unnamable* | "I" speaks → speech undermines speaker → "I can't go on, I'll go on" |
| Blanchot, *Thomas the Obscure* | Thomas → not-Thomas → the neutral |

**Gesture sequence**: NARROW (on observation) → NARROW (on observation) → subject falls away

**MVA effect**:
- Valuation ground shifts from agent-centered to process-centered
- Orientation: no more point-attractor (self); diffuse field instead

**Constraint derived**:
```
Constraint {
  predicate: (s) => s.dimensions.agential in ['non-human', null]
                 && s.derived_via includes agent-dissolving-gesture-sequence
}
```

**Use**: When you want to get the ego out of the generative process. What happens when there's no "I" to have the insights?

---

## Pattern 5: Ontological Shift Site

**Structure**:
- Entry site has one `dimensions.ontological` value
- Derived site has a different `dimensions.ontological` value
- The shift is the meaning

**What it does**: Transforms how a domain is ontologically categorized. What was "substance" becomes "absence." What was "process" becomes "limit."

**Literary instances**:

| Work | Ontological shift |
|------|------------------|
| Kafka, *Metamorphosis* | Gregor: person (substance) → vermin (substance) → obstacle (relation) → absence (after death) |
| Borges, "Funes" | Memory: process → substance (everything remembered) → limit (can't think because can't forget) |
| Lispector, *Passion According to G.H.* | Cockroach: substance → limit → tension → (something unnameable) |

**What the shift reveals**: The ontological categories are not fixed. A site can migrate through them. The migration path is itself meaningful.

**Constraint derived**:
```
Constraint {
  predicate: (s) => s.dimensions.ontological != s.derived_from.dimensions.ontological
  
  // Track the shift
  as_mapping: {
    source: original ontological position
    target: new ontological position
    transfer: what survived the shift
  }
}
```

**Use**: When a domain feels stuck in one ontological mode (everything is "substance"), look for sites that could shift to another mode (relation, absence, limit).

---

## Pattern 6: The Valuation Inversion

**Structure**:
- Domain has established `valuation.ground`
- Event or site encounter inverts the valuation
- What was high becomes low; what was low becomes high

**What it does**: Destabilizes meaning-system. Not new content — new values.

**Literary instances**:

| Work | Valuation inversion |
|------|---------------------|
| Tolstoy, *Ivan Ilyich* | Success (high) → revealed as failure; servant's care (low) → revealed as love |
| Dostoyevsky, *Notes from Underground* | Social success (high) → revealed as shallow; underground spite (low) → revealed as truth |
| Flaubert, *Madame Bovary* | Romance (high) → revealed as delusion; domestic boredom (low) → revealed as reality |

**MVA analysis**:
```
Valuation {
  before: { function: social_success → high }
  after:  { function: social_success → low }
  
  ground: shifted from GIVEN to DERIVED (the ground itself was interrogated)
}
```

**Use**: When generating in a domain with fixed values, look for the site where valuation inverts. The inversion reveals the contingency of the value system.

---

## Pattern 7: The DEFER Endpoint

**Structure**:
- `gestures.dominant = DEFER`
- `gestures.blocked = [COMMIT, RESOLVE]`
- Site has no exit except return to flux or external interruption

**What it does**: Creates sites of permanent postponement. Nothing happens — but the not-happening is the site.

**Literary instances**:

| Work | The perpetual deferral |
|------|------------------------|
| Kafka, *The Castle* | K. never reaches the Castle; approach is infinitely deferred |
| Beckett, *Waiting for Godot* | Godot is deferred every day |
| Bernhard, *Correction* | Roithamer defers completion of the Cone until it kills him |

**Site characteristics**:
```
Site {
  gestures: {
    dominant: DEFER
    blocked: [COMMIT, RESOLVE]
    available: [DEFER]  // Only deferral available
    latent: [SUSPEND]
  }
  
  orientation_properties: {
    type: attractor  // Something pulls
    stability: stable  // But it never arrives
  }
  
  existence_type: periodic
  // The deferral recurs; it's the structure, not an accident
}
```

**Use**: When you want to generate sites about what never happens. The undone thing, the avoided thing, the thing that would end something if it happened.

---

## Pattern 8: Interference as Site

**Structure**:
- `dimensions.ontological = 'interference'`
- Two or more patterns overlap
- The overlap is the site (not either pattern alone)

**What it does**: Creates meaning from collision. Neither source fully determines the site.

**Literary instances**:

| Work | The interference |
|------|-----------------|
| Lispector, "Love" | Blindness + public gaze = paradoxical visibility |
| Joyce, *Ulysses* | Homer + 1904 Dublin = neither heroic nor merely local |
| Borges, "Pierre Menard" | Cervantes' *Quixote* + Menard's *Quixote* = different texts with identical words |

**MVA analysis**:
```
Mapping {
  instance_type: interference
  // Not translation, not embedding — collision
  
  transfer: {
    elements: partial from each source
    relations: some preserved, some broken
    operations: new operations emerge from collision
  }
}
```

**Use**: When generating, try colliding two patterns that have no natural relationship. The interference — what happens in the collision — is where new sites emerge.

---

## Summary

| Pattern | Key Structure | Effect |
|---------|--------------|--------|
| SUSPEND blocks RESOLVE | Gestures: dominant SUSPEND, blocked RESOLVE | Sustained irresolution |
| Failure-mediated perception | Perceptual: failure-mediated | Hidden becomes visible |
| WIDEN cascade | Repeated WIDEN → scale shift | Local → cosmic |
| Disappearing agent | Agential → null | Self dissolves |
| Ontological shift | Ontological value changes | Category migration |
| Valuation inversion | High ↔ Low | Value system destabilized |
| DEFER endpoint | Dominant DEFER, blocked COMMIT/RESOLVE | Permanent postponement |
| Interference site | Ontological: interference | Meaning from collision |

---

## Using Patterns

1. **Recognition**: When analyzing a work, identify which patterns are present
2. **Generation**: When stuck, pick a pattern and apply its constraint structure
3. **Combination**: Multiple patterns can operate simultaneously in a single work

---

## Next

[Chapter 11: Troubleshooting →](./11_TROUBLESHOOTING.md)

What to do when analysis fails or generation stalls.

---

## Exercises

### Warm-up

**10.1** A friend keeps talking about applying for a job but never does. Which pattern is this? (DEFER endpoint, SUSPEND blocks RESOLVE, something else?)

**10.2** Think of a movie you love. Which of the eight patterns is most central to how it works?

---

### Standard

**10.3** Generate three sites using the "Failure-Mediated Perception" constraint:
- A domain where something only becomes visible through breakdown

What did you find? Were the sites surprising?

**10.4** Apply "Valuation Inversion" to a domain where you have strong preferences. What's currently high-value? What would it look like inverted?

Can you actually operate from the inverted values, or just describe them?

**10.5** Execute a "WIDEN cascade" starting from wherever you're sitting right now:
1. This seat
2. WIDEN → ?
3. WIDEN → ?
4. WIDEN → ?

Where do you end up? How many WIDENs before you hit cosmic scale or loop back?

---

### Challenge

**10.6** The patterns are derived from literature. But you live a life, not a text.

Do these patterns show up in lived experience? Pick a pattern and trace it through a period of your life. Was it generative then, or only visible in retrospect?

**10.7** Design a new pattern not listed in the chapter. Give it:
- Structure (dimensional and gestural)
- Literary instances (2-3 examples)
- Derived constraint
- Use case

What does this pattern reveal?

---

*Solutions: [SOLUTIONS.md](./SOLUTIONS.md#chapter-10-patterns)*

