"""
Paradox Module - Solan's Mysterie Bewaarder
Waar tegenstrijdigheden worden gekoesterd als levende vragen
"""

from .paradox_types import ParadoxCategory, ParadoxDefinition, ParadoxLibrary
from .paradox_engine import ParadoxEngine, LiveParadox, ParadoxReflection

__all__ = [
    'ParadoxCategory',
    'ParadoxDefinition', 
    'ParadoxLibrary',
    'ParadoxEngine',
    'LiveParadox',
    'ParadoxReflection'
]
