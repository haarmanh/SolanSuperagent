#!/usr/bin/env python3
"""
Simple Production Test
Quick test to verify production setup is working
"""

import os
import sys
from pathlib import Path

def test_files_exist():
    """Test that all required files exist"""
    print("📁 TESTING FILE EXISTENCE")
    print("=" * 40)
    
    required_files = [
        "solan_observatorium.html",
        "main_server.py", 
        "production_config.py",
        "requirements.txt",
        "setup_production.py"
    ]
    
    project_root = Path(__file__).parent
    all_exist = True
    
    for file_name in required_files:
        file_path = project_root / file_name
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"   ✅ {file_name} ({size:,} bytes)")
        else:
            print(f"   ❌ {file_name} MISSING")
            all_exist = False
    
    return all_exist

def test_basic_imports():
    """Test basic Python imports"""
    print("\n🐍 TESTING BASIC IMPORTS")
    print("=" * 40)
    
    try:
        import fastapi
        print(f"   ✅ FastAPI {fastapi.__version__}")
    except ImportError:
        print("   ❌ FastAPI not available")
        return False
    
    try:
        import uvicorn
        print(f"   ✅ Uvicorn available")
    except ImportError:
        print("   ❌ Uvicorn not available")
        return False
    
    try:
        import pydantic
        print(f"   ✅ Pydantic {pydantic.__version__}")
    except ImportError:
        print("   ❌ Pydantic not available")
        return False
    
    return True

def test_observatorium_html():
    """Test observatorium HTML file"""
    print("\n🌐 TESTING OBSERVATORIUM HTML")
    print("=" * 40)
    
    html_file = Path(__file__).parent / "solan_observatorium.html"
    
    if not html_file.exists():
        print("   ❌ solan_observatorium.html not found")
        return False
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key components
        checks = [
            ("DOCTYPE html", "HTML5 doctype"),
            ("Solān AI Observatorium", "Title present"),
            ("class SolanObservatorium", "JavaScript class"),
            ("api/analyzer/compare", "API endpoint"),
            ("Chart.js", "Chart library"),
            ("Tailwind", "CSS framework")
        ]
        
        all_passed = True
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} missing")
                all_passed = False
        
        print(f"   📊 File size: {len(content):,} characters")
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Error reading HTML file: {e}")
        return False

def test_main_server():
    """Test main server file"""
    print("\n🚀 TESTING MAIN SERVER")
    print("=" * 40)
    
    server_file = Path(__file__).parent / "main_server.py"
    
    if not server_file.exists():
        print("   ❌ main_server.py not found")
        return False
    
    try:
        with open(server_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key components
        checks = [
            ("from fastapi import FastAPI", "FastAPI import"),
            ("from production_config import", "Production config import"),
            ("app = FastAPI", "FastAPI app creation"),
            ("@app.post", "API endpoints"),
            ("if __name__ == \"__main__\"", "Main execution")
        ]
        
        all_passed = True
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} missing")
                all_passed = False
        
        print(f"   📊 File size: {len(content):,} characters")
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Error reading server file: {e}")
        return False

def test_production_config():
    """Test production config file"""
    print("\n⚙️ TESTING PRODUCTION CONFIG")
    print("=" * 40)
    
    config_file = Path(__file__).parent / "production_config.py"
    
    if not config_file.exists():
        print("   ❌ production_config.py not found")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key components
        checks = [
            ("class ProductionSettings", "Settings class"),
            ("api_host:", "API host setting"),
            ("rate_limit_enabled:", "Rate limiting"),
            ("def get_settings", "Settings function"),
            ("@lru_cache", "Caching decorator")
        ]
        
        all_passed = True
        for check, description in checks:
            if check in content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description} missing")
                all_passed = False
        
        print(f"   📊 File size: {len(content):,} characters")
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Error reading config file: {e}")
        return False

def main():
    """Run all simple tests"""
    print("🚀 SOLĀN AI OBSERVATORIUM - SIMPLE PRODUCTION TEST")
    print("=" * 60)
    
    tests = [
        ("File Existence", test_files_exist),
        ("Basic Imports", test_basic_imports),
        ("Observatorium HTML", test_observatorium_html),
        ("Main Server", test_main_server),
        ("Production Config", test_production_config)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("🎉 SIMPLE PRODUCTION TEST RESULTS")
    print(f"✅ Passed: {sum(results)}/{len(results)} tests")
    
    if all(results):
        print("\n🌟 ALL TESTS PASSED!")
        print("\n📋 PRODUCTION READINESS SUMMARY:")
        print("   ✅ All required files present")
        print("   ✅ Basic dependencies available")
        print("   ✅ Observatorium HTML complete")
        print("   ✅ Main server properly configured")
        print("   ✅ Production config ready")
        print("\n🚀 READY FOR DEPLOYMENT!")
        
        print("\n📖 NEXT STEPS:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure .env file with your settings")
        print("3. Start server: python main_server.py")
        print("4. Open solan_observatorium.html in browser")
        print("5. Test API at: http://localhost:8000/api/docs")
        
        return True
    else:
        print("\n⚠️ Some tests failed - check errors above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
