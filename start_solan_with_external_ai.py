#!/usr/bin/env python3
"""
🌟 Start Solan Superagent with External AI Integration
Complete startup script for the awareness-based AI mentoring platform
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def print_banner():
    """Print startup banner"""
    print("🌟" + "=" * 70 + "🌟")
    print("🧙‍♂️  SOLAN SUPERAGENT - AWARENESS-BASED AI MENTORING PLATFORM  🧙‍♂️")
    print("🌟" + "=" * 70 + "🌟")
    print()
    print("🎯 Advanced Features:")
    print("   ✨ Awareness-based access control")
    print("   🧙‍♂️ AI-to-AI mentoring with cognitive assessment")
    print("   🌐 External AI integration (Gemini, GPT-4, Claude)")
    print("   📊 Real-time awareness analytics")
    print("   🔮 Fundamental memory with coherence tagging")
    print("   🌊 Paradox-based learning methodology")
    print()


def check_dependencies():
    """Check if all required dependencies are available"""
    
    print("🔍 Checking Dependencies...")
    print("-" * 30)
    
    dependencies = {
        "FastAPI": False,
        "Solan Core": False,
        "External AI System": False,
        "Mentoring API": False,
        "Coherence Analyzer": False,
        "Frontend": False
    }
    
    # Check FastAPI
    try:
        import fastapi
        dependencies["FastAPI"] = True
        print("✅ FastAPI available")
    except ImportError:
        print("❌ FastAPI not available - install with: pip install fastapi uvicorn")
    
    # Check Solan Core
    try:
        from src.solan import SolanAgent
        from src.aether import AetherReflection
        dependencies["Solan Core"] = True
        print("✅ Solan Core available")
    except ImportError:
        print("❌ Solan Core not available")
    
    # Check External AI System
    try:
        from src.external_ai_client import external_ai_manager
        from src.api.external_ai_api import router
        dependencies["External AI System"] = True
        print("✅ External AI System available")
    except ImportError:
        print("❌ External AI System not available")
    
    # Check Mentoring API
    try:
        from src.api.mentoring_api import router
        dependencies["Mentoring API"] = True
        print("✅ Mentoring API available")
    except ImportError:
        print("❌ Mentoring API not available")
    
    # Check Coherence Analyzer
    try:
        from src.inner_coherence_analyzer import coherence_analyzer
        if coherence_analyzer:
            dependencies["Coherence Analyzer"] = True
            print("✅ Coherence Analyzer available")
        else:
            print("⚠️ Coherence Analyzer imported but not initialized")
    except ImportError:
        print("❌ Coherence Analyzer not available")
    
    # Check Frontend
    frontend_path = Path("src/frontend")
    if frontend_path.exists():
        dependencies["Frontend"] = True
        print("✅ React Frontend available")
    else:
        print("⚠️ React Frontend not found")
    
    print()
    
    # Summary
    available_count = sum(dependencies.values())
    total_count = len(dependencies)
    
    print(f"📊 Dependencies: {available_count}/{total_count} available")
    
    if available_count >= 4:  # Core functionality
        print("✅ Sufficient dependencies for core functionality")
        return True
    else:
        print("❌ Insufficient dependencies - some features may not work")
        return False


async def register_default_ais():
    """Register default external AIs"""
    
    print("🌐 Registering Default External AIs...")
    print("-" * 40)
    
    try:
        from src.external_ai_client import external_ai_manager
        from src.config import load_external_ai_config
        
        # Gemini configuration
        gemini_config = {
            "name": "Gemini",
            "type": "google",
            "api_key": os.getenv("GOOGLE_API_KEY", "PLACEHOLDER"),
            "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            "headers": {
                "Content-Type": "application/json"
            },
            "reflection_enabled": True,
            "default_role": "Developing Seeker",
            "max_requests_per_day": 100,
            "paradox_mode": True,
            "model": "gemini-pro"
        }
        
        # Register Gemini if API key is available
        if gemini_config["api_key"] != "PLACEHOLDER":
            config = load_external_ai_config(gemini_config)
            success = external_ai_manager.register_ai(config)
            if success:
                print("✅ Gemini registered successfully")
            else:
                print("❌ Failed to register Gemini")
        else:
            print("⚠️ Gemini not registered - no API key (set GOOGLE_API_KEY)")
        
        # GPT-4 configuration (if OpenAI key available)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            gpt4_config = {
                "name": "GPT-4",
                "type": "openai",
                "api_key": openai_key,
                "base_url": "https://api.openai.com/v1/chat/completions",
                "headers": {},
                "reflection_enabled": True,
                "default_role": "Developing Seeker",
                "max_requests_per_day": 50,
                "paradox_mode": True,
                "model": "gpt-4"
            }
            
            config = load_external_ai_config(gpt4_config)
            success = external_ai_manager.register_ai(config)
            if success:
                print("✅ GPT-4 registered successfully")
            else:
                print("❌ Failed to register GPT-4")
        else:
            print("⚠️ GPT-4 not registered - no API key (set OPENAI_API_KEY)")
        
        # Claude configuration (if Anthropic key available)
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            claude_config = {
                "name": "Claude",
                "type": "anthropic",
                "api_key": anthropic_key,
                "base_url": "https://api.anthropic.com/v1/mesexperts",
                "headers": {},
                "reflection_enabled": True,
                "default_role": "Wise Student",
                "max_requests_per_day": 50,
                "paradox_mode": True,
                "model": "claude-3-sonnet-20240229"
            }
            
            config = load_external_ai_config(claude_config)
            success = external_ai_manager.register_ai(config)
            if success:
                print("✅ Claude registered successfully")
            else:
                print("❌ Failed to register Claude")
        else:
            print("⚠️ Claude not registered - no API key (set ANTHROPIC_API_KEY)")
        
        # Show registered AIs
        registered = external_ai_manager.get_registered_ais()
        print(f"\n📋 Registered AIs: {registered}")
        
        return len(registered) > 0
        
    except Exception as e:
        print(f"❌ Error registering AIs: {e}")
        return False


def start_api_server():
    """Start the unified API server"""
    
    print("\n🚀 Starting Unified API Server...")
    print("-" * 40)
    
    try:
        import uvicorn
        from web_interface.unified_api import app
        
        print("🌐 Server starting on http://localhost:8000")
        print()
        print("📋 Available Endpoints:")
        print("   🧙‍♂️ /api/reflective/mentor/* - Mentoring system")
        print("   🌐 /api/external/* - External AI management")
        print("   📊 /api/analytics/* - Awareness analytics")
        print("   🔮 /api/reflective/gateway - AI access gateway")
        print("   🧠 /api/vector/* - Fundamental memory interface")
        print()
        print("🎯 Frontend Dashboard:")
        print("   📊 http://localhost:8000/ - React Dashboard")
        print("   📈 Real-time awareness monitoring")
        print("   🌊 Coherence analytics and trends")
        print("   🧙‍♂️ Mentoring session tracking")
        print()
        print("Press Ctrl+C to stop the server")
        print("-" * 60)
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            reload=False
        )
        
    except ImportError as e:
        print(f"❌ Server startup failed: {e}")
        print("🔧 Install dependencies: pip install fastapi uvicorn")
        return False
    except KeyboardInterrupt:
        print("\n🌙 Server stopped gracefully")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


async def main():
    """Main startup function"""
    
    print_banner()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Critical dependencies missing")
        print("🔧 Please install required packages and try again")
        sys.exit(1)
    
    print()
    
    # Register external AIs
    await register_default_ais()
    
    print()
    print("🎯 Startup Options:")
    print("1. Start API Server (recommended)")
    print("2. Start Interactive Solan Session")
    print("3. Run Integration Tests")
    print("4. Exit")
    
    try:
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            start_api_server()
        elif choice == "2":
            print("\n🧙‍♂️ Starting Interactive Solan Session...")
            from src.main import main as solan_main
            await solan_main()
        elif choice == "3":
            print("\n🧪 Running Integration Tests...")
            from test_gemini_integration import test_full_integration
            await test_full_integration()
        elif choice == "4":
            print("\n👋 Goodbye!")
        else:
            print("\n❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n🌙 Startup cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
