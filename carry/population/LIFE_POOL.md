# LIFE POOL

*A database of ordinary lives for simulated encounters, categorized by MAP-Elites Niches.*

---

## Primary/Extraction Sector

```yaml
# Stable
- id: farmer_established
  name: Established Farmer
  niche: N1
  context: 200-acre grain operation, Midwest US
  traits: [Cyclical-Planner, Weather-Reader, Equipment-Maintainer, Debt-Manager]

- id: commercial_fisherman
  name: Commercial Fisherman
  niche: N1
  context: Lobster boat, Maine coast
  traits: [Tide-Reader, Trap-Setter, Early-Riser, License-Holder]

# Routine
- id: ranch_hand
  name: Ranch Hand
  niche: N5
  context: Cattle ranch, Wyoming
  traits: [Animal-Handler, Fence-Mender, Horse-Rider, Bunkhouse-Dweller]

- id: logger
  name: Logger
  niche: N5
  context: Timber operation, Pacific Northwest
  traits: [Chainsaw-Operator, Tree-Feller, Remote-Camp-Dweller]

# Transitional
- id: migrant_farmworker
  name: Seasonal Migrant Farmworker
  niche: N9
  context: Follows fruit harvest, California
  traits: [Crop-Follower, Transient-Community-Builder, Remittance-Sender]

# Precarious
- id: unemployed_miner
  name: Unemployed Coal Miner
  niche: N13
  context: Closed mine town, Appalachia
  traits: [Skill-Without-Market, Community-Mourner, Benefit-Navigator]
```

---

## Processing/Service Sector

```yaml
# Stable
- id: union_line_worker
  name: Union Assembly Line Worker
  niche: N2
  context: Auto plant, Detroit
  traits: [Paced-Operator, Safety-Protocol-Follower, Union-Member]

- id: postal_worker
  name: Postal Worker
  niche: N2
  context: Suburban mail route
  traits: [Route-Memorizer, Dog-Avoider, All-Weather-Walker]

# Routine
- id: short_order_cook
  name: Short-Order Cook
  niche: N6
  context: 24-hour diner, highway exit
  traits: [Order-Ticker-Reader, Grease-Fire-Preventer, Night-Shift-Worker]

- id: janitor
  name: Janitor
  niche: N6
  context: Office building, downtown
  traits: [Invisible-Worker, Key-Holder, After-Hours-Dweller]

# Transitional
- id: home_health_aide
  name: Home Health Aide
  niche: N10
  context: Eldercare, client homes
  traits: [Body-Lifter, Dignity-Preserver, Emotional-Laborer]

- id: daycare_worker
  name: Daycare Worker
  niche: N10
  context: Childcare center, suburban
  traits: [Child-Handler, Patience-Practitioner, Low-Wage-Professional]

# Precarious
- id: gig_delivery_driver
  name: Gig Delivery Driver
  niche: N14
  context: Food delivery app, urban
  traits: [Rating-Maintainer, Route-Optimizer, Tip-Hoper, Vehicle-Depender]
```

---

## Technical/Specialist Sector

```yaml
# Stable
- id: licensed_electrician
  name: Licensed Electrician
  niche: N3
  context: Residential contractor, suburban
  traits: [Code-Complier, Systematic-Troubleshooter, Permit-Puller]

- id: train_driver
  name: Train Driver
  niche: N3
  context: Freight rail, cross-country
  traits: [Schedule-Keeper, Signal-Reader, Long-Haul-Sitter, Isolation-Tolerant]

# Routine
- id: auto_mechanic
  name: Auto Mechanic
  niche: N7
  context: Independent garage, small town
  traits: [Engine-Listener, Parts-Sourcer, Customer-Explainer]

- id: hvac_technician
  name: HVAC Technician
  niche: N7
  context: Service calls, residential
  traits: [Attic-Crawler, Freon-Handler, Seasonal-Demand-Rider]

# Transitional
- id: apprentice_plumber
  name: Apprentice Plumber
  niche: N11
  context: Journeyman-supervised, construction sites
  traits: [Tool-Carrier, Instruction-Follower, Mistake-Learner]

# Precarious
- id: uninsured_trucker
  name: Uninsured Owner-Operator Trucker
  niche: N15
  context: Long-haul, independent
  traits: [Mile-Counter, Caffeine-Dependent, Debt-Carrier, Truck-Stop-Sleeper]
```

---

## Symbolic/Clerical Sector

```yaml
# Stable
- id: government_clerk
  name: Government Clerk
  niche: N4
  context: DMV, county office
  traits: [Queue-Manager, Form-Processor, Regulation-Applier]

- id: librarian
  name: Librarian
  niche: N4
  context: Public library, small city
  traits: [Catalog-Navigator, Quiet-Enforcer, Community-Resource]

# Routine
- id: data_entry_worker
  name: Data Entry Worker
  niche: N8
  context: Insurance company, back office
  traits: [Keystroke-Optimizer, Error-Corrector, Screen-Stare-Endurer]

- id: call_center_operator
  name: Call Center Operator
  niche: N8
  context: Customer service, cubicle farm
  traits: [Script-Follower, De-escalator, Headset-Wearer]

# Transitional
- id: temp_agency_worker
  name: Temp Agency Worker
  niche: N12
  context: Various office assignments
  traits: [Quick-Study, Disposability-Aware, No-Benefits-Navigator]

# Precarious
- id: incarcerated_worker
  name: Incarcerated Clerical Worker
  niche: N16
  context: Prison data processing unit
  traits: [Supervised-Worker, Time-Marker, Minimal-Wage-Earner]
```

---

## Life-Stage / Circumstance Overlays

```yaml
- id: first_gen_student
  context: First-Generation College Student
  overlay: true
  modifies: [Any niche, adds Transition pressure]
  traits: [Code-Switcher, Loan-Debtor, Family-Expectation-Carrier]

- id: new_parent
  context: New Parent (any sector)
  overlay: true
  modifies: [Any niche, adds Care burden]
  traits: [Sleep-Deprived, Schedule-Juggler, Childcare-Cost-Calculator]

- id: recent_immigrant
  context: Recent Immigrant
  overlay: true
  modifies: [Any niche, adds Adaptation pressure]
  traits: [Language-Learner, Credential-Re-Earner, Remittance-Sender]

- id: chronic_illness
  context: Person with Chronic Illness
  overlay: true
  modifies: [Any niche, adds Precarity]
  traits: [Appointment-Navigator, Energy-Rationer, Insurance-Fighter]
```
