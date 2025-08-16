#!/usr/bin/env python3
"""
Quick Rate Limit Test - Test 70 requests to trigger 429
"""
import requests
import time
import json

def test_rate_limit():
    url = "http://127.0.0.1:8787/api/health"
    
    print("🔄 Testing rate limit (70 requests)...")
    print("Expected: First ~60 should succeed, then 429 errors")
    
    success_count = 0
    rate_limited_count = 0
    
    for i in range(70):
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                success_count += 1
                print(f"✅ Request {i+1}: OK")
            elif response.status_code == 429:
                rate_limited_count += 1
                print(f"🚫 Request {i+1}: Rate limited (429) - EXPECTED!")
            else:
                print(f"⚠️ Request {i+1}: Unexpected status {response.status_code}")
        except Exception as e:
            print(f"❌ Request {i+1}: Error - {e}")
        
        # Small delay to avoid overwhelming
        time.sleep(0.1)
    
    print(f"\n📊 Results:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   🚫 Rate limited: {rate_limited_count}")
    print(f"   🎯 Rate limiting {'WORKING' if rate_limited_count > 0 else 'NOT TRIGGERED'}")

if __name__ == "__main__":
    test_rate_limit()
