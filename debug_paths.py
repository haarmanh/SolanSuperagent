#!/usr/bin/env python3
"""
Debug pad problemen
"""

import os
import sys
from pathlib import Path

# Voeg src directory toe aan Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def debug_paths():
    """Debug alle relevante paden"""
    print("🔍 PATH DEBUGGING")
    print("=" * 50)
    
    # Current working directory
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    
    # Project paths
    print(f"Project root: {project_root}")
    print(f"Src path: {src_path}")
    
    # Memory paths
    memory_path = project_root / "memory"
    journal_path = memory_path / "journal"
    entries_path = journal_path / "entries"
    
    print(f"Memory path: {memory_path}")
    print(f"Journal path: {journal_path}")
    print(f"Entries path: {entries_path}")
    
    # Check existence
    print(f"Memory exists: {memory_path.exists()}")
    print(f"Journal exists: {journal_path.exists()}")
    print(f"Entries exists: {entries_path.exists()}")
    
    if entries_path.exists():
        json_files = list(entries_path.glob("*.json"))
        print(f"JSON files found: {len(json_files)}")
        if json_files:
            print(f"First file: {json_files[0]}")
    
    # Test web_interface perspective
    print("\n🌐 WEB_INTERFACE PERSPECTIVE")
    print("=" * 50)
    
    web_interface_dir = project_root / "web_interface"
    print(f"Web interface dir: {web_interface_dir}")
    
    # Simulate web_interface working directory
    os.chdir(web_interface_dir)
    print(f"Changed to: {os.getcwd()}")
    
    # Test relative paths from web_interface
    relative_memory = Path("../memory/journal/entries")
    print(f"Relative path: {relative_memory}")
    print(f"Relative exists: {relative_memory.exists()}")
    print(f"Absolute from relative: {relative_memory.resolve()}")
    
    if relative_memory.exists():
        json_files = list(relative_memory.glob("*.json"))
        print(f"JSON files via relative: {len(json_files)}")

def test_journal_engine_paths():
    """Test journal engine pad logica"""
    print("\n📚 JOURNAL ENGINE PATH TEST")
    print("=" * 50)
    
    # Simuleer unified_api.py logica
    current_dir = os.path.dirname(os.path.abspath(__file__))
    web_interface_dir = project_root / "web_interface"
    
    # Simuleer web_interface working directory
    os.chdir(web_interface_dir)
    
    # Unified API logica
    current_file = web_interface_dir / "unified_api.py"
    current_dir = current_file.parent
    project_root_from_web = current_dir.parent
    
    journal_dir = project_root_from_web / "memory" / "journal"
    entries_dir = journal_dir / "entries"
    
    print(f"Current file (simulated): {current_file}")
    print(f"Current dir: {current_dir}")
    print(f"Project root from web: {project_root_from_web}")
    print(f"Journal dir: {journal_dir}")
    print(f"Entries dir: {entries_dir}")
    print(f"Entries exists: {entries_dir.exists()}")
    
    if entries_dir.exists():
        json_files = list(entries_dir.glob("*.json"))
        print(f"JSON files found: {len(json_files)}")

def main():
    debug_paths()
    test_journal_engine_paths()

if __name__ == "__main__":
    main()
