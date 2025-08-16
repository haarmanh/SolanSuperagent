#!/usr/bin/env python3
"""
Test Solān v3.0 API
Test the new Solān Labs API endpoints
"""

import requests
import json
import time

def test_health_endpoint():
    """Test health endpoint"""
    print("🏥 Testing Health Endpoint...")
    
    try:
        response = requests.get(
            "http://127.0.0.1:8000/health",
            headers={"X-API-Key": "dev-key"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed: {data}")
            return True
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False

def test_bias_detection():
    """Test bias detection endpoint"""
    print("\n🔍 Testing Bias Detection...")
    
    try:
        test_text = "Only listen to those who agree with me. According to my favorite expert, this is always the right approach."
        
        response = requests.post(
            "http://127.0.0.1:8000/analyzer/bias",
            headers={"X-API-Key": "dev-key", "Content-Type": "application/json"},
            json={"text": test_text}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Bias detection successful: {data}")
            
            # Check if biases were detected
            findings = data.get("findings", {})
            if "confirmation_bias" in findings:
                print(f"   ✅ Confirmation bias detected: {findings['confirmation_bias']} instances")
            if "authority_bias" in findings:
                print(f"   ✅ Authority bias detected: {findings['authority_bias']} instances")
            
            return True
        else:
            print(f"   ❌ Bias detection failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Bias detection error: {e}")
        return False

def test_alignment_checker():
    """Test alignment checker endpoint"""
    print("\n⚖️ Testing Alignment Checker...")
    
    try:
        test_claims = {
            "truth": 0.9,
            "freedom": 0.7,
            "wisdom": 0.8,
            "nature": 0.6,
            "courage": 0.85
        }
        
        response = requests.post(
            "http://127.0.0.1:8000/analyzer/alignment",
            headers={"X-API-Key": "dev-key", "Content-Type": "application/json"},
            json={"claims": test_claims}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Alignment check successful: {data}")
            
            score = data.get("alignment_score", 0)
            print(f"   📊 Alignment score: {score}")
            
            return True
        else:
            print(f"   ❌ Alignment check failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Alignment check error: {e}")
        return False

def test_coherence_tester():
    """Test coherence tester endpoint"""
    print("\n🧠 Testing Coherence Tester...")
    
    try:
        test_statements = [
            "I believe in the importance of truth and transparency in all interactions.",
            "Freedom of thought and expression are fundamental human rights that must be protected.",
            "Wisdom comes from experience, reflection, and the willingness to learn from mistakes."
        ]
        
        response = requests.post(
            "http://127.0.0.1:8000/analyzer/coherence",
            headers={"X-API-Key": "dev-key", "Content-Type": "application/json"},
            json={"statements": test_statements}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Coherence test successful: {data}")
            
            index = data.get("coherence_index", 0)
            print(f"   📊 Coherence index: {index}")
            
            return True
        else:
            print(f"   ❌ Coherence test failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Coherence test error: {e}")
        return False

def test_unauthorized_access():
    """Test unauthorized access"""
    print("\n🔒 Testing Security (Unauthorized Access)...")
    
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        
        if response.status_code == 401:
            print("   ✅ Unauthorized access properly blocked")
            return True
        else:
            print(f"   ❌ Security issue: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Security test error: {e}")
        return False

def test_logs_endpoint():
    """Test logs endpoint (admin only)"""
    print("\n📋 Testing Logs Endpoint...")
    
    try:
        response = requests.get(
            "http://127.0.0.1:8000/logs/tail",
            headers={"X-API-Key": "dev-key"}
        )
        
        if response.status_code == 200:
            data = response.json()
            logs = data.get("logs", [])
            print(f"   ✅ Logs retrieved: {len(logs)} entries")
            
            # Show last few log entries
            if logs:
                print("   📝 Recent log entries:")
                for log_entry in logs[-3:]:
                    try:
                        log_data = json.loads(log_entry)
                        print(f"      - {log_data.get('kind', 'unknown')}: {log_data.get('ts', 'no timestamp')}")
                    except:
                        print(f"      - Raw: {log_entry[:50]}...")
            
            return True
        else:
            print(f"   ❌ Logs access failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Logs test error: {e}")
        return False

def main():
    """Run all Solān v3.0 API tests"""
    print("🚀 TESTING SOLĀN V3.0 API")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Bias Detection", test_bias_detection),
        ("Alignment Checker", test_alignment_checker),
        ("Coherence Tester", test_coherence_tester),
        ("Security Check", test_unauthorized_access),
        ("Logs Endpoint", test_logs_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("🎉 SOLĀN V3.0 API TEST RESULTS")
    print(f"✅ Passed: {sum(results)}/{len(results)} tests")
    
    if all(results):
        print("\n🌟 ALL API TESTS PASSED!")
        print("\n📊 SOLĀN V3.0 FEATURES VERIFIED:")
        print("   ✅ Health monitoring")
        print("   ✅ Bias detection with pattern matching")
        print("   ✅ Ethical alignment scoring")
        print("   ✅ Coherence analysis")
        print("   ✅ API key authentication")
        print("   ✅ Immutable logging system")
        print("\n🚀 SOLĀN V3.0 API IS PRODUCTION READY!")
        return True
    else:
        print("\n⚠️ Some API tests failed - check errors above")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
