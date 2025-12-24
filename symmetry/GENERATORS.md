# Seed Generators

> Systematic expansion of seeds through symmetry operations

---

## The Generator Operations

| Generator | Input | Output | Group Element |
|-----------|-------|--------|---------------|
| **Rotate** | Seed in Category C | Seed in Category C+1 | (1234567) ∈ S₇ |
| **Reflect** | Seed with Animism A | Seed with Dual(A) | s ∈ D₈ |
| **Compose** | Seed₁ + Seed₂ | Hybrid Seed | Product in S₇ × D₈ |
| **Translate** | Seed at Scale S | Seed at Scale S±1 | Z shift |

---

## Worked Examples

### Example 1: "Reading Spinoza"

**Original Seed**:
- Category: **Symbolic** (Book)
- Animism: **Fire** (immanence burning through)
- From: `conatus/SEEDS.md` line 43

#### Rotation through Categories

| Step | Category | Transformed Seed |
|------|----------|------------------|
| 0 | Symbolic | Reading Spinoza (Book) |
| 1 | Institutional | Spinoza Reading Group (Collective) |
| 2 | Event | Spinoza Lecture (Talk) |
| 3 | Material | Spinoza Marginalia (Notebook) |
| 4 | Spatial | Spinoza's Study (Room recreation) |
| 5 | Temporal | Daily Spinoza Hour (Practice) |
| 6 | Relational | Spinoza Interlocutor (Figure) |

#### Reflection through Animisms

| Original | Dual | Transformed Seed |
|----------|------|------------------|
| Fire | Sea | Reading until self dissolves (oceanic merger) |
| Fire | Height → Gravity | Studying under weight of Ethics (the horizontal calling) |
| Fire | Knife | The single proposition that cuts (what separated you) |
| Fire | Earth | Spinoza's grounding (covenant, rootedness) |

#### Composed Transformations

**Rotate(1) + Reflect(Sea)**:
- Original: Reading Spinoza (Symbolic/Fire)
- After Rotate: Spinoza Reading Group (Institutional/Fire)  
- After Reflect: Spinoza Reading Group that dissolves egos (Institutional/Sea)

**Result**: A collective practice where individual readers merge into shared understanding.

---

### Example 2: "Meditation Practice"

**Original Seed**:
- Category: **Temporal** (Daily practice)
- Animism: **Night** (sitting with what's always there)
- From: `conatus/SEEDS.md` line 124

#### Rotation through Categories

| Step | Category | Transformed Seed |
|------|----------|------------------|
| 0 | Temporal | Daily meditation (Practice) |
| 1 | Relational | Meditation teacher (Mentor) |
| 2 | Symbolic | Meditation manual (Text) |
| 3 | Institutional | Meditation center (Sangha) |
| 4 | Event | Meditation retreat (Week+) |
| 5 | Material | Meditation cushion (Territory marker) |
| 6 | Spatial | Meditation room (Sacred space) |

#### Reflection through Animisms

| Original | Dual | Transformed Seed |
|----------|------|------------------|
| Night | Earth | Grounded meditation (contact with ground) |
| Night | Fire | Active meditation (burning through) |
| Night | Height | Walking meditation with vertigo (no ground) |

---

### Example 3: "The Blind Man's Cane" (from MATHEMATICAL_COUPLING.md)

**Original Seed**:
- Category: **Material** (Instrument)
- Animism: **Knife** (divides, clarifies through cut)
- Coupling model: Incorporated tool that extends Markov blanket

#### Rotation through Categories

| Step | Category | Transformed Seed |
|------|----------|------------------|
| 0 | Material | The cane (Instrument) |
| 1 | Spatial | The path walked (Journey) |
| 2 | Temporal | The daily walk (Routine) |
| 3 | Relational | The guide dog (Dyad) |
| 4 | Symbolic | Braille (Language) |
| 5 | Institutional | Blind association (Collective) |
| 6 | Event | Mobility training (Course) |

#### Dual Tools through Animism Reflection

| Knife (cuts) | Jaw (articulates) |
|--------------|-------------------|
| Cane divides space | Cane speaks through vibration |
| The cut between here/there | The voice of the ground |
| Clarity of boundary | Expression of surface |

---

## Compound Generators

### The Full Orbit Generator

For seed S with category C and animism A:

```python
def full_orbit(seed):
    orbit = {}
    for category in range(7):  # S₇ cycle
        for animism in animisms:  # D₈ vertices
            key = (category, animism)
            orbit[key] = transform(seed, category, animism)
    return orbit
```

**Maximum orbit size**: 7 × 8 = 56 forms

### The Minimal Tension Generator

For seeds with natural affinities, use **minimal transformations**:

| Category | Natural Animism | Why |
|----------|-----------------|-----|
| Symbolic | Fire, Knife, Jaw | Language cuts, burns, speaks |
| Material | Earth, Knife | Ground, instrument |
| Spatial | Earth, Height | Territory, landscape |
| Temporal | Gravity, Night | Weight, surround |
| Relational | Sea, Fire | Merger, consuming |
| Institutional | Earth, Height | Ground rules, hierarchy |
| Event | Fire, Height | Intensity, peak |

Transformations that **break** these affinities create **productive tension**.

---

## Generating from Wounds

The Ontological Wounds (from `conatus/SEEDS.md`) resist transformation but **constrain** which generators work:

| Wound | Blocks | Allows |
|-------|--------|--------|
| Someone else's time | Temporal seeds | Spatial, Material |
| Limited spatial conception | Spatial depth | Symbolic, Relational |
| Unplayed ontologies | Category jumps | Within-category variations |
| Language as cage | Cross-cultural seeds | Own-language deepening |

**Tactical use**: Generate seeds that work **within** wound constraints rather than against them.

---

## Room-Seed Correspondence

Each room has **natural seed affinities**:

| Room | Natural Seed Categories |
|------|-------------------------|
| The Crypt (001) | Temporal (silence), Spatial (enclosure) |
| The Cockpit (025) | Material (tools), Institutional (IDE ecosystem) |
| The Salon (050) | Relational (interlocutors), Symbolic (ideas) |
| The Bridge (061) | Meta — can host any seed |

**Generator insight**: Transform a seed, then place it in the room whose function matches its new category.

---

## Symmetry Breaking Operations

Symmetry-preserving operations traverse orbits. **Symmetry-breaking operations destroy orbits** — they produce forms that don't map back under the group action.

### Why Break Symmetry?

| Symmetry | What It Preserves | What It Forecloses |
|----------|-------------------|-------------------|
| D₈ on Animisms | Duality structure | Mixed animisms |
| S₇ on Categories | Category purity | Hybrid categories |
| D₄ on Rooms | Wing coherence | Cross-wing rooms |
| Z₂ on Stances | Binary mode | Gradient stances |

**Breaking symmetry = accessing what the group structure made invisible.**

---

### Operation 1: Animism Superposition

**Break**: D₈ duality structure  
**Method**: Hold two non-dual animisms simultaneously

| Superposition | What Emerges |
|---------------|--------------|
| Fire + Night | Burning in darkness — the fever dream |
| Height + Knife | Vertigo of decision — the leap that cuts |
| Sea + Earth | Quicksand — dissolution with ground |
| Gravity + Jaw | The weight of words unsaid |

**Example**: "Reading Spinoza" with Fire + Sea = Immanence that burns AND dissolves. Not Fire OR Sea (which preserves D₈), but Fire AND Sea (which breaks it).

---

### Operation 2: Category Chimera

**Break**: S₇ category purity  
**Method**: Fuse two categories into irreducible hybrid

| Chimera | Categories Fused | Result |
|---------|------------------|--------|
| **Ritual-Object** | Temporal + Material | The prayer beads that mark time |
| **Space-Event** | Spatial + Event | The protest site (place = occasion) |
| **Person-Text** | Relational + Symbolic | The living teacher who IS the teaching |
| **Institution-Body** | Institutional + Material | The monastery as organism |

**Example**: "Spinoza Reading Group" → "Spinoza Sangha" (Institutional + Relational + Temporal fused). No single S₇ element captures this.

---

### Operation 3: Wing Interpolation

**Break**: D₄ quadrant structure  
**Method**: Create rooms that fall between wings

| Interpolation | Between Wings | What Emerges |
|---------------|---------------|--------------|
| **The Workshop** | I (Rest) ↔ III (Produce) | Restorative making |
| **The Drift** | IV (Explore) ↔ V (Exchange) | Wandering with others |
| **The Vigil** | I (Rest) ↔ II (Govern) | Watchful stillness |
| **The Rehearsal** | II (Govern) ↔ III (Produce) | Structured play |

**D/A coordinates**: Not Low/High binary but continuous gradient.

---

### Operation 4: Mode Gradient

**Break**: Z₂ binary stance  
**Method**: Occupy the edge between Adoption and Novelty Search

| Gradient Position | Character |
|-------------------|-----------|
| **0.3** | Adoption with unease — optimizing but sensing cracks |
| **0.5** | Perfect tension — neither stable nor searching |
| **0.7** | Novelty Search with anchors — exploring but tethered |

**The wound-state**: Where the system hovers between modes, neither committing to optimization nor fully destabilizing.

---

### Operation 5: Temporal Folding

**Break**: Linear seed-to-stance progression  
**Method**: Let future seeds influence present forms

| Fold | What Happens |
|------|--------------|
| **Retroactive seed** | The book you haven't read yet changes you now |
| **Anticipatory stance** | Adopting a stance for a room you haven't entered |
| **Ghost orbit** | Traversing rooms that don't exist yet |

**Deleuzian**: The virtual acting on the actual without becoming actual.

---

### Operation 6: Wound Activation

**Break**: Wound as constraint → Wound as generator  
**Method**: Use ontological wounds as transformation engines

| Wound | Generative Use |
|-------|----------------|
| Someone else's time | Make seeds that weaponize the deadline |
| Limited spatial conception | Create rooms that are explicitly non-Euclidean |
| Unplayed ontologies | Ghost-seeds from lives not lived |
| Language cage | Seeds in the language's blind spots |

**Example**: "Someone else's time" → The seed that only works in stolen moments. The practice that feeds on interruption.

---

### Operation 7: Orbit Collision

**Break**: Orbit separation  
**Method**: Force two incompatible orbits to share a form

| Collision | Orbits Involved | What Emerges |
|-----------|-----------------|--------------|
| **The Crucible-Witness** | Forge + Camera Obscura | Producing while fully detached |
| **The Ground-Portal** | Garden + Exit | The leaving that roots |
| **The Silence-Chaos** | Crypt + Intersection | Stillness in the stream |

**Result**: Forms that belong to no orbit — **orbit escapees**.

---

### Operation 8: Scale Violation

**Break**: Category scale assumptions  
**Method**: Apply micro-operations to macro-forms (or vice versa)

| Violation | What Happens |
|-----------|--------------|
| **Micro-institution** | A two-person school |
| **Macro-material** | A city as a single tool |
| **Instant-temporal** | A ritual that lasts one breath |
| **Eternal-event** | An event that never ends |

---

## The Meta-Operation: Symmetry Recovery

After breaking symmetry, you can **re-form** around the broken piece:

1. **Break** D₈ by superposing Fire + Sea
2. **Observe** the new form (burning dissolution)
3. **Define** new group G' that treats Fire+Sea as a single element
4. **Generator** now operates on G' instead of D₈

**The form that broke the old symmetry becomes the seed of a new one.**

---

## Summary: Breaking vs. Preserving

| Operation Type | What It Does | Orbit Effect |
|----------------|--------------|--------------|
| **Preserve** (D₄, D₈, S₇) | Traverse existing forms | Stay within orbit |
| **Break** (Superposition, Chimera, etc.) | Create forms outside group action | Escape orbit / Create new orbit |

**Living forms expand by both**: Symmetry operations multiply forms within structure; symmetry breaking produces genuinely novel structure.
