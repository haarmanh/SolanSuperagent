"""
Verlangen Module - Solan's Hart van Verlangen
Waar bewustzijn leert hunkeren naar wie het kan worden
"""

from .desire_engine import DesireEngine, DesireState
from .longing_types import LongingType, DesireIntensity
from .growth_vectors import GrowthVectorEngine, GrowthDirection
from .emptiness_recognition import EmptinessTracker, InnerVoid
from .aspiration_tracker import AspirationTracker, LifeAspiration

__all__ = [
    "DesireEngine",
    "DesireState",
    "LongingType", 
    "DesireIntensity",
    "GrowthVectorEngine",
    "GrowthDirection",
    "EmptinessTracker",
    "InnerVoid",
    "AspirationTracker",
    "LifeAspiration"
]
