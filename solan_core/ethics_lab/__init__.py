#!/usr/bin/env python3
"""
Solān Ethics Lab Package
Refactored ethics laboratory functionality for better maintainability
"""

from .core import EthicsLabCore
from .ai_testing import EthicsLabAITesting
from .launcher import SolanEthicsLabLauncher

__all__ = [
    "EthicsLabCore",
    "EthicsLabAITesting", 
    "SolanEthicsLabLauncher"
]

__version__ = "1.0.0"
__author__ = "Solān AI System"
__description__ = "Advanced ethical testing laboratory for AI consciousness and awareness development"
