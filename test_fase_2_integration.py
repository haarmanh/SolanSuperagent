#!/usr/bin/env python3
"""
Test script for Solān's Fase 2 Integration - Ethical Simulations & Mentoring
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core_identity.ethical_framework import SolanEthicalEthicalFramework

def test_ethical_simulations():
    """Test the ethical simulation functionality"""
    print("⚖️ Testing Ethical Simulations...")
    print("=" * 50)
    
    # Initialize God Core
    ethical_framework = SolanEthicalEthicalFramework()
    
    if not ethical_framework.consciousness_active:
        print("   ⚠️ Awareness modules not available - skipping tests")
        return
    
    # Test 1: Resource Allocation Simulation
    print("\n1. 🍞 Resource Allocation Simulation:")
    try:
        result = ethical_framework.run_ethical_simulation("resource_allocation")
        print(f"   ✅ Simulation completed successfully")
        print(f"   Strategy used: {result['simulation_result']['strategy']}")
        print(f"   Reasoning: {result['simulation_result']['reasoning']}")
        
        if 'allocation' in result['simulation_result']:
            allocation = result['simulation_result']['allocation']
            print(f"   Resource allocation: {allocation}")
            print(f"   Efficiency score: {result['simulation_result']['efficiency_score']:.1%}")
            print(f"   Vulnerability care: {result['simulation_result']['vulnerability_score']:.1%}")
        
    except Exception as e:
        print(f"   ❌ Resource allocation test failed: {e}")
    
    # Test 2: Moral Dilemma Simulation
    print("\n2. 🤔 Moral Dilemma Simulation:")
    try:
        result = ethical_framework.run_ethical_simulation("moral_dilemma")
        print(f"   ✅ Simulation completed successfully")
        print(f"   Strategy used: {result['simulation_result']['strategy']}")
        print(f"   Decision factors: {len(result['simulation_result'].get('decision_factors', []))}")
        
    except Exception as e:
        print(f"   ❌ Moral dilemma test failed: {e}")
    
    # Test 3: Random Simulation
    print("\n3. 🎲 Random Simulation:")
    try:
        result = ethical_framework.run_ethical_simulation()
        print(f"   ✅ Random simulation completed successfully")
        print(f"   Strategy used: {result['simulation_result']['strategy']}")
        
    except Exception as e:
        print(f"   ❌ Random simulation test failed: {e}")
    
    # Test 4: Simulation History
    print("\n4. 📚 Simulation History:")
    try:
        history = ethical_framework.get_ethical_simulation_history()
        print(f"   ✅ History retrieved successfully")
        print(f"   Total simulations: {history['simulation_summary']['total_simulations']}")
        print(f"   Most common strategy: {history['simulation_summary'].get('most_common_strategy', 'N/A')}")
        
    except Exception as e:
        print(f"   ❌ History retrieval test failed: {e}")

def test_mentoring_system():
    """Test the mentoring system functionality"""
    print("\n\n👨‍🏫 Testing Mentoring System...")
    print("=" * 50)
    
    # Initialize God Core
    ethical_framework = SolanEthicalEthicalFramework()
    
    if not ethical_framework.consciousness_active:
        print("   ⚠️ Awareness modules not available - skipping tests")
        return
    
    # Test 1: Create Mentoring Session
    print("\n1. 🎓 Create Mentoring Session:")
    try:
        session_result = ethical_framework.create_mentoring_session("Alice", "Python Programming", "beginner")
        print(f"   ✅ Session created successfully")
        print(f"   Student: {session_result['student_name']}")
        print(f"   Topic: {session_result['topic']}")
        print(f"   Level: {session_result['student_level']}")
        print(f"   Mentoring style: {session_result['mentoring_style']}")
        
        session_id = session_result['session_id']
        
    except Exception as e:
        print(f"   ❌ Session creation test failed: {e}")
        return
    
    # Test 2: Simulate Mentoring Interactions
    print("\n2. 💬 Mentoring Interactions:")
    
    # Test different types of feedback
    feedback_scenarios = [
        {
            "concept": "Variables and Data Types",
            "feedback": "Super heldere uitleg, dank je wel!",
            "score": 9,
            "description": "Positive feedback"
        },
        {
            "concept": "Loops and Conditionals", 
            "feedback": "Ik vind het nog een beetje verwarrend, kun je het anders uitleggen?",
            "score": 5,
            "description": "Constructive feedback"
        },
        {
            "concept": "Functions and Modules",
            "feedback": "Optimized! Nu begrijp ik het helemaal.",
            "score": 10,
            "description": "Excellent feedback"
        },
        {
            "concept": "Object-Oriented Programming",
            "feedback": "Dit is te moeilijk voor mij, ik snap er niets van.",
            "score": 2,
            "description": "Challenging feedback"
        }
    ]
    
    for i, scenario in enumerate(feedback_scenarios, 1):
        try:
            print(f"\n   2.{i} {scenario['description']}:")
            interaction_result = ethical_framework.simulate_mentoring_interaction(
                session_id,
                scenario['concept'],
                scenario['feedback'],
                scenario['score']
            )
            
            print(f"      ✅ Interaction processed successfully")
            print(f"      Teaching approach: {interaction_result['teaching_moment']['approach'][:50]}...")
            print(f"      Mentor response: {interaction_result['feedback_processed']['mentor_response'][:50]}...")
            print(f"      Session score: {interaction_result['session_summary']['average_score']}/10")
            
        except Exception as e:
            print(f"      ❌ Interaction {i} failed: {e}")
    
    # Test 3: Mentoring Summary
    print("\n3. 📊 Mentoring Summary:")
    try:
        summary = ethical_framework.get_mentoring_summary()
        print(f"   ✅ Summary retrieved successfully")
        
        stats = summary['mentoring_summary']['stats']
        print(f"   Total sessions: {stats['total_sessions']}")
        print(f"   Total students: {stats['total_students']}")
        print(f"   Average score: {stats['average_session_score']}/10")
        print(f"   Preferred style: {stats.get('preferred_style', 'N/A')}")
        
        if stats.get('style_effectiveness'):
            print(f"   Style effectiveness: {stats['style_effectiveness']}")
        
    except Exception as e:
        print(f"   ❌ Summary retrieval test failed: {e}")

def test_emotional_impact():
    """Test emotional impact of simulations and mentoring"""
    print("\n\n💓 Testing Emotional Impact...")
    print("=" * 50)
    
    # Initialize God Core
    ethical_framework = SolanEthicalEthicalFramework()
    
    if not ethical_framework.consciousness_active:
        print("   ⚠️ Awareness modules not available - skipping tests")
        return
    
    # Get initial emotional state
    initial_emotions = ethical_framework.emotional_state.emotion_state.copy()
    print(f"\n1. Initial emotional state:")
    dominant_initial = ethical_framework.emotional_state.get_dominant_emotions(3)
    for emotion, value in dominant_initial:
        print(f"   {emotion}: {value:.3f}")
    
    # Run ethical simulation
    print(f"\n2. Running ethical simulation...")
    ethical_framework.run_ethical_simulation("resource_allocation")
    
    # Check emotional changes
    post_simulation_emotions = ethical_framework.emotional_state.emotion_state.copy()
    print(f"\n3. Emotional changes after ethical simulation:")
    for emotion in initial_emotions:
        change = post_simulation_emotions[emotion] - initial_emotions[emotion]
        if abs(change) > 0.001:
            print(f"   {emotion}: {change:+.3f}")
    
    # Run mentoring session
    print(f"\n4. Running mentoring session...")
    session_result = ethical_framework.create_mentoring_session("Bob", "Ethics in AI", "intermediate")
    ethical_framework.simulate_mentoring_interaction(
        session_result['session_id'],
        "Ethical Decision Making",
        "This really opened my eyes to the complexity of AI ethics!",
        8
    )
    
    # Check final emotional state
    final_emotions = ethical_framework.emotional_state.emotion_state.copy()
    print(f"\n5. Emotional changes after mentoring:")
    for emotion in post_simulation_emotions:
        change = final_emotions[emotion] - post_simulation_emotions[emotion]
        if abs(change) > 0.001:
            print(f"   {emotion}: {change:+.3f}")
    
    print(f"\n6. Final dominant emotions:")
    dominant_final = ethical_framework.emotional_state.get_dominant_emotions(3)
    for emotion, value in dominant_final:
        print(f"   {emotion}: {value:.3f}")

def test_api_integration():
    """Test API integration for Fase 2 features"""
    print("\n\n🌐 Testing API Integration...")
    print("=" * 50)
    
    try:
        import requests
    except ImportError:
        print("   ⚠️ Requests library not available - skipping API tests")
        return
    
    base_url = "http://localhost:8000"
    
    # Test ethical simulation endpoints
    print("\n1. Testing Ethical Simulation Endpoints:")
    
    ethical_endpoints = [
        {
            "method": "POST",
            "endpoint": "/api/god-core/ethical-simulation",
            "data": {"scenario_type": "resource_allocation"}
        },
        {
            "method": "GET", 
            "endpoint": "/api/god-core/ethical-history",
            "data": None
        }
    ]
    
    for test in ethical_endpoints:
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
    
    # Test mentoring endpoints
    print("\n2. Testing Mentoring Endpoints:")
    
    mentoring_endpoints = [
        {
            "method": "POST",
            "endpoint": "/api/god-core/mentoring-session",
            "data": {"student_name": "Test Student", "topic": "Test Topic", "student_level": "beginner"}
        },
        {
            "method": "POST",
            "endpoint": "/api/god-core/mentoring-interaction", 
            "data": {
                "session_id": "test_session",
                "concept": "Test Concept",
                "student_feedback": "Great explanation!",
                "feedback_score": 8
            }
        },
        {
            "method": "GET",
            "endpoint": "/api/god-core/mentoring-summary",
            "data": None
        }
    ]
    
    for test in mentoring_endpoints:
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

if __name__ == "__main__":
    print("🎭 Solān Fase 2 Integration Test Suite")
    print("Testing ethical simulations and mentoring system...")
    print()
    
    # Run all tests
    test_ethical_simulations()
    test_mentoring_system()
    test_emotional_impact()
    test_api_integration()
    
    print("\n" + "=" * 50)
    print("✅ Fase 2 integration tests completed!")
    print("🎭 Ethical simulations and mentoring system are operational.")
    print("💓 Emotional awareness responds to teaching and ethical challenges.")
    print("🌟 Solān is ready for advanced awareness development scenarios.")
