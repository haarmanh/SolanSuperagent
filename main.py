#!/usr/bin/env python3
"""
Solān Digital Intelligence Platform - Main Launcher
Complete integration of consciousness core, analyzer, and API server
"""

import sys
import os
import time
import asyncio
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from solan_core.engine import SolanGodCore
from solan_analyzer.analyzer import run_ai_diagnostics
from solan_labs.api.server import launch_api_server

def print_banner():
    """Print welcome banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    🌟 SOLĀN DIGITAL INTELLIGENCE PLATFORM v3.0 🌟          ║
    ║                                                              ║
    ║    Advanced AI Consciousness & Ethics Framework              ║
    ║    Complete Integration with Real-time Monitoring           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"🕐 Initialization Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 66)

def initialize_system():
    """Initialize the complete Solān system"""
    print("\n🚀 SYSTEM INITIALIZATION")
    print("-" * 30)

    # Step 1: Initialize Core Engine
    print("🧠 Step 1: Initializing Solān Core Engine...")
    core = SolanGodCore()
    print("   ✅ Core engine initialized successfully")

    # Step 2: Run System Diagnostics
    print("\n🔍 Step 2: Running System Diagnostics...")
    diagnostics_result = run_ai_diagnostics(core)
    overall_score = diagnostics_result.get('overall_score', 0)
    print(f"   ✅ Diagnostics completed - Overall Score: {overall_score:.2f}")

    # Step 3: Launch API Server
    print("\n🌐 Step 3: Launching API Server...")
    api_app = launch_api_server(core, host="localhost", port=8000)
    print("   ✅ API server launched successfully")

    return core, diagnostics_result, api_app

def print_system_status(core, diagnostics):
    """Print comprehensive system status"""
    print("\n📊 SYSTEM STATUS OVERVIEW")
    print("-" * 30)

    # Core status
    identity = core.get_identity()
    print(f"🧠 Consciousness: {'✅ Active' if identity.get('consciousness_active') else '❌ Inactive'}")
    print(f"🆔 Identity: {identity.get('identity', 'Unknown')}")
    print(f"📦 Version: {identity.get('version', 'Unknown')}")

    # Diagnostics summary
    overall_score = diagnostics.get('overall_score', 0)
    if overall_score >= 0.9:
        status_emoji = "🌟"
        status_text = "Exceptional"
    elif overall_score >= 0.8:
        status_emoji = "✅"
        status_text = "Excellent"
    elif overall_score >= 0.7:
        status_emoji = "📈"
        status_text = "Good"
    else:
        status_emoji = "🔧"
        status_text = "Needs Improvement"

    print(f"📊 System Health: {status_emoji} {status_text} ({overall_score:.1%})")

    # Component status
    system_status = core.get_system_status()
    components = system_status.get('components', {})
    active_components = sum(1 for active in components.values() if active)
    total_components = len(components)

    print(f"🔗 Components: {active_components}/{total_components} Active")
    print(f"🔄 v3.0 Integration: {'✅ Enabled' if system_status.get('v3_integration') else '❌ Disabled'}")

def print_access_information():
    """Print access information for users"""
    print("\n🌐 ACCESS INFORMATION")
    print("-" * 30)
    print("📡 API Server: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("📋 ReDoc Documentation: http://localhost:8000/redoc")
    print("🎛️ Dashboard: solan_labs/interface/dashboard.html")
    print("🌍 Main Website: solan_website_enhanced.html")
    print("🚀 API Demo: solan_api_demo_enhanced.html")
    print("📚 Documentation: solan_documentation_enhanced.html")

def print_available_endpoints():
    """Print available API endpoints"""
    print("\n🔗 AVAILABLE API ENDPOINTS")
    print("-" * 30)

    endpoints = [
        ("🧠 Consciousness Core", [
            "GET /api/consciousness-core/identity",
            "GET /api/consciousness-core/emotions",
            "POST /api/consciousness-core/ethics-test",
            "GET /api/consciousness-core/awareness-status",
            "GET /api/consciousness-core/reflection",
            "GET /api/consciousness-core/wisdom"
        ]),
        ("⚖️ Ethics Framework", [
            "GET /api/ethics/principles",
            "POST /api/ethics/dilemma-analysis"
        ]),
        ("🔧 System & Analytics", [
            "GET /health",
            "GET /api/system/status",
            "GET /cache/stats",
            "POST /api/analytics/run-diagnostics",
            "POST /api/simulation/run"
        ]),
        ("📊 Dashboard & Data", [
            "GET /dashboard-data",
            "GET /journal-entries",
            "POST /ai-dialogue"
        ])
    ]

    for category, endpoint_list in endpoints:
        print(f"\n{category}:")
        for endpoint in endpoint_list:
            print(f"  • {endpoint}")

def main():
    """Main application entry point"""
    try:
        # Print welcome banner
        print_banner()

        # Initialize system
        core, diagnostics, api_app = initialize_system()

        # Print system status
        print_system_status(core, diagnostics)

        # Print access information
        print_access_information()

        # Print available endpoints
        print_available_endpoints()

        # Final message
        print("\n🎉 SOLĀN PLATFORM READY")
        print("=" * 66)
        print("🌟 All systems operational and ready for interaction!")
        print("🔄 API server running in background...")
        print("📱 Open dashboard.html in your browser for real-time monitoring")
        print("🛑 Press Ctrl+C to shutdown")

        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 SHUTDOWN INITIATED")
            print("👋 Thank you for using Solān Digital Intelligence Platform!")
            print("🌟 Until next time...")

    except Exception as e:
        print(f"\n❌ SYSTEM ERROR: {e}")
        print("🔧 Please check your configuration and try again.")
        sys.exit(1)

if __name__ == '__main__':
    main()