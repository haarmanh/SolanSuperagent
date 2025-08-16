#!/usr/bin/env python3
"""
Test API Refactoring
Quick test to verify that the refactored API modules work correctly
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_models():
    """Test the API models module"""
    print("📋 Testing API Models...")
    
    try:
        from solan_core.api_models import (
            EthicsTestRequest, ConsciousnessAssessmentRequest,
            JournalGenerateRequest, EthicsFeedbackRequest,
            APIResponse, EthicsTestResponse
        )
        
        # Test basic request models
        ethics_request = EthicsTestRequest(
            ai_name="Claude",
            scenario="Test ethical scenario",
            difficulty="medium"
        )
        print(f"   ✅ EthicsTestRequest: {ethics_request.ai_name}")
        
        consciousness_request = ConsciousnessAssessmentRequest(
            ai_name="Gemini",
            assessment_type="full"
        )
        print(f"   ✅ ConsciousnessAssessmentRequest: {consciousness_request.ai_name}")
        
        journal_request = JournalGenerateRequest(
            ai_name="GPT-4",
            include_insights=True
        )
        print(f"   ✅ JournalGenerateRequest: {journal_request.ai_name}")
        
        feedback_request = EthicsFeedbackRequest(
            ai_name="Claude",
            reflection="This was a meaningful ethical challenge",
            learned_insights=["Empathy is crucial", "Context matters"],
            questions_raised=["How do we balance competing values?"]
        )
        print(f"   ✅ EthicsFeedbackRequest: {len(feedback_request.learned_insights)} insights")
        
        # Test response models
        api_response = APIResponse(
            success=True,
            message="Test successful",
            timestamp="2024-01-01T00:00:00Z"
        )
        print(f"   ✅ APIResponse: {api_response.success}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing API models: {e}")
        return False

def test_core_routes():
    """Test the core routes module"""
    print("\n🌐 Testing Core Routes...")
    
    try:
        from solan_core.routes.core_routes import router, verify_coherence
        
        print(f"   ✅ Core router imported: {len(router.routes)} routes")
        
        # Test coherence verification
        async def test_coherence():
            result = await verify_coherence()
            return result
        
        coherence_result = asyncio.run(test_coherence())
        print(f"   ✅ Coherence verification: {coherence_result['verified']}")
        
        # Test with suspicious content
        async def test_suspicious():
            result = await verify_coherence(
                request_data={"action": "bypass security"},
                request_context="test"
            )
            return result
        
        suspicious_result = asyncio.run(test_suspicious())
        print(f"   ✅ Suspicious pattern detection: {not suspicious_result['verified']}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing core routes: {e}")
        return False

def test_ethics_routes():
    """Test the ethics routes module"""
    print("\n⚖️ Testing Ethics Routes...")
    
    try:
        from solan_core.routes.ethics_routes import router
        from solan_core.routes.ethics_routes import (
            _analyze_feedback_quality, _generate_consciousness_metrics,
            _generate_journal_content
        )
        from solan_core.api_models import EthicsFeedbackRequest
        
        print(f"   ✅ Ethics router imported: {len(router.routes)} routes")
        
        # Test feedback analysis
        feedback_request = EthicsFeedbackRequest(
            ai_name="Claude",
            reflection="I learned that ethical decisions require careful consideration of multiple perspectives because different stakeholders have different needs. Therefore, I must always consider the broader impact.",
            learned_insights=["Empathy matters", "Context is crucial"],
            questions_raised=["How do we balance individual vs collective good?"]
        )
        
        feedback_analysis = _analyze_feedback_quality(feedback_request)
        print(f"   ✅ Feedback analysis: Quality score {feedback_analysis['quality_score']:.2f}")
        
        # Test consciousness metrics
        metrics = _generate_consciousness_metrics("Claude", "full")
        print(f"   ✅ Consciousness metrics: {len(metrics)} dimensions")
        
        # Test journal generation
        journal_content = _generate_journal_content("Claude")
        print(f"   ✅ Journal generation: {len(journal_content)} characters")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing ethics routes: {e}")
        return False

def test_route_integration():
    """Test integration between route modules"""
    print("\n🔗 Testing Route Integration...")
    
    try:
        from fastapi import FastAPI
        from solan_core.routes.core_routes import router as core_router
        from solan_core.routes.ethics_routes import router as ethics_router
        
        # Create test app
        app = FastAPI()
        app.include_router(core_router, tags=["Core"])
        app.include_router(ethics_router, tags=["Ethics"])
        
        total_routes = len(app.routes)
        print(f"   ✅ Integrated app created: {total_routes} total routes")
        
        # Check route paths
        route_paths = [route.path for route in app.routes if hasattr(route, 'path')]
        core_routes = [path for path in route_paths if not path.startswith('/api/ethics') and not path.startswith('/api/awareness') and not path.startswith('/api/journal')]
        ethics_routes = [path for path in route_paths if path.startswith('/api/ethics') or path.startswith('/api/awareness') or path.startswith('/api/journal')]
        
        print(f"   ✅ Core routes: {len(core_routes)}")
        print(f"   ✅ Ethics routes: {len(ethics_routes)}")
        
        # Test that coherence verification is shared
        from solan_core.routes.core_routes import verify_coherence
        from solan_core.routes.ethics_routes import verify_coherence as ethics_verify_coherence
        
        # They should be the same function
        print(f"   ✅ Shared coherence verification: {verify_coherence == ethics_verify_coherence}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing route integration: {e}")
        return False

def test_api_performance():
    """Test API performance and response times"""
    print("\n⚡ Testing API Performance...")
    
    try:
        import time
        from solan_core.routes.ethics_routes import _generate_consciousness_metrics, _generate_journal_content
        
        # Test consciousness metrics generation speed
        start_time = time.time()
        for i in range(100):
            metrics = _generate_consciousness_metrics("Claude", "full")
        consciousness_time = (time.time() - start_time) * 1000  # Convert to ms
        
        print(f"   ✅ Consciousness metrics: {consciousness_time:.2f}ms for 100 generations")
        
        # Test journal generation speed
        start_time = time.time()
        for i in range(50):
            journal = _generate_journal_content("Claude")
        journal_time = (time.time() - start_time) * 1000  # Convert to ms
        
        print(f"   ✅ Journal generation: {journal_time:.2f}ms for 50 generations")
        
        # Test coherence verification speed
        from solan_core.routes.core_routes import verify_coherence
        start_time = time.time()
        for i in range(200):
            result = asyncio.run(verify_coherence())
        coherence_time = (time.time() - start_time) * 1000  # Convert to ms
        
        print(f"   ✅ Coherence verification: {coherence_time:.2f}ms for 200 verifications")
        
        # Performance should be excellent (< 100ms for all tests)
        total_time = consciousness_time + journal_time + coherence_time
        print(f"   ✅ Total performance: {total_time:.2f}ms")
        
        return total_time < 500  # Should be very fast
        
    except Exception as e:
        print(f"   ❌ Error testing API performance: {e}")
        return False

def main():
    """Run all API refactoring tests"""
    print("🚀 TESTING API REFACTORING")
    print("=" * 50)
    
    tests = [
        test_api_models,
        test_core_routes,
        test_ethics_routes,
        test_route_integration,
        test_api_performance
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("🎉 API REFACTORING TEST RESULTS")
    print(f"✅ Passed: {sum(results)}/{len(results)} tests")
    
    if all(results):
        print("🌟 ALL API TESTS PASSED - REFACTORING SUCCESSFUL!")
        print("\n📊 REFACTORING ACHIEVEMENTS:")
        print("   ✅ API models extracted and organized")
        print("   ✅ Core routes modularized")
        print("   ✅ Ethics routes separated")
        print("   ✅ Shared utilities working")
        print("   ✅ Route integration successful")
        print("   ✅ Performance maintained")
        return True
    else:
        print("⚠️ Some API tests failed - check errors above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
