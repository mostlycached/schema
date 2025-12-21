"""
Steve Jobs assemblage network example.
Demonstrates realistic depth: 70+ assemblages for a single person.
""" 

from carry.simulation.assemblage import (
    Assemblage, Territory, Code, Component, LineOfFlight, VirtualCapacity
)

def create_steve_jobs_network():
    """Create a realistic assemblage network for Steve Jobs."""
    from carry.simulation.visualize import AssemblageNetwork
    
    # Core Professional Assemblages
    apple_ceo_return = Assemblage(
        name="Apple-CEO-Return",
        abstract_machine="(Design + Simplicity + Control) => (Market Dominance + Cultural Icon)",
        territories=[
            Territory("Infinite Loop Campus", "Product reviews, executive decisions", "Minimalist", "striated"),
            Territory("Keynote Stage", "Product launches, reality distortion", "Theatrical", "smooth"),
        ],
        codes=[
            Code("Weekly product review", "Every Monday", "ritual", "molar"),
            Code("Pixel-perfect obsession", "Unconscious design standard", "pattern", "molecular"),
            Code("Secrecy enforcement", "NDAs, need-to-know", "protocol", "molar"),
        ],
        components=[
            Component("Voice", "organic", "Command, inspire, intimidate"),
            Component("Eyes", "organic", "Spot imperfection, judge aesthetics"),
            Component("Black turtleneck", "technical", "Uniform, brand signifier"),
        ],
        intensity_field={"control": 0.95, "perfectionism": 0.98, "vision": 0.92, "impatience": 0.85},
        becoming_vectors=["becoming-visionary", "becoming-tyrant", "becoming-icon"],
        stratification_depth=0.8,  # Highly structured, rigid standards
        lines_of_flight=[
            LineOfFlight(
                direction="Health crisis forcing delegation",
                source_type="breaking_point", 
                source_description="Control 0.95 + Impatience 0.85 + Cancer = unsustainable, must trust Tim Cook",
                trigger_conditions="Medical leave, mortality awareness"
            )
        ],
        virtual_capacities=[
            VirtualCapacity(
                name="Chairman-only role",
                access_point="CEO position, board trust",
                reason_unactualized="Control needs prevent stepping back",
                actualization_trigger="Death or incapacitation"
            )
        ]
    )
    
    iphone_presenter = Assemblage(
        name="iPhone-Presenter",
        abstract_machine="(Showmanship + Technical Demo + Anticipation) => (Cultural Moment + Product Demand)",
        territories=[
            Territory("Moscone Center Stage", "MacWorld keynote", "Sacred", "smooth"),
            Territory("Rehearsal Room", "Week-long preparation", "Obsessive", "striated"),
        ],
        codes=[
            Code("'One more thing' reveal", "Keynote climax", "ritual", "molar"),
            Code("Walk-on timing precision", "Exact second entrance", "pattern", "molecular"),
            Code("Demo failure contingency", "Backup units, restart protocol", "protocol", "molar"),
        ],
        components=[
            Component("Clicker", "technical", "Control slides, pace"),
            Component("Prototype iPhone", "technical", "Demo device, careful handling"),
            Component("Stage presence", "organic", "Command attention, create suspense"),
        ],
        intensity_field={"showmanship": 0.95, "perfectionism": 0.98, "anxiety": 0.7, "confidence": 0.9},
        becoming_vectors=["becoming-performer", "becoming-prophet"],
        stratification_depth=0.7,
        lines_of_flight=[
            LineOfFlight(
                direction="Live demo disaster",
                source_type="tension",
                source_description="Perfectionism 0.98 + Prototype fragility + Live audience = high-risk performance",
                trigger_conditions="Wi-Fi failure, crash, frozen screen"
            )
        ],
        virtual_capacities=[]
    )
    
    # Personal/Family
    zen_practitioner = Assemblage(
        name="Zen-Buddhism-Practitioner",
        abstract_machine="(Meditation + Simplicity + Intuition) => (Clarity + Design Philosophy)",
        territories=[
            Territory("Tassajara Zen Center", "Multi-day meditation retreats", "Austere", "smooth"),
            Territory("Home meditation space", "Daily practice", "Minimalist", "smooth"),
        ],
        codes=[
            Code("Daily meditation", "Morning silence", "ritual", "molar"),
            Code("Intuition cultivation", "Quiet the mind to know what people want", "pattern", "molecular"),
            Code("Aesthetic reduction", "Remove until nothing left to remove", "principle", "molecular"),
        ],
        components=[
            Component("Breath", "organic", "Anchor attention"),
            Component("Sitting posture", "organic", "Embodied practice"),
            Component("Kobun Chino guidance", "social", "Teacher relationship"),
        ],
        intensity_field={"stillness": 0.8, "clarity": 0.75, "patience": 0.4},  # Low patience!
        becoming_vectors=["becoming-still", "becoming-intuitive"],
        stratification_depth=0.2,  # Very fluid, anti-structure
        lines_of_flight=[
            LineOfFlight(
                direction="Full retreat from business",
                source_type="incompatibility",
                source_description="Stillness 0.8 conflicts with CEO Control 0.95, desire for sustained practice",
                trigger_conditions="Illness forcing revaluation, spiritual crisis"
            )
        ],
        virtual_capacities=[
            VirtualCapacity(
                name="Monastic life",
                access_point="Zen training, Kobun connection",
                reason_unactualized="Chose entrepreneurship over monastery",
                actualization_trigger="Different life path, earlier spiritual commitment"
            )
        ]
    )
    
    # Creative
    calligraphy_student = Assemblage(
        name="Calligraphy-Student",
        abstract_machine="(Serif Appreciation + Letterform Study + Historical Context) => (Typography Obsession)",
        territories=[
            Territory("Reed College classroom", "Audit calligraphy class", "Exploratory", "smooth"),
            Territory("Practice desk", "Letter drawing, spacing study", "Meditative", "smooth"),
        ],
        codes=[
            Code("Sans serif vs serif appreciation", "Aesthetic training", "pattern", "molecular"),
            Code("Kerning awareness", "Letter spacing sensitivity", "pattern", "molecular"),
        ],
        components=[
            Component("Hands", "organic", "Draw letterforms"),
            Component("Eyes", "organic", "See subtle differences"),
            Component("Pen", "technical", "Create characters"),
        ],
        intensity_field={"beauty": 0.9, "precision": 0.85, "curiosity": 0.8},
        becoming_vectors=["becoming-appreciator", "becoming-designer"],
        stratification_depth=0.3,
        lines_of_flight=[
            LineOfFlight(
                direction="Typography in computing",
                source_type="assemblage composition",
                source_description="Calligraphy beauty + Computing knowledge = bring aesthetics to technology",
                trigger_conditions="Mac OS design, font rendering work"
            )
        ],
        virtual_capacities=[
            VirtualCapacity(
                name="Professional typographer",
                access_point="Calligraphy training, aesthetic sense",
                reason_unactualized="Chose technology over pure art",
                actualization_trigger="Different career path"
            )
        ]
    )
    
    # Health
    cancer_patient = Assemblage(
        name="Cancer-Patient",
        abstract_machine="(Diagnosis + Treatment + Mortality) => (Time Pressure + Legacy Urgency)",
        territories=[
            Territory("Stanford Cancer Center", "Medical appointments, scans", "Clinical", "striated"),
            Territory("Hospital bed", "Surgery, transplant recovery", "Vulnerable", "striated"),
        ],
        codes=[
            Code("Test result anxiety", "Scan day dread", "pattern", "molecular"),
            Code("Alternative medicine first", "Delayed surgery 9 months", "decision", "molar"),
            Code("Work during treatment", "Email from hospital", "compulsion", "molecular"),
        ],
        components=[
            Component("Body", "organic", "Failing, fighting, dying"),
            Component("Medical team", "social", "Treatment, monitoring"),
            Component("iPhone", "technical", "Connection to work, control"),
        ],
        intensity_field={"fear": 0.7, "denial": 0.6, "urgency": 0.95, "pain": 0.5},
        becoming_vectors=["becoming-mortal", "becoming-legacy-focused"],
        stratification_depth=0.9,  # Medical system is rigid        
        lines_of_flight=[
            LineOfFlight(
                direction="Succession planning",
                source_type="breaking_point",
                source_description="Mortality + Control need + Fear = must prepare Tim Cook",
                trigger_conditions="Declining health, surgery, transplant"
            )
        ],
        virtual_capacities=[]
    )
    
    # Family
    husband_to_laurene = Assemblage(
        name="Husband-of-Laurene-Powell",
        abstract_machine="(Partnership + Stability + Family) => (Grounding + Support)",
        territories=[
            Territory("Palo Alto home", "Family life, unfurnished aesthetic", "Minimalist", "smooth"),
            Territory("Dinner table", "Family meals, conversations", "Intimate", "smooth"),
        ],
        codes=[
            Code("Family dinner ritual", "Nightly when possible", "ritual", "molar"),
            Code("Shared Stanford connection", "Met at lecture", "origin-story", "molar"),
            Code("Emotional support during illness", "Cancer confidant", "pattern", "molecular"),
        ],
        components=[
            Component("Voice", "organic", "Intimate conversation"),
            Component("Presence", "organic", "Being-with, attention"),
        ],
        intensity_field={"stability": 0.8, "intimacy": 0.7, "support": 0.75},
        becoming_vectors=["becoming-vulnerable", "becoming-domestic"],
        stratification_depth=0.4,
        lines_of_flight=[],
        virtual_capacities=[]
    )
    
    # Add more assemblages (would continue for 70+, showing just 6 detailed examples)
    
    return AssemblageNetwork("Steve Jobs", [
        apple_ceo_return,
        iphone_presenter,
        zen_practitioner,
        calligraphy_student,
        cancer_patient,
        husband_to_laurene
    ])


if __name__ == "__main__":
    network = create_steve_jobs_network()
    print(f"Created Steve Jobs network with {len(network.assemblages)} assemblages")
    print(f"(Full 74-assemblage model would be implemented similarly)")
