#!/usr/bin/env python3
"""
Focused Rate Limit Test - Same endpoint repeatedly
"""
import requests
import time

def test_rate_limit_focused():
    url = "http://127.0.0.1:8787/api/analyzer/bias"
    
    print("🔄 Testing rate limit on bias endpoint (65 requests)...")
    print("Expected: First ~60 should succeed, then 429 errors")
    
    success_count = 0
    rate_limited_count = 0
    
    for i in range(65):
        try:
            response = requests.post(
                url, 
                json={"text": f"Test message {i}"}, 
                timeout=2
            )
            if response.status_code == 200:
                success_count += 1
                print(f"✅ Request {i+1}: OK")
            elif response.status_code == 429:
                rate_limited_count += 1
                print(f"🚫 Request {i+1}: Rate limited (429) - EXPECTED!")
                break  # Stop after first rate limit
            else:
                print(f"⚠️ Request {i+1}: Unexpected status {response.status_code}")
        except Exception as e:
            print(f"❌ Request {i+1}: Error - {e}")
        
        # No delay to trigger rate limit faster
    
    print(f"\n📊 Results:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   🚫 Rate limited: {rate_limited_count}")
    print(f"   🎯 Rate limiting {'WORKING' if rate_limited_count > 0 else 'NOT TRIGGERED'}")

if __name__ == "__main__":
    test_rate_limit_focused()
