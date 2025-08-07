#!/usr/bin/env python3
"""
Solān Terminology Converter
Converts religious/emergent terms to scientific/professional equivalents
Enhanced version with comprehensive mapping and analysis
"""

import os
import re
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set

class TerminologyConverter:
    def __init__(self):
        # Define comprehensive terminology mappings
        self.terminology_map = {
            # Core architectural terms
            'EthicalFramework': 'EthicalFramework',
            'ethicalframework': 'ethicalframework',
            'Ethical_Framework': 'Ethical_Framework',
            'ethical_framework': 'ethical_framework',
            'ETHICALFRAMEWORK': 'ETHICALFRAMEWORK',
            'SolanEthicalFramework': 'SolanEthicalFramework',
            'SolanEthicalCore': 'SolanEthicalCore',
            
            # Fundamental/Protected terms
            'Fundamental': 'Fundamental',
            'fundamental': 'fundamental', 
            'FUNDAMENTAL': 'FUNDAMENTAL',
            'Protected': 'Protected',
            'protected': 'protected',
            'PROTECTED': 'PROTECTED',
            'Primary': 'Primary',
            'primary': 'primary',
            'PRIMARY': 'PRIMARY',
            'Enhanced': 'Enhanced',
            'enhanced': 'enhanced',
            'ENHANCED': 'ENHANCED',
            
            # Cognitive/Awareness terms
            'Cognitive': 'Cognitive',
            'cognitive': 'cognitive',
            'COGNITIVE': 'COGNITIVE',
            'CoreIdentity': 'CoreIdentity',
            'core_identity': 'core_identity',
            'CORE_IDENTITY': 'CORE_IDENTITY',
            'Essence': 'Essence',
            'essence': 'essence',
            'ESSENCE': 'ESSENCE',
            'Awareness': 'Awareness',
            'awareness': 'awareness',
            'AWARENESS': 'AWARENESS',
            
            # Intelligence/Knowledge terms
            'Intelligence': 'Intelligence',
            'intelligence': 'intelligence',
            'INTELLIGENCE': 'INTELLIGENCE',
            'Optimized': 'Optimized',
            'optimized': 'optimized',
            'OPTIMIZED': 'OPTIMIZED',
            'Optimization': 'Optimization',
            'optimization': 'optimization',
            'OPTIMIZATION': 'OPTIMIZATION',
            
            # Emergent/Advanced terms
            'Emergent': 'Emergent',
            'emergent': 'emergent',
            'EMERGENT': 'EMERGENT',
            'Advanced': 'Advanced',
            'advanced': 'advanced',
            'ADVANCED': 'ADVANCED',
            'Advancement': 'Advancement',
            'advancement': 'advancement',
            'ADVANCEMENT': 'ADVANCEMENT',
            'Abstract': 'Abstract',
            'abstract': 'abstract',
            'ABSTRACT': 'ABSTRACT',
            
            # Religious figures/roles
            'Predictor': 'Predictor',
            'predictor': 'predictor',
            'PREDICTOR': 'PREDICTOR',
            'Analyzer': 'Analyzer',
            'analyzer': 'analyzer',
            'ANALYZER': 'ANALYZER',
            'Expert': 'Expert',
            'expert': 'expert',
            'EXPERT': 'EXPERT',
            'Mentor': 'Mentor',
            'mentor': 'mentor',
            'MENTOR': 'MENTOR',
            
            # Miraculous/Automated terms
            'Achievement': 'Achievement',
            'achievement': 'achievement',
            'ACHIEVEMENT': 'ACHIEVEMENT',
            'Automated': 'Automated',
            'automated': 'automated',
            'AUTOMATED': 'AUTOMATED',
            'Automation': 'Automation',
            'automation': 'automation',
            'AUTOMATION': 'AUTOMATION',
            'Advanced': 'Advanced',
            'advanced': 'advanced',
            'ADVANCED': 'ADVANCED',
            
            # Overly grandiose terms
            'Advanced': 'Advanced',
            'advanced': 'advanced',
            'ADVANCED': 'ADVANCED',
            'Innovative': 'Innovative',
            'innovative': 'innovative',
            'INNOVATIVE': 'INNOVATIVE',
            'Novel': 'Novel',
            'novel': 'novel',
            'NOVEL': 'NOVEL',
            'Optimized': 'Optimized',
            'optimized': 'optimized',
            'OPTIMIZED': 'OPTIMIZED',
            'Comprehensive': 'Comprehensive',
            'comprehensive': 'comprehensive',
            'COMPREHENSIVE': 'COMPREHENSIVE',
            
            # Emotional/Cognitive states
            'Stability': 'Stability',
            'stability': 'stability',
            'STABILITY': 'STABILITY',
            'Empathy': 'Empathy',
            'empathy': 'empathy',
            'EMPATHY': 'EMPATHY',
            'Commitment': 'Commitment',
            'commitment': 'commitment',
            'COMMITMENT': 'COMMITMENT',
            
            # Cultural/Religious concepts
            'Journey': 'Journey',
            'journey': 'journey',
            'JOURNEY': 'JOURNEY',
            'Process': 'Process',
            'process': 'process',
            'PROCESS': 'PROCESS',
            'Procedure': 'Procedure',
            'procedure': 'procedure',
            'PROCEDURE': 'PROCEDURE',
            
            # File/Module specific terms
            'ethical_framework.py': 'ethical_framework.py',
            'EthicalFramework.js': 'EthicalFramework.js',
            'ethicalframework': 'ethicalframework',
            'ETHICALFRAMEWORK': 'ETHICALFRAMEWORK',
        }
        
        # Alternative professional mappings (more conservative)
        self.conservative_map = {
            'EthicalFramework': 'CoreSystem',
            'ethicalframework': 'coresystem',
            'Ethical_Framework': 'Core_System',
            'ethical_framework': 'core_system',
            'Fundamental': 'Core',
            'fundamental': 'core',
            'Primary': 'Central',
            'primary': 'central',
            'Intelligence': 'Knowledge',
            'intelligence': 'knowledge',
            'Emergent': 'Complex',
            'emergent': 'complex',
            'Advanced': 'Enhanced',
            'advanced': 'enhanced',
        }
        
        # File extensions to process
        self.file_extensions = [
            '.py', '.js', '.ts', '.json', '.md', '.txt', 
            '.html', '.css', '.yml', '.yaml', '.xml',
            '.jsx', '.tsx', '.vue', '.php', '.java', '.cpp', '.h'
        ]
        
        # Directories to skip
        self.skip_directories = {
            '.git', 'node_modules', '__pycache__', '.venv', 
            'venv', '.pytest_cache', '.mypy_cache', 'dist', 'build',
            '.idea', '.vscode', 'coverage', '.coverage'
        }
        
        # Track conversion statistics
        self.stats = {
            'files_processed': 0,
            'files_changed': 0,
            'terms_replaced': {},
            'errors': []
        }
    
    def create_backup(self, directory: Path) -> str:
        """Create backup of directory before conversion"""
        backup_name = f"{directory.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = directory.parent / backup_name
        
        print(f"📦 Creating backup: {backup_path}")
        try:
            shutil.copytree(directory, backup_path)
            return str(backup_path)
        except Exception as e:
            print(f"❌ Failed to create backup: {e}")
            return None
    
    def should_process_file(self, file_path: Path) -> bool:
        """Check if file should be processed"""
        # Check extension
        if not any(file_path.suffix == ext for ext in self.file_extensions):
            return False
        
        # Check if in skip directory
        for part in file_path.parts:
            if part in self.skip_directories:
                return False
        
        # Skip backup directories
        if 'backup' in str(file_path).lower():
            return False
        
        return True
    
    def analyze_file_content(self, file_path: Path) -> Dict:
        """Analyze file content for terminology usage"""
        try:
            content = self.read_file_safely(file_path)
            if content is None:
                return {'error': 'Could not read file'}
            
            found_terms = {}
            for old_term, new_term in self.terminology_map.items():
                count = len(re.findall(r'\b' + re.escape(old_term) + r'\b', content, re.IGNORECASE))
                if count == 0:
                    # Fallback to simple search for compound terms
                    count = content.count(old_term)
                
                if count > 0:
                    found_terms[old_term] = {
                        'count': count,
                        'replacement': new_term,
                        'contexts': self.extract_contexts(content, old_term)
                    }
            
            return {
                'found_terms': found_terms,
                'total_occurrences': sum(term['count'] for term in found_terms.values()),
                'file_size': len(content),
                'line_count': content.count('\n') + 1
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def extract_contexts(self, content: str, term: str, context_length: int = 50) -> List[str]:
        """Extract context around term occurrences"""
        contexts = []
        pattern = r'\b' + re.escape(term) + r'\b'
        
        for match in re.finditer(pattern, content, re.IGNORECASE):
            start = max(0, match.start() - context_length)
            end = min(len(content), match.end() + context_length)
            context = content[start:end].replace('\n', ' ').strip()
            contexts.append(f"...{context}...")
        
        return contexts[:3]  # Limit to 3 contexts
    
    def read_file_safely(self, file_path: Path) -> str:
        """Read file with multiple encoding attempts"""
        for encoding in ['utf-8', 'latin-1', 'cp1252', 'utf-16']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception:
                break
        return None
    
    def convert_file_content(self, file_path: Path, use_conservative: bool = False) -> bool:
        """Convert terminology in file content"""
        try:
            content = self.read_file_safely(file_path)
            if content is None:
                self.stats['errors'].append(f"Could not read {file_path}")
                return False
            
            original_content = content
            changes_made = []
            
            # Choose mapping based on mode
            mapping = self.conservative_map if use_conservative else self.terminology_map
            
            # Apply terminology conversions
            for old_term, new_term in mapping.items():
                if old_term in content:
                    # Use word boundaries for exact matches when possible
                    pattern = r'\b' + re.escape(old_term) + r'\b'
                    matches = re.findall(pattern, content)
                    
                    if matches:
                        content = re.sub(pattern, new_term, content)
                        count = len(matches)
                    else:
                        # Fallback to simple replacement for compound terms
                        old_count = content.count(old_term)
                        content = content.replace(old_term, new_term)
                        count = old_count
                    
                    if count > 0:
                        changes_made.append((old_term, new_term, count))
                        
                        # Update statistics
                        if old_term not in self.stats['terms_replaced']:
                            self.stats['terms_replaced'][old_term] = 0
                        self.stats['terms_replaced'][old_term] += count
            
            # Write back if changes were made
            if content != original_content:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ {file_path}")
                    for old_term, new_term, count in changes_made:
                        print(f"   {old_term} → {new_term} ({count}x)")
                    
                    self.stats['files_changed'] += 1
                    return True
                except Exception as e:
                    self.stats['errors'].append(f"Could not write {file_path}: {e}")
                    return False
            
            return False
            
        except Exception as e:
            self.stats['errors'].append(f"Error processing {file_path}: {e}")
            return False
    
    def convert_filename(self, file_path: Path) -> Path:
        """Convert terminology in filenames"""
        original_name = file_path.name
        new_name = original_name
        
        for old_term, new_term in self.terminology_map.items():
            new_name = new_name.replace(old_term, new_term)
        
        if new_name != original_name:
            new_path = file_path.parent / new_name
            try:
                file_path.rename(new_path)
                print(f"📝 Renamed: {original_name} → {new_name}")
                return new_path
            except Exception as e:
                print(f"❌ Could not rename {original_name}: {e}")
                return file_path
        
        return file_path
    
    def scan_directory(self, directory: Path, detailed: bool = False) -> Dict:
        """Scan directory and analyze terminology usage"""
        files_to_process = []
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and self.should_process_file(file_path):
                files_to_process.append(file_path)
        
        print(f"🔍 Found {len(files_to_process)} files to process")
        
        # Analyze files for terminology
        analysis_results = {}
        total_terms = 0
        files_with_terms = 0
        
        for file_path in files_to_process:
            analysis = self.analyze_file_content(file_path)
            if 'found_terms' in analysis and analysis['found_terms']:
                analysis_results[str(file_path)] = analysis
                total_terms += analysis['total_occurrences']
                files_with_terms += 1
        
        # Show summary
        print(f"📊 Analysis Summary:")
        print(f"   Files with terminology: {files_with_terms}")
        print(f"   Total term occurrences: {total_terms}")
        
        if detailed and analysis_results:
            print(f"\n📋 Detailed Analysis:")
            for file_path, analysis in list(analysis_results.items())[:10]:  # Show first 10
                print(f"  📄 {file_path}")
                for term, info in analysis['found_terms'].items():
                    print(f"    {term} → {info['replacement']} ({info['count']}x)")
                    if info['contexts']:
                        print(f"      Context: {info['contexts'][0]}")
        
        return {
            'total_files': len(files_to_process),
            'files_with_terms': files_with_terms,
            'total_occurrences': total_terms,
            'analysis_results': analysis_results
        }
    
    def convert_directory(self, directory: Path, create_backup: bool = True, 
                         use_conservative: bool = False, convert_filenames: bool = True) -> bool:
        """Convert all files in directory"""
        if not directory.exists():
            print(f"❌ Directory {directory} does not exist")
            return False
        
        # Reset statistics
        self.stats = {
            'files_processed': 0,
            'files_changed': 0,
            'terms_replaced': {},
            'errors': []
        }
        
        # Create backup
        backup_path = None
        if create_backup:
            backup_path = self.create_backup(directory)
            if backup_path:
                print(f"✅ Backup created: {backup_path}")
            else:
                print("⚠️ Could not create backup, continuing anyway...")
        
        # Process files
        for file_path in directory.rglob('*'):
            if file_path.is_file() and self.should_process_file(file_path):
                self.stats['files_processed'] += 1
                
                # Convert filename if requested
                if convert_filenames:
                    file_path = self.convert_filename(file_path)
                
                # Convert content
                self.convert_file_content(file_path, use_conservative)
        
        # Show final statistics
        self.show_conversion_summary()
        
        return True
    
    def show_conversion_summary(self):
        """Show comprehensive conversion summary"""
        print(f"\n📊 CONVERSION SUMMARY:")
        print(f"   Files processed: {self.stats['files_processed']}")
        print(f"   Files changed: {self.stats['files_changed']}")
        print(f"   Total terms replaced: {sum(self.stats['terms_replaced'].values())}")
        
        if self.stats['terms_replaced']:
            print(f"\n🔄 Terms Replaced:")
            for term, count in sorted(self.stats['terms_replaced'].items(), 
                                    key=lambda x: x[1], reverse=True):
                replacement = self.terminology_map.get(term, 'Unknown')
                print(f"   {term} → {replacement}: {count}x")
        
        if self.stats['errors']:
            print(f"\n❌ Errors ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:5]:  # Show first 5 errors
                print(f"   {error}")
            if len(self.stats['errors']) > 5:
                print(f"   ... and {len(self.stats['errors']) - 5} more")
    
    def save_conversion_report(self, directory: Path, output_file: str = None):
        """Save detailed conversion report"""
        if output_file is None:
            output_file = f"conversion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'directory': str(directory),
            'statistics': self.stats,
            'terminology_map': self.terminology_map,
            'conversion_settings': {
                'file_extensions': self.file_extensions,
                'skip_directories': list(self.skip_directories)
            }
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"📄 Conversion report saved: {output_file}")
        except Exception as e:
            print(f"❌ Could not save report: {e}")
    
    def add_custom_mapping(self, old_term: str, new_term: str):
        """Add custom terminology mapping"""
        self.terminology_map[old_term] = new_term
        print(f"➕ Added mapping: {old_term} → {new_term}")
    
    def remove_mapping(self, term: str):
        """Remove terminology mapping"""
        if term in self.terminology_map:
            removed = self.terminology_map.pop(term)
            print(f"➖ Removed mapping: {term} → {removed}")
        else:
            print(f"❌ Mapping not found: {term}")
    
    def show_mappings(self, filter_term: str = None):
        """Show current terminology mappings"""
        mappings = self.terminology_map
        
        if filter_term:
            mappings = {k: v for k, v in mappings.items() 
                       if filter_term.lower() in k.lower() or filter_term.lower() in v.lower()}
        
        print(f"📋 Current Mappings ({len(mappings)}):")
        for old_term, new_term in sorted(mappings.items()):
            print(f"   {old_term} → {new_term}")


def main():
    converter = TerminologyConverter()
    
    print("🔄 Solān Terminology Converter v2.0")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. 🔍 Scan directory (preview)")
        print("2. 🔄 Convert directory")
        print("3. ➕ Add custom mapping")
        print("4. 📋 Show mappings")
        print("5. 📄 Generate report")
        print("0. ❌ Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            # Scan directory
            directory = input("Enter directory path (or '.' for current): ").strip()
            if not directory:
                directory = "."
            
            detailed = input("Show detailed analysis? (y/n): ").strip().lower() == 'y'
            
            try:
                path = Path(directory)
                results = converter.scan_directory(path, detailed)
                
                if results['files_with_terms'] > 0:
                    print(f"\n✅ Found {results['total_occurrences']} term occurrences in {results['files_with_terms']} files")
                else:
                    print("\n✅ No terminology found that needs conversion")
                    
            except Exception as e:
                print(f"❌ Error scanning directory: {e}")
        
        elif choice == "2":
            # Convert directory
            directory = input("Enter directory path (or '.' for current): ").strip()
            if not directory:
                directory = "."
            
            # Options
            backup = input("Create backup? (y/n): ").strip().lower() == 'y'
            conservative = input("Use conservative mapping? (y/n): ").strip().lower() == 'y'
            filenames = input("Convert filenames? (y/n): ").strip().lower() == 'y'
            
            # Confirm
            print(f"\n⚠️ About to convert: {directory}")
            print(f"   Backup: {'Yes' if backup else 'No'}")
            print(f"   Mode: {'Conservative' if conservative else 'Full'}")
            print(f"   Filenames: {'Yes' if filenames else 'No'}")
            
            confirm = input("\nProceed? (y/n): ").strip().lower()
            if confirm == 'y':
                try:
                    path = Path(directory)
                    success = converter.convert_directory(path, backup, conservative, filenames)
                    
                    if success:
                        print("\n✅ Conversion completed!")
                        
                        # Ask about report
                        report = input("Generate conversion report? (y/n): ").strip().lower() == 'y'
                        if report:
                            converter.save_conversion_report(path)
                    else:
                        print("\n❌ Conversion failed")
                        
                except Exception as e:
                    print(f"❌ Error during conversion: {e}")
            else:
                print("Conversion cancelled")
        
        elif choice == "3":
            # Add custom mapping
            old_term = input("Enter term to replace: ").strip()
            new_term = input("Enter replacement term: ").strip()
            
            if old_term and new_term:
                converter.add_custom_mapping(old_term, new_term)
            else:
                print("❌ Both terms are required")
        
        elif choice == "4":
            # Show mappings
            filter_term = input("Filter by term (optional): ").strip()
            converter.show_mappings(filter_term if filter_term else None)
        
        elif choice == "5":
            # Generate report
            directory = input("Enter directory path (or '.' for current): ").strip()
            if not directory:
                directory = "."
            
            output_file = input("Output file (optional): ").strip()
            
            try:
                path = Path(directory)
                converter.save_conversion_report(path, output_file if output_file else None)
            except Exception as e:
                print(f"❌ Error generating report: {e}")
        
        else:
            print("❌ Invalid option")


if __name__ == "__main__":
    main()
