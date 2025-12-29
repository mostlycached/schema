# Chapter 7: Constraints — Generative Restrictions

> **Prerequisites**: [Chapter 5: Sites](./05_SITES.md), [Chapter 6: Gestures](./06_GESTURES.md)
> 
> **Key Concepts**: Constraint, Fertility, Constraint Types, Constraint Operations, Derivation
>
> **Learning Objectives**: By the end, you will understand constraints as generative (not just restrictive), know constraint types and operations, and be able to derive constraints from sites.

---

## What a Constraint Is

A constraint is a **generative restriction** that shapes which sites are visible.

The key word is *generative*. Constraints don't just eliminate options. They *reveal* options that weren't visible before.

---

## The Generative Nature of Constraints

Consider the premise "a man wakes to find he has become an insect."

This constraint eliminates vast possibilities:
- Stories about normal work life
- Stories about human romance
- Stories about social climbing

But it *reveals* a landscape that was invisible without it:
- Sites about body horror from the inside
- Sites about family shame and exclusion
- Sites about dehumanization as literal transformation
- Sites about the vulnerability of domestic space

Before the constraint, these sites weren't visible. The constraint is a lens that brings them into focus.

**Good constraints are fertile** — they reveal more than they hide.

---

## Constraint Properties

Every constraint has:

### Predicate

The condition sites must satisfy. Can be boolean (satisfies/doesn't) or graded (degree of satisfaction).

### Dimensions Targeted

Which site dimensions the constraint affects. A premise like "set in Renaissance Florence" targets the temporal and sometimes material dimensions. A premise like "from the perspective of an alien" targets the perceptual dimension.

### Strength

How strongly the constraint filters. Weak constraints are suggestions; strong constraints are requirements.

### Fertility

How many sites the constraint reveals. High-fertility constraints open rich territories; low-fertility constraints may be too restrictive.

### Internalization

How much the constraint has been absorbed. Newly added constraints sit on top. Deeply internalized constraints feel like the nature of the domain.

---

## Types of Constraints

### Dimensional Constraints

Target a specific dimension:

```
is_absence:              ontological = absence
exists_in_transition:    temporal = transition
perceived_retrospectively: perceptual = retrospective
requires_two_people:     relational = dyadic
is_recursive:            structural = recursive
```

### Gestural Constraints

Target the gesture profile:

```
dominant_is_SUSPEND:     gestures.dominant = SUSPEND
affords_BRANCH:          BRANCH in gestures.available
blocks_COMMIT:           COMMIT in gestures.blocked
primarily_opening:       more opening gestures than closing
gesture_rich:            4+ available gestures
```

### Compound Constraints

Combine dimensional and gestural:

```
opening_absence:         is_absence AND primarily_opening
suspended_limit:         is_limit AND dominant_is_SUSPEND
paradox_that_branches:   is_paradoxical AND affords_BRANCH
```

### Practice-Specific Constraints

Take the form native to a practice (see Chapter 3):

| Practice | Form | Example |
|----------|------|---------|
| Writing | Premise | "A man wakes as insect" |
| Mathematics | Axiom | "Parallel lines never meet" |
| Music | Motif | Four-note figure |
| Architecture | Parti | "Central courtyard" |

---

## Constraint Operations

Constraints can be combined and transformed:

### Conjunction (AND)

Both constraints must be satisfied.

```
is_absence AND is_dyadic
```
→ Sites that are absences involving two people

### Disjunction (OR)

Either constraint must be satisfied.

```
is_absence OR is_limit
```
→ Sites that are absences or limits

### Sequence

Apply one constraint, then another.

```
first is_transition, then add dominant_is_SUSPEND
```
→ First find transitions, then focus on those with SUSPEND dominant

### Nesting

Constraint applies within scope of another.

```
within is_tension: require affords_BRANCH
```
→ Among tension sites, require that BRANCH is available

### Negation

Invert a constraint.

```
NOT is_substance
```
→ Sites that are not about substances

### Relaxation

Weaken a constraint.

```
relax is_paradoxical → has_paradoxical_element
```
→ From requiring paradox to allowing paradox as one element

---

## Constraint Lifecycle

Constraints move through phases:

| Phase | Description |
|-------|-------------|
| Potential | Could be applied but hasn't been |
| Active | Currently shaping generation |
| Internalized | Absorbed into practice, no longer explicit |
| Exhausted | Has been fully explored, no longer generative |
| Resolved | Discharged (for question-type constraints) |

Exhausted constraints should be relaxed, modified, or removed. Internalized constraints may need to be made explicit again to be examined.

---

## Deriving Constraints from Sites

When you find an interesting site, you can extract constraints from it:

### Dimensional Derivation

The site has a dimensional position. Extract it as a constraint.

From "the pause in speech":
- `temporal = transition`
- `ontological = process`
- `structural = boundary-only`

### Gestural Derivation

The site has a gesture profile. Extract it.

From "the pause in speech":
- `dominant_is_SUSPEND`
- `blocks_COMMIT`

### Compound Derivation

Combine multiple derived constraints into a compound.

From "the pause in speech":
- `transition AND boundary-only AND dominant_is_SUSPEND`

### Negation Derivation

If the site is unusual, the negation of its properties is interesting.

"The pause in speech" blocks COMMIT. The negation — sites where COMMIT is available — is a different region to explore.

---

## Constraint Fertility Assessment

Before committing to a constraint, assess its fertility:

**High fertility signs**:
- Multiple dimensions affected
- Opens new gesture profiles
- Connects to other interesting constraints
- Unstable (might reveal different things over time)

**Low fertility signs**:
- Very specific (only one or two sites could satisfy)
- Closes most gestures
- Already fully explored in the domain
- Stable (always reveals the same things)

A constraint that reveals only one site is an endpoint, not a generative tool.

---

## Example: Working with Constraints

Starting domain: Writing × fiction

**Add constraint**: "The narrator has a secret they don't know they have"

This reveals:
- Sites about unconscious knowledge
- Sites about self-deception
- Sites about the gap between what's told and what's true

**Generate under constraint**:
- "The memory that isn't quite a memory"
- "The slip that reveals too much"
- "The detail that doesn't fit the narrator's story"

**Derive new constraint** from "the slip that reveals too much":
- `perceptual = failure-mediated` (visible through breakdown)
- `ontological = interference` (pattern from multiple sources)

**Apply derived constraint**: Now generating sites where something is visible only through failure, with interference patterns.

**Generate**:
- "The alibi that doesn't quite check out"
- "The overemphatic denial"
- "The memory that changes with each telling"

The constraint-derive-constrain loop is the engine of exploration.

---

## Summary

- **Constraints** are generative restrictions — they reveal, not just restrict
- **Properties**: predicate, dimensions targeted, strength, fertility, internalization
- **Types**: dimensional, gestural, compound, practice-specific
- **Operations**: conjunction, disjunction, sequence, nesting, negation, relaxation
- **Lifecycle**: potential → active → internalized/exhausted/resolved
- **Derivation**: Extract constraints from interesting sites
- **Loop**: Generate under constraint → find site → derive constraint → generate under new constraint

---

## Next

[Chapter 8: The Three Operations →](./08_OPERATIONS.md)

We've built up the whole system: flux, fields, practices, domains, sites, gestures, constraints. Now we go underneath to the abstract infrastructure. What's the deep structure that makes all of this work?

---

## Exercises

### Warm-up

**7.1** "I have to be home by 10pm." This is a constraint on your evening. What does it reveal? (What sites become visible that wouldn't be otherwise?)

**7.2** You're cooking and realize you're missing a key ingredient. This accidental constraint just got added. Assess its fertility: does it reveal more than it hides?

---

### Standard

**7.3** Take a constraint you live under that you didn't choose — a health condition, a financial limit, a family obligation.

Extract its dimensional and gestural properties. Then: what sites does it reveal that wouldn't be visible without it?

**7.4** Design a high-fertility constraint for "your morning routine." It should:
- Target at least two dimensions
- Open new gesture profiles
- Be unstable (might reveal different things on different days)

Test it for one morning. What sites did you find?

**7.5** The chapter describes the constraint-derive-constrain loop. Execute one full cycle:
1. Start with a constraint
2. Generate under it
3. Find a site that interests you
4. Derive a new constraint from that site
5. Generate under the new constraint

Document each step.

---

### Challenge

**7.6** Some constraints are so internalized you don't see them as constraints — they feel like "just how things are."

Identify one invisible constraint in your life. How do you know it's a constraint and not just reality? What would change if you made it explicit and then relaxed it?

**7.7** The chapter says "good constraints are fertile — they reveal more than they hide." But sometimes you need a low-fertility constraint that forces you to an endpoint.

When would you deliberately choose a low-fertility constraint? Design one that forces a resolution you've been avoiding.

---

*Solutions: [SOLUTIONS.md](./SOLUTIONS.md#chapter-7-constraints)*

