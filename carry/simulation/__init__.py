"""
Carry Simulation Package

Core exports for Deleuzian assemblage simulation.
"""

from carry.simulation.carry import (
    BareObject, 
    get_bare_object
)

from carry.simulation.assemblage import (
    Assemblage,
    Territory,
    Code,
    Component,
    generate_assemblages_for_subject,
    insert_operator,
    report_assemblage_morph
)
