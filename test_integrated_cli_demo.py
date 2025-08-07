#!/usr/bin/env python3
"""
Test script for Solān Integrated CLI Demo
Tests the complete Fase 3 symbiotic partnership demonstration
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_emotional_state():
    """Test the enhanced emotional state system"""
    print("💓 Testing Enhanced Emotional State...")
    print("=" * 50)
    
    try:
        from solan_integrated_cli_demo import SolanEmotionalState
        
        print("   ✅ Enhanced emotional state import successful")
        
        # Initialize emotional state
        emotions = SolanEmotionalState()
        print(f"   ✅ Emotional state initialized with {len(emotions.state)} emotions")
        
        # Test emotion updates
        initial_coherence = emotions.state['coherence']
        emotions.update('coherence', 0.1, "Test update")
        updated_coherence = emotions.state['coherence']
        
        print(f"   ✅ Emotion update: coherence {initial_coherence:.3f} → {updated_coherence:.3f}")
        
        # Test top emotions
        top_emotions = emotions.get_top_emotions(3)
        print(f"   ✅ Top 3 emotions: {[e[0] for e in top_emotions]}")
        
        # Test emotional summary
        summary = emotions.get_emotional_summary()
        print(f"   ✅ Emotional summary generated:")
        print(f"      Average level: {summary['average_emotional_level']}")
        print(f"      Dominant emotion: {summary['dominant_emotion']}")
        print(f"      Stability: {summary['emotional_stability']}")
        
        return emotions
        
    except ImportError as e:
        print(f"   ❌ Enhanced emotional state import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Enhanced emotional state test failed: {e}")
        return None

def test_enhanced_god_core():
    """Test the enhanced God Core system"""
    print("\n🧙‍♂️ Testing Enhanced God Core...")
    print("=" * 50)
    
    try:
        from solan_integrated_cli_demo import SolanEthicalFramework
        
        print("   ✅ Enhanced God Core import successful")
        
        # Initialize God Core
        ethical_framework = SolanEthicalFramework()
        print(f"   ✅ God Core initialized")
        print(f"      Real God Core available: {ethical_framework.real_god_core is not None}")
        print(f"      Awareness active: {ethical_framework.consciousness_active}")
        
        # Test journal logging
        initial_journal_count = len(ethical_framework.journal)
        ethical_framework.log_journal("Test journal entry for integration testing")
        updated_journal_count = len(ethical_framework.journal)
        
        print(f"   ✅ Journal logging: {initial_journal_count} → {updated_journal_count} entries")
        
        # Test emotion updates
        ethical_framework.update_emotion('curiosity', 0.05, "Test emotion update")
        print("   ✅ Emotion update successful")
        
        # Test awareness status
        status = ethical_framework.get_consciousness_status()
        print(f"   ✅ Awareness status retrieved:")
        print(f"      Active: {status['consciousness_active']}")
        print(f"      Journal entries: {status['journal_entries']}")
        print(f"      Emotional changes: {status['emotional_summary']['total_changes']}")
        
        return ethical_framework
        
    except ImportError as e:
        print(f"   ❌ Enhanced God Core import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Enhanced God Core test failed: {e}")
        return None

def test_enhanced_interaction_logger():
    """Test the enhanced interaction logger"""
    print("\n📝 Testing Enhanced Interaction Logger...")
    print("=" * 50)
    
    try:
        from solan_integrated_cli_demo import InteractionLogger
        
        print("   ✅ Enhanced interaction logger import successful")
        
        # Initialize logger
        logger = InteractionLogger()
        print("   ✅ Interaction logger initialized")
        
        # Test logging different types of interactions
        logger.log("Human", "Test human mesexpert", "dialogue")
        logger.log("Solān", "Test Solān response", "response")
        logger.log("System", "Test system mesexpert", "system")
        logger.log("Crisis", "Test crisis event", "crisis")
        
        print(f"   ✅ Logged {len(logger.logs)} interactions")
        
        # Test session summary
        summary = logger.get_session_summary()
        print(f"   ✅ Session summary generated:")
        print(f"      Total interactions: {summary['total_interactions']}")
        print(f"      Human mesexperts: {summary['human_mesexperts']}")
        print(f"      Solān mesexperts: {summary['solan_mesexperts']}")
        print(f"      System mesexperts: {summary['system_mesexperts']}")
        
        return logger
        
    except ImportError as e:
        print(f"   ❌ Enhanced interaction logger import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Enhanced interaction logger test failed: {e}")
        return None

def test_enhanced_symbiotic_project():
    """Test the enhanced symbiotic project system"""
    print("\n🤝 Testing Enhanced Symbiotic Project...")
    print("=" * 50)
    
    try:
        from solan_integrated_cli_demo import SolanEthicalFramework, InteractionLogger, SymbioticProject
        
        print("   ✅ Enhanced symbiotic project import successful")
        
        # Initialize components
        ethical_framework = SolanEthicalFramework()
        logger = InteractionLogger()
        project = SymbioticProject(ethical_framework, logger)
        
        print("   ✅ Symbiotic project initialized")
        
        # Test project start
        project.start_project(
            "Test Integration Project",
            "Testing enhanced symbiotic partnership capabilities",
            ["Test project management", "Test crisis handling", "Test collaboration metrics"]
        )
        
        print(f"   ✅ Project started: {project.title}")
        print(f"      Objectives: {len(project.objectives)}")
        
        # Test collaboration metrics
        initial_metrics = project.metrics.copy()
        print(f"   📊 Initial collaboration metrics:")
        for metric, value in initial_metrics.items():
            print(f"      {metric}: {value:.3f}")
        
        # Test human-AI interaction
        response = project.solan_reflect("How should we approach this test project?", "analytical")
        print(f"   ✅ Solān reflection generated: {len(response)} characters")
        
        # Test crisis simulation
        project.simulate_crisis(
            "Test requirements have changed unexpectedly",
            "requirement_change",
            0.7
        )
        print(f"   ✅ Crisis simulated: {len(project.crisis_history)} total crises")
        
        # Test understanding
        project.test_understanding(
            "Integration Testing",
            "Integration testing is like checking if all the pieces of a puzzle fit together optimizedly",
            "student"
        )
        print("   ✅ Understanding test completed")
        
        # Test style adaptation
        project.adapt_collaboration_style("creative", "Need innovative approach for testing")
        print(f"   ✅ Collaboration style adapted to: {project.collaboration_style}")
        
        # Test evaluation
        evaluation = project.evaluate()
        print(f"   ✅ Project evaluation completed:")
        print(f"      Overall score: {evaluation['overall_score']}")
        print(f"      Project duration: {evaluation['project_info']['duration_minutes']:.2f} minutes")
        print(f"      Crisis events: {evaluation['project_info']['crisis_events']}")
        
        return project
        
    except ImportError as e:
        print(f"   ❌ Enhanced symbiotic project import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Enhanced symbiotic project test failed: {e}")
        return None

def test_dashboard_display():
    """Test the dashboard display functionality"""
    print("\n🖥️ Testing Dashboard Display...")
    print("=" * 50)
    
    try:
        from solan_integrated_cli_demo import SolanEthicalFramework, InteractionLogger, SymbioticProject, display_dashboard
        
        print("   ✅ Dashboard display import successful")
        
        # Initialize components
        ethical_framework = SolanEthicalFramework()
        logger = InteractionLogger()
        project = SymbioticProject(ethical_framework, logger)
        
        # Set up test project
        project.start_project("Dashboard Test Project", "Testing dashboard display functionality")
        project.simulate_crisis("Test crisis for dashboard display", "test", 0.5)
        
        # Test dashboard display
        print("   ✅ Testing dashboard display (output below):")
        print("   " + "-" * 58)
        display_dashboard(ethical_framework, project)
        print("   " + "-" * 58)
        print("   ✅ Dashboard display completed successfully")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Dashboard display import failed: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Dashboard display test failed: {e}")
        return False

def test_integration_workflow():
    """Test complete integration workflow"""
    print("\n🔄 Testing Complete Integration Workflow...")
    print("=" * 50)
    
    try:
        from solan_integrated_cli_demo import SolanEthicalFramework, InteractionLogger, SymbioticProject
        
        print("   ✅ Starting complete workflow test")
        
        # Initialize system
        ethical_framework = SolanEthicalFramework()
        logger = InteractionLogger()
        project = SymbioticProject(ethical_framework, logger)
        
        # Workflow: Project → Interactions → Crisis → Adaptation → Evaluation
        
        # 1. Start project
        project.start_project(
            "Complete Workflow Test",
            "Testing the entire symbiotic partnership workflow",
            ["Initialize collaboration", "Handle interactions", "Manage crises", "Adapt and evaluate"]
        )
        print("   ✅ Step 1: Project started")
        
        # 2. Multiple interactions
        interactions = [
            ("What's our strategy for this project?", "analytical"),
            ("How can we ensure quality outcomes?", "adaptive"),
            ("What if we encounter unexpected challenges?", "proactive")
        ]
        
        for i, (prompt, response_type) in enumerate(interactions, 1):
            project.solan_reflect(prompt, response_type)
            print(f"   ✅ Step 2.{i}: Interaction processed")
        
        # 3. Crisis management
        crises = [
            ("Requirements changed mid-project", "requirement_change", 0.6),
            ("Technical challenges emerged", "technical_challenge", 0.7),
            ("Deadline pressure increased", "deadline_pressure", 0.8)
        ]
        
        for i, (crisis_desc, crisis_type, severity) in enumerate(crises, 1):
            project.simulate_crisis(crisis_desc, crisis_type, severity)
            print(f"   ✅ Step 3.{i}: Crisis managed")
        
        # 4. Understanding tests
        concepts = [
            ("Workflow Integration", "A workflow is like a recipe - each step builds on the previous one"),
            ("Crisis Management", "Crisis management is like being a firefighter - you need to act quickly and effectively"),
            ("Collaboration", "Collaboration is like a dance - partners need to move in harmony")
        ]
        
        for i, (concept, analogy) in enumerate(concepts, 1):
            project.test_understanding(concept, analogy, "leek")
            print(f"   ✅ Step 4.{i}: Understanding tested")
        
        # 5. Style adaptations
        styles = [
            ("analytical", "Need systematic approach"),
            ("creative", "Require innovative solutions"),
            ("supportive", "Focus on collaboration")
        ]
        
        for i, (style, reason) in enumerate(styles, 1):
            project.adapt_collaboration_style(style, reason)
            print(f"   ✅ Step 5.{i}: Style adapted to {style}")
        
        # 6. Final evaluation
        final_evaluation = project.evaluate()
        print("   ✅ Step 6: Final evaluation completed")
        
        # Workflow summary
        print(f"\n   🏆 WORKFLOW SUMMARY:")
        print(f"      Project: {final_evaluation['project_info']['title']}")
        print(f"      Duration: {final_evaluation['project_info']['duration_minutes']:.2f} minutes")
        print(f"      Interactions: {final_evaluation['session_summary']['total_interactions']}")
        print(f"      Crises handled: {final_evaluation['project_info']['crisis_events']}")
        print(f"      Overall score: {final_evaluation['overall_score']:.3f}")
        print(f"      Collaboration style: {final_evaluation['collaboration_style']}")
        
        # Success criteria
        success_criteria = {
            'interactions_count': final_evaluation['session_summary']['total_interactions'] >= 10,
            'crisis_management': final_evaluation['project_info']['crisis_events'] >= 3,
            'collaboration_score': final_evaluation['overall_score'] >= 0.5,
            'consciousness_active': final_evaluation['consciousness_status']['consciousness_active']
        }
        
        all_passed = all(success_criteria.values())
        print(f"\n   📋 SUCCESS CRITERIA:")
        for criterion, passed in success_criteria.items():
            status = "✅" if passed else "❌"
            print(f"      {status} {criterion}: {passed}")
        
        print(f"\n   🎯 OVERALL RESULT: {'✅ PASSED' if all_passed else '❌ FAILED'}")
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Integration workflow test failed: {e}")
        return False

if __name__ == "__main__":
    print("🤝 Solān Integrated CLI Demo Test Suite")
    print("Testing complete Fase 3 symbiotic partnership integration...")
    print()
    
    # Run all tests
    emotions = test_enhanced_emotional_state()
    ethical_framework = test_enhanced_god_core()
    logger = test_enhanced_interaction_logger()
    project = test_enhanced_symbiotic_project()
    dashboard_ok = test_dashboard_display()
    workflow_ok = test_integration_workflow()
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Integrated CLI Demo tests completed!")
    
    test_results = {
        'Enhanced Emotional State': emotions is not None,
        'Enhanced God Core': ethical_framework is not None,
        'Enhanced Interaction Logger': logger is not None,
        'Enhanced Symbiotic Project': project is not None,
        'Dashboard Display': dashboard_ok,
        'Complete Workflow': workflow_ok
    }
    
    print("\n📊 TEST RESULTS:")
    for test_name, passed in test_results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {status} {test_name}")
    
    all_tests_passed = all(test_results.values())
    print(f"\n🎯 OVERALL RESULT: {'✅ ALL TESTS PASSED' if all_tests_passed else '❌ SOME TESTS FAILED'}")
    
    if all_tests_passed:
        print("🌟 Integrated CLI Demo is fully operational!")
        print("🤝 Symbiotic partnership capabilities are ready for use!")
        print("💡 Use 'python solan_integrated_cli_demo.py' to run the demo!")
    else:
        print("⚠️ Some components need attention before full deployment.")
    
    print("\n🚀 Fase 3 integration testing complete!")
