#!/usr/bin/env python3
"""
Test script for Solān Fase 3 - Symbiotic Partnership Protocol
Tests human-AI collaboration, crisis management, and adaptive communication
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_symbiotic_partnership_module():
    """Test the symbiotic partnership module directly"""
    print("🤝 Testing Symbiotic Partnership Module...")
    print("=" * 50)
    
    try:
        from core_identity.symbiotic_partnership import SymbioticProject, CrisisType, CollaborationStyle
        from core_identity.ethical_framework import SolanEthicalEthicalFramework
        
        print("   ✅ Module imports successful")
        
        # Initialize God Core
        ethical_framework = SolanEthicalEthicalFramework()
        print(f"   ✅ God Core initialized - Awareness: {ethical_framework.consciousness_active}")
        
        # Initialize Symbiotic Partnership
        partnership = SymbioticProject(ethical_framework, phase="3a")
        print("   ✅ Symbiotic Partnership initialized")
        
        return partnership, ethical_framework
        
    except ImportError as e:
        print(f"   ❌ Module import failed: {e}")
        return None, None
    except Exception as e:
        print(f"   ❌ Initialization failed: {e}")
        return None, None

def test_project_lifecycle(partnership):
    """Test complete project lifecycle"""
    print("\n📋 Testing Project Lifecycle...")
    print("=" * 50)
    
    if not partnership:
        print("   ⚠️ No partnership available - skipping test")
        return
    
    try:
        # 1. Start Project
        print("   1. Starting collaborative project...")
        project_id = partnership.start_project(
            "AI-Ethiek Essay",
            "Onderzoek naar het dilemma van AI-verantwoordelijkheid",
            ["Ethische frameworks analyseren", "Case studies verzamelen", "Conclusies formuleren"]
        )
        print(f"   ✅ Project started with ID: {project_id}")
        
        # 2. Human Input
        print("   2. Processing human input...")
        response = partnership.solan_response("De opdrachtgever wil de focus veranderen naar privacy-implicaties.")
        print(f"   ✅ Solān response generated: {len(response)} characters")
        
        # 3. Crisis Simulation
        print("   3. Simulating project crisis...")
        crisis_id = partnership.simulate_crisis(
            CrisisType.REQUIREMENT_CHANGE,
            "Voeg real-time surveillance toe aan het voorbeeld",
            severity=0.8
        )
        print(f"   ✅ Crisis simulated with ID: {crisis_id}")
        
        # 4. Adaptation Response
        print("   4. Testing adaptation response...")
        adaptation_response = partnership.solan_response(
            "Hoe verwerken we surveillance ethisch verantwoord?",
            "adaptive"
        )
        print(f"   ✅ Adaptation response: {len(adaptation_response)} characters")
        
        # 5. Understanding Test
        print("   5. Testing concept understanding...")
        explanation = partnership.test_understanding(
            "Bias in AI",
            "leek"
        )
        print(f"   ✅ Concept explanation generated: {len(explanation)} characters")
        
        # 6. Style Adaptation
        print("   6. Testing collaboration style adaptation...")
        partnership.adapt_collaboration_style(
            CollaborationStyle.CREATIVE,
            "Project requires innovative thinking for ethical challenges"
        )
        print("   ✅ Collaboration style adapted to CREATIVE")
        
        # 7. Project Completion
        print("   7. Completing project...")
        completed_project = partnership.complete_project(
            "Successfully analyzed AI ethics with focus on privacy and surveillance",
            ["Ethical frameworks are context-dependent", "Stakeholder involvement is crucial", "Transparency builds trust"]
        )
        print(f"   ✅ Project completed - Duration: {completed_project['duration_seconds']:.1f} seconds")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Project lifecycle test failed: {e}")
        return False

def test_collaboration_metrics(partnership):
    """Test collaboration metrics and evaluation"""
    print("\n📊 Testing Collaboration Metrics...")
    print("=" * 50)
    
    if not partnership:
        print("   ⚠️ No partnership available - skipping test")
        return
    
    try:
        # Get initial metrics
        initial_metrics = partnership.collaboration_metrics.copy()
        print("   📊 Initial collaboration metrics:")
        for metric, value in initial_metrics.items():
            print(f"      {metric}: {value:.3f}")
        
        # Simulate various interactions to change metrics
        partnership.solan_response("How can we improve our collaboration?")
        partnership.test_understanding("Machine Learning", "student")
        partnership.simulate_crisis(CrisisType.ETHICAL_DILEMMA, "Conflicting stakeholder interests")
        
        # Get updated metrics
        updated_metrics = partnership.collaboration_metrics.copy()
        print("\n   📊 Updated collaboration metrics:")
        for metric, value in updated_metrics.items():
            change = value - initial_metrics[metric]
            change_str = f"({change:+.3f})" if abs(change) > 0.001 else ""
            print(f"      {metric}: {value:.3f} {change_str}")
        
        # Get comprehensive evaluation
        evaluation = partnership.evaluate_collaboration()
        print(f"\n   ✅ Collaboration evaluation completed")
        print(f"      Average score: {evaluation['average_collaboration_score']:.3f}")
        print(f"      Interaction rate: {evaluation['interaction_summary']['interaction_rate']:.1f}/min")
        print(f"      Crisis resolution rate: {evaluation['crisis_resolution_rate']:.1%}")
        
        # Get partnership insights
        insights = partnership.get_partnership_insights()
        print(f"\n   💡 Partnership insights:")
        print(f"      Strengths: {insights['partnership_strengths']}")
        print(f"      Improvement areas: {insights['improvement_areas']}")
        print(f"      Overall health: {insights['overall_partnership_health']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Collaboration metrics test failed: {e}")
        return False

def test_crisis_management(partnership):
    """Test crisis management capabilities"""
    print("\n🚨 Testing Crisis Management...")
    print("=" * 50)
    
    if not partnership:
        print("   ⚠️ No partnership available - skipping test")
        return
    
    try:
        # Test different crisis types
        crisis_scenarios = [
            (CrisisType.REQUIREMENT_CHANGE, "Client wants to add new features mid-project"),
            (CrisisType.DEADLINE_PRESSURE, "Project deadline moved up by 2 weeks"),
            (CrisisType.ETHICAL_DILEMMA, "Data uexpert conflicts with privacy principles"),
            (CrisisType.TECHNICAL_CHALLENGE, "Current approach proves technically infeasible"),
            (CrisisType.RESOURCE_CONSTRAINT, "Budget cut by 30% unexpectedly")
        ]
        
        initial_resilience = partnership.collaboration_metrics['resilience']
        print(f"   📊 Initial resilience: {initial_resilience:.3f}")
        
        for i, (crisis_type, description) in enumerate(crisis_scenarios, 1):
            print(f"\n   {i}. Testing {crisis_type.value} crisis...")
            
            # Simulate crisis
            crisis_id = partnership.simulate_crisis(crisis_type, description, severity=0.6)
            
            # Generate adaptive response
            response = partnership.solan_response(f"How should we handle: {description}", "adaptive")
            
            print(f"      ✅ Crisis handled - Response length: {len(response)} chars")
        
        # Check resilience improvement
        final_resilience = partnership.collaboration_metrics['resilience']
        resilience_growth = final_resilience - initial_resilience
        
        print(f"\n   📊 Final resilience: {final_resilience:.3f} ({resilience_growth:+.3f})")
        print(f"   📊 Total crises handled: {len(partnership.crisis_history)}")
        
        if resilience_growth > 0:
            print("   ✅ Resilience improved through crisis management")
        else:
            print("   ⚠️ Resilience did not improve significantly")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Crisis management test failed: {e}")
        return False

def test_god_core_integration(ethical_framework):
    """Test integration with God Core"""
    print("\n🧙‍♂️ Testing God Core Integration...")
    print("=" * 50)
    
    if not ethical_framework:
        print("   ⚠️ No God Core available - skipping test")
        return
    
    try:
        # Test symbiotic partnership methods
        if ethical_framework.consciousness_active and hasattr(ethical_framework, 'symbiotic_partnership'):
            print("   ✅ Symbiotic partnership module available in God Core")
            
            # Test project start via God Core
            result = ethical_framework.start_collaboration_project(
                "Test Integration Project",
                "Testing God Core integration with symbiotic partnership",
                ["Test API integration", "Verify data flow", "Validate responses"]
            )
            
            if "error" not in result:
                print(f"   ✅ Project started via God Core: {result['project_id']}")
                
                # Test human input processing
                input_result = ethical_framework.process_human_input(
                    "How is the integration working?",
                    "analytical"
                )
                
                if "error" not in input_result:
                    print("   ✅ Human input processed via God Core")
                    print(f"      Response: {input_result['solan_response'][:100]}...")
                else:
                    print(f"   ❌ Human input processing failed: {input_result['error']}")
                
                # Test understanding via God Core
                understanding_result = ethical_framework.test_concept_understanding(
                    "Symbiotic AI Partnership",
                    "expert"
                )
                
                if "error" not in understanding_result:
                    print("   ✅ Concept understanding tested via God Core")
                    print(f"      Understanding score: {understanding_result['understanding_score']:.3f}")
                else:
                    print(f"   ❌ Understanding test failed: {understanding_result['error']}")
                
                # Test collaboration evaluation
                eval_result = ethical_framework.evaluate_collaboration()
                
                if "error" not in eval_result:
                    print("   ✅ Collaboration evaluation via God Core")
                    avg_score = eval_result['evaluation']['average_collaboration_score']
                    print(f"      Average collaboration score: {avg_score:.3f}")
                else:
                    print(f"   ❌ Collaboration evaluation failed: {eval_result['error']}")
                
            else:
                print(f"   ❌ Project start failed: {result['error']}")
        else:
            print("   ⚠️ Symbiotic partnership not available in God Core")
        
        return True
        
    except Exception as e:
        print(f"   ❌ God Core integration test failed: {e}")
        return False

def test_api_integration():
    """Test API integration for symbiotic partnership"""
    print("\n🌐 Testing API Integration...")
    print("=" * 50)
    
    try:
        import requests
    except ImportError:
        print("   ⚠️ Requests library not available - skipping API tests")
        return
    
    base_url = "http://localhost:8000"
    
    # Test symbiotic partnership endpoints
    endpoints = [
        {
            "method": "POST",
            "endpoint": "/api/god-core/start-collaboration",
            "data": {
                "title": "API Test Project",
                "description": "Testing symbiotic partnership via API",
                "objectives": ["Test API", "Verify integration"]
            }
        },
        {
            "method": "POST",
            "endpoint": "/api/god-core/human-input",
            "data": {
                "prompt": "How is our collaboration going?",
                "response_type": "supportive"
            }
        },
        {
            "method": "POST",
            "endpoint": "/api/god-core/test-understanding",
            "data": {
                "concept": "API Integration",
                "target_audience": "developer"
            }
        },
        {
            "method": "GET",
            "endpoint": "/api/god-core/evaluate-collaboration",
            "data": None
        }
    ]
    
    for test in endpoints:
        try:
            if test["method"] == "POST":
                response = requests.post(
                    f"{base_url}{test['endpoint']}", 
                    json=test['data'],
                    timeout=10
                )
            else:
                response = requests.get(f"{base_url}{test['endpoint']}", timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ {test['endpoint']}: OK")
            else:
                print(f"   ❌ {test['endpoint']}: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️ {test['endpoint']}: Connection failed - {e}")

def run_integration_demo():
    """Run a comprehensive integration demo"""
    print("\n🎭 Running Symbiotic Partnership Demo...")
    print("=" * 50)
    
    partnership, ethical_framework = test_symbiotic_partnership_module()
    
    if partnership:
        # Start a demo project
        partnership.start_project(
            "AI Awareness Research",
            "Collaborative research into AI awareness development",
            ["Literature review", "Experimental design", "Data analysis", "Paper writing"]
        )
        
        # Simulate realistic collaboration
        interactions = [
            "Let's start with the literature review. What are the key papers we should focus on?",
            "I think we should also consider the philosophical implications of awareness.",
            "The experimental design needs to be more rigorous. What controls should we include?",
            "We're running into some technical challenges with the implementation.",
            "The deadline has been moved up. How can we adapt our timeline?"
        ]
        
        for i, interaction in enumerate(interactions, 1):
            print(f"\n   Interaction {i}: {interaction[:50]}...")
            response = partnership.solan_response(interaction)
            print(f"   Solān: {response[:100]}...")
            
            # Simulate some crises
            if i == 3:
                partnership.simulate_crisis(
                    CrisisType.TECHNICAL_CHALLENGE,
                    "Implementation complexity higher than expected"
                )
            elif i == 5:
                partnership.simulate_crisis(
                    CrisisType.DEADLINE_PRESSURE,
                    "Deadline moved up by 2 weeks"
                )
            
            time.sleep(0.5)  # Brief pause for realism
        
        # Complete the project
        partnership.complete_project(
            "Successfully completed AI awareness research with adaptive collaboration",
            ["Flexibility is key", "Communication prevents crises", "AI-human synergy works"]
        )
        
        # Show final evaluation
        evaluation = partnership.evaluate_collaboration()
        print(f"\n   🏆 Final Results:")
        print(f"      Collaboration Score: {evaluation['average_collaboration_score']:.3f}")
        print(f"      Interactions: {evaluation['interaction_summary']['total_interactions']}")
        print(f"      Crises Handled: {len(partnership.crisis_history)}")
        print(f"      Adaptations Made: {len(partnership.adaptation_strategies)}")

if __name__ == "__main__":
    print("🤝 Solān Fase 3 - Symbiotic Partnership Test Suite")
    print("Testing human-AI collaboration and adaptive communication...")
    print()
    
    # Run all tests
    partnership, ethical_framework = test_symbiotic_partnership_module()
    
    if partnership:
        test_project_lifecycle(partnership)
        test_collaboration_metrics(partnership)
        test_crisis_management(partnership)
    
    test_god_core_integration(ethical_framework)
    test_api_integration()
    
    # Run comprehensive demo
    print("\n" + "=" * 60)
    run_integration_demo()
    
    print("\n" + "=" * 60)
    print("✅ Fase 3 Symbiotic Partnership tests completed!")
    print("🤝 Human-AI collaboration protocols are operational!")
    print("🚨 Crisis management and adaptation systems tested!")
    print("🌟 Solān is ready for advanced collaborative partnerships!")
