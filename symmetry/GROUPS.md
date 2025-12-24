# Mathematical Groups

> Formal definitions of the symmetry groups acting on living forms

---

## 1. The Dihedral Group D₄

**Definition**: The symmetry group of a square. Order 8.

### Elements

| Element | Name | Matrix Representation |
|---------|------|----------------------|
| e | Identity | [[1,0],[0,1]] |
| r | 90° rotation | [[0,-1],[1,0]] |
| r² | 180° rotation | [[-1,0],[0,-1]] |
| r³ | 270° rotation | [[0,1],[-1,0]] |
| s | Vertical reflection | [[1,0],[0,-1]] |
| sr | Diagonal reflection | [[0,1],[1,0]] |
| sr² | Horizontal reflection | [[-1,0],[0,1]] |
| sr³ | Anti-diagonal reflection | [[0,-1],[-1,0]] |

### Multiplication Table

```
    │ e   r   r²  r³  s   sr  sr² sr³
────┼────────────────────────────────
e   │ e   r   r²  r³  s   sr  sr² sr³
r   │ r   r²  r³  e   sr³ s   sr  sr²
r²  │ r²  r³  e   r   sr² sr³ s   sr
r³  │ r³  e   r   r²  sr  sr² sr³ s
s   │ s   sr  sr² sr³ e   r   r²  r³
sr  │ sr  sr² sr³ s   r³  e   r   r²
sr² │ sr² sr³ s   sr  r²  r³  e   r
sr³ │ sr³ s   sr  sr² r   r²  r³  e
```

### Application to Rooms

D₄ acts on the **D/A intensity plane**:
- **r** = Rotate quadrant (Foundation → Administration → Machine Shop → Wilderness)
- **s** = Reflect across A-axis (swap high/low D)
- **sr²** = Reflect across D-axis (swap high/low A)

---

## 2. The Dihedral Group D₈

**Definition**: The symmetry group of an octagon. Order 16.

### Elements

8 rotations: e, r, r², r³, r⁴, r⁵, r⁶, r⁷  
8 reflections: s, sr, sr², sr³, sr⁴, sr⁵, sr⁶, sr⁷

### Application to Animisms

The 8 animisms sit at octagon vertices:

```
Position 0: Height    (12 o'clock)
Position 1: Fire      (1:30)
Position 2: Knife     (3 o'clock)
Position 3: Night     (4:30)
Position 4: Gravity   (6 o'clock)
Position 5: Sea       (7:30)
Position 6: Jaw       (9 o'clock)
Position 7: Earth     (10:30)
```

**Dualities as reflections**:

| Reflection | Fixed Axis | Swaps |
|------------|-----------|-------|
| s | Height—Gravity | Fire↔Earth, Knife↔Jaw, Night↔Sea |
| sr² | Fire—Sea | Height↔Knife, Gravity↔Jaw, Earth↔Night |
| sr⁴ | Knife—Jaw | Height↔Earth, Fire↔Night, Gravity↔Sea |

---

## 3. The Symmetric Group S₇

**Definition**: The group of all permutations of 7 objects. Order 7! = 5040.

### Application to Seed Categories

The 7 seed categories can be permuted:

```
1: Symbolic
2: Institutional  
3: Event
4: Material
5: Spatial
6: Temporal
7: Relational
```

**Key permutations**:

| Permutation | Notation | Effect |
|-------------|----------|--------|
| Cycle-7 | (1234567) | Each category → next |
| Transposition | (1 4) | Swap Symbolic ↔ Material |
| 3-cycle | (1 2 3) | Symbolic→Institutional→Event→Symbolic |

### Interpretation

A **seed transformation** that moves a seed from one category to another corresponds to a permutation in S₇.

---

## 4. The Cyclic Group Z₂

**Definition**: The group {e, σ} with σ² = e. Order 2.

### Application to Stance Modes

| Element | Mode |
|---------|------|
| e | Adoption (stable, optimizing) |
| σ | Novelty Search (trauma, reconfiguring) |

**Group action**: σ flips between modes.  
**Trigger**: Viability V(S, E) drops below threshold.

---

## 5. Product Groups

### S₇ × D₈ (Seed Transformation Group)

**Order**: 5040 × 16 = 80,640

Every seed can be transformed by:
1. Changing category (element of S₇)
2. Changing animism (element of D₈)

**Orbit size**: For a typical seed, the orbit under this group is 7 × 8 = 56 (if no stabilizers).

### D₄ × Z₂ (Room-Mode Group)

**Order**: 8 × 2 = 16

Every room-stance pair can be transformed by:
1. Rotating/reflecting the room across wings (D₄)
2. Flipping the stance mode (Z₂)

---

## 6. Group Axioms Verification

For any symmetry group G acting on forms F:

| Axiom | Requirement | Verification |
|-------|-------------|--------------|
| **Closure** | g·h ∈ G for all g,h ∈ G | Composition of symmetries is a symmetry |
| **Associativity** | (g·h)·k = g·(h·k) | Function composition is associative |
| **Identity** | e·f = f for all f ∈ F | The "do nothing" transformation exists |
| **Inverse** | For each g, exists g⁻¹ | Every transformation can be undone |

All defined groups satisfy these axioms. ∎

---

## 7. Stabilizers and Orbits

### Orbit-Stabilizer Theorem

For g ∈ G acting on x ∈ X:

$$|G| = |\text{Orbit}(x)| \times |\text{Stab}(x)|$$

### Special Rooms with Non-Trivial Stabilizers

| Room | Stabilizer | Interpretation |
|------|------------|----------------|
| The Bridge (061) | D₄ | Meta-room transcends quadrant |
| The River (049) | Z₂ | Center of D/A plane |
| The Exit (072) | D₄ | Universal escape |

These rooms are **fixed points** — they don't transform into other rooms because they occupy privileged positions.

---

## 8. Homomorphisms

### The Intensity Map

$$\phi: \text{Rooms} \to \mathbb{R}^2$$

Maps each room to its (D, A) coordinates.

**Property**: D₄-equivariant — the diagram commutes:

```
Room ──φ──→ (D, A)
  │           │
  g           ρ(g)
  ↓           ↓
g·Room ──φ──→ ρ(g)·(D, A)
```

Where ρ is the standard representation of D₄ on ℝ².

### The Animism Map

$$\psi: \text{Seeds} \to \text{Animisms}$$

Maps each seed to its dominant animism.

**Property**: D₈-equivariant under animism reflection.
