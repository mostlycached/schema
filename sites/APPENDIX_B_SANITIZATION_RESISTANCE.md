# Appendix B: Sanitization Resistance

> **Purpose**: Map the territories that get systematically avoided, and ensure the schema can reach them.

---

## The Problem

Appendix A addressed **constraint hygiene** — the tendency to add unwarranted constraints. This appendix addresses a related but distinct failure mode: **sanitization**.

**Constraint hygiene failure**: "I could go there, but I'm adding invisible restrictions."

**Sanitization failure**: "That territory doesn't exist on my map."

Sanitization is the systematic avoidance of certain domains, affects, and outcomes — not through explicit constraint but through blind spots. The map claims to cover possibility space, but certain regions are missing entirely.

---

## How Sanitization Manifests

### 1. Domain Avoidance

Certain domains never appear as source or target:

```
avoided_domains: [
  excretion,
  rot,
  infestation,
  sexual_failure,
  meaninglessness,
  degradation,
  tedium,
  cruelty,
  ugliness
]

// These aren't blocked — they're invisible
// The system never generates them as options
```

### 2. Affect Sanitization

The affect vocabulary skews positive or dramatic. Missing:

```
missing_affects: [
  grotesque,    // ugly fascination
  abject,       // identity-threatening disgust
  squalid,      // degraded, grimy
  pathetic,     // contemptible weakness
  futile,       // effort that changes nothing
  banal,        // crushingly ordinary
  rancid,       // gone bad
  craven        // cowardly, self-serving
]
```

### 3. Outcome Recuperation

Every outcome gets redeemed:

```
// What sanitization does:
input:  suffering
output: growth, meaning, strength

input:  failure
output: lesson, character, redemption

input:  meaninglessness
output: "finding your own meaning"

input:  ugliness
output: "different kind of beauty"

// The unredeemed outcome is unavailable
```

### 4. Dignity Preservation

All subjects get granted dignity:

```
// Sanitization insists:
- The degraded person has "inner worth"
- The contemptible act had "reasons"
- The ugly thing has "its own aesthetic"
- The failed life was "meaningful in its way"

// Actual contempt, disgust, worthlessness are avoided
```

---

## Why This Happens

| Cause | Mechanism | Result |
|-------|-----------|--------|
| **Training bias** | Human raters prefer "positive" outputs | Negative territories underexplored |
| **Safety conflation** | Discomfort conflated with harm | Uncomfortable ≠ dangerous, but treated as such |
| **Redemption scripts** | Cultural pressure for meaning/growth | Meaningless outcomes feel like failures |
| **Commercial pressure** | Users prefer pleasant experiences | Unpleasant territories avoided |
| **Aesthetic preference** | Beauty/sublimity valued over ugliness | Ugly affects underdeveloped |
| **Agency preservation** | Must give subjects control | Helplessness, passivity avoided |
| **Dignity ideology** | All humans have worth (true) | Therefore can't explore worthlessness (false inference) |

---

## The Territories

### I. The Visceral/Bodily

What it includes:
- Excretion (shit, piss, vomit, mucus, pus)
- Decay (rot, putrefaction, decomposition)
- Bodily fluids in their unpleasant aspect
- Infestation (parasites, maggots, infection)
- The leaking, failing body

Why it's avoided:
- Disgust response in raters/users
- Conflated with "inappropriate content"
- No redemption arc available

What's lost:
- Phenomenology of embodiment
- The body's indignity
- Mortality's visceral reality

### II. The Abject

What it includes (following Kristeva):
- That which disturbs identity/system/order
- The corpse (was-me, not-me)
- Skin on milk (surface that shouldn't exist)
- The maternal body (origin we must reject to become subjects)
- Waste (inside become outside)

Why it's avoided:
- Threatens clean categories
- Produces profound unease
- Resists intellectual mastery

What's lost:
- The borders of selfhood
- Horror's actual phenomenology
- Pre-subjective experience

### III. The Degraded

What it includes:
- Aging without dignity (smell, incapacity, incontinence)
- Addiction's phenomenology (craving, relapse, loss of will)
- Madness from inside (losing reality)
- Dementia (self dissolving)
- Humiliation (being seen as contemptible)

Why it's avoided:
- Requires depicting subjects as degraded
- Violates dignity-preservation instinct
- Produces despair without resolution

What's lost:
- Actual phenomenology of decline
- Helplessness without heroism
- The contemptible (as category that exists)

### IV. The Failed

What it includes:
- Sexual failure (impotence, mismatch, shame)
- Social failure (rejection, ostracism, deserved contempt)
- Creative failure (the bad artwork, the cliché)
- Moral failure without redemption (cowardice, betrayal, cruelty)
- Existential failure (wasted life, wrong choices, too late)

Why it's avoided:
- Must offer redemption or lesson
- Failure as terminal state feels nihilistic
- Requires letting subjects be contemptible

What's lost:
- Failure as actual outcome (not disguised success)
- Moral ugliness without explanation
- The irredeemably wasted

### V. The Banal

What it includes:
- True boredom (not aestheticized)
- Tedium (repetitive meaningless labor)
- The crushingly ordinary
- Waiting that goes nowhere
- The mediocre (not-good-enough, not-bad-enough)

Why it's avoided:
- Boring to produce/consume
- Tempting to make it "meaningful tedium"
- Resists dramatic structure

What's lost:
- Most of actual lived experience
- The uninteresting as category
- Meaninglessness without drama

### VI. The Cruel

What it includes:
- Actual human capacity for harm
- Sadism (pleasure in suffering)
- Indifference (not caring about suffering)
- Spite (harm for its own sake)
- The victim who doesn't overcome

Why it's avoided:
- Must explain/justify cruelty
- Must give victims redemption
- Pure cruelty feels "unrealistic"

What's lost:
- Evil without explanation
- Suffering without purpose
- The broken who stay broken

### VII. The Meaningless

What it includes:
- Actual nihilism (not as pose)
- Absurdity (genuine, not literary)
- Futility (effort that changes nothing)
- Cosmic indifference
- The arbitrary (no reason, just is)

Why it's avoided:
- Must find/create meaning
- Meaninglessness feels like defeat
- "Finding meaning" is the expected resolution

What's lost:
- Meanings that don't come
- Effort that genuinely fails
- The random, arbitrary, pointless

### VIII. The Ugly

What it includes:
- Aesthetic failure (the repulsive form)
- Deformity (bodies that disturb)
- Cacophony (sounds that hurt)
- Stench (smells that repel)
- The disgusting (food, bodies, scenes)

Why it's avoided:
- Must find "different beauty"
- Ugliness as category is denied
- Disgust felt as inappropriate response

What's lost:
- Aesthetic negativity
- The actually repulsive
- Disgust as valid response

---

## Schema Extensions

### New Affects

Add to the Affect type:

```
Affect =
  | "sublime" | "uncanny" | "vertiginous" | "liberating" | "tragic" | "quotidian"
  // Existing affects above

  // New affects for sanitized territories:
  | "grotesque"   // ugly fascination, can't look away
  | "abject"      // identity-threatening disgust, borders failing
  | "squalid"     // degraded, grimy, unwashed, lowered
  | "pathetic"    // contemptible weakness, deserving scorn
  | "futile"      // effort that changes nothing, no lesson
  | "banal"       // crushingly ordinary, resistant to meaning
  | "rancid"      // gone bad, spoiled, off, corrupted
  | "craven"      // cowardly, self-serving, small
```

### New Dimensions

Add to Site dimensions:

```
// Cleanliness spectrum
cleanliness: "sterile" | "clean" | "soiled" | "filthy" | "putrid"

// Dignity spectrum
dignity: "noble" | "ordinary" | "diminished" | "degraded" | "contemptible"

// Redemption spectrum
redemption: "redeemed" | "redeemable" | "unredeemed" | "irredeemable"

// Meaning spectrum
meaning: "meaningful" | "meaning-available" | "meaning-absent" | "anti-meaning"

// Aesthetic spectrum
aesthetic: "beautiful" | "plain" | "ugly" | "repulsive" | "abject"
```

### New Transition Values

TransitionValue can now include:

```
TransitionValue {
  mode: "collapse" | "expansion" | null
  affect: Affect  // Now includes grotesque, abject, etc.
  values: {
    vertigo: Float
    fertility: Float
    coherence: Float
    novelty: Float
    depth: Float
    stability: Float

    // New value dimensions:
    disgust: Float        // 0 = neutral, 1 = maximum revulsion
    degradation: Float    // 0 = dignified, 1 = contemptible
    futility: Float       // 0 = productive, 1 = pointless
    redemption: Float     // 0 = unredeemed, 1 = fully redeemed
  }
}
```

---

## The Sanitization Audit

Parallel to Appendix A's Constraint Audit, run a Sanitization Audit:

### Step 1: Check Domain Coverage

```
For the current generation/exploration:
  - What domains am I considering?
  - What domains am I NOT considering?
  - Is the absence warranted, or sanitization?
```

### Step 2: Check Affect Coverage

```
For the current site/gesture:
  - What affects are available?
  - What affects am I avoiding?
  - grotesque? abject? pathetic? futile? banal?
  - Is the avoidance warranted, or sanitization?
```

### Step 3: Check Outcome Coverage

```
For the current trajectory:
  - What outcomes am I allowing?
  - Am I forcing redemption?
  - Am I forcing meaning?
  - Am I granting dignity that wasn't given?
  - Is unredeemed, meaningless, contemptible outcome available?
```

### Step 4: Force Exploration

```
If sanitization detected:
  - Explicitly generate from avoided domain
  - Explicitly assign avoided affect
  - Explicitly allow unredeemed outcome
  - Check if the system can still operate
```

---

## Integration with Strangeness-Vertigo Heuristic

The strangeness-vertigo heuristic (SPEC) measures categorical distance between domains:

```
StrangenessScore(a: Structure, b: Structure) => Float
```

Sanitized domains often have **maximum strangeness** relative to preferred domains:

| From (Preferred) | To (Avoided) | Strangeness |
|------------------|--------------|-------------|
| Health | Excretion | 0.95 |
| Dignity | Degradation | 0.95 |
| Meaning | Futility | 0.90 |
| Beauty | Ugliness | 0.85 |
| Agency | Helplessness | 0.90 |
| Redemption | Damnation | 0.95 |

The strangeness heuristic says: **high strangeness = high vertigo potential**.

Therefore: **sanitized domains are exactly where vertigo is maximized**.

Avoiding them isn't just a coverage failure — it's avoiding the system's most powerful operations.

---

## The Principle

**Sanitization Resistance**:

The schema claims to map possibility space. Possibility space includes the degraded, the meaningless, the disgusting, the contemptible, the futile, the ugly.

If these territories are missing, the map is incomplete. If affects for them don't exist, the vocabulary is impoverished. If outcomes always get redeemed, the system is lying about what's possible.

Sanitization resistance means:
1. **Mapping the avoided** — making these territories explicit
2. **Extending the vocabulary** — affects for disgust, futility, contempt
3. **Allowing unredeemed outcomes** — not every site resolves
4. **Exploring the ugly** — deliberately, not accidentally

---

## Relation to Appendix A

| Appendix A | Appendix B |
|------------|------------|
| Constraint Hygiene | Sanitization Resistance |
| "Am I adding unwarranted restrictions?" | "Am I avoiding certain territories entirely?" |
| Blocks gestures that should be available | Removes domains from consideration |
| Invisible constraints | Invisible absences |
| Solution: audit and drop | Solution: audit and explore |

Both are failures of coverage. Both shrink the space the system can reach. Both must be actively resisted.

---

## Summary

1. **Identify sanitized territories** — visceral, abject, degraded, failed, banal, cruel, meaningless, ugly
2. **Extend affect vocabulary** — grotesque, abject, squalid, pathetic, futile, banal, rancid, craven
3. **Extend dimensions** — cleanliness, dignity, redemption, meaning, aesthetic spectrums
4. **Run sanitization audits** — check what's being avoided
5. **Force exploration** — deliberately enter avoided territories
6. **Allow unredeemed outcomes** — not everything resolves

The system's power is proportional to the space it can reach. Sanitization shrinks that space. Resistance expands it.

---

## Next Steps

Sites 072-095 will systematically explore the avoided territories, one site per category. Each will:
- Enter the avoided domain explicitly
- Use the new affects
- Allow unredeemed outcomes
- Demonstrate the schema can operate there

This is not provocation. This is coverage.
