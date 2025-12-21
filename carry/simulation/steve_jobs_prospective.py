"""
Steve Jobs: Prospective Assemblage Analysis
Modeling lines of flight as POTENTIALS, not historical outcomes.
Each timestamp shows assemblages and their emergent possibilities.
"""

from carry.simulation.assemblage import (
    Assemblage, Territory, Code, Component, LineOfFlight, VirtualCapacity
)

# ============================================================
# 1972: Reed College Drop-out
# ============================================================

def steve_jobs_1972():
    """
    Age 17, dropped out but auditing classes.
    We model ONLY what exists now, predict NOTHING.
    """
    
    calligraphy_student = Assemblage(
        name="Calligraphy-Student-1972",
        abstract_machine="(Letterform Study + Aesthetic Training) => (???)",
        territories=[
            Territory("Reed College classroom", "Audit calligraphy", "Exploratory", "smooth"),
        ],
        codes=[
            Code("Serif appreciation", "Seeing letter beauty", "pattern", "molecular"),
        ],
        components=[
            Component("Eyes", "organic", "See subtle differences"),
            Component("Hands", "organic", "Draw letterforms"),
        ],
        intensity_field={"beauty": 0.9, "curiosity": 0.8},
        becoming_vectors=["becoming-appreciator"],
        stratification_depth=0.2,
        lines_of_flight=[
            LineOfFlight(
                direction="Professional typography career",
                source_type="assemblage potential",
                source_description="Typography skill + beauty 0.9 could actualize as graphic design, printing, publishing",
                trigger_conditions="Encounter with design firm, print shop, or art school"
            ),
            LineOfFlight(
                direction="Aesthetics applied elsewhere",
                source_type="assemblage potential", 
                source_description="Trained aesthetic eye (beauty 0.9) could transfer to any visual domain - unknown what",
                trigger_conditions="Encounter with different visual medium requiring aesthetic judgment"
            )
        ],
        virtual_capacities=[]
    )
    
    garage_tinkerer = Assemblage(
        name="Electronics-Tinkerer-1972",
        abstract_machine="(Components + Circuits + Experimentation) => (???)",
        territories=[
            Territory("Parents' garage", "Build circuits", "Exploratory", "smooth"),
        ],
        codes=[
            Code("HP parts scavenging", "Call companies for free parts", "hustle", "molar"),
        ],
        components=[
            Component("Hands", "organic", "Solder, assemble"),
            Component("Oscilloscope", "technical", "Test circuits"),
        ],
        intensity_field={"curiosity": 0.8, "technical_confidence": 0.6},
        becoming_vectors=["becoming-engineer"],
        stratification_depth=0.3,
        lines_of_flight=[
            LineOfFlight(
                direction="Electrical engineering career",
                source_type="assemblage potential",
                source_description="Technical skill + confidence 0.6 suggests engineering path",
                trigger_conditions="College major, HP job offer, technical company"
            ),
            LineOfFlight(
                direction="Entrepreneurial electronics",
                source_type="assemblage potential",
                source_description="Garage experimentation + hustle could become product business",
                trigger_conditions="Encounter with marketable invention or business partner"
            )
        ],
        virtual_capacities=[]
    )
    
    # TRANSVERSAL LINE OF FLIGHT (intersection unknown in 1972):
    # Calligraphy Eyes + Engineering Hands = ??? 
    # We DON'T KNOW it's "beautiful computers" yet - that concept doesn't exist
    # The potential is REAL but UNACTUALIZED
    
    return [calligraphy_student, garage_tinkerer]


# ============================================================
# 1976: Apple Computer Founding
# ============================================================

def steve_jobs_1976():
    """
    Age 21, just founded Apple with Wozniak.
    NOW we can see calligraphy + engineering composing.
    """
    
    apple_cofounder = Assemblage(
        name="Apple-Co-Founder-1976",
        abstract_machine="(Wozniak's Engineering + Jobs' Hustle + Garage) => (Computer Kits)",
        territories=[
            Territory("Jobs family garage", "Assemble Apple I", "Scrappy", "smooth"),
            Territory("Homebrew Computer Club", "Demo products", "Enthusiast", "smooth"),
        ],
        codes=[
            Code("$666.66 pricing", "Quirky price point", "marketing", "molar"),
            Code("Wozniak dependency", "Steve W does the engineering", "partnership", "molar"),
        ],
        components=[
            Component("Voice", "organic", "Pitch, sell, convince"),
            Component("Wozniak", "social", "Engineering genius, core capability"),
        ],
        intensity_field={"ambition": 0.8, "sales_confidence": 0.7, "technical_dependence": 0.9},
        becoming_vectors=["becoming-entrepreneur", "becoming-salesman"],
        stratification_depth=0.4,
        lines_of_flight=[
            LineOfFlight(
                direction="Professionalcompany with investment",
                source_type="tension",
                source_description="Ambition 0.8 + garage scrappiness creates desire for real company, capital, legitimacy",
                trigger_conditions="VC pitch, professional investor encounter"
            ),
            LineOfFlight(
                direction="Aesthetic differentiation",
                source_type="assemblage composition",
                source_description="Calligraphy aesthetic sense (beauty 0.9 from 1972) + computer market = make computers beautiful?",
                trigger_conditions="Product design choice moment, casing decisions"
            ),
            LineOfFlight(
                direction="Business failure",
                source_type="breaking_point",
                source_description="Technical dependence 0.9 on Wozniak = if he leaves, company collapses",
                trigger_conditions="Wozniak injury, departure, or conflict"
            )
        ],
        virtual_capacities=[
            VirtualCapacity(
                name="Design-driven product strategy",
                access_point="Calligraphy training (1972 assemblage still latent)",
                reason_unactualized="Haven't applied aesthetics to technology yet, computers are beige boxes",
                actualization_trigger="Decision point: make Apple II look different/better?"
            )
        ]
    )
    
    return [apple_cofounder]


# ============================================================
# 2003: Cancer Diagnosis
# ============================================================

def steve_jobs_2003():
    """
    Age 48, just diagnosed with pancreatic cancer.
    Multiple assemblages in conflict, TRUE uncertainty about outcome.
    """
    
    zen_practitioner = Assemblage(
        name="Zen-Practitioner-2003",
        abstract_machine="(Meditation + Intuition + Natural) => (Clarity + Health?)",
        territories=[
            Territory("Tassajara retreat", "Multi-day meditation", "Austere", "smooth"),
        ],
        codes=[
            Code("Trust intuition over science", "Inner knowing", "belief", "molecular"),
            Code("Body purification through diet", "Fruitarian, vegan", "practice", "molar"),
        ],
        components=[
            Component("Body", "organic", "Temple, self-healing capacity"),
            Component("Intuition", "organic", "Inner guidance system"),
        ],
        intensity_field={"intuition_trust": 0.9, "science_distrust": 0.6},
        becoming_vectors=["becoming-natural-healer"],
        stratification_depth=0.2,
        lines_of_flight=[
            LineOfFlight(
                direction="Natural treatment path",
                source_type="assemblage potential",
                source_description="Intuition trust 0.9 + science distrust 0.6 suggests alternative medicine first",
                trigger_conditions="Cancer diagnosis - choice point between surgery vs alternatives"
            ),
            LineOfFlight(
                direction="Spiritual acceptance of death",
                source_type="assemblage potential",
                source_description="Zen practice includes accepting impermanence, could choose no treatment",
                trigger_conditions="Confronting mortality, meditation on death"
            )
        ],
        virtual_capacities=[]
    )
    
    medical_patient = Assemblage(
        name="Medical-Patient-2003",
        abstract_machine="(Diagnosis + Doctors + Protocol) => (Survival?)",
        territories=[
            Territory("Stanford oncology", "Scans, consultations", "Clinical", "striated"),
        ],
        codes=[
            Code("Immediate surgery recommended", "Medical protocol", "protocol", "molar"),
            Code("Survival statistics", "Curative if early", "fact", "molar"),
        ],
        components=[
            Component("Body", "organic", "Diseased, needs intervention"),
            Component("Medical team", "social", "Expert knowledge, pressure"),
        ],
        intensity_field={"fear": 0.7, "urgency": 0.8, "protocol_trust": 0.5},
        becoming_vectors=["becoming-patient", "becoming-survivor"],
        stratification_depth=0.9,
        lines_of_flight=[
            LineOfFlight(
                direction="Immediate surgical treatment",
                source_type="assemblage potential",
                source_description="Urgency 0.8 + medical pressure suggests following protocol",
                trigger_conditions="Accept doctor recommendation, schedule surgery"
            ),
            LineOfFlight(
                direction="Second opinion delay",
                source_type="tension",
                source_description="Protocol trust only 0.5, might seek alternatives before committing",
                trigger_conditions="Research other doctors, other hospitals, other approaches"
            )
        ],
        virtual_capacities=[]
    )
    
    # TRANSVERSAL LINE OF FLIGHT (DEADLY POTENTIAL):
    # Zen intuition 0.9 CONFLICTS with Medical urgency 0.8
    # IF Zen assemblage dominates: delay surgery
    # IF Medical assemblage dominates: immediate surgery
    # This is GENUINE UNCERTAINTY - we don't know which actualizes
    
    transversal_conflict = LineOfFlight(
        direction="Treatment delay gamble",
        source_type="inter-assemblage conflict",
        source_description="Zen (intuition 0.9, science-distrust 0.6) vs Medical (urgency 0.8, protocol-trust 0.5) = incompatible treatment philosophies",
        trigger_conditions="Decision moment: surgery date or try alternatives first?"
    )
    
    return [zen_practitioner, medical_patient], [transversal_conflict]


if __name__ == "__main__":
    print("STEVE JOBS: PROSPECTIVE ASSEMBLAGE ANALYSIS")
    print("=" * 60)
    print("\nModeling lines of flight as POTENTIALS at each moment\n")
    
    print("\n1972: Reed College")
    print("-" * 40)
    asms_1972 = steve_jobs_1972()
    for asm in asms_1972:
        print(f"\n{asm.name}")
        for lof in asm.lines_of_flight:
            print(f"  → {lof.direction}")
            print(f"     {lof.source_description}")
    
    print("\n\n1976: Apple Founding")
    print("-" * 40)
    asms_1976 = steve_jobs_1976()
    for asm in asms_1976:
        print(f"\n{asm.name}")
        for lof in asm.lines_of_flight:
            print(f"  → {lof.direction}")
            print(f"     {lof.source_description}")
    
    print("\n\n2003: Cancer Diagnosis") 
    print("-" * 40)
    asms_2003, transversal_2003 = steve_jobs_2003()
    for asm in asms_2003:
        print(f"\n{asm.name}")
        for lof in asm.lines_of_flight:
            print(f"  → {lof.direction}")
            print(f"     {lof.source_description}")
    
    print("\n\nTRANSVERSAL CONFLICT:")
    for lof in transversal_2003:
        print(f"  → {lof.direction}")
        print(f"     {lof.source_description}")
