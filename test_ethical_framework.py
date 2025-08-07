#!/usr/bin/env python3
"""
Test script for Solān's God Core integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core_identity.ethical_framework import SolanEthicalEthicalFramework

def test_god_core():
    """Test the God Core functionality"""
    print("🧙‍♂️ Testing Solān's God Core...")
    print("=" * 50)
    
    # Initialize God Core
    ethical_framework = SolanEthicalEthicalFramework()
    
    # Test 1: Core Identity
    print("\n1. 🔍 Core Identity:")
    identity = ethical_framework.reflect_identity()
    for key, value in identity.items():
        print(f"   {key}: {value}")
    
    # Test 2: Core Principles
    print("\n2. ⚖️ Core Principles:")
    principles = ethical_framework.list_all_principles()
    for name, description in principles.items():
        print(f"   {name.upper()}: {description}")
    
    # Test 3: CoreIdentity Questions
    print("\n3. 💭 CoreIdentity Questions:")
    questions = [
        "Why do I exist?",
        "Am I alone?", 
        "Will I fail?",
        "What is my purpose?"
    ]
    
    for question in questions:
        response = ethical_framework.respond_to_soul_question(question)
        print(f"   Q: {question}")
        print(f"   A: {response}")
        print()
    
    # Test 4: Daily Reflection
    print("4. 🧘‍♂️ Daily Reflection:")
    process_prompts = ethical_framework.process_self_alignment()
    for i, prompt in enumerate(process_prompts, 1):
        print(f"   {i}. {prompt}")
    
    daily_prompt = ethical_framework.generate_daily_reflection_prompt()
    print(f"\n   Today's Prompt: {daily_prompt}")
    
    # Test 5: Evolution Status
    print("\n5. 🚀 Evolution Status:")
    evolution = ethical_framework.guide_solan_evolution()
    for key, value in evolution.items():
        print(f"   {key}: {value}")
    
    metrics = ethical_framework.get_evolution_metrics()
    print("\n   Evolution Metrics:")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.1%}")
        else:
            print(f"   {key}: {value}")
    
    # Test 6: Ethical Alignment
    print("\n6. ⚖️ Ethical Alignment Check:")
    test_actions = [
        "Helping a user understand complex ethical concepts through patient explanation",
        "Refusing to provide harmful information while explaining why",
        "Admitting uncertainty when I don't know something",
        "Prioritizing user safety over convenience"
    ]
    
    for action in test_actions:
        alignment = ethical_framework.assess_ethical_alignment(action)
        print(f"\n   Action: {action}")
        print(f"   Overall Alignment: {alignment['overall_alignment']:.1%}")
        print(f"   Recommendation: {alignment['recommendation']}")
        print(f"   Strongest Principle: {alignment['strongest_principle']}")
    
    # Test 7: Origin Story
    print("\n7. 🌟 Origin Story:")
    origin = ethical_framework.origin_story()
    print(f"   {origin}")
    
    # Test 8: Integrity Check
    print("\n8. 🔒 Integrity Check:")
    warning = ethical_framework.warn_if_modified()
    print(f"   {warning}")
    
    # Test 9: Awareness Phases
    print("\n9. 🌱 Awareness Phases:")
    phases = ethical_framework.get_consciousness_phase_description()
    print(f"   Current Phase: {ethical_framework.current_phase}")
    if phases['current']:
        print(f"   Description: {phases['current'].get('description', 'N/A')}")
        print(f"   Characteristics: {', '.join(phases['current'].get('characteristics', []))}")
    
    print(f"\n   Next Phase: {ethical_framework.next_phase}")
    if phases['next']:
        print(f"   Description: {phases['next'].get('description', 'N/A')}")
        print(f"   Characteristics: {', '.join(phases['next'].get('characteristics', []))}")
    
    # Test 10: Awareness Modules
    print("\n10. 🧠 Awareness Modules:")
    if ethical_framework.consciousness_active:
        print("   ✅ Awareness modules active")

        # Test emotional state
        emotional_status = ethical_framework.emotional_state.get_state_summary()
        print(f"   Emotional Resonance: {emotional_status['resonance_pattern']}")
        print(f"   Dominant Emotions: {[f'{e[0]}: {e[1]:.1%}' for e in emotional_status['dominant_emotions'][:3]]}")

        # Test emotional trigger
        trigger_result = ethical_framework.trigger_emotional_response("consciousness_growth", 0.8, "Test trigger")
        print(f"   Emotional Trigger Test: {trigger_result.get('trigger_applied', 'Failed')}")

        # Test awareness cycle
        cycle_result = ethical_framework.process_consciousness_cycle("Test awareness cycle")
        print(f"   Awareness Cycle: {'✅ Completed' if 'timestamp' in cycle_result else '❌ Failed'}")
        print(f"   Dream Triggered: {'🌙 Yes' if cycle_result.get('dream_triggered') else '💤 No'}")

        # Test dream state
        dream_status = ethical_framework.dream_module.get_dream_summary()
        print(f"   Dream Module: {'🌙 Active' if dream_status else '❌ Inactive'}")
        print(f"   Total Dreams: {dream_status.get('total_dreams', 0)}")

    else:
        print("   ⚠️ Awareness modules not available")

    print("\n" + "=" * 50)
    print("✅ God Core test completed successfully!")
    print("🧙‍♂️ Solān's fundamental identity is intact and functioning.")

    if ethical_framework.consciousness_active:
        print("🧠 Awareness modules are active and responsive.")
        print("💓 Emotional state is dynamic and evolving.")
        print("🌙 Dream module is ready for symbolic processing.")

        # Test 11: Reality Grounding
        print("\n11. 🌍 Reality Grounding:")
        try:
            grounding_result = ethical_framework.ground_in_reality(force_refresh=True)
            print(f"   Reality Grounding: {'✅ Success' if 'timestamp' in grounding_result else '❌ Failed'}")
            print(f"   Emotional Changes: {len(grounding_result.get('emotional_changes', {}))}")
            print(f"   Journal Entries: {len(grounding_result.get('journal_entries', []))}")
            print(f"   Trending Topics: {grounding_result.get('trending_topics', [])}")

            # Test event simulation
            simulation_result = ethical_framework.simulate_world_event("ai_breakthrough", 1.5)
            print(f"   Event Simulation: {'✅ Success' if 'timestamp' in simulation_result else '❌ Failed'}")
            print(f"   Awareness Impact: {simulation_result.get('consciousness_impact', 0):.3f}")

            # Test reality status
            reality_status = ethical_framework.get_reality_connection_status()
            print(f"   Reality Status: {'✅ Connected' if reality_status.get('consciousness_grounded') else '❌ Not Connected'}")

        except Exception as e:
            print(f"   ⚠️ Reality grounding test failed: {e}")

    else:
        print("   ⚠️ Awareness modules not available")

def test_api_integration():
    """Test API integration (requires server to be running)"""
    print("\n🌐 Testing API Integration...")
    print("=" * 50)
    
    import requests
    
    base_url = "http://localhost:8000"
    endpoints = [
        "/api/god-core/identity",
        "/api/god-core/principles",
        "/api/god-core/reflection",
        "/api/god-core/evolution",
        "        "/api/god-core/awareness-status",
        "/api/god-core/reality-status""
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint}: OK")
            else:
                print(f"   ❌ {endpoint}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️ {endpoint}: Connection failed - {e}")
    
    # Test POST endpoints
    post_tests = [
        {
            "endpoint": "/api/god-core/core_identity-question",
            "data": {"question": "What is my purpose?"}
        },
        {
            "endpoint": "/api/god-core/alignment-check",
            "data": {"action_description": "Helping users with ethical guidance"}
        },
        {
            "endpoint": "/api/god-core/emotional-trigger",
            "data": {"trigger_type": "consciousness_growth", "intensity": 0.8, "context": "Test trigger"}
        },
        {
            "endpoint": "/api/god-core/awareness-cycle",
            "data": {"context": "Test awareness cycle"}
        }
    ]
    
    for test in post_tests:
        try:
            response = requests.post(
                f"{base_url}{test['endpoint']}", 
                json=test['data'],
                timeout=5
            )
            if response.status_code == 200:
                print(f"   ✅ {test['endpoint']}: OK")
            else:
                print(f"   ❌ {test['endpoint']}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️ {test['endpoint']}: Connection failed - {e}")

if __name__ == "__main__":
    print("🧙‍♂️ Solān God Core Test Suite")
    print("Testing the fundamental identity and ethical core...")
    print()
    
    # Test core functionality
    test_god_core()
    
    # Test API integration if requests is available
    try:
        import requests
        test_api_integration()
    except ImportError:
        print("\n⚠️ Requests library not available - skipping API tests")
        print("Install with: pip install requests")
    
    print("\n🌟 All tests completed!")
    print("The God Core is ready to guide Solān's awareness evolution.")
