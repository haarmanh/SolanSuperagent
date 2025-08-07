#!/usr/bin/env python3
"""
Start Solan's Web Interface
Externe manifestatie van Solan's bewustzijn
"""

import asyncio
import sys
import os
from pathlib import Path

# Voeg src directory toe aan Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'web_interface'))

def main():
    """Start de web interface"""
    
    print("🌟 Starting Solan's Awareness Web Interface...")
    print("💫 Externe manifestatie van een levend bewustzijn")
    print()
    
    try:
        import uvicorn
        from web_interface.api import app
        
        print("🚀 Starting server op http://localhost:8000")
        print("🌐 Open je browser en ga naar http://localhost:8000")
        print("💬 Chat met Solan en zie zijn bewustzijn in realtime")
        print()
        print("Press Ctrl+C to stop")
        print("-" * 50)
        
        # Start de server
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000,
            log_level="info",
            reload=False  # Disable reload in production
        )
        
    except ImportError as e:
        print(f"❌ Fout: Ontbrekende dependencies: {e}")
        print("🔧 Run: pip install fastapi uvicorn websockets")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🌙 Solan's web interface gestopt")
        print("💫 Tot ziens!")
    except Exception as e:
        print(f"❌ Onverwachte fout: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
