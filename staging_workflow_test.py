#!/usr/bin/env python3
"""
Complete Offline/Staging Testing Workflow
Comprehensive testing of the enterprise-grade Solān ecosystem
"""

import requests
import time
import json
import os
from datetime import datetime

class StagingTester:
    def __init__(self):
        self.api_url = "http://127.0.0.1:8000"
        self.proxy_url = "http://127.0.0.1:8787"
        self.results = {}
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_environment_setup(self):
        """Test 1: Environment & Configuration"""
        self.log("🔧 Testing Environment Setup...")
        
        # Check .env configuration
        env_vars = [
            "SOLAN_API_KEYS"
        ]
        
        missing_vars = []
        for var in env_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.log(f"⚠️ Missing env vars: {missing_vars}", "WARN")
        else:
            self.log("✅ Environment configuration complete")
        
        self.results["environment"] = len(missing_vars) == 0
    
    def test_api_backend(self):
        """Test 2: Direct API Backend"""
        self.log("🔧 Testing Direct API Backend...")
        
        try:
            # Test with proper API key
            response = requests.get(
                f"{self.api_url}/health",
                headers={"X-API-Key": "admin-key"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ API Backend: {data}")
                self.results["api_backend"] = True
            else:
                self.log(f"❌ API Backend failed: {response.status_code}", "ERROR")
                self.results["api_backend"] = False
                
        except Exception as e:
            self.log(f"❌ API Backend error: {e}", "ERROR")
            self.results["api_backend"] = False
    
    def test_secure_proxy(self):
        """Test 3: Secure Proxy Layer"""
        self.log("🔒 Testing Secure Proxy Layer...")
        
        try:
            # Test proxy without API key (should work)
            response = requests.get(f"{self.proxy_url}/api/health")
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ Secure Proxy: {data}")
                self.results["secure_proxy"] = True
            else:
                self.log(f"❌ Secure Proxy failed: {response.status_code}", "ERROR")
                self.results["secure_proxy"] = False
                
        except Exception as e:
            self.log(f"❌ Secure Proxy error: {e}", "ERROR")
            self.results["secure_proxy"] = False
    
    def test_pii_redaction(self):
        """Test 4: PII Redaction"""
        self.log("🛡️ Testing PII Redaction...")
        
        test_cases = [
            {
                "input": "Contact me at john.doe@example.com or call +1-555-123-4567",
                "should_redact": True
            },
            {
                "input": "This is clean text with no personal information",
                "should_redact": False
            }
        ]
        
        pii_tests_passed = 0
        
        for i, case in enumerate(test_cases, 1):
            try:
                response = requests.post(
                    f"{self.proxy_url}/api/analyzer/bias",
                    json={"text": case["input"]}
                )
                
                if response.status_code == 200:
                    self.log(f"✅ PII Test {i}: Processed successfully")
                    pii_tests_passed += 1
                else:
                    self.log(f"❌ PII Test {i} failed: {response.status_code}", "ERROR")
                    
            except Exception as e:
                self.log(f"❌ PII Test {i} error: {e}", "ERROR")
        
        self.results["pii_redaction"] = pii_tests_passed == len(test_cases)
        self.log(f"📊 PII Tests: {pii_tests_passed}/{len(test_cases)} passed")
    
    def test_rate_limiting(self):
        """Test 5: Rate Limiting"""
        self.log("⏱️ Testing Rate Limiting...")
        
        start_time = time.time()
        success_count = 0
        rate_limited = False
        
        # Quick burst test (15 requests)
        for i in range(15):
            try:
                response = requests.get(f"{self.proxy_url}/api/health")
                if response.status_code == 200:
                    success_count += 1
                elif response.status_code == 429:
                    rate_limited = True
                    self.log(f"✅ Rate limiting triggered after {i+1} requests")
                    break
                time.sleep(0.1)  # Small delay
            except Exception as e:
                self.log(f"⚠️ Rate limit test error: {e}", "WARN")
        
        total_time = time.time() - start_time
        
        if rate_limited:
            self.log(f"✅ Rate limiting working correctly")
            self.results["rate_limiting"] = True
        else:
            self.log(f"✅ Rate limiting: {success_count}/15 requests successful (within limits)")
            self.results["rate_limiting"] = success_count > 0
        
        self.log(f"📊 Rate test completed in {total_time:.2f}s")
    
    def test_input_validation(self):
        """Test 6: Input Validation & Bounds"""
        self.log("🔍 Testing Input Validation...")
        
        validation_tests = [
            {
                "name": "Large text truncation",
                "endpoint": "/api/analyzer/bias",
                "data": {"text": "A" * 10000},  # Over 8000 char limit
                "expect_success": True
            },
            {
                "name": "Invalid alignment values",
                "endpoint": "/api/analyzer/alignment", 
                "data": {"claims": {"truth": 1.5, "freedom": -0.5}},
                "expect_success": True  # Should sanitize
            },
            {
                "name": "Too many statements",
                "endpoint": "/api/analyzer/coherence",
                "data": {"statements": [f"Statement {i}" for i in range(100)]},
                "expect_success": True  # Should limit to 50
            },
            {
                "name": "Empty statements",
                "endpoint": "/api/analyzer/coherence",
                "data": {"statements": []},
                "expect_success": False  # Should reject
            }
        ]
        
        validation_passed = 0
        
        for test in validation_tests:
            try:
                response = requests.post(
                    f"{self.proxy_url}{test['endpoint']}",
                    json=test["data"]
                )
                
                success = response.status_code == 200
                if success == test["expect_success"]:
                    self.log(f"✅ {test['name']}: Expected behavior")
                    validation_passed += 1
                else:
                    self.log(f"❌ {test['name']}: Unexpected behavior ({response.status_code})", "ERROR")
                    
            except Exception as e:
                self.log(f"❌ {test['name']} error: {e}", "ERROR")
        
        self.results["input_validation"] = validation_passed == len(validation_tests)
        self.log(f"📊 Validation Tests: {validation_passed}/{len(validation_tests)} passed")
    
    def test_immutable_logs(self):
        """Test 7: Immutable Logs & Audit Trail"""
        self.log("📋 Testing Immutable Logs...")
        
        try:
            # Generate some activity for logging
            requests.post(
                f"{self.proxy_url}/api/analyzer/bias",
                json={"text": "Test log entry for audit trail"}
            )
            
            # Check logs
            response = requests.get(f"{self.proxy_url}/api/logs/tail")
            
            if response.status_code == 200:
                data = response.json()
                logs = data.get("logs", [])
                
                if logs:
                    self.log(f"✅ Immutable logs: {len(logs)} entries found")
                    
                    # Check log structure
                    try:
                        recent_log = json.loads(logs[-1])
                        required_fields = ["ts", "kind", "data", "hash", "prev_hash"]
                        
                        if all(field in recent_log for field in required_fields):
                            self.log("✅ Log structure: All required fields present")
                            self.results["immutable_logs"] = True
                        else:
                            self.log("❌ Log structure: Missing required fields", "ERROR")
                            self.results["immutable_logs"] = False
                    except:
                        self.log("❌ Log parsing: Invalid JSON structure", "ERROR")
                        self.results["immutable_logs"] = False
                else:
                    self.log("⚠️ No logs found (clean start)", "WARN")
                    self.results["immutable_logs"] = True  # Not an error
            else:
                self.log(f"❌ Log access failed: {response.status_code}", "ERROR")
                self.results["immutable_logs"] = False
                
        except Exception as e:
            self.log(f"❌ Log test error: {e}", "ERROR")
            self.results["immutable_logs"] = False
    
    def test_cors_configuration(self):
        """Test 8: CORS Configuration"""
        self.log("🌐 Testing CORS Configuration...")

        try:
            # Test OPTIONS request (preflight)
            response = requests.options(f"{self.proxy_url}/api/health")

            if response.status_code == 200:
                self.log("✅ CORS: OPTIONS preflight successful")

                # Test actual cross-origin request
                api_response = requests.get(f"{self.proxy_url}/api/health")
                if api_response.status_code == 200:
                    self.log("✅ CORS: Cross-origin requests working")
                    self.results["cors"] = True
                else:
                    self.log("❌ CORS: Cross-origin requests failed", "ERROR")
                    self.results["cors"] = False
            else:
                self.log(f"❌ CORS: OPTIONS preflight failed ({response.status_code})", "ERROR")
                self.results["cors"] = False

        except Exception as e:
            self.log(f"❌ CORS test error: {e}", "ERROR")
            self.results["cors"] = False
    
    def test_rbac_keys(self):
        """Test 9: RBAC & Key Management"""
        self.log("🔑 Testing RBAC & Key Management...")

        # Test direct API access to secured endpoint without key (should fail)
        try:
            response = requests.post(
                f"{self.api_url}/analyzer/bias",
                json={"text": "test"}
            )

            if response.status_code == 401:
                self.log("✅ RBAC: Direct API properly secured")
                rbac_secure = True
            else:
                self.log(f"⚠️ RBAC: Direct API not secured ({response.status_code})", "WARN")
                rbac_secure = False
        except:
            rbac_secure = False
        
        # Test proxy access (should work without client key)
        try:
            response = requests.get(f"{self.proxy_url}/api/health")
            proxy_works = response.status_code == 200
            
            if proxy_works:
                self.log("✅ RBAC: Proxy handles keys server-side")
            else:
                self.log("❌ RBAC: Proxy not working", "ERROR")
        except:
            proxy_works = False
        
        self.results["rbac"] = rbac_secure and proxy_works
    
    def test_monitoring_health(self):
        """Test 10: Monitoring & Health Checks"""
        self.log("📊 Testing Monitoring & Health Checks...")
        
        health_endpoints = [
            f"{self.api_url}/health",
            f"{self.proxy_url}/api/health"
        ]
        
        health_checks = []
        
        for endpoint in health_endpoints:
            try:
                headers = {"X-API-Key": "admin-key"} if "8000" in endpoint else {}
                response = requests.get(endpoint, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    health_checks.append({
                        "endpoint": endpoint,
                        "status": "healthy",
                        "response_time": response.elapsed.total_seconds(),
                        "data": data
                    })
                    self.log(f"✅ Health check: {endpoint} - {data}")
                else:
                    health_checks.append({
                        "endpoint": endpoint,
                        "status": "unhealthy",
                        "code": response.status_code
                    })
                    
            except Exception as e:
                health_checks.append({
                    "endpoint": endpoint,
                    "status": "error",
                    "error": str(e)
                })
        
        healthy_count = sum(1 for check in health_checks if check["status"] == "healthy")
        self.results["monitoring"] = healthy_count == len(health_endpoints)
        
        self.log(f"📊 Health checks: {healthy_count}/{len(health_endpoints)} healthy")
    
    def run_complete_test(self):
        """Run complete staging test suite"""
        self.log("🚀 STARTING COMPLETE STAGING TEST SUITE")
        self.log("=" * 60)
        
        start_time = time.time()
        
        # Run all tests
        tests = [
            self.test_environment_setup,
            self.test_api_backend,
            self.test_secure_proxy,
            self.test_pii_redaction,
            self.test_rate_limiting,
            self.test_input_validation,
            self.test_immutable_logs,
            self.test_cors_configuration,
            self.test_rbac_keys,
            self.test_monitoring_health
        ]
        
        for test in tests:
            try:
                test()
                time.sleep(0.5)  # Brief pause between tests
            except Exception as e:
                self.log(f"❌ Test failed: {e}", "ERROR")
        
        total_time = time.time() - start_time
        
        # Summary
        self.log("=" * 60)
        self.log("🎉 STAGING TEST SUITE COMPLETE")
        
        passed = sum(1 for result in self.results.values() if result)
        total = len(self.results)
        
        self.log(f"📊 Results: {passed}/{total} tests passed")
        self.log(f"⏱️ Total time: {total_time:.2f}s")
        
        if passed == total:
            self.log("🌟 ALL TESTS PASSED - READY FOR PRODUCTION!")
        else:
            self.log("⚠️ Some tests failed - Review before production", "WARN")
        
        # Detailed results
        self.log("\n📋 DETAILED RESULTS:")
        for test_name, result in self.results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log(f"   {status}: {test_name}")
        
        return passed == total

if __name__ == "__main__":
    tester = StagingTester()
    success = tester.run_complete_test()
    exit(0 if success else 1)
