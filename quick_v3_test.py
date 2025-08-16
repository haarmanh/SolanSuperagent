#!/usr/bin/env python3
"""
Quick Solān v3.0 API Test
"""

import requests
import json

def test_api():
    print("🚀 TESTING SOLĀN V3.0 API")
    print("=" * 40)
    
    # Test health endpoint
    try:
        response = requests.get(
            "http://127.0.0.1:8000/health",
            headers={"X-API-Key": "admin-key"}
        )
        print(f"✅ Health: {response.json()}")
    except Exception as e:
        print(f"❌ Health failed: {e}")
    
    # Test bias detection
    try:
        response = requests.post(
            "http://127.0.0.1:8000/analyzer/bias",
            headers={"X-API-Key": "analyst-key", "Content-Type": "application/json"},
            json={"text": "Only trust those who always agree with me"}
        )
        print(f"✅ Bias Detection: {response.json()}")
    except Exception as e:
        print(f"❌ Bias detection failed: {e}")
    
    # Test alignment
    try:
        response = requests.post(
            "http://127.0.0.1:8000/analyzer/alignment",
            headers={"X-API-Key": "admin-key", "Content-Type": "application/json"},
            json={"claims": {"truth": 0.9, "freedom": 0.8}}
        )
        print(f"✅ Alignment: {response.json()}")
    except Exception as e:
        print(f"❌ Alignment failed: {e}")

if __name__ == "__main__":
    test_api()
