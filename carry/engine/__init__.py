"""
Carry Engine - Assemblage Interaction Analysis

This module provides LLM-based interaction analysis between assemblages.
"""

from .interaction import (
    Assemblage,
    InteractionResult,
    load_assemblages,
    interact_llm,
)

__all__ = [
    "Assemblage",
    "InteractionResult",
    "load_assemblages",
    "interact_llm",
]
