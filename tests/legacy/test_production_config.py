#!/usr/bin/env python3
"""
Test Production Configuration
Test the production configuration system
"""

import os
import sys
from pathlib import Path

def test_production_config():
    """Test production configuration loading"""
    print("🔧 TESTING PRODUCTION CONFIGURATION")
    print("=" * 50)
    
    try:
        # Test configuration import
        from production_config import get_settings, get_uvicorn_config, print_config_summary
        print("   ✅ Production config imports successful")
        
        # Test settings loading
        settings = get_settings()
        print(f"   ✅ Settings loaded: {type(settings).__name__}")
        
        # Test basic settings
        print(f"   ✅ API Host: {settings.api_host}")
        print(f"   ✅ API Port: {settings.api_port}")
        print(f"   ✅ Debug Mode: {settings.debug}")
        print(f"   ✅ Rate Limiting: {settings.rate_limit_enabled}")
        
        # Test Uvicorn config
        uvicorn_config = get_uvicorn_config(settings)
        print(f"   ✅ Uvicorn config generated: {len(uvicorn_config)} settings")
        
        # Test config summary
        print("\n📋 Configuration Summary:")
        print_config_summary(settings)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration test failed: {e}")
        return False

def test_main_server_imports():
    """Test main server imports with production config"""
    print("\n🚀 TESTING MAIN SERVER IMPORTS")
    print("=" * 50)
    
    try:
        # Test main server import
        import main_server
        print("   ✅ Main server imports successful")
        
        # Test FastAPI app creation
        app = main_server.app
        print(f"   ✅ FastAPI app created: {type(app).__name__}")
        
        # Test settings integration
        settings = main_server.settings
        print(f"   ✅ Settings integrated: {settings.api_title}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Main server test failed: {e}")
        return False

def test_observatorium_files():
    """Test observatorium files exist"""
    print("\n🌐 TESTING OBSERVATORIUM FILES")
    print("=" * 50)
    
    files_to_check = [
        "solan_observatorium.html",
        "requirements.txt",
        "production_config.py",
        "setup_production.py",
        "main_server.py"
    ]
    
    project_root = Path(__file__).parent
    missing_files = []
    
    for file_name in files_to_check:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"   ✅ {file_name} exists ({file_path.stat().st_size} bytes)")
        else:
            print(f"   ❌ {file_name} missing")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"   ⚠️ Missing files: {missing_files}")
        return False
    
    return True

def test_environment_variables():
    """Test environment variable handling"""
    print("\n⚙️ TESTING ENVIRONMENT VARIABLES")
    print("=" * 50)
    
    try:
        # Test default environment
        os.environ.pop("ENVIRONMENT", None)
        from production_config import get_settings
        settings = get_settings()
        print(f"   ✅ Default environment: {type(settings).__name__}")
        
        # Test development environment
        os.environ["ENVIRONMENT"] = "development"
        # Clear cache
        get_settings.cache_clear()
        settings = get_settings()
        print(f"   ✅ Development environment: debug={settings.debug}")
        
        # Test production environment
        os.environ["ENVIRONMENT"] = "production"
        get_settings.cache_clear()
        settings = get_settings()
        print(f"   ✅ Production environment: debug={settings.debug}")
        
        # Clean up
        os.environ.pop("ENVIRONMENT", None)
        get_settings.cache_clear()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Environment test failed: {e}")
        return False

def test_requirements_file():
    """Test requirements.txt file"""
    print("\n📦 TESTING REQUIREMENTS FILE")
    print("=" * 50)
    
    try:
        requirements_file = Path(__file__).parent / "requirements.txt"
        
        if not requirements_file.exists():
            print("   ❌ requirements.txt not found")
            return False
        
        with open(requirements_file, 'r') as f:
            content = f.read()
        
        # Check for essential packages
        essential_packages = [
            "fastapi",
            "uvicorn",
            "pydantic",
            "slowapi",
            "python-dotenv"
        ]
        
        missing_packages = []
        for package in essential_packages:
            if package not in content.lower():
                missing_packages.append(package)
            else:
                print(f"   ✅ {package} found in requirements")
        
        if missing_packages:
            print(f"   ❌ Missing packages: {missing_packages}")
            return False
        
        print(f"   ✅ Requirements file valid ({len(content)} characters)")
        return True
        
    except Exception as e:
        print(f"   ❌ Requirements test failed: {e}")
        return False

def main():
    """Run all production tests"""
    print("🚀 SOLĀN AI OBSERVATORIUM - PRODUCTION TESTS")
    print("=" * 60)
    
    tests = [
        ("Production Configuration", test_production_config),
        ("Main Server Imports", test_main_server_imports),
        ("Observatorium Files", test_observatorium_files),
        ("Environment Variables", test_environment_variables),
        ("Requirements File", test_requirements_file)
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
    print("🎉 PRODUCTION TEST RESULTS")
    print(f"✅ Passed: {sum(results)}/{len(results)} tests")
    
    if all(results):
        print("🌟 ALL PRODUCTION TESTS PASSED!")
        print("\n📊 PRODUCTION READINESS:")
        print("   ✅ Configuration system working")
        print("   ✅ Main server integration complete")
        print("   ✅ All required files present")
        print("   ✅ Environment handling functional")
        print("   ✅ Dependencies properly defined")
        print("\n🚀 READY FOR PRODUCTION DEPLOYMENT!")
        return True
    else:
        print("⚠️ Some production tests failed - check errors above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
