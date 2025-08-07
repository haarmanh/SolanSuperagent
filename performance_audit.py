#!/usr/bin/env python3
"""
Comprehensive Performance Audit van het Solan+Aether systeem
"""

import os
import sys
import time
import json
import requests
from pathlib import Path

def print_section(title):
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print('='*60)

def audit_file_structure():
    """Audit bestandsstructuur en grootte"""
    print_section("File Structure Audit")
    
    project_root = Path(".")
    total_size = 0
    file_counts = {}
    large_files = []
    
    for root, dirs, files in os.walk(project_root):
        # Skip hidden directories en __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if file.startswith('.'):
                continue
                
            file_path = Path(root) / file
            try:
                size = file_path.stat().st_size
                total_size += size
                
                # Track file types
                ext = file_path.suffix.lower()
                file_counts[ext] = file_counts.get(ext, 0) + 1
                
                # Track large files (>1MB)
                if size > 1024 * 1024:
                    large_files.append((file_path, size / (1024 * 1024)))
                    
            except (OSError, PermissionError):
                continue
    
    # Results
    print(f"📁 Total Size: {total_size / (1024 * 1024):.1f} MB")
    print(f"📁 Large Files (>1MB): {len(large_files)}")

    # Top file types
    sorted_types = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"📁 File Types:")
    for ext, count in sorted_types:
        print(f"   {ext or 'no ext'}: {count}")

    if large_files:
        print(f"\n🔍 Large Files:")
        for file_path, size_mb in sorted(large_files, key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {file_path}: {size_mb:.1f} MB")
    
    return total_size, len(large_files)

def audit_memory_uexpert():
    """Audit geheugengebruik (simplified)"""
    print_section("Memory Uexpert Audit")

    # Basic memory info from system
    try:
        import resource
        memory_uexpert = resource.getruexpert(resource.RUEXPERT_SELF).ru_maxrss
        # On Windows, this is in bytes, on Unix it's in KB
        if sys.platform == "win32":
            memory_mb = memory_uexpert / (1024 * 1024)
        else:
            memory_mb = memory_uexpert / 1024

        print(f"🧠 Current Memory Uexpert: {memory_mb:.1f} MB")
    except ImportError:
        memory_mb = 100  # Estimate
        print(f"🧠 Memory monitoring not available (estimated: {memory_mb} MB)")

    return memory_mb

def audit_api_performance():
    """Test API response times"""
    print_section("API Performance Audit")
    
    endpoints = [
        "/api/analytics/summary",
        "/api/analytics/trends", 
        "/api/analytics/insights",
        "/api/journal/entries?limit=10"
    ]
    
    results = []

    for endpoint in endpoints:
        print(f"⚡ Testing {endpoint}...")

        times = []
        for i in range(3):  # Test 3 times
            try:
                start = time.time()
                response = requests.get(f"http://localhost:8002{endpoint}", timeout=10)
                end = time.time()

                if response.status_code == 200:
                    times.append((end - start) * 1000)  # Convert to ms
                else:
                    times.append(None)

            except Exception as e:
                times.append(None)

        # Calculate stats
        valid_times = [t for t in times if t is not None]
        if valid_times:
            avg_time = sum(valid_times) / len(valid_times)
            min_time = min(valid_times)
            max_time = max(valid_times)
            success_rate = len(valid_times) / len(times) * 100
        else:
            avg_time = min_time = max_time = 0
            success_rate = 0

        results.append({
            'endpoint': endpoint,
            'avg_ms': avg_time,
            'min_ms': min_time,
            'max_ms': max_time,
            'success_rate': success_rate
        })
    
    # Display results
    print(f"\n⚡ API Performance Results:")
    for result in results:
        status = "✅" if result['success_rate'] == 100 else "⚠️" if result['success_rate'] > 0 else "❌"
        avg_str = f"{result['avg_ms']:.1f}ms" if result['avg_ms'] > 0 else "FAIL"
        print(f"   {status} {result['endpoint']}: {avg_str} (success: {result['success_rate']:.0f}%)")
    return results

def audit_database_performance():
    """Test journal loading performance"""
    print_section("Database Performance Audit")
    
    journal_dir = Path("memory/journal/entries")
    
    if not journal_dir.exists():
        print("❌ Journal directory not found")
        return {}
    
    # Count files
    json_files = list(journal_dir.glob("*.json"))
    total_files = len(json_files)
    
    # Test loading speed
    start_time = time.time()
    loaded_count = 0
    total_size = 0
    
    for file_path in json_files[:20]:  # Test first 20 files
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                loaded_count += 1
                total_size += file_path.stat().st_size
        except Exception:
            continue
    
    end_time = time.time()
    load_time = (end_time - start_time) * 1000  # ms
    
    print(f"💾 Total JSON Files: {total_files}")
    print(f"💾 Test Files Loaded: {loaded_count}")
    print(f"💾 Load Time (20 files): {load_time:.1f} ms")
    print(f"💾 Avg per File: {load_time/max(loaded_count,1):.1f} ms")
    print(f"💾 Estimated Full Load: {(load_time/max(loaded_count,1)) * total_files:.0f} ms")
    print(f"💾 Total Data Size: {total_size / 1024:.1f} KB")
    
    return {
        'total_files': total_files,
        'load_time_ms': load_time,
        'files_per_second': loaded_count / (load_time / 1000) if load_time > 0 else 0
    }

def generate_recommendations(file_audit, memory_mb, api_results, db_results):
    """Genereer performance aanbevelingen"""
    print_section("Performance Recommendations")
    
    recommendations = []
    
    # File structure recommendations
    if file_audit[1] > 5:  # More than 5 large files
        recommendations.append("🗂️  Consider compressing or archiving large files")
    
    # Memory recommendations
    if memory_mb > 500:
        recommendations.append("🧠 High memory uexpert - consider implementing data pagination")
    elif memory_mb > 200:
        recommendations.append("🧠 Moderate memory uexpert - monitor for memory leaks")
    else:
        recommendations.append("✅ Memory uexpert is optimal")
    
    # API recommendations
    slow_apis = [r for r in api_results if r['avg_ms'] > 1000]
    if slow_apis:
        recommendations.append("⚡ Some APIs are slow (>1s) - consider caching or optimization")
    elif any(r['avg_ms'] > 500 for r in api_results):
        recommendations.append("⚡ Some APIs are moderate (>500ms) - consider minor optimizations")
    else:
        recommendations.append("✅ API performance is good")
    
    # Database recommendations
    if db_results.get('files_per_second', 0) < 50:
        recommendations.append("💾 JSON loading is slow - consider database migration")
    elif db_results.get('total_files', 0) > 100:
        recommendations.append("💾 Many JSON files - consider implementing indexing")
    else:
        recommendations.append("✅ Database performance is acceptable")
    
    # General recommendations
    recommendations.extend([
        "🔧 Consider implementing Redis caching for frequently accessed data",
        "📊 Add performance monitoring and logging",
        "🚀 Consider implementing lazy loading for large datasets",
        "🔄 Implement background processing for heavy analytics"
    ])
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i:2d}. {rec}")

def main():
    print("🔍 Starting Comprehensive Performance Audit...")
    print("=" * 60)
    
    # Run audits
    file_audit = audit_file_structure()

    memory_mb = audit_memory_uexpert()

    api_results = audit_api_performance()

    db_results = audit_database_performance()

    # Generate recommendations
    generate_recommendations(file_audit, memory_mb, api_results, db_results)

    print("\n" + "=" * 60)
    print("🎉 Performance Audit Complete!")

if __name__ == "__main__":
    main()
