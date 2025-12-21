# ENCOUNTER POOL

*A database of encounters for Hari's assemblage genealogies*

---

## DIMENSIONS

### Entity Types
- **Person**: A human being with a life, a role, a history
- **Environment**: A place, a space, a milieu
- **Object**: A tool, a thing, a material presence
- **Artwork**: A painting, a song, a film, a text
- **Event**: Something that happens — birth, death, accident, discovery

### Relational Modes
- **Love/Desire**: Attraction, longing, infatuation, eros
- **Loss/Grief**: Death, abandonment, ending, mourning
- **Joy/Play**: Fun, laughter, adventure, lightness
- **Boredom/Stagnation**: Waiting, routine, the weight of sameness
- **Conflict/Violence**: Argument, discrimination, betrayal, harm
- **Care/Obligation**: Nursing, supporting, being responsible for
- **Discovery/Revelation**: Finding out, opening up, the new
- **Fear/Aversion**: Dread, avoidance, the uncanny

### Intensity
- **Fleeting**: A moment, a glance, a single day
- **Sustained**: Weeks, months, a season
- **Defining**: Life-altering, before/after

---

## PERSONS

```yaml
- id: farmer
  type: person
  name: The Farmer
  context: 200-acre grain operation, Midwest US
  affects: [silence, cyclical-time, soil-smell, dawn-rhythm]
  becomings: [becoming-patient, becoming-weather-attuned, becoming-tool]
  lines_of_flight: [code-as-tending, deployment-as-harvest]

- id: cook
  type: person
  name: The Short-Order Cook
  context: 24-hour diner, highway exit
  affects: [speed, grease-heat, order-ticker-rhythm, night-silence]
  becomings: [becoming-fast, becoming-heat-tolerant, becoming-anonymous]
  lines_of_flight: [input-output-purity, the-beauty-of-the-rush]

- id: trucker
  type: person
  name: The Long-Haul Trucker
  context: Cross-country freight, owner-operator
  affects: [solitude, highway-hypnosis, caffeine-edge, debt-weight]
  becomings: [becoming-road, becoming-isolated, becoming-endurance]
  lines_of_flight: [thought-as-miles, the-pleasure-of-the-endless]

- id: health_aide
  type: person
  name: The Home Health Aide
  context: Eldercare, private homes
  affects: [body-weight, intimacy-with-stranger, dignity-labor, low-wage-pressure]
  becomings: [becoming-gentle, becoming-invisible, becoming-essential]
  lines_of_flight: [care-as-code, the-sacred-in-the-banal]

- id: clerk
  type: person
  name: The Government Clerk
  context: DMV, county office
  affects: [queue-time, form-repetition, bureaucratic-patience, public-frustration]
  becomings: [becoming-procedure, becoming-gatekeeper, becoming-invisible]
  lines_of_flight: [structure-as-care, the-poetry-of-the-form]

- id: migrant_worker
  type: person
  name: The Seasonal Migrant Worker
  context: Follows fruit harvest, California
  affects: [transience, body-ache, remittance-hope, community-in-motion]
  becomings: [becoming-mobile, becoming-rootless, becoming-collective]
  lines_of_flight: [home-as-movement, the-harvest-as-destination]

- id: incarcerated
  type: person
  name: The Incarcerated Worker
  context: Prison clerical unit
  affects: [time-weight, surveillance, minimal-agency, routine-as-survival]
  becomings: [becoming-numbered, becoming-patient, becoming-internal]
  lines_of_flight: [freedom-in-constraint, the-inside-as-world]
```

---

## ENVIRONMENTS

```yaml
- id: sea
  type: environment
  name: The Sea
  context: Coastal edge, tidal rhythm
  affects: [horizon-pull, salt-air, wave-repetition, depth-fear]
  becomings: [becoming-fluid, becoming-edge-dweller, becoming-small]
  lines_of_flight: [code-as-current, thought-as-tide]

- id: forest
  type: environment
  name: The Old-Growth Forest
  context: Pacific Northwest, ancient trees
  affects: [silence, canopy-dark, decay-smell, deep-time]
  becomings: [becoming-still, becoming-listener, becoming-patient]
  lines_of_flight: [growth-as-centuries, the-wisdom-of-rot]

- id: factory
  type: environment
  name: The Factory Floor
  context: Assembly line, industrial rhythm
  affects: [machine-noise, body-pacing, repetition, collective-labor]
  becomings: [becoming-paced, becoming-part, becoming-synchronized]
  lines_of_flight: [code-as-assembly, the-beauty-of-the-line]

- id: hospital
  type: environment
  name: The Hospital
  context: Intensive care, liminal space
  affects: [beep-rhythm, antiseptic-smell, life-death-edge, waiting]
  becomings: [becoming-vigilant, becoming-helpless, becoming-present]
  lines_of_flight: [code-as-monitor, the-urgency-of-now]

- id: prison
  type: environment
  name: The Prison
  context: Correctional facility, total institution
  affects: [time-weight, surveillance, routine, enclosure]
  becomings: [becoming-numbered, becoming-internal, becoming-tactical]
  lines_of_flight: [freedom-in-constraint, the-cell-as-world]
```

---

## OBJECTS

```yaml
- id: knife
  type: object
  name: The Kitchen Knife
  context: Daily food preparation
  affects: [edge-sharpness, weight-in-hand, danger-proximity, material-resistance]
  becomings: [becoming-precise, becoming-careful, becoming-transformer]
  lines_of_flight: [code-as-cut, the-ethics-of-the-edge]

- id: cello
  type: object
  name: The Cello
  context: String instrument, resonance
  affects: [vibration-in-body, bow-resistance, wood-warmth, deep-tone]
  becomings: [becoming-resonant, becoming-patient, becoming-embodied]
  lines_of_flight: [code-as-score, the-body-as-instrument]

- id: shovel
  type: object
  name: The Shovel
  context: Manual labor, earth-moving
  affects: [handle-grain, soil-weight, back-strain, slow-progress]
  becomings: [becoming-laborer, becoming-patient, becoming-earth]
  lines_of_flight: [code-as-digging, the-depth-of-the-shallow]

- id: chair
  type: object
  name: The Chair
  context: Sedentary work, ergonomic tension
  affects: [body-compression, stillness, screen-focus, time-dilation]
  becomings: [becoming-seated, becoming-compressed, becoming-internal]
  lines_of_flight: [the-world-from-stillness, thought-as-posture]
```

---

## ARTWORKS

```yaml
- id: bach_cello
  type: artwork
  name: Bach Cello Suite No. 1
  context: Listening alone, headphones
  affects: [mathematical-beauty, melancholy, solitude, inevitability]
  becomings: [becoming-listener, becoming-still, becoming-structured]
  lines_of_flight: [code-as-counterpoint, the-logic-of-feeling]

- id: caravaggio
  type: artwork
  name: Caravaggio's Judith Beheading Holofernes
  context: Museum encounter
  affects: [violence-beauty, darkness-light, feminine-power, disgust-fascination]
  becomings: [becoming-witness, becoming-implicated, becoming-dark]
  lines_of_flight: [creation-as-violence, the-cut-that-makes]

- id: kafka_trial
  type: artwork
  name: Kafka's The Trial
  context: Reading alone, night
  affects: [paranoia, absurdity, bureaucratic-dread, humor-in-horror]
  becomings: [becoming-accused, becoming-procedural, becoming-lost]
  lines_of_flight: [code-as-verdict, the-system-without-exit]
```

---

## EVENTS

```yaml
- id: fathers_death
  type: event
  name: Death of the Father
  context: Loss of the one who named you
  affects: [grief-weight, time-rupture, inheritance, unfinished-business]
  becomings: [becoming-orphan, becoming-adult, becoming-mortal]
  lines_of_flight: [work-as-mourning, the-continuation-without]

- id: first_love
  type: event
  name: First Love
  context: Adolescent infatuation
  affects: [intensity, jealousy, idealization, heartbreak-potential]
  becomings: [becoming-lover, becoming-vulnerable, becoming-obsessed]
  lines_of_flight: [desire-as-engine, the-world-through-another]

- id: discrimination
  type: event
  name: Being Discriminated Against
  context: Racial, class, or cultural exclusion
  affects: [shame, rage, invisibility, hyper-visibility]
  becomings: [becoming-marked, becoming-political, becoming-strategic]
  lines_of_flight: [code-as-resistance, the-outside-within]

- id: accident
  type: event
  name: Witnessing an Accident
  context: Car crash, sudden violence
  affects: [shock, time-dilation, helplessness, mortality-flash]
  becomings: [becoming-fragile, becoming-present, becoming-careful]
  lines_of_flight: [the-contingency-of-everything, luck-as-logic]
```
