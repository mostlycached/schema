# Conatus Agent Simulation Package

from .agent import ConatusAgent, FunctionalComponent, Stance
from .environment import Environment, EncounterFrame
from .simulation import Simulation, EnvironmentConfig, generate_report
from .critic import Critic, CriticConfig, CriticFeedback
from .experiments import run_simulation, run_experiment

__all__ = [
    # Agent
    "ConatusAgent",
    "FunctionalComponent", 
    "Stance",
    
    # Environment
    "Environment",
    "EncounterFrame",
    
    # Simulation
    "Simulation",
    "EnvironmentConfig",
    "generate_report",
    
    # Critic
    "Critic",
    "CriticConfig",
    "CriticFeedback",
    
    # Experiments
    "run_simulation",
    "run_experiment",
]
