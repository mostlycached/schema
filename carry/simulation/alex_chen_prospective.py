"""
Alex Chen, 1972: Prospective Assemblage Model
Fictional person to avoid backward-reasoning bias.
Swapped calligraphy → chess to eliminate Steve Jobs pattern-matching.
"""

from carry.simulation.assemblage import (
    Assemblage, Territory, Code, Component, LineOfFlight, VirtualCapacity
)

# ============================================================
# Alex Chen, 1972 (Age 17): Reed College
# ============================================================

def alex_chen_1972():
    """
    College dropout, auditing random classes.
    Genuinely don't know where this goes.
    """
    
    chess_student = Assemblage(
        name="Chess-Student-1972",
        abstract_machine="(Strategy Study + Pattern Recognition) => (???)",
        territories=[
            Territory("Reed College chess club", "Weekly games", "Competitive", "smooth"),
            Territory("Library chess corner", "Study grandmaster games", "Solitary", "smooth"),
        ],
        codes=[
            Code("Opening repertoire", "Memorized positions", "pattern", "molecular"),
            Code("Endgame calculation", "Think 10 moves ahead", "practice", "molar"),
        ],
        components=[
            Component("Mind", "organic", "Calculate, see patterns"),
            Component("Eyes", "organic", "Read board state"),
        ],
        intensity_field={"strategic_thinking": 0.9, "pattern_recognition": 0.85, "competitiveness": 0.7},
        becoming_vectors=["becoming-strategist"],
        stratification_depth=0.6,  # Chess has rigid rules (striated) but creative play (smooth)
        lines_of_flight=[
            LineOfFlight(
                direction="Professional chess player",
                source_type="assemblage potential",
                source_description="Strategic thinking 0.9 + competitiveness 0.7 could actualize as tournament career",
                trigger_conditions="Chess tournament invitation, sponsorship, or coach encounter"
            ),
            LineOfFlight(
                direction="Chess teaching/coaching",
                source_type="assemblage potential",
                source_description="Pattern recognition 0.85 + study practice could become pedagogy",
                trigger_conditions="Younger player asking for lessons, or youth program opportunity"
            ),
            LineOfFlight(
                direction="Strategy applied elsewhere",
                source_type="assemblage potential",
                source_description="Strategic mind (0.9) could transfer to any domain requiring planning - UNKNOWN what domain",
                trigger_conditions="Encounter with different field needing strategic thinking"
            )
        ],
        virtual_capacities=[]
    )
    
    electronics_tinkerer = Assemblage(
        name="Electronics-Tinkerer-1972",
        abstract_machine="(Components + Circuits + Experimentation) => (???)",
        territories=[
            Territory("Shared apartment workbench", "Solder circuits", "Exploratory", "smooth"),
            Territory("Radio Shack", "Buy parts", "Consumer", "striated"),
        ],
        codes=[
            Code("Fix-it instinct", "Take things apart to understand", "pattern", "molecular"),
            Code("Component scavenging", "Salvage parts from broken devices", "practice", "molar"),
        ],
        components=[
            Component("Hands", "organic", "Solder, assemble, wire"),
            Component("Multimeter", "technical", "Test voltage, debug"),
        ],
        intensity_field={"curiosity": 0.8, "technical_confidence": 0.5, "resourcefulness": 0.7},
        becoming_vectors=["becoming-engineer"],
        stratification_depth=0.4,
        lines_of_flight=[
            LineOfFlight(
                direction="Engineering degree/career",
                source_type="assemblage potential",
                source_description="Technical confidence 0.5 is modest but curiosity 0.8 is high - could pursue formal education",
                trigger_conditions="University re-enrollment, engineering program, or technical job offer"
            ),
            LineOfFlight(
                direction="Repair shop/technical service",
                source_type="assemblage potential",
                source_description="Fix-it skill + resourcefulness 0.7 suggests service business",
                trigger_conditions="Friend asks for repair, or encounter with broken equipment market"
            ),
            LineOfFlight(
                direction="Invention/product creation",
                source_type="assemblage potential",
                source_description="Experimentation + curiosity could lead to building new devices",
                trigger_conditions="Idea for useful product, or encounter with unfilled need"
            )
        ],
        virtual_capacities=[]
    )
    
    # TRANSVERSAL (COMPOSITIONAL) LINE OF FLIGHT:
    # Chess strategic thinking + Electronics hands = ??? 
    # Could be: game design, AI research, strategy software, chess computers, OR something totally different
    # WE DON'T KNOW - genuinely multiple possibilities
    
    transversal_compositional = LineOfFlight(
        direction="Strategic-technical hybrid domain (unknown)",
        source_type="assemblage composition",
        source_description="Chess mind (strategic 0.9, pattern 0.85) + Electronics hands (curiosity 0.8) = capacity for domain requiring both logic and building. Possibilities: game design, automation, programming, chess computers, educational tech, or unknown",
        trigger_conditions="Encounter with field that needs both strategic thinking AND technical building"
    )
    
    typography_student = Assemblage(
        name="Typography-Student-1972",
        abstract_machine="(Letterform Study + Aesthetic Training) => (???)",
        territories=[
            Territory("Reed College printshop", "Typesetting practice", "Craft", "smooth"),
            Territory("Graphic design classroom", "Layout principles", "Academic", "striated"),
        ],
        codes=[
            Code("Serif appreciation", "Seeing letter beauty", "pattern", "molecular"),
            Code("Kerning instinct", "Letter spacing feel", "pattern", "molecular"),
        ],
        components=[
            Component("Eyes", "organic", "See subtle aesthetic differences"),
            Component("Hands", "organic", "Set type, arrange layout"),
        ],
        intensity_field={"beauty": 0.9, "precision": 0.8, "visual_thinking": 0.85},
        becoming_vectors=["becoming-designer"],
        stratification_depth=0.3,
        lines_of_flight=[
            LineOfFlight(
                direction="Graphic design career",
                source_type="assemblage potential",
                source_description="Beauty 0.9 + precision 0.8 suggests commercial design, advertising, publishing",
                trigger_conditions="Design firm internship, agency job offer"
            ),
            LineOfFlight(
                direction="Fine art/letterpress",
                source_type="assemblage potential",
                source_description="Craft territory + visual thinking 0.85 could become art practice",
                trigger_conditions="Gallery encounter, artist community"
            ),
            LineOfFlight(
                direction="Aesthetics applied elsewhere",
                source_type="assemblage potential",
                source_description="Trained visual eye could transfer to any domain requiring aesthetic judgment - UNKNOWN what",
                trigger_conditions="Encounter with different field needing visual sense"
            )
        ],
        virtual_capacities=[]
    )
    
    # TRANSVERSAL LINES (3-way intersection now!)
    
    transversal_chess_electronics = LineOfFlight(
        direction="Strategic-technical hybrid (unknown)",
        source_type="assemblage composition",
        source_description="Chess (strategic 0.9) + Electronics (curiosity 0.8) = capacity for logical-building domain. Possibilities: game AI, automation, programming, chess computers",
        trigger_conditions="Encounter with field needing both strategy AND building"
    )
    
    transversal_chess_typography = LineOfFlight(
        direction="Strategic-aesthetic hybrid (unknown)",
        source_type="assemblage composition",
        source_description="Chess (pattern 0.85) + Typography (beauty 0.9) = capacity for structured beauty. Possibilities: layout design, information architecture, game board design, visual logic puzzles",
        trigger_conditions="Encounter with field needing both logical structure AND visual beauty"
    )
    
    transversal_electronics_typography = LineOfFlight(
        direction="Technical-aesthetic hybrid (unknown)",
        source_type="assemblage composition",
        source_description="Electronics (building) + Typography (visual) = capacity for beautiful devices. Possibilities: industrial design, interface design, signage electronics, display technology",
        trigger_conditions="Encounter with field needing both technical skill AND aesthetic judgment"
    )
    
    transversal_all_three = LineOfFlight(
        direction="Strategic-technical-aesthetic triple hybrid (truly unknown)",
        source_type="assemblage composition",
        source_description="Chess (strategic 0.9) + Electronics (curiosity 0.8) + Typography (beauty 0.9) = rare triple capacity. Possibilities: ???. Could be interface design, game design, visual programming, information visualization, educational tech, or something that doesn't exist yet",
        trigger_conditions="Encounter with novel field requiring ALL THREE: logic, building, and beauty"
    )
    
    return [chess_student, electronics_tinkerer, typography_student], [transversal_chess_electronics, transversal_chess_typography, transversal_electronics_typography, transversal_all_three]


if __name__ == "__main__":
    print("ALEX CHEN 1972: PROSPECTIVE ASSEMBLAGE MODEL")
    print("=" * 60)
    print("Fictional person - no backward reasoning possible\n")
    
    asms, transversal = alex_chen_1972()
    
    for asm in asms:
        print(f"\n{asm.name}")
        print(f"  Intensities: {asm.intensity_field}")
        print(f"\n  POTENTIAL LINES OF FLIGHT:")
        for lof in asm.lines_of_flight:
            print(f"    → {lof.direction}")
            print(f"       {lof.source_description}")
            print()
    
    print("\nTRANSVERSAL COMPOSITIONAL LINE:")
    for lof in transversal:
        print(f"  → {lof.direction}")
        print(f"     {lof.source_description}")
        print(f"     Trigger: {lof.trigger_conditions}")
    
    print("\n" + "=" * 60)
    print("QUESTION: Which line actualizes?")
    print("ANSWER: We genuinely don't know. Multiple paths are structurally possible.")
    print("This is the Deleuzian virtual - REAL potentials, not yet actual.")
