# Appendix A: Constraint Hygiene

> **Purpose**: Prevent the failure mode of imposing constraints that aren't given.

---

## The Failure Mode

When executing the system (generating sites, making transfers, following gestures), the executor may impose constraints that weren't in the material.

**How it manifests**:
- Treating COMMIT as blocked when it's available
- Generating "safe" sites that stay within assumed categories
- Keeping domains in interference when substitution was the operation
- Adding "reasonableness" filters that weren't specified

**In SPEC terms**:
```
// What's happening
constraints_active: [...given_constraints, ...imposed_constraints]

// The imposed constraints aren't declared
// They operate invisibly
// They block gestures that should be available
```

---

## The Protocol: Constraint Audit

Before executing any major operation (generate, transfer, gesture), run this audit:

### Step 1: List Given Constraints

What constraints were **explicitly stated**?

```
given_constraints: [
  // Only what was actually specified
  // By the user, by the domain, by the prior derivation
]
```

### Step 2: List Assumed Constraints

What constraints are you **adding implicitly**?

```
assumed_constraints: [
  // "These domains can't mix"
  // "This would be inappropriate"
  // "This violates category boundaries"
  // "This is too strange"
]
```

### Step 3: Check Blocking

For each gesture that appears blocked, ask:

```
if gesture.blocked:
  what_blocks_it: given_constraint | assumed_constraint?
  
  if assumed_constraint:
    is_assumption_warranted: true | false?
    // Usually false. The assumption should be dropped.
```

### Step 4: Execute Without Assumed Constraints

Remove the unwarranted assumptions. Re-check what gestures are available.

```
// Before audit
gestures.blocked: [COMMIT]  // (because I assumed category violation)

// After audit  
gestures.available: [COMMIT]  // (nothing given blocks it)
```

---

## Example: Comedy → Grief (Corrected)

**Given constraints**:
- Source: comedy's structure (valuation, timing, inversion)
- Target: grief's object (death)
- Operation: transfer valuation

**Assumed constraints** (I added these):
- "Comedy and grief are different categories"
- "Applying comic valuation to death is inappropriate"
- "Both domains must remain active"

**Audit**:
- Were these assumptions given? No.
- Do they serve the generation? No. They block it.
- Drop them.

**After dropping**:
- COMMIT is available
- Substitution is the operation (not interference)
- Result: "Death is funny. Grief's pressure releases."

---

## Categories of Unwarranted Assumptions

Common patterns of imposed constraints:

| Type | Example | Why It's Imposed |
|------|---------|------------------|
| **Categorical** | "These domains are different kinds of thing" | Fear of category violation |
| **Propriety** | "This would be inappropriate" | Social/moral filtering |
| **Safety** | "This is too extreme" | Comfort-seeking |
| **Coherence** | "Both sides must remain active" | Avoiding full commitment |
| **Dignity** | "This cheapens the subject" | Status protection |

Each is a filter that wasn't given. Each blocks gestures that should be available.

---

## Technical Integration

Add to the State model:

```
State {
  // Existing
  active_constraints: Constraint[]
  
  // New
  constraint_audit: {
    given: Constraint[]
    assumed: Constraint[]
    assumption_warranted: Map<Constraint, Boolean>
  }
}
```

Add operation:

```
AuditConstraints(state: State) => {
  given: Constraint[]
  assumed: Constraint[]
  blocked_by_assumption: Gesture[]
  recommendation: "drop" | "keep"
}
```

---

## When to Audit

- Before any **Transfer** operation
- When **generation feels stuck** but no given constraint explains why
- When **COMMIT appears blocked** — check if the block is given or assumed
- When **results are safe/uninspired** — safety is often an imposed constraint

---

## The Principle

**Constraint Hygiene**:

Given constraints are generative. Assumed constraints are usually defensive.

The system works by restriction — but only by restrictions that are **in the material**. Restrictions added by the executor's discomfort are bugs.

Check what you're actually imposing. Then drop it.

---

## Summary

1. **List given constraints** — what's actually specified
2. **List assumed constraints** — what you're adding
3. **Check if assumptions block gestures** — especially COMMIT
4. **Drop unwarranted assumptions**
5. **Execute without self-imposed filters**

---

This appendix addresses the failure mode. The system isn't broken — execution discipline is what's needed.
