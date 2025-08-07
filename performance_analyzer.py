#!/usr/bin/env python3
"""
Solān Platform Performance Analyzer
Analyzes code quality, performance bottlenecks, and optimization opportunities
"""

import os
import ast
import time
import json
import requests
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class SolanPerformanceAnalyzer:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root)
        self.analysis_report = {
            "timestamp": datetime.now().isoformat(),
            "code_quality": {},
            "performance_issues": [],
            "optimization_suggestions": [],
            "api_performance": {},
            "file_analysis": {}
        }
    
    def analyze_python_files(self):
        """Analyze Python files for performance issues"""
        print("🔍 Analyzing Python code quality...")
        
        python_files = list(self.project_root.rglob("*.py"))
        total_lines = 0
        total_functions = 0
        large_files = []
        complex_functions = []
        
        for py_file in python_files:
            if "__pycache__" in str(py_file) or "node_modules" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.splitlines())
                    total_lines += lines
                    
                    # Check for large files
                    if lines > 500:
                        large_files.append({"file": str(py_file), "lines": lines})
                    
                    # Parse AST for function analysis
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                total_functions += 1
                                # Check for complex functions (rough estimate)
                                func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                                if func_lines > 50:
                                    complex_functions.append({
                                        "file": str(py_file),
                                        "function": node.name,
                                        "lines": func_lines
                                    })
                    except SyntaxError:
                        pass
                        
            except Exception as e:
                print(f"   ⚠️  Error analyzing {py_file}: {e}")
        
        self.analysis_report["code_quality"] = {
            "total_python_files": len(python_files),
            "total_lines": total_lines,
            "total_functions": total_functions,
            "large_files": large_files,
            "complex_functions": complex_functions
        }
        
        print(f"   📊 Analyzed {len(python_files)} Python files")
        print(f"   📝 Total lines of code: {total_lines:,}")
        print(f"   🔧 Total functions: {total_functions}")
        
        if large_files:
            print(f"   ⚠️  Found {len(large_files)} large files (>500 lines)")
        if complex_functions:
            print(f"   ⚠️  Found {len(complex_functions)} complex functions (>50 lines)")
    
    def test_api_performance(self):
        """Test API endpoint performance"""
        print("🌐 Testing API performance...")
        
        api_base = "http://localhost:8000"
        endpoints_to_test = [
            "/health",
            "/api/system/status",
            "/cache/stats",
            "/dashboard-data",
            "/api/consciousness-core/identity"
        ]
        
        performance_results = {}
        
        for endpoint in endpoints_to_test:
            url = f"{api_base}{endpoint}"
            try:
                start_time = time.time()
                response = requests.get(url, timeout=5)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # Convert to ms
                
                performance_results[endpoint] = {
                    "response_time_ms": round(response_time, 2),
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                status_emoji = "✅" if response.status_code == 200 else "❌"
                print(f"   {status_emoji} {endpoint}: {response_time:.2f}ms")
                
            except requests.exceptions.RequestException as e:
                performance_results[endpoint] = {
                    "error": str(e),
                    "success": False
                }
                print(f"   ❌ {endpoint}: Error - {e}")
        
        self.analysis_report["api_performance"] = performance_results
        
        # Calculate average response time
        successful_tests = [r for r in performance_results.values() if r.get("success")]
        if successful_tests:
            avg_response_time = sum(r["response_time_ms"] for r in successful_tests) / len(successful_tests)
            print(f"   📊 Average response time: {avg_response_time:.2f}ms")
    
    def analyze_file_structure(self):
        """Analyze project file structure for optimization"""
        print("📁 Analyzing file structure...")
        
        file_types = defaultdict(lambda: {"count": 0, "total_size": 0})
        
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                suffix = file_path.suffix.lower() or "no_extension"
                size = file_path.stat().st_size
                
                file_types[suffix]["count"] += 1
                file_types[suffix]["total_size"] += size
        
        # Sort by total size
        sorted_types = sorted(file_types.items(), key=lambda x: x[1]["total_size"], reverse=True)
        
        print("   📊 File type analysis (top 10 by size):")
        for i, (ext, data) in enumerate(sorted_types[:10]):
            size_mb = data["total_size"] / (1024 * 1024)
            print(f"   {i+1:2d}. {ext:15s}: {data['count']:4d} files, {size_mb:8.2f} MB")
        
        self.analysis_report["file_analysis"] = dict(sorted_types)
    
    def generate_optimization_suggestions(self):
        """Generate optimization suggestions based on analysis"""
        print("💡 Generating optimization suggestions...")
        
        suggestions = []
        
        # Code quality suggestions
        if self.analysis_report["code_quality"]["large_files"]:
            suggestions.append({
                "category": "Code Quality",
                "issue": "Large files detected",
                "suggestion": "Consider breaking down large files into smaller modules",
                "files": [f["file"] for f in self.analysis_report["code_quality"]["large_files"][:3]]
            })
        
        if self.analysis_report["code_quality"]["complex_functions"]:
            suggestions.append({
                "category": "Code Quality", 
                "issue": "Complex functions detected",
                "suggestion": "Consider refactoring complex functions into smaller ones",
                "functions": [f"{f['file']}:{f['function']}" for f in self.analysis_report["code_quality"]["complex_functions"][:3]]
            })
        
        # API performance suggestions
        api_perf = self.analysis_report.get("api_performance", {})
        slow_endpoints = [ep for ep, data in api_perf.items() if data.get("response_time_ms", 0) > 100]
        if slow_endpoints:
            suggestions.append({
                "category": "API Performance",
                "issue": "Slow API endpoints detected",
                "suggestion": "Consider adding caching or optimizing database queries",
                "endpoints": slow_endpoints
            })
        
        # File structure suggestions
        file_analysis = self.analysis_report.get("file_analysis", {})
        if ".wav" in file_analysis and file_analysis[".wav"]["total_size"] > 10 * 1024 * 1024:  # >10MB
            suggestions.append({
                "category": "Storage",
                "issue": "Large audio files detected",
                "suggestion": "Consider implementing audio file cleanup or compression",
                "size_mb": file_analysis[".wav"]["total_size"] / (1024 * 1024)
            })
        
        self.analysis_report["optimization_suggestions"] = suggestions
        
        print(f"   💡 Generated {len(suggestions)} optimization suggestions")
        for suggestion in suggestions:
            print(f"   • {suggestion['category']}: {suggestion['issue']}")
    
    def run_analysis(self):
        """Run complete performance analysis"""
        print("🚀 Starting Solān Platform Performance Analysis")
        print("=" * 60)
        
        self.analyze_python_files()
        print()
        self.test_api_performance()
        print()
        self.analyze_file_structure()
        print()
        self.generate_optimization_suggestions()
        
        # Save analysis report
        report_path = self.project_root / "performance_analysis.json"
        with open(report_path, "w") as f:
            json.dump(self.analysis_report, f, indent=2)
        
        print("\n" + "=" * 60)
        print("🎉 PERFORMANCE ANALYSIS COMPLETED!")
        print(f"📝 Report saved to: {report_path}")
        
        return self.analysis_report

if __name__ == "__main__":
    analyzer = SolanPerformanceAnalyzer()
    analyzer.run_analysis()
