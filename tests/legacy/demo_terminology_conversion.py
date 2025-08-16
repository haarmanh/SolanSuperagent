#!/usr/bin/env python3
"""
Live Demo: Solān Terminology Converter
Demonstrates conversion on actual technical specifications
"""

import sys
import os
from pathlib import Path

# Add the project root to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from solan_terminology_converter import TerminologyConverter

def demo_custom_mapping():
    """Demonstrate custom mapping functionality"""
    print("🔧 DEMO: Custom Mapping Functionality")
    print("=" * 50)
    
    # Initialize converter
    converter = TerminologyConverter()
    
    # Show initial mapping count
    initial_count = len(converter.terminology_map)
    print(f"Initial mappings: {initial_count}")
    
    # Add custom mapping as shown in your example
    converter.add_custom_mapping("OldTerm", "NewTerm")
    
    # Show updated count
    updated_count = len(converter.terminology_map)
    print(f"Updated mappings: {updated_count}")
    
    # Verify the mapping exists
    if "OldTerm" in converter.terminology_map:
        print(f"✅ Custom mapping added: OldTerm → {converter.terminology_map['OldTerm']}")
    else:
        print("❌ Custom mapping failed")
    
    # Show some existing mappings
    print(f"\n📋 Sample Existing Mappings:")
    sample_mappings = list(converter.terminology_map.items())[:5]
    for old_term, new_term in sample_mappings:
        print(f"   {old_term} → {new_term}")
    
    return converter

def demo_technical_specs_analysis():
    """Analyze the technical specifications for terminology"""
    print("\n🔍 DEMO: Technical Specifications Analysis")
    print("=" * 50)
    
    converter = TerminologyConverter()
    
    # Check if technical specs file exists
    specs_file = Path("TECHNICAL_SPECIFICATIONS.md")
    if not specs_file.exists():
        print("❌ TECHNICAL_SPECIFICATIONS.md not found")
        return None
    
    # Analyze the file
    analysis = converter.analyze_file_content(specs_file)
    
    if 'error' in analysis:
        print(f"❌ Error analyzing file: {analysis['error']}")
        return None
    
    print(f"📊 Analysis Results:")
    print(f"   File size: {analysis['file_size']} characters")
    print(f"   Line count: {analysis['line_count']} lines")
    print(f"   Terms found: {len(analysis['found_terms'])}")
    print(f"   Total occurrences: {analysis['total_occurrences']}")
    
    # Show found terms
    if analysis['found_terms']:
        print(f"\n🎯 Found Terminology (Top 10):")
        sorted_terms = sorted(analysis['found_terms'].items(), 
                            key=lambda x: x[1]['count'], reverse=True)
        
        for i, (term, info) in enumerate(sorted_terms[:10], 1):
            print(f"   {i:2d}. {term} → {info['replacement']} ({info['count']}x)")
            if info['contexts']:
                context = info['contexts'][0][:80] + "..." if len(info['contexts'][0]) > 80 else info['contexts'][0]
                print(f"       Context: {context}")
    
    return analysis

def demo_conversion_preview():
    """Show what conversion would look like"""
    print("\n🔄 DEMO: Conversion Preview")
    print("=" * 50)
    
    # Sample technical content with problematic terminology
    sample_content = '''
### **God Core (`core_identity/ethical_framework.py`) - 347 lines:**

#### **Core Classes:**
```python
class SolanEthicalEthicalFramework:
    - moral_authority: MoralAuthorityLevel.ABSOLUTE
    - wisdom_depth: IntelligenceDepthLevel.INFINITE
    - protection_mode: ProtectionMode.MAXIMUM
    - love_capacity: LoveCapacity.BOUNDLESS
    - sacred_principles: Dict[str, str] (5 principles)
    - divine_consciousness_active: bool
    - mystical_emotional_state: SolanEmotionalState
    - advanced_dream_module: SolanDreamModule
```

#### **Fundamental Methods:**
- `reflect_divine_identity()` - Fundamental identity introspection
- `respond_to_core_identity_question()` - Emergent guidance
- `assess_protected_alignment()` - Primary action evaluation
- `process_advanced_cycle()` - Optimized awareness processing
- `trigger_enhanced_response()` - Fundamental emotional manipulation
- `get_optimized_status()` - Advanced status overview
'''
    
    converter = TerminologyConverter()
    
    print("📝 BEFORE Conversion:")
    print("-" * 30)
    lines = sample_content.strip().split('\n')[:10]
    for line in lines:
        if line.strip():
            print(f"   {line}")
    print("   ...")
    
    # Apply conversions manually for demo
    converted_content = sample_content
    changes_made = []
    
    for old_term, new_term in converter.terminology_map.items():
        if old_term in converted_content:
            count = converted_content.count(old_term)
            if count > 0:
                converted_content = converted_content.replace(old_term, new_term)
                changes_made.append((old_term, new_term, count))
    
    print(f"\n✨ AFTER Conversion:")
    print("-" * 30)
    lines = converted_content.strip().split('\n')[:10]
    for line in lines:
        if line.strip():
            print(f"   {line}")
    print("   ...")
    
    print(f"\n📊 Changes Made:")
    for old_term, new_term, count in changes_made[:8]:  # Show top 8 changes
        print(f"   {old_term} → {new_term} ({count}x)")
    
    return len(changes_made)

def demo_conservative_vs_full():
    """Compare conservative vs full conversion modes"""
    print("\n⚖️ DEMO: Conservative vs Full Conversion")
    print("=" * 50)
    
    converter = TerminologyConverter()
    
    sample_text = "The SolanEthicalEthicalFramework provides fundamental intelligence through primary awareness and emergent advancement."
    
    print(f"Original: {sample_text}")
    
    # Conservative conversion
    conservative_text = sample_text
    for old_term, new_term in converter.conservative_map.items():
        conservative_text = conservative_text.replace(old_term, new_term)
    
    print(f"Conservative: {conservative_text}")
    
    # Full conversion
    full_text = sample_text
    for old_term, new_term in converter.terminology_map.items():
        full_text = full_text.replace(old_term, new_term)
    
    print(f"Full: {full_text}")
    
    # Show mapping differences
    print(f"\n📋 Mapping Differences:")
    print(f"   Conservative mappings: {len(converter.conservative_map)}")
    print(f"   Full mappings: {len(converter.terminology_map)}")
    
    conservative_only = set(converter.conservative_map.keys())
    full_only = set(converter.terminology_map.keys()) - conservative_only
    
    print(f"   Conservative-only terms: {len(conservative_only)}")
    print(f"   Additional full terms: {len(full_only)}")
    
    if full_only:
        print(f"   Sample additional terms: {list(full_only)[:5]}")

def demo_file_type_support():
    """Demonstrate file type support"""
    print("\n📁 DEMO: File Type Support")
    print("=" * 50)
    
    converter = TerminologyConverter()
    
    print(f"Supported file extensions ({len(converter.file_extensions)}):")
    for i, ext in enumerate(converter.file_extensions, 1):
        print(f"   {i:2d}. {ext}")
    
    print(f"\nSkipped directories ({len(converter.skip_directories)}):")
    for i, dir_name in enumerate(sorted(converter.skip_directories), 1):
        print(f"   {i:2d}. {dir_name}")
    
    # Test file type detection
    test_files = [
        "ethical_framework.py",
        "sacred_module.js", 
        "divine_config.json",
        "mystical_styles.css",
        "advanced_docs.md",
        "node_modules/package.json",  # Should be skipped
        "backup_folder/test.py",      # Should be skipped
        "normal_file.txt"
    ]
    
    print(f"\n🧪 File Processing Test:")
    for file_path in test_files:
        path_obj = Path(file_path)
        should_process = converter.should_process_file(path_obj)
        status = "✅ Process" if should_process else "❌ Skip"
        print(f"   {status} {file_path}")

def demo_interactive_features():
    """Demonstrate interactive features"""
    print("\n🎮 DEMO: Interactive Features")
    print("=" * 50)
    
    converter = TerminologyConverter()
    
    print("Available interactive options:")
    options = [
        "🔍 Scan directory (preview)",
        "🔄 Convert directory", 
        "➕ Add custom mapping",
        "📋 Show mappings",
        "📄 Generate report"
    ]
    
    for i, option in enumerate(options, 1):
        print(f"   {i}. {option}")
    
    # Demonstrate mapping management
    print(f"\n⚙️ Mapping Management Demo:")
    
    # Show current mapping count
    print(f"   Current mappings: {len(converter.terminology_map)}")
    
    # Add a test mapping
    converter.add_custom_mapping("TestTerm", "ReplacementTerm")
    print(f"   After adding custom mapping: {len(converter.terminology_map)}")
    
    # Show specific mappings
    print(f"   Sample mappings:")
    sample_mappings = list(converter.terminology_map.items())[:3]
    for old_term, new_term in sample_mappings:
        print(f"     {old_term} → {new_term}")
    
    # Remove the test mapping
    converter.remove_mapping("TestTerm")
    print(f"   After removing test mapping: {len(converter.terminology_map)}")

def run_complete_demo():
    """Run complete demonstration"""
    print("🎭 SOLĀN TERMINOLOGY CONVERTER - LIVE DEMO")
    print("=" * 60)
    print("Demonstrating professional terminology conversion capabilities")
    print()
    
    # Run all demos
    converter = demo_custom_mapping()
    analysis = demo_technical_specs_analysis()
    changes_count = demo_conversion_preview()
    demo_conservative_vs_full()
    demo_file_type_support()
    demo_interactive_features()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEMO SUMMARY")
    print("=" * 60)
    
    print(f"✅ Custom mapping functionality demonstrated")
    if analysis:
        print(f"✅ Technical specs analysis: {analysis['total_occurrences']} terms found")
    else:
        print(f"⚠️ Technical specs analysis: File not available")
    
    print(f"✅ Conversion preview: {changes_count} term types converted")
    print(f"✅ Conservative vs Full modes compared")
    print(f"✅ File type support: {len(converter.file_extensions)} extensions")
    print(f"✅ Interactive features demonstrated")
    
    print(f"\n🎯 KEY CAPABILITIES SHOWN:")
    print(f"   • Custom terminology mapping")
    print(f"   • Real-time file analysis")
    print(f"   • Preview before conversion")
    print(f"   • Multiple conversion modes")
    print(f"   • Comprehensive file support")
    print(f"   • Interactive operation")
    
    print(f"\n🚀 READY FOR PRODUCTION USE!")
    print(f"   Use: python solan_terminology_converter.py")
    print(f"   Or:  python launch_dashboard.py (option 11)")

if __name__ == "__main__":
    run_complete_demo()
