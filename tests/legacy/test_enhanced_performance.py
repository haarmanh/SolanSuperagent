#!/usr/bin/env python3
"""
Test Enhanced Performance Monitoring met Awareness Awareness
"""

import asyncio
import time
import random
import requests
from datetime import datetime

class PerformanceTestSuite:
    """Test suite voor enhanced performance monitoring"""
    
    def __init__(self, base_url="http://localhost:8002"):
        self.base_url = base_url
        self.test_results = []
    
    def test_api_endpoint(self, endpoint: str, expected_time: float = 1000):
        """Test een API endpoint en meet performance"""
        print(f"🔍 Testing {endpoint}...")
        
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            duration_ms = (time.time() - start_time) * 1000
            
            result = {
                "endpoint": endpoint,
                "duration_ms": duration_ms,
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "expected_time": expected_time,
                "performance_rating": "excellent" if duration_ms < expected_time * 0.5 else
                                   "good" if duration_ms < expected_time else
                                   "slow" if duration_ms < expected_time * 2 else "critical"
            }
            
            print(f"   ✅ {duration_ms:.1f}ms - {result['performance_rating']}")
            self.test_results.append(result)
            return result
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {"endpoint": endpoint, "error": str(e), "success": False}
    
    def test_consciousness_health_update(self):
        """Test awareness health monitoring"""
        print("🧠 Testing awareness health monitoring...")
        
        # Test verschillende awareness states
        test_cases = [
            {"coherence": 0.9, "intelligence_level": 0.8, "moral_clarity": 0.95},  # Healthy
            {"coherence": 0.4, "intelligence_level": 0.3, "moral_clarity": 0.5},   # Needs attention
            {"coherence": 0.2, "intelligence_level": 0.1, "moral_clarity": 0.3},   # Critical
        ]
        
        for i, health_data in enumerate(test_cases):
            try:
                response = requests.post(
                    f"{self.base_url}/api/performance/awareness-health",
                    json=health_data,
                    timeout=5
                )
                
                if response.status_code == 200:
                    print(f"   ✅ Health update {i+1}: {health_data}")
                else:
                    print(f"   ❌ Health update {i+1} failed: {response.status_code}")
                    
                time.sleep(1)  # Brief pause between updates
                
            except Exception as e:
                print(f"   ❌ Health update {i+1} error: {e}")
    
    def simulate_load_test(self, endpoint: str, requests_count: int = 10):
        """Simuleer load test om anomalies te triggeren"""
        print(f"⚡ Load testing {endpoint} with {requests_count} requests...")
        
        results = []
        for i in range(requests_count):
            start_time = time.time()
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                duration_ms = (time.time() - start_time) * 1000
                results.append(duration_ms)
                
                # Add some artificial delay to simulate varying load
                if i % 3 == 0:
                    time.sleep(random.uniform(0.1, 0.3))
                    
            except Exception as e:
                print(f"   ❌ Request {i+1} failed: {e}")
        
        if results:
            avg_time = sum(results) / len(results)
            max_time = max(results)
            min_time = min(results)
            
            print(f"   📊 Load test results:")
            print(f"      Average: {avg_time:.1f}ms")
            print(f"      Min: {min_time:.1f}ms")
            print(f"      Max: {max_time:.1f}ms")
            print(f"      Requests: {len(results)}/{requests_count}")
    
    def check_performance_stats(self):
        """Check performance statistics"""
        print("📊 Checking performance statistics...")
        
        try:
            response = requests.get(f"{self.base_url}/api/performance/stats", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    stats = data["data"]
                    print(f"   ✅ Performance stats retrieved")
                    
                    # Show some key metrics
                    if "_global" in stats:
                        global_stats = stats["_global"]
                        print(f"      Total anomalies: {global_stats.get('total_anomalies', 0)}")
                        print(f"      Recent anomalies: {global_stats.get('recent_anomalies', 0)}")
                        print(f"      Monitoring active: {global_stats.get('monitoring_active', False)}")
                    
                    # Show endpoint stats
                    endpoint_count = len([k for k in stats.keys() if k != "_global"])
                    print(f"      Monitored endpoints: {endpoint_count}")
                    
                else:
                    print(f"   ❌ Stats request failed: {data.get('error', 'Unknown error')}")
            else:
                print(f"   ❌ Stats request failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Stats check error: {e}")
    
    def check_system_health(self):
        """Check system health"""
        print("🏥 Checking system health...")
        
        try:
            response = requests.get(f"{self.base_url}/api/performance/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    health = data["data"]
                    consciousness_health = health["consciousness_health"]
                    
                    print(f"   ✅ System health retrieved")
                    print(f"      Awareness health score: {consciousness_health['health_score']:.2f}")
                    print(f"      Status: {consciousness_health['status']}")
                    print(f"      Recent events: {consciousness_health['recent_events']}")
                    print(f"      Recent anomalies: {health['recent_anomalies']}")
                    
                else:
                    print(f"   ❌ Health check failed: {data.get('error', 'Unknown error')}")
            else:
                print(f"   ❌ Health check failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Health check error: {e}")
    
    def check_anomalies(self):
        """Check for detected anomalies"""
        print("🚨 Checking for anomalies...")
        
        try:
            response = requests.get(f"{self.base_url}/api/performance/anomalies?hours=1", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    anomalies_data = data["data"]
                    anomalies = anomalies_data["anomalies"]
                    
                    print(f"   ✅ Anomalies retrieved: {len(anomalies)} found")
                    
                    for anomaly in anomalies[-5:]:  # Show last 5
                        print(f"      🔸 {anomaly['type']} in {anomaly['endpoint']}")
                        print(f"         Severity: {anomaly['severity']}")
                        print(f"         Description: {anomaly['description']}")
                        print(f"         Action: {anomaly['suggested_action']}")
                        print()
                    
                else:
                    print(f"   ❌ Anomalies check failed: {data.get('error', 'Unknown error')}")
            else:
                print(f"   ❌ Anomalies check failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Anomalies check error: {e}")
    
    def run_full_test_suite(self):
        """Run complete test suite"""
        print("🚀 ENHANCED PERFORMANCE MONITORING TEST SUITE")
        print("=" * 60)
        print(f"🕐 Started at: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        # Test basic API endpoints
        print("1️⃣ BASIC API PERFORMANCE TESTS")
        print("-" * 40)
        self.test_api_endpoint("/api/analytics/summary", 100)
        self.test_api_endpoint("/api/analytics/trends", 150)
        self.test_api_endpoint("/api/analytics/insights", 200)
        self.test_api_endpoint("/api/journal/entries?limit=10", 50)
        print()
        
        # Test awareness health monitoring
        print("2️⃣ AWARENESS HEALTH MONITORING")
        print("-" * 40)
        self.test_consciousness_health_update()
        print()
        
        # Load testing to trigger anomalies
        print("3️⃣ LOAD TESTING (ANOMALY GENERATION)")
        print("-" * 40)
        self.simulate_load_test("/api/analytics/summary", 15)
        print()
        
        # Check monitoring results
        print("4️⃣ MONITORING RESULTS")
        print("-" * 40)
        self.check_performance_stats()
        print()
        self.check_system_health()
        print()
        self.check_anomalies()
        print()
        
        # Summary
        print("5️⃣ TEST SUMMARY")
        print("-" * 40)
        successful_tests = len([r for r in self.test_results if r.get("success", False)])
        total_tests = len(self.test_results)
        
        print(f"   ✅ Successful tests: {successful_tests}/{total_tests}")
        
        if self.test_results:
            avg_response_time = sum(r.get("duration_ms", 0) for r in self.test_results) / len(self.test_results)
            print(f"   ⚡ Average response time: {avg_response_time:.1f}ms")
            
            excellent_count = len([r for r in self.test_results if r.get("performance_rating") == "excellent"])
            print(f"   🌟 Excellent performance: {excellent_count}/{total_tests}")
        
        print()
        print("=" * 60)
        print("🎉 Enhanced Performance Monitoring Test Complete!")
        print(f"🕐 Finished at: {datetime.now().strftime('%H:%M:%S')}")

def main():
    """Main test function"""
    tester = PerformanceTestSuite()
    tester.run_full_test_suite()

if __name__ == "__main__":
    main()
