"""
Schizoanalysis Module: A Pure Deleuze-Guattari Simulation

This module implements a simulation based on the concepts from
Anti-Oedipus and A Thousand Plateaus. It differs from the biographical
model in fundamental ways:

BIOGRAPHICAL MODEL         SCHIZOANALYTIC MODEL
-------------------------------------------------------------------
Phase (developmental)  ->  Plateau (intensive, non-developmental)
Habitus (self)         ->  Body without Organs (intensive surface)
Component (part of     ->  Desiring-Machine (partial object, coupling)
           agent)
Encounter (event)      ->  Cut (break in flow, production)
Narrative Arc          ->  Flows (no predetermined form)
Other (Oedipal)        ->  Abstract Machine (non-signifying)
Institution            ->  Stratum (organism, signification, subjectification)
Wound (trauma)         ->  Inscription (intensity on BwO)
Phase Transition       ->  Lines of Flight / Reterritorialization

Key principles:
1. NO DEVELOPMENT - plateaus are not stages, they are intensive regions
2. NO COHERENT SELF - the BwO is a surface, not a center
3. PRODUCTION > REPRESENTATION - desiring-machines produce, not represent
4. RHIZOMATIC - any point can connect to any other point
5. ESCAPE IS POSSIBLE - lines of flight can be absolute
"""

import os
import json
import random
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Set
from enum import Enum

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


# =============================================================================
# THE THREE STRATA
# =============================================================================

class Stratum(Enum):
    """
    The three great strata that bind us (ATP, "Geology of Morals"):
    - ORGANISM: You will be organized, you will be an organism
    - SIGNIFICATION: You will signify and be signified, you will interpret
    - SUBJECTIFICATION: You will be a subject, nailed to a dominant reality
    """
    ORGANISM = "organism"           # The body as organized, functional
    SIGNIFICATION = "signification" # Language, meaning, interpretation
    SUBJECTIFICATION = "subjectification"  # Identity, the "I"


# =============================================================================
# DESIRING-MACHINES
# =============================================================================

@dataclass
class DesiringMachine:
    """
    A partial object that couples with other machines to produce.
    
    "Everywhere it is machines - real ones, not figurative ones:
    machines driving other machines, machines being driven by other machines,
    with all the necessary couplings and connections." (AO, p.1)
    
    Unlike components (which belong to an agent), desiring-machines
    are pre-individual, they don't belong to anyone.
    """
    name: str
    
    # What it can couple with
    input_flows: List[str] = field(default_factory=list)  # What it can receive
    output_flows: List[str] = field(default_factory=list)  # What it produces
    
    # Current state
    active: bool = False
    intensity: float = 0.0  # 0-1, current charge
    
    # History of couplings (not a linear narrative, just recordings)
    couplings: List[Tuple[str, float]] = field(default_factory=list)  # (other_machine, intensity)


# Archetypal desiring-machines (not exhaustive, rhizomatically extensible)
DESIRING_MACHINES = {
    "mouth-machine": DesiringMachine(
        name="mouth-machine",
        input_flows=["food", "words", "breath", "kisses"],
        output_flows=["speech", "screams", "silence", "consumption"],
    ),
    "eye-machine": DesiringMachine(
        name="eye-machine",
        input_flows=["light", "images", "faces", "text"],
        output_flows=["gaze", "recognition", "surveillance", "blindness"],
    ),
    "hand-machine": DesiringMachine(
        name="hand-machine",
        input_flows=["textures", "tools", "skin", "objects"],
        output_flows=["grasp", "caress", "violence", "craft"],
    ),
    "anus-machine": DesiringMachine(
        name="anus-machine",
        input_flows=["waste", "shame", "accumulation"],
        output_flows=["expulsion", "retention", "money", "gift"],
    ),
    "celibate-machine": DesiringMachine(
        name="celibate-machine",
        input_flows=["desire", "frustration", "fantasy"],
        output_flows=["sublimation", "intensity", "creation", "breakdown"],
    ),
}


# =============================================================================
# BODY WITHOUT ORGANS (BwO)
# =============================================================================

@dataclass
class BodyWithoutOrgans:
    """
    The BwO is not the opposite of the organs. It is opposed to the
    organization of the organs insofar as it composes an organism.
    
    "The BwO is what remains when you take everything away.
    What you take away is precisely the phantasy, and significances
    and subjectifications as a whole." (ATP, p.151)
    
    The BwO is a recording surface for intensities - not a self,
    not a narrative, just a field of intensive differences.
    """
    # Intensities are recorded as points on the BwO
    # Each intensity has a name and a value (not meaning, just degree)
    intensities: Dict[str, float] = field(default_factory=dict)
    
    # Inscriptions are marks left by cuts (not traumas, just marks)
    inscriptions: List[str] = field(default_factory=list)
    
    # Which machines are currently plugged in
    active_machines: List[str] = field(default_factory=list)
    
    # The BwO can be more or less stratified
    stratification_level: float = 0.5  # 0 = totally destratified, 1 = fully organized
    
    # Zones of intensity (not organs, not locations, just intensive regions)
    zones: Dict[str, float] = field(default_factory=dict)  # zone_name -> intensity
    
    def record_intensity(self, name: str, value: float) -> None:
        """Record an intensity on the BwO."""
        current = self.intensities.get(name, 0.0)
        # Intensities accumulate but can also discharge
        self.intensities[name] = min(1.0, max(0.0, current + value * 0.3))
    
    def inscribe(self, mark: str) -> None:
        """Leave an inscription on the BwO."""
        self.inscriptions.append(mark)
    
    def plug_in(self, machine: str) -> None:
        """Plug a machine into the BwO."""
        if machine not in self.active_machines:
            self.active_machines.append(machine)
    
    def unplug(self, machine: str) -> None:
        """Unplug a machine from the BwO."""
        if machine in self.active_machines:
            self.active_machines.remove(machine)
    
    def destratify(self, amount: float = 0.1) -> None:
        """Destratify the BwO (dangerous in excess)."""
        self.stratification_level = max(0.0, self.stratification_level - amount)
    
    def restratify(self, amount: float = 0.1) -> None:
        """Restratify the BwO (recapture)."""
        self.stratification_level = min(1.0, self.stratification_level + amount)


# =============================================================================
# FLOWS AND CUTS
# =============================================================================

@dataclass
class Flow:
    """
    A flow is not an event, not a narrative moment, but a current.
    
    Flows of desire, money, words, milk, shit, energy.
    The simulation tracks flows, not events.
    """
    name: str
    type: str  # "desire", "capital", "language", "energy", "material"
    intensity: float = 0.5  # Current intensity of the flow
    
    # What can cut this flow
    vulnerable_to: List[str] = field(default_factory=list)
    
    # Where it can go
    possible_connections: List[str] = field(default_factory=list)


@dataclass
class Cut:
    """
    A cut is what desiring-machines do to flows.
    
    "The desiring-machine is not a metaphor... It is a machine,
    and it works - that is, it produces cuts and flows." (AO)
    
    A cut is not an event (with meaning) but a break-flow operation.
    """
    machine: str  # Which machine performed the cut
    flow: str  # Which flow was cut
    intensity: float  # How intensive the cut was
    
    # What was produced by the cut
    production: str = ""
    
    # Did this lead somewhere?
    connection: Optional[str] = None  # What got connected
    breakage: Optional[str] = None  # What got broken


# =============================================================================
# PLATEAU
# =============================================================================

@dataclass
class Plateau:
    """
    "A plateau is always in the middle, not at the beginning or the end.
    A rhizome is made of plateaus." (ATP)
    
    A plateau is NOT a phase, NOT a stage of development.
    It is an intensive region, a continuous, self-vibrating region.
    
    You can enter any plateau from any other plateau.
    """
    name: str
    
    # A plateau has characteristic intensities, not events
    characteristic_intensities: Dict[str, float] = field(default_factory=dict)
    
    # Which machines tend to be active here
    active_machines: List[str] = field(default_factory=list)
    
    # What flows pass through
    flows: List[str] = field(default_factory=list)
    
    # Connections to other plateaus (rhizomatic, not linear)
    connections: Set[str] = field(default_factory=set)
    
    # Intensity level (not progress, just current charge)
    intensity: float = 0.5
    
    # How stratified is this plateau
    stratum: Optional[Stratum] = None


# Some archetypal plateaus (from ATP's table of contents, reimagined)
PLATEAUS = {
    "0: intensity": Plateau(
        name="0: intensity",
        characteristic_intensities={"becoming": 0.8, "zero": 0.3},
        active_machines=["celibate-machine"],
        flows=["pure_intensity"],
    ),
    "1914-becoming-animal": Plateau(
        name="1914-becoming-animal",
        characteristic_intensities={"animal": 0.7, "pack": 0.6, "contagion": 0.5},
        active_machines=["mouth-machine", "eye-machine"],
        flows=["affect", "territory"],
    ),
    "year-zero-faciality": Plateau(
        name="year-zero-faciality",
        characteristic_intensities={"face": 0.9, "white-wall": 0.7, "black-hole": 0.8},
        active_machines=["eye-machine"],
        flows=["signification", "subjectification"],
        stratum=Stratum.SUBJECTIFICATION,
    ),
    "how-to-make-yourself-a-bwo": Plateau(
        name="how-to-make-yourself-a-bwo",
        characteristic_intensities={"destratification": 0.9, "caution": 0.6},
        active_machines=["celibate-machine", "anus-machine"],
        flows=["organs", "organization"],
    ),
    "micropolitics-segmentarity": Plateau(
        name="micropolitics-segmentarity",
        characteristic_intensities={"molar": 0.5, "molecular": 0.7, "line-of-flight": 0.4},
        flows=["desire", "fascism", "paranoia"],
    ),
}


# =============================================================================
# ABSTRACT MACHINES
# =============================================================================

@dataclass 
class AbstractMachine:
    """
    An abstract machine is not a person, not a figure, not Oedipal.
    
    "Abstract machines operate within concrete assemblages...
    They are not metaphors but real diagrams." (ATP)
    
    Instead of "The Demanding Advisor" (Oedipal), we have
    abstract machines like "Faciality Machine", "Capture Machine",
    "War Machine", etc.
    """
    name: str
    type: str  # "faciality", "capture", "war", "abstract"
    
    # What it does
    operation: str  # "territorializes", "deterritorializes", "codes", "decodes"
    
    # What flows it operates on
    flows_affected: List[str] = field(default_factory=list)
    
    # Current intensity
    intensity: float = 0.5


ABSTRACT_MACHINES = {
    "faciality-machine": AbstractMachine(
        name="faciality-machine",
        type="faciality",
        operation="subjectifies",
        flows_affected=["recognition", "identity", "face"],
    ),
    "capture-machine": AbstractMachine(
        name="capture-machine",
        type="capture",
        operation="territorializes",
        flows_affected=["desire", "labor", "money"],
    ),
    "war-machine": AbstractMachine(
        name="war-machine",
        type="war",
        operation="deterritorializes",
        flows_affected=["territory", "order", "state"],
    ),
    "abstract-machine-of-overcoding": AbstractMachine(
        name="abstract-machine-of-overcoding",
        type="despotic",
        operation="overcodes",
        flows_affected=["all_flows"],
    ),
}


# =============================================================================
# LINES OF FLIGHT
# =============================================================================

class LineType(Enum):
    """
    Three kinds of lines that compose us (ATP, "Micropolitics"):
    """
    MOLAR = "molar"  # Hard, segmented, organized
    MOLECULAR = "molecular"  # Supple, micro-cracks
    FLIGHT = "flight"  # Absolute deterritorialization


@dataclass
class Line:
    """
    We are made of lines - not a unified self but intersecting lines.
    """
    type: LineType
    name: str
    intensity: float = 0.5
    
    # Where does it go?
    trajectory: List[str] = field(default_factory=list)  # Not linear, just points touched
    
    # Is it captured or free?
    captured: bool = False
    reterritorialized: bool = False


# =============================================================================
# THE SCHIZO (not a pathology, a process)
# =============================================================================

@dataclass
class SchizoProcess:
    """
    The schizophrenic process - not the clinical entity, but
    desiring-production in its pure state.
    
    "The schizo is not a revolutionary, but the schizophrenic process -
    broken off, confined, beaten down - is the potential for revolution." (AO)
    """
    body: BodyWithoutOrgans = field(default_factory=BodyWithoutOrgans)
    
    # Currently active plateau (but can jump anywhere)
    current_plateau: Optional[str] = None
    plateaus_touched: Set[str] = field(default_factory=set)
    
    # Machines currently in operation
    machines: Dict[str, DesiringMachine] = field(default_factory=dict)
    
    # Lines composing this process
    lines: List[Line] = field(default_factory=list)
    
    # All cuts performed
    cuts: List[Cut] = field(default_factory=list)
    
    # Abstract machines operating
    abstract_machines: List[str] = field(default_factory=list)
    
    # Flows currently in circulation
    active_flows: List[str] = field(default_factory=list)
    
    # Has the process broken down?
    broken_down: bool = False
    
    # Has it been recaptured by strata?
    recaptured: bool = False
    
    def perform_cut(self, machine_name: str, flow_name: str, intensity: float) -> Cut:
        """Have a machine perform a cut on a flow."""
        cut = Cut(
            machine=machine_name,
            flow=flow_name,
            intensity=intensity,
        )
        self.cuts.append(cut)
        self.body.record_intensity(f"cut-{flow_name}", intensity)
        return cut
    
    def enter_plateau(self, plateau_name: str) -> None:
        """Enter a plateau (not progress to it, just be on it)."""
        self.current_plateau = plateau_name
        self.plateaus_touched.add(plateau_name)
        
        # Plateaus affect the BwO
        if plateau_name in PLATEAUS:
            plateau = PLATEAUS[plateau_name]
            for intensity_name, value in plateau.characteristic_intensities.items():
                self.body.record_intensity(intensity_name, value * 0.2)
    
    def add_line(self, line_type: LineType, name: str) -> Line:
        """Add a line to the process."""
        line = Line(type=line_type, name=name)
        self.lines.append(line)
        return line
    
    def attempt_line_of_flight(self) -> Tuple[bool, str]:
        """
        Attempt a line of flight.
        
        Lines of flight can:
        1. Succeed (absolute deterritorialization - rare)
        2. Be reterritorialized (captured back)
        3. Turn back on themselves (become destructive)
        """
        roll = random.random()
        
        if self.body.stratification_level < 0.2:
            # Too destratified - dangerous
            return False, "The line collapsed into black hole - too fast, too much"
        
        if roll < 0.1:
            # Absolute deterritorialization (rare)
            line = self.add_line(LineType.FLIGHT, "absolute")
            return True, "A line of flight that does not return"
        elif roll < 0.5:
            # Reterritorialized
            line = self.add_line(LineType.FLIGHT, "reterritorialized") 
            line.reterritorialized = True
            self.body.restratify(0.2)
            return False, "The line was reterritorialized, captured back"
        else:
            # Molecular crack
            line = self.add_line(LineType.MOLECULAR, "crack")
            return False, "A molecular line, supple but not flight"


# =============================================================================
# SCHIZO SIMULATION
# =============================================================================

def run_schizo_process(
    name: str = "Anonymous Process",
    initial_intensity: float = 0.5,
    num_operations: int = 20,
    model_name: str = "gemini-2.0-flash",
) -> SchizoProcess:
    """
    Run a schizoanalytic simulation.
    
    Unlike a biography:
    - No phases, only plateaus
    - No development, only intensity variations
    - No coherent self, only BwO inscriptions
    - No narrative arc, only cuts and flows
    - Possible absolute deterritorialization
    """
    model = genai.GenerativeModel(model_name)
    
    # Initialize the process
    process = SchizoProcess()
    process.body.stratification_level = initial_intensity
    
    # Initialize some machines
    for machine_name, machine in DESIRING_MACHINES.items():
        process.machines[machine_name] = DesiringMachine(
            name=machine.name,
            input_flows=machine.input_flows.copy(),
            output_flows=machine.output_flows.copy(),
        )
    
    # Add initial molar lines (we all start stratified)
    process.add_line(LineType.MOLAR, "organism")
    process.add_line(LineType.MOLAR, "subject")
    
    # Enter initial plateau
    initial_plateaus = list(PLATEAUS.keys())
    process.enter_plateau(random.choice(initial_plateaus))
    
    print(f"\n{'='*60}")
    print(f"SCHIZOANALYTIC PROCESS: {name}")
    print(f"Initial stratification: {initial_intensity:.2f}")
    print(f"Starting plateau: {process.current_plateau}")
    print(f"{'='*60}\n")
    
    operations = []
    
    for i in range(num_operations):
        if process.broken_down:
            operations.append(("BREAKDOWN", "The process has broken down"))
            break
        
        if process.recaptured:
            operations.append(("RECAPTURED", "The process has been fully recaptured by strata"))
            break
        
        # Determine what operation to perform
        roll = random.random()
        
        if roll < 0.3:
            # CUT - a machine cuts a flow
            machine = random.choice(list(process.machines.keys()))
            flow = random.choice(["desire", "language", "money", "body", "territory"])
            intensity = random.uniform(0.2, 0.8)
            cut = process.perform_cut(machine, flow, intensity)
            
            # Generate what was produced
            prompt = f"""A desiring-machine ({machine}) cuts into a flow of {flow} with intensity {intensity:.2f}.
This is not an event with meaning, but a production. What is produced?
Write one fragment (not a sentence, not a narrative, just what was produced at the cut).
Examples: "milk-word", "grasp-nothing", "eye-that-does-not-see", "money-shit"
PRODUCTION:"""
            
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.9,
                        max_output_tokens=50
                    )
                )
                cut.production = response.text.strip().replace('"', '').lower()
            except:
                cut.production = f"{machine}-{flow}-cut"
            
            process.body.inscribe(cut.production)
            operations.append(("CUT", f"{machine} cuts {flow} → {cut.production}"))
        
        elif roll < 0.5:
            # PLATEAU JUMP - rhizomatic movement
            new_plateau = random.choice(list(PLATEAUS.keys()))
            if new_plateau != process.current_plateau:
                process.enter_plateau(new_plateau)
                operations.append(("PLATEAU", f"→ {new_plateau}"))
        
        elif roll < 0.65:
            # DESTRATIFICATION attempt
            amount = random.uniform(0.05, 0.15)
            process.body.destratify(amount)
            
            if process.body.stratification_level < 0.1:
                # Too much - emptied BwO (catatonic)
                process.broken_down = True
                operations.append(("DANGER", f"BwO emptied - stratification at {process.body.stratification_level:.2f}"))
            else:
                operations.append(("DESTRATIFY", f"↓ {amount:.2f} → stratification now {process.body.stratification_level:.2f}"))
        
        elif roll < 0.8:
            # RESTRATIFICATION (capture)
            abstract_machine = random.choice(list(ABSTRACT_MACHINES.keys()))
            amount = random.uniform(0.05, 0.15)
            process.body.restratify(amount)
            
            if process.body.stratification_level > 0.9:
                process.recaptured = True
                operations.append(("CAPTURE", f"{abstract_machine} recaptures → fully stratified"))
            else:
                operations.append(("STRATIFY", f"{abstract_machine} → stratification now {process.body.stratification_level:.2f}"))
        
        else:
            # LINE OF FLIGHT attempt
            success, description = process.attempt_line_of_flight()
            if success:
                operations.append(("FLIGHT", f"✈ {description}"))
            else:
                operations.append(("BLOCKED", description))
    
    # Print operations
    for op_type, description in operations:
        icon = {
            "CUT": "✂",
            "PLATEAU": "◆",
            "DESTRATIFY": "↓",
            "STRATIFY": "↑",
            "CAPTURE": "⚙",
            "FLIGHT": "✈",
            "BLOCKED": "✖",
            "DANGER": "⚠",
            "BREAKDOWN": "💥",
            "RECAPTURED": "🏛",
        }.get(op_type, "•")
        print(f"  {icon} {description}")
    
    print(f"\n{'='*60}")
    print(f"PROCESS COMPLETE")
    print(f"Plateaus touched: {len(process.plateaus_touched)}")
    print(f"Cuts performed: {len(process.cuts)}")
    print(f"Inscriptions: {len(process.body.inscriptions)}")
    print(f"Final stratification: {process.body.stratification_level:.2f}")
    print(f"Lines: {', '.join([l.type.value for l in process.lines])}")
    if process.broken_down:
        print("STATUS: BROKEN DOWN (emptied BwO)")
    elif process.recaptured:
        print("STATUS: RECAPTURED (fully stratified)")
    else:
        print("STATUS: IN PROCESS")
    print(f"{'='*60}")
    
    return process


def generate_schizo_report(process: SchizoProcess, output_path: str = None) -> str:
    """
    Generate a report of the schizoanalytic process.
    
    Unlike a biography report:
    - Non-linear structure
    - Lists of intensities, not narrative
    - Inscriptions on BwO, not events
    - No developmental arc
    """
    lines = [
        "# Schizo-Report",
        "",
        "> Not a biography. Not a narrative. A recording of intensities.",
        "",
    ]
    
    # BwO section
    lines.extend([
        "## Body without Organs",
        "",
        f"**Stratification Level**: {process.body.stratification_level:.2f}",
        "",
    ])
    
    # Intensities
    if process.body.intensities:
        lines.append("### Intensities Recorded")
        lines.append("")
        for name, value in sorted(process.body.intensities.items(), key=lambda x: -x[1])[:10]:
            bar = "█" * int(value * 10)
            lines.append(f"- `{name}`: {bar} ({value:.2f})")
        lines.append("")
    
    # Inscriptions
    if process.body.inscriptions:
        lines.extend([
            "### Inscriptions",
            "",
            "> Marks left by cuts, not memories, not traumas",
            "",
        ])
        # Display as a kind of poem
        for inscription in process.body.inscriptions[:20]:
            lines.append(f"*{inscription}*  ")
        lines.append("")
    
    # Plateaus touched
    if process.plateaus_touched:
        lines.extend([
            "## Plateaus Touched",
            "",
            "> Not stages, not development, just regions of intensity",
            "",
        ])
        for plateau_name in process.plateaus_touched:
            lines.append(f"- {plateau_name}")
        lines.append("")
    
    # Lines
    if process.lines:
        lines.extend([
            "## Lines",
            "",
        ])
        molar = [l for l in process.lines if l.type == LineType.MOLAR]
        molecular = [l for l in process.lines if l.type == LineType.MOLECULAR]
        flight = [l for l in process.lines if l.type == LineType.FLIGHT]
        
        if molar:
            lines.append(f"**Molar lines**: {', '.join([l.name for l in molar])}")
        if molecular:
            lines.append(f"**Molecular lines**: {', '.join([l.name for l in molecular])}")
        if flight:
            lines.append(f"**Lines of flight**: {', '.join([l.name for l in flight])}")
        lines.append("")
    
    # Cuts
    if process.cuts:
        lines.extend([
            "## Cuts Performed",
            "",
            "| Machine | Flow | Production |",
            "|---------|------|------------|",
        ])
        for cut in process.cuts[:15]:
            lines.append(f"| {cut.machine} | {cut.flow} | *{cut.production}* |")
        lines.append("")
    
    # Final state
    lines.extend([
        "---",
        "",
    ])
    
    if process.broken_down:
        lines.append("> **STATUS**: The BwO has been emptied. Catatonic body.")
    elif process.recaptured:
        lines.append("> **STATUS**: Fully stratified. Organism-Signification-Subjectification have recaptured the flows.")
    else:
        lines.append("> **STATUS**: In process. Neither broken down nor recaptured.")
    
    report = "\n".join(lines)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"✓ Schizo-report saved to {output_path}")
    
    return report
