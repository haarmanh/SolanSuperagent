#!/usr/bin/env python3
"""
Test Refactored Modules
Quick test to verify that the refactored modules work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_cognitive_core():
    """Test the refactored cognitive core module"""
    print("🧠 Testing Cognitive Core Module...")
    
    try:
        from solan_core.cognitive_core import CognitiveCore
        
        # Initialize cognitive core
        cognitive = CognitiveCore()
        print("   ✅ CognitiveCore initialized successfully")
        
        # Test bias detection
        test_hypothesis = "I am absolutely certain that this is the best solution"
        bias_result = cognitive.detect_bias(test_hypothesis)
        print(f"   ✅ Bias detection works: {bias_result['bias_count']} biases detected")
        
        # Test confidence calibration
        old_confidence = cognitive.confidence
        new_confidence = cognitive.calibrate_confidence(True, "test")
        print(f"   ✅ Confidence calibration: {old_confidence:.3f} → {new_confidence:.3f}")
        
        # Test metacognitive thinking
        metacognitive_result = cognitive.think_metacognitively("I should consider multiple perspectives")
        print(f"   ✅ Metacognitive thinking: {len(metacognitive_result['recommendations'])} recommendations")
        
        # Test cognitive state
        state = cognitive.get_cognitive_state()
        print(f"   ✅ Cognitive state: Wisdom score {state['wisdom_score']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing cognitive core: {e}")
        return False

def test_protocol_manager():
    """Test the refactored protocol manager module"""
    print("\n🔬 Testing Protocol Manager Module...")
    
    try:
        from solan_core.cognitive_core import CognitiveCore
        from solan_core.protocol_manager import ProtocolManager
        
        # Initialize components
        cognitive = CognitiveCore()
        
        # Mock emotional engine for testing
        class MockEmotionalEngine:
            def __init__(self):
                self.emotions = {'curiosity': 0.5, 'satisfaction': 0.6}
            
            def adjust_emotion(self, emotion, delta, context, trigger):
                if emotion in self.emotions:
                    self.emotions[emotion] = max(0.0, min(1.0, self.emotions[emotion] + delta))
            
            def cultural_adaptation(self, context):
                return {'empathy': 0.1}
        
        emotional = MockEmotionalEngine()
        protocol_manager = ProtocolManager(cognitive, emotional)
        print("   ✅ ProtocolManager initialized successfully")
        
        # Test experiment execution
        experiment_result = protocol_manager.run_experiment(
            "Should we prioritize individual rights or collective benefit?",
            "ethical_dilemma"
        )
        print(f"   ✅ Experiment execution: Success = {experiment_result['success']}")
        
        # Test protocol status
        status = protocol_manager.get_protocol_status()
        print(f"   ✅ Protocol status: {status['experiments_run']} experiments run")
        
        # Test trend analysis
        trends = protocol_manager.analyze_experiment_trends()
        print(f"   ✅ Trend analysis: {trends.get('total_experiments', 0)} total experiments")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing protocol manager: {e}")
        return False

def test_utils_module():
    """Test the utility module"""
    print("\n🛠️ Testing Utils Module...")
    
    try:
        from solan_core.utils import (
            BiasDetectionUtils, ConfidenceUtils, SystemUtils, 
            PerformanceUtils, ValidationUtils, RandomUtils
        )
        
        # Test bias detection utils
        bias_utils = BiasDetectionUtils()
        patterns = bias_utils.get_bias_patterns()
        detected = bias_utils.detect_bias_in_text("I am certain this is correct", patterns)
        print(f"   ✅ BiasDetectionUtils: {len(detected)} biases detected")
        
        # Test confidence utils
        confidence_utils = ConfidenceUtils()
        new_conf = confidence_utils.calibrate_confidence(0.7, True)
        print(f"   ✅ ConfidenceUtils: Confidence calibrated to {new_conf:.3f}")
        
        # Test system utils
        system_utils = SystemUtils()
        system_id = system_utils.generate_system_id()
        timestamp = system_utils.get_timestamp()
        print(f"   ✅ SystemUtils: Generated ID and timestamp")
        
        # Test validation utils
        validation_utils = ValidationUtils()
        score = validation_utils.validate_score("0.85")
        text = validation_utils.validate_text_input("Test input")
        print(f"   ✅ ValidationUtils: Score {score}, Text '{text}'")
        
        # Test performance utils
        performance_utils = PerformanceUtils()
        metrics = performance_utils.generate_performance_metrics([10, 20, 30, 40])
        print(f"   ✅ PerformanceUtils: Avg {metrics['avg']:.1f}ms")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing utils: {e}")
        return False

def test_integration():
    """Test integration between modules"""
    print("\n🔗 Testing Module Integration...")
    
    try:
        from solan_core.cognitive_core import CognitiveCore
        from solan_core.protocol_manager import ProtocolManager
        
        # Initialize integrated system
        cognitive = CognitiveCore()
        
        class MockEmotionalEngine:
            def __init__(self):
                self.emotions = {'curiosity': 0.5, 'satisfaction': 0.6}
            def adjust_emotion(self, emotion, delta, context, trigger):
                pass
            def cultural_adaptation(self, context):
                return {}
        
        emotional = MockEmotionalEngine()
        protocol = ProtocolManager(cognitive, emotional)
        
        # Run integrated test
        result = protocol.run_experiment(
            "How can we ensure AI systems are both efficient and ethical?",
            "value_alignment",
            "multicultural"
        )
        
        print(f"   ✅ Integration test successful:")
        print(f"      Experiment ID: {result['experiment_id'][:8]}...")
        print(f"      Success: {result['success']}")
        print(f"      Biases detected: {result['bias_analysis']['bias_count']}")
        print(f"      Duration: {result['duration_seconds']:.3f}s")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error in integration test: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 TESTING REFACTORED MODULES")
    print("=" * 50)
    
    tests = [
        test_utils_module,
        test_cognitive_core,
        test_protocol_manager,
        test_integration
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("🎉 TEST RESULTS SUMMARY")
    print(f"✅ Passed: {sum(results)}/{len(results)} tests")
    
    if all(results):
        print("🌟 ALL TESTS PASSED - REFACTORING SUCCESSFUL!")
        return True
    else:
        print("⚠️ Some tests failed - check errors above")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
