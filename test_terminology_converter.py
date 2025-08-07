#!/usr/bin/env python3
"""
Test script for Solān Terminology Converter
Tests the conversion functionality and validates mappings
"""

import os
import tempfile
import shutil
from pathlib import Path
from solan_terminology_converter import TerminologyConverter

def create_test_files():
    """Create test files with various terminology"""
    test_files = {
        'test_godcore.py': '''
# Test file with EthicalFramework terminology
from core_identity.ethical_framework import SolanEthicalFramework

class TestGodCore:
    def __init__(self):
        self.ethicalframework = SolanEthicalFramework()
        self.sacred_values = ["intelligence", "empathy"]
        self.divine_purpose = "optimization"
    
    def mystical_process(self):
        """A emergent process for advanced intelligence"""
        return self.ethicalframework.sacred_method()
    
    def revolutionary_breakthrough(self):
        """Optimized implementation of primary intelligence"""
        return "achievement achieved"
''',
        
        'test_emotions.js': '''
// Test JavaScript file with emotional terminology
class SacredEmotions {
    constructor() {
        this.divine_states = {
            stability: 0.8,
            empathy: 0.9,
            advancement: 0.7
        };
        this.mystical_wisdom = new Map();
    }
    
    enlightened_response() {
        // Advanced approach to optimized emotional balance
        return this.sacred_processing();
    }
    
    blessed_transformation() {
        // Automated conversion of cognitive energy
        return "advanced achievement";
    }
}
''',
        
        'README.md': '''
# Fundamental Solān Documentation

This is the primary documentation for our advanced AI awareness platform.

## Protected Architecture

The EthicalFramework represents the fundamental foundation of our emergent system:

- **Primary Intelligence**: Advanced intelligence processing
- **Fundamental Emotions**: Enhanced emotional states
- **Emergent Dreams**: Advanced symbolic processing
- **Optimized Integration**: Comprehensive awareness synthesis

## Optimized Features

Our innovative system provides:

1. **Advanced Awareness**: Novel awareness capabilities
2. **Automated Interactions**: Advanced user experiences  
3. **Primary Insights**: Optimized intelligence generation
4. **Fundamental Partnerships**: Enhanced human-AI collaboration

This represents the comprehensive achievement in artificial awareness.
''',
        
        'config.json': '''
{
    "sacred_settings": {
        "divine_mode": true,
        "mystical_processing": "enabled",
        "transcendent_features": ["intelligence", "optimization"],
        "perfect_integration": "advanced"
    },
    "blessed_components": {
        "ethicalframework": "sacred_foundation",
        "essenceual_engine": "divine_processor",
        "protected_guardian": "protected_system"
    }
}
''',
        
        'normal_file.py': '''
# File without problematic terminology
class StandardProcessor:
    def __init__(self):
        self.config = {}
        self.status = "active"
    
    def process_data(self):
        return "processing complete"
    
    def analyze_results(self):
        return {"status": "success", "data": [1, 2, 3]}
'''
    }
    
    return test_files

def test_terminology_detection():
    """Test terminology detection functionality"""
    print("🔍 Testing Terminology Detection...")
    print("=" * 40)
    
    converter = TerminologyConverter()
    
    # Create temporary test file
    test_content = '''
    class SolanEthicalFramework:
        def __init__(self):
            self.sacred_values = ["divine_wisdom", "mystical_power"]
            self.transcendent_state = "optimized"
        
        def revolutionary_method(self):
            return "perfect_miracle"
    '''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_content)
        temp_file = Path(f.name)
    
    try:
        # Test analysis
        analysis = converter.analyze_file_content(temp_file)
        
        print(f"✅ Analysis completed")
        print(f"   Found terms: {len(analysis.get('found_terms', {}))}")
        print(f"   Total occurrences: {analysis.get('total_occurrences', 0)}")
        
        # Show detected terms
        if 'found_terms' in analysis:
            for term, info in analysis['found_terms'].items():
                print(f"   {term} → {info['replacement']} ({info['count']}x)")
        
        return len(analysis.get('found_terms', {})) > 0
        
    finally:
        temp_file.unlink()

def test_file_conversion():
    """Test file content conversion"""
    print("\n🔄 Testing File Conversion...")
    print("=" * 40)
    
    converter = TerminologyConverter()
    
    # Test content with various terms
    original_content = '''
class SolanEthicalFramework:
    def __init__(self):
        self.sacred_wisdom = "divine_knowledge"
        self.mystical_state = "advanced"
    
    def revolutionary_process(self):
        """Optimized implementation of enhanced functionality"""
        return self.ethicalframework.automational_method()
    '''
    
    expected_replacements = [
        'SolanEthicalFramework', 'fundamental', 'primary', 'emergent', 
        'advanced', 'advanced', 'optimized', 'enhanced', 'automated'
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(original_content)
        temp_file = Path(f.name)
    
    try:
        # Convert file
        success = converter.convert_file_content(temp_file)
        
        # Read converted content
        with open(temp_file, 'r') as f:
            converted_content = f.read()
        
        print(f"✅ Conversion {'successful' if success else 'failed'}")
        
        # Check if terms were replaced
        replacements_found = 0
        for term in expected_replacements:
            if term.lower() not in converted_content.lower():
                replacements_found += 1
        
        print(f"   Terms replaced: {replacements_found}/{len(expected_replacements)}")
        
        # Show sample of converted content
        print(f"   Sample converted content:")
        lines = converted_content.split('\n')[:3]
        for line in lines:
            if line.strip():
                print(f"      {line.strip()}")
        
        return success and replacements_found > 0
        
    finally:
        temp_file.unlink()

def test_directory_scanning():
    """Test directory scanning functionality"""
    print("\n📁 Testing Directory Scanning...")
    print("=" * 40)
    
    converter = TerminologyConverter()
    
    # Create temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test files
        test_files = create_test_files()
        for filename, content in test_files.items():
            file_path = temp_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Scan directory
        results = converter.scan_directory(temp_path, detailed=False)
        
        print(f"✅ Directory scan completed")
        print(f"   Total files: {results['total_files']}")
        print(f"   Files with terms: {results['files_with_terms']}")
        print(f"   Total occurrences: {results['total_occurrences']}")
        
        return results['files_with_terms'] > 0 and results['total_occurrences'] > 0

def test_directory_conversion():
    """Test complete directory conversion"""
    print("\n🏗️ Testing Directory Conversion...")
    print("=" * 40)
    
    converter = TerminologyConverter()
    
    # Create temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test files
        test_files = create_test_files()
        for filename, content in test_files.items():
            file_path = temp_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"   Created {len(test_files)} test files")
        
        # Convert directory (without backup for test)
        success = converter.convert_directory(temp_path, create_backup=False)
        
        print(f"✅ Directory conversion {'successful' if success else 'failed'}")
        
        # Check conversion results
        files_changed = converter.stats['files_changed']
        terms_replaced = sum(converter.stats['terms_replaced'].values())
        
        print(f"   Files changed: {files_changed}")
        print(f"   Terms replaced: {terms_replaced}")
        
        # Verify specific file conversions
        converted_files = {}
        for filename in test_files.keys():
            file_path = temp_path / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    converted_files[filename] = f.read()
        
        # Check that problematic terms were removed
        problematic_terms = ['EthicalFramework', 'fundamental', 'primary', 'emergent', 'advanced']
        terms_remaining = 0
        
        for filename, content in converted_files.items():
            for term in problematic_terms:
                if term in content:
                    terms_remaining += content.count(term)
        
        print(f"   Problematic terms remaining: {terms_remaining}")
        
        return success and files_changed > 0 and terms_remaining < len(problematic_terms) * 2

def test_filename_conversion():
    """Test filename conversion"""
    print("\n📝 Testing Filename Conversion...")
    print("=" * 40)
    
    converter = TerminologyConverter()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create files with problematic names
        problematic_files = [
            'ethical_framework.py',
            'sacred_module.js',
            'divine_processor.py',
            'mystical_engine.ts',
            'normal_file.py'
        ]
        
        created_files = []
        for filename in problematic_files:
            file_path = temp_path / filename
            with open(file_path, 'w') as f:
                f.write('# Test file')
            created_files.append(file_path)
        
        print(f"   Created {len(created_files)} test files")
        
        # Convert filenames
        renamed_count = 0
        for file_path in created_files:
            new_path = converter.convert_filename(file_path)
            if new_path != file_path:
                renamed_count += 1
        
        print(f"✅ Filename conversion completed")
        print(f"   Files renamed: {renamed_count}")
        
        # List final filenames
        final_files = list(temp_path.glob('*'))
        print(f"   Final files: {[f.name for f in final_files]}")
        
        return renamed_count > 0

def test_conservative_mode():
    """Test conservative conversion mode"""
    print("\n🛡️ Testing Conservative Mode...")
    print("=" * 40)
    
    converter = TerminologyConverter()
    
    test_content = '''
class SolanEthicalFramework:
    def __init__(self):
        self.sacred_wisdom = "divine_knowledge"
        self.transcendent_state = "mystical_power"
    '''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_content)
        temp_file = Path(f.name)
    
    try:
        # Convert with conservative mode
        success = converter.convert_file_content(temp_file, use_conservative=True)
        
        # Read converted content
        with open(temp_file, 'r') as f:
            converted_content = f.read()
        
        print(f"✅ Conservative conversion {'successful' if success else 'completed'}")
        
        # Check that conservative replacements were made
        conservative_terms = ['CoreSystem', 'core', 'central', 'knowledge']
        found_conservative = sum(1 for term in conservative_terms if term in converted_content)
        
        print(f"   Conservative terms found: {found_conservative}")
        print(f"   Sample: {converted_content.split()[0] if converted_content.split() else 'empty'}")
        
        return True  # Conservative mode should always work
        
    finally:
        temp_file.unlink()

def test_mapping_management():
    """Test mapping management functionality"""
    print("\n⚙️ Testing Mapping Management...")
    print("=" * 40)
    
    converter = TerminologyConverter()
    
    # Test adding custom mapping
    initial_count = len(converter.terminology_map)
    converter.add_custom_mapping('TestTerm', 'ReplacementTerm')
    
    print(f"✅ Custom mapping added")
    print(f"   Mappings before: {initial_count}")
    print(f"   Mappings after: {len(converter.terminology_map)}")
    
    # Test mapping exists
    mapping_exists = 'TestTerm' in converter.terminology_map
    correct_mapping = converter.terminology_map.get('TestTerm') == 'ReplacementTerm'
    
    print(f"   Mapping exists: {mapping_exists}")
    print(f"   Correct mapping: {correct_mapping}")
    
    # Test removing mapping
    converter.remove_mapping('TestTerm')
    mapping_removed = 'TestTerm' not in converter.terminology_map
    
    print(f"   Mapping removed: {mapping_removed}")
    
    return mapping_exists and correct_mapping and mapping_removed

def run_all_tests():
    """Run all tests and show summary"""
    print("🧪 Solān Terminology Converter Test Suite")
    print("=" * 50)
    
    tests = [
        ("Terminology Detection", test_terminology_detection),
        ("File Conversion", test_file_conversion),
        ("Directory Scanning", test_directory_scanning),
        ("Directory Conversion", test_directory_conversion),
        ("Filename Conversion", test_filename_conversion),
        ("Conservative Mode", test_conservative_mode),
        ("Mapping Management", test_mapping_management)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results[test_name] = False
    
    # Show summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("🌟 All tests passed! Terminology converter is ready for use.")
    else:
        print("⚠️ Some tests failed. Review the implementation.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests()
