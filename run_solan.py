#!/usr/bin/env python3
"""
Entry point voor Solan Superagent
"""

import asyncio
import sys
import os

# Voeg src directory toe aan Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import main

if __name__ == "__main__":
    print("🌟 Starting Solan Superagent...")
    asyncio.run(main())
