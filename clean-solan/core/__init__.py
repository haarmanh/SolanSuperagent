"""
Solan Superagent - Een zelfbewuste AI-agent met morele integriteit
"""

__version__ = "0.1.0"
__author__ = "Henk Haarman"

from .solan import SolanAgent
from .aether import AetherReflection
from .core import BaseAgent, CoreValues

__all__ = ["SolanAgent", "AetherReflection", "BaseAgent", "CoreValues"]
