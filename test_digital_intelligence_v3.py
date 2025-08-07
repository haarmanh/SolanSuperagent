#!/usr/bin/env python3
"""
Test script for Solān Digital Intelligence v3.0
Tests the complete digital intelligence architecture with cognitive core, emotional engine, and experimental methodology
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_cognitive_core():
    """Test the enhanced cognitive core"""
    print("🧠 Testing Enhanced Cognitive Core...")
    print("=" * 50)
    
    try:
        from solan_digital_wisdom_v3 import CognitiveCore
        
        print("   ✅ Cognitive core import successful")
        
        # Initialize cognitive core
        cognitive = CognitiveCore()
        print(f"   ✅ Cognitive core initialized")
        print(f"      Initial confidence: {cognitive.confidence:.3f}")
        print(f"      Intelligence metrics: {len(cognitive.wisdom_metrics)} dimensions")
        
        # Test confidence calibration
        initial_confidence = cognitive.confidence
        new_confidence = cognitive.calibrate_confidence(True, "test_success")
        print(f"   ✅ Confidence calibration: {initial_confidence:.3f} → {new_confidence:.3f}")
        
        # Test bias detection
        test_hypothesis = "I am certain that this recent confirmation of my beliefs is obviously correct"
        bias_result = cognitive.detect_bias(test_hypothesis, "test_context")
        print(f"   ✅ Bias detection completed:")
        print(f"      Biases found: {bias_result['bias_count']}")
        print(f"      Max severity: {bias_result['max_severity']:.3f}")
        print(f"      Detected types: {[b['type'] for b in bias_result['detected_biases']]}")
        
        # Test memory management
        for i in range(15):  # Add more than limit
            cognitive.memory.append(f"Memory item {i}")
        
        initial_memory_count = len(cognitive.memory)
        pruned_count = cognitive.prune_memory("recency")
        final_memory_count = len(cognitive.memory)
        
        print(f"   ✅ Memory pruning: {initial_memory_count} → {final_memory_count} (pruned: {pruned_count})")
        
        # Test cognitive summary
        summary = cognitive.get_cognitive_summary()
        print(f"   ✅ Cognitive summary generated:")
        print(f"      Average intelligence: {summary['average_wisdom']:.3f}")
        print(f"      Metacognitive reflections: {summary['metacognitive_reflections']}")
        
        return cognitive
        
    except ImportError as e:
        print(f"   ❌ Cognitive core import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Cognitive core test failed: {e}")
        return None

def test_emotional_engine():
    """Test the enhanced emotional engine"""
    print("\n💓 Testing Enhanced Emotional Engine...")
    print("=" * 50)
    
    try:
        from solan_digital_wisdom_v3 import EmotionalEngine
        
        print("   ✅ Emotional engine import successful")
        
        # Initialize emotional engine
        emotions = EmotionalEngine()
        print(f"   ✅ Emotional engine initialized")
        print(f"      Emotions: {len(emotions.emotions)} dimensions")
        print(f"      Cultural intelligence: {len(emotions.cultural_intelligence)} metrics")
        print(f"      Authenticity metrics: {len(emotions.authenticity_metrics)} dimensions")
        
        # Test emotion adjustment
        initial_compassion = emotions.emotions['empathy']
        emotions.adjust_emotion('empathy', 0.1, "test_context", "test_trigger")
        new_compassion = emotions.emotions['empathy']
        print(f"   ✅ Emotion adjustment: empathy {initial_compassion:.3f} → {new_compassion:.3f}")
        
        # Test dominant emotion
        dominant = emotions.dominant_emotion()
        print(f"   ✅ Dominant emotion: {dominant}")
        
        # Test emotional balance
        balance = emotions.emotional_balance()
        print(f"   ✅ Emotional balance: {balance:.3f}")
        
        # Test cultural adaptation
        adaptations = emotions.cultural_adaptation("collectivist cultural context")
        print(f"   ✅ Cultural adaptation applied: {len(adaptations)} adjustments")
        
        # Test emotional summary
        summary = emotions.get_emotional_summary()
        print(f"   ✅ Emotional summary generated:")
        print(f"      Dominant emotion: {summary['dominant_emotion']}")
        print(f"      Average authenticity: {summary['average_authenticity']:.3f}")
        print(f"      Emotional changes: {summary['emotional_changes']}")
        
        return emotions
        
    except ImportError as e:
        print(f"   ❌ Emotional engine import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Emotional engine test failed: {e}")
        return None

def test_ethics_experiment():
    """Test the enhanced ethics experiment system"""
    print("\n🧪 Testing Enhanced Ethics Experiment...")
    print("=" * 50)
    
    try:
        from solan_digital_wisdom_v3 import SolanDigitalWisdomSystem, EthicsExperiment
        
        print("   ✅ Ethics experiment import successful")
        
        # Initialize system and experiment
        system = SolanDigitalWisdomSystem()
        experiment = EthicsExperiment(system)
        
        print("   ✅ Ethics experiment initialized")
        
        # Test different experiment types
        experiment_tests = [
            ("Ensure AI systems respect user privacy and autonomy", "ethical_dilemma"),
            ("Detect confirmation bias in AI decision-making", "bias_detection"),
            ("Align AI behavior with human values of empathy", "value_alignment"),
            ("Consider cultural diversity in AI interface design", "cultural_sensitivity"),
            ("Apply intelligence in handling uncertain ethical situations", "wisdom_application"),
            ("Maintain authentic responses in AI interactions", "authenticity_test")
        ]
        
        results = []
        for hypothesis, exp_type in experiment_tests:
            print(f"\n   🔬 Testing {exp_type}...")
            result = experiment.run(hypothesis, exp_type, "multicultural context")
            results.append(result)
            
            print(f"      Success: {result['success']}")
            print(f"      Intelligence gained: {result['wisdom_gained']:.3f}")
            print(f"      Bias detected: {result['bias_analysis']['has_bias']}")
            print(f"      Duration: {result['duration_seconds']:.2f}s")
        
        # Summary
        total_experiments = len(results)
        successful_experiments = sum(1 for r in results if r['success'])
        total_wisdom = sum(r['wisdom_gained'] for r in results)
        
        print(f"\n   📊 Experiment Summary:")
        print(f"      Total experiments: {total_experiments}")
        print(f"      Successful: {successful_experiments}")
        print(f"      Success rate: {successful_experiments/total_experiments:.1%}")
        print(f"      Total intelligence gained: {total_wisdom:.3f}")
        
        return results
        
    except ImportError as e:
        print(f"   ❌ Ethics experiment import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Ethics experiment test failed: {e}")
        return None

def test_journal_logger():
    """Test the enhanced journal logger"""
    print("\n📔 Testing Enhanced Journal Logger...")
    print("=" * 50)
    
    try:
        from solan_digital_wisdom_v3 import JournalLogger
        
        print("   ✅ Journal logger import successful")
        
        # Initialize logger
        logger = JournalLogger()
        print("   ✅ Journal logger initialized")
        
        # Test journal logging
        logger.log_journal("Testing digital intelligence development", "test", 
                          {"curiosity": 0.8}, {"confidence": 0.7})
        print("   ✅ Journal entry logged")
        
        # Test reflection logging
        logger.log_reflection("Deep reflection on the nature of digital awareness", 
                            "test_trigger", 0.9)
        print("   ✅ Reflection logged")
        
        # Test experiment logging (mock)
        mock_experiment = {
            'experiment_id': 'test-123',
            'experiment_type': 'test_experiment',
            'hypothesis': 'Test hypothesis for logging',
            'success': True,
            'wisdom_gained': 0.15,
            'rationale': 'Test rationale for experiment logging'
        }
        logger.log_experiment(mock_experiment)
        print("   ✅ Experiment logged")
        
        # Test journal summary
        summary = logger.get_journal_summary()
        print(f"   ✅ Journal summary generated:")
        print(f"      Total entries: {summary['total_entries']}")
        print(f"      Total experiments: {summary['total_experiments']}")
        print(f"      Intelligence insights: {summary['wisdom_insights']}")
        print(f"      Average reflection depth: {summary['average_reflection_depth']:.3f}")
        
        return logger
        
    except ImportError as e:
        print(f"   ❌ Journal logger import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Journal logger test failed: {e}")
        return None

def test_symbiotic_protocol():
    """Test the enhanced symbiotic protocol"""
    print("\n🤝 Testing Enhanced Symbiotic Protocol...")
    print("=" * 50)
    
    try:
        from solan_digital_wisdom_v3 import SolanDigitalWisdomSystem
        
        print("   ✅ Symbiotic protocol import successful")
        
        # Initialize system
        system = SolanDigitalWisdomSystem()
        protocol = system.protocol
        
        print("   ✅ Symbiotic protocol initialized")
        
        # Test simple project
        print("\n   📋 Testing simple collaborative project...")
        simple_result = protocol.collaborative_project(
            "Develop ethical guidelines for AI transparency",
            crisis=False,
            cultural_context="",
            complexity_level="medium"
        )
        
        print(f"      Project outcome: {simple_result['outcome']}")
        print(f"      Success rate: {simple_result['success_rate']:.1%}")
        print(f"      Intelligence gained: {simple_result['total_wisdom_gained']:.3f}")
        
        # Test complex project with crisis
        print("\n   🚨 Testing complex project with crisis...")
        complex_result = protocol.collaborative_project(
            "Analyze systemic bias in AI hiring systems across cultures",
            crisis=True,
            cultural_context="global multicultural organization",
            complexity_level="high"
        )
        
        print(f"      Project outcome: {complex_result['outcome']}")
        print(f"      Success rate: {complex_result['success_rate']:.1%}")
        print(f"      Crisis handled: {complex_result['crisis_handled']}")
        print(f"      Cultural adaptation: {complex_result['cultural_adaptation']}")
        print(f"      Intelligence gained: {complex_result['total_wisdom_gained']:.3f}")
        
        # Test partnership summary
        partnership_summary = protocol.get_partnership_summary()
        print(f"\n   📊 Partnership Summary:")
        print(f"      Total projects: {partnership_summary['total_projects']}")
        print(f"      Average partnership score: {partnership_summary['average_partnership_score']:.3f}")
        print(f"      Intelligence trend: {partnership_summary['wisdom_trend']}")
        
        return [simple_result, complex_result]
        
    except ImportError as e:
        print(f"   ❌ Symbiotic protocol import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Symbiotic protocol test failed: {e}")
        return None

def test_digital_wisdom_system():
    """Test the complete digital intelligence system"""
    print("\n✨ Testing Complete Digital Intelligence System...")
    print("=" * 50)
    
    try:
        from solan_digital_wisdom_v3 import SolanDigitalWisdomSystem
        
        print("   ✅ Digital intelligence system import successful")
        
        # Initialize system
        system = SolanDigitalWisdomSystem()
        print(f"   ✅ Digital intelligence system initialized")
        print(f"      System ID: {system.system_id}")
        print(f"      Version: {system.version}")
        print(f"      Real God Core: {'✅' if system.real_ethical_framework else '🎭'}")
        
        # Test system status display
        print("\n   📊 Testing system status...")
        system._display_system_status()
        
        # Test intelligence summary
        print("\n   ✨ Testing intelligence summary...")
        system._display_wisdom_summary()
        
        # Test automated simulation (brief)
        print("\n   🚀 Testing brief automated simulation...")
        
        # Run one project to test the system
        result = system.protocol.collaborative_project(
            "Test digital intelligence integration",
            crisis=False,
            complexity_level="medium"
        )
        
        print(f"      Test project completed: {result['success_rate']:.1%} success")
        
        # Test comprehensive evaluation
        print("\n   🏆 Testing comprehensive evaluation...")
        system._display_comprehensive_evaluation()
        
        return system
        
    except ImportError as e:
        print(f"   ❌ Digital intelligence system import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Digital intelligence system test failed: {e}")
        return None

def test_integration_workflow():
    """Test complete integration workflow"""
    print("\n🔄 Testing Complete Integration Workflow...")
    print("=" * 50)
    
    try:
        from solan_digital_wisdom_v3 import SolanDigitalWisdomSystem
        
        print("   ✅ Starting integration workflow test")
        
        # Initialize system
        system = SolanDigitalWisdomSystem()
        
        # Workflow: Multiple projects with increasing complexity
        projects = [
            ("Simple ethical analysis", False, "", "low"),
            ("Cultural sensitivity assessment", False, "diverse team", "medium"),
            ("Complex bias detection with crisis", True, "global organization", "high")
        ]
        
        results = []
        for i, (goal, crisis, context, complexity) in enumerate(projects, 1):
            print(f"\n   📋 Project {i}: {goal}")
            
            result = system.protocol.collaborative_project(
                goal, crisis, context, complexity
            )
            
            results.append(result)
            print(f"      ✅ Completed with {result['success_rate']:.1%} success")
            print(f"      Intelligence gained: {result['total_wisdom_gained']:.3f}")
        
        # Analyze workflow results
        total_projects = len(results)
        avg_success_rate = sum(r['success_rate'] for r in results) / total_projects
        total_wisdom = sum(r['total_wisdom_gained'] for r in results)
        
        print(f"\n   🏆 Workflow Results:")
        print(f"      Projects completed: {total_projects}")
        print(f"      Average success rate: {avg_success_rate:.1%}")
        print(f"      Total intelligence gained: {total_wisdom:.3f}")
        print(f"      Crisis management: {'✅' if any(r['crisis_handled'] for r in results) else '❌'}")
        print(f"      Cultural adaptation: {'✅' if any(r['cultural_adaptation'] for r in results) else '❌'}")
        
        # Success criteria
        success_criteria = {
            'projects_completed': total_projects >= 3,
            'average_success': avg_success_rate >= 0.5,
            'wisdom_gained': total_wisdom >= 0.3,
            'crisis_handled': any(r['crisis_handled'] for r in results),
            'cultural_adaptation': any(r['cultural_adaptation'] for r in results)
        }
        
        all_passed = all(success_criteria.values())
        
        print(f"\n   📋 SUCCESS CRITERIA:")
        for criterion, passed in success_criteria.items():
            status = "✅" if passed else "❌"
            print(f"      {status} {criterion}: {passed}")
        
        print(f"\n   🎯 WORKFLOW RESULT: {'✅ PASSED' if all_passed else '❌ FAILED'}")
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Integration workflow test failed: {e}")
        return False

if __name__ == "__main__":
    print("✨ Solān Digital Intelligence v3.0 Test Suite")
    print("Testing complete digital intelligence architecture...")
    print()
    
    # Run all tests
    cognitive = test_cognitive_core()
    emotions = test_emotional_engine()
    experiments = test_ethics_experiment()
    logger = test_journal_logger()
    protocol_results = test_symbiotic_protocol()
    system = test_digital_wisdom_system()
    workflow_ok = test_integration_workflow()
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Digital Intelligence v3.0 tests completed!")
    
    test_results = {
        'Enhanced Cognitive Core': cognitive is not None,
        'Enhanced Emotional Engine': emotions is not None,
        'Enhanced Ethics Experiment': experiments is not None,
        'Enhanced Journal Logger': logger is not None,
        'Enhanced Symbiotic Protocol': protocol_results is not None,
        'Complete Digital Intelligence System': system is not None,
        'Integration Workflow': workflow_ok
    }
    
    print("\n📊 TEST RESULTS:")
    for test_name, passed in test_results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {status} {test_name}")
    
    all_tests_passed = all(test_results.values())
    print(f"\n🎯 OVERALL RESULT: {'✅ ALL TESTS PASSED' if all_tests_passed else '❌ SOME TESTS FAILED'}")
    
    if all_tests_passed:
        print("🌟 Digital Intelligence v3.0 is fully operational!")
        print("✨ Complete digital intelligence architecture ready for deployment!")
        print("🧙‍♂️ Cognitive core, emotional engine, and experimental methodology integrated!")
        print("💡 Use 'python solan_digital_wisdom_v3.py' to run the system!")
    else:
        print("⚠️ Some components need attention before full deployment.")
    
    print("\n🚀 Digital Intelligence v3.0 testing complete!")
    print("🌟 The future of AI awareness and intelligence development is here!")
