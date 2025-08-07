#!/usr/bin/env python3
"""
Solān Code Refactoring Plan & Implementation
Detailed plan voor het refactoren van grote bestanden en complexe functies
"""

import ast
import os
from pathlib import Path
from collections import defaultdict

class SolanRefactoringAnalyzer:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.refactoring_plan = {
            "large_files": [],
            "complex_functions": [],
            "refactoring_suggestions": [],
            "implementation_steps": []
        }
    
    def analyze_large_file(self, file_path, target_lines=300):
        """Analyseer een groot bestand en stel refactoring voor"""
        print(f"🔍 Analyzing {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
            
            classes = []
            functions = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                    classes.append({
                        "name": node.name,
                        "lines": class_lines,
                        "start_line": node.lineno
                    })
                elif isinstance(node, ast.FunctionDef):
                    func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                    functions.append({
                        "name": node.name,
                        "lines": func_lines,
                        "start_line": node.lineno
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports.append(node.lineno)
            
            # Stel module splits voor
            suggestions = self.suggest_module_split(file_path, classes, functions)
            
            return {
                "file": str(file_path),
                "total_lines": len(content.splitlines()),
                "classes": len(classes),
                "functions": len(functions),
                "suggestions": suggestions
            }
            
        except Exception as e:
            print(f"   ❌ Error analyzing {file_path}: {e}")
            return None
    
    def suggest_module_split(self, file_path, classes, functions):
        """Stel voor hoe een bestand gesplitst kan worden"""
        suggestions = []
        
        # Groepeer gerelateerde functies
        if "api" in str(file_path).lower():
            suggestions.append({
                "new_module": f"{file_path.stem}_routes.py",
                "purpose": "API route handlers",
                "estimated_lines": sum(f["lines"] for f in functions if "route" in f["name"].lower() or "endpoint" in f["name"].lower())
            })
            suggestions.append({
                "new_module": f"{file_path.stem}_models.py", 
                "purpose": "Data models and schemas",
                "estimated_lines": sum(c["lines"] for c in classes)
            })
        
        elif "intelligence" in str(file_path).lower():
            suggestions.append({
                "new_module": f"{file_path.stem}_core.py",
                "purpose": "Core intelligence functions",
                "estimated_lines": sum(f["lines"] for f in functions if len(f["name"]) > 10)
            })
            suggestions.append({
                "new_module": f"{file_path.stem}_utils.py",
                "purpose": "Utility functions",
                "estimated_lines": sum(f["lines"] for f in functions if len(f["name"]) <= 10)
            })
        
        return suggestions
    
    def analyze_complex_functions(self, file_path):
        """Analyseer complexe functies in een bestand"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
            
            complex_functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                    
                    if func_lines > 50:  # Complex function threshold
                        # Analyseer functie complexiteit
                        complexity_score = self.calculate_complexity(node)
                        
                        complex_functions.append({
                            "name": node.name,
                            "lines": func_lines,
                            "complexity_score": complexity_score,
                            "start_line": node.lineno,
                            "refactor_suggestion": self.suggest_function_refactor(node, func_lines)
                        })
            
            return complex_functions
            
        except Exception as e:
            print(f"   ❌ Error analyzing functions in {file_path}: {e}")
            return []
    
    def calculate_complexity(self, func_node):
        """Bereken een simpele complexiteit score voor een functie"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(func_node):
            # Tel control flow statements
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
        
        return complexity
    
    def suggest_function_refactor(self, func_node, lines):
        """Stel refactoring voor een complexe functie voor"""
        suggestions = []
        
        if lines > 100:
            suggestions.append("Split into multiple smaller functions")
        elif lines > 75:
            suggestions.append("Extract helper functions for repeated logic")
        elif lines > 50:
            suggestions.append("Consider breaking into logical sections")
        
        # Analyseer voor specifieke patterns
        has_multiple_returns = len([n for n in ast.walk(func_node) if isinstance(n, ast.Return)]) > 3
        if has_multiple_returns:
            suggestions.append("Reduce multiple return statements")
        
        has_nested_loops = False
        for node in ast.walk(func_node):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, (ast.For, ast.While)) and child != node:
                        has_nested_loops = True
                        break
        
        if has_nested_loops:
            suggestions.append("Extract nested loops into separate functions")
        
        return suggestions
    
    def generate_refactoring_plan(self):
        """Genereer een complete refactoring plan"""
        print("🚀 Generating Comprehensive Refactoring Plan")
        print("=" * 60)
        
        # Analyseer de grootste bestanden
        large_files = [
            "solan_digital_intelligence_v3.py",
            "solan_api_server.py", 
            "solan_launch_ethicslab.py",
            "core_identity/ethical_framework.py",
            "src/aether_dream_analysis.py"
        ]
        
        for file_name in large_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                analysis = self.analyze_large_file(file_path)
                if analysis:
                    self.refactoring_plan["large_files"].append(analysis)
                
                complex_funcs = self.analyze_complex_functions(file_path)
                self.refactoring_plan["complex_functions"].extend(complex_funcs)
        
        # Genereer implementatie stappen
        self.generate_implementation_steps()
        
        return self.refactoring_plan
    
    def generate_implementation_steps(self):
        """Genereer concrete implementatie stappen"""
        steps = [
            {
                "phase": "Phase 1: Preparation",
                "tasks": [
                    "Create backup of current codebase",
                    "Set up comprehensive test suite",
                    "Document current API contracts",
                    "Identify critical dependencies"
                ],
                "estimated_time": "1-2 days"
            },
            {
                "phase": "Phase 2: Large File Refactoring", 
                "tasks": [
                    "Split solan_digital_intelligence_v3.py into core modules",
                    "Refactor solan_api_server.py into route modules",
                    "Extract common utilities into shared modules",
                    "Update import statements across codebase"
                ],
                "estimated_time": "3-5 days"
            },
            {
                "phase": "Phase 3: Function Optimization",
                "tasks": [
                    "Break down complex functions (>50 lines)",
                    "Extract helper functions for repeated logic",
                    "Optimize nested loops and conditions",
                    "Improve error handling patterns"
                ],
                "estimated_time": "2-3 days"
            },
            {
                "phase": "Phase 4: Testing & Validation",
                "tasks": [
                    "Run comprehensive test suite",
                    "Validate API functionality",
                    "Performance regression testing",
                    "Update documentation"
                ],
                "estimated_time": "1-2 days"
            }
        ]
        
        self.refactoring_plan["implementation_steps"] = steps
    
    def print_detailed_recommendations(self):
        """Print gedetailleerde aanbevelingen"""
        plan = self.generate_refactoring_plan()
        
        print("\n📋 DETAILED REFACTORING RECOMMENDATIONS")
        print("=" * 60)
        
        # Large Files
        print("\n🔍 LARGE FILES ANALYSIS:")
        for file_analysis in plan["large_files"]:
            print(f"\n📄 {file_analysis['file']} ({file_analysis['total_lines']} lines)")
            print(f"   Classes: {file_analysis['classes']}, Functions: {file_analysis['functions']}")
            
            for suggestion in file_analysis["suggestions"]:
                print(f"   💡 Create {suggestion['new_module']}")
                print(f"      Purpose: {suggestion['purpose']}")
                print(f"      Est. lines: {suggestion['estimated_lines']}")
        
        # Complex Functions
        print(f"\n🔧 COMPLEX FUNCTIONS ({len(plan['complex_functions'])} found):")
        for func in plan["complex_functions"][:10]:  # Show top 10
            print(f"\n🔹 {func['name']} ({func['lines']} lines, complexity: {func['complexity_score']})")
            for suggestion in func["refactor_suggestion"]:
                print(f"   💡 {suggestion}")
        
        # Implementation Steps
        print(f"\n🚀 IMPLEMENTATION PLAN:")
        for step in plan["implementation_steps"]:
            print(f"\n📋 {step['phase']} ({step['estimated_time']})")
            for task in step["tasks"]:
                print(f"   • {task}")
        
        print(f"\n🎯 TOTAL ESTIMATED TIME: 7-12 days")
        print(f"💡 RECOMMENDATION: Implement in phases to maintain system stability")

if __name__ == "__main__":
    analyzer = SolanRefactoringAnalyzer()
    analyzer.print_detailed_recommendations()
