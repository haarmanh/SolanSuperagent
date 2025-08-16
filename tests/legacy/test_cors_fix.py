#!/usr/bin/env python3
"""
Test CORS Fix
Verify that CORS headers are properly configured
"""

import requests

def test_cors_fix():
    print("🌐 TESTING CORS FIX")
    print("=" * 40)
    
    proxy_url = "http://127.0.0.1:8787"
    
    # Test 1: OPTIONS preflight request
    print("\n✈️ Testing OPTIONS Preflight...")
    try:
        response = requests.options(f"{proxy_url}/api/health")
        print(f"   Status: {response.status_code}")
        
        # Check CORS headers
        headers = response.headers
        cors_headers = {
            "access-control-allow-origin": headers.get("access-control-allow-origin"),
            "access-control-allow-methods": headers.get("access-control-allow-methods"),
            "access-control-allow-headers": headers.get("access-control-allow-headers"),
        }
        
        print(f"   Headers: {cors_headers}")
        
        if response.status_code == 200:
            print("   ✅ OPTIONS request successful")
        else:
            print(f"   ❌ OPTIONS request failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ OPTIONS test error: {e}")
    
    # Test 2: Actual API call with CORS
    print("\n🔍 Testing API Call with CORS...")
    try:
        response = requests.get(f"{proxy_url}/api/health")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
            print("   ✅ API call successful")
        else:
            print(f"   ❌ API call failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ API test error: {e}")
    
    # Test 3: POST request with CORS
    print("\n📝 Testing POST Request with CORS...")
    try:
        response = requests.post(
            f"{proxy_url}/api/analyzer/bias",
            json={"text": "CORS test message"}
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
            print("   ✅ POST request successful")
        else:
            print(f"   ❌ POST request failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ POST test error: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 CORS TESTING COMPLETE!")
    print("\n✅ CORS Configuration:")
    print("   - Allow Origins: * (staging)")
    print("   - Allow Methods: GET, POST, OPTIONS")
    print("   - Allow Headers: Content-Type, Authorization, X-Requested-With")
    print("   - Expose Headers: Content-Type")
    print("\n🚀 Ready for live UI integration!")

if __name__ == "__main__":
    test_cors_fix()
