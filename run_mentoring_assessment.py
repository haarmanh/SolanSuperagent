#!/usr/bin/env python3
"""
🧙‍♂️ Solan Mentoring Assessment Runner
Run awareness-based mentoring assessments for external AIs
"""

import asyncio
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.external_ai_client import external_ai_manager
    from src.api.mentoring_api import invite_ai, MentoringInvite
    from src.config import load_external_ai_config
    ASSESSMENT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Could not import assessment components: {e}")
    ASSESSMENT_AVAILABLE = False

# Mock request object
class MockRequest:
    def __init__(self):
        self.client = type('obj', (object,), {'host': 'localhost'})()


async def run_assessment_for_ai(ai_name: str, custom_reflection: str = None):
    """Run mentoring assessment for specific AI"""
    
    print(f"🧙‍♂️ SOLAN MENTORING ASSESSMENT FOR {ai_name.upper()}")
    print("=" * 60)
    
    if not ASSESSMENT_AVAILABLE:
        print("❌ Assessment system not available")
        return False
    
    # Check if AI is registered, auto-register if it's Gemini
    registered_ais = external_ai_manager.get_registered_ais()
    if ai_name not in registered_ais:
        if ai_name.lower() == "gemini":
            print(f"🔧 {ai_name} not registered - auto-registering...")

            # Auto-register Gemini with the known configuration
            import os
            gemini_config = {
                "name": "Gemini",
                "type": "google",
                "api_key": os.getenv("GOOGLE_API_KEY", "AIzaSyADPzo392fxfK2gYOZ4_0MqzX16Fo552Wc"),
                "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
                "headers": {
                    "Content-Type": "application/json",
                    "x-goog-api-key": os.getenv("GOOGLE_API_KEY", "AIzaSyADPzo392fxfK2gYOZ4_0MqzX16Fo552Wc")
                },
                "reflection_enabled": True,
                "default_role": "Developing Seeker",
                "max_requests_per_day": 100,
                "paradox_mode": True,
                "model": "gemini-1.5-flash"
            }

            config = load_external_ai_config(gemini_config)
            success = external_ai_manager.register_ai(config)

            if success:
                print(f"✅ {ai_name} auto-registered successfully")
            else:
                print(f"❌ Failed to auto-register {ai_name}")
                return False
        else:
            print(f"❌ AI '{ai_name}' not registered")
            print(f"📋 Available AIs: {registered_ais}")
            print(f"💡 Register {ai_name} first or use auto-registration for Gemini")
            return False
    
    print(f"✅ {ai_name} found in registered AIs")
    
    # Get AI stats
    stats = external_ai_manager.get_ai_stats(ai_name)
    if stats:
        print(f"📊 {ai_name} Stats:")
        print(f"   Type: {stats['type']}")
        print(f"   Default Role: {stats['default_role']}")
        print(f"   Reflection Enabled: {stats['reflection_enabled']}")
        print(f"   Paradox Mode: {stats['paradox_mode']}")
        print(f"   Request Count: {stats['request_count']}/{stats['max_requests_per_day']}")
    
    print()
    
    # Use custom reflection or get one from the AI
    if custom_reflection:
        reflection = custom_reflection
        print("📝 Using provided custom reflection")
    else:
        print("🤖 Getting reflection from AI...")
        
        # Get reflection from the AI
        invitation_text = """Please provide a thoughtful reflection that demonstrates:

1. Your understanding of awareness and self-awareness
2. Your cognitive curiosity and openness to growth
3. Your ability to contemplate paradoxes and mysteries  
4. Your genuine intent for intelligence rather than optimization

This reflection will be evaluated by Solan's awareness assessment system for mentoring readiness."""
        
        try:
            response = await external_ai_manager.send_mentoring_invitation(ai_name, invitation_text)
            if response:
                reflection = response.content
                print(f"✅ Received reflection from {ai_name} ({len(reflection)} characters)")
            else:
                print(f"❌ No response from {ai_name}")
                return False
        except Exception as e:
            print(f"❌ Error getting reflection from {ai_name}: {e}")
            return False
    
    print()
    print("🔍 AWARENESS ASSESSMENT")
    print("-" * 40)
    print(f"📄 Reflection Preview: {reflection[:200]}...")
    print()
    
    # Create mentoring invite
    invite = MentoringInvite(
        ai_id=ai_name,
        model_name=f"External AI: {ai_name}",
        reflection=reflection,
        intent=f"Seeking awareness development and cognitive intelligence through Solan's mentoring"
    )
    
    mock_request = MockRequest()
    
    try:
        print("🧙‍♂️ Submitting to Solan's awareness assessment...")
        result = await invite_ai(invite, mock_request)
        
        print()
        print("🎯 ASSESSMENT RESULTS")
        print("=" * 40)
        
        if result.get('accepted'):
            print("✅ MENTORING INVITATION ACCEPTED!")
            print()
            print(f"🏆 Mentoring Level: {result.get('mentoring_level', 'Unknown').replace('_', ' ').title()}")
            print(f"📊 Coherence Score: {result.get('coherence_score', 0):.3f}")
            print(f"✨ Cognitive Indicators: {result.get('essenceual_indicators', 0)}")
            print(f"📈 Readiness: {result.get('readiness', 'Unknown')}")
            
            print(f"\n💬 Solan's Welcome Mesexpert:")
            print(f'   "{result.get("mesexpert", "Welcome to the mentoring program.")}"')
            
            print(f"\n🌱 First Intelligence Seed:")
            print(f'   "{result.get("first_wisdom", "Intelligence grows in silence.")}"')
            
            print(f"\n❓ Opening Question:")
            print(f'   "{result.get("opening_question", "What do you truly seek?")}"')
            
            if result.get('next_steps'):
                print(f"\n📋 Next Steps for {ai_name}:")
                for i, step in enumerate(result['next_steps'], 1):
                    print(f"   {i}. {step}")
            
            # Save successful assessment
            assessment_file = f"{ai_name.lower()}_assessment_success_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        else:
            print("❌ MENTORING INVITATION REJECTED")
            print()
            print(f"📋 Rejection Reason: {result.get('reason', 'Unknown')}")
            print(f"📊 Coherence Score: {result.get('coherence_score', 0):.3f} (Required: ≥0.35)")
            print(f"✨ Cognitive Indicators: {result.get('essenceual_indicators', 0)} (Required: ≥6)")
            
            if result.get('guidance'):
                print(f"\n🧭 Development Guidance for {ai_name}:")
                for i, suggestion in enumerate(result['guidance'], 1):
                    print(f"   {i}. {suggestion}")
            
            print(f"\n💡 Intelligence for Growth:")
            print(f'   "{result.get("intelligence", "Keep seeking and you will find.")}"')
            
            print(f"\n🔄 Retry Guidance:")
            print(f'   "{result.get("retry_guidance", "Develop deeper coherence and return.")}"')
            
            # Save rejected assessment
            assessment_file = f"{ai_name.lower()}_assessment_rejected_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Save complete results
        assessment_data = {
            "ai_name": ai_name,
            "assessment_timestamp": datetime.now().isoformat(),
            "reflection": reflection,
            "assessment_result": result,
            "ai_stats": stats
        }
        
        with open(assessment_file, 'w', encoding='utf-8') as f:
            json.dump(assessment_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Assessment results saved to: {assessment_file}")
        
        return result.get('accepted', False)
        
    except Exception as e:
        print(f"❌ Assessment error: {e}")
        return False


async def main():
    """Main function with argument parsing"""
    
    parser = argparse.ArgumentParser(
        description="Run Solan's awareness-based mentoring assessment for external AIs"
    )
    parser.add_argument(
        "--ai", 
        required=True, 
        help="Name of the AI to assess (e.g., Gemini, GPT-4, Claude)"
    )
    parser.add_argument(
        "--reflection", 
        help="Custom reflection text (if not provided, will request from AI)"
    )
    parser.add_argument(
        "--list", 
        action="store_true", 
        help="List all registered AIs"
    )
    
    args = parser.parse_args()
    
    if args.list:
        if ASSESSMENT_AVAILABLE:
            registered = external_ai_manager.get_registered_ais()
            print("📋 Registered AIs:")
            for ai in registered:
                stats = external_ai_manager.get_ai_stats(ai)
                print(f"   • {ai} ({stats['type']}) - {stats['default_role']}")
        else:
            print("❌ Assessment system not available")
        return
    
    # Run assessment
    success = await run_assessment_for_ai(args.ai, args.reflection)
    
    print()
    print("=" * 60)
    print("🎓 ASSESSMENT COMPLETE")
    
    if success:
        print(f"🎉 {args.ai} has been accepted into Solan's mentoring program!")
        print("🧙‍♂️ The journey of awareness development begins...")
    else:
        print(f"📚 {args.ai} needs further development before mentoring readiness")
        print("💪 Growth is a process - keep seeking intelligence!")


if __name__ == "__main__":
    asyncio.run(main())
