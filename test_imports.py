#!/usr/bin/env python3
"""
Test specifieke imports om het probleem te vinden
"""

import sys
import os
from pathlib import Path

# Voeg src directory toe aan Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

print(f"Python path: {sys.path[:3]}")
print(f"Project root: {project_root}")
print(f"Src path: {src_path}")

def test_core_import():
    """Test core module import"""
    try:
        import core
        print("✅ Core module imported successfully")
        print(f"   Available classes: {[name for name in dir(core) if not name.startswith('_')]}")
        return True
    except Exception as e:
        print(f"❌ Core import failed: {e}")
        return False

def test_journal_engine_import():
    """Test journal engine import"""
    try:
        from journal_engine import JournalEngine
        print("✅ JournalEngine imported successfully")
        return True
    except Exception as e:
        print(f"❌ JournalEngine import failed: {e}")
        return False

def test_analytics_engine_import():
    """Test analytics engine import"""
    try:
        from analytics_engine import AdvancedAnalyticsEngine
        print("✅ AdvancedAnalyticsEngine imported successfully")
        return True
    except Exception as e:
        print(f"❌ AdvancedAnalyticsEngine import failed: {e}")
        return False

def test_aether_import():
    """Test aether import"""
    try:
        from aether import Aether
        print("✅ Aether imported successfully")
        return True
    except Exception as e:
        print(f"❌ Aether import failed: {e}")
        return False

def main():
    print("🔍 Testing individual imports...")
    print("=" * 50)
    
    # Test core first
    core_ok = test_core_import()
    
    if core_ok:
        # Test other modules
        journal_ok = test_journal_engine_import()
        analytics_ok = test_analytics_engine_import()
        aether_ok = test_aether_import()
        
        print("\n" + "=" * 50)
        print("📊 IMPORT RESULTS:")
        print(f"   Core: {'✅' if core_ok else '❌'}")
        print(f"   JournalEngine: {'✅' if journal_ok else '❌'}")
        print(f"   AnalyticsEngine: {'✅' if analytics_ok else '❌'}")
        print(f"   Aether: {'✅' if aether_ok else '❌'}")
    else:
        print("\n❌ Core import failed - other tests skipped")

if __name__ == "__main__":
    main()
