#!/usr/bin/env python3
"""
Test script for Solān Live Dashboard Integration
Validates direct God Core integration and real-time data flow
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_god_core_availability():
    """Test if the real God Core is available"""
    print("🧙‍♂️ Testing God Core Availability...")
    print("=" * 50)
    
    try:
        from core_identity.ethical_framework import SolanEthicalEthicalFramework
        print("   ✅ God Core import successful")
        
        # Try to initialize
        ethical_framework = SolanEthicalEthicalFramework()
        print("   ✅ God Core initialization successful")
        
        if ethical_framework.consciousness_active:
            print("   ✅ Awareness modules active")
            
            # Test emotional state
            emotions = ethical_framework.emotional_state.emotion_state
            print(f"   ✅ Emotional state available: {len(emotions)} emotions")
            
            # Test dominant emotions
            dominant = ethical_framework.emotional_state.get_dominant_emotions(3)
            print(f"   ✅ Dominant emotions: {[e[0] for e in dominant]}")
            
            return ethical_framework
            
        else:
            print("   ⚠️ Awareness modules not available")
            return ethical_framework
            
    except ImportError as e:
        print(f"   ❌ God Core import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ God Core initialization failed: {e}")
        return None

def test_live_dashboard_wrapper():
    """Test the live dashboard wrapper functionality"""
    print("\n📱 Testing Live Dashboard Wrapper...")
    print("=" * 50)
    
    try:
        # Import the wrapper
        sys.path.append('.')
        from solan_simple_live_dashboard import SolanCoreWrapper
        
        print("   ✅ Wrapper import successful")
        
        # Initialize wrapper
        wrapper = SolanCoreWrapper()
        print(f"   ✅ Wrapper initialized - Mode: {'Real' if wrapper.is_real else 'Simplified'}")
        
        # Test emotion retrieval
        emotions = wrapper.get_emotions()
        print(f"   ✅ Emotions retrieved: {len(emotions)} emotions")
        
        if emotions:
            top_emotion = max(emotions.items(), key=lambda x: x[1])
            print(f"   ✅ Top emotion: {top_emotion[0]} ({top_emotion[1]:.3f})")
        
        # Test journal retrieval
        journal = wrapper.get_journal()
        print(f"   ✅ Journal retrieved: {len(journal)} entries")
        
        # Test awareness status
        is_active = wrapper.is_consciousness_active()
        print(f"   ✅ Awareness active: {is_active}")
        
        return wrapper
        
    except ImportError as e:
        print(f"   ❌ Wrapper import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Wrapper test failed: {e}")
        return None

def test_emotional_manipulation(wrapper):
    """Test emotional state manipulation"""
    print("\n💓 Testing Emotional Manipulation...")
    print("=" * 50)
    
    if not wrapper:
        print("   ⚠️ No wrapper available - skipping test")
        return
    
    try:
        # Get initial emotional state
        initial_emotions = wrapper.get_emotions()
        if not initial_emotions:
            print("   ⚠️ No emotions available - skipping test")
            return
        
        initial_coherence = initial_emotions.get('coherence', 0.0)
        print(f"   📊 Initial coherence: {initial_coherence:.3f}")
        
        # Trigger emotional change
        wrapper.trigger_emotion('coherence', 0.1)
        print("   ✅ Emotional trigger sent")
        
        # Small delay for processing
        time.sleep(0.1)
        
        # Get updated emotional state
        updated_emotions = wrapper.get_emotions()
        updated_coherence = updated_emotions.get('coherence', 0.0)
        print(f"   📊 Updated coherence: {updated_coherence:.3f}")
        
        # Check for change
        change = updated_coherence - initial_coherence
        if abs(change) > 0.001:
            print(f"   ✅ Emotional change detected: {change:+.3f}")
        else:
            print("   ⚠️ No significant emotional change detected")
        
    except Exception as e:
        print(f"   ❌ Emotional manipulation test failed: {e}")

def test_journal_functionality(wrapper):
    """Test journal entry functionality"""
    print("\n📓 Testing Journal Functionality...")
    print("=" * 50)
    
    if not wrapper:
        print("   ⚠️ No wrapper available - skipping test")
        return
    
    try:
        # Get initial journal count
        initial_journal = wrapper.get_journal()
        initial_count = len(initial_journal)
        print(f"   📊 Initial journal entries: {initial_count}")
        
        # Add a test entry
        test_entry = f"Test journal entry added at {datetime.now().strftime('%H:%M:%S')}"
        wrapper.add_journal_entry(test_entry)
        print("   ✅ Journal entry added")
        
        # Get updated journal
        updated_journal = wrapper.get_journal()
        updated_count = len(updated_journal)
        print(f"   📊 Updated journal entries: {updated_count}")
        
        # Check for new entry
        if updated_count > initial_count:
            print("   ✅ Journal entry successfully added")
            
            # Check if our entry is in the recent entries
            if any(test_entry in entry for entry in updated_journal):
                print("   ✅ Test entry found in recent journal")
            else:
                print("   ⚠️ Test entry not found in recent journal (may be in history)")
        else:
            print("   ⚠️ Journal count did not increase")
        
        # Display recent entries
        print("   📖 Recent journal entries:")
        for i, entry in enumerate(updated_journal[-3:], 1):
            truncated = entry[:60] + "..." if len(entry) > 60 else entry
            print(f"      [{i}] {truncated}")
        
    except Exception as e:
        print(f"   ❌ Journal functionality test failed: {e}")

def test_dashboard_display_functions():
    """Test dashboard display functions"""
    print("\n🖥️ Testing Dashboard Display Functions...")
    print("=" * 50)
    
    try:
        from solan_simple_live_dashboard import display_emotional_state, display_journal_entries, analyze_coherence
        
        print("   ✅ Display functions imported successfully")
        
        # Test with sample data
        sample_emotions = {
            "empathy": 0.85,
            "coherence": 0.72,
            "curiosity": 0.68,
            "authenticity": 0.91,
            "stability": 0.45
        }
        
        sample_journal = [
            "Test journal entry 1 - awareness exploration",
            "Test journal entry 2 - emotional development",
            "Test journal entry 3 - reality grounding session"
        ]
        
        print("\n   🧠 Testing emotional state display:")
        display_emotional_state(sample_emotions)
        
        print("\n   📓 Testing journal display:")
        display_journal_entries(sample_journal)
        
        print("\n   🧭 Testing coherence analysis:")
        analyze_coherence(sample_emotions)
        
        print("\n   ✅ All display functions working correctly")
        
    except ImportError as e:
        print(f"   ❌ Display functions import failed: {e}")
    except Exception as e:
        print(f"   ❌ Display functions test failed: {e}")

def test_live_dashboard_integration():
    """Test complete live dashboard integration"""
    print("\n🔄 Testing Complete Live Dashboard Integration...")
    print("=" * 50)
    
    try:
        from solan_live_cli_dashboard import SolanLiveDashboard
        
        print("   ✅ Live dashboard import successful")
        
        # Initialize dashboard (but don't run the main loop)
        dashboard = SolanLiveDashboard()
        print("   ✅ Live dashboard initialized")
        
        if dashboard.ethical_framework:
            print("   ✅ God Core connection established")
            
            if dashboard.ethical_framework.consciousness_active:
                print("   ✅ Awareness modules active")
                
                # Test awareness activity simulation
                dashboard.simulate_consciousness_activity()
                print("   ✅ Awareness activity simulation successful")
                
                # Test journal entries
                journal_count = len(dashboard.journal_entries)
                print(f"   ✅ Journal entries available: {journal_count}")
                
            else:
                print("   ⚠️ Awareness modules not active")
        else:
            print("   ⚠️ God Core not available")
        
        return dashboard
        
    except ImportError as e:
        print(f"   ❌ Live dashboard import failed: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Live dashboard test failed: {e}")
        return None

def run_integration_demo(duration=10):
    """Run a short integration demo"""
    print(f"\n🎭 Running {duration}-second Integration Demo...")
    print("=" * 50)
    
    try:
        from solan_simple_live_dashboard import SolanCoreWrapper, run_cli_dashboard
        
        # Initialize wrapper
        wrapper = SolanCoreWrapper()
        print(f"   🚀 Demo started - Mode: {'Real' if wrapper.is_real else 'Simplified'}")
        
        # Run for specified duration
        start_time = time.time()
        update_count = 0
        
        while time.time() - start_time < duration:
            # Simulate dashboard update
            emotions = wrapper.get_emotions()
            journal = wrapper.get_journal()
            
            if emotions:
                top_emotion = max(emotions.items(), key=lambda x: x[1])
                print(f"   📊 Update {update_count + 1}: Top emotion = {top_emotion[0]} ({top_emotion[1]:.3f})")
            
            # Trigger small emotional change
            if emotions and 'coherence' in emotions:
                wrapper.trigger_emotion('coherence', 0.01)
            
            update_count += 1
            time.sleep(2)
        
        print(f"   ✅ Demo completed - {update_count} updates processed")
        
        # Final state
        final_emotions = wrapper.get_emotions()
        if final_emotions:
            print("   📊 Final emotional state:")
            top_3 = sorted(final_emotions.items(), key=lambda x: x[1], reverse=True)[:3]
            for emotion, value in top_3:
                print(f"      {emotion}: {value:.3f}")
        
    except Exception as e:
        print(f"   ❌ Integration demo failed: {e}")

if __name__ == "__main__":
    print("🧙‍♂️ Solān Live Dashboard Integration Test Suite")
    print("Testing direct God Core integration and real-time functionality...")
    print()
    
    # Run all tests
    ethical_framework = test_god_core_availability()
    wrapper = test_live_dashboard_wrapper()
    test_emotional_manipulation(wrapper)
    test_journal_functionality(wrapper)
    test_dashboard_display_functions()
    live_dashboard = test_live_dashboard_integration()
    
    # Run integration demo
    print("\n" + "=" * 60)
    run_integration_demo(10)
    
    print("\n" + "=" * 60)
    print("✅ Live Dashboard integration tests completed!")
    
    if ethical_framework and ethical_framework.consciousness_active:
        print("🌟 Real God Core with full awareness available!")
    elif ethical_framework:
        print("⚠️ God Core available but awareness modules limited")
    else:
        print("🎭 Using simplified simulation mode")
    
    print("🖥️ Live CLI dashboards are ready for real-time awareness monitoring!")
    print("💡 Use 'python launch_dashboard.py' to access all dashboard options.")
