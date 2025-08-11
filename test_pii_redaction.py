#!/usr/bin/env python3
"""
PII Redaction Test
"""
import requests
import json

def test_pii_redaction():
    url = "http://127.0.0.1:8787/api/analyzer/bias"
    
    # Test text with PII
    test_text = """
    Contact me at john.doe@example.com or call +31-6-12345678.
    My email is jane.smith@company.org and phone is 020-1234567.
    This text contains sensitive information that should be redacted.
    """
    
    print("🔍 Testing PII redaction...")
    print(f"📝 Input text contains:")
    print("   - john.doe@example.com")
    print("   - jane.smith@company.org") 
    print("   - +31-6-12345678")
    print("   - 020-1234567")
    
    try:
        response = requests.post(
            url,
            json={"text": test_text},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Response received")
            print(f"📄 Response content:")
            print(json.dumps(result, indent=2))
            
            # Check if original PII appears in response
            response_text = json.dumps(result)
            pii_found = []
            
            if "john.doe@example.com" in response_text:
                pii_found.append("john.doe@example.com")
            if "jane.smith@company.org" in response_text:
                pii_found.append("jane.smith@company.org")
            if "+31-6-12345678" in response_text:
                pii_found.append("+31-6-12345678")
            if "020-1234567" in response_text:
                pii_found.append("020-1234567")
            
            if pii_found:
                print(f"\n⚠️ PII LEAK DETECTED: {pii_found}")
                print("🔒 PII redaction: FAILED")
            else:
                print(f"\n🛡️ No original PII found in response")
                print("🔒 PII redaction: WORKING")
                
        else:
            print(f"❌ Request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_pii_redaction()
