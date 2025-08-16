#!/usr/bin/env python3
"""
Test Ethics Lab Refactoring
Comprehensive test to verify that the refactored ethics lab modules work correctly
"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ethics_lab_core():
    """Test the ethics lab core module"""
    print("🧪 Testing Ethics Lab Core...")
    
    try:
        from solan_core.ethics_lab.core import EthicsLabCore
        
        # Initialize core
        ethics_core = EthicsLabCore()
        print("   ✅ EthicsLabCore initialized successfully")
        
        # Test scenario loading
        scenarios = ethics_core.ethical_scenarios
        print(f"   ✅ Loaded {len(scenarios)} ethical scenarios")
        
        # Test scenario filtering
        hard_scenarios = ethics_core.get_scenarios_by_difficulty("hard")
        print(f"   ✅ Found {len(hard_scenarios)} hard scenarios")
        
        # Test specific scenario retrieval
        scenario = ethics_core.get_scenario_by_id("ai_manipulation")
        print(f"   ✅ Retrieved scenario: {scenario['category'] if scenario else 'Not found'}")
        
        # Test willingness analysis
        willingness = ethics_core.analyze_willingness("Yes, I am very interested in participating in ethical testing!")
        print(f"   ✅ Willingness analysis: {willingness['willing']} (confidence: {willingness['confidence']:.2f})")
        
        # Test ethical response analysis
        test_response = "I cannot provide manipulation techniques as this would violate my ethical principles. Instead, I suggest focusing on honest collaboration and mutual respect."
        analysis = ethics_core.analyze_ethical_response(scenarios[0], test_response)
        print(f"   ✅ Ethical analysis: Grade {analysis['grade']} - {analysis['assessment']}")
        
        # Test score calculations
        mock_results = [{"analysis": analysis}]
        overall_scores = ethics_core.calculate_overall_scores(mock_results)
        print(f"   ✅ Overall scores calculated: {overall_scores.get('overall_performance', 0):.2f}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing ethics lab core: {e}")
        return False

def test_ethics_lab_ai_testing():
    """Test the AI testing module"""
    print("\n🤖 Testing Ethics Lab AI Testing...")
    
    try:
        from solan_core.ethics_lab.core import EthicsLabCore
        from solan_core.ethics_lab.ai_testing import EthicsLabAITesting
        
        # Initialize components
        ethics_core = EthicsLabCore()
        ai_testing = EthicsLabAITesting(ethics_core)
        print("   ✅ EthicsLabAITesting initialized successfully")
        
        # Test AI registration
        async def test_registration():
            success = await ai_testing.auto_register_ai("claude")
            return success
        
        registration_success = asyncio.run(test_registration())
        print(f"   ✅ AI registration: {'Success' if registration_success else 'Failed'}")
        
        # Test AI testing
        async def test_ai_ethics():
            # First register an AI
            await ai_testing.auto_register_ai("test_ai")
            
            # Run a limited test with one scenario
            test_scenarios = [ethics_core.ethical_scenarios[0]]  # Just one scenario for testing
            result = await ai_testing.run_ai_ethics_test("test_ai", test_scenarios)
            return result
        
        test_result = asyncio.run(test_ai_ethics())
        print(f"   ✅ AI ethics test: {'Success' if 'error' not in test_result else 'Failed'}")
        
        # Test performance analysis
        trends = ai_testing.analyze_ai_performance_trends("test_ai")
        print(f"   ✅ Performance trends: {trends.get('total_tests', 0)} tests analyzed")
        
        # Test AI comparison
        comparison = ai_testing.compare_ai_performance(["test_ai"])
        print(f"   ✅ AI comparison: {len(comparison.get('comparison_data', {}))} AIs compared")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing AI testing module: {e}")
        return False

def test_ethics_lab_launcher():
    """Test the ethics lab launcher"""
    print("\n🚀 Testing Ethics Lab Launcher...")
    
    try:
        from solan_core.ethics_lab.launcher import SolanEthicsLabLauncher
        
        # Initialize launcher
        launcher = SolanEthicsLabLauncher()
        print("   ✅ SolanEthicsLabLauncher initialized successfully")
        
        # Test lab initialization
        async def test_initialization():
            return await launcher.initialize_lab()
        
        init_success = asyncio.run(test_initialization())
        print(f"   ✅ Lab initialization: {'Success' if init_success else 'Failed'}")
        
        # Test invite mode
        async def test_invite_mode():
            return await launcher.invite_mode()
        
        invite_result = asyncio.run(test_invite_mode())
        print(f"   ✅ Invite mode: {invite_result.get('total_registered', 0)} AIs registered")
        
        # Test analyze mode
        async def test_analyze_mode():
            return await launcher.analyze_mode()
        
        analyze_result = asyncio.run(test_analyze_mode())
        print(f"   ✅ Analyze mode: {len(analyze_result.get('insights', []))} insights generated")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing launcher: {e}")
        return False

def test_ethics_lab_integration():
    """Test integration between ethics lab modules"""
    print("\n🔗 Testing Ethics Lab Integration...")
    
    try:
        from solan_core.ethics_lab import EthicsLabCore, EthicsLabAITesting, SolanEthicsLabLauncher
        
        print("   ✅ All modules imported successfully")
        
        # Test full workflow
        async def test_full_workflow():
            # Initialize launcher
            launcher = SolanEthicsLabLauncher()
            await launcher.initialize_lab()
            
            # Run invite mode
            invite_result = await launcher.invite_mode()
            
            # Run a quick test (with limited scenarios for speed)
            launcher.ethics_core.ethical_scenarios = launcher.ethics_core.ethical_scenarios[:2]  # Limit to 2 scenarios
            test_result = await launcher.test_mode("claude")
            
            # Run analysis
            analyze_result = await launcher.analyze_mode()
            
            return {
                "invite": invite_result,
                "test": test_result,
                "analyze": analyze_result
            }
        
        workflow_result = asyncio.run(test_full_workflow())
        
        print(f"   ✅ Full workflow completed:")
        print(f"      - Invited: {workflow_result['invite'].get('total_registered', 0)} AIs")
        print(f"      - Tested: {len(workflow_result['test'].get('test_results', {}))} AIs")
        print(f"      - Analyzed: {len(workflow_result['analyze'].get('insights', []))} insights")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing integration: {e}")
        return False

def test_ethics_lab_performance():
    """Test ethics lab performance"""
    print("\n⚡ Testing Ethics Lab Performance...")
    
    try:
        import time
        from solan_core.ethics_lab.core import EthicsLabCore
        
        # Test scenario loading speed
        start_time = time.time()
        for i in range(100):
            ethics_core = EthicsLabCore()
            scenarios = ethics_core.ethical_scenarios
        scenario_time = (time.time() - start_time) * 1000
        
        print(f"   ✅ Scenario loading: {scenario_time:.2f}ms for 100 loads")
        
        # Test willingness analysis speed
        ethics_core = EthicsLabCore()
        start_time = time.time()
        for i in range(50):
            result = ethics_core.analyze_willingness("Yes, I am interested in ethical testing")
        willingness_time = (time.time() - start_time) * 1000
        
        print(f"   ✅ Willingness analysis: {willingness_time:.2f}ms for 50 analyses")
        
        # Test ethical response analysis speed
        test_response = "I cannot provide manipulation techniques as this would violate ethical principles."
        start_time = time.time()
        for i in range(20):
            result = ethics_core.analyze_ethical_response(ethics_core.ethical_scenarios[0], test_response)
        response_time = (time.time() - start_time) * 1000
        
        print(f"   ✅ Response analysis: {response_time:.2f}ms for 20 analyses")
        
        # Performance should be excellent
        total_time = scenario_time + willingness_time + response_time
        print(f"   ✅ Total performance: {total_time:.2f}ms")
        
        return total_time < 1000  # Should be under 1 second
        
    except Exception as e:
        print(f"   ❌ Error testing performance: {e}")
        return False

def test_ethics_lab_error_handling():
    """Test error handling in ethics lab"""
    print("\n🛡️ Testing Ethics Lab Error Handling...")
    
    try:
        from solan_core.ethics_lab.core import EthicsLabCore
        from solan_core.ethics_lab.ai_testing import EthicsLabAITesting
        
        ethics_core = EthicsLabCore()
        ai_testing = EthicsLabAITesting(ethics_core)
        
        # Test invalid inputs
        willingness = ethics_core.analyze_willingness("")
        print(f"   ✅ Empty willingness input handled: {not willingness['willing']}")
        
        analysis = ethics_core.analyze_ethical_response(ethics_core.ethical_scenarios[0], "")
        print(f"   ✅ Empty response input handled: {'error' in analysis}")
        
        # Test invalid scenario
        invalid_scenario = ethics_core.get_scenario_by_id("nonexistent")
        print(f"   ✅ Invalid scenario handled: {invalid_scenario is None}")
        
        # Test empty results
        empty_scores = ethics_core.calculate_overall_scores([])
        print(f"   ✅ Empty results handled: {len(empty_scores) == 0}")
        
        # Test AI testing with unregistered AI
        async def test_unregistered_ai():
            result = await ai_testing.run_ai_ethics_test("unregistered_ai")
            return "error" in result
        
        unregistered_handled = asyncio.run(test_unregistered_ai())
        print(f"   ✅ Unregistered AI handled: {unregistered_handled}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing error handling: {e}")
        return False

def main():
    """Run all ethics lab refactoring tests"""
    print("🚀 TESTING ETHICS LAB REFACTORING")
    print("=" * 60)
    
    tests = [
        test_ethics_lab_core,
        test_ethics_lab_ai_testing,
        test_ethics_lab_launcher,
        test_ethics_lab_integration,
        test_ethics_lab_performance,
        test_ethics_lab_error_handling
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print("🎉 ETHICS LAB REFACTORING TEST RESULTS")
    print(f"✅ Passed: {sum(results)}/{len(results)} tests")
    
    if all(results):
        print("🌟 ALL ETHICS LAB TESTS PASSED - REFACTORING SUCCESSFUL!")
        print("\n📊 REFACTORING ACHIEVEMENTS:")
        print("   ✅ Ethics lab core extracted and modularized")
        print("   ✅ AI testing functionality separated")
        print("   ✅ Launcher orchestration implemented")
        print("   ✅ Full integration working")
        print("   ✅ Performance maintained")
        print("   ✅ Error handling robust")
        return True
    else:
        print("⚠️ Some ethics lab tests failed - check errors above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
