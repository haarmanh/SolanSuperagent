#!/usr/bin/env python3
"""
Test RBAC Security
"""

import requests

def test_rbac():
    print("🔑 Testing RBAC Security...")
    
    # Test direct API access to secured endpoint
    try:
        response = requests.post(
            "http://127.0.0.1:8000/analyzer/bias",
            json={"text": "test"}
        )
        print(f"Direct API bias endpoint (no key): {response.status_code}")
        
        if response.status_code == 401:
            print("✅ RBAC: Secured endpoints properly protected")
        else:
            print(f"❌ RBAC: Secured endpoint not protected ({response.status_code})")
            
    except Exception as e:
        print(f"❌ RBAC test error: {e}")
    
    # Test with proper key
    try:
        response = requests.post(
            "http://127.0.0.1:8000/analyzer/bias",
            headers={"X-API-Key": "analyst-key"},
            json={"text": "test"}
        )
        print(f"Direct API bias endpoint (with key): {response.status_code}")
        
        if response.status_code == 200:
            print("✅ RBAC: Proper key authentication works")
        else:
            print(f"❌ RBAC: Key authentication failed ({response.status_code})")
            
    except Exception as e:
        print(f"❌ RBAC key test error: {e}")

if __name__ == "__main__":
    test_rbac()
